#!/usr/bin/env python3
"""Complete exact test for N=22*m^2, m positive.

Uses the written square-class-22 theorem, including its established elliptic
rank input. The program enumerates prime allocations, not geometric tilings.
"""
import argparse
import json
from math import gcd
import allocate


def allocations(fs):
    """Each prime power is unused or assigned wholly to x or wholly to y."""
    out=[(1,1)]
    for p,e in sorted(fs.items()):
        out=[pair for x,y in out for pair in
             ([(x,y)]+[(x*p**r,y) for r in range(1,e+1)]
                      +[(x,y*p**r) for r in range(1,e+1)])]
    return out


def classify(m):
    if m<1:
        raise ValueError('m must be a positive integer')
    base=dict(m=m,N=22*m*m,scope='complete square class 22; all positive multipliers',
              proof='docs/square-class-22.md',full_Erdos634_solved=False)
    if m%2==0:
        t=m//2
        return dict(base,status='YES',witness=dict(branch='F4',a=3,b=5,c=7,
                    primitive_coefficient=88,t=t,target_sides=[21*t,55*t,56*t],
                    construction='old 88-tile dissection followed by quadratic refinement'))
    tried=0
    for x,y in allocations(allocate.tails.factor(m)):
        tried+=1
        if x%11==0 or not 3*x*x<11*y*y<4*x*x:
            continue
        v=allocate.tails.root(11*y*y-2*x*x)
        u=allocate.tails.root(22*y*y-6*x*x)
        if u is None or v is None:
            continue
        if not (0<u<v and gcd(x,y)==gcd(u,v)==1):
            raise RuntimeError('unexpected primitive inverse failure')
        Q,P=2*x*x,11*y*y
        t=m//(x*y)
        b=v*v-u*u
        return dict(base,status='YES',witness=dict(branch='QP',x=x,y=y,u=u,v=v,
                    Q=Q,P=P,t=t,tile_sides=[u*v,b,v*v],
                    target_sides=[t*v**4,t*v*v*Q,t*b*P],
                    construction='existing QP dissection at every positive multiplier'),
                    allocations_checked=tried)
    return dict(base,status='NO',witness=None,allocations_checked=tried,
                exclusion='complete coefficient allocation plus the written all-branch theorem')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('m',type=int,nargs='+')
    args=parser.parse_args()
    try:
        result=[classify(m) for m in args.m]
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
