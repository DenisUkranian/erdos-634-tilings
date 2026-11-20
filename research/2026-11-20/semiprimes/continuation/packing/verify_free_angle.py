"""An integer-only, all-orientations saturation certificate for the 5063 residual hexagon.

Coordinates use the oblique basis (1, exp(pi*i/3)). See SATURATED_HEXAGON.md.
"""
from itertools import combinations
from math import gcd


def multiply(z, w):
    x, y = z
    a, b = w
    return x * a - y * b, x * b + y * a + y * b


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def difference(u, v):
    return u[0] - v[0], u[1] - v[1]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def normal(u, v):
    dx, dy = difference(v, u)
    g = gcd(dx, dy)
    return -dy // g, dx // g


def intersects(bounds):
    """Nonempty bounded intersection of closed planar half-planes has a vertex."""
    for (a, b, c), (d, e, f) in combinations(bounds, 2):
        det = a * e - b * d
        if not det:
            continue
        x, y = c * e - b * f, a * f - c * d
        if det < 0:
            x, y, det = -x, -y, -det
        if all(k * x + l * y >= m * det for k, l, m in bounds):
            return True
    return False


def product_fits(hexagon, tile, denom, drift):
    """Return the number of candidate separator axes, raising on any feasible one."""
    hull = [hexagon[i] for i in (0, 1, 2, 4, 5)]
    axes = [normal(hull[j - 1], h) for j, h in enumerate(hull)]
    # Hexagon data are in 43 times physical coordinates. Trial translations
    # and trial tile vertices are in 43 * denom times physical coordinates.
    bounds = []
    for n, h in zip(axes, hull):
        needed = denom * (dot(n, h) - drift * (abs(n[0]) + abs(n[1])))
        bounds.append((*n, needed - min(dot(n, v) for v in tile)))
    r = hexagon[3]
    corner = (denom * (r[0] - drift), denom * (r[1] - drift))
    directions = {(0, 1), (1, 0)}
    for j, v in enumerate(tile):
        x, y = normal(tile[j - 1], v)
        if x <= 0 and y <= 0:
            x, y = -x, -y
        if x >= 0 and y >= 0:
            directions.add((x, y))
    for n in directions:
        last = dot(n, corner) - min(dot(n, v) for v in tile)
        if intersects(bounds + [(*n, last)]):
            raise ValueError('The relaxed translated triangle fits this orientation.')
    return len(directions)


def main():
    hexagon = [(0, 0), (-817, 0), (-817, -559), (688, -559),
               (688, -1118), (1248, -910)]
    hand = [(0, 0), (35, 0), (35, 13)]
    panels = 64
    snapshots = lp_count = 0
    for sign in (1, -1):
        vertices = hand if sign == 1 else [(x + y, -y) for x, y in hand]
        for j in range(panels):
            # t=m/n is the midpoint of [j/panels, (j+1)/panels].
            m, n = 2 * j + 1, 2 * panels
            rotation = n * n - m * m, 2 * n * m + m * m
            denom = n * n + n * m + m * m
            assert rotation[0]**2 + rotation[0] * rotation[1] + rotation[1]**2 == denom**2
            for sector in range(6):
                tile = [multiply(rotation, (43 * x, 43 * y)) for x, y in vertices]
                lp_count += product_fits(hexagon, tile, denom, drift=43)
                snapshots += 1
                rotation = multiply(rotation, (0, 1))
    print('Rotation snapshots including both hands:', snapshots)
    print('Exact bounded half-plane feasibility tests:', lp_count)
    print('Feasible relaxed placements: 0')


if __name__ == '__main__':
    main()
