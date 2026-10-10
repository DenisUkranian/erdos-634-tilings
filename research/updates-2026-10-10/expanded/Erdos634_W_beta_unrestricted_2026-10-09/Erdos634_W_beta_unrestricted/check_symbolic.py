#!/usr/bin/env python3
"""Exact algebraic checks of the NEW proof. Not a formal geometry proof.
The identities are universal; the separate integer loop is a regression only.
"""
from pathlib import Path
import json, time
import sympy as sp

if not __debug__: raise RuntimeError('Do not run with -O')
u,v,t,j,J,r = sp.symbols('u v t j J r')
b=v*v-u*u;d=v-u;m=v+t;w=u+t;K=b+d*t;Q=2*v*v-u*u;P=3*v*v-u*u
add=lambda x,y:tuple(a+b for a,b in zip(x,y))
sub=lambda x,y:tuple(a-b for a,b in zip(x,y))
scale=lambda k,x:tuple(k*a for a in x)
det=lambda x,y:x[0]*y[1]-x[1]*y[0]
norm=lambda x:v*v*(x[0]**2+x[1]**2)+u*P*x[0]*x[1]/v
s=(b/v,0);e=(v**3/b,-u*v*v/b);s2=(-u,v);e2=scale(u/v,e)
X=(0,0);O=scale(u*m,e);A=(-u*v*m,u*u*m);C=(-u*v*m,v*v*m)
Q0=(u*b,0);S=add(Q0,scale(u*t,s2));P0=add(Q0,scale(u*t,e));R0=add(S,scale(d*t,e2))
V=(-u*u*w,u*v*w)
proof=[]
def eq(name,lhs,rhs=0):
    z=sp.factor(lhs-rhs)
    if z!=0: raise AssertionError((name,z))
    proof.append(name)
def veq(name,lhs,rhs):
    for k in range(2):eq(name+f'[{k}]',lhs[k],rhs[k])
for name,vec,length in [('A0 leg a',(u,0),u*v),('A0 leg c',(0,v),v*v),('A0 diagonal',(-u,v),b),
 ('B0 leg c',(v,0),v*v),('B0 leg a',(0,u),u*v),('B0 diagonal',(-v,u),b),
 ('s',s,b),('e',e,v*v),('e-s',sub(e,s),u*v),('s2',s2,b),('e2',e2,u*v),('e2-s2',sub(e2,s2),v*v)]:
 eq('metric '+name,norm(vec),length**2)
eq('Gram determinant',v**4-u*u*P*P/(4*v*v),b*b*(4*v*v-u*u)/(4*v*v))
veq('C=V+K*s2',C,add(V,scale(K,s2)))
veq('R0=V+K*e2',R0,add(V,scale(K,e2)))
veq('S=V+b*e2',S,add(V,scale(b,e2)))
veq('OP0 direction/order',sub(O,P0),scale(u*v,sub(e,s)))
veq('P0R0 direction/order',sub(P0,R0),scale(u*t,sub(e2,s2)))
veq('R0C direction/order',sub(R0,C),scale(K,sub(e2,s2)))
veq('OA line/order',sub(O,A),scale(u*Q*m/(v*v),e))
for name,pair,length in [('OA',(O,A),u*Q*m),('OC',(O,C),v**3*m),('AC',(A,C),v*b*m)]:
 eq('target '+name,norm(sub(*pair)),length**2)
