from fractions import Fraction as F
from itertools import pairwise

A, B, C = 35, 13, 43
p = [(35217, 0), (46397, 0), (30212, 32025), (35217, 13545)]
verts = [(F(x, C), F(y, C)) for x, y in p]
edges = list(pairwise(verts + verts[:1]))


def multiply(u, v):
    x, y = u
    a, b = v
    return x*a - y*b, x*b + y*a + y*b


def rotate(u):
    return -u[1], u[0] + u[1]


def direction(h, j):
    z = (F(A, C), F(B, C))
    v = (1, 0)
    for _ in range(h):
        v = multiply(v, z)
    for _ in range(j):
        v = rotate(v)
    return v


def partitions(length):
    return [(x, y, z) for x in range(length//A + 1)
            for z in range((length - A*x)//C + 1)
            for y, remainder in [divmod(length - A*x - C*z, B)] if remainder == 0]


word = [(260, 0, 0), (645, 2, 1), (385, 1, 4), (315, 0, 4)]
for ((x, y), (u, v)), (l, h, j) in zip(edges, word):
    d, e = direction(h, j)
    assert (u-x, v-y) == (l*d, l*e)
assert sum(x*v-y*u for (x, y), (u, v) in edges) == 345*A*B
assert verts[0] == (819, 0) and verts[1] == (1079, 0)
assert [y for _, y in verts[2:]] == [F(32025, 43), 315]
for x, y in verts[1:3]:
    assert 2135*x + 1079*y == 2135*1079
assert all(len(partitions(k*s)) == 1 for k in range(1, 6) for s in (A, B, C))
assert partitions(260) == [(0, 20, 0), (1, 14, 1), (2, 8, 2), (3, 2, 3)]
assert max(z for _, _, z in partitions(455)) == 5
assert 3*A*F(B, C) < 32 and (2*C)**2 < 3*50**2 and 32+50 < 315
print("345 polygon, side headings, purity through 5, and c-edge bounds 3 and 5 verified.")
