#!/usr/bin/env python3
"""Independent exact checker; imports neither Geometry nor PhaseBudget."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
PRIMES = {7: (3, -1), 37: (7, -3), 43: (6, 1)}


def add(p, q): return p[0] + q[0], p[1] + q[1]
def sub(p, q): return p[0] - q[0], p[1] - q[1]
def scale(t, p): return t * p[0], t * p[1]
def cross(p, q): return p[0] * q[1] - p[1] * q[0]
def norm(p): return p[0] ** 2 + p[0] * p[1] + p[1] ** 2
def mul(p, q):
    x, y = p; u, v = q
    return x * u - y * v, x * v + y * u + y * v


def separated(first, second):
    for triangle, other in ((first, second), (second, first)):
        for i, p in enumerate(triangle):
            edge = sub(triangle[(i + 1) % 3], p)
            if all(cross(edge, sub(q, p)) <= 0 for q in other):
                return True
    return False


def valuation_numerator(p, prime, c):
    if p == (0, 0):
        return 10 ** 9
    conjugate = prime[0] + prime[1], -prime[1]
    count = 0
    while True:
        x, y = mul(p, conjugate)
        if x % c or y % c:
            return count
        p = x // c, y // c
        count += 1


def verify(path):
    data = json.loads(path.read_text())
    a, b, c = data['tile']
    A, B = b * (2 * a + b), a * (a + 2 * b)
    assert a * a + a * b + b * b == c * c
    assert data['N'] == (a + 2 * b) * (2 * a + b)

    def point(p):
        x, y, e = p
        return F(x, c ** e), F(y, c ** e)

    def integer(p):
        x, y = scale(c, point(p))
        assert x.denominator == y.denominator == 1
        return int(x), int(y)

    def heading(h, j):
        result = UNITS[j % 6]
        base = (F(a, c), F(b, c)) if h >= 0 else (F(a + b, c), F(-b, c))
        for _ in range(abs(h)):
            result = mul(result, base)
        return result

    triangles, betas, alphas = [], [], []
    placements = data['placements']
    for tile in placements:
        q, h, j, s = point(tile['q']), tile['h'], tile['j'], tile['s']
        beta = add(q, scale(-a, heading(h, j)))
        alpha = add(q, scale(b, heading(h, j + s)))
        expected = (beta, q, alpha) if s == 1 else (alpha, q, beta)
        assert tuple(map(point, tile['vertices'])) == expected
        vertices = tuple(map(integer, tile['vertices']))
        assert cross(sub(vertices[1], vertices[0]), sub(vertices[2], vertices[0])) == a * b * c * c
        assert sorted(norm(sub(vertices[(i + 1) % 3], vertices[i])) for i in range(3)) == sorted(n * n * c * c for n in (a, b, c))
        for x, y in vertices:
            assert x > 0 and y > 0 and B * x + A * y < A * B * c
        triangles.append(vertices)
        betas.append(scale(c, beta)); alphas.append(scale(c, alpha))

    checks = 0
    for i, first in enumerate(triangles):
        for second in triangles[:i]:
            assert separated(first, second), ('overlap', i)
            checks += 1

    region = tuple(map(integer, data['region']))
    region_area2 = sum(cross(p, region[(i + 1) % 4]) for i, p in enumerate(region))
    assert region_area2 == 2 * c * a * b * c * c
    interior = [i for i, tile in enumerate(placements) if tile['role'] == 'interior']
    assert len(interior) == 2 * c
    for i in interior:
        assert placements[i]['h'] == 0 and placements[i]['s'] == -1
        for p in triangles[i]:
            assert all(cross(sub(region[(k + 1) % 4], origin), sub(p, origin)) >= 0
                       for k, origin in enumerate(region))
    # Non-overlap, containment and exact equality of areas imply that the
    # interior triangles tile the entire closed parallelogram.

    cycle = data['cycle']
    assert len(cycle) == 2 * a + 2
    starts = [integer(edge['start']) for edge in cycle]
    ends = [integer(edge['end']) for edge in cycle]
    assert len(set(starts)) == len(starts)
    assert all(ends[i] == starts[(i + 1) % len(starts)] for i in range(len(starts)))
    assert sum(cross(starts[i], ends[i]) for i in range(len(cycle))) == region_area2
    for i, edge in enumerate(cycle):
        index = edge['tile']
        assert starts[i] == betas[index] and ends[i] == alphas[index]
        assert edge['height'] == placements[index]['h'] + placements[index]['s']
        assert norm(sub(ends[i], starts[i])) == c ** 4
        # Each segment lies on one side of the convex region and has its
        # counterclockwise direction, ruling out an erroneous bank choice.
        assert any(cross(sub(q, p), sub(starts[i], p)) == 0
                   and cross(sub(q, p), sub(ends[i], p)) == 0
                   and all(min(p[k], q[k]) <= starts[i][k] <= max(p[k], q[k])
                           and min(p[k], q[k]) <= ends[i][k] <= max(p[k], q[k]) for k in (0, 1))
                   and sum(sub(q, p)[k] * sub(ends[i], starts[i])[k] for k in (0, 1)) > 0
                   for p, q in zip(region, region[1:] + region[:1]))
    assert Counter(edge['height'] for edge in cycle) == {-1: 2, 0: 2 * a}

    mate_count = 0
    for i in interior:
        candidates = [j for j in interior if j != i and betas[i] == alphas[j] and alphas[i] == betas[j]]
        assert len(candidates) <= 1
        if candidates:
            j = candidates[0]
            assert placements[i]['h'] == placements[j]['h']
            assert placements[i]['s'] == placements[j]['s']
            assert (placements[i]['j'] - placements[j]['j']) % 6 == 3
            assert add(scale(c, point(placements[i]['q'])), scale(c, point(placements[j]['q']))) == add(betas[i], alphas[i])
            mate_count += 1
    assert mate_count == 2 * c - 2
    signs = Counter(placements[i]['s'] * (-1 if placements[i]['j'] % 2 else 1) for i in interior)
    assert signs == {1: c, -1: c}

    # Exact prime division, not the search's Hensel key implementation.
    prime = PRIMES[c]
    assert norm(prime) == c
    assert valuation_numerator((a, b), prime, c) == 2
    origin = integer(data['shift'])
    assert valuation_numerator(origin, prime, c) - 1 == -1
    for i in interior:
        assert valuation_numerator(sub(integer(placements[i]['q']), origin), prime, c) - 1 >= 0
    for outer in data['board']:
        assert valuation_numerator(sub(integer(outer), origin), prime, c) - 1 == -1
    for tile in placements:
        if tile['role'] != 'interior':
            assert tile['h'] == -1
            assert valuation_numerator(integer(tile['q']), prime, c) - 1 >= -1

    # Independent arithmetic for the no-lowering strip example. Its boundary
    # forces these opposite, inward height-minus-one teeth in any replacement
    # using only lower short heights. Chords between cells are fully blocked.
    V, step = sub(region[1], region[0]), (0, c * c)
    forced = []
    assert 2 * a > c and 2 * c < 3 * a
    for i in range(a):
        Pi = add(region[0], scale(i, step)); Pj = add(Pi, step)
        Qi = add(Pi, V); Qj = add(Pj, V)
        left = (Pi, add(Pi, scale(F(a, c), V)), Pj)
        right = (Qj, sub(Qj, scale(F(a, c), V)), Qi)
        cell = (Pi, Qi, Qj, Pj)
        cell_area2 = sum(cross(p, cell[(k + 1) % 4]) for k, p in enumerate(cell))
        remainder = F(cell_area2 - 2 * a * b * c * c, a * b * c * c)
        assert remainder == F(2 * (c - a), a) and 0 < remainder < 1
        for triangle in (left, right):
            assert cross(sub(triangle[1], triangle[0]), sub(triangle[2], triangle[0])) == a * b * c * c
            for p in triangle:
                assert all(cross(sub(cell[(k + 1) % 4], origin), sub(p, origin)) >= 0
                           for k, origin in enumerate(cell))
            forced.append(triangle)
    assert all(separated(first, second) for i, first in enumerate(forced) for second in forced[:i])

    result = dict(N=data['N'], placements=len(placements), interior_tiles=len(interior),
                  bank_tiles=len(placements) - len(interior), overlap_tests=checks,
                  directed_cycle_edges=len(cycle), cycle_heights=dict(Counter(e['height'] for e in cycle)),
                  interior_long_pairs=mate_count // 2, interior_unpaired=2,
                  interior_sign_counts=[signs[1], signs[-1]],
                  interior_node='one exterior-free level-0 coset of valuation -1',
                  lowering_cell_remainder=str(F(2 * (c - a), a)),
                  scope='Partial packing only; no full-board completion certified.')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    for n in (143, 3431, 5063):
        verify(Path(__file__).with_name(f'mixed_cycle_{n}.json'))
