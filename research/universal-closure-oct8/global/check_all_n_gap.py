#!/usr/bin/env python3
"""Exact arithmetic audit, not a tiling decision or an infinite uniqueness claim."""
from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def factor(n):
    out = []
    p = 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def divisors_from_factorization(factors):
    out = [1]
    for p, e in factors:
        out = [d * p**j for d in out for j in range(e + 1)]
    return sorted(out)


def family(h):
    require(h >= 13 and h % 600 == 13, 'Wrong family parameter')
    a, b, c = (h*h-1)//3, (2*h+1)//3, (h*h+h+1)//3
    N = 3*(a+b)*(a+2*b)
    D, nested = b*b+2*a*b-a*a, b*c-a*a
    require(gcd(a, b) == 1 and c*c == a*a+a*b+b*b, 'Not primitive norm')
    require(3*N == h*(h+2)*(h*h+4*h+1), 'Wrong coefficient')
    require(N % 16 == 14 and N % 5 == 0 and N % 25 != 0, 'Isolation residues')
    require(9*D == -h**4+4*h**3+8*h*h-2 and D < 0, 'Mixed residual')
    require(9*nested == -h**4+2*h**3+5*h*h+3*h and nested < 0, 'Nested residual')
    require(a//b == (h-1)//2, 'Wrong ratio floor')
    tail = (3*(a//b+2)+1)//2
    require(tail == (3*(h+3)+3)//4 and tail >= 12, 'Wrong safe tail')
    require(1139*a > 2725*b and 2*a > 5*b and 4*a > 3*c, 'Sector comparison')
    return dict(h=h, count=N, tile=[a,b,c], multiplier=1,
                mixed_residual=D, nested_residual=nested,
                sufficient_F3_tail=tail)


def main():
    # These finite controls check arithmetic; the note proves the infinite claim.
    samples = [family(13+600*i) for i in range(10)]
    N = samples[0]['count']
    factors = factor(N)
    require(all(e == 1 for p, e in factors), '14430 not squarefree')
    require(N == 14430 and factors == [(2,1),(3,1),(5,1),(13,1),(37,1)], 'Factorization')
    pairs = []
    for V in divisors_from_factorization(factor(N//3)):
        U = (N//3)//V
        if not V < U < 2*V:
            continue
        a, b = 2*V-U, U-V
        s = a*a+a*b+b*b
        c = isqrt(s)
        pairs.append(dict(V=V, U=U, a=a, b=b, norm=s,
                          square=(c*c == s), c=c, primitive=(gcd(a,b)==1)))
    require(len(pairs) == 1 and (pairs[0]['V'], pairs[0]['U']) == (65,74), 'Divisor gate')
    require(pairs[0]['square'] and pairs[0]['primitive'], 'F3 norm gate')
    spec = importlib.util.spec_from_file_location(
        'all_n_gap_candidates', ROOT/'research/uniform-reduction/candidates.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    candidates = module.enumerate_candidates(N, remove_scale_one=False)
    require(module.classical(N) is None, 'Unexpected classical witness')
    require(len(candidates) == 1, 'Global gate not unique')
    candidate = candidates[0]
    require(candidate.branch == 'F3-120' and candidate.tile == (56,9,61)
            and candidate.target == (3721,4514,1755)
            and candidate.multiplier == 1, 'Wrong sole candidate')
    result = dict(status='PASS',
                  theorem='Infinite family is F3-branch-isolated; displayed scale-one corner criteria fail.',
                  sample_controls=samples,
                  fully_gated_count=N, factorization=factors,
                  independent_divisor_pairs=pairs,
                  complete_repository_candidates=[asdict(candidate)],
                  exclusions_disabled_in_global_gate='scale-one theta and double-angle removals',
                  count_14430_geometrically_decided=False,
                  infinite_candidate_uniqueness_claimed=False,
                  full_problem_solved=False)
    (HERE/'all_n_gap_checked.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], fully_gated_count=N,
                         candidate_count=len(candidates), samples=len(samples),
                         count_14430_geometrically_decided=False)))


if __name__ == '__main__':
    main()
