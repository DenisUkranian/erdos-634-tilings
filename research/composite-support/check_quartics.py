#!/usr/bin/env python3
"""Exact quartic and rational-conic checks for the fixed-prime-support reduction.

Only the Python standard library is used. Coefficients are integers, ordered
by increasing exponent of the first variable: [y^d, x*y^(d-1), ..., x^d].
The finite parameter regression supplements the written primitive-normalization
proof; it is not a proof of its universal quantifier or a Thue-Mahler solver.
"""
from __future__ import annotations
import argparse
import json
from math import gcd
from pathlib import Path

if not __debug__:
    raise SystemExit('Run this verifier without Python optimization (-O).')


def add(p, q):
    assert len(p) == len(q)
    return [a + b for a, b in zip(p, q)]


def scale(n, p):
    return [n * a for a in p]


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def value(p, x, y):
    d = len(p) - 1
    return sum(a * x**i * y**(d-i) for i, a in enumerate(p))


def binary_quartic_discriminant(p):
    """Discriminant of a*x^4+b*x^3*y+c*x^2*y^2+d*x*y^3+e*y^4.

    The homogeneous formula also handles a simple root at infinity (a=0).
    Do not substitute a degree-three univariate discriminant in that case.
    """
    assert len(p) == 5
    e, d, c, b, a = p
    return (256*a**3*e**3 - 192*a*a*b*d*e*e - 128*a*a*c*c*e*e
            + 144*a*a*c*d*d*e - 27*a*a*d**4 + 144*a*b*b*c*e*e
            - 6*a*b*b*d*d*e - 80*a*b*c*c*d*e + 18*a*b*c*d**3
            + 16*a*c**4*e - 4*a*c**3*d*d - 27*b**4*e*e
            + 18*b**3*c*d*e - 4*b**3*d**3 - 4*b*b*c**3*e
            + b*b*c*c*d*d)


def verify():
    # A=k^2-h^2; B_sigma=k(2h-sigma*k); C_sigma=h^2-sigma*h*k+k^2.
    A = [1, 0, -1]
    h = [0, 1]
    k = [1, 0]
    conics = []
    cases = 0
    g_counts = {1: 0, 3: 0}
    for sigma in (-1, 1):
        B = [-sigma, 2, 0]
        C = [1, -sigma, 1]
        L = [-sigma, 2]  # L=2h-sigma*k.
        residual = add(mul(C,C), scale(-1, add(add(mul(A,A),scale(sigma,mul(A,B))),mul(B,B))))
        assert residual == [0] * 5
        assert add(mul(k,add(C,scale(-1,A))),scale(-1,mul(h,B))) == [0]*4
        # 3h^2=A+4hL-L^2 and C=3h^2-3hL+L^2 support the gcd proof.
        assert add(add(A,scale(4,mul(h,L))),scale(-1,mul(L,L))) == [0,0,3]
        assert C == add(add([0,0,3],scale(-3,mul(h,L))),mul(L,L))
        local = 0
        for kk in range(1,201):
            for hh in range(-kk,kk+1):
                if gcd(hh,kk) != 1:
                    continue
                aa,bb,cc = (value(p,hh,kk) for p in (A,B,C))
                if min(aa,bb,cc) <= 0:
                    continue
                gg = gcd(gcd(aa,bb),cc)
                assert gg in (1,3)
                assert gcd(aa,bb) == gg
                assert cc*cc == aa*aa + sigma*aa*bb + bb*bb
                assert kk*(cc-aa) == hh*bb
                assert gcd(gcd(aa//gg,bb//gg),cc//gg) == 1
                g_counts[gg] += 1
                cases += 1
                local += 1
        conics.append({'sigma':sigma,'A':A,'B':B,'C':C,
                       'conic_identity':'PASS','inverse_slope_identity':'PASS',
                       'gcd_lemma_identities':'PASS','regression_pairs':local})
    Bplus = [-1,2,0]
    Bminus = [1,2,0]
    W = add(A,Bplus)
    U = add(A,scale(2,Bplus))
    V = add(scale(2,A),Bplus)
    # Each 120-degree factor is nonsingular as a binary quadratic.
    quadratics = {'A':A,'B_plus':Bplus,'B_minus':Bminus,'W':W,'U':U,'V':V}
    qdiscs = {}
    for name,p in quadratics.items():
        z,y,x = p
        disc = y*y-4*x*z
        assert disc in (4,12)
        qdiscs[name] = disc
    difference = [1,0,-1]  # v^2-u^2.
    Q = [2,0,-1]
    P = [3,0,-1]
    forms = [
        ('equilateral_60',mul(A,Bminus),1),
        ('equilateral_120',mul(A,Bplus),1),
        ('F1_120',mul(Bplus,W),1),
        ('isosceles_120',mul(Bplus,U),1),
        ('F2_120',mul(U,V),1),
        ('F3_120',scale(3,mul(U,W)),3),
        ('F4_120',mul(V,W),1),
        ('group1_alpha',mul(difference,Q),1),
        ('group1_other_scalene',mul(Q,P),1),
    ]
    results = []
    for name,form,constant in forms:
        disc = binary_quartic_discriminant(form)
        assert disc != 0, (name,form)
        results.append({'row':name,'coefficients_y4_to_x4':form,
                        'binary_quartic_discriminant':disc,
                        'distinct_projective_roots':4,
                        'displayed_constant_factor':constant})
    return {'result':'PASS','arithmetic':'integer polynomial identities and homogeneous discriminants',
            'coefficient_order':'[y^4,x*y^3,x^2*y^2,x^3*y,x^4]',
            'quartic_count':len(results),'quartics':results,
            'quadratic_discriminants':qdiscs,'conic_checks':conics,
            'normalization_regression':{'k_max':200,'primitive_positive_pairs':cases,
                                        'g_counts':{str(g):n for g,n in g_counts.items()},
                                        'universal_proof':'For a common prime divisor, gcd(h,k)=1 forces it to divide L=2h-sigma*k and then 3. If 9 divides L, A is 3h^2 modulo 9; otherwise B has 3-adic valuation at most one. Thus gcd(A,B,C) is 1 or 3.'},
            'scope':'Algebraic prerequisites only; no Thue-Mahler solutions, geometric tilings, or complete Erdos 634 classification computed.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report',type=Path,help='Optionally write the exact report; default is read-only.')
    args = ap.parse_args()
    text = json.dumps(verify(),indent=2) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
