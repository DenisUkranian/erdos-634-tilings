"""Independent transcriptions of the written W construction and its two inputs.
Tests macro intersections by rational clipping, not positioned currents.
Finite regression plus separate exact symbolic identities; not Lean.
"""
from fractions import Fraction as F
from math import gcd
from itertools import combinations
from pathlib import Path
import json,time,sys
from exact_geometry import *
ROOT=Path(__file__).resolve().parents[1]

def require(c,msg):
 if not c:raise ValueError(msg)

def norm(x,u,v):
 P=3*v*v-u*u
 return v*v*(x[0]*x[0]+x[1]*x[1])+F(u*P,v)*x[0]*x[1]
def normdiag(x,D):return x[0]*x[0]+D*x[1]*x[1]
def norms(poly,f):return sorted(f(sub(a,b)) for a,b in zip(poly,poly[1:]+poly[:1]))

def seed_macro(u,v,t):
 b=v*v-u*u;d=v-u;m=v+t;w=u+t;K=v*m-u*w
 e=p(F(v**3,b),-F(u*v*v,b));e2=mul(F(u,v),e);s2=p(-u,v)
 X=p(0,0);O=mul(u*m,e);A=p(-u*v*m,u*u*m);C=p(-u*v*m,v*v*m)
 Q0=p(u*b,0);S=add(Q0,mul(u*t,s2));P0=add(Q0,mul(u*t,e));R0=add(S,mul(d*t,e2));V=p(-u*u*w,u*v*w)
 target=ccw([O,A,C]);macros=[ccw([O,X,Q0,P0]),ccw([P0,Q0,S,R0]),ccw([R0,V,C])]
 # Decompose the nonconvex H by its actual horizontal breakpoints.
 cuts=[0,u*v*t,u*u*m,u*v*w,v*v*m]
 def left(y):return -F(v,u)*y if y<=u*u*m else F(-u*v*m)
 def right(y):
  if y<=u*v*t:return u*b-F(u,v)*y
  if y<=u*v*w:return b*w-F(v,u)*y
  return -F(u,v)*y
 hs=[ccw([p(left(y0),y0),p(right(y0),y0),p(right(y1),y1),p(left(y1),y1)]) for y0,y1 in zip(cuts,cuts[1:])]
 Q=2*v*v-u*u
 require(norms(target,lambda x:norm(x,u,v))==sorted(x*x for x in (m*v**3,m*u*Q,m*v*b)),'target metric')
 for tr,L,basis in [(macros[2],K,None)]:
  require(norms(tr,lambda x:norm(x,u,v))==sorted(L*L*x*x for x in (u*v,b,v*v)),'third macro metric')
 pieces=macros+hs
 for piece in pieces:
  require(signed2(piece)>0,'nonpositive macro')
  require(all(inside_convex(target,x) for x in piece),'macro outside')
 count=0
 for x,y in combinations(pieces,2):
  require(intersect_area2(x,y)==0,'macro overlap');count+=1
 require(sum(signed2(x) for x in pieces)==signed2(target),'macro gap')
 require(signed2(target)==u*v*Q*m*m,'area count')
 # independent strip and clipping corner identities
 J=u*m//v;r=v*(J+1)-u*m
 require(t<=J<w and 1<=r<=v,'kink range')
 for j in range(t):
  qj=(d-1)*u+d*j;W=u*b+b*j-u*u
  require(W==u*(v+qj)+v*qj and qj>=0,'lower width')
 q=(d-1)*u+d*(t-1)
 require(b*w-v*v==u*(v+q)+v*q and q>=0,'middle width')
 for j in range(J+1,w):
  W=b*w+u*v*m-v*v*(j+1)
  require(W==u*K+v*v*(w-1-j) and W>0,'clipped width')
 Fj=p(-v*v*(J+1),u*v*(J+1))
 require(add(Fj,p(v*r,-u*r))==A,'removed corner endpoint')
 require(add(Fj,p(v*r,0))[0]==A[0],'cut vertical endpoint')
 P=3*v*v-u*u;B=add(O,mul(F(P,Q),sub(A,O)));extra=ccw([A,B,C]);bt=ccw([O,B,C])
 require(norms(extra,lambda x:norm(x,u,v))==sorted((v*m*x)**2 for x in (u*v,b,v*v)),'beta attachment metric')
 require(intersect_area2(target,extra)==0 and signed2(target)+signed2(extra)==signed2(bt),'beta lift partition')
 require(norms(bt,lambda x:norm(x,u,v))==sorted(x*x for x in (m*v**3,m*v**3,m*u*P)),'beta target')
 return {'pieces':len(pieces),'intersection_checks':count+1,'J':J,'r':r,'u':u,'v':v,'t':t}

