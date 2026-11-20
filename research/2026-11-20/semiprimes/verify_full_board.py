"""Reproduce the whole-board calculations with integer and rational arithmetic."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd
from pathlib import Path
import json

from controls.verify_grids import check as verify_grid

ROOT = Path(__file__).resolve().parent
E, U, S = (1, 0), (0, 1), (1, -1)
NEG_U = (0, -1)


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def product(x, y):
    a, b = x
    c, d = y
    return (a*c - b*d, a*d + b*c + b*d)


def conjugate(x):
    return (x[0] + x[1], -x[1])


def norm(x):
    return product(x, conjugate(x))[0]


def cross(x, y):
    return x[0]*y[1] - x[1]*y[0]


def divide(x, divisor):
    return tuple(Fraction(element, divisor) for element in x)


def board_angles_and_heights(data):
    """Use actual cell directions in a checked dissection; derive the base frame from its vertices."""
    a, b, c = data['tile']
    scale = data.get('dilation', 1)
    den = data['coordinate_denominator']
    tiles_checked = verify_grid(data)['count']
    vertices = data['target']
    origin, base, third = next((o, x, y) for o in vertices for x in vertices for y in vertices
                               if norm(sub(x, o)) == (den*scale*c*c)**2
                               and norm(sub(y, o)) == (den*scale*a*(a+2*b))**2)
    base_axis = divide(sub(base, origin), den*scale*c*c)
    mirror = cross(sub(base, origin), sub(third, origin)) < 0
    z = divide((a, b), c)
    axes = {}
    # Only for reading finite positive controls. Failing to find an axis raises an error.
    for sign in [-1, 1]:
        power = (1, 0)
        for exponent in range(9):
            ray = power
            for _ in range(6):
                axes[ray] = sign*exponent
                ray = product(ray, (0, 1))
            power = product(power, z if sign == 1 else conjugate(z))
    counts = Counter()
    for region in data['blocks']:
        points = region['points']
        tri = region['kind'] == 'triangle'
        rows = region['scale'] if tri else region['rows']
        cols = rows if tri else region['cols']
        u = divide(sub(points[1], points[0]), rows)
        v = divide(sub(points[-1], points[0]), cols)
        diagonal = sub(u, v) if tri or region['diagonal'] == 'difference' else sub(u, (-v[0], -v[1]))
        by_length = {}
        for edge in (u, v, diagonal):
            length = next(length for length in (a, b, c) if norm(edge) == (den*length)**2)
            ray = product(divide(edge, den*length), conjugate(base_axis))
            by_length[length] = axes[conjugate(ray) if mirror else ray]
        assert by_length[a] == by_length[b] and abs(by_length[c] - by_length[a]) == 1
        counts[by_length[a]] += rows**2 if tri else 2*rows*cols
    assert sum(counts.values()) == tiles_checked
    assert all(n % c == (tiles_checked % c if h == 2 else 0) for h, n in counts.items())
    if scale == 1:
        support = range(min(counts), max(counts) + 1)
        assert sum(h not in counts for h in support) <= 1 and counts[2] > 0
        if counts[1] == 0:
            assert sum(n for h, n in counts.items() if h <= 0) == c*c
    return dict(sorted(counts.items()))


def population_candidates(a, b, c):
    """Search integer interface characters using only triangle area and the two sign budgets."""
    d = a - b
    total = (a+2*b)*(2*a+b)
    assert c*c == a*a+a*b+b*b and total == 2*c*c+3*a*b
    possible = []
    for low in range(c*c, total, c*c):
        high = total-low
        # |c^2+cM| <= (c-d)*low; take the exact integer ceiling/floor.
        start = -((c*c + (c-d)*low) // c)
        stop = ((c-d)*low - c*c) // c
        # Both weight quotients must be integers. Their CRT period is 3ab.
        assert gcd(c-d, c+d) == 1 and (c-d)*(c+d) == 3*a*b
        step = 3*a*b
        for charge in range(start + (-d-start) % step, stop+1, step):
            ordinary, rem = divmod(c*c+c*charge, d-c)
            alternating, rem_alt = divmod(c*c-c*charge, d+c)
            assert rem == rem_alt == 0
            high_ordinary = c+d-ordinary
            high_alternating = -(c-d)-alternating
            if all(abs(x) <= n and (x-n) % 2 == 0
                   for x, n in [(ordinary, low), (alternating, low),
                                (high_ordinary, high), (high_alternating, high)]):
                possible.append((low, high, charge))
    assert possible == [(c*c, c*c+3*a*b, -d)]
    return possible[0]


def read_word(a, b, word):
    """Check the whole-board half-planes, doubled area, displacement and all signed directions."""
    point = (0, 0)
    visited = {point}
    area2 = 0
    counts = Counter()
    for vector in word:
        x, y = (point[0]+vector[0], point[1]+vector[1])
        assert (x, y) not in visited
        assert (a+b)*y >= -b*x and a*y <= b*x and (a+b)*x+b*y <= a*(a+2*b)
        visited.add((x, y))
        area2 += cross(point, (x, y))
        counts[vector] += 1
        point = (x, y)
    assert point == (a+b, -b) and area2 == -a*b
    assert counts[E] == a and counts[S] == b and counts[U] == counts[NEG_U]
    return len(word)


def check_paths(a, b):
    shortest = [E]*a + [S]*b
    detour = [E]*(a-2) + [U, S, E, S, NEG_U, E] + [S]*(b-2)
    assert read_word(a, b, shortest) == a+b
    assert read_word(a, b, detour) == a+b+2
    forced = (a+b-1)//b
    for i in range(forced):
        for dx, dy in (U, NEG_U, S, (-1, 1)):
            x, y = i+dx, dy
            assert (a+b)*y < -b*x or a*y > b*x
    return forced


def check_minimal_paths():
    # Exhaust the step orders on a small example without imposing containment.
    for a, b in [(5, 3), (7, 3), (9, 5)]:
        maximum, words_at_maximum = a*b, []
        for subset in combinations(range(a+b), b):
            where = set(subset)
            word = [S if i in where else E for i in range(a+b)]
            x = y = area = 0
            for dx, dy in word:
                area -= x*dy - y*dx
                x, y = x+dx, y+dy
            assert area <= maximum
            if area == maximum:
                words_at_maximum.append(word)
        assert words_at_maximum == [[E]*a + [S]*b]


def shape(u, v):
    g = gcd(3, u-v)
    return (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g


def main():
    check_minimal_paths()
    tested = 0
    for u in range(2, 101, 2):
        for v in range(1, u, 2):
            if gcd(u, v) != 1:
                continue
            a, b, c = shape(u, v)
            if a > b:
                population_candidates(a, b, c)
                tested += 1
    print(f'Exact scalar checks on {tested} primitive odd shapes with u <= 100.')
    print('N  low  high  forced_bisector  interface_edges_min  detour_edges')
    for u, v in [(10, 1), (6, 1), (16, 1), (12, 1), (22, 1), (18, 1), (40, 1), (44, 3)]:
        a, b, c = shape(u, v)
        low, high, _ = population_candidates(a, b, c)
        forced = check_paths(a, b)
        print((a+2*b)*(2*a+b), low, high, c*forced, a+b, a+b+2)
    for path in [ROOT/'staircase'/'certificate_143.json', ROOT/'controls'/'double_3431.json',
                 ROOT/'controls'/'double_5063.json']:
        data = json.loads(path.read_text())
        print(f"Certified tiling {data['count']}, short-height populations: {board_angles_and_heights(data)}")


if __name__ == '__main__':
    main()
