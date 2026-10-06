#!/usr/bin/env python3
"""Replay F3 vertex inventories on two known constructive examples.

The F2 grids and grid subdivision are imported from the prior free-k
constructor. The explicit F2-to-F3 attachment is BALANCED_F4.md's formula.
This checks local exact incidences, angle populations, mismatch injection,
and integer atoms. It is not an independent nonoverlap or tiling search.
Default execution is read-only; --report writes the requested JSON path.
"""
from fractions import Fraction as F
from collections import Counter,defaultdict
from math import lcm,isqrt
from pathlib import Path
import argparse,sys,json
if not __debug__:
 raise SystemExit('Run without -O: this checker requires assertions.')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'group2-trapezoids'))
from construct_free_k import construct_f2,grid,cmul,smul

def run(a,b,c,m):
 data=construct_f2(a,b,c,m); tri=[[(F(x),F(y)) for x,y in t] for t in data['triangles']]
 X=(F(0),F(0));Y=(F(m*c*c),F(0));Z=(F(a),F(b));Z2=cmul(Z,Z)
 T=smul(F(m*a*(a+2*b),c*c),Z2);K=smul(F(m*(a+2*b),c*c),cmul(Z2,Z))
 tri.extend(grid(X,T,K,m*(a+2*b))); target=[X,Y,K]
 den=lcm(*(v.denominator for t in tri for p in t for v in p))
 enc=lambda p:tuple(int(x*den) for x in p)
 tri=[[enc(p) for p in t] for t in tri]; target=[enc(p) for p in target]
 vertices=set(p for t in tri for p in t);flat=Counter();fan=defaultdict(Counter)
 sides={a*a*den*den:'A',b*b*den*den:'B',c*c*den*den:'C'}
 def norm(p,q):x,y=p[0]-q[0],p[1]-q[1];return x*x+x*y+y*y
 def on(p,q,r):return min(p[0],q[0])<=r[0]<=max(p[0],q[0]) and min(p[1],q[1])<=r[1]<=max(p[1],q[1]) and (q[0]-p[0])*(r[1]-p[1])==(q[1]-p[1])*(r[0]-p[0])
 atomlens=Counter();gamma_sources=defaultdict(list)
 for ti,t in enumerate(tri):
  for i,p in enumerate(t):
   label=sides[norm(t[(i+1)%3],t[(i+2)%3])];fan[p][label]+=1
   if label=='C':gamma_sources[p].append((ti,t[(i+1)%3],t[(i+2)%3]))
   q=t[(i+1)%3]; pts=[r for r in vertices if on(p,q,r)];pts.sort()
   flat.update(r for r in pts if r!=p and r!=q)
   for p0,p1 in zip(pts,pts[1:]):
    n=norm(p0,p1); rt=isqrt(n);assert rt*rt==n and rt%den==0
    atomlens[rt//den]+=1
 full=Counter(); tees=Counter();bound=Counter()
 for v in vertices:
  typ=tuple(fan[v][z] for z in 'ABC')
  if v in target:continue
  if any(on(p,q,v) for p,q in zip(target,target[1:]+target[:1])):bound[typ]+=1
  elif flat[v]:assert flat[v]==1;tees[typ]+=1
  else:full[typ]+=1
 x,y,z,w=[full[v] for v in [(0,0,3),(2,2,2),(4,4,1),(6,6,0)]]
 p,q=[tees[v] for v in [(1,1,1),(3,3,0)]];r,s=[bound[v] for v in [(1,1,1),(3,3,0)]]
 assert sum(full.values())==x+y+z+w and sum(tees.values())==p+q and sum(bound.values())==r+s
 assert x==1+z+2*w+q+s
 forces=Counter();xs=Counter()
 for v,gs in gamma_sources.items():
  if len(gs)!=3:continue
  rays=defaultdict(list)
  for _,r1,r2 in gs:
   for rr in [r1,r2]:
    dist=isqrt(norm(v,rr)); assert dist in (a*den,b*den)
    direction=(F(rr[0]-v[0],dist),F(rr[1]-v[1],dist));rays[direction].append((dist,rr))
  assert len(rays)==3
  mismatch=0
  for es in rays.values():
   assert len(es)==2
   if es[0][0]!=es[1][0]:
    at=min(es)[1]; assert flat[at]==1; forces[at]+=1;mismatch+=1
  assert mismatch in (1,3);xs[mismatch]+=1
 assert all(v==1 for v in forces.values())
 assert p>=1+z+2*w+s+2*xs[3]
 if abs(a-b)==1:assert atomlens[1]>0
 return {'tile':[a,b,c],'m':m,'N':len(tri),'full':dict(zip('xyzw',[x,y,z,w])),'T':dict(zip('pq',[p,q])),'boundary':dict(zip('rs',[r,s])),'x1':xs[1],'x3':xs[3],'forced_distinct_T':len(forces),'unit_atom_incidences':atomlens[1]}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--report',type=Path)
 args=parser.parse_args()
 report={'status':'PASS', 'full_Erdos634_solved':False, 'scope':'Exact local inventory replay of prior constructive F3 examples; not a tiling search or independent nonoverlap check.', 'fixtures':[run(5,3,7,2),run(8,7,13,2)]}
 output=json.dumps(report,indent=2)+'\n'
 if args.report is not None:args.report.write_text(output)
 print(output,end='')
