#!/usr/bin/env python3
"""Finite exact checks of the elliptic maps and the class-number sector.

Universal statements require the accompanying proofs and cited theorems;
finite point/parameter samples are not substituted for those arguments.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import importlib.util
import json
from math import gcd, isqrt
import os
from pathlib import Path
import sys
import elliptic
import sector

if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
    raise SystemExit('Run ordinary Python without optimization.')


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('invalid input was accepted')


def decomposition(n):
    d = s = 1
    for p, e in sector.tails.factor(n).items():
        d *= p**(e % 2)
        s *= p**(e//2)
    return d, s


def check_forms():
    known = {-3: 1, -4: 1, -7: 1, -8: 1, -11: 1, -19: 1,
             -23: 3, -43: 1, -52: 2, -67: 1, -88: 2, -163: 1}
    for delta, h in known.items():
        require(len(sector.reduced_forms(delta)) == h, f'class number {delta}')
    require(sector.reduced_forms(-88) == [[1, 0, 22], [2, 0, 11]], 'tiny rank certificate')
    compared = 0
    for d in range(2, 1001, 2):
        if any(e > 1 for e in sector.tails.factor(d).values()):
            continue
        delta, direct = -4*d, set()
        # Independent b-first/divisor enumeration, using a deliberately
        # larger bound sqrt(|delta|); compare complete representative sets.
        for b in range(-isqrt(-delta), isqrt(-delta)+1):
            if (b*b-delta) % 4:
                continue
            M = (b*b-delta)//4
            for a in sector.tails.divisors(M):
                c = M//a
                if abs(b) > a or a > c or gcd(gcd(a, b), c) != 1:
                    continue
                if b < 0 and (abs(b) == a or a == c):
                    continue
                direct.add((a, b, c))
        require(set(map(tuple, sector.reduced_forms(delta))) == direct, 'form enumeration disagreement')
        compared += 1
    for delta in [0, 4, -12, -16, -20*4, -5, True]:
        rejected(lambda delta=delta: sector.reduced_forms(delta))
    return dict(known_class_numbers=len(known), complete_form_comparisons=compared)


def check_maps():
    count = 0
    for a in range(1, 101):
        for b in range(1, 101):
            if gcd(a, b) != 1:
                continue
            c = isqrt(a*a+a*b+b*b)
            if c*c != a*a+a*b+b*b:
                continue
            D = 3*(a+2*b)*(a+b)
            d, s = decomposition(D)
            P = elliptic.forward_f3(d, a, b, c)
            witness = elliptic.reverse_f3(d, P)
            require([witness[q] for q in ['a', 'b', 'c', 's']] == [a, b, c, s], 'F3 roundtrip')
            K = 3*d
            require(elliptic.on_curve(K, P) and 0 < P[0] < K, 'F3 point cone')
            doubled = elliptic.add(K, P, P)
            u, v = P
            w = (u*u+2*K*u-2*K*K)/(2*v)
            require(doubled[0]+K == w*w, 'square lift doubling identity')
            require(elliptic.mul(K, 3, P) == elliptic.add(K, doubled, P), 'group law consistency')
            require(elliptic.add(K, P, (u, -v)) is None, 'inverse law')
            # Check the explicit degree-three map to y²=x³-d³.
            xx = (u**3+108*d**3)/(9*u*u)
            yy = v*(u**3-216*d**3)/(27*u**3)
            require(yy*yy == xx**3-d**3, '3-isogeny identity')
            # Independent birational quartic coordinates and 2-isogeny.
            k = elliptic.squarefree_kernel(3*d)
            T, ww = F(a+2*b, a+b), F(c, a+b)
            z = elliptic.rational_sqrt(T/k)
            require(z is not None, 'quartic square lift')
            x = k*(2*ww+2*T-3)
            y = 2*k*x*z
            require(y*y == x**3+6*k*x*x-3*k*k*x, 'quartic model identity')
            R = elliptic.dual_isogeny(k, (x, y))
            require(elliptic.on_curve(k, R), 'dual 2-isogeny')
            require(0 < R[0] < k and elliptic.rational_sqrt(R[0]+k) is not None, 'isogenous cone')
            count += 1
    found = elliptic.f3_from_generator(6, (9, 81), max_steps=20)
    require(found['status'] == 'FOUND', 'constructive search')
    budget = elliptic.f3_from_generator(6, (9, 81), max_steps=0)
    require(budget['status'] == 'INCOMPLETE', 'zero budget cannot exclude')
    for K, P, order in [(66, None, 1), (66, (-66, 0), 2),
                        (9, (0, 27), 3), (9, (18, 81), 6)]:
        require(elliptic.torsion_order(K, P) == order, 'torsion classification')
    invalid = [lambda: elliptic.f3_from_generator(22, (-66, 0)),
               lambda: elliptic.f3_from_generator(3, (0, 27)),
               lambda: elliptic.f3_from_generator(6, (9., 81.)),
               lambda: elliptic.reverse_f3(6, (0, 0)),
               lambda: elliptic.forward_f3(22, 8, 7, 13),
               lambda: elliptic.forward_f3(110, 16, 14, 26),
               lambda: elliptic.f3_from_generator(24, (0, 0))]
    for fn in invalid:
        rejected(fn)
    return dict(primitive_norm_roundtrips=count, generator_search_steps=found['steps'],
                torsion_cases=4, invalid_cases=len(invalid),
                generated_primitive_coefficient_verified=True)


def check_qp():
    dmax, mmax = 1000, 31
    bound, forward = dmax*mmax*mmax, set()
    # Primitive QP>v^4 supplies a complete forward parameter bound.
    primitive = 0
    for v in range(2, isqrt(isqrt(bound))+1):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            Q, P = 2*v*v-u*u, 3*v*v-u*u
            D = Q*P
            if D > bound:
                continue
            primitive += 1
            d, s = decomposition(D)
            if d > dmax or d % 16 != 6 or s % 2 == 0:
                continue
            for t in range(1, mmax//s+1, 2):
                forward.add((d, s*t))
    compared = 0
    for d in range(6, dmax+1, 16):
        if any(e > 1 for e in sector.tails.factor(d).values()):
            continue
        for m in range(1, mmax+1, 2):
            result = sector.qp_witness(d, m)
            require((result['witness'] is not None) == ((d, m) in forward), 'QP inverse vs forward')
            triple = sector.qp_witness(d, 3*m)
            require((triple['witness'] is not None) == (result['witness'] is not None), 'QP 3-saturation')
            compared += 1
    # Necessary alpha allocations, specifically including 3 in coefficients.
    alpha_count = alpha_with_3 = 0
    for v in range(2, 101):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            b, Q = v*v-u*u, 2*v*v-u*u
            d, s = decomposition(b*Q)
            if d % 16 != 6 or s % 2 == 0:
                continue
            A, _ = decomposition(Q//2)
            B, _ = decomposition(b)
            require(dict(A=A, B=B) in sector.alpha_partitions(d), 'alpha sieve false exclusion')
            alpha_count += 1
            alpha_with_3 += int((d*s) % 3 == 0)
    return dict(forward_coefficient_bound=bound, primitive_QP_pairs=primitive,
                complete_QP_input_comparisons=compared, alpha_candidates=alpha_count,
                alpha_candidates_divisible_by_3=alpha_with_3)


def check_scope():
    path = Path(__file__).resolve().parents[1] / 'composite-support'
    sys.path.insert(0, str(path))
    spec = importlib.util.spec_from_file_location('prior_class22', path/'classify22.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    cases = list(range(1, 102)) + [248599631, 3*248599631, 9*248599631]
    for m in cases:
        r = sector.classify(22, m)
        require(r['status'] == old.classify(m)['status'], 'prior complete class22 disagreement')
        require(r['full_Erdos634_solved'] is False, 'scope flag')
    require(sector.rank_zero_certificate(118)['certified'] is False, 'noncertifying class number')
    require(sector.classify(118, 1)['status'] == 'NOT_COVERED', 'h divisible by3 is not rank proof')
    require(sector.classify(70, 1)['status'] == 'NOT_COVERED', 'alpha survivor is not excluded')
    require(sector.classify(166, 2)['status'] == 'NOT_COVERED', 'missing even seed is not excluded')
    require(sector.classify(110, 3)['status'] == 'NOT_COVERED', 'old unresolved geometry retained')
    require(sector.classify(6, 1)['status'] == 'NOT_COVERED', 'classical 6 not falsely excluded')
    for d, m in [(0, 1), (88, 1), (22, 0), (22, -1), (True, 1), (22, 1.0)]:
        rejected(lambda d=d, m=m: sector.classify(d, m))
    return dict(prior_class22_comparisons=len(cases), scope_controls=5, invalid_cases=6)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = dict(status='PASS', forms=check_forms(), maps=check_maps(),
                  allocation=check_qp(), scope=check_scope(),
                  full_Erdos634_solved=False, general_rank_algorithm=False,
                  Mordell_Weil_bases_computed=False,
                  boundary='Exact finite regression; universal theorems require written proofs and cited inputs.')
    content = json.dumps(result, indent=2)+'\n'
    if args.report:
        args.report.write_text(content)
    print(content, end='')


if __name__ == '__main__':
    main()
