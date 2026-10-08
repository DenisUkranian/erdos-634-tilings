#!/usr/bin/env python3
from pathlib import Path
import json, math
P=[(0,0),(649,0),(264,264),(0,143)]
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def mul(p,k):return(p[0]*k,p[1]*k)
def rot(p):return(-p[1],p[0]+p[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def inside(p):return all(det(sub(q,u),sub(p,u))>=0 for u,q in zip(P,P[1:]+P[:1]))
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def variants():
 out=[]
 for a,b in ((24,11),(11,24)):
  u,v=(a,0),(-b,b)
  for r in range(6):
   out.append([(0,0),u,v]);u,v=rot(u),rot(v)
 return out
V=variants();forced=[]
for u,v in zip(P,P[1:]+P[:1]):
 w=sub(v,u);n=math.gcd(*w);d=(w[0]//n,w[1]//n)
 if norm(d)!=31**2:continue
 for i in range(n):
  p,q=add(u,mul(d,i)),add(u,mul(d,i+1));fits=[]
  for T in V:
   for j in range(3):
    for k in range(3):
     if sub(T[k],T[j])!=d:continue
     shift=sub(p,T[j]);tri=[add(t,shift) for t in T]
     if all(inside(t) for t in tri):fits.append(tri)
  assert len(fits)==1,(p,q,fits)
  forced+=fits
out={'scope':'One short-edge direction class only, sufficient recipe for 4830','target':P,'forced_boundary_tiles':forced,'forced_count':len(forced),'remaining_parallelograms':(792-len(forced))//2}
if __name__=='__main__':
 Path(__file__).with_name('one_level_structure.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='forced_boundary_tiles'},indent=2))
