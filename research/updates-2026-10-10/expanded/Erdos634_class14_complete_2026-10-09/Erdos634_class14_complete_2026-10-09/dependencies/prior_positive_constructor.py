#!/usr/bin/env python3
"""Unrestricted positive W/beta tail for all integer 0<u<v and M>=v.

New work: the three-macro residue seed in parameters(), macros(), seed_units().
Prior inputs: the elementary grids, Michael Beeson's scale-v seed, and the
previous +u external cap; retained from the 9 October golden-cone package.
No nonexistence is asserted for M<v; this does not solve Erdős 634 in full.
Exact rational coordinates throughout. No search solver is used.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import gcd, lcm
import argparse, json
from pathlib import Path

Point=tuple[F,F]
Tri=tuple[Point,Point,Point]

def pt(x,y): return (F(x),F(y))
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def mul(k,p):return (k*p[0],k*p[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def ccw(tri):
    a,b,c=tri
    if det(sub(b,a),sub(c,a))<0:return (a,c,b)
    if det(sub(b,a),sub(c,a))==0:raise ValueError('zero-area tile')
    return (a,b,c)

def coin(width:int,u:int,v:int)->tuple[int,int]:
    """Return exact nonnegative p,q with width=p*u+q*v or fail."""
    g=gcd(u,v)
    if width<0 or width%g:raise ValueError(f'width {width} not supported')
    U,V,W=u//g,v//g,width//g
    p=0 if V==1 else (W*pow(U,-1,V))%V
    q=(W-p*U)//V
    if q<0:raise ValueError(f'width {width} not in <{u},{v}>')
    return p,q

def grid(origin:Point,f:Point,g:Point,k:int,hole:int=0,corner:str='f'):
    """k-fold triangle with an optional whole grid corner of scale hole removed."""
    if not 0<=hole<=k:raise ValueError((k,hole))
    for i in range(k):
        for j in range(k-i):
            o=add(origin,add(mul(i,f),mul(j,g)))
            keep=(i<k-hole) if corner=='f' else (i+j>=hole)
            if keep:yield ccw((o,add(o,f),add(o,g)))
            if i+j<k-1:
                keep=(i<k-hole) if corner=='f' else (i+j>=hole-1)
                if keep:yield ccw((add(o,f),add(o,g),add(add(o,f),g)))

def rectangle(x:int,y:int,width:int,u:int,v:int):
    """Rectangle of height uv filled with u-by-v and v-by-u cells."""
    p,q=coin(width,u,v)
    X=x
    for n,w,h in ((p,u,v),(q,v,u)):
        for _ in range(n):
            for row in range(u*v//h):
                o=pt(X,y+row*h)
                f=pt(w,0);g=pt(0,h)
                yield ccw((o,add(o,f),add(o,g)))
                yield ccw((add(o,f),add(o,g),add(add(o,f),g)))
            X+=w
    assert X==x+width

def parameters(u:int,v:int,t:int):
    if not (0<u<v and 1<=t<u):
        raise ValueError('Require 0<u<v and 1<=t<u for a new seed')
    b=v*v-u*u;d=v-u;m=v+t;w=u+t;K=b+d*t
    Q=2*v*v-u*u;P=3*v*v-u*u
    s=pt(F(b,v),0);e=pt(F(v**3,b),-F(u*v*v,b))
    s2=pt(-u,v);e2=mul(F(u,v),e)
    X=pt(0,0);O=mul(u*m,e);A=pt(-u*v*m,u*u*m);C=pt(-u*v*m,v*v*m)
    q0=pt(u*b,0);S=add(q0,mul(u*t,s2))
    p0=add(q0,mul(u*t,e));r0=add(S,mul(d*t,e2))
    V=pt(-u*u*w,u*v*w)
    assert C==add(V,mul(K,s2)) and r0==add(V,mul(K,e2))
    return dict(u=u,v=v,t=t,m=m,w=w,K=K,b=b,d=d,Q=Q,P=P,s=s,e=e,s2=s2,e2=e2,
                X=X,O=O,A=A,C=C,V=V,q0=q0,S=S,p0=p0,r0=r0)

def macros(u:int,v:int,t:int):
    p=parameters(u,v,t)
    x=lambda *names:[p[k] for k in names]
    return p,[x('O','X','q0','p0'),x('p0','q0','S','r0'),
              x('r0','V','C'),x('X','A','C','V','S','q0')]

def seed_units(u:int,v:int,t:int):
    """New three-macro construction: no aspect-ratio or Omega hypothesis."""
    p=parameters(u,v,t)
    b,d,m,w,K=(p[k] for k in ('b','d','m','w','K'))
    tiles=[]
    def emit(ts):tiles.extend(ts)
    emit(grid(p['X'],p['s'],p['e'],u*m,u*t))
    emit(grid(p['q0'],p['s2'],p['e2'],v*t,d*t))
    emit(grid(p['V'],p['s2'],p['e2'],K))
    outside_count=len(tiles)
    # Lower expanding strips. The width equals
    # u*(v+q)+v*q, q=(d-1)*u+d*j >= 0.
    for j in range(t):
        y=u*v*j;left=-v*v*j;right=u*b-u*u*j
        emit(grid(pt(left-v*v,y+u*v),pt(v,0),pt(v,-u),v))
        emit(grid(pt(right-u*u,y),pt(u,0),pt(0,v),u))
        emit(rectangle(left,y,right-u*u-left,u,v))
    J=u*m//v
    r=v*(J+1)-u*m
    assert t<=J<w and 1<=r<=v
    # Exactly u middle strips, rather than strips through height uv*m.
    for j in range(t,w):
        y=u*v*j;left=-v*v*j;right=b*w-v*v*j
        emit(grid(pt(right-v*v,y),pt(v,0),pt(0,u),v))
        if j<=J:
            cut=r if j==J else 0
            emit(grid(pt(left-v*v,y+u*v),pt(v,0),pt(v,-u),v,cut,'origin'))
            emit(rectangle(left,y,b*w-v*v,u,v))
        else:
            x=-u*v*m
            width=right-v*v-x
            assert width==u*K+v*v*(w-1-j)
            emit(rectangle(x,y,width,u,v))
    emit(grid(pt(-u*v*m,u*v*w),pt(u,0),pt(0,v),K))
    assert len(tiles)==p['Q']*m*m,(len(tiles),p['Q']*m*m)
    return tiles,p,{'method':'unrestricted_three_macro',
        'outer_macro_count':outside_count,'remainder_count':len(tiles)-outside_count,
        'middle_strip_count':u,'top_grid_scale':K,'middle_top_index':w,
        'clipped_layer':J,'removed_B_corner_scale':r,
        'aspect_ratio_restriction':False}


def parallelogram(origin:Point,f:Point,g:Point,n:int,k:int,diagonal='difference'):
    for i in range(n):
        for j in range(k):
            o=add(origin,add(mul(i,f),mul(j,g)))
            x,y,z=add(o,f),add(o,g),add(add(o,f),g)
            if diagonal=='difference':
                yield ccw((o,x,y));yield ccw((x,y,z))
            else:
                yield ccw((o,x,z));yield ccw((o,y,z))

def target_points(u,v,m):
    b=v*v-u*u
    return (pt(F(u*m*v**3,b),-F(u*u*m*v*v,b)),pt(-u*v*m,u*u*m),pt(-u*v*m,v*v*m))

def affine_map(src,dst):
    f=sub(src[1],src[0]);g=sub(src[2],src[0]);h=det(f,g)
    Fv=sub(dst[1],dst[0]);Gv=sub(dst[2],dst[0])
    def transform(P):
        w=sub(P,src[0]);r=det(w,g)/h;s=det(f,w)/h
        return add(dst[0],add(mul(r,Fv),mul(s,Gv)))
    return transform

def beeson_seed(u,v):
    """Previous scale-v triquadratic seed; attributed to Michael Beeson."""
    b=v*v-u*u;Q=2*v*v-u*u
    o=pt(0,0);a=pt(b*b,0);c=pt(-F(u*u*b,2),F(u*b,2))
    d=pt(-F(u*u*b,2),-F(u*b,2));e=pt(-F(u*u*Q,2),-F(u**3,2));bb=add(d,e)
    ts=[]
    for A,B,k in ((a,c,b),(a,d,b),(c,e,u*v)):
        ts.extend(grid(o,mul(F(1,k),A),mul(F(1,k),B),k))
    ts.extend(parallelogram(o,mul(F(1,b),d),mul(F(1,u*u),e),b,u*u))
    O,A,C=target_points(u,v,v)
    transform=affine_map((a,c,bb),(C,A,O))
    out=[ccw(tuple(transform(P) for P in tri)) for tri in ts]
    assert len(out)==Q*v*v
    return out

def cap(u,v,T):
    """Previous six-block +u cap; T>=v-u. No search or necessity claim."""
    if T<v-u:raise ValueError('cap cutoff')
    a=u*v;b=v*v-u*u;c=v*v;Q=b+c;P=b+2*c
    h=u*(v-u);q=u*u;k=u*v;L0=h*b
    p=pt(a,0);w=pt(-F(u*P,2*v),F(b,2*v))
    r=pt(F(u*Q,2*v),F(u*u,2*v));s=pt(-F(u*b,2*v),F(b,2*v))
    O=pt(0,0);K=pt(u*v**3,0);R=mul(b,r);J=mul(h,add(r,s))
    C=add(K,mul(h,p));E=add(R,mul(h,s));B=sub(E,pt(L0,0))
    X=mul(h,r);Y=add(C,mul(q,w))
    ts=[]
    ts.extend(grid(O,mul(F(1,k),K),mul(F(1,k),R),k))
    ts.extend(grid(J,mul(F(1,h),sub(B,J)),mul(F(1,h),sub(E,J)),h))
    ts.extend(grid(O,r,add(r,s),h))
    ts.extend(parallelogram(X,r,s,b-h,h,'sum'))
    ts.extend(parallelogram(K,p,w,h,q,'sum'))
    ts.extend(grid(R,p,add(p,w),h))
    assert len(ts)==u**4+2*u*v*b
    L=u*Q*T-L0
    ts=[tuple(add(P,pt(L,0)) for P in tri) for tri in ts]
    ts.extend(parallelogram(O,pt(a,0),mul(F(1,a),B),v*T,a,'sum'))
    ts.extend(parallelogram(pt(a*v*T,0),pt(b,0),mul(F(1,b),B),u*(T-v+u),b,'sum'))
    M=T+u;Aout=target_points(u,v,M)[1]
    def transform(P):
        x,y=P
        return add(Aout,pt(F(v,b)*x-F(u*v,b)*y,-F(u,b)*x+F(Q,b)*y))
    ts=[ccw(tuple(transform(P) for P in tri)) for tri in ts]
    assert len(ts)==Q*(M*M-T*T)
    return ts

def construction(u:int,v:int,m:int,beta:bool=False):
    if not (0<u<v and m>=v):raise ValueError('Require 0<u<v and m>=v')
    b=v*v-u*u;d=v-u;Q=2*v*v-u*u;P=3*v*v-u*u
    t=(m-v)%u;M0=v+t;steps=(m-M0)//u
    if t:
        tiles,p,stats=seed_units(u,v,t)
    else:
        tiles=beeson_seed(u,v);stats={'prior_Beeson_seed':True}
    shift=mul(m-M0,target_points(u,v,1)[2])
    tiles=[tuple(add(P,shift) for P in tri) for tri in tiles]
    for j in range(steps):
        T=M0+j*u;M=T+u
        shift=mul(m-M,target_points(u,v,1)[2])
        tiles.extend(tuple(add(P,shift) for P in tri) for tri in cap(u,v,T))
    O,A,C=target_points(u,v,m)
    target=ccw((O,A,C))
    assert len(tiles)==Q*m*m
    if beta:
        B=add(O,mul(F(P,Q),sub(A,O)))
        tiles.extend(grid(A,mul(F(1,v*m),sub(C,A)),mul(F(1,v*m),sub(B,A)),v*m))
        target=ccw((O,B,C))
        assert len(tiles)==P*m*m
    stats.update({'seed_scale':M0,'cap_count':steps})
    den=1
    for tri in tiles+[target]:
        for point in tri:
            for val in point:den=lcm(den,val.denominator)
    to_int=lambda P:[int(den*P[0]),int(den*P[1])]
    return {'schema':'erdos634-oblique-exact-v1','claim':'positive_certificate_only',
            'u':u,'v':v,'m':m,'seed_t':t,'branch':'beta' if beta else 'W',
            'tile_sides':[u*v,b,v*v], 'tile_count':len(tiles),
            'metric_integer':[v**3,u*P,v**3],
            'metric_common_divisor':v,'coordinate_denominator':den,
            'target':[to_int(P) for P in target],
            'triangles':[[to_int(P) for P in tri] for tri in tiles],
            'construction_stats':stats}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--u',type=int,required=True);ap.add_argument('--v',type=int,required=True)
    ap.add_argument('--m',type=int,required=True);ap.add_argument('--beta',action='store_true')
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--max-tiles',type=int,default=2000000)
    a=ap.parse_args()
    N=((3 if a.beta else 2)*a.v*a.v-a.u*a.u)*a.m*a.m
    if N>a.max_tiles: ap.error(f'Known positive construction needs {N} unit tiles; increase --max-tiles to export. This is not a negative mathematical result.')
    doc=construction(a.u,a.v,a.m,a.beta)
    a.output.write_text(json.dumps(doc,separators=(',',':')))
    print(json.dumps({k:val for k,val in doc.items() if k!='triangles'},indent=2))
