#!/usr/bin/env python3
"""Small independent checks of lattice coordinates, counts, and bit kernels.
No large trace replay; that is provided by the separate 154-audit verifier.
"""
from pathlib import Path
import hashlib,json,subprocess,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'154-cpsat/bitmap_zero_rotated.cpp'
OUT=Path(__file__).resolve().parent

def mul(p,q):
 a,b=p;c,d=q
 return(a*c-b*d,a*d+b*c+b*d)
def pw(p,n):
 r=(1,0)
 for _ in range(n):r=mul(r,p)
 return r
def rot(p):return(-p[1],p[0]+p[1])
def scale(k,p):return(k*p[0],k*p[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]

def counts(L,U,forced_rotation=None):
 inv=mul(pw((3,1),-L),pw((4,-1),U));opts=[]
 for rotation in range(6):
  T=[(0,0),scale(154,inv),mul(inv,(49,56))]
  xx=[p[0] for p in T];yy=[p[1] for p in T]
  opts.append((((max(xx)-min(xx)+64)//64)*(max(yy)-min(yy)+1),rotation,inv,T))
  inv=rot(inv)
 _,rotation,inv,T=(min(opts,key=lambda z:z[0]) if forced_rotation is None else opts[forced_rotation]);ns=norm(inv)
 xmin,xmax=min(p[0] for p in T),max(p[0] for p in T)
 ymin,ymax=min(p[1] for p in T),max(p[1] for p in T)
 allcounts=[];templates=[]
 for h in range(L,U+1):
  u=mul(pw((3,1),h-L),pw((4,-1),U-h))
  for _ in range(rotation):u=rot(u)
  assert norm(u)==ns
  for a,b in((8,7),(7,8)):
   v,w=scale(a,u),scale(b,rot(rot(u)))
   for r in range(6):
    tmp=[(0,0),v,w]
    assert sorted(norm(sub(tmp[(i+1)%3],tmp[i])) for i in range(3))==[49*ns,64*ns,169*ns]
    assert cross(v,w)==56*ns
    # Direct erosion halfplanes for the anchor; not the producer's
    # intersection of three precomputed shifted horizontal intervals.
    constraints=[]
    for i,p in enumerate(T):
     e=sub(T[(i+1)%3],p)
     C=max(cross(e,sub(p,t)) for t in tmp)
     constraints.append((-e[1],e[0],C))
    count=0
    for y in range(ymin,ymax+1):
     lo,hi=xmin,xmax
     for A,B,C in constraints:
      if A>0:lo=max(lo,-((B*y-C)//A))
      elif A<0:hi=min(hi,(B*y-C)//(-A))
      elif B*y<C:hi=lo-1;break
     count+=max(0,hi-lo+1)
    allcounts.append(count);templates.append(tmp)
    v,w=rot(v),rot(w)
 expected={(0,4):4759540301,(-1,3):4770414013,(-2,2):4773371018}
 assert sum(allcounts)==expected[L,U],(L,U,sum(allcounts))
 return{'L':L,'U':U,'basis_rotation':rotation,'target':T,'normscale':ns,'candidate_placements':sum(allcounts),'per_orientation_counts':allcounts,'independent_halfplane_count':'PASS'}

def bitmap_check():
 text=SOURCE.read_text();lines=text.splitlines()
 read=next(s for s in lines if s.startswith('auto read='))
 erase=next(s for s in lines if s.startswith('auto erase='))
 harness=r'''#include <vector>
#include <cstdint>
#include <iostream>
#include <cstdlib>
using namespace std;using UI=uint64_t;
struct ShiftTerm{int o,dy,q,k,sign;};
int main(){const int H=3,WP=4;vector<vector<UI>>bitmap(2,vector<UI>(H*WP));
UI state=634;auto random=[&](){state^=state<<13;state^=state>>7;state^=state<<17;return state;};
'''+read+'\n'+erase+r'''
UI cases=0;
for(int dx=-2048;dx<=2048;dx++)for(int dy=-4;dy<=4;dy++)for(int y=0;y<H;y++)for(int w=0;w<WP;w++){
 for(auto &a:bitmap)for(auto &v:a)v=random();
 int q=dx>=0?dx/64:-((-dx+63)/64),k=dx-64*q;ShiftTerm t{int(random()%2),dy,q,k,1};
 auto expected=bitmap;UI readExpected=0,removeExpected=0,mask=random();
 int yy=y+dy;
 for(int j=0;j<64;j++){
  int x=64*w+j+dx;
  if(yy<0||yy>=H||x<0||x>=64*WP)continue;
  UI bit=UI(1)<<(x%64),&value=expected[t.o][yy*WP+x/64];
  if(value&bit){readExpected|=UI(1)<<j;if((mask>>j)&1){value&=~bit;removeExpected++;}}
 }
 if(read(t,y,w)!=readExpected){cerr<<"fetch mismatch";return 1;}
 if(erase(t,y,w,mask)!=removeExpected||bitmap!=expected){cerr<<"erase mismatch";return 2;}
 cases++;
}
cout<<"{\"status\":\"PASS\",\"test_cases\":"<<cases<<",\"copied_exact_source_kernels\":true,\"undefined_behavior_sanitizer\":true}\n";
}
'''
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);(p/'check.cpp').write_text(harness)
  subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=undefined',str(p/'check.cpp'),'-o',str(p/'check')],check=True)
  result=subprocess.run([str(p/'check')],check=True,text=True,capture_output=True)
  assert not result.stderr,result.stderr
  return json.loads(result.stdout)

if __name__=='__main__':
 start=time.monotonic();bit=bitmap_check();print(json.dumps(bit),flush=True)
 rec=[]
 for L,U in((0,4),(-1,3),(-2,2)):
  x=counts(L,U,0 if(L,U)==(-2,2) else None);rec.append(x);print(json.dumps({k:v for k,v in x.items() if k!='per_orientation_counts'}),flush=True)
 report={'status':'PASS','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'unrotated_producer_sha256':hashlib.sha256((ROOT/'154-cpsat/bitmap_zero.cpp').read_bytes()).hexdigest(),'bitmap_kernels':bit,'bands':rec,'seconds':time.monotonic()-start,'large_trace_replay':'Separate 154-audit verifier; not rerun here.'}
 (OUT/'arithmetic_audit.json').write_text(json.dumps(report,indent=2)+'\n')
