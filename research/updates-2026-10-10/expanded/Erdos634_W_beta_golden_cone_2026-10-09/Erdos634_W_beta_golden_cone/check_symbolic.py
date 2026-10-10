#!/usr/bin/env python3
"""Exact symbolic identities and bounded arithmetic regression.
This is not a proof-assistant formalization of the geometric argument.
"""
if not __debug__:
    raise RuntimeError('Assertions must be enabled; do not run with python -O')

import json
from collections import defaultdict
from math import gcd
from pathlib import Path
import sympy as S

def symbolic():
    u,v,t,j=S.symbols('u v t j')
    b=v*v-u*u;d=v-u;m=v+t;Q=2*v*v-u*u;P=3*v*v-u*u
    Vc=lambda x,y:S.Matrix([x,y])
    cr=lambda p,q:S.det(S.Matrix.hstack(p,q))
    simple=lambda x:S.factor(S.cancel(x))
    labels=[]
    def eq(label,l,r=0):
        assert simple(l-r)==0,(label,simple(l-r));labels.append(label)
    def veq(label,L,R):
        eq(label+' x',L[0],R[0]);eq(label+' y',L[1],R[1])
    def norm(p):
        x,y=p;return v*v*(x*x+y*y)+u*P/v*x*y
    s=Vc(b/v,0);e=Vc(v**3/b,-u*v*v/b);s2=Vc(-u,v);e2=u/v*e
    O=u*m*e;X=Vc(0,0);A=Vc(-u*v*m,u*u*m);C=Vc(-u*v*m,v*v*m)
    V=Vc(-u*u*m,u*v*m);q0=Vc(u*b,0);SS=Vc(u*b-u*u*t,u*v*t)
    p0=q0+u*t*e;r0=SS+d*t*e2;R=Vc(-u*u*v+b*(t-d),u*v*v)
    U=Vc(-u*u*v+b*t,u*v*v);t0=V+d*m*e2
    for name,vec,n in [('s',s,b*b),('e',e,v**4),('e-s',e-s,u*u*v*v),
                       ('s2',s2,b*b),('e2',e2,u*u*v*v),('e2-s2',e2-s2,v**4),
                       ('A-grid-u',Vc(u,0),u*u*v*v),('A-grid-v',Vc(0,v),v**4),
                       ('A-grid-third',Vc(u,-v),b*b),('B-grid-third',Vc(v,-u),b*b)]:
        eq('metric '+name,norm(vec),n)
    eq('Gram determinant',v**4-(u*P/(2*v))**2,b*b*(4*v*v-u*u)/(4*v*v))
    for name,vec,n in [('OA',O-A,(u*Q*m)**2),('OC',O-C,(v**3*m)**2),('AC',A-C,(v*b*m)**2)]:
        eq('outer side '+name,norm(vec),n)
    veq('third annulus',r0,R+(b-d*t)*e)
    veq('third-fourth join',t0,U+d*(u-t)*e)
    polys=[[O,X,q0,p0],[p0,q0,SS,r0],[r0,R,U,t0],[t0,V,C],[X,A,C,V,U,R,SS,q0]]
    area=lambda p:sum(cr(p[i],p[(i+1)%len(p)]) for i in range(len(p)))
    counts=[u*u*(m*m-t*t),v*v*t*t-d*d*t*t,(b-d*t)**2-d*d*(u-t)**2,d*d*m*m,b*(2*u*v+4*v*t+t*t)]
    for i,(poly,n) in enumerate(zip(polys,counts)):eq(f'macro signed area {i}',area(poly),-u*v*n)
    eq('whole count',sum(counts),Q*m*m)
    # Oriented endpoint-event equality on exact affine supporting lines.
    # These derivatives of signed interval currents retain positions.
    events=defaultdict(int)
    def add_poly(poly,sgn):
        for i,a in enumerate(poly):
            bb=poly[(i+1)%len(poly)]
            aa=simple(bb[1]-a[1]);bbb=simple(a[0]-bb[0]);cc=simple(bb[0]*a[1]-a[0]*bb[1])
            divisor=aa if aa!=0 else bbb
            line=tuple(str(simple(k/divisor)) for k in (aa,bbb,cc))
            point=lambda p:tuple(str(simple(k)) for k in p)
            events[line+point(a)]+=sgn;events[line+point(bb)]-=sgn
    for poly in polys:add_poly(poly,1)
    add_poly([O,A,C],-1)
    assert all(val==0 for val in events.values())
    labels.append('full positioned boundary cancellation')
    # All rectangle identities used in the written nonnegative decompositions.
    K0=(d-1)*u+d*j
    eq('lower rectangle',u*b+b*j-u*u,u*(v+K0)+v*K0)
    K1=(d-1)*u+d*(t-1)
    eq('middle full rectangle',b*(u+t)-v*v,u*(v+K1)+v*K1)
    K2=d*m-v
    eq('upper full rectangle',b*m-v*v,u*(v+K2)+v*K2)
    delta=u*u+u*v-v*v;omega=d*delta+b+u*v
    eq('omega identity',omega,u*v+d*(delta+u+v))
    eq('middle clipped width',b*(u+t)+u*v*m-v*v*(j+1),omega+(t-1)*(b+u*v)+v*v*(v-1-j))
    eq('upper clipped width',b*m+u*v*m-v*v*(j+1),u*d*m+v*v*(m-j-1))
    rr=v*(j+1)-u*m
    veq('clipped corner upper endpoint',Vc(-v*v*(j+1)+v*rr,u*v*(j+1)),Vc(-u*v*m,u*v*(j+1)))
    veq('clipped corner lower endpoint',Vc(-v*v*(j+1)+v*rr,u*v*(j+1)-u*rr),A)
    betaB=O+P/Q*(A-O)
    eq('beta extra side',norm(betaB-C),(m*v**3)**2)
    eq('beta base',norm(betaB-O),(m*u*P)**2)
    eq('beta added grid side',norm(betaB-A),(m*u*v*v)**2)
    eq('beta count',Q+v*v,P)
    return {'status':'PASS','identities':labels,'identity_count':len(labels),'positioned_endpoint_events':len(events)}

