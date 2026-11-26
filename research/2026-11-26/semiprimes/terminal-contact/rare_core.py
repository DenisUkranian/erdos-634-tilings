"""Exclude the five-direction core inventory at M=107 on the 3431 board."""
from collections import Counter
from functools import lru_cache

from junction import Model, ccw, contains, overlap
from terminal import UNITS, add, scale


def rotate(p, j):
    for _ in range(j):
        p = -p[1], p[0] + p[1]
    return p


def clean(triangles):
    return all(not overlap(p, q) for i, p in enumerate(triangles) for q in triangles[:i])


def positioned(word, owner, size):
    counts = [0] * size
    result = []
    for token in word:
        result.append(owner(tuple(counts), token))
        counts[token] += 1
    return result


def verify():
    a, b, c = 33, 7, 37
    model = Model(a, b, c)
    # Effective bank, heading, multiplicity; the high bank supplies the core owners.
    letters = [(0, 0, 14), (0, 2, 1), (0, 4, 33), (1, 2, 1), (1, 4, 10)]
    caps = tuple(n for _, _, n in letters)
    zero = (0,) * len(letters)
    native = [rotate((a, b) if bank else (c, 0), j) for bank, j, _ in letters]
    moves = [rotate((c, 0) if bank else (a+b, -b), j) for bank, j, _ in letters]
    apex = [rotate((a*(a+b), -a*b) if bank else (a*c, 0), j) for bank, j, _ in letters]

    def displacement(counts, vectors):
        return tuple(sum(k*v[i] for k, v in zip(counts, vectors)) for i in range(2))

    @lru_cache(None)
    def owner(s, token):
        p = scale(c, displacement(s, moves))
        return ccw(p, add(p, scale(c, moves[token])), add(p, apex[token]))

    @lru_cache(None)
    def options(s, last):
        out = []
        for token, cap in enumerate(caps):
            if s[token] == cap:
                continue
            poly = owner(s, token)
            if not all(contains(p, model.board) for p in poly):
                continue
            if last >= 0:
                prev = list(s)
                prev[last] -= 1
                if overlap(owner(tuple(prev), last), poly):
                    continue
            nxt = list(s)
            nxt[token] += 1
            out.append((token, tuple(nxt)))
        return out

    @lru_cache(None)
    def viable(s, last):
        return s == caps or any(viable(nxt, token) for token, nxt in options(s, last))

    @lru_cache(None)
    def extensions(s, last, vertical, diagonal, horizontal, diagonal_b):
        x, y = displacement(s, native)
        y += model.B
        states = []
        for token, nxt in options(s, last):
            if not viable(nxt, token):
                continue
            residues = [vertical, diagonal, horizontal, diagonal_b]
            checks = []
            if token == 2:
                checks.append((0, x % a))
            if token in (1, 4):
                checks.append((1, (x+y) % a))
            if token == 3 or (token == 0 and y % a):
                checks.append((2, y % a))
            if token in (1, 3):
                checks.append((3, (x+y) % b))
            if any(residues[k] not in (-1, value) for k, value in checks):
                continue
            for k, value in checks:
                residues[k] = value
            states.append((nxt, token, *residues))
        return states

    @lru_cache(None)
    def count(state):
        return 1 if state[0] == caps else sum(count(ns) for ns in extensions(*state))

    def words(state, prefix):
        if state[0] == caps:
            yield prefix
            return
        for ns in extensions(*state):
            if count(ns):
                yield from words(ns, prefix+(ns[1],))

    @lru_cache(None)
    def edge(p, j, length):
        q = add(p, scale(length, UNITS[j]))
        increments = []
        for m in (a, b):
            increments.append(((m, j % 3, p[0] % m, p[1] % m), -1))
            increments.append(((m, j % 3, q[0] % m, q[1] % m), 1))
        return q, increments

    def exact_tori(word):
        # O -> Y -> X -> O is the negative of the core remainder boundary.
        p = (0, 0)
        coefficients = Counter()

        def take(j, length):
            nonlocal p
            p, changes = edge(p, j, length)
            for key, delta in changes:
                coefficients[key] += delta

        take(1, model.B)
        for token in word:
            bank, j, _ = letters[token]
            if bank:
                take(j, a)
                take((j+1) % 6, b)
            else:
                take(j, c)
        take(3, model.A)
        assert p == (0, 0)
        return not any(coefficients.values())

    start = (zero, -1, -1, -1, -1, -1)
    assert count(start) == 6186
    survivors = [w for w in words(start, ()) if exact_tori(w)]
    assert len(survivors) == 85
    first = [P for w in survivors if clean(P := positioned(w, owner, 5))]
    second = [P for w, _ in model.upper()
              if clean(P := positioned(map(int, w), lambda s, t: model.tri(1, s, t), 3))]
    assert (len(first), len(second)) == (30, 42)
    assert all(any(overlap(p, q) for p in P for q in Q) for P in first for Q in second)
    print("3431 five-direction core: 6186 words, 85 torus passes, 30 disjoint-owner paths; all 30 x 42 pairings conflict.")


if __name__ == "__main__":
    verify()
