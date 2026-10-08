#!/usr/bin/env python3
"""Symbolic all-u audit of the residual dissection, without a CAS/solver.

Exact polynomials in u. Convexity/positive area are proved by nonnegative
coefficients after u=t+2. Positioned boundary endpoint currents cancel
identically. Thus positive region multiplicities equal the target's.
"""
from collections import Counter
from math import comb
from pathlib import Path
import json


class P:
    def __init__(self, x=0):
        cc = list(x.c) if isinstance(x, P) else list(x) if isinstance(x, (tuple,list)) else [x]
        while len(cc)>1 and cc[-1]==0:cc.pop()
        self.c=tuple(cc)
    def __add__(self, x):
        x=P(x); n=max(len(self.c),len(x.c))
        return P([(self.c[i] if i<len(self.c) else 0)+(x.c[i] if i<len(x.c) else 0) for i in range(n)])
    __radd__=__add__
    def __neg__(self):return P([-x for x in self.c])
    def __sub__(self,x):return self+-P(x)
    def __rsub__(self,x):return P(x)+-self
    def __mul__(self,x):
        x=P(x);cc=[0]*(len(self.c)+len(x.c)-1)
        for i,a in enumerate(self.c):
            for j,b in enumerate(x.c):cc[i+j]+=a*b
        return P(cc)
    __rmul__=__mul__
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,x):return self.c==P(x).c
    def __hash__(self):return hash(self.c)
    def val(self,n):return sum(c*n**i for i,c in enumerate(self.c))
    def shift_two(self):
        return [sum(self.c[i]*comb(i,k)*2**(i-k) for i in range(k,len(self.c))) for k in range(len(self.c))]


def point(x,y):return (P(x),P(y))
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def edges(p):return zip(p,p[1:]+p[:1])
def area2(p):return sum((cross(a,b) for a,b in edges(p)),P(0))
def rect(x0,y0,x1,y1):return [point(x0,y0),point(x1,y0),point(x1,y1),point(x0,y1)]


