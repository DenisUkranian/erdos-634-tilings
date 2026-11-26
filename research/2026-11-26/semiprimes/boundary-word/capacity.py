"""Paired-bank area upper bounds using integer determinants."""
from itertools import combinations, combinations_with_replacement
from spectrum import det, units


def capacity(a, b, c, r):
    assert r*r < c
    base = a, b
    axes = list(units((c, 0)))[:3] + list(units(base))[:3]
    def bound(vectors):
        return (c * sum(abs(det(base, v)) for v in vectors)
                + sum(abs(det(v, w)) for v, w in combinations(vectors, 2)))
    best = max(bound(vectors) for vectors in combinations_with_replacement(axes, r))
    return best // (a*b*c)


if __name__ == "__main__":
    for a, b, c in [(5, 3, 7), (33, 7, 37), (35, 13, 43)]:
        print((a, b, c), [capacity(a, b, c, r) for r in range(7) if r*r < c])
