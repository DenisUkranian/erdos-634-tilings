"""Check the finite families of polygons against every geometrically admissible chord.

Run python3 verify.py from any directory. Only integer and rational arithmetic is used.
"""
import json
from collections import defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import lcm
from pathlib import Path


def multiply(u, v):
    x, y = u
    s, t = v
    return x * s - y * t, x * t + y * s + y * t


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def polygon_key(edges):
    """A polygon up to rotation, reflection, translation and cyclic relabelling."""
    mirror = [(length, -height, (3 - phase) % 6)
              for length, height, phase in reversed(edges)]
    keys = []
    for boundary in (list(edges), mirror):
        for i, (_, h, j) in enumerate(boundary):
            cycle = boundary[i:] + boundary[:i]
            keys.append(tuple((n, k - h, (s - j) % 6) for n, k, s in cycle))
    return min(keys)


class Tile:
    def __init__(self, a, b, c):
        assert c * c == a * a + a * b + b * b
        assert 1 < Fraction(2 * a + b, c) < 2
        self.a, self.b, self.c = a, b, c
        self.rho = (0, 1)
        self.z = (Fraction(a, c), Fraction(b, c))
        self.coins = {0}
        for n in range(1, a * (a + 2 * b) + 1):
            if any(n - s in self.coins for s in (a, b, c)):
                self.coins.add(n)
        # An interior or exterior sector of a cut polygon lies between 0 and pi.
        self.turns = {(n - m, m % 6) for m in range(4) for n in range(4)
                      if (m, n) not in ((0, 0), (3, 3))}

    @cache
    def unit(self, h, j):
        z = self.z if h >= 0 else (self.z[0] + self.z[1], -self.z[1])
        u = (1, 0)
        for _ in range(abs(h)):
            u = multiply(u, z)
        for _ in range(j % 6):
            u = multiply(u, self.rho)
        return u

    def area(self, edges):
        x = y = twice_area = 0
        for length, h, j in edges:
            s, t = self.unit(h, j)
            dx, dy = length * s, length * t
            twice_area += x * dy - y * dx
            x, y = x + dx, y + dy
        assert (x, y) == (0, 0)
        return Fraction(twice_area, self.a * self.b)

    def convex(self, edges):
        vertices = []
        x = y = 0
        for size, h, j in edges:
            vertices.append((x, y))
            dx, dy = self.unit(h, j)
            x, y = x + size * dx, y + size * dy
        if (x, y) != (0, 0):
            return False
        for i, (x, y) in enumerate(vertices):
            dx, dy = self.unit(*edges[i][1:])
            for k, (vx, vy) in enumerate(vertices):
                if k not in (i, (i + 1) % len(edges)):
                    if det((dx, dy), (vx - x, vy - y)) <= 0:
                        return False
        return True

    def admissible(self, edges):
        if len(edges) < 3:
            return False
        for i, (length, h, j) in enumerate(edges):
            _, k, s = edges[i - 1]
            if length not in self.coins or (h - k, (j - s) % 6) not in self.turns:
                return False
        mass = self.area(edges)
        if mass <= 0 or mass.denominator != 1:
            return False
        ordinary = sum(n * (-1 if j % 2 else 1) for n, h, j in edges)
        alternating = sum(n * (-1 if (j + h) % 2 else 1) for n, h, j in edges)
        for total, unit in ((ordinary, self.a - self.b - self.c),
                            (alternating, self.a - self.b + self.c)):
            if total % unit:
                return False
            signed_count = total // unit
            if abs(signed_count) > mass or (signed_count - mass) % 2:
                return False
        return True

    def board(self):
        a, b = self.a, self.b
        u, v = b * (2 * a + b), a * (a + 2 * b)
        # Board vertices (0,0), (u,0), (0,v). Its diagonal is c^2 rho^j z^h.
        diagonal = (Fraction(-u, self.c**2), Fraction(v, self.c**2))
        h, j = next((h, j) for h in range(-2, 3) for j in range(6)
                    if self.unit(h, j) == diagonal)
        return ((u, 0, 0), (self.c**2, h, j), (v, 0, 4))

    @staticmethod
    def boundary_arc(edges, source, end):
        i, first = source
        k, last = end
        n, h, j = edges[i]
        arc = [(n - first, h, j)]
        i = (i + 1) % len(edges)
        while i != k:
            arc.append(edges[i])
            i = (i + 1) % len(edges)
        if last:
            arc.append((last, *edges[k][1:]))
        return arc

    def chords(self, edges):
        """Group boundary points on actual lines in a common integer coordinate system."""
        assert self.admissible(edges)
        vectors = [self.unit(h, j) for _, h, j in edges]
        scale = lcm(*(Fraction(x).denominator for u in vectors for x in u))
        sites = []
        x = y = 0
        for i, ((size, _, _), (dx, dy)) in enumerate(zip(edges, vectors)):
            dx, dy = int(scale * dx), int(scale * dy)
            for offset in range(size):
                if offset in self.coins and size - offset in self.coins:
                    sites.append((i, offset, x + offset * dx, y + offset * dy))
            x, y = x + size * dx, y + size * dy
        assert (x, y) == (0, 0)

        axes = {(h + dh, (j + dj) % 3) for _, h, j in edges
                for dh, dj in self.turns}
        for h, j in sorted(axes):
            dx, dy = self.unit(h, j)
            den = lcm(Fraction(dx).denominator, Fraction(dy).denominator)
            rx, ry = int(dx * den), int(dy * den)
            # All points along a boundary side parallel to the tested axis are
            # tangent. Strictly convex corners at its endpoints also have no
            # chord along that tangent. Only the other sides need be grouped.
            groups = defaultdict(list)
            for i, v, x, y in sites:
                if (edges[i][1], edges[i][2] % 3) == (h, j):
                    continue
                if v == 0 and (edges[i-1][1], edges[i-1][2] % 3) == (h, j):
                    continue
                groups[rx * y - ry * x].append((i, v, x, y))
            for points in groups.values():
                for start, finish in combinations(points, 2):
                    i, u, x1, y1 = start
                    k, v, x2, y2 = finish
                    if i == k:
                        continue
                    signed = (Fraction((x2 - x1) * den, scale * rx) if rx
                              else Fraction((y2 - y1) * den, scale * ry))
                    size = abs(signed)
                    if size <= 0 or size.denominator != 1 or size not in self.coins:
                        continue
                    size = int(size)
                    forward = j if signed > 0 else j + 3
                    first = self.boundary_arc(edges, (i, u), (k, v))
                    first.append((size, h, (forward + 3) % 6))
                    second = self.boundary_arc(edges, (k, v), (i, u))
                    second.append((size, h, forward))
                    if self.admissible(first) and self.admissible(second):
                        yield (i, u, k, v, size), polygon_key(first), polygon_key(second)


