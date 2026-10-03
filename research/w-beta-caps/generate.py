"""Exact six-block W cap, its collar, and complete W/beta certificates.

All coordinates are rational pairs in the metric diag(1, 4*v*v-u*u).
The credited scale-v seed is reproduced locally for self-contained checking.
No output here is a necessity claim about scales outside the construction.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import gcd
from pathlib import Path


def add(p, q): return (p[0]+q[0], p[1]+q[1])
def sub(p, q): return (p[0]-q[0], p[1]-q[1])
def mul(k, p): return (k*p[0], k*p[1])
def enc(p): return [[F(z).numerator, F(z).denominator] for z in p]
def dec(p): return tuple(F(*z) for z in p)
def tri(points, n):
    return dict(type='triangle_grid', vertices=[enc(p) for p in points], n=n)
def para(points, rows, columns, diagonal='sum'):
    return dict(type='parallelogram_grid', vertices=[enc(p) for p in points],
                rows=rows, columns=columns, diagonal=diagonal)


def parameters(u, v):
    if type(u) is not int or type(v) is not int or not 0 < u < v or gcd(u,v) != 1:
        raise ValueError('Require coprime integers 0 < u < v')
    a,b,c=u*v,v*v-u*u,v*v
    return a,b,c,b+c,b+2*c,4*v*v-u*u


def transform(blocks, fn):
    return [dict(block, vertices=[enc(fn(dec(p))) for p in block['vertices']])
            for block in blocks]


def cap(u, v):
    """The cap, with its left bottom vertex at zero, in six grid blocks."""
    a,b,c,Q,P,D=parameters(u,v)
    p=(F(a),F(0)); w=(F(-u*P,2*v),F(b,2*v))
    r=(F(u*Q,2*v),F(u*u,2*v)); s=(F(-u*b,2*v),F(b,2*v))
    k,h,q=u*v,u*(v-u),u*u
    O=(F(0),F(0)); K=(F(u*v**3),F(0)); R=mul(b,r)
    J=mul(h,add(r,s)); C=add(K,mul(h,p)); E=add(R,mul(h,s))
    L0=h*b; B=sub(E,(F(L0),F(0)))
    X=mul(h,r); Y=add(C,mul(q,w))
    blocks=[tri([O,K,R],k),tri([J,B,E],h),tri([O,X,J],h),
            para([X,R,E,J],b-h,h),
            para([K,C,Y,R],h,q),tri([R,Y,E],h)]
    return dict(format='erdos634-w-beta-caps-v1',kind='cap',u=u,v=v,
                metric_D=D,tile_sides=[a,b,c],tile_count=u**4+2*u*v*b,
                target=[enc(p) for p in [O,C,E,B]],blocks=blocks,
                top_length=L0,bottom_length=L0+u*u*Q,
                expanded_individual_tiles=False)


def canonical(u,v):
    a,b,c,Q,P,D=parameters(u,v)
    z=(F(-v*Q,2),F(-u*v,2))
    w=(F(-b*Q,2*v),F(u*b,2*v))
    z2=add(z,mul(F(P,Q),sub(w,z)))
    return z,w,z2


def strip_solution(u,v,T):
    """Exact nonnegative a/b-strip feasibility for this cap extension.

    The universal proof uses x=v*T, y=u*(T-v+u). The reduced modular
    solution verifies exact strip feasibility, which holds iff T>=v-u.
    """
    a,b,c,Q,P,D=parameters(u,v)
    if type(T) is not int or T < 1:
        raise ValueError('T must be a positive integer')
    L=u*Q*T-u*(v-u)*b
    if L < 0:
        raise ValueError('Cap top is longer than the requested collar')
    x=(pow(a,-1,b)*L) % b
    y=(L-a*x)//b
    if y < 0:
        raise ValueError('No nonnegative a/b-strip filling for this cap')
    return L,x,y


def tile_annulus(e,f,k,h):
    ke,kf=mul(k,e),mul(k,f)
    corner=add(ke,mul(h,f)); outer_f=mul(k+h,f)
    return [tri([ke,mul(k+h,e),corner],h),
            para([ke,kf,outer_f,corner],k,h,'difference')]


def shell(u,v,T,family='W'):
    a,b,c,Q,P,D=parameters(u,v)
    if family not in ('W','beta'):
        raise ValueError('Unknown family')
    L,x,y=strip_solution(u,v,T)
    V=(F(u*u*b,2),F(u*b,2)); zero=(F(0),F(0))
    blocks=[]
    if x:
        X=(F(a*x),F(0))
        blocks.append(para([zero,X,add(X,V),V],x,a))
    if y:
        X=(F(a*x),F(0)); Y=(F(L),F(0))
        blocks.append(para([X,Y,add(Y,V),add(X,V)],y,b))
    blocks+=transform(cap(u,v)['blocks'],lambda p:add(p,(F(L),F(0))))
    apex=(F(u*b*(T+u),2),F(b*(T+u),2))
    def isometry(p):
        x,y=sub(p,apex)
        return (F(-u*x+D*y,2*v),F(-x-u*y,2*v))
    blocks=transform(blocks,isometry)
    z,w,z2=canonical(u,v)
    if family=='beta':
        blocks+=tile_annulus(mul(F(1,v),w),mul(F(1,v),z2),v*T,v*u)
    target=[zero,mul(T+u,z),mul(T+u,w if family=='W' else z2)]
    inner=[zero,mul(T,z),mul(T,w if family=='W' else z2)]
    coefficient=Q if family=='W' else P
    return dict(format='erdos634-w-beta-caps-v1',kind='shell',u=u,v=v,
                T=T,family=family,metric_D=D,tile_sides=[a,b,c],
                tile_count=coefficient*((T+u)**2-T*T),
                target=[enc(p) for p in target],inner=[enc(p) for p in inner],
                blocks=blocks,strip_solution=dict(length=L,a_strips=x,b_strips=y),
                expanded_individual_tiles=False)


def seed(u,v,r,family):
    """Beeson's triquadratic seed, expanded into four ordinary grid blocks."""
    a,b,c,Q,P,D=parameters(u,v)
    O=(F(0),F(0)); A=(F(b*b),F(0))
    C=(F(-u*u*b,2),F(u*b,2)); V=(C[0],-C[1])
    E=(F(-u*u*Q,2),F(-u**3,2)); B=add(V,E)
    shift=lambda p:mul(r,sub(p,A))
    blocks=[tri([shift(p) for p in row],r*n)
            for row,n in [([O,A,C],b),([O,A,V],b),([O,C,E],a)]]
    blocks.append(para([shift(p) for p in [O,V,B,E]],b*r,u*u*r,'difference'))
    if family=='beta':
        z,w,z2=canonical(u,v)
        blocks.append(tri([O,mul(r*v,w),mul(r*v,z2)],r*v*v))
    return blocks


