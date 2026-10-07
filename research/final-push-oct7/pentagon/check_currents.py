#!/usr/bin/env python3
"""Exact checks for the short-height obstruction and two-height identity."""

from collections import defaultdict
import json
from math import isqrt


def add(*terms):
    out = defaultdict(int)
    for term in terms:
        for key, value in term.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def mul(left, right):
    out = defaultdict(int)
    for (i, h), x in left.items():
        for (j, k), y in right.items():
            q, r = divmod(i + j, 3)
            out[r, h + k] += (-1) ** q * x * y
    return {key: value for key, value in out.items() if value}


def signed_axis_current(points):
    current = [0, 0, 0]
    for p, q in zip(points, points[1:] + points[:1]):
        x, y = q[0] - p[0], q[1] - p[1]
        if y == 0:
            current[0] += x
        elif x == 0:
            current[1] += y
        else:
            assert x == -y, (x, y)
            current[2] += y
    return tuple(current)


def check(a, b, c):
    p = {(0, 0): a, (1, 0): b, (0, 1): -c}
    q = {(0, 0): -a, (2, 0): b, (0, -1): c}
    d = {(0, 0): -b, (1, 0): -(a - b), (2, 0): a}
    xr = {(1, 1): c, (2, 1): -c}
    target = {(0, 0): -2*a*b, (1, 0): 2*a*b, (2, 0): -2*a*b}
    assert add(mul(p, d), mul(q, xr)) == target
    h = [(b*(a-b), -2*a*b), (-b*b, -a*b), (0, -a*b),
         (0, 0), (-a*b, a*b), (b*(a-b), a*b)]
    assert signed_axis_current(h) == (2*a*b, -2*a*b, 2*a*b)
    determinant_sum = sum(p[0]*q[1] - p[1]*q[0]
                          for p, q in zip(h, h[1:] + h[:1]))
    count = 2*b*(3*a - 2*b)
    assert -determinant_sum == a*b*count
    assert count >= 2*(a+c) and (count - 2*(a+c)) % 2 == 0


if __name__ == '__main__':
    checked = 0
    for a in range(2, 401):
        for b in range(1, a):
            c2 = a*a + a*b + b*b
            c = isqrt(c2)
            if c*c == c2:
                check(a, b, c)
                checked += 1
    assert checked > 0
    print(json.dumps({
        'status': 'PASS',
        'checked': checked,
        'parameter_bound_a': 400,
        'checks': ['exact direction currents', 'hexagon area',
                   'two-height current identity', 'positive inventory count'],
        'geometric_filling_constructed': False,
        'new_admissible_count_claimed': False,
        'full_Erdos634_solved': False,
    }, indent=2))