def check_case(record):
    tile = Tile(*record['tile'])
    nodes = [tuple(tuple(v) for v in item) for item in record['polygons']]
    assert not record['exclude_equilateral_ab']
    assert record['limit'] + 1 == tile.a * tile.b
    assert len(set(nodes)) == len(nodes)
    known = set()
    chord_total = 0
    for shape in nodes:
        assert tile.convex(shape)
        assert polygon_key(shape) == shape and tile.admissible(shape)
        assert tile.area(shape) >= tile.a * tile.b
        for _, left, right in tile.chords(shape):
            assert left in known or right in known, (shape, left, right)
            chord_total += 1
        known.add(shape)
    board = tile.board()
    assert polygon_key(board) == nodes[-1]
    assert tile.area(board) == (tile.a + 2 * tile.b) * (2 * tile.a + tile.b)
    # Side 0 goes from the 60-degree corner to the end of the shorter leg.
    # Side 2 returns from the end of the longer leg to that corner.
    cuts = []
    for (i, u, k, v, length), _, _ in tile.chords(board):
        assert (i, k) == (0, 2) and u and v
        long_leg = board[2][0] - v
        short_leg = u
        count = Fraction(long_leg * short_leg, tile.a * tile.b)
        assert count.denominator == 1
        cuts.append((long_leg, short_leg, int(count), length))
    assert len(cuts) == 6
    print(f'{int(tile.area(board))}: {len(nodes)} polygons, {chord_total} chords, '
          f'minimum area {tile.a * tile.b}')
    for row in sorted(cuts):
        print(' ', *row)
    small = [shape for shape in nodes if tile.area(shape) == tile.a * tile.b]
    assert sorted(len(shape) for shape in small) == [3, 4]
    for shape in small:
        assert list(tile.chords(shape)) == []
    a, b, c = tile.a, tile.b, tile.c
    s = a * b
    assert polygon_key(((b * (a + b - c), 0, 0), (s, 0, 2),
                        (s - b * (a + b - c), -1, 4), (s, -1, 0))) in small
    expected = {int(tile.area(board)), int(tile.area(board)) - a * (a + b),
                int(tile.area(board)) - 4 * b * (a + b), 4 * s}
    expected.update(b * (a + b) - k * k for k in range(b + 1))
    assert {tile.area(shape) for shape in nodes} == expected
    # Every smaller member is a direct cut of F1 with a gridded complement.
    f1 = next(sh for sh in nodes if tile.area(sh) == b*(a+b) and len(sh) == 3)
    assert f1 == polygon_key(((a*b, 0, 0), (b*c, -1, 2), (b*(a+b), 0, 4)))
    grids = {polygon_key(((k*a, 0, 0), (k*c, -1, 3), (k*b, 0, 5)))
             for k in range(1, b+1)}
    embeddable = {f1}
    for _, first, second in tile.chords(f1):
        if first in grids:
            embeddable.add(second)
        if second in grids:
            embeddable.add(first)
    small_family = {sh for sh in nodes if tile.area(sh) <= b*(a+b)}
    assert small_family <= embeddable
    large_areas = sorted(int(tile.area(sh)) for sh in nodes if sh not in small_family)
    assert len(large_areas) == 4
    print(f'  {len(small_family)} shapes embed in the {b*(a+b)}-tile F1 triangle;'
          f' remaining areas {large_areas}')
    check_controls(tile)
    return cuts


