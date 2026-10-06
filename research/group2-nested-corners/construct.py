#!/usr/bin/env python3
"""Positive nested-corner extension of the existing reflected-corner grids.

Coordinates are x+y*rho with rho=exp(i*pi/3).  The rectangle height q is
allowed to exceed the corner removed, m*(a-b).  No search for unit tiles.
"""
import argparse
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path


def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def smul(k,p): return (k*p[0],k*p[1])
def cmul(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def conj(p): return (p[0]+p[1],-p[1])
def enc(poly): return [[str(x),str(y)] for x,y in poly]


def grid(p,q,r,n):
    if type(n) is not int or n<=0: raise ValueError('positive integer grid scale required')
    u,v=smul(F(1,n),sub(q,p)),smul(F(1,n),sub(r,p))
    for i in range(n):
        for j in range(n-i):
            o=add(p,add(smul(i,u),smul(j,v)));x=add(o,u);y=add(o,v)
            yield [o,x,y]
            if i+j<n-1: yield [x,add(x,v),y]


def semigroup(n,a,b):
    g=gcd(a,b)
    if n<0 or n%g: raise ValueError('negative or inadmissible semigroup width')
    aa,bb,nn=a//g,b//g,n//g
    x=0 if bb==1 else nn*pow(aa,-1,bb)%bb
    y=(n-a*x)//b
    if y<0: raise ValueError('width is outside the short-side semigroup')
    return x,y


def witness(a,b,c,m,k,q):
    if any(type(x) is not int for x in (a,b,c,m,k,q)):
        raise ValueError('integer parameters required')
    if not (a>b>0 and c*c==a*a+a*b+b*b and m>0 and k>0):
        raise ValueError('require a>b>0, plus norm, m,k>0')
    n=m*(a-b)
    if not(q>=n and k*c>=n and m*c>k*a):
        raise ValueError('the deleted corner or high triangles do not fit')
    r=m*a*c-a*a*k-c*q
    x,y=semigroup(r,a,b)
    return {'removed_corner':n,'rectangle_columns':k*c,'rectangle_rows':q,
            'k':k,'q':q,'width':r,'a_coefficient':x,'b_coefficient':y}


def choose(a,b,c,m):
    n=m*(a-b)
    for k in range((n+c-1)//c,(m*b*c)//(a*a)+1):
        for q in range(n,(m*a*c-a*a*k)//c+1):
            try: return witness(a,b,c,m,k,q)
            except ValueError: pass
    raise ValueError('no nested-corner witness in this construction family')


def q_tiles(a,b,c,m,k,q):
    data=witness(a,b,c,m,k,q)
    n=data['removed_corner'];r=data['width'];xcoef=data['a_coefficient'];ycoef=data['b_coefficient']
    z=(F(a,c),F(b,c))
    A=(F(m*c*c),F(0));B=(F(m*a*a),F(m*a*b))
    C=(F(q*a),F(q*b));E=(F(k*a*c),F(0));D=add(C,E)
    U=add(C,smul(k*a*a,z));V=add(E,smul(a*(m*c-k*a),z))
    # The large rectangular grid contains the deleted n-grid corner because
    # both its dimensions are >=n.  Its height is q, independently of n.
    u=(F(a),F(0));v=(F(a),F(b))
    for i in range(k*c):
        for j in range(q):
            o=add(smul(i,u),smul(j,v));x=add(o,u);y=add(o,v)
            if i+j>=n: yield [o,x,y]
            if i+j>=n-1: yield [x,add(x,v),y]
    yield from grid(C,D,U,k*a)
    yield from grid(E,A,V,m*c-k*a)
    w=smul(F(1,k*a*b),sub(D,U))
    offset=0
    for count,width,height in ((xcoef,a,b),(ycoef,b,a)):
        for _ in range(count):
            base=add(U,smul(offset,z));du=smul(width,z);dv=smul(height,w)
            for j in range(k*a*b//height):
                o=add(base,smul(j,dv));x=add(o,du);y=add(o,dv);xy=add(x,dv)
                yield [o,x,xy];yield [o,xy,y]
            offset+=width
    if offset!=r: raise RuntimeError('width bookkeeping error')


def construct(a,b,c,m=1,family='F3',k=None,q=None):
    if (k is None)!=(q is None): raise ValueError('specify both k and q or neither')
    data=choose(a,b,c,m) if k is None else witness(a,b,c,m,k,q)
    k,q=data['k'],data['q']
    core=list(q_tiles(a,b,c,m,k,q))
    if len(core)!=3*a*b*m*m: raise RuntimeError('corner count error')
    origin=(F(0),F(0));S=c*c;h=a+2*b;ell=2*a+b
    Z=(F(a),F(b));Z2=cmul(Z,Z)
    if family in ('F2','F3'):
        Y=(F(m*S),F(0));I=smul(m*a,Z);J=smul(m,Z2);T=smul(F(m*a*h,S),Z2)
        v2=(F(b*ell,S),F(-a*h,S))
        def reflect(w): return add(Y,cmul(v2,conj(sub(w,Y))))
        triangles=[[reflect(p) for p in tri] for tri in core]
        triangles.extend(grid(origin,Y,I,m*c));triangles.extend(grid(origin,I,J,m*c))
        target=[origin,Y,T];expected=h*ell*m*m
        if family=='F3':
            K=smul(F(m*h,S),cmul(Z2,Z))
            triangles.extend(grid(origin,T,K,m*h))
            target=[origin,Y,K];expected=3*h*(a+b)*m*m
    elif family=='F4':
        u=(F(b),F(a));A=(F(b*c),F(0));D=(F((a+b)*c),F(0))
        C=smul(F(b*ell,c),u);E=add(A,smul(F(a*b,c),u));H=add(A,(F(0),F(b*c)))
        Bbig=smul(m*c,u);rot=smul(F(-1,c),u)
        triangles=[[add(Bbig,cmul(rot,p)) for p in tri] for tri in core]
        for p,qq,r,n in ((A,D,E,m*a),(D,C,E,m*a),(H,A,E,m*b)):
            triangles.extend(grid(smul(m,p),smul(m,qq),smul(m,r),n))
        target=[smul(m,p) for p in (origin,D,C)];expected=ell*(a+b)*m*m
    else: raise ValueError('family must be F2, F3, or F4')
    if len(triangles)!=expected: raise RuntimeError('target count error')
    return {'format':f'ERDOS634_{family}_UNIT_TRIANGLES_V1',
            'coordinate_metric':'x^2+x*y+y^2','tile':[a,b,c],
            'multiplier':m,'count':expected,'target':enc(target),
            'triangles':[enc(t) for t in triangles],
            'construction':'nested reflected corner with independent rectangle height',
            'nested_corner_witness':data,'Q_count':len(core)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ('a','b','c'): ap.add_argument(name,type=int)
    ap.add_argument('--multiplier',type=int,default=1)
    ap.add_argument('--family',choices=('F2','F3','F4'),default='F3')
    ap.add_argument('--k',type=int);ap.add_argument('--q',type=int)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    result=construct(args.a,args.b,args.c,args.multiplier,args.family,args.k,args.q)
    args.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({'count':result['count'],'witness':result['nested_corner_witness']}))


if __name__=='__main__': main()
