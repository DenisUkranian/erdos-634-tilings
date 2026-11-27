"""Moments and widths of actual pairs after removing four prescribed middle owners."""
from collections import Counter
from terminal import UNITS, add, scale, det
from functools import lru_cache

@lru_cache(None)
def row(a, b, c, s, j, w):
    steps = []
    for ch in w:
        if ch in 'ES012345':
            k = int(ch) if ch.isdigit() else {'E': 0, 'S': 5}[ch]
            steps.append((k, c))
        else:
            assert ch in '+-67'
            k = j if ch in '+6' else j + 3
            steps.extend([(k % 6, a), ((k + s) % 6, b)])
    return steps

def valid(a, b, c, C, T):
    rows = [Counter() for _ in range(3)]
    tor = [Counter(), Counter()]
    # Negate the clockwise axial contour and add the slant one.
    for record, s in [(C, 1), (T, -1)]:
        n, j, w = record
        p = (0, 0)
        for k, d in row(a, b, c, s, j, w):
            q = add(p, scale(d, UNITS[k]))
            rows[k % 3][det(UNITS[k % 3], p)] -= s * d * (1 if k < 3 else -1)
            for A, m in zip(tor, (a, b)):
                A[k % 3, p[0] % m, p[1] % m] += s
                A[k % 3, q[0] % m, q[1] % m] -= s
            p = q
    K = (C[0] - T[0] - 4) // 2
    J = [-sum((t * h for t, h in r.items())) for r in rows]
    assert sum(J) == 2 * a * b * K
    if any((i < 0 or i > K * a * b or i % (a * b) for i in J)):
        return 0
    if any((any(r.values()) for r in tor)):
        return 1
    ok = {a * i + b * j for i in range(K + 1) for j in range(K + 1 - i)}
    for r in rows:
        v = 0
        for t in sorted(r):
            v += r[t]
            if v not in ok:
                return 2
    return 3
