#!/usr/bin/env python3
"""Exact L(E,1)>0 certificate for E: y^2=x^3+287496.

Inputs: conductor 69696=264^2 and global root number +1, from the
rigorous local data for LMFDB 69696.ej4 / Cremona 69696o3.  This program
does not compute the conductor or root number.  Modularity and the
rank-zero theorem then imply rank E(Q)=0.  The numerical certificate
uses integer interval arithmetic only; no floating-point operations.
By default verification is read-only; --report writes its JSON result.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


SCALE = 10**30
CUTOFF = 500
CONDUCTOR = 69696
ROOT_NUMBER = 1
A6 = 287496


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def atan_bounds(q: int, count: int) -> tuple[Fraction, Fraction]:
    """Alternating-series bounds for atan(1/q), count even."""
    assert q > 1 and count > 0 and count % 2 == 0
    lower = sum((Fraction((-1)**j, (2*j+1)*q**(2*j+1))
                 for j in range(count)), Fraction(0))
    upper = lower + Fraction(1, (2*count+1)*q**(2*count+1))
    return lower, upper


def exp_minus_bounds(x: Fraction, count: int = 12) -> tuple[Fraction, Fraction]:
    """Bounds from the alternating exponential series, 0 < x < 1."""
    assert 0 < x < 1 and count > 0 and count % 2 == 0
    term = Fraction(1)
    total = term
    for j in range(1, count):
        term *= -x / j
        total += term
    lower = total
    upper = lower + term * (-x / count)
    return lower, upper


def q_bounds() -> tuple[int, int]:
    """Bounds for exp(-pi/132), denominator SCALE.

    Machin's identity pi=16 atan(1/5)-4 atan(1/239) is exact.
    """
    a_lo, a_hi = atan_bounds(5, 12)
    b_lo, b_hi = atan_bounds(239, 4)
    pi_lo, pi_hi = 16*a_lo-4*b_hi, 16*a_hi-4*b_lo
    e_lo = exp_minus_bounds(pi_hi/132)[0]
    e_hi = exp_minus_bounds(pi_lo/132)[1]
    return ((e_lo.numerator*SCALE)//e_lo.denominator,
            ceil_div(e_hi.numerator*SCALE, e_hi.denominator))


def point_count(p: int) -> int:
    # All callers supply primes of good reduction. Count y from the
    # quadratic-character criterion, including zero separately.
    result = 1
    for x in range(p):
        value = (x*x*x+A6) % p
        result += 1 if value == 0 else (2 if pow(value, (p-1)//2, p) == 1 else 0)
    return result


def coefficients(limit: int) -> list[int]:
    """Exact Euler coefficients, with additive reduction at 2,3,11."""
    spf = list(range(limit+1))
    for p in range(2, limit+1):
        if spf[p] == p:
            for n in range(p*p, limit+1, p):
                if spf[n] == n:
                    spf[n] = p
    ap = {p: (0 if CONDUCTOR % p == 0 else p+1-point_count(p))
          for p in range(2, limit+1) if spf[p] == p}
    result = [0]*(limit+1)
    result[1] = 1
    for n in range(2, limit+1):
        p = spf[n]
        n1 = n//p
        result[n] = ap[p]*result[n1]
        if n1 % p == 0 and CONDUCTOR % p:
            result[n] -= p*result[n1//p]
    return result


def decimal(n: int) -> str:
    sign = '-' if n < 0 else ''
    n = abs(n)
    return f'{sign}{n//SCALE}.{n%SCALE:030d}'


def verify() -> dict:
    assert CONDUCTOR == 264**2 and ROOT_NUMBER == 1
    q_lo, q_hi = q_bounds()
    assert 0 < q_lo <= q_hi < SCALE
    a = coefficients(CUTOFF)
    # Cross-check the first terms with direct counts; the complete
    # coefficient vector is computed independently of the source tables.
    assert (point_count(5), point_count(7)) == (6, 4)
    assert a[2] == a[3] == a[11] == 0
    lo = hi = 0
    power_lo = power_hi = SCALE
    for n in range(1, CUTOFF+1):
        power_lo = (power_lo*q_lo)//SCALE
        power_hi = ceil_div(power_hi*q_hi, SCALE)
        left, right = 2*a[n]*power_lo, 2*a[n]*power_hi
        lo += min(left, right)//n
        hi += ceil_div(max(left, right), n)
    next_power_hi = ceil_div(power_hi*q_hi, SCALE)
    # Deligne/Hasse bound |a_n| <= tau(n)*sqrt(n) <= 2n gives
    # |2 sum_{n>K} a_n q^n/n| <= 4q^(K+1)/(1-q).
    tail_hi = ceil_div(4*next_power_hi*SCALE, SCALE-q_hi)
    lower, upper = lo-tail_hi, hi+tail_hi
    assert lower > 0
    # Good reduction at 5 and 7 bounds rational torsion by gcd(6,4)=2;
    # (-66,0) realizes its nontrivial element.
    assert (-66)**3+A6 == 0
    return {
        'status': 'PASS',
        'curve': [0, 0, 0, 0, A6],
        'conductor_input': CONDUCTOR,
        'global_root_number_input': ROOT_NUMBER,
        'additive_primes_input': [2, 3, 11],
        'source': 'https://www.lmfdb.org/EllipticCurve/Q/69696/ej/4',
        'input_status': 'Conductor and local root/reduction types are cited, not recomputed.',
        'cutoff': CUTOFF,
        'arithmetic': 'Exact integer intervals; common denominator 10^30.',
        'q_lower': decimal(q_lo),
        'q_upper': decimal(q_hi),
        'partial_sum_lower': decimal(lo),
        'partial_sum_upper': decimal(hi),
        'tail_absolute_upper': decimal(tail_hi),
        'L_at_1_lower': decimal(lower),
        'L_at_1_upper': decimal(upper),
        'positive': True,
        'point_counts': {'5': 6, '7': 4},
        'rank_conclusion': '0 by modularity and the rank-zero theorem from L(E,1) != 0.',
        'rational_points_conclusion': ['O', [-66, 0]],
    }


def main() -> None:
    if not __debug__:
        raise SystemExit('Run without Python -O: assertions are part of verification.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = verify()
    data = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(data, encoding='utf-8')
    print(data, end='')


if __name__ == '__main__':
    main()
