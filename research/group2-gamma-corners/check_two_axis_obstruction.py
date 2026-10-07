#!/usr/bin/env python3
"""Replay the exact boundary obstruction to a single-short-height gamma filler.

This does not test arbitrary F3 tilings. PROOF.md shows that the gamma
remainder's axis boundary would be partitioned into whole a- and b-edges
under the single-short-direction-class restriction. This script checks
only the subsequent exact arithmetic, without internal seam assumptions.
"""
import argparse
import json
from math import gcd
from pathlib import Path


def check(a, b, c):
    if not all(type(x) is int for x in (a, b, c)):
        raise ValueError('Integer sides required')
    if not (a > 2*b and b > 1 and gcd(a, b) == 1
            and c*c == a*a+a*b+b*b):
        raise ValueError('Require a>2b>2, a primitive pair, and the plus norm')
    h, delta = a+2*b, a-b
    if a*delta > b*h:
        raise ValueError('Reflected corner is not contained in the outer triangle')
    quotient, remainder = divmod(a, b)
    lower, upper = a*delta, b*h
    boundary_length = upper-lower
    least_a_coefficient = b-remainder
    difference = boundary_length-a*least_a_coefficient
    if not (0 < remainder < b and quotient >= 2
            and difference == b*((1-quotient)*a+2*b) < 0
            and (boundary_length-a*least_a_coefficient) % b == 0):
        raise RuntimeError('Exact semigroup obstruction identity failed')
    return {
        'status': 'PASS',
        'scope': 'Single-short-height filling of the specified gamma-corner remainder only',
        'tile': [a, b, c],
        'F3_count': 3*(a+b)*h,
        'outer_scale': h,
        'reflected_corner_scale': delta,
        'axis_boundary_side': {'lower': lower, 'upper': upper,
                               'length': boundary_length},
        'a_divided_by_b': {'quotient': quotient, 'remainder': remainder},
        'least_possible_a_coefficient': least_a_coefficient,
        'least_required_a_length': a*least_a_coefficient,
        'boundary_length_minus_least_required_a_length': difference,
        'boundary_length_in_nonnegative_semigroup_generated_by_a_b': False,
        'two_axis_gamma_filler_exists': False,
        'single_short_height_gamma_filler_exists': False,
        'obstruction': 'An actual boundary side cannot be partitioned into whole a,b sides',
        'rectangle_DFS': 'Not run: an exact necessary boundary condition fails',
        'arbitrary_F3_tiling_excluded': False,
        'full_Erdos634_solved': False,
    }


def main():
    if not __debug__:
        raise SystemExit('Run without -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('a', type=int, nargs='?', default=24)
    parser.add_argument('b', type=int, nargs='?', default=11)
    parser.add_argument('c', type=int, nargs='?', default=31)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = check(args.a, args.b, args.c)
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