def arithmetic(limit=100):
    accepted=cone=seeds=rectangles=0;exceptions=[]
    def represent(w,u,v):
        g=gcd(u,v)
        if w<0 or w%g:return None
        uu,vv=u//g,v//g
        x=(w//g*pow(uu,-1,vv))%vv if vv>1 else 0
        y=(w-x*u)//v
        return (x,y) if y>=0 else None
    for u in range(2,limit+1):
        for v in range(u+1,2*u+3):
            b=v*v-u*u;d=v-u;D=u*u+u*v-v*v;w=u*v+d*(D+u+v)
            rep=represent(w,u,v)
            if D>0:
                cone+=1;assert rep is not None
            if rep is None or w==0:continue
            accepted+=1
            x,y=rep
            if D<0 and len(exceptions)<10:exceptions.append([u,v,w,x,y])
            for t in range(1,u):
                m=v+t;J=u*m//v;r=v*(J+1)-u*m
                assert t<=J<m and 1<=r<=v
                assert u*u*m>u*v*t
                assert b-d*t>d*(u-t)>=0
                seeds+=1
                for j in set([t,min(J,m-1),max(t,J-1),min(m-1,J+1),v-1,v,m-1]):
                    if not t<=j<m:continue
                    K=b*(u+t) if j<v else b*m
                    if j<=J:
                        coef=(d-1)*u+d*(t-1) if j<v else d*m-v
                        px,py=v+coef,coef
                        width=K-v*v
                    elif j<v:
                        px=x+(t-1)*(d+v);py=y+(t-1)*d+v*(v-1-j)
                        width=K+u*v*m-v*v*(j+1)
                    else:
                        px=d*m;py=v*(m-j-1);width=K+u*v*m-v*v*(j+1)
                    assert px>=0 and py>=0 and px*u+py*v==width
                    rectangles+=1
    return {'status':'PASS','u_limit':limit,'v_limit_rule':'v<=2u+2','accepted_parameter_pairs':accepted,
            'golden_cone_pairs':cone,'seed_parameter_cases':seeds,
            'critical_rectangle_checks':rectangles,'sample_extra_pairs':exceptions}
if __name__=='__main__':
    out={'symbolic':symbolic(),'arithmetic_regression':arithmetic(),
         'scope':'Universal identities plus a written geometric proof. Bounded regression is not the proof of the infinite quantifier.',
         'formal_proof_assistant':False,'external_review':False}
    Path(__file__).with_name('symbolic_report.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
