"""Verify the explicit nonempty-notch positive control using integer arithmetic."""
from itertools import combinations
from pathlib import Path


def det(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def length2(p, q):
    x, y = p[0] - q[0], p[1] - q[1]
    return x*x + x*y + y*y


def edges(polygon):
    return zip(polygon, polygon[1:] + polygon[:1])


def separates(poly, other):
    return any(all(det(p, q, r) <= 0 for r in other) for p, q in edges(poly))


def verify():
    a, b, c, t, k, den = 5, 3, 7, 14, 5, 7
    board = [(t*a*den,0), (t*a*den,t*b*den), (k*a*a,k*a*b), (k*c*den,0)]
    vertices = []
    data = Path(__file__).with_name("control171.txt").read_text().splitlines()
    assert data[0].startswith("YES ")
    for line in data[1:]:
        x0, y0, x1, y1, x2, y2, _ = map(int, line.split())
        triangle = [(x0,y0),(x1,y1),(x2,y2)]
        assert det(*triangle) == a*b*den**2
        assert sorted(length2(p,q) for p,q in edges(triangle)) == sorted((s*den)**2 for s in (a,b,c))
        assert all(det(p,q,r) >= 0 for p,q in edges(board) for r in triangle)
        vertices.append(triangle)
    assert all(separates(p,q) or separates(q,p) for p,q in combinations(vertices,2))
    board_area = sum(p[0]*q[1]-q[0]*p[1] for p,q in edges(board))
    assert board_area == sum(det(*tri) for tri in vertices)
    assert len(vertices) == t*t-k*k == 171
    print("Verified 171 congruent interiors-disjoint triangles covering the prescribed notch.")


if __name__ == "__main__":
    verify()