qj=(d-1)*u+d*j
q1=(d-1)*u+d*(t-1)
eq('lower nonnegative width',u*b+b*j-u*u,u*(v+qj)+v*qj)
eq('full middle width',b*w-v*v,u*(v+q1)+v*q1)
eq('clipped middle width',b*w+u*v*m-v*v*(j+1),u*K+v*v*(w-1-j))
eq('K=vm-uw',K,v*m-u*w)
F=(-v*v*(J+1),u*v*(J+1));rr=v*(J+1)-u*m
veq('clipped corner x endpoint',add(F,(v*rr,0)),(-u*v*m,u*v*(J+1)))
veq('clipped corner lower endpoint',add(F,(v*rr,-u*rr)),A)
eq('top triangle vertical leg',v*v*m-u*v*w,v*K)
eq('top triangle horizontal leg',u*v*m-u*u*w,u*K)
H=[X,A,C,V,S,Q0]
a2=sum(det(H[i],H[(i+1)%len(H)]) for i in range(len(H)))
NH=b*(t*t+2*t*(u+v)+u*u+v*v)
eq('hexagon signed area',a2,-u*v*NH)
Nc=u*u*(m*m-t*t)+t*t*(v*v-d*d)+K*K
eq('total tile count',Nc+NH,Q*m*m)
Bstar=add(O,scale(P/Q,sub(A,O)))
for name,vec,L in [('extension AC',sub(A,C),v*m*b),('extension ABstar',sub(A,Bstar),v*m*u*v),('extension CBstar',sub(C,Bstar),v*m*v*v)]:
 eq('beta '+name,norm(vec),L*L)
eq('beta count',Q+v*v,P)
# Signs without numerically sampling p,q,h: expand in the entire nonnegative cone.
x,y,z=sp.symbols('x y z',nonnegative=True)
# u=x+y+2, t=y+1, v=u+z+1 parametrizes u>=2, 1<=t<u, v>u.
param={u:x+y+2,t:y+1,v:x+y+z+3}
sign_polys={'b':b,'d':d,'m':m,'w':w,'K':K,'m-t':m-t,'v-d':v-d,
 'kink above lower':u*m-v*t,'kink below top':v*w-u*m,
 'top gap':v*m-u*w,'full width':b*w-v*v,
 'first annulus count':u*u*(m*m-t*t),'second annulus count':t*t*(v*v-d*d),
 'residual count':NH}
for name,p in sign_polys.items():
 pp=sp.Poly(sp.expand(p.subs(param, simultaneous=True)),x,y,z)
 assert all(c>=0 for c in pp.coeffs()) and any(c>0 for c in pp.coeffs()),name
# Finite regression, deliberately not used as a premise of the universal proof.
pairs=seeds=width_checks=0;minratio=None;maxratio=0.0
for U in range(2,36):
 for Vv in range(U+1,4*U+41):
  pairs+=1;B=Vv*Vv-U*U;dd=Vv-U
  for T in range(1,U):
   seeds+=1;M=Vv+T;W=U+T;kk=B+dd*T;jj=U*M//Vv;rr=Vv*(jj+1)-U*M
   assert T<=jj<W and 1<=rr<=Vv
   for j0 in range(T):
    q0=(dd-1)*U+dd*j0
    assert q0>=0 and U*B+B*j0-U*U==U*(Vv+q0)+Vv*q0
    width_checks+=1
   q0=(dd-1)*U+dd*(T-1)
   assert q0>=0 and B*W-Vv*Vv==U*(Vv+q0)+Vv*q0
   width_checks+=1
   for j0 in range(jj+1,W):
    ww=B*W+U*Vv*M-Vv*Vv*(j0+1)
    assert ww==U*kk+Vv*Vv*(W-1-j0)>0
    width_checks+=1
report={'status':'PASS','universal_symbolic_identities':len(proof),'identity_names':proof,
 'universal_nonnegative_coefficient_sign_checks':len(sign_polys),
 'regression_parameter_pairs':pairs,'regression_residue_seeds':seeds,'regression_rectangle_checks':width_checks,
 'regression_range':'2<=u<=35, u<v<=4u+40, every 1<=t<u; includes nonprimitive pairs',
 'geometric_forcing_formally_verified':False,'all_parameter_proof':'PROOF.md',
 'full_Erdos634_solved':False}
Path('symbolic_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='identity_names'},indent=2))
