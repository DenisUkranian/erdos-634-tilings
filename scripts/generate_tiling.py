#!/usr/bin/env python3
"""Exact all-parameter construction of the other-scalene Group 1 branch.

Coordinates (x,y) represent (x,y*sqrt(4v^2-u^2)). Output JSON uses one
common coordinate denominator and integer numerators. Validation uses only
integer arithmetic after generation: side norms, containment, summed area,
and pairwise separating-axis non-overlap.
"""
from fractions import Fraction as F
from math import gcd,lcm
import json,sys
if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")

P=lambda x,y:(F(x),F(y))
add=lambda x,y:(x[0]+y[0],x[1]+y[1])
sub=lambda x,y:(x[0]-y[0],x[1]-y[1])
scale=lambda x,k:(x[0]*k,x[1]*k)
cross=lambda x,y:x[0]*y[1]-x[1]*y[0]
orient=lambda a,b,c:cross(sub(b,a),sub(c,a))
def ccw(t):
 a,b,c=t
 return (a,b,c) if orient(a,b,c)>0 else (a,c,b)
def grid(V,n):
 A,B,C=V;e=scale(sub(B,A),F(1,n));f=scale(sub(C,A),F(1,n));out=[]
 for i in range(n):
  for j in range(n-i):
   p=add(A,add(scale(e,i),scale(f,j)))
   out.append(ccw((p,add(p,e),add(p,f))))
   if i+j<n-1:out.append(ccw((add(p,e),add(p,add(e,f)),add(p,f))))
 assert len(out)==n*n
 return out

def construct(u,v):
 assert 0<u<v and gcd(u,v)==1
 a=u*v;b=v*v-u*u;c=v*v;J=u*u;D=4*v*v-u*u;Q=b+c;R=b+2*c
 z=P(F(-u,2*v),F(1,2*v));z2=P(z[0]**2-D*z[1]**2,2*z[0]*z[1])
 O=P(0,0);A=P(b*b,0);C=scale(z,a*b);Dpt=P(C[0],-C[1]);E=scale(z2,a*a);B=add(Dpt,E)
 H=add(C,scale(sub(C,A),F(Q,c)))
 tiles=[]
 components=[]
 for label,tri,n in [('b_square_1',(O,A,C),b),('b_square_2',(O,A,Dpt),b),('a_square',(O,C,E),a),('Q_square',(B,C,H),Q)]:
  batch=grid(tri,n);components.append({'name':label,'first':len(tiles),'count':len(batch)});tiles+=batch
 d=scale(Dpt,F(1,b));e=scale(E,F(1,J))
 first=len(tiles)
 for i in range(b):
  for j in range(J):
   p=add(scale(d,i),scale(e,j));tiles.extend([ccw((p,add(p,d),add(p,e))),ccw((add(p,d),add(p,add(d,e)),add(p,e)))])
 components.append({'name':'parallelogram','first':first,'count':len(tiles)-first})
 target=ccw((A,B,H));den=lcm(*(x.denominator for t in tiles+[target] for p in t for x in p))
 conv=lambda t:tuple(tuple(int(x*den) for x in p) for p in t)
 return {'u':u,'v':v,'a':a,'b':b,'c':c,'D':D,'Q':Q,'P':R,'N':Q*R,'denominator':den,'target':conv(target),'tiles':[conv(t) for t in tiles],'components':components}

def verify(obj):
 a,b,c,D,N,den=[obj[k] for k in ('a','b','c','D','N','denominator')];ts=obj['tiles'];outer=obj['target']
 wanted=sorted(s*s*den*den for s in (a,b,c))
 norm=lambda p:p[0]**2+D*p[1]**2
 assert len(ts)==N
 for t in ts:
  assert orient(*t)>0
  assert sorted(norm(sub(t[i],t[(i+1)%3])) for i in range(3))==wanted
  assert all(orient(outer[i],outer[(i+1)%3],p)>=0 for p in t for i in range(3))
 assert sum(orient(*t) for t in ts)==orient(*outer)
 boxes=[(min(p[0] for p in t),max(p[0] for p in t),min(p[1] for p in t),max(p[1] for p in t)) for t in ts]
 checked=0
 for i,T in enumerate(ts):
  a0,a1,a2,a3=boxes[i]
  for j in range(i):
   b0,b1,b2,b3=boxes[j]
   if a1<=b0 or b1<=a0 or a3<=b2 or b3<=a2:continue
   U=ts[j];checked+=1
   assert any(all(orient(V[k],V[(k+1)%3],p)<=0 for p in W) for V,W in ((T,U),(U,T)) for k in range(3)),(i,j)
 return {'u':obj['u'],'v':obj['v'],'N':N,'all_squared_sides':'PASS','containment':'PASS','total_area':'PASS','pairwise_nonoverlap':'PASS','nontrivial_pairs':checked}

if __name__=='__main__':
 u,v=map(int,sys.argv[1:3]);obj=construct(u,v);result=verify(obj);print(json.dumps(result,indent=2))
 if len(sys.argv)>3:
  with open(sys.argv[3],'w',encoding='utf-8') as f:json.dump(obj,f,separators=(',',':'));f.write('\n')
