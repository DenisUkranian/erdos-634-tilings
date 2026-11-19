"""Enumerate the five exactly placed corner tiles of a possible 280-tiling."""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm


# A point (x,y) means x + i sqrt(2) y.
left, right, top = (0, 0), (140, 0), (70, 40)
apex_left = (F(-7, 9), F(-4, 9))
apex_right = (F(7, 9), F(-4, 9))
turn = {"a": (F(7, 9), F(4, 9)), "b": (F(23, 27), F(10, 27))}
adjacent = {"a": (5, 9), "b": (6, 9)}


def rotate(p, u):
    return p[0]*u[0] - 2*p[1]*u[1], p[0]*u[1] + p[1]*u[0]


def advance(p, u, length):
    return p[0] + length*u[0], p[1] + length*u[1]


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])


def squared(p, q):
    return (q[0]-p[0])**2 + 2*(q[1]-p[1])**2


def canonical(tile):
    return tuple(sorted(tile))


def at_corner(p, start, end, angle, order):
    lengths = adjacent[angle][::1 if order == 0 else -1]
    tile = p, advance(p, start, lengths[0]), advance(p, end, lengths[1])
    assert sorted(squared(tile[j-1], tile[j]) for j in range(3)) == [25, 36, 81]
    return canonical(tile)


def common_denominator(pattern):
    return lcm(*(F(coord).denominator for tile in pattern for point in tile for coord in point))


def interior_disjoint(t, s):
    for polygon, other in ((t, s), (s, t)):
        for i in range(3):
            a, b, c = polygon[i-2], polygon[i-1], polygon[i]
            if all(det(a,b,c)*det(a,b,p) <= 0 for p in other):
                return True
    return False


def mirror(pattern):
    return tuple(sorted(canonical((140-x,y) for x,y in tile) for tile in pattern))


def solve():
    top_den = {}
    full_patterns = set()
    base_left = [at_corner(left, (1,0), (F(7,9),F(4,9)), "a", order) for order in range(2)]
    base_right = [at_corner(right, (-1,0), (F(-7,9),F(4,9)), "a", order) for order in range(2)]
    board = (left,right,top)
    for sequence in sorted(set(permutations("abb"))):
        rays = [apex_left]
        for angle in sequence:
            rays.append(rotate(rays[-1], turn[angle]))
        assert rays[-1] == apex_right
        counts = Counter()
        for orders in product(range(2), repeat=3):
            fan = tuple(at_corner(top, rays[i], rays[i+1], angle, orders[i])
                        for i,angle in enumerate(sequence))
            counts[common_denominator(fan)] += 1
            for ltile,rtile in product(base_left,base_right):
                pattern = tuple(sorted((*fan,ltile,rtile)))
                assert all(det(board[j-1],board[j],p) >= 0
                           for tile in pattern for p in tile for j in range(3))
                assert all(interior_disjoint(t,s) for j,t in enumerate(pattern) for s in pattern[:j])
                full_patterns.add(pattern)
        top_den["".join(sequence)] = dict(sorted(counts.items()))
    assert len(full_patterns) == 96
    assert all(mirror(p) in full_patterns and p != mirror(p) for p in full_patterns)
    representatives = {min(p, mirror(p)) for p in full_patterns}
    all_den = Counter(map(common_denominator, full_patterns))
    reps_den = Counter(map(common_denominator, representatives))
    assert dict(reps_den) == {3:4, 9:20, 27:8, 81:16}
    print("Apex fans by order and least denominator:", top_den)
    print("Marked five-tile patterns:", len(full_patterns), dict(sorted(all_den.items())))
    print("Reflection classes:", len(representatives), dict(sorted(reps_den.items())))


if __name__ == "__main__":
    solve()
