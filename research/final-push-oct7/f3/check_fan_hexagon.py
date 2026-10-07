#!/usr/bin/env python3
"""Exact replay of the symbolic fan and seven-macro positive partition.
No search, no unit-tiling existence claim for the residual hexagon.
"""
from fractions import Fraction as F
from math import isqrt,gcd
import json

def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area2(p):return sum(det(x,y)for x,y in zip(p,p[1:]+p[:1]))
def n2(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def ccw(p):return p if area2(p)>0 else list(reversed(p))
def inside(t,p):return all(det(sub(y,x),sub(p,x))>=0 for x,y in zip(t,t[1:]+t[:1]))
def separated(t,u):
 return any(all(det(sub(y,x),sub(p,x))<=0 for p in other)
            for poly,other in ((t,u),(u,t))
            for x,y in zip(poly,poly[1:]+poly[:1]))
def test(a,b,c):
 A,B=a*b,b*b
 X=(-a*a,0);Y=(2*A,-2*A-B);K=(2*A,A+2*B)
 R1=(A,-A);R2=(A+B,0);R3=(0,A)
 E0=(2*A,-2*A);E1=(A+B,-A);E2=(B,A);V=(2*A,A)
 target=ccw([X,Y,K])
 triples=([X,Y,R1],[X,R1,R2],[X,R2,R3],
          [Y,R1,E0],[R1,R2,E1],[R2,R3,E2],[R3,K,V])
 scales=(c,c,c,b,b,b,2*b)
 tt=[ccw(list(t))for t in triples]
 for t,k in zip(tt,scales):
  assert sorted(n2(sub(x,y))for x,y in zip(t,t[1:]+t[:1]))==sorted(k*k*v*v for v in (a,b,c))
  assert all(inside(target,p)for p in t)
 for i,t in enumerate(tt):
  assert all(separated(t,u)for u in tt[i+1:])
 H=ccw([E0,R1,E1,R2,E2,V])
 assert area2(target)-sum(area2(t)for t in tt)==area2(H)==2*A*(3*A-2*B)
 assert area2(H)==a*b*2*b*(3*a-2*b)
 assert sum(k*k for k in scales)+2*b*(3*a-2*b)==3*(a+b)*(a+2*b)
 return {'tile':[a,b,c],'count':3*(a+b)*(a+2*b),'hexagon_count':2*b*(3*a-2*b)}

rows=[]
for a in range(2,501):
 for b in range(1,a):
  c=isqrt(a*a+a*b+b*b)
  if c*c==a*a+a*b+b*b and gcd(a,b)==1:rows.append(test(a,b,c))
for h in (29,53,101,1001):
 a,b,c=h*h-1,2*h+1,h*h+h+1
 rows.append(test(a,b,c))
print(json.dumps({'status':'PASS','primitive_range_a_max':500,'checked':len(rows),
 'required_4830':next(r for r in rows if r['count']==4830),
 'large_ratio_cases':rows[-4:],'unrestricted_hexagon_fill':'UNRESOLVED',
 'full_Erdos634_solved':False},indent=2))
