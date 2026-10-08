#!/usr/bin/env python3
"""Independent physical-frame comparison of complete reduced135 dictionaries."""
from pathlib import Path
import argparse,json,hashlib,struct
D=7**8
ROOTS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
def need(ok,message):
 if not ok:raise RuntimeError(message)
def mul(u,v):return(u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1])
def power(u,n):
 r=(1,0)
 for _ in range(n):r=mul(r,u)
 return r

def load(prefix):
 j=json.loads(Path(prefix+'.json').read_text());L,U=j['L'],j['U'];rotation=j['basis_rotation']
 frame=mul(mul(power((2,1),-L),power((3,-1),U)),ROOTS[rotation]);a,b=frame;n=a*a+a*b+b*b
 need(D%n==0,'incompatible denominator')
 offsets=[]
 for h in range(L,U+1):
  znum=power((3,5)if h>=0 else(8,-5),abs(h));zd=7**abs(h)
  need(D%zd==0,'height denominator')
  z=(znum[0]*(D//zd),znum[1]*(D//zd))
  for reverse in [False,True]:
   for rot in range(6):
    u=mul(z,ROOTS[rot]);v=mul(u,(-1,1));aa,bb=(5,3)if reverse else(3,5)
    offsets.append(((0,0),(aa*u[0],aa*u[1]),(bb*v[0],bb*v[1])))
 pool=set()
 with open(prefix+'.remaining.txt')as f:
  lo,hi,count=map(int,next(f).split());need((lo,hi,count)==(L,U,j['remaining']),'pool header')
  for line in f:
   t,x,y=map(int,line.split());need(0<=t<len(offsets),'template index')
   # Invert the real two-coordinate transformation matrix directly.
   px=((a+b)*x+b*y)*(D//n);py=(-b*x+a*y)*(D//n)
   tri=tuple(sorted((px+u,py+v)for u,v in offsets[t]))
   need(all(u>=0 and v>=0 and u+v<=45*D for u,v in tri),'physical containment')
   need(tri not in pool,'duplicate physical triangle');pool.add(tri)
 need(len(pool)==count,'pool length')
 return pool

def digest(pool):
 h=hashlib.sha256()
 for tri in sorted(pool):h.update(struct.pack('<6q',*(x for p in tri for x in p)))
 return h.hexdigest()

def main():
 here=Path(__file__).resolve().parent
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--manifest',type=Path,default=here.parent/'e135/all_k9_normalized.json')
 parser.add_argument('--output',type=Path,default=here/'e135_pool_embedding_verified.json')
 args=parser.parse_args()
 reference_report=json.loads(args.manifest.read_text())
 ref=load(reference_report['reference_prefix']);refhash=digest(ref)
 need(len(ref)==246600 and refhash==reference_report['reference_sha256'],'reference normalization mismatch')
 reflection=lambda t:tuple(sorted((y,x)for x,y in t))
 need(all(reflection(t)in ref for t in ref),'reference not reflection invariant')
 records=[]
 for entry in reference_report['pools']:
  pool=load(entry['prefix']);need(pool<=ref,'pool is not contained')
  need(all(reflection(t)in ref for t in pool),'reflected pool is not contained')
  hashed=digest(pool);need(hashed==entry['normalized_sha256'],'pool normalization mismatch')
  records.append(dict(prefix=entry['prefix'],count=len(pool),sha256=hashed,subset_of_reference=True,reflected_subset_of_reference=True))
 out=dict(status='PASS',reference_count=len(ref),reference_sha256=refhash,
          independent_physical_templates=True,direct_inverse_coordinate_matrix=True,records=records)
 args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
