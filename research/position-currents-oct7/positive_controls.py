#!/usr/bin/env python3
"""Exact integer/rational verification for a restricted Erdős 634 result.
See PROOF.md and README.md for the complete scope and dependencies.
"""
if not __debug__:
    raise RuntimeError("Do not run this verifier with Python optimization enabled.")
from fractions import Fraction as F
from collections import defaultdict
from math import gcd
from pathlib import Path
import json
R=Path(__file__).resolve().parent
def plus(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def mul(k,p):return(k*p[0],k*p[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def rho(p):return(-p[1],p[0]+p[1])
def conj(p):return(p[0]+p[1],-p[1])
def norm(p):return p[0]**2+p[0]*p[1]+p[1]**2
def orient(T):return T if det(sub(T[1],T[0]),sub(T[2],T[0]))>0 else (T[0],T[2],T[1])
def grid(T,k,remove=0):
 O,U,V=T;u=mul(F(1,k),sub(U,O));v=mul(F(1,k),sub(V,O));out=[]
 for i in range(k):
  for j in range(k-i):
   P=plus(O,plus(mul(i,u),mul(j,v)))
   if i+j>=remove:out.append(orient((P,plus(P,u),plus(P,v))))
   if i+j<k-1 and i+j>=remove-1:out.append(orient((plus(P,u),plus(plus(P,u),v),plus(P,v))))
 return out
# Proof-based 88 construction, then conjugate to height band {0,1}.
a,b,c=3,5,7;u=(F(b),F(a));O=(F(0),F(0));A=(F(b*c),F(0));B=mul(c,u);D=(F((a+b)*c),F(0));C=mul(F(b*(2*a+b),c),u);E=plus(A,mul(F(a*b,c),u));V=plus(A,(F(0),F(b*c)))
triangles=grid((O,A,B),c)+grid((A,D,E),a)+grid((D,C,E),a)+grid((V,A,E),b,b-a)
triangles=[orient(tuple(conj(v) for v in T)) for T in triangles];P=orient(tuple(conj(v) for v in (O,D,C)))
assert len(triangles)==88
z=(F(3,7),F(5,7));dirs=set()
for h,v in [(0,(F(1),F(0))),(1,z)]:
 for j in range(6):dirs.add((v,h));v=rho(v)
levels=set()
for T in triangles:
 ns=[norm(sub(T[(i+1)%3],T[i])) for i in range(3)];assert sorted(ns)==[9,25,49]
 for i,n in enumerate(ns):
  if n in(9,25):
   v=mul(F(1,3 if n==9 else 5),sub(T[(i+1)%3],T[i]));hs=[h for v0,h in dirs if v==v0];assert len(hs)==1;levels.update(hs)
assert levels=={0,1}

def scaled(T):
 S=tuple((c*p[0],c*p[1]) for p in T)
 assert all(x.denominator==y.denominator==1 for x,y in S)
 return tuple((int(x),int(y)) for x,y in S)

def atoms(T):
 for p,q in zip(T,T[1:]+T[:1]):
  x,y=q[0]-p[0],q[1]-p[1];g=gcd(x,y);ux,uy=x//g,y//g;f=c//gcd(c,ux-2*uy);assert g%f==0
  for k in range(g//f):
   s=(p[0]+k*f*ux,p[1]+k*f*uy);t=(s[0]+f*ux,s[1]+f*uy)
   yield ((s,t),1) if s<t else ((t,s),-1)

Ts=[scaled(t) for t in triangles];PS=scaled(P)
def currents(TT):
 out=defaultdict(int)
 for T in TT:
  for e,sg in atoms(T):out[e]+=sg
 for e,sg in atoms(PS):out[e]-=sg
 return {e:v for e,v in out.items() if v}
assert not currents(Ts)
assert currents(Ts[:-1]);assert currents(Ts+[Ts[0]])
def overlap(T,S):
 for V in (T,S):
  for p,q in zip(V,V[1:]+V[:1]):
   d=sub(q,p);u=[det(d,x) for x in T];v=[det(d,x) for x in S]
   if max(u)<=min(v) or max(v)<=min(u):return False
 return True
for i,T in enumerate(Ts):
 assert all(det(sub(PS[(j+1)%3],PS[j]),sub(v,PS[j]))>=0 for j in range(3) for v in T)
 for S in Ts[:i]:assert not overlap(T,S)
assert sum(det(sub(T[1],T[0]),sub(T[2],T[0])) for T in Ts)==det(sub(PS[1],PS[0]),sub(PS[2],PS[0]))
report={'status':'EXACT_PASS','known_positive_control':88,'tile':[3,5,7],'short_heights':[0,1],'pair_checks':88*87//2,'currents':'exact boundary cancellation','rejected_controls':['missing tile','duplicated tile'],'attribution':'Reconstructed from repository research/group2-f4/PROOF.md, credits Harries 88 example; not a new 88 tiling'}
(R/'positive_controls.json').write_text(json.dumps(report,indent=2));print(report)