def old_seed(u,v):
 b=v*v-u*u;c=v*v;Q=2*v*v-u*u;D=4*v*v-u*u;a=u*v
 O=p(0,0);A=p(b*b,0);C=p(-F(u*u*b,2),F(u*b,2));D0=p(C[0],-C[1]);E=p(-F(u*u*Q,2),-F(u**3,2));B=add(D0,E)
 target=ccw([A,C,B]);pieces=[ccw(x) for x in ([O,A,C],[O,A,D0],[O,C,E],[O,D0,B,E])]
 f=lambda x:normdiag(x,D)
 for tri,L in zip(pieces[:3],(b,b,a)):require(norms(tri,f)==sorted((L*s)**2 for s in (a,b,c)),'seed triangle metric')
 cellf=mul(F(1,b),D0);cellg=mul(F(1,u*u),E)
 require(sorted([f(cellf),f(cellg),f(sub(cellf,cellg))])==sorted(s*s for s in (a,b,c)),'seed cell metric')
 for piece in pieces:
  require(all(inside_convex(target,x) for x in piece),'seed containment')
 for x,y in combinations(pieces,2):require(intersect_area2(x,y)==0,'seed overlap')
 require(sum(signed2(x) for x in pieces)==signed2(target),'seed coverage')
 require(norms(target,f)==sorted(s*s for s in (v**4,u*v*Q,v*v*b)),'seed target')
 return 6

def cap(u,v,T):
 b=v*v-u*u;c=v*v;Q=2*v*v-u*u;P=3*v*v-u*u;D=4*v*v-u*u;a=u*v
 k=u*v;h=u*(v-u);q=u*u;L0=h*b
 pv=p(u*v,0);wv=p(-F(u*P,2*v),F(b,2*v));r=p(F(u*Q,2*v),F(u*u,2*v));s=p(-F(u*b,2*v),F(b,2*v))
 O=p(0,0);K=p(u*v**3,0);R=mul(b,r);J=mul(h,add(r,s));C=add(K,mul(h,pv));E=add(R,mul(h,s));B=sub(E,p(L0,0));X=mul(h,r);Y=add(C,mul(q,wv))
 pieces=[ccw(x) for x in ([O,K,R],[J,B,E],[O,X,J],[X,R,E,J],[K,C,Y,R],[R,Y,E])]
 outer=ccw([O,C,E,B]);f=lambda x:normdiag(x,D)
 for piece in pieces:
  require(signed2(piece)>0 and all(inside_convex(outer,z) for z in piece),'cap containment')
 for x,y in combinations(pieces,2):require(intersect_area2(x,y)==0,'cap overlap')
 require(sum(signed2(x) for x in pieces)==signed2(outer),'cap coverage')
 for tri,L in ((pieces[0],k),(pieces[1],h),(pieces[2],h),(pieces[5],h)):
  require(norms(tri,f)==sorted((L*x)**2 for x in (a,b,c)),'cap metric')
 L=u*Q*T-L0;require(L==a*(v*T)+b*u*(T-v+u) and T>=v-u,'collar width')
 shift=p(L,0);shifted=[add(z,shift) for z in outer];par=ccw([O,shift,add(shift,B),B])
 G=p(F(u*b*(T+u),2),F(b*(T+u),2));target=ccw([O,p(u*Q*(T+u),0),G]);inner=ccw([B,add(B,p(u*Q*T,0)),G])
 require(intersect_area2(shifted,par)==0,'collar overlap')
 require(intersect_area2(shifted,inner)==0 and intersect_area2(par,inner)==0,'collar intersects old tiling')
 require(sum(abs(signed2(z)) for z in [shifted,par,inner])==signed2(target),'collar coverage')
 require(norms(target,f)==sorted(((T+u)*x)**2 for x in (v*b,v**3,u*Q)),'collar outer metric')
 require(norms(inner,f)==sorted((T*x)**2 for x in (v*b,v**3,u*Q)),'collar inner metric')
 require((u**4+2*u*v*b)+2*L==Q*((T+u)**2-T*T),'collar count')
 return 18

