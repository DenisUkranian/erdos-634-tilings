"""Construct the two-scale tiling and certify disjointness, containment and area exactly.

The hexagons represent blocks tiled by a single translated m-grid. The other
tiles are genuine n-triangles. All predicates use only Python integers.
"""
import argparse
from collections import defaultdict
from itertools import combinations
from math import gcd


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


def support_levels(faces, m, n, k, height):
    # Boundary values on the coarse vertices prescribe compatible line levels.
    def potential(vertex):
        i, j = vertex
        return k*i if i+j == m else 0

    levels = {}
    inverse = pow(n, -1, m)
    for _, _, sides in faces:
        for direction, (a,b) in enumerate(sides):
            if (a,b) in levels:
                continue
            dx = potential(b)-potential(a)
            # Endpoints are sorted by x, then by y. Vertical edges run up.
            residue = -dx if direction == 0 else dx
            old = height*(a[0], a[1], sum(a))[direction]
            levels[a,b] = old + n*(((residue-old)*inverse) % m)
    return levels


def separated(first, second):
    # Every edge normal of both polygons belongs to the set x, y, x+y.
    return any(b <= c or d <= a for (a, b), (c, d) in zip(first, second))


def certify(m, n, target=None):
    assert m > 1 and n > 1 and gcd(m, n) == 1
    r, M = m, m*n
    K = 20*m*M if target is None else target
    if K < 20*m*M:
        raise ValueError(f'The construction guarantees K >= {20*m*M} for this ordering.')
    limit = K//m
    H = limit - (limit - K*pow(m, -1, n)) % n
    cap, radius = 5*M, 9*M
    assert 0 <= K-m*H < M and (K-m*H) % n == 0
    assert H > 2*radius and H-cap-2*M > radius
    faces = face_grid(r)
    levels = support_levels(faces, m, n, K, H)
    by_vertex = defaultdict(list)
    boxes = []
    macro_area = 0
    for sign, vertices, (xe, ye, ze) in faces:
        X, Y, Z = levels[xe], levels[ye], levels[ze]
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
    assert macro_area % (m*m) == 0
    return K, macro_area//(m*m), small


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sizes', type=int, nargs='*', help='Pairs of coprime sizes m n.')
    parser.add_argument('--target', type=int, help='Requested board size for one pair.')
    args = parser.parse_args()
    if len(args.sizes) % 2 or (args.target is not None and len(args.sizes) != 2):
        parser.error('Supply size pairs m n and use --target with a single pair.')
    pairs = list(zip(args.sizes[::2], args.sizes[1::2])) or [(2,3), (3,5), (4,3), (5,2)]
    for m, n in pairs:
        if min(m,n) < 2 or gcd(m,n) != 1:
            parser.error('Positive coprime sizes greater than one are required.')
        if args.target is not None and args.target < 20*m*m*n:
            parser.error(f'The stated bound is {20*m*m*n} for sizes {m} and {n} in this order.')
        k, count_m, count_n = certify(m, n, args.target)
        print(f'm={m}, n={n}, K={k}: {count_m} of size {m} and {count_n} of size {n}.')
