#!/usr/bin/env python3
"""Exact tests of the fixed-degree moment barrier; no tiling decision."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import json


def edge_integral(p, q, r, s):
    """Integral x^r y^s dt; constant edge length is immaterial here."""
    dx, dy = q[0]-p[0], q[1]-p[1]
    return sum((F(comb(r, i)*comb(s, k)
                    * p[0]**(r-i)*p[1]**(s-k)*dx**i*dy**k,
                    i+k+1)
                for i in range(r+1) for k in range(s+1)), F(0))


def area_integral(j, r, s):
    """Integral over conv((j,0),(j+1,0),(j,1))."""
    return sum((F(comb(r, k)*j**(r-k)*factorial(k)*factorial(s),
                  factorial(k+s+2)) for k in range(r+1)), F(0))


def check_degree(d):
    M = 2**(d+1)
    signs = [(-1)**j.bit_count() for j in range(M)]
    assert signs.count(1) == signs.count(-1) == M//2
    assert all(1+e in (0,2) for e in signs)
    assert sum(signs) == 0
    for r in range(d+1):
        assert sum(e*j**r for j,e in enumerate(signs)) == 0
    tests = 0
    for r in range(d+1):
        for s in range(d+1-r):
            assert sum((e*area_integral(j,r,s)
                        for j,e in enumerate(signs)),F(0)) == 0
            for edge in range(3):
                total = F(0)
                for j,e in enumerate(signs):
                    vertices = [(j,0),(j+1,0),(j,1)]
                    total += e*edge_integral(vertices[edge],
                                             vertices[(edge+1)%3],r,s)
                assert total == 0
            tests += 4
    # All row vertices are in x>=0,y>=0,x+y<=M; their interiors
    # are pairwise disjoint. Each deleted/duplicated tile contributes
    # exactly its area to the squared density discrepancy.
    for j in range(M):
        for x,y in [(j,0),(j+1,0),(j,1)]:
            assert x >= 0 and y >= 0 and x+y <= M
    return {"degree":d,"row_length":M,"count":M*M,
            "holes":M//2,"identical_pairs":M//2,
            "energy_in_tile_areas":M,"moment_equalities":tests}


def polynomial_value(p, x):
    value = F(0)
    for coefficient in reversed(p):
        value = value*x+coefficient
    return value


def root_power_sums(p, max_degree):
    """Newton identities, for a monic ascending-coefficient polynomial."""
    M = len(p)-1
    assert p[-1] == 1 and max_degree < M
    sums = [F(M)]
    for r in range(1,max_degree+1):
        sums.append(-sum((p[M-k]*sums[r-k]
                          for k in range(1,r)),F(0))-r*p[M-r])
    return sums


def check_distinct_degree(d):
    M = d+1
    p = [F(1)]
    for j in range(1,M+1):
        new = [F(0)]*(len(p)+1)
        for k,c in enumerate(p):
            new[k] -= j*c
            new[k+1] += c
        p = new
    epsilon = F(1,2*4**M)
    q = p.copy()
    q[0] += epsilon
    for j in range(1,M+1):
        lo,hi = F(j)-F(1,4),F(j)+F(1,4)
        plo,phi = polynomial_value(p,lo),polynomial_value(p,hi)
        qlo,qhi = polynomial_value(q,lo),polynomial_value(q,hi)
        assert abs(plo) >= F(1,4**M) > epsilon
        assert abs(phi) >= F(1,4**M) > epsilon
        assert plo*qlo > 0 and phi*qhi > 0 and qlo*qhi < 0
        assert polynomial_value(q,F(j)) == epsilon
        assert lo > 0 and hi+1 < M+2
    expected = [F(sum(j**r for j in range(1,M+1)))
                for r in range(d+1)]
    assert root_power_sums(p,d) == root_power_sums(q,d) == expected
    return {"degree":d,"count":(d+3)**2,"moved_tiles":M,
            "disjoint_exact_root_brackets":M,
            "newton_moments_checked":d+1,"all_placements_distinct":True}


def run():
    cases = [check_degree(d) for d in range(7)]
    distinct_cases = [check_distinct_degree(d) for d in range(21)]
    source = Path(__file__).parents[1]/"f3-moments-oct7/exact-4830.json"
    data = json.loads(source.read_text())
    ns = [t["multiplicity"] for t in data["types"]]
    assert sum(ns) == 4830
    lower = sum(n*(n-1) for n in ns)
    assert lower == 11157206
    return {"status":"PASS","full_Erdos634_solved":False,
            "theorem_scope":"Fixed-degree moments do not certify displayed placements; no untileable target is produced.",
            "cases":cases,"witness_4830_energy_lower_in_tile_areas":lower,
            "distinct_placement_cases":distinct_cases,
            "decides_154":False,"decides_4830":False}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O: verification uses assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path)
    args = parser.parse_args()
    text = json.dumps(run(),indent=2,sort_keys=True)+"\n"
    if args.report:
        args.report.write_text(text)
    print(text,end="")
