#!/usr/bin/env python3
"""Exact rational identities for the alpha/congruent-number equivalence.

The formulas are weighted homogeneous. Cancelling powers of d reduces
them to the identities at d=1 checked here by coefficient arithmetic.
This does not identify different quadratic twists over the rationals.
Only the Python standard library is needed; default execution is read-only.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import os
from pathlib import Path

if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
    raise SystemExit('Run ordinary Python without optimization.')


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim([(p[i] if i < len(p) else 0)
                 + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def mul(p, q):
    result = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            result[i+j] += a*b
    return trim(result)


class RationalFunction:
    """Univariate polynomial fraction; equality needs no gcd reduction."""

    def __init__(self, numerator=0, denominator=(1,)):
        if not isinstance(numerator, (tuple, list)):
            numerator = (F(numerator),)
        self.n = trim(list(numerator))
        self.d = trim(list(denominator))
        assert any(self.d), 'zero polynomial denominator'

    def __add__(self, other):
        if not isinstance(other, RationalFunction):
            other = RationalFunction(other)
        return RationalFunction(add(mul(self.n, other.d),
                                    mul(other.n, self.d)),
                                mul(self.d, other.d))

    __radd__ = __add__

    def __neg__(self):
        return RationalFunction(tuple(-v for v in self.n), self.d)

    def __sub__(self, other):
        if not isinstance(other, RationalFunction):
            other = RationalFunction(other)
        return self + -other

    def __rsub__(self, other):
        return RationalFunction(other) + -self

    def __mul__(self, other):
        if not isinstance(other, RationalFunction):
            other = RationalFunction(other)
        return RationalFunction(mul(self.n, other.n), mul(self.d, other.d))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, RationalFunction):
            other = RationalFunction(other)
        assert any(other.n), 'division by zero rational function'
        return RationalFunction(mul(self.n, other.d), mul(self.d, other.n))

    def __rtruediv__(self, other):
        return RationalFunction(other) / self

    def __pow__(self, exponent):
        assert isinstance(exponent, int)
        if exponent < 0:
            return (RationalFunction(1) / self)**(-exponent)
        result = RationalFunction(1)
        for _ in range(exponent):
            result = result * self
        return result


def verify():
    """Return a JSON-serializable report; do not write files or print."""
    x = RationalFunction((0, 1))
    f = x**3-x
    g = x**3+6*x**2+x
    px = x*(x-1)/(x+1)
    pyfactor = 1-2/(x+1)**2
    qx = (x+1)**2/(4*x)
    qyfactor = (x**2-1)/(8*x**2)
    qx_composed = (px+1)**2/(4*px)
    qx_quartic = (1+x)/(1-x)
    quartic = (1-x**2)*(2-x**2)
    checks = {
        'E_to_Eprime': f*pyfactor**2-(px**3+6*px**2+px),
        'Eprime_to_E': g*qyfactor**2-(qx**3-qx),
        'quartic_to_Eprime': (4*quartic/(1-x)**4
                              -(qx_quartic**3+6*qx_quartic**2+qx_quartic)),
        'quartic_inverse_z': (qx_quartic-1)/(qx_quartic+1)-x,
        'quartic_inverse_w_factor': 4/((1-x)**2*(qx_quartic+1)**2)-1,
        'quartic_to_E_direct': x**2*quartic-((x**2-1)**3-(x**2-1)),
        'dual_composition_doubling_x': (qx_composed
                                        -(x**2+1)**2/(4*x*(x**2-1))),
        'Eprime_doubling_x': ((3*x*x+12*x+1)**2/(4*g)-6-2*x
                              -(x*x-1)**2/(4*g)),
        'Eprime_torsion_translation': g/x**4-(1/x**3+6/x**2+1/x),
    }
    for name, residual in checks.items():
        assert all(v == 0 for v in residual.n), (name, residual.n)
    return {
        'result': 'PASS',
        'arithmetic': 'exact rational-function polynomial coefficients',
        'normalization': 'weighted homogeneous identities with powers of d cancelled',
        'identity_count': len(checks),
        'checks': list(checks),
        'scope': ('Universal algebraic map identities; geometric tails, torsion '
                  'theorems, ranks and small tiling scales are not computed.'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path,
                        help='Optional JSON output path; default is read-only.')
    args = parser.parse_args()
    report = json.dumps(verify(), indent=2) + '\n'
    if args.report:
        args.report.write_text(report, encoding='utf-8')
    print(report, end='')


if __name__ == '__main__':
    main()
