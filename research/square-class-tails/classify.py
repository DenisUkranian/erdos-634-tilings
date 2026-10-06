#!/usr/bin/env python3
"""Finite square-class tail and odd-prime-power-ray tests.

These tests decide quantified tail/ray properties, NOT membership of an
arbitrary individual N. See ../../docs/square-class-tails.md for the proof.
Integer arithmetic only; trial division is exact but not optimized for huge d.
"""
from __future__ import annotations
import argparse
import json
from math import gcd, isqrt


def factor(n: int) -> dict[int, int]:
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors(n: int) -> list[int]:
    out = [1]
    for p, e in factor(n).items():
        out = [a * p ** k for a in out for k in range(e + 1)]
    return sorted(out)


def root(n: int) -> int | None:
    if n < 0:
        return None
    r = isqrt(n)
    return r if r * r == n else None


def ceildiv(a: int, b: int) -> int:
    return -(-a // b)


def validate_kernel(d: int) -> dict[int, int]:
    if d < 1:
        raise ValueError('d must be a positive squarefree integer')
    fs = factor(d)
    if any(e != 1 for e in fs.values()):
        raise ValueError('d must be squarefree')
    return fs


def product_witnesses(D: int) -> list[dict]:
    """All primitive witnesses to the nine product coefficient rows at D."""
    if D < 1:
        raise ValueError('coefficient must be positive')
    hits = {}

    def group(branch, u2, v2):
        u, v = root(u2), root(v2)
        if u is not None and v is not None and 0 < u < v and gcd(u, v) == 1:
            hits[(branch, u, v)] = dict(branch=branch, u=u, v=v, coefficient=D)

    def norm(branch, a, b, sign=1):
        if a <= 0 or b <= 0 or gcd(a, b) != 1:
            return
        c = root(a*a + sign*a*b + b*b)
        if c is not None:
            hits[(branch, a, b, c)] = dict(branch=branch, a=a, b=b, c=c, coefficient=D)

    for x in divisors(D):
        y = D // x
        group('alpha', y - 2*x, y - x)
        group('QP', 2*y - 3*x, y - x)
        norm('E60', x, y, -1)
        norm('E120', x, y)
        norm('F1', y - x, x)
        norm('I120', y - 2*x, x)
        if (2*y-x) % 3 == 0 and (2*x-y) % 3 == 0:
            norm('F2', (2*y-x)//3, (2*x-y)//3)
        norm('F4', y-x, 2*x-y)
    if D % 3 == 0:
        for x in divisors(D//3):
            y = D//(3*x)
            norm('F3', 2*x-y, y-x)
    return [hits[key] for key in sorted(hits)]


def theta_threshold(u: int, v: int) -> int:
    """Existing explicit seed + annuli bound, not a newly optimal cutoff."""
    a, b, c = u*v, v*v-u*u, v*v
    F = (b-1)*(c-1)
    S = a*a+b*b
    delta = b*S-a*a*c
    if delta > 0:
        return ceildiv((a*a*c+(a-1)*(b-1))*S, u*delta)
    if delta == 0:
        raise ValueError('unexpected zero Delta for primitive parameters')
    n = ceildiv(F-a*a*delta, b**3*c*c)
    seed = u*c*n*S
    H = ceildiv(a*a+b*b+F, u*b)
    return seed*ceildiv(H, seed)+(u-1)*(v-1)


def threshold(w: dict) -> int:
    branch = w['branch']
    if branch in ('classical', 'QP'):
        return 1
    if branch in ('W', 'beta'):
        return w['u']*w['v']-w['u']+1
    if branch == 'theta':
        return theta_threshold(w['u'], w['v'])
    if branch == 'alpha':
        return ceildiv(theta_threshold(w['u'], w['v']), w['v'])
    a, b = w['a'], w['b']
    A, B = max(a,b), min(a,b)
    if A == B:  # the sole primitive E60 equilateral case
        return 1
    M = 3*(A//B+(1 if branch == 'E60' else 2))
    return ceildiv(M,2) if branch in ('F2','F3') else M


def elementary_witnesses(d: int, fs: dict[int, int]) -> list[dict]:
    """Classical and the full signed W/beta norm tests for even d."""
    out = []
    if d in (1,2,3,6) or all(p % 4 == 1 for p in fs if p != 2):
        out.append(dict(branch='classical', coefficient=d))
    W = all(p % 8 in (1,7) for p in fs if p != 2)
    beta = (all(p % 12 in (1,11) for p in fs if p > 3)
            and (d % 3 == 2 if d % 3 else (d//3) % 3 == 1))
    if d > 2:
        for branch, compatible, k in [('W',W,2),('beta',beta,3)]:
            if not compatible or (branch == 'beta' and d == 3):
                continue
            before = len(out)
            for v in range(2,isqrt(d)+1):
                u = root(k*v*v-d)
                if u is not None and 0 < u < v and gcd(u,v) == 1:
                    out.append(dict(branch=branch,u=u,v=v,coefficient=d))
            if len(out) == before:
                raise RuntimeError('norm reduction witness missing')
    return out


def tail(d: int) -> dict:
    fs = validate_kernel(d)
    witnesses = elementary_witnesses(d,fs)
    if d % 2 and d > 1:
        witnesses.append(dict(branch='theta',u=(d-1)//2,v=(d+1)//2,coefficient=d))
    if d % 2 == 0:
        witnesses.extend(product_witnesses(d))
    for w in witnesses:
        w['sufficient_multiplier'] = threshold(w)
    if witnesses:
        w = min(witnesses,key=lambda w:w['sufficient_multiplier'])
        return dict(d=d,property='all sufficiently large multipliers are admissible',
                    status='COFINITE_TAIL',sufficient_multiplier=w['sufficient_multiplier'],
                    witness=w,all_witnesses=witnesses,exact_minimum_claimed=False,
                    full_Erdos634_solved=False)
    return dict(d=d,property='all sufficiently large odd multipliers are admissible',
                status='NOT_COFINITE',excluded_prime_power_rays='every prime q > 2*d, every exponent k >= 0',
                large_prime_cutoff=2*d,individual_composite_membership='NOT_DECIDED',
                full_Erdos634_solved=False)


def prime_power_ray(d: int, q: int) -> dict:
    fs = validate_kernel(d)
    if q < 3 or q % 2 == 0 or factor(q) != {q:1}:
        raise ValueError('q must be an odd prime')
    if d % 2:
        w = tail(d)['witness']
        witnesses = [dict(w,coefficient_exponent=0)]
    else:
        witnesses = [dict(w,coefficient_exponent=0) for w in elementary_witnesses(d,fs)]
        s,r = 1,0
        while s < 2*d:
            witnesses.extend(dict(w,coefficient_exponent=r) for w in product_witnesses(d*s*s))
            s *= q
            r += 1
    for w in witnesses:
        C = threshold(w)
        power,j = 1,0
        while power < C:
            power *= q
            j += 1
        w['sufficient_exponent'] = w['coefficient_exponent']+j
        w['sufficient_branch_multiplier'] = C
    base = dict(d=d,q=q,ray='N = d*q^(2*k), k >= 0',full_Erdos634_solved=False)
    if not witnesses:
        return dict(base,status='EMPTY_RAY',all_exponents_excluded=True)
    w = min(witnesses,key=lambda w:w['sufficient_exponent'])
    return dict(base,status='NONEMPTY_RAY',all_exponents_at_least=w['sufficient_exponent'],
                witness=w,earlier_exponents='NOT_DECIDED',exact_first_exponent_claimed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('d',type=int,nargs='+',help='positive squarefree kernels')
    parser.add_argument('--prime',type=int,help='test this odd-prime-power ray instead of cofinite tails')
    args = parser.parse_args()
    try:
        results = [tail(d) if args.prime is None else prime_power_ray(d,args.prime) for d in args.d]
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
