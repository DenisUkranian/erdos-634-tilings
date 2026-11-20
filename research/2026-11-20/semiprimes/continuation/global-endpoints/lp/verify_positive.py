#!/usr/bin/env python3
"""Independently validate an integral positive solver output.

Floating LP weights are never a proof. They are rounded only when near 0 or 1;
all metrics, counts, containment, distinctness and boundary identities are then
checked exactly using rational arithmetic.
"""
import argparse,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from verify_endpoint_dual import Geometry,add,scale,sub,norm,rows,render_point

def verify(solution,sides):
    a,b,c=map(int,sides);N=(a+2*b)*(2*a+b)
    board=((Q(0),Q(0)),(Q(b*(2*a+b)),Q(0)),(Q(0),Q(a*(a+2*b))))
    geom=Geometry((a,b,c),board,True)
    triangles=[];boundary=Counter()
    for key,weight in solution:
        if abs(float(weight))<1e-7:continue
        if abs(float(weight)-1)>1e-7:raise ValueError('The candidate remains fractional.')
        point,h,j,hand=key;x,y,e=map(int,point)
        if hand not in (-1,1):raise ValueError('Bad tile hand.')
        p=(Q(x,c**e),Q(y,c**e))
        T=tuple(sorted((p,add(p,scale(-a,geom.unit(int(h),int(j)))),add(p,scale(b,geom.unit(int(h),int(j)+int(hand)))))))
        assert sorted(norm(sub(T[i],T[(i+1)%3])) for i in range(3))==geom.metric
        assert geom.admissible(T)
        triangles.append(T);boundary.update(rows(T))
    assert len(triangles)==N,(len(triangles),N)
    assert len(set(triangles))==N
    assert {r:w for r,w in boundary.items() if w}==rows(board)
    # Exact oriented boundary equality for positive triangles proves coverage
    # and disjoint interiors by winding number, including arbitrary T-junctions.
    return dict(sides=[a,b,c],N=N,board=[render_point(p) for p in board],triangles=[[render_point(p) for p in T] for T in triangles],verified=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('solution',type=Path);ap.add_argument('a',type=int);ap.add_argument('b',type=int);ap.add_argument('c',type=int);ap.add_argument('--output',type=Path)
    args=ap.parse_args();out=verify(json.loads(args.solution.read_text()),(args.a,args.b,args.c))
    if args.output:args.output.write_text(json.dumps(out,separators=(',',':'))+'\n')
    print('Exact positive tiling verified:',out['N'],'tiles')
if __name__=='__main__':main()
