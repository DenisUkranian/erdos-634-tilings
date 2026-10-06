#!/usr/bin/env python3
"""Replay the constructive ternary-semigroup conductor bound.

Default execution is read-only. The theorem and geometric dependency
are documented in TERNARY_SEMIGROUP_TAIL.md.
"""
from math import gcd
from pathlib import Path
import argparse
import json


def primitive(m, n):
    if not (m > n > 0 and gcd(m, n) == 1):
        raise ValueError('Require coprime m>n>0.')
    a0, b0, c0 = m*m-n*n, n*(2*m+n), m*m+m*n+n*n
    g = gcd(gcd(a0, b0), c0)
    if g not in (1, 3):
        raise ValueError('Unexpected primitive normalization.')
    return a0//g, b0//g, c0//g, g


def witness(a, b, c, x):
    d = gcd(a+c, b)
    m, n = (a+c)//d, b//d
    threshold = (m+n-2)*(b+c)
    if x < threshold:
        raise ValueError('The sufficient conductor bound does not apply.')
    b0 = ((x-(n-1)*(b+c))*pow(b, -1, a)) % a
    determinant = m*m-n*n
    u, v = (m*b0)//determinant, (n*b0)//determinant
    B = b0-m*u+n*v+n-1
    C = n*u-m*v+n-1
    residual = x-B*b-C*c
    if residual % a:
        raise ValueError('Residue representative is inconsistent.')
    A = residual//a
    if not (min(A, B, C) >= 0 and B <= m+n-2 and C <= m+n-2):
        raise ValueError('Invalid nonnegative representative.')
    if A*a+B*b+C*c != x:
        raise ValueError('Wrong semigroup representation.')
    return {'A': A, 'B': B, 'C': C, 'm': m, 'n': n,
            'conductor_bound': threshold}


def replay():
    triples = residues = 0
    normalizations = {1: 0, 3: 0}
    for m in range(2, 41):
        for n in range(1, m):
            if gcd(m, n) != 1:
                continue
            a, b, c, g = primitive(m, n)
            threshold = (m+n-2)*(b+c)
            for r in range(a):
                out = witness(a, b, c, threshold+r)
                if (out['m'], out['n']) != (m, n):
                    raise ValueError('Parameter reconstruction failed.')
            triples += 1
            residues += a
            normalizations[g] += 1
    examples = []
    for m, n in [(101, 30), (173, 50)]:
        a, b, c, g = primitive(m, n)
        if not (a > b >= 4900 and 5*a <= 7*b):
            raise ValueError('Example lies outside the stated explicit cone.')
        x = b*c-a*a
        examples.append({'tile': [a, b, c], 'normalization': g,
                         'remainder': x, 'representation': witness(a, b, c, x)})
    return {'status': 'PASS', 'full_Erdos634_solved': False,
            'coprime_parameter_triples': triples,
            'residue_representatives_checked': residues,
            'normalizations': normalizations, 'large_examples': examples,
            'scope': 'Exact arithmetic replay. Positive tilings use the separately proved nested-corner theorem.'}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    output = json.dumps(replay(), indent=2) + '\n'
    if args.report is not None:
        args.report.write_text(output)
    print(output, end='')
