"""Construct the two-scale tiling and certify disjointness, containment and area exactly.

The hexagons represent blocks tiled by a single translated m-grid. The other
tiles are genuine n-triangles. All predicates use only Python integers.
"""
from collections import defaultdict
from itertools import combinations
from math import gcd
import sys


def edge(a, b):
    return tuple(sorted((a, b)))


def face_grid(r):
    faces = []
    for i in range(r):
        for j in range(r - i):
            p, q, t = (i, j), (i + 1, j), (i, j + 1)
            faces.append((1, (p, q, t), (edge(p, t), edge(p, q), edge(q, t))))
            if i + j < r - 1:
                s = (i + 1, j + 1)
                faces.append((-1, (s, t, q), (edge(s, q), edge(s, t), edge(t, q))))
    return faces


def compatible_shifts(faces, m):
    adjacent = defaultdict(list)
    for face_id, (sign, _, sides) in enumerate(faces):
        for side, coefficient in zip(sides, (sign, sign, -sign)):
            adjacent[side].append((face_id, coefficient))
    assigned = {}
    balance = [0] * len(faces)
    neighbours = [[] for _ in faces]
    for side, connections in adjacent.items():
        if len(connections) == 1:
            f, coeff = connections[0]
            a, b = side
            val = int(sum(a) == sum(b))
            assigned[side] = val
            balance[f] += coeff*val
        else:
            (f, c), (g, d) = connections
            assert c == -d
            neighbours[f].append((g, side, d))
            neighbours[g].append((f, side, c))
            assigned[side] = 0
    parents = {0: None}
    order = [0]
    for f in order:
        for g, side, coeff_g in neighbours[f]:
            if g not in parents:
                parents[g] = (f, side, coeff_g)
                order.append(g)
    assert len(order) == len(faces)
    for g in reversed(order[1:]):
        f, side, coeff_g = parents[g]
        value = (-balance[g]*coeff_g) % m
        assigned[side] = value
        balance[f] -= coeff_g*value
    assert balance[0] % m == 0
    for _, _, (x, y, z) in faces:
        assert (assigned[x]+assigned[y]-assigned[z]) % m == 0
    return assigned


def separated(first, second):
    # Every edge normal of both polygons belongs to the set x, y, x+y.
    return any(b <= c or d <= a for (a, b), (c, d) in zip(first, second))


def certify(m, n):
    assert m > 1 and n > 1 and gcd(m, n) == 1
    r, M = m, m*n
    H, cap, radius = 100*M+m, 10*M, 20*M
    K = r*H+n
    faces = face_grid(r)
    shifts = compatible_shifts(faces, m)
    by_vertex = defaultdict(list)
    boxes = []
    macro_area = 0
    for sign, vertices, (xe, ye, ze) in faces:
        X = H*xe[0][0] + n*shifts[xe]
        Y = H*ye[0][1] + n*shifts[ye]
        Z = H*sum(ze[0]) + n*shifts[ze]
        side = sign*(Z-X-Y)
        assert side > 2*cap and side % m == 0 and cap % m == 0
        if sign == 1:
            bounds = ((X, X+side-cap), (Y, Y+side-cap), (X+Y+cap, Z))
        else:
            bounds = ((X-side+cap, X), (Y-side+cap, Y), (Z, X+Y-cap))
        assert bounds[0][0] >= 0 and bounds[1][0] >= 0 and bounds[2][1] <= K
        boxes.append(bounds)
        macro_area += side**2 - 3*cap**2
        for v in vertices:
            by_vertex[v].append(bounds)
    assert all(separated(a,b) for a,b in combinations(boxes, 2))

    small = 0
    for (vx,vy), incident in by_vertex.items():
        ox, oy = H*vx, H*vy
        patch = ((ox-radius, ox+radius), (oy-radius, oy+radius),
                 (ox+oy-radius, ox+oy+radius))
        nearby = [b for b in boxes if not separated(b, patch)]
        assert all(b in incident for b in nearby)
        span = radius//n
        for i in range(-span, span):
            for j in range(max(-span,-span-i-1), min(span,span-i)):
                x, y = ox+i*n, oy+j*n
                # Normal-coordinate ranges for the two halves of this n-square.
                for down in (0,1):
                    tri = ((x, x+n), (y, y+n),
                           (x+y+down*n, x+y+(down+1)*n))
                    if any(a<lo or b>hi for (a,b),(lo,hi) in zip(tri,patch)):
                        continue
                    if x < 0 or y < 0 or tri[2][1] > K:
                        continue
                    if all(separated(tri, big) for big in nearby):
                        small += 1
    # n-tiles inside a fixed patch are distinct elementary faces of one grid.
    # Patches themselves are separated because their centers are H apart.
    assert H > 2*radius
    assert macro_area + small*n**2 == K*K
    assert gcd(K, m*n) == 1 and macro_area % (m*m) == 0
    return K, macro_area//(m*m), small


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    args = list(map(int, sys.argv[1:]))
    if len(args) % 2:
        raise SystemExit('Supply size pairs m n.')
    pairs = [(2,3), (3,5), (4,3), (5,2)] if not args else list(zip(args[::2],args[1::2]))
    for m, n in pairs:
        K, small_m, small_n = certify(m,n)
        print(f"m={m}, n={n}, K={K}: {small_m} of size {m} and {small_n} of size {n}; exact full area and disjointness.")
