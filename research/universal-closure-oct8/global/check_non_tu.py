#!/usr/bin/env python3
from pathlib import Path
import json
from math import gcd

def require(ok,message):
 if not ok:raise RuntimeError(message)
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]
def segment_inside(p,q,a,b):
 v=sub(b,a)
 if cross(v,sub(p,a)) or cross(v,sub(q,a)):return False
 return all(min(a[i],b[i])<=r[i]<=max(a[i],b[i])for r in [p,q]for i in [0,1])
triangles=[[(70,70),(91,70),(35,105)],[(73,70),(94,70),(38,105)],[(65,75),(86,75),(30,110)]]
rows=[((80,70),(81,70)),((60,80),(61,79)),((62,90),(70,85))]
for tri in triangles:
 require(cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]))==735,'orientation/area')
 require(sorted(norm(sub(a,b))for a,b in zip(tri,tri[1:]+tri[:1]))==[441,1225,2401],'congruence')
 require(all(x>=0 and y>=0 and x+y<=210 for x,y in tri),'containment')
M=[]
for p,q in rows:
 require(gcd(*sub(q,p))==1,'row is not a primitive lattice atom')
 row=[]
 for tri in triangles:
  entries=[]
  for a,b in zip(tri,tri[1:]+tri[:1]):
   if segment_inside(p,q,a,b):
    e=sub(b,a);r=sub(q,p);entries.append(1 if e[0]*r[0]+e[1]*r[1]>0 else -1)
  require(len(entries)<=1,'duplicate edge')
  row.append(sum(entries))
 M.append(row)
a,b,c=M[0];d,e,f=M[1];g,h,i=M[2];det=a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
require(M==[[1,1,0],[1,0,1],[0,-1,-1]] and det==2,'wrong minor')
require(all(sum(row)==2*rhs for row,rhs in zip(M,[1,1,-1])),'fractional three-row solution')
out=dict(status='PASS',denominator=7,tile=[3,5,7],target_side=30,complete_band=[-1,1],triangles=triangles,atomic_rows=rows,matrix=M,determinant=det,special_triangular_rhs_integrality_decided=False)
Path(__file__).with_name('non_tu_verified.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
