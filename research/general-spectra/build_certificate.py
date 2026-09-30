#!/usr/bin/env python3
"""Exact hierarchical construction for rational 60/120-degree triangle tiles.

Coordinates (x,y) mean (x+y/2, sqrt(3)*y/2). The certificate is a
partition into integer-scale copies of the tile and tiled parallelograms.
No experimental numerical coordinates or numerical-angle filters are used.
"""
from __future__ import annotations
import argparse
import json
from math import gcd, isqrt
from pathlib import Path


def rotate(p: tuple[int, int], turns: int) -> tuple[int, int]:
    x,y=p
    for _ in range(turns % 3):
        x,y=-x-y,x
    return x,y


def construct(a: int,b: int,c: int,angle: int,m: int) -> dict:
    if not (a>b>1 and gcd(a,b)==1 and angle in (60,120)):
        raise ValueError('Require coprime a>b>1, and angle 60 or 120.')
    sign=1 if angle==120 else -1
    if c*c != a*a+b*b+sign*a*b:
        raise ValueError('Tile does not satisfy the specified norm equation.')
    q,r=divmod(a,b)
    k0=q+(2 if angle==120 else 1)
    if m<3*k0:
        raise ValueError('This construction requires m >= 3*k0.')
    L=a*b
    K=a*a+b*b-(L if angle==60 else 0)
    rr=ss=k0
    tt=m-2*k0
    S=m*L
    # Standard trapezoid: (0,0),(x+h,0),(x,h),(0,h).
    # Three trapezoids exactly partition the equilateral triangle.
    settings=[(rr,tt,(ss*L,0),0),
              (tt,ss,(0,(ss+tt)*L),2),
              (ss,rr,((ss+rr)*L,tt*L),1)]
    regions=[]
    bands=[]
    def emit(kind, pts, origin, turns, name, **kw):
        out=[]
        for p in pts:
            x,y=rotate(p,turns)
            out.append([x+origin[0],y+origin[1]])
        regions.append(dict(id=name,kind=kind,vertices=out,**kw))
    for ti,(k,n,offset,turns) in enumerate(settings):
        for j in range(n):
            # From bottom to top, the shorter bases decrease by L.
            kb=k+n-j-1
            x=kb*L
            R=x-K
            eff=kb+(1 if angle==60 else 0)
            na=b-r
            nb=a*(eff-q-1)-b
            if min(R,na,nb)<0 or R!=na*a+nb*b:
                raise ArithmeticError('Invalid exact strip decomposition.')
            dy=rotate((0,j*L),turns)
            origin=(offset[0]+dy[0],offset[1]+dy[1])
            A=(0,0);B=(K+L,0);C=(K,L);D=(0,L)
            if angle==120:
                E=(a*a,L)
                pieces=[(a,[A,E,D]),(c,[A,B,E]),(b,[E,B,C])]
            else:
                E=(a*a,0)
                pieces=[(a,[A,E,D]),(c,[D,E,C]),(b,[E,B,C])]
            for sc,pts in pieces:
                emit('similar_triangle',pts,origin,turns,
                     f'T{ti}_band{j}_scale{sc}',scale=sc)
            if R:
                emit('strip_parallelogram',
                     [B,(x+L,0),(x,L),C],origin,turns,
                     f'T{ti}_band{j}_strip',counts=[na,nb])
            bands.append(dict(trapezoid=ti,band=j,short_base=x,leg=L,
                              surplus=R,strip_counts=[na,nb]))
    return dict(format='ERDOS634_HIERARCHICAL_TRIANGLE_PARTITION_V1',
                coordinate_basis='(1,0),(1/2,sqrt(3)/2)',
                tile=[a,b,c], angle_opposite_c=angle,
                target_vertices=[[0,0],[S,0],[0,S]],
                target_side=S, expected_tile_count=L*m*m, multiplier=m,
                guaranteed_multiplier_threshold=3*k0,
                zhang_v4_displayed_threshold=3*((K+L-a-b+L-1)//L),
                bands=bands,regions=regions,
                scope='Exact construction for the specified tile and target; '
                      'not a classification of all triangle-tiling counts.')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tile',nargs=3,type=int,default=[45,32,67],metavar=('A','B','C'))
    ap.add_argument('--angle',type=int,choices=[60,120],default=120)
    ap.add_argument('--m',type=int,default=9)
    ap.add_argument('--output',type=Path,default=Path('construction_116640.json'))
    args=ap.parse_args()
    data=construct(*args.tile,args.angle,args.m)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'regions':len(data['regions']),
                      'tiles':data['expected_tile_count']}))
if __name__=='__main__':
    main()
