"""Check the two signed triangular disc constructions using integer coordinates."""
from collections import defaultdict, Counter
from itertools import combinations
from math import gcd, isqrt
from notchshape import make


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def edges(poly):
    return zip(poly, poly[1:] + poly[:1])


def area(poly):
    return sum(cross(p, q) for p, q in edges(poly))


def ccw(poly):
    return poly if area(poly) > 0 else list(reversed(poly))


def left(p, q, v):
    return cross(sub(q, p), sub(v, p))


def separates(poly, other):
    return any(all(left(p, q, v) <= 0 for v in other) for p, q in edges(poly))


def norm(p):
    return p[0]**2 + p[0] * p[1] + p[1]**2


def strictly_between(p, w, q):
    return left(p, w, q) == 0 and min(p, q) < w < max(p, q)


def checked(a, b, c):
    n = (a + 2 * b) * (2 * a + b)
    step = ((c - b) // 2, (c - a) // 2, 1)
    if n == 3431:
        scaffold = make(a, b, c, 1, 2, [(8, 2, 1), (15, 2, 1)], allow_left_padding=True)
        padding = [(-7 * c, 0), (0, 0), (0, 165 * c), (-7 * c, 165 * c)]
        # Split each of the five 7-by-33 cells across its long diagonal.
        triangle_sides = [7, 33, isqrt(7**2 + 7 * 33 + 33**2)]
        assert sorted(triangle_sides) == sorted((a, b, c)) and 5 * 33 == 165
        padding_faces = 10
    else:
        scaffold = make(a, b, c, 1, 1, [step, step])
        padding = []
        padding_faces = 0
    board = ccw(scaffold['target'])
    pieces = []
    positive, negative = 0, padding_faces

    def triangle(poly, factor):
        assert len(poly) == 3 and factor > 0
        wanted = sorted((c * factor * side)**2 for side in (a, b, c))
        assert sorted(norm(sub(q, p)) for p, q in edges(poly)) == wanted

    for block in scaffold['blocks']:
        pts = block['points']
        poly = ccw(pts)
        assert area(poly) > 0
        assert all(left(p, q, v) >= 0 for p, q in edges(poly) for v in poly)
        pieces.append(poly)
        if block['kind'] == 'notch':
            x, y, w, d = pts
            t, k = block['scale'], block['notch']
            z = y[0] + t * a * c, y[1]
            triangle([x, y, z], t)
            triangle([z, w, d], k)
            assert strictly_between(y, w, z) and strictly_between(x, d, z)
            assert abs(area([x,y,z])) - abs(area([z,w,d])) == area(poly)
            positive += t*t
            negative += k*k
        elif block['kind'] == 'triangle':
            triangle(pts, block['scale'])
            positive += block['scale']**2
        else:
            assert block['kind'] == 'parallelogram'
            p, q, r, s = pts
            assert sub(q, p) == sub(r, s) and sub(s, p) == sub(r, q)
            m, k = block['rows'], block['cols']
            u, v = sub(q, p), sub(s, p)
            assert all(x % m == 0 for x in u) and all(x % k == 0 for x in v)
            u = u[0] // m, u[1] // m
            v = v[0] // k, v[1] // k
            if block['diagonal'] == 'difference':
                triangle([(0, 0), u, v], 1)
            else:
                assert block['diagonal'] == 'sum'
                triangle([(0, 0), u, (u[0] + v[0], u[1] + v[1])], 1)
            positive += 2*m*k

    assert all(separates(p, q) or separates(q, p) for p, q in combinations(pieces, 2))
    assert sum(area(p) for p in pieces) == area(board) + area(padding)
    # Equality of oriented boundary chains, allowing all partial contacts.
    # With CCW interiors and disjoint blocks this proves exact coverage.
    supports = defaultdict(Counter)
    for sign, poly in [(1, p) for p in pieces] + [(-1, board), (-1, padding)]:
        for p, q in edges(poly):
            dx, dy = sub(q, p)
            divisor = gcd(dx, dy)
            u = dx // divisor, dy // divisor
            if u < (0, 0):
                u = -u[0], -u[1]
            row = supports[(u, cross(u, p))]
            row[p] += sign
            row[q] -= sign
    assert all(not any(row.values()) for row in supports.values())
    # When the macro edges meet, every vertex on the common run is at an
    # integer physical distance from the endpoints of the edge containing it.
    for poly in pieces:
        for p, q in edges(poly):
            for other in pieces + [board, padding]:
                for w in other:
                    if strictly_between(p, w, q):
                        for delta in (sub(w,p),sub(q,w)):
                            square = norm(delta)
                            length = isqrt(square)
                            assert length * length == square and length % c == 0
    assert positive - negative == n
    assert negative == {3431: 75, 5063: 8}[n]
    print(n, 'board:', len(pieces), 'convex blocks.', positive, 'positive faces,',
          negative, 'negative faces,', positive + negative, 'faces in all.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable assertions to run this checker.')
    checked(33, 7, 37)
    checked(35, 13, 43)
