#!/usr/bin/env python3
"""Positive controls for the affine-line residue lower bound; no search claim."""
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
from itertools import combinations
from math import gcd, isqrt, lcm
from pathlib import Path
import json
import random

HERE=Path(__file__).resolve().parent


def norm(v):return v[0]*v[0]+v[0]*v[1]+v[1]*v[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]


def direction(v):
    factor=gcd(*v)
    x,y=v[0]//factor,v[1]//factor
    sign=1 if y>0 or y==0 and x>0 else -1
    return (sign*x,sign*y),sign


def distances(a,b,c):
    answer=[None]*c;answer[0]=0;queue=deque([0])
    while queue:
        r=queue.popleft()
        for step in (a,-a,b,-b):
            s=(r+step)%c
            if answer[s] is None:answer[s]=answer[r]+1;queue.append(s)
    assert all(x is not None for x in answer)
    return answer


def prepare(tiles,target,a,b,c,unit_directions):
    scale=lcm(*(Q(v).denominator for t in tiles+[target] for p in t for v in p))
    integer=lambda p:tuple(int(Q(v)*scale) for v in p)
    directions={}
    for vector,h in unit_directions:
        denominator=lcm(*(Q(x).denominator for x in vector))
        key,_=direction(tuple(int(Q(x)*denominator) for x in vector))
        directions[key]=h
    def edge(p,q):
        v=sub(q,p);length=isqrt(norm(v));assert length*length==norm(v) and length%scale==0
        d,sign=direction(v)
        return d,(d[0]*p[1]-d[1]*p[0]),sign*(length//scale)
    tile_data=[]
    for t in tiles:
        points=tuple(map(integer,t));short=[];heights=[]
        for p,q in zip(points,points[1:]+points[:1]):
            d,offset,ell=edge(p,q)
            if abs(ell)==c:continue
            assert abs(ell) in (a,b)
            h=directions[d];heights.append(h);short.append(((h,d,offset),ell))
        assert len(short)==2 and heights[0]==heights[1] and short[0][0][1]!=short[1][0][1]
        tile_data.append((heights[0],short))
    boundary=Counter();points=tuple(map(integer,target))
    for p,q in zip(points,points[1:]+points[:1]):
        d,offset,ell=edge(p,q)
        if ell%c:boundary[directions[d],d,offset]+=ell
    return tile_data,boundary,distances(a,b,c)


def bounds(tile_data,boundary,distance,selected):
    currents=Counter();placed=Counter()
    for i in selected:
        h,edges=tile_data[i];placed[h]+=1
        for key,value in edges:currents[key]+=value
    by_axis=defaultdict(Counter)
    modulus=len(distance)
    for key in set(currents)|set(boundary):
        h,d,_=key
        by_axis[h][d]+=distance[(boundary[key]-currents[key])%modulus]
    return {h:max((sum(axes.values())+1)//2,max(axes.values(),default=0))
            for h,axes in by_axis.items()}


def verify_controls(tiles,target,a,b,c,dirs,selections):
    data,boundary,distance=prepare(tiles,target,a,b,c,dirs)
    totals=Counter(h for h,_ in data)
    for selected in selections:
        required=bounds(data,boundary,distance,selected)
        placed=Counter(data[i][0] for i in selected)
        assert all(n<=totals[h]-placed[h] for h,n in required.items()),(selected,required)
    assert all(n==0 for n in bounds(data,boundary,distance,range(len(data))).values())
    return len(selections)


def main():
    a,b,c=8,7,13
    assert distances(a,b,c)==[0,2,2,2,3,1,1,1,1,3,2,2,2]
    target=((Q(0),Q(0)),(Q(16),Q(0)),(Q(-14),Q(14)))
    o,u,v=target;mid=lambda p,q:tuple((x+y)/2 for x,y in zip(p,q))
    ou,ov,uv=mid(o,u),mid(o,v),mid(u,v)
    tiles=[(o,ou,ov),(ou,u,uv),(ov,uv,v),(ou,uv,ov)]
    directions=[];direction_vector=(Q(1),Q(0))
    for _ in range(6):
        directions.append((direction_vector,0))
        x,y=direction_vector;direction_vector=(-y,x+y)
    choices=[combo for k in range(5) for combo in combinations(range(4),k)]
    grid_cases=verify_controls(tiles,target,a,b,c,directions,choices)

    # Read-only reconstruction of the existing attributed Harries 88 control.
    # Exclude its final report-writing statement, preserving the frozen package.
    source=HERE.parent.parent/'position-currents-oct7/positive_controls.py'
    code=source.read_text().split('report={',1)[0]
    namespace={'__file__':str(source),'__name__':'positive_control_read_only'}
    exec(compile(code,str(source),'exec'),namespace)
    rng=random.Random(63415488)
    choices=[(),tuple(range(88))]
    choices.extend((i,) for i in range(88))
    choices.extend(tuple(j for j in range(88) if j!=i) for i in range(88))
    choices.extend(tuple(rng.sample(range(88),rng.randrange(89))) for _ in range(1000))
    harries_cases=verify_controls(namespace['triangles'],namespace['P'],3,5,7,namespace['dirs'],choices)
    report={'status':'PASS','four_tile_grid_subsets':grid_cases,'Harries_88_partial_subsets':harries_cases,
            'distance_table_mod13':distances(8,7,13),'search_pruning_enabled':False,
            'scope':'Necessary future-tile bounds never exceed the actual omitted populations in positive controls',
            'N154_decided':False,'full_Erdos634_solved':False}
    (HERE/'line-residue-bound-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
