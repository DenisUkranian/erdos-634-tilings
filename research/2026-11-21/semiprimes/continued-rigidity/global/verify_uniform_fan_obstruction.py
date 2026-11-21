#!/usr/bin/env python3
"""Exact arithmetic and geometry controls for one uniform fan family."""
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path

U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def triangle(a, b, q, j, s):
    x, y = q
    return (q, (x-a*U[j][0], y-a*U[j][1]),
            (x+b*U[(j+s) % 6][0], y+b*U[(j+s) % 6][1]))


def overlap(first, second):
    for poly in (first, second):
        for i in range(3):
            p, q = poly[i], poly[(i+1) % 3]
            dx, dy = q[0]-p[0], q[1]-p[1]
            aa = [dx*y-dy*x for x, y in first]
            bb = [dx*y-dy*x for x, y in second]
            if max(aa) <= min(bb) or max(bb) <= min(aa):
                return False
    return True


def as_pair(q):
    return [q.numerator, q.denominator]


def run():
    results = []
    for a, b, c in ((33, 7, 37), (35, 13, 43)):
        assert gcd(a, b) == 1 and a*a+a*b+b*b == c*c
        board_a, board_b = b*(2*a+b), a*(a+2*b)
        fan = F(a*(a+2*b), a+b)
        assert fan == a+F(a*b, a+b)
        # Intersection of [(-a,0),(b,-b)] with x=0.
        parameter = F(a, a+b)
        assert -a+parameter*(a+b) == 0
        carrier_lower = -parameter*b
        assert a-carrier_lower == fan
        ceiling = -((-fan.numerator)//fan.denominator)
        assert fan.denominator > 1
        required = (c-1)*ceiling+fan
        chords = (F(board_a*board_b*c, board_b*a+board_a*b),
                  min(F(board_a*c, b), F(board_b*c, a+b)),
                  min(F(board_a*c, a+b), F(board_b*c, a)))
        assert chords[0] == F(board_a*board_b, c*(a+b))
        assert chords[1] == c*fan
        assert chords[2] == F(board_a*c, a+b)
        assert max(chords) == chords[1]
        assert required-max(chords) == (c-1)*(ceiling-fan) > 0
        orientations = ((0, -1), (0, 1), (4, 1))
        first = [triangle(a, b, (0, 0), j, s) for j, s in orientations]
        assert all(not overlap(first[i], first[j])
                   for i in range(3) for j in range(i+1, 3))
        second = [triangle(a, b, (0, c+1), j, s) for j, s in orientations]
        bad = [(i, j) for i in range(3) for j in range(3)
               if overlap(first[i], second[j])]
        assert bad == [(2, 0)]
        safe = [triangle(a, b, (0, ceiling), j, s) for j, s in orientations]
        assert all(not overlap(p, q) for p in first for q in safe)
        results.append({
            'N': (a+2*b)*(2*a+b), 'tile': [a, b, c],
            'board_vertices': [[0, 0], [board_a, 0], [0, board_b]],
            'fan_carrier_section_length': as_pair(fan),
            'minimum_integer_anchor_gap': ceiling,
            'required_carrier_span_for_c_fans': as_pair(required),
            'three_height_one_maximum_chords': [as_pair(q) for q in chords],
            'excess_over_longest_chord': as_pair(required-max(chords)),
            'adjacent_overlap_pairs_at_gap_c_plus_one': bad,
            'adjacent_overlap_pairs_at_minimum_integer_gap': [],
            'scope': 'This c-fan, same-carrier, integer-anchor family at '
                     'height one, including rotations by multiples of 60 '
                     'degrees. No classification of general 3c kernels.',
        })
    return {'verified': True, 'controls': results}


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('UNIFORM_FAN_OBSTRUCTION_REPLAY.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
