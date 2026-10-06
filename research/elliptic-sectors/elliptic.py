#!/usr/bin/env python3
"""Exact elliptic arithmetic for the F3 square-class correspondence.

E_K: Y^2 = X^3 + K^3, with K=3*d and d positive squarefree.
Points are pairs of integers/Fractions; None denotes infinity. No floating
point arithmetic, rank computation, or bounded-search nonexistence claim is
used. The elliptic rank/existence theorem is a separate mathematical input.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt, lcm
from typing import TypeAlias

Scalar: TypeAlias = int | Fraction
Point: TypeAlias = tuple[Fraction, Fraction] | None


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f'{name} must be a positive integer')
    return value


def squarefree_kernel(value: int) -> int:
    """Squarefree part by exact trial division; intended for research inputs."""
    n = _positive_integer(value, 'value')
    result = 1
    p = 2
    while p*p <= n:
        odd = False
        while n % p == 0:
            n //= p
            odd = not odd
        if odd:
            result *= p
        p = 3 if p == 2 else p+2
    if n > 1:
        result *= n
    return result


def _kernel(d: int) -> int:
    d = _positive_integer(d, 'd')
    if squarefree_kernel(d) != d:
        raise ValueError('d must be squarefree')
    return d


def _point(point: tuple[Scalar, Scalar] | None) -> Point:
    if point is None:
        return None
    if not isinstance(point, (tuple, list)) or len(point) != 2:
        raise ValueError('a point must be None or an exact coordinate pair')
    if any(isinstance(t, bool) or not isinstance(t, (int, Fraction)) for t in point):
        raise ValueError('point coordinates must be integers or Fractions')
    return Fraction(point[0]), Fraction(point[1])


def on_curve(K: int, point: tuple[Scalar, Scalar] | None) -> bool:
    """Test membership in E_K; reject inexact or malformed coordinates."""
    K = _positive_integer(K, 'K')
    P = _point(point)
    return P is None or P[1]**2 == P[0]**3 + K**3


def _checked(K: int, point: tuple[Scalar, Scalar] | None) -> Point:
    P = _point(point)
    if not on_curve(K, P):
        raise ValueError('point is not on E_K')
    return P


def add(K: int, left: tuple[Scalar, Scalar] | None,
        right: tuple[Scalar, Scalar] | None) -> Point:
    """Exact group addition on E_K, validating both inputs."""
    K = _positive_integer(K, 'K')
    P, Q = _checked(K, left), _checked(K, right)
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == -y2:
        return None
    slope = (3*x1*x1/(2*y1) if P == Q else (y2-y1)/(x2-x1))
    x3 = slope*slope-x1-x2
    result = (x3, slope*(x1-x3)-y1)
    if not on_curve(K, result):
        raise ArithmeticError('elliptic addition invariant failed')
    return result


def mul(K: int, n: int, point: tuple[Scalar, Scalar] | None) -> Point:
    """Exact signed integer multiplication, by binary addition."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError('n must be an integer')
    P = _checked(_positive_integer(K, 'K'), point)
    if n < 0:
        P = None if P is None else (P[0], -P[1])
        n = -n
    result = None
    while n:
        if n & 1:
            result = add(K, result, P)
        n >>= 1
        if n:
            P = add(K, P, P)
    return result


def torsion_order(K: int, point: tuple[Scalar, Scalar] | None) -> int | None:
    """Return the rational torsion order, or None for a nontorsion point.

    The proved torsion classification for positive integral K is C2,
    extended to C6 exactly when K is a square. Its coordinates are explicit,
    so no bounded point search or expensive sequence of additions is needed.
    """
    P = _checked(_positive_integer(K, 'K'), point)
    if P is None:
        return 1
    if P == (Fraction(-K), Fraction(0)):
        return 2
    root = isqrt(K)
    if root*root == K:
        if P[0] == 0 and abs(P[1]) == K*root:
            return 3
        if P[0] == 2*K and abs(P[1]) == 3*K*root:
            return 6
    return None


