#!/usr/bin/env python3
"""Exact small checks accompanying two general proofs; read-only by default."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def fan_check(t):
    lengths = [F(2), F(2), t, F(2), F(2), 1-t, F(2), t, 1-t]
    sectors = []
    start = F(0)
    for length in lengths:
        end = start + length
        pieces = []
        for period in range(2):
            lo, hi = max(start, 6*period), min(end, 6*(period+1))
            if lo < hi:
                pieces.append((lo-6*period, hi-6*period))
        sectors.append(pieces)
        start = end
    assert start == 12
    cuts = sorted({x for sec in sectors for piece in sec for x in piece})
    for lo, hi in zip(cuts, cuts[1:]):
        mid = (lo+hi)/2
        assert sum(any(a < mid < b for a,b in sec) for sec in sectors) == 2
    selected = (0,1,3,4,6)
    edges = set()
    for k,i in enumerate(selected):
        for j in selected[k+1:]:
            if any(max(a,c) < min(b,d) for a,b in sectors[i] for c,d in sectors[j]):
                edges.add((i,j))
    assert edges == {(0,3),(0,4),(1,4),(1,6),(3,6)}
    for coloring in range(1 << 5):
        colors = {v:(coloring >> k) & 1 for k,v in enumerate(selected)}
        assert any(colors[i] == colors[j] for i,j in edges)
    return {'alpha_over_60':str(t), 'multiplicity':2, 'induced_cycle':[0,4,1,6,3]}


P = 3
ONE = (0,0,0)


def mul(x,y):
    return ((x[0]+y[0])%P, (x[1]+y[1])%P, (x[2]+y[2]+x[0]*y[1])%P)


def power(x,k):
    out = ONE
    for _ in range(k%P):
        out = mul(out,x)
    return out


def edge(h,j):
    generators = [(1,0,0),(0,1,0),ONE]
    r = (j+h)%6
    g = generators[r%3]
    if r >= 3:
        g = power(g,-1)
    return power(g,1 if h%2 == 0 else -1)


def heisenberg_check():
    a,b,c = 24,11,31
    assert mul((1,0,0),(0,1,0)) != mul((0,1,0),(1,0,0))
    tested = 0
    for h in range(-6,7):
        for j in range(6):
            assert edge(h,j+3) == power(edge(h,j),-1)
            assert mul(power(edge(h,j),a),power(edge(h,j+1),b)) == power(edge(h+1,j),c)
            assert mul(power(edge(h,j),a),power(edge(h,j-1),b)) == power(edge(h-1,j),c)
            tested += 2
    for m in (1,2,3):
        out = mul(power(edge(0,0),m*c*c),power(edge(2,1),3*m*b*(a+b)))
        out = mul(out,power(edge(3,0),-m*c*(a+2*b)))
        assert out == ONE
    return {'tile':[a,b,c], 'group_order':27, 'group_exponent':3,
            'nonabelian':True, 'tile_relations_checked':tested,
            'F3_scales_checked':[1,2,3]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args = parser.parse_args()
    result = {'status':'PASS', 'local_fans':[fan_check(t) for t in (F(1,7),F(1,2),F(6,7))],
              'nonabelian_quotient':heisenberg_check(),
              'whole_triangle_multiple_cover_constructed':False,
              'full_Erdos634_solved':False}
    content = json.dumps(result,indent=2)+'\n'
    if args.report is not None:
        args.report.write_text(content)
    print(content,end='')


if __name__ == '__main__':
    main()
