from fractions import Fraction as F
from itertools import permutations
from math import isqrt
def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(k,p):return k*p[0],k*p[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(P):return sum(det(p,q) for p,q in zip(P,P[1:]+P[:1]))
def clip(P,Q):
 for A,B in zip(Q,Q[1:]+Q[:1]):
  U=[]; v=sub(B,A)
  for p,q in zip(P,P[1:]+P[:1]):
   d=det(v,sub(p,A));e=det(v,sub(q,A))
   if d>=0:U.append(p)
   if d*e<0:U.append(add(p,mul(d/(d-e),sub(q,p))))
  P=U
 return P
from pathlib import Path
def N(p):return p[0]**2+p[1]**2+p[0]*p[1]
def L(p):
    squared=N(p)
    length=F(isqrt(squared.numerator),isqrt(squared.denominator))
    assert length*length==squared
    return length
def prod(p,q):x,y=p;u,v=q;return (x*u-y*v,x*v+y*u+y*v)
def bar(p):x,y=p;return (x+y,-y)
def triangulate(P):
 tris=[];P=P[:]
 while len(P)>3:
  for j,Y in enumerate(P):
   tr=[P[j-1],Y,P[(j+1)%len(P)]]
   if area(tr)<=0:continue
   if any(all(det(sub(y,x),sub(p,x))>=0 for x,y in zip(tr,tr[1:]+tr[:1])) for p in P if p not in tr):continue
   tris.append(tr);P.pop(j);break
  else:raise RuntimeError
 return tris+[P]
def enumerate_at(a,b,c,P,C,D,k):
 ray=mul(1/L(D),D);mesh=triangulate(P);A=[]
 for r,s,t in permutations([a,b,c]):
  ix=F(r*r+s*s-t*t-a*b,2*r);iy=F(a*b,r)
  tip=prod(ray,(ix,iy) if k==1 else bar((ix,iy)))
  T=[C,add(C,mul(r,ray)),add(C,tip)]
  if area(T)<0:T=[T[0],T[2],T[1]]
  contained=sum(area(clip(T,tri)) for tri in mesh)==a*b
  if contained:A.append((r,s,T))
 return A
if __name__=='__main__':
 if not __debug__:raise SystemExit('Run without -O.')
 table=[(34400,12986),(35905,12986),(35905,12427),(36465,12635),(38337,11270),(37882,12950),(39754,11585),(39299,13265),(36179,15540),(36634,13860),(34762,15225),(35217,13545),(34400,13545)]
 P=[(F(x,43),F(y,43)) for x,y in table];a,b,c=35,13,43
 assert area(P)==22*a*b
 A=enumerate_at(a,b,c,P,P[0],(F(0),F(1)),-1)
 B=enumerate_at(a,b,c,P,P[10],sub(P[11],P[10]),1)
 assert len(A)==1
 T=A[0][2]
 assert set(T)=={(800,302),(835,315),(800,315)}
 assert {(r,s) for r,s,_ in B}=={(35,43),(13,43),(43,35),(43,13)}
 possible=[(r,s,U) for r,s,U in B if area(clip(T,U))==0]
 assert len(possible)==1
 r,s,U=possible[0];assert (r,s)==(13,43)
 W=P[11];Z=U[1];assert det(sub(Z,W),sub(P[10],W))==0 and L(sub(Z,W))==22
 assert W[1]==315 and min(T[1][0],T[2][0])<W[0]<max(T[1][0],T[2][0])
 assert all(13*i+35*j+43*k!=22 for i in range(3) for j in range(2) for k in range(2))
 print('22-tile region: unique first tile, four second candidates, one after overlap, length 22 excludes it.')
