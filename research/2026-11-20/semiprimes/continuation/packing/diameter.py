"""Exact diameters of axial-coordinate polygons and of a nonconvex residual hexagon."""
from fractions import Fraction as F
from itertools import combinations, pairwise


HULL = [(F(0), F(0)), (F(-19), F(0)), (F(-19), F(-13)),
        (F(16), F(-26)), (F(1248, 43), F(-910, 43))]
R = F(16), F(-13)


def cap(s):
    vertices = []
    for p, q in pairwise(HULL + HULL[:1]):
        first = s * (p[0] - R[0]) + (1 - s) * (p[1] - R[1])
        last = s * (q[0] - R[0]) + (1 - s) * (q[1] - R[1])
        if first >= 0:
            vertices.append(p)
        if first * last < 0:
            vertices.append(tuple((last * u - first * v) / (last - first) for u, v in zip(p, q)))
    return vertices


def diameter_sq(vertices):
    return max((x-z)**2 + (x-z)*(y-w) + (y-w)**2
               for (x, y), (z, w) in combinations(vertices, 2))


if __name__ == '__main__':
    panel_values = [diameter_sq(cap(F(i, 3)) + cap(F(i + 1, 3))) for i in range(3)]
    assert panel_values == [F(188257,121), F(49228,43), F(256)]
    assert max(panel_values) < 43**2
    print('Squared diameter upper bounds from three panels:', *panel_values)
    events = {F(0), F(1)}
    for x, y in HULL:
        dx, dy = x - R[0], y - R[1]
        if dx != dy:
            s = dy / (dy - dx)
            if 0 < s < 1:
                events.add(s)
    values = [(s, diameter_sq(cap(s))) for s in sorted(events)]
    for s, d in values:
        print('event', s, 'squared diameter', d)
    assert max(d for s, d in values) == F(1289,35)**2
    assert (F(624,35), F(-13)) in cap(F(0)) and HULL[2] in cap(F(0))
    print('Longest contained segment:', F(1289,35))
