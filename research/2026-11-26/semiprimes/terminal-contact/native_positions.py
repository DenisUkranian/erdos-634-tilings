"""Test actual long-edge owners in the reflected middle chart."""
from terminal import add, scale
from two_native import turn, census
from itertools import combinations, product

def cross(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def overlap(A, B):
    for P, Q in ((A, B), (B, A)):
        for p, q in zip(P, P[1:] + P[:1]):
            if all((cross(p, q, r) <= 0 for r in Q)):
                return False
    return True

def covered(p, path):
    """Clockwise winding at the centroid whose tripled coordinates are p."""
    n = 0
    for u, v in zip(path, path[1:] + path[:1]):
        x = p[0] - 3 * u[0]
        y = p[1] - 3 * u[1]
        d = (v[0] - u[0]) * y - (v[1] - u[1]) * x
        if u[1] * 3 <= p[1] < v[1] * 3 and d > 0:
            n -= 1
        if v[1] * 3 <= p[1] < u[1] * 3 and d < 0:
            n += 1
    return n

def shape(a, b, c, s, j, word):
    z = (a, b) if s == 1 else (a + b, -b)
    board = [(0, 0), scale(c * c, (a + b, -b)), scale(a * (a + 2 * b), (a, b))]
    p = (0, 0)
    path = [p]
    owners = []
    for ch in word:
        rot = 0 if ch == 'E' else 5 if ch == 'S' else j if ch == '+' else j + 3
        B = ch in '+-'
        step = turn(scale(c, z) if B else (c * c, 0), rot)
        off = turn((c * a, 0) if B else scale(a, z), rot)
        q = add(p, step)
        r = add(p, off)
        tri = (p, q, r) if cross(p, q, r) > 0 else (q, p, r)
        if any((cross(u, v, r) < 0 for u, v in zip(board, board[1:] + board[:1]))):
            return
        owners.append((B, tri))
        path.append(q)
        p = q
    if len(path) != len(set(path)):
        return
    if any((overlap(P, Q) for (_, P), (_, Q) in combinations(owners, 2))):
        return
    for B, P in owners:
        cen = tuple(map(sum, zip(*P)))
        if covered(cen, path) != int(B == (s == 1)):
            return
    return (path, owners)

def main(a, b, c):
    rows = {}
    for s in (-1, 1):
        vals = []
        for j in range(6):
            r = census(a, b, c, s, j)
            back = census(a, b, c, s, (j + 3) % 6, reverse=True)
            assert set(r) == {(w[::-1].translate(str.maketrans('+-', '-+')), n) for w, n in back}
            for w, n in r:
                z = shape(a, b, c, s, j, w)
                if z:
                    vals.append((n, j, w, *z))
        rows[s] = vals
    good = []
    for C, T in product(rows[1], rows[-1]):
        if C[0] - T[0] < 2 * c:
            continue
        if any((overlap(P, Q) for _, P in C[4] for _, Q in T[4])):
            continue
        if any((covered(tuple(map(sum, zip(*P))), C[3]) != 1 for _, P in T[4])):
            continue
        if any((covered(tuple(map(sum, zip(*P))), T[3]) != 0 for _, P in C[4])):
            continue
        good.append((C[:3], T[:3]))
    return good
