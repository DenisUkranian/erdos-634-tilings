"""Exact independent score check for the auxiliary 180-count theta target."""
import argparse
import gzip
from math import gcd
from pathlib import Path


def primitive(dx, dy):
    g=gcd(abs(dx),abs(dy))
    if dx<0 or (dx==0 and dy<0): g=-g
    return dx//g,dy//g


def signed_cost(corners, weights):
    value=0
    for p,q in zip(corners,corners[1:]+corners[:1]):
        a=primitive(q[0]-p[0],q[1]-p[1]); value+=weights.get((*p,*a),0)-weights.get((*q,*a),0)
    return value


def lengths(points):
    return sorted((p[0]-q[0])**2+2*(p[1]-q[1])**2 for p,q in zip(points,points[1:]+points[:1]))


def inside_board(x,y,D):
    return y>=0 and y<=2*x and y<=2*(60*D-x)


def verify(pool,certificate,mass):
    with gzip.open(certificate,'rt') as f:
        weights={}
        for line in f:
            x,y,u,v,w=map(int,line.split());assert (u,v)==primitive(u,v)
            key=(x,y,u,v);assert key not in weights;weights[key]=w
    shape_path=Path(str(pool.with_suffix('') if pool.suffix=='.gz' else pool)+'.shapes')
    with shape_path.open() as s:
        D,N,total_shapes=map(int,s.readline().split());assert (D,N)==(729,180)
        shapes=[tuple(map(int,l.split())) for l in s]
    assert len(shapes)==total_shapes
    for x,y,u,v in shapes:
        assert x*v-y*u==20*D**2
        assert lengths([(0,0),(x,y),(u,v)])==[25*D**2,36*D**2,81*D**2]
    assert mass>=0
    outer=[(0,0),(60*D,0),(30*D,60*D)]
    demand=signed_cost(outer,weights)
    excess=0;positive=0;seen=set();scores=[]
    with (gzip.open(pool,'rt') if pool.suffix=='.gz' else pool.open()) as f:
        assert tuple(map(int,f.readline().split()))==(729,180,146434)
        for line in f:
            sid,x,y=map(int,line.split()); assert 0<=sid<len(shapes)
            assert (sid,x,y) not in seen;seen.add((sid,x,y))
            a,b,c,d=shapes[sid];t=[(x,y),(x+a,y+b),(x+c,y+d)]
            assert all(inside_board(u,v,D) for u,v in t)
            score=signed_cost(t,weights)
            scores.append(score)
            e=max(0,score-mass)
            if e: positive+=1;excess+=e
    assert len(seen)==146434
    gap=demand-excess-N*mass
    print(f'D={D} N={N} shapes={total_shapes} placements={len(seen)} weights={len(weights)} mass={mass} demand={demand} positive_count={positive} excess={excess} integer_gap={gap}')
    assert gap>0
    scores.sort(reverse=True)
    ceiling=N*scores[0]; best=sum(scores[:N])
    assert demand>ceiling and demand>best
    print(f"maximum_tile={scores[0]} uniform_ceiling={ceiling} uniform_gap={demand-ceiling} top180={best} top180_gap={demand-best}")

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pool',type=Path);parser.add_argument('certificate',type=Path);parser.add_argument('--mass',type=int,default=1000000)
    args=parser.parse_args();verify(args.pool,args.certificate,args.mass)
