#!/usr/bin/env python3
"""Exact odd-multiplier decisions in a certified class-number sector.

Uses the written theorem in docs/elliptic-square-classes.md. A failed
sufficient rank certificate returns NOT_COVERED, never a rank assertion.
Trial division and reduced binary quadratic forms are finite, not optimized
for very large inputs. The general elliptic-rank problem is not implemented.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from math import gcd, isqrt
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / 'square-class-tails' / 'classify.py'
_spec = importlib.util.spec_from_file_location('elliptic_sector_tails', _path)
tails = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tails)


def positive_integer(n, name):
    if type(n) is not int or n < 1:
        raise ValueError(f'{name} must be a positive integer')


def validate_kernel(d):
    positive_integer(d, 'd')
    return tails.validate_kernel(d)


def reduced_forms(delta):
    """All primitive reduced positive forms of a negative fundamental delta.

    Representatives obey |b|<=a<=c, b>=0 on either boundary. Reduction
    theory gives a<=sqrt(|delta|/3), so this is a complete enumeration.
    """
    if type(delta) is not int or delta >= 0:
        raise ValueError('negative fundamental discriminant required')
    if delta % 4 == 1:
        kernel = -delta
    elif delta % 4 == 0 and (delta//4) % 4 in (2, 3):
        kernel = -delta//4
    else:
        raise ValueError('not a fundamental discriminant')
    if any(e != 1 for e in tails.factor(kernel).values()):
        raise ValueError('not a fundamental discriminant')
    out = []
    for a in range(1, isqrt((-delta)//3) + 1):
        for b in range(-a, a+1):
            numerator = b*b-delta
            if numerator % (4*a):
                continue
            c = numerator//(4*a)
            if c < a or gcd(gcd(a, b), c) != 1:
                continue
            if (abs(b) == a or a == c) and b < 0:
                continue
            out.append([a, b, c])
    return out


def rank_zero_certificate(d):
    validate_kernel(d)
    base = dict(d=d, curve=f'Y^2=X^3+({3*d})^3',
                theorem='Stoll 1998 Corollary 2.1, as stated in Chang Theorem 1.1')
    if d % 2 or d % 3 != 1:
        return dict(base, certified=False, reason='requires even d congruent to 1 modulo 3')
    forms = reduced_forms(-4*d)
    h = len(forms)
    return dict(base, certified=(h % 3 != 0), discriminant=-4*d,
                class_number=h, reduced_forms=forms,
                reason='3 does not divide the class number' if h % 3 else
                       'class-number bound does not certify rank zero')


def alpha_partitions(d):
    """Necessary alpha allocations; valid also when 3 divides d or m."""
    fs = validate_kernel(d)
    if d % 16 != 6:
        raise ValueError('alpha sector requires d congruent to 6 modulo 16')
    D = d//2
    out = []
    for A in tails.divisors(D):
        B = D//A
        if A % 8 != 7 or B % 8 != 5:
            continue
        if any(pow(2, (p-1)//2, p) != 1 or pow(-B, (p-1)//2, p) != 1
               for p in fs if A % p == 0):
            continue
        if any(pow(2*A, (p-1)//2, p) != 1
               for p in fs if B % p == 0):
            continue
        out.append(dict(A=A, B=B))
    return out


def square_allocations(m):
    """For each p|m, send its chosen square block to x, y, or neither."""
    out = [(1, 1)]
    for p, e in sorted(tails.factor(m).items()):
        out = [pair for x, y in out for pair in
               ([(x, y)] + [(x*p**r, y) for r in range(1, e+1)]
                         + [(x, y*p**r) for r in range(1, e+1)])]
    return out


def qp_witness(d, m):
    """Finite exact QP test in d=6 mod16, m odd; no elliptic assumption.

    Absence alone is NOT global nonexistence without the sector hypotheses.
    Powers of 3 are removed only from coefficient allocation, not scale.
    """
    validate_kernel(d)
    positive_integer(m, 'm')
    if d % 16 != 6 or m % 2 == 0:
        raise ValueError('requires d=6 mod16 and odd m')
    core = m
    while core % 3 == 0:
        core //= 3
    blocks = square_allocations(core)
    tried = 0
    for A in tails.divisors(d//2):
        B = d//(2*A)
        if A % 8 != 1 or B % 8 != 3:
            continue
        for x, y in blocks:
            tried += 1
            Q, P = 2*A*x*x, B*y*y
            if gcd(Q, P) != 1 or not 3*Q < 2*P < 4*Q:
                continue
            v, u = tails.root(P-Q), tails.root(2*P-3*Q)
            if v is None or u is None:
                continue
            if not (0 < u < v and gcd(u, v) == 1):
                raise ArithmeticError('primitive QP reconstruction failed')
            t, b = m//(x*y), v*v-u*u
            return dict(witness=dict(branch='QP', A=A, B=B, x=x, y=y,
                        u=u, v=v, Q=Q, P=P, t=t,
                        tile_sides=[u*v, b, v*v],
                        target_sides=[t*v**4, t*v*v*Q, t*b*P]),
                        allocations_checked=tried)
    return dict(witness=None, allocations_checked=tried)


def even_seed(d):
    """Sufficient old oriented F4 seed, not a necessary test for 4d."""
    validate_kernel(d)
    for w in tails.product_witnesses(4*d):
        if w['branch'] == 'F4' and w['a'] < w['b']:
            return w
    return None


def classify(d, m):
    validate_kernel(d)
    positive_integer(m, 'm')
    out = dict(d=d, m=m, N=d*m*m,
               proof='docs/elliptic-square-classes.md', full_Erdos634_solved=False)
    if m % 2 == 0:
        seed = even_seed(d)
        if seed:
            return dict(out, status='YES', witness=dict(seed, t=m//2),
                        reason='existing oriented F4 construction and refinement')
        return dict(out, status='NOT_COVERED', reason='even F4 seed test failed; not an exclusion')
    if d % 16 != 6:
        return dict(out, status='NOT_COVERED', reason='odd sector requires d=6 modulo 16')
    cert = rank_zero_certificate(d)
    out['rank_certificate'] = cert
    if not cert['certified']:
        return dict(out, status='NOT_COVERED', reason='rank zero not certified by this sufficient test')
    partitions = alpha_partitions(d)
    out['alpha_partitions'] = partitions
    if partitions:
        return dict(out, status='NOT_COVERED', reason='alpha local sieve survives; not an existence claim')
    result = qp_witness(d, m)
    return dict(out, **result, status='YES' if result['witness'] else 'NO',
                reason='complete odd-sector theorem and finite QP allocation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('d', type=int)
    parser.add_argument('m', type=int, nargs='+')
    args = parser.parse_args()
    try:
        result = [classify(args.d, m) for m in args.m]
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