def check_controls(tile):
    a, b, c = tile.a, tile.b, tile.c
    triple = ((2*a, 0, 0), (2*c, -1, 3), (2*b, 0, 5))
    unit_tile = polygon_key(((a, 0, 0), (c, -1, 3), (b, 0, 5)))
    assert tile.area(triple) == 4
    midcuts = {locations for locations, p, q in tile.chords(triple)
               if unit_tile in (p, q)}
    assert len(midcuts) >= 3

    # The basic 120-degree trapezoid has a dissection into grids of scales a,b,c.
    leg, top = a * b, a*a + b*b
    basic = ((top + leg, 0, 0), (leg, 0, 2), (top, 0, 3), (leg, 0, 4))
    gridded = {polygon_key(((scale*a, 0, 0), (scale*c, -1, 3), (scale*b, 0, 5)))
               for scale in (a, b, c)}
    for _, p, q in tile.chords(basic):
        if p not in gridded and q not in gridded:
            continue
        rest = q if p in gridded else p
        if any(left in gridded and right in gridded for _, left, right in tile.chords(rest)):
            break
    else:
        raise AssertionError('failed to replay a known three-grid trapezoid')

    # Four pieces in the reflected board with side length 2ab at the 60-degree corner.
    s = a*b
    origin, x, y = (0, 0), (a*(a+2*b), 0), (0, b*(2*a+b))
    middle, u, v = (s, s), (2*s, 0), (0, 2*s)
    regions = [(origin,u,v), (u,x,middle), (middle,y,v), (x,y,middle)]
    def sub(p, q):
        return p[0]-q[0], p[1]-q[1]
    def length2(p, q):
        dx, dy = sub(p,q)
        return dx*dx + dx*dy + dy*dy
    def borders(poly):
        return zip(poly, poly[1:] + poly[:1])
    for tri, sides in zip(regions, [(2*s,)*3] +
                          [tuple(k*n for n in (a,b,c)) for k in (a,b,c)]):
        assert sorted(length2(p,q) for p,q in borders(tri)) == sorted(n*n for n in sides)
        assert det(sub(tri[1],tri[0]),sub(tri[2],tri[0])) > 0
        assert all(det(sub(q,p), sub(w,p)) >= 0 for p,q in borders((origin,x,y)) for w in tri)
    assert sum(det(sub(q,p),sub(r,p)) for p,q,r in regions) == det(x,y)
    for left, right in combinations(regions,2):
        assert any(all(det(sub(q,p),sub(w,p)) <= 0 for w in other)
                   for poly,other in [(left,right),(right,left)] for p,q in borders(poly))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run this checker with assertions enabled.')
    for n in (3431, 5063):
        file = Path(__file__).with_name(f'family_{n}.json')
        check_case(json.loads(file.read_text()))
