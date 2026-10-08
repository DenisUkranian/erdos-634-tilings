#!/usr/bin/env python3
'''Exact maximal counts of unit lattice triangles inside a rotated E45/7.
The translation fundamental square is partitioned by all cell-containment
lines. No floating point enters the bound.
'''
from fractions import Fraction as F
from math import gcd,lcm,floor,ceil
from itertools import combinations
from pathlib import Path
import json,time

def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def intersect(u,v):
 a,b,c=u;d,e,f=v;det=a*e-b*d
 if not det:return None
 x=c*e-b*f;y=a*f-c*d
 if det<0:x,y,det=-x,-y,-det
 g=gcd(gcd(abs(x),abs(y)),det)
 return(x//g,y//g,det//g)
def holds(p,ineq):
 x,y,d=p;a,b,c=ineq;return a*x+b*y>=c*d
SQUARE=[(1,0,0),(-1,0,-1),(0,1,0),(0,-1,-1)]
def region_nonempty(ineq):
 return any(p is not None and all(holds(p,u) for u in ineq)
            for a,b in combinations(ineq,2) for p in [intersect(a,b)])
def normal(line):
 a,b,c=line;g=gcd(gcd(abs(a),abs(b)),abs(c));a,b,c=a//g,b//g,c//g
 if a<0 or a==0 and b<0:a,b,c=-a,-b,-c
 return(a,b,c)
def run(k):
 start=time.monotonic();v=(F(45,7),F(0))
 for _ in range(k):v=mul(v,(F(8,7),F(-5,7)))
 target=[(F(0),F(0)),v,mul(v,(0,1))];D=lcm(*(q.denominator for p in target for q in p));P=[(int(x*D),int(y*D))for x,y in target]
 cells=[];lines=set(map(normal,SQUARE))
 for i in range(floor(min(p[0] for p in target))-2,ceil(max(p[0] for p in target))+2):
  for j in range(floor(min(p[1] for p in target))-2,ceil(max(p[1] for p in target))+2):
   for typ,offs in [(0,[(0,0),(1,0),(0,1)]),(1,[(1,0),(1,1),(0,1)])]:
    tri=[(i+x,j+y)for x,y in offs];ine=[]
    for A,B in zip(P,P[1:]+P[:1]):
     e=sub(B,A);ine.append((-D*e[1],D*e[0],cross(e,A)-D*min(cross(e,q)for q in tri)))
    if not region_nonempty(ine+SQUARE):continue
    cells.append((typ,i,j,ine));lines.update(map(normal,ine))
 points=set()
 for a,b in combinations(sorted(lines),2):
  p=intersect(a,b)
  if p is not None and 0<=p[0]<=p[2] and 0<=p[1]<=p[2]:points.add(p)
 best=-1;witness=None;maxes=[0,0];hist={}
 for p in points:
  cnt=[0,0]
  for typ,i,j,ineq in cells:
   if all(holds(p,u)for u in ineq):cnt[typ]+=1
  maxes=[max(x,y)for x,y in zip(maxes,cnt)];value=min(cnt)
  hist[tuple(cnt)]=hist.get(tuple(cnt),0)+1
  if value>best:best=value;witness=dict(translation=p,counts=cnt)
 return dict(k=k,target_numerators=P,target_denominator=D,potential_cells=len(cells),lines=len(lines),arrangement_vertices=len(points),maximum_balanced_pairs=best,individual_maxima=maxes,witness=witness,tail98_excluded=(best<15),seconds=time.monotonic()-start)
if __name__=='__main__':
 out=[]
 for k in [1,2,3]:
  r=run(k);out.append(r);print(json.dumps(r),flush=True)
 Path(__file__).with_name('cell_bound_checked.json').write_text(json.dumps(dict(status='EXACT_FINITE_CELL_CONTAINMENT',records=out),indent=2)+'\n')