def run():
    u=P((0,1));v=u+1;m=u+2;b=2*u+1;k=u*u-u-1
    V=point(-u*u*m,u*v*m)
    xl=-v-u*u*v;yl=u+u**3;xr=v*(u-1)
    F=point(xl,yl+u*b)
    central=[point(xl,yl),point(-v,u),point(xr,u),point(xr,u+u*v),
             add(F,point(v,-u)),add(F,point(0,-u))]
    right=[
        [point(0,0),point(-v,u),point(0,u)],
        rect(0,0,xr,u),rect(xr,0,u*v,u*v),
        [point(u*v,0),point(u*b,0),point(u*v,u*v)],
        [point(xr,u*v),point(u*v,u*v),point(xr,u*v+u)],
    ]
    left=[
        [point(-u*m,v*m),point(-u*m,v),point(-u,v)],
        rect(-u*m,1,-u,v),
        [point(-u,0),point(-u,v),point(0,0)],
        rect(-u*m,-u*m,-u,1),
        [point(-u*m,-u*m),point(-u,-u*m),point(-u,-2*u*v)],
        rect(-u,-u*v,0,0),
        [point(0,0),point(0,-u*v),point(v*v,-u*v)],
        rect(-u,-2*u*v,k,-u*v),
        [point(-u,-2*u*v),point(k,-2*u*v),point(k,-3*u*u-u)],
    ]
    pieces=[central]+right+[[add(p,V) for p in poly] for poly in left]
    target=[point(0,0),point(-u*v*m,u*u*m),point(-u*v*m,v*v*m),V,
            point(-u*u*m+v*v,u*v*v),point(-u*u*v,u*v*v),
            point(u*v,u*v),point(u*b,0)]
    positive_sign_proofs=0
    oriented=[]
    for poly in pieces:
        if area2(poly).val(2)<0:poly=list(reversed(poly))
        coeff=area2(poly).shift_two()
        assert all(c>=0 for c in coeff) and coeff[0]>0
        positive_sign_proofs+=1
        for a,z in edges(poly):
            for p in poly:
                coeff=cross(sub(z,a),sub(p,a)).shift_two()
                assert all(c>=0 for c in coeff), ('convexity',len(oriented),coeff)
                positive_sign_proofs+=1
        oriented.append(poly)
    if area2(target).val(2)<0:target=list(reversed(target))
    directions=[point(1,0),point(0,1),point(u,-v),point(v,-u)]
    events=Counter()
    for sign,poly in [(1,p) for p in oriented]+[(-1,target)]:
        for a,z in edges(poly):
            e=sub(z,a)
            kinds=[i for i,d in enumerate(directions) if cross(d,e)==0]
            assert len(kinds)==1
            kind=kinds[0];offset=cross(directions[kind],a)
            events[(kind,offset,a)]+=sign
            events[(kind,offset,z)]-=sign
    nonzero=[value for value in events.values() if value]
    assert not nonzero, (len(nonzero),nonzero)
    total=sum((area2(poly) for poly in oriented),P(0))
    assert total==area2(target)
    expected=(4*u**3+14*u*u+16*u+5)*u*v
    assert total==expected
    # Verify the exact tile exchanged between the strip and cap.
    H=point(k,-u*u);K=point(k,-u*v);R=point(u*u,-u*v)
    assert add(H,V)==F
    assert sub(K,H)==point(0,-u) and sub(R,H)==point(v,-u)
    # A second identity includes all four outside macros and the whole W
    # triangle. Multiply every coordinate by b to clear denominators.
    def scaled(p):return (b*p[0],b*p[1])
    OO=point(u*m*v**3,-u*u*m*v*v)
    XX=point(0,0);AA=point(-u*v*m*b,u*u*m*b);CC=point(-u*v*m*b,v*v*m*b)
    VV=point(-u*u*m*b,u*v*m*b);UU=point((-u*u*m+v*v)*b,u*v*v*b)
    RR=point(-u*u*v*b,u*v*v*b);SS=point(u*v*b,u*v*b);QQ=point(u*b*b,0)
    PP=add(QQ,point(u*v**3,-u*u*v*v))
    R0=add(SS,point(u*v*v,-u*u*v))
    TT=add(UU,point((u-1)*v**3,-(u-1)*u*v*v))
    outside=[[OO,XX,QQ,PP],[PP,QQ,SS,R0],[R0,RR,UU,TT],[TT,VV,CC]]
    # Physical Gram form in the oblique basis vE,vF. Coordinates here
    # are additionally multiplied by b. This polynomial equals v times
    # the physical squared norm of the b-scaled displacement.
    def metric(p):
        x,y=p
        return v**3*(x*x+y*y)+u*(3*v*v-u*u)*x*y
    a=u*v;c=v*v
    assert metric(point(u,0))==v*a*a
    assert metric(point(0,v))==v*c*c
    assert metric(point(u,-v))==v*b*b
    assert metric(point(v,0))==v*c*c
    assert metric(point(0,u))==v*a*a
    assert metric(point(v,-u))==v*b*b
    gram_discriminant=4*v**6-u*u*(3*v*v-u*u)**2
    assert gram_discriminant==b*b*(4*v*v-u*u)
    assert all(c>=0 for c in gram_discriminant.shift_two())
    assert gram_discriminant.val(2)>0
    lengths=[[c*u*m,b*u*v,c*u,a*u*v],
             [a*v,b*u,a,c*u],
             [c*2*u,b*v,c*(u-1),a*v],
             [a*m,b*m,c*m]]
    for poly,wanted in zip(outside,lengths):
        for (start,end),length in zip(edges(poly),wanted):
            assert metric(sub(end,start))==v*b*b*length*length
    for poly,r,s in zip(outside[:3],[u*m,v,2*u],[u,1,u-1]):
        bottom=sub(poly[1],poly[0]);top=sub(poly[2],poly[3])
        assert (r*top[0],r*top[1])==(s*bottom[0],s*bottom[1])
    all_regions=[[scaled(p) for p in poly] for poly in oriented]
    for poly in outside:
        if area2(poly).val(2)<0:poly=list(reversed(poly))
        coeff=area2(poly).shift_two()
        assert all(c>=0 for c in coeff) and coeff[0]>0
        for a,z in edges(poly):
            for p in poly:
                coeff=cross(sub(z,a),sub(p,a)).shift_two()
                assert all(c>=0 for c in coeff), ('outside convexity',coeff)
        all_regions.append(poly)
    whole=[OO,AA,CC]
    if area2(whole).val(2)<0:whole=list(reversed(whole))
    all_directions=directions+[point(-u*(2*v*v-u*u),v**3)]
    full_events=Counter()
    for sign,poly in [(1,p) for p in all_regions]+[(-1,whole)]:
        for a,z in edges(poly):
            e=sub(z,a)
            kinds=[i for i,d in enumerate(all_directions) if cross(d,e)==0]
            assert len(kinds)==1
            kind=kinds[0];offset=cross(all_directions[kind],a)
            full_events[(kind,offset,a)]+=sign
            full_events[(kind,offset,z)]-=sign
    assert not any(full_events.values())
    assert sum((area2(p) for p in all_regions),P(0))==area2(whole)
    # Every primitive A/B tile has coordinate doubled area uv before
    # scaling by b. Therefore the full tile count is Q*m^2.
    assert area2(whole)==u*v*b*b*(2*v*v-u*u)*m*m
    report={'status':'PASS','scope':'Exact polynomial identities for every integer u>=2',
            'fixed_positive_macroregions':len(oriented),
            'symbolic_nonnegative_sign_checks':positive_sign_proofs,
            'positioned_boundary_identity':True,'area_identity':True,
            'corner_exchange_identity':True,
            'full_W_positive_macroregions':len(all_regions),
            'full_W_boundary_identity':True,'full_W_area_and_count_identity':True,
            'outside_grid_metric_and_homothety_identities':True,
            'primitive_A_B_metric_identities':True,'positive_definite_Gram_form':True,
            'method':'All sign polynomials have nonnegative coefficients in t=u-2; all boundary endpoint currents cancel identically.'}
    Path(__file__).with_name('adjacent_symbolic_verified.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    run()
