#!/usr/bin/env python3
"""Audit forbidden-anchor inequalities against exact rational clipping."""
from fractions import Fraction as F
from pathlib import Path
import json,random

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def prod(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def scale(a,n):return(a[0]*n,a[1]*n)
def rot(a):return(-a[1],sum(a))
def norm(a):return a[0]**2+a[0]*a[1]+a[1]**2
def edges(p):return zip(p,p[1:]+p[:1])
def area(p):return sum(det(a,b) for a,b in edges(p))
def ccw(p):return p if area(p)>0 else p[::-1]
def clipping(p,ob):
    p=[tuple(map(F,a))for a in p]
    for a,b in edges(ob):
        d=sub(b,a);out=[]
        if not p:break
        for u,v in edges(p):
            cu,cv=det(d,sub(u,a)),det(d,sub(v,a))
            if cu>=0:out.append(u)
            if (cu>0 and cv<0)or(cu<0 and cv>0):
                t=cu/(cu-cv);out.append(add(u,scale(sub(v,u),t)))
        p=out
    return bool(p)and area(p)>0
def forbidden(t,ob):
    f=[]
    for a,b in edges(t):
        d=sub(b,a);M=max(det(d,sub(z,a))for z in ob)
        f.append((-d[1],d[0],M-1))
    for a,b in edges(ob):
        d=sub(b,a);M=det(d,a)-max(det(d,z)for z in t)
        f.append((d[1],-d[0],-M-1))
    return f

rng=random.Random(63414430);checks=overlaps=0
for q in(1,2,4):
    a,b,c=q*(3*q+2),2*q+1,3*q*q+3*q+1
    A,B=a*b,b*b;eta=(2*q+1,-q);bar=(q+1,q)
    assert norm(eta)==norm(bar)==c
    X=(-a*a,0);Y=(2*A,-2*A-B);K=(2*A,A+2*B)
    R1=(A,-A);R2=(A+B,0);R3=(0,A)
    obs=[ccw([prod(p,bar)for p in t])for t in([X,Y,R1],[X,R1,R2],[X,R2,R3])]
    templates=[]
    for u in (bar,eta):
        for aa,bb in ((a,b),(b,a)):
            x,y=scale(u,aa),scale(rot(rot(u)),bb)
            for _ in range(6):
                t=[(0,0),x,y]
                assert sorted(norm(sub(v,u))for u,v in edges(t))==[b*b*c,a*a*c,c*c*c]
                templates.append(t);x,y=rot(x),rot(y)
    vertices=[prod(p,bar)for p in (X,Y,K)]
    xx=[p[0]for p in vertices];yy=[p[1]for p in vertices]
    for _ in range(1000):
        t=rng.choice(templates);ob=rng.choice(obs)
        anchor=(rng.randint(min(xx),max(xx)),rng.randint(min(yy),max(yy)))
        predicted=all(kx*anchor[0]+ky*anchor[1]<=v for kx,ky,v in forbidden(t,ob))
        exact=clipping([add(anchor,p)for p in t],ob)
        assert predicted==exact,(q,t,ob,anchor)
        checks+=1;overlaps+=exact
assert 0<overlaps<checks
report={'status':'PASS','exact_rational_clipping_comparisons':checks,
        'interior_overlap_cases':overlaps,'tested_family_parameters':[1,2,4],
        'claim':'Audit of candidate-obstacle filtering only; no tiling existence result.'}
Path(__file__).with_name('candidate_geometry_checked.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
