"""Exact lattice graph for a tiling with no short edges of intermediate height."""
from collections import Counter
from pathlib import Path
import json

E, U, S = (1, 0), (0, 1), (1, -1)
DIRECTIONS = [E, U, (-1, 1), (-1, 0), (0, -1), S]


def inside(a, b, p, den=1):
    x, y = p
    return (a+b)*y >= -b*x and a*y <= b*x and (a+b)*x+b*y <= den*a*(a+2*b)


def ring_product(p, q):
    x, y = p
    u, v = q
    return x*u-y*v, x*v+y*u+y*v


def kites_fit(a, b, start, step):
    den = a*a+a*b+b*b
    translation = (den*start[0], den*start[1])
    # Candidate c-edges have length one in this frame. These are apex vectors times den.
    for apex in [(a*(a+b), -a*b), (a*a, a*b)]:
        u, v = ring_product(step, apex)
        if not inside(a, b, (translation[0]+u, translation[1]+v), den):
            return False
    return True


def graph(a, b):
    points = set()
    for x in range(a+b+1):
        y_low = -(b*x//(a+b))
        y_high = min(b*x//a, (a*(a+2*b)-(a+b)*x)//b)
        for y in range(y_low, y_high+1):
            points.add((x, y))
    edges = set()
    for x, y in points:
        for step in DIRECTIONS:
            end = (x+step[0], y+step[1])
            if end in points and kites_fit(a, b, (x, y), step):
                edges.add(((x, y), end))
    return points, edges


def trace(a, b, word, edges):
    x = y = shoelace = 0
    path = [(x, y)]
    for dx, dy in word:
        end = (x+dx, y+dy)
        if ((x, y), end) not in edges:
            return None
        shoelace += x*dy-y*dx
        x, y = end
        path.append(end)
    assert (x, y) == (a+b, -b) and len(set(path)) == len(path)
    assert shoelace == -a*b
    counts = Counter(word)
    assert counts[E]-counts[(-1, 0)] == a and counts[S]-counts[(-1, 1)] == b
    assert counts[U] == counts[(0, -1)]
    return path


def placed_kites(a, b, path):
    """Full elementary triangles in coordinates multiplied by c squared."""
    c2 = a*a+a*b+b*b
    for start, end in zip(path, path[1:]):
        step = (end[0]-start[0], end[1]-start[1])
        p = (c2*start[0], c2*start[1])
        q = (c2*end[0], c2*end[1])
        for apex in [(a*(a+b), -a*b), (a*a, a*b)]:
            dx, dy = ring_product(step, apex)
            yield (p, q, (p[0]+dx, p[1]+dy))


def disjoint(a, b):
    """Triangle separating axes, allowing contact along an edge or point."""
    for tr in (a, b):
        for i in range(3):
            x, y = tr[i]
            dx, dy = tr[i-1][0]-x, tr[i-1][1]-y
            first = [(p[0]-x)*dy-(p[1]-y)*dx for p in a]
            second = [(p[0]-x)*dy-(p[1]-y)*dx for p in b]
            if max(first) <= min(second) or max(second) <= min(first):
                return True
    return False


def check_collar(a, b, path):
    from itertools import combinations
    tris = list(placed_kites(a, b, path))
    c2 = a*a+a*b+b*b
    for tri in tris:
        assert all(inside(a, b, p, c2) for p in tri)
        lengths = []
        for i in range(3):
            x, y = tri[i][0]-tri[i-1][0], tri[i][1]-tri[i-1][1]
            lengths.append(x*x+x*y+y*y)
        assert sorted(lengths) == [b*b*c2, a*a*c2, c2*c2]
    assert all(disjoint(p, q) for p, q in combinations(tris, 2))
    return len(tris)


def detour_word(a, b):
    return [E]*(a-2)+[U, S, E, S, (0, -1), E]+[S]*(b-2)


def partial_certificate(a, b, path):
    return {
        "status": "partial_tiling",
        "coordinate_frame": "numerator in (1,rho), divide by c^2, multiply by c*z",
        "tile": [a, b, int_square_root(a*a+a*b+b*b)],
        "target_count": (a+2*b)*(2*a+b),
        "placed_count": 2*(len(path)-1),
        "path_vertices_in_unit_lattice": [list(p) for p in path],
        "triangles": [[list(p) for p in tri] for tri in placed_kites(a, b, path)],
    }


def int_square_root(n):
    from math import isqrt
    c = isqrt(n)
    assert c*c == n
    return c


def main():
    # The signed-area detour is tested again here with all mandatory neighboring tiles.
    for a, b in [(5, 3), (33, 7), (35, 13), (85, 11), (143, 25), (161, 15), (323, 37), (533, 27)]:
        points, edges = graph(a, b)
        pair = ([E]*a+[S]*b, detour_word(a, b))
        sizes = []
        for word in pair:
            path = trace(a, b, word, edges)
            if path and a <= 35:
                sizes.append(check_collar(a, b, path))
            else:
                sizes.append(2*len(word) if path else 0)
        if (a, b) in ((33,7), (35,13)):
            certificate = partial_certificate(a, b, trace(a, b, pair[1], edges))
            path = Path(__file__).parent/'controls'/f"interface_{certificate['target_count']}.json"
            assert json.loads(path.read_text()) == certificate
        print(f'{(a+2*b)*(2*a+b)}: {len(points)} vertices, {len(edges)} directed edges; '
              f'shortest/detour collar tile counts {sizes[0]}/{sizes[1]}')


if __name__ == '__main__':
    main()