def plan(u,v,m):
    parameters(u,v)
    if type(m) is not int or m<1:
        raise ValueError('Scale must be a positive integer')
    steps=(m*pow(u,-1,v)) % v
    seed_scale=m-steps*u
    if seed_scale<v:
        raise ValueError('Scale is outside the proved semigroup v + <u,v>')
    return dict(seed_scale=seed_scale,seed_factor=seed_scale//v,steps=steps,
                sufficient_tail=u*v-u+1)


def generate(u,v,m,family='W'):
    a,b,c,Q,P,D=parameters(u,v)
    if family not in ('W','beta'):
        raise ValueError('Unknown family')
    chosen=plan(u,v,m)
    blocks=seed(u,v,chosen['seed_factor'],family)
    T=chosen['seed_scale']
    stages=[dict(kind='seed',scale=T,block_end=len(blocks))]
    for _ in range(chosen['steps']):
        blocks+=shell(u,v,T,family)['blocks']
        T+=u
        stages.append(dict(kind='shell',scale=T,block_end=len(blocks)))
    z,w,z2=canonical(u,v)
    target=[(F(0),F(0)),mul(m,z),mul(m,w if family=='W' else z2)]
    return dict(format='erdos634-w-beta-caps-v1',kind='tiling',u=u,v=v,m=m,
                family=family,metric_D=D,tile_sides=[a,b,c],
                tile_count=(Q if family=='W' else P)*m*m,
                target=[enc(p) for p in target],blocks=blocks,stages=stages,
                arithmetic_plan=chosen,expanded_individual_tiles=False,
                attribution='Scale-v triquadratic seed: Beeson. Six-block cap: '
                'project internal construction; no priority claim.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('u',type=int);parser.add_argument('v',type=int)
    parser.add_argument('scale',type=int,nargs='?')
    parser.add_argument('--family',choices=['W','beta'],default='W')
    parser.add_argument('--kind',choices=['cap','shell','tiling'],default='tiling')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.kind=='cap': data=cap(args.u,args.v)
    elif args.kind=='shell': data=shell(args.u,args.v,args.scale,args.family)
    else: data=generate(args.u,args.v,args.scale,args.family)
    content=json.dumps(data,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content)
    else: print(content,end='')