def symbolic():
 import sympy as s
 u,v,t,j=s.symbols('u v t j',positive=True);b=v*v-u*u;d=v-u;m=v+t;w=u+t;K=v*m-u*w;Q=2*v*v-u*u;P=3*v*v-u*u
 identities={
 'K factor':K-d*(u+v+t),
 'lower width':u*b+b*j-u*u-(u*(v+(d-1)*u+d*j)+v*((d-1)*u+d*j)),
 'middle width':b*w-v*v-(u*(v+(d-1)*u+d*(t-1))+v*((d-1)*u+d*(t-1))),
 'clipped width':b*w+u*v*m-v*v*(j+1)-(u*K+v*v*(w-1-j)),
 'count':u*u*(m*m-t*t)+t*t*(v*v-d*d)+K*K+b*(t*t+2*t*(u+v)+u*u+v*v)-Q*m*m,
 'beta count':Q+v*v-P,
 'first gap':u*u*m-u*v*t-u*(u*v-d*t),
 'second gap':u*v*w-u*u*m-u*d*t,
 'third gap':v*v*m-u*v*w-v*K,
 'seed count':2*b*b+(u*v)**2+2*b*u*u-v*v*Q,
 }
 for label,x in identities.items():require(s.factor(x)==0,('symbolic',label))
 x,y,z=s.symbols('x y z',nonnegative=True)
 subdom={u:x+y+2,t:y+1,v:x+y+z+3}
 signs={'first height gap':u*u*m-u*v*t,'second height gap':u*v*w-u*u*m,'third height gap':v*v*m-u*v*w,'K':K,'q_middle':(d-1)*u+d*(t-1)}
 cert={}
 for name,e in signs.items():
  poly=s.Poly(s.expand(e.subs(subdom,simultaneous=True)),x,y,z)
  require(all(c>=0 for c in poly.coeffs()) and poly.as_expr()!=0,('nonnegative',name));cert[name]=str(poly.as_expr())
 return {'identities':len(identities),'nonnegative_polynomials':cert}

def main():
 started=time.monotonic();pairs=[(u,v) for v in range(3,14) for u in range(2,v) if gcd(u,v)==1]
 seeds=[(u,v,t) for u,v in pairs for t in range(1,u)]
 seeds.extend([(2,101,1),(2,1009,1),(7,1009,1),(7,1009,6),(99,100,1),(99,100,98),(4,6,1),(4,6,3),(12,18,5)])
 records=[seed_macro(*x) for x in seeds]
 pp=[(u,v) for v in range(2,13) for u in range(1,v) if gcd(u,v)==1]+[(2,101),(7,1009),(99,100),(4,6)]
 old=sum(old_seed(*p) for p in pp)
 caps=sum(cap(u,v,T) for u,v in pp for T in (v-u,v,v+u))
 report={'status':'PASS','seed_parameter_cases':len(records),'seed_convex_intersection_tests':sum(z['intersection_checks'] for z in records),'seed_macropieces_checked':sum(z['pieces'] for z in records),'old_seed_parameter_cases':len(pp),'old_seed_intersections':old,'cap_cases':3*len(pp),'cap_intersections':caps,'symbolic':symbolic(),'seconds':round(time.monotonic()-started,3),'new_checker':'independent rational polygon clipping; no import of project constructor or validator','scope':'sampled macro geometry plus symbolic algebra and separately written universal proof; not full theorem formalization'}
 (ROOT/'results'/'universal_geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