def rational_sqrt(value: Scalar) -> Fraction | None:
    """Nonnegative rational square root, or None when it is not rational."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError('square test requires an exact rational')
    q = Fraction(value)
    if q < 0:
        return None
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    return Fraction(a, b) if a*a == q.numerator and b*b == q.denominator else None


def forward_f3(d: int, a: int, b: int, c: int) -> Point:
    """Map a primitive positive F3 coefficient d*s^2 to E_(3d).

    Raises ValueError if the triple or its asserted square class is invalid.
    The output has 0<X<3d and Y>0; X+3d is a rational square.
    """
    d = _kernel(d)
    for name, value in (('a', a), ('b', b), ('c', c)):
        _positive_integer(value, name)
    if gcd(a, b) != 1 or c*c != a*a+a*b+b*b:
        raise ValueError('a,b,c must form a primitive positive plus-norm triple')
    A, B = a+2*b, a+b
    scale = rational_sqrt(Fraction(3*A*B, d))
    if scale is None or scale.denominator != 1:
        raise ValueError('the F3 coefficient does not have squarefree kernel d')
    K, h = 3*d, scale/3
    point = (Fraction(K*(A-B), B), Fraction(K*A*c, B)/h)
    if not on_curve(K, point):
        raise ArithmeticError('forward F3 identity failed')
    return point


def reverse_f3(d: int, point: tuple[Scalar, Scalar] | None) -> dict:
    """Recover a primitive positive F3 coefficient from a square-lift point.

    Required: point on E_(3d), 0<X<3d, and X+3d a rational square.
    Returns integer a,b,c,s with 3(a+2b)(a+b)=d*s^2. This is a coefficient
    witness, not a claim that multiplier one gives a geometric F3 tiling.
    """
    d = _kernel(d)
    K = 3*d
    P = _checked(K, point)
    if P is None or not 0 < P[0] < K:
        raise ValueError('point must lie in the strict F3 real cone 0<X<3d')
    root = rational_sqrt(P[0]+K)
    if root is None or root == 0:
        raise ValueError('X+3d must be a nonzero rational square')
    ratio_A = (P[0]+K)/K
    ratio_c = abs(P[1])/(K*root)
    B = lcm(ratio_A.denominator, ratio_c.denominator)
    A, c = int(ratio_A*B), int(ratio_c*B)
    a, b = 2*B-A, A-B
    common = gcd(a, b)
    if c % common:
        raise ArithmeticError('primitive norm normalization failed')
    a, b, c = a//common, b//common, c//common
    D = 3*(a+2*b)*(a+b)
    scale = rational_sqrt(Fraction(D, d))
    if (min(a, b, c) <= 0 or gcd(a, b) != 1 or c*c != a*a+a*b+b*b
            or scale is None or scale.denominator != 1):
        raise ArithmeticError('reverse F3 identity failed')
    return {'d': d, 'a': a, 'b': b, 'c': c, 's': scale.numerator,
            'coefficient': D, 'point': P}


def dual_isogeny(K: int, point: tuple[Scalar, Scalar] | None) -> Point:
    """Map E'_K: y²=x³+6Kx²−3K²x to E_K exactly.

    Infinity and (0,0) map to infinity. Every other image has X+K equal
    to the rational square (y/(2x))². The sign convention is fixed here.
    """
    K = _positive_integer(K, 'K')
    P = _point(point)
    if P is None:
        return None
    x, y = P
    if y*y != x*x*x+6*K*x*x-3*K*K*x:
        raise ValueError('point is not on the stated 2-isogenous curve')
    if x == 0:
        return None
    result = (y*y/(4*x*x)-K, y*(x*x+3*K*K)/(8*x*x))
    if not on_curve(K, result):
        raise ArithmeticError('dual isogeny invariant failed')
    return result


def f3_from_generator(d: int, point: tuple[Scalar, Scalar] | None,
                      max_steps: int = 100) -> dict:
    """Search 2P,4P,... for a constructive arithmetic F3 witness.

    Any rational nontorsion P is sufficient; no full Mordell-Weil basis is
    needed. The real-density theorem proves eventual success without a
    universal search bound. Exhausting max_steps returns INCOMPLETE, never NO.
    Fractions in the output point must be serialized by the calling program.
    """
    d = _kernel(d)
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError('max_steps must be a nonnegative integer')
    K = 3*d
    P = _checked(K, point)
    order = torsion_order(K, P)
    if order is not None:
        raise ValueError(f'a nontorsion point is required; input has order {order}')
    step = add(K, P, P)
    current = None
    for n in range(1, max_steps+1):
        current = add(K, current, step)
        if current is None:
            raise ArithmeticError('nontorsion multiple unexpectedly reached infinity')
        # A double's shifted coordinate is a rational square by the exact
        # duplication identity; only the strict real interval remains to test.
        if 0 < current[0] < K:
            witness = reverse_f3(d, current)
            return {'status': 'FOUND', 'steps': n, 'multiple': 2*n,
                    'witness': witness}
    return {'status': 'INCOMPLETE', 'steps': max_steps,
            'reason': 'Search budget exhausted; no nonexistence conclusion.'}
