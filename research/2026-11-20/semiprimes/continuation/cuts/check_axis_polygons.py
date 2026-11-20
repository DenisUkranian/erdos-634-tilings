"""Small exact checks of the algebra and translation argument in AXIS_POLYGONS."""
from itertools import product
from math import gcd, isqrt

DIRECTIONS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]


def convex_hull(points):
    points = sorted(set(points))

    def half(vertices):
        result = []
        for p in vertices:
            while len(result) >= 2:
                a, b = result[-2:]
                cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
                if cross > 0:
                    break
                result.pop()
            result.append(p)
        return result

    return half(points)[:-1] + half(reversed(points))[:-1]


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def check_polygons():
    count = 0
    for lengths in product(range(6), repeat=6):
        vertices = [(0, 0)]
        for s, (x, y) in zip(lengths, DIRECTIONS):
            vertices.append(add(vertices[-1], (s*x, s*y)))
        if vertices[-1] != (0, 0):
            continue
        hull = convex_hull(vertices)
        if len(hull) < 3:
            continue
        w = lengths[0] - lengths[3]
        assert w == lengths[2] - lengths[5] == lengths[4] - lengths[1]
        points = {(0, 0), (w, 0), (0, w)}
        for j in range(3):
            m = min(lengths[j], lengths[j+3])
            x, y = DIRECTIONS[j]
            points |= {add(p, (m*x, m*y)) for p in points}
        reconstructed = convex_hull(points)

        def translate_to_first(v):
            return [(x - v[0][0], y - v[0][1]) for x, y in v]

        assert translate_to_first(hull) == translate_to_first(reconstructed)
        count += 1
    return count


def check_packing():
    count = 0
    for size in range(1, 17):
        anchors = [(x, y) for x in range(size+1) for y in range(size-x+1)]
        vertices = {(0, 0), (size, 0), (0, size)}
        for (x, y), (u, v) in product(anchors, repeat=2):
            dx, dy = x-u, y-v
            distance = max(abs(dx), abs(dy), abs(dx+dy))
            intersects = max(x, u) + max(y, v) < size + min(x+y, u+v)
            assert intersects == (distance < size)
            if not intersects:
                assert vertices.intersection({(x,y), (u,v)})
            count += 1
    return count


def check_character_scales():
    count = 0
    for a in range(2, 130):
        for b in range(1, a):
            c = isqrt(a*a+a*b+b*b)
            if c*c != a*a+a*b+b*b or gcd(a, b) != 1:
                continue
            x, y = c+a-b, c+b-a
            assert x*y == 3*a*b and c % 3 != 0
            for m in range(1, 16):
                assert (m*x % 3 == m*y % 3 == 0) == (m % 3 == 0)
                count += 1
    return count


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    print("Convex integer polygons checked:", check_polygons())
    print("Ordered translation pairs checked:", check_packing())
    print("Character and scale checks:", check_character_scales())
