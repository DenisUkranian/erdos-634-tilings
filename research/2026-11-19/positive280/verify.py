"""Standalone exact proof of the 280-tile witness. Requires only Python 3."""
from collections import Counter
from csv import reader
from itertools import combinations
from math import gcd
from pathlib import Path

DEN = 81
OUTER = ((0, 0), (140 * DEN, 0), (70 * DEN, 40 * DEN))
SIDES = (5, 6, 9)


def verify(condition, error):
    if not condition:
        raise ValueError(error)


def edges(triangle):
    return zip(triangle, triangle[1:] + triangle[:1])


def det(a, b, p):
    return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])


def length_squared(a, b):
    # The Euclidean point belonging to (x,y) is (x, sqrt(2)*y)/DEN.
    return (b[0]-a[0])**2 + 2*(b[1]-a[1])**2


def interiors_disjoint(first, second):
    # A line through an edge can support a strict separation of open interiors.
    for source, other in ((first, second), (second, first)):
        for a, b in edges(source):
            if all(det(a, b, point) <= 0 for point in other):
                return True
    return False


def update_edge_events(counter, triangle, weight):
    # An oriented interval's multiplicity changes only at its two endpoints.
    for a, b in edges(triangle):
        dx, dy = b[0]-a[0], b[1]-a[1]
        div = gcd(dx, dy)
        if (dx, dy) < (0, 0):
            div = -div
        ux, uy = dx//div, dy//div
        line = ux*a[1] - uy*a[0]
        # Events at oriented start and end implement both signs of an edge.
        counter[ux, uy, line, ux*a[0]+uy*a[1]] += weight
        counter[ux, uy, line, ux*b[0]+uy*b[1]] -= weight


def load(path):
    with path.open(newline='', encoding='ascii') as file:
        lines = reader(file)
        verify(next(lines) == 'x1,y1,x2,y2,x3,y3'.split(','), 'Incorrect CSV header')
        triangles = []
        for i, row in enumerate(lines, 2):
            verify(len(row) == 6, f'Incorrect number of fields in row {i}')
            coords = list(map(int, row))
            triangles.append(tuple(zip(coords[::2], coords[1::2])))
    return triangles


def main():
    triangles = load(Path(__file__).with_name('tiling_280.csv'))
    verify(len(triangles) == 280, 'Expected precisely 280 triangles')
    verify(len(set(tuple(sorted(t)) for t in triangles)) == 280, 'Repeated tile')
    target_lengths = [k*k*DEN*DEN for k in SIDES]
    target_area = det(*OUTER)
    verify([length_squared(a,b) for a,b in edges(OUTER)] ==
           [140**2*DEN**2, 90**2*DEN**2, 90**2*DEN**2], 'Incorrect board')
    total = 0
    events = Counter()
    for i, tri in enumerate(triangles, 1):
        area = det(*tri)
        verify(area == 20*DEN**2, f'Wrong signed determinant at tile {i}')
        verify(sorted(length_squared(a,b) for a,b in edges(tri)) == target_lengths,
               f'Wrong edge lengths at tile {i}')
        verify(all(det(a,b,p) >= 0 for a,b in edges(OUTER) for p in tri),
               f'Tile {i} leaves the board')
        total += area
        update_edge_events(events, tri, 1)
    verify(total == target_area, 'The total area differs from the board')
    tested = 0
    for (i,first), (j,second) in combinations(enumerate(triangles, 1), 2):
        verify(interiors_disjoint(first, second), f'Interiors overlap at tiles {i} and {j}')
        tested += 1
    update_edge_events(events, OUTER, -1)
    verify(all(v == 0 for v in events.values()), 'Unbalanced oriented edge segment')
    print(f'{len(triangles)} congruent (5,6,9) tiles inside the (90,90,140) board.')
    print(f'All {tested} pairs have disjoint interiors.')
    print(f'Sum of signed doubled axial areas = board determinant = {total}.')
    print('The oriented tile boundaries sum exactly to the outer boundary.')


if __name__ == '__main__':
    main()
