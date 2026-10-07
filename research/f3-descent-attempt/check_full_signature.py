#!/usr/bin/env python3
"""Exact symbolic F3 edge-signature identity; not a geometric tiling test.

The coefficient ring is Z[a,b,c,T,X,X^-1] modulo c²-a²-ab-b²,T³+1.
Default execution is read-only; --report optionally saves deterministic JSON.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path


def add(*polys):
    out = defaultdict(int)
    for p in polys:
        for key, value in p.items():
            out[key] += value
    return {k: v for k, v in out.items() if v}


def term(value=1, a=0, b=0, c=0, t=0, x=0):
    if c >= 2:
        return add(term(value,a+2,b,c-2,t,x),
                   term(value,a+1,b+1,c-2,t,x),
                   term(value,a,b+2,c-2,t,x))
    quotient, remainder = divmod(t, 3)
    return {(a,b,c,remainder,x): value*(-1)**quotient} if value else {}


def mul(p, q):
    return add(*(term(v*w, *(k[i]+j[i] for i in range(5)))
                 for k,v in p.items() for j,w in q.items()))


def replay():
    one,a,b,c,T,X,Xinv = (term(),term(a=1),term(b=1),term(c=1),
                         term(t=1),term(x=1),term(x=-1))
    minus = term(-1)
    delta = add(a,mul(minus,b))
    h = add(a,mul(term(2),b))
    P = add(a,mul(b,T),mul(minus,mul(c,X)))
    Q = add(mul(minus,a),mul(b,mul(T,T)),mul(c,Xinv))
    U = add(mul(c,mul(add(one,mul(minus,T)),X)),mul(h,mul(X,X)))
    V = add(mul(c,X),mul(delta,mul(T,mul(X,X))))
    X2 = mul(X,X)
    X3 = mul(X2,X)
    side2 = mul(term(3),mul(b,mul(add(a,b),mul(T,X2))))
    side3 = mul(minus,mul(c,mul(h,X3)))
    target = add(mul(c,c),side2,side3)
    discrepancy = add(mul(U,P),mul(V,Q),mul(minus,target))
    if discrepancy:
        raise ValueError(discrepancy)
    fixtures=[]
    for aa,bb,cc in [(8,7,13),(24,11,31),(5,3,7)]:
        count=3*(aa+2*bb)*(aa+bb)
        short=3*cc+2*aa+bb
        if (count-short)%2 or count<short:
            raise ValueError('Invalid padding.')
        fixtures.append({'tile':[aa,bb,cc],'target_count':count,
                         'unplaced_orientation_inventory_count':short,
                         'half_turn_pairs':(count-short)//2,
                         'short_height_populations':{'1':3*cc,'2':count-3*cc}})
    return {'status':'PASS','symbolic_remainder_terms':len(discrepancy),
            'fixtures':fixtures,'geometric_tiling_claimed':False,
            'full_Erdos634_solved':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    output=json.dumps(replay(),indent=2)+'\n'
    if args.report is not None:args.report.write_text(output)
    print(output,end='')
