"""Exact positive-letter suffix bounds in two boundary groups."""
from functools import lru_cache
from terminal import UNITS, add, scale, det

def turn(p, j):
    x, y = p
    for _ in range(j % 6):
        x, y = (-y, x + y)
    return (x, y)

def prepend(w, k, e, m):
    if w and w[0][0] == k:
        e += w[0][1]
        w = w[1:]
    e %= m
    return ((k, e),) + w if e else w

@lru_cache(None)
def need(exps, m, ds):
    """Minimum positive ordinary letters after assigning or omitting defects."""
    if not ds:
        return sum(exps)
    v, *rest = ds
    rest = tuple(rest)
    return min([need(exps, m, rest)] + [need(exps[:i] + ((x - v) % m,) + exps[i + 1:], m, rest) for i, x in enumerate(exps)])

def census(a, b, c, hand, j, reverse=False):
    v = turn((a, b) if hand == 1 else (a + b, -b), j)
    H = a * (a + 2 * b)
    D = (a + b, -b)

    def inside(p):
        if reverse:
            p = add(scale(c, D), scale(-1, p))
        return det(D, p) >= 0 and det(p, (a, b)) >= 0 and (det((H * a - c * c * D[0], H * b - c * c * D[1]), add(p, scale(-c, D))) >= 0)

    def letter(m):
        k = (j + (hand if m == a else 0)) % 6
        e = (b if m == a else a) * pow(c, -1, m)
        if k >= 3:
            e = -e
        # Axis two uses the positive S generator in place of heading two.
        if k % 3 == 2:
            e = -e
        return (k % 3, e % m)
    la, lb = (letter(a), letter(b))
    results = []

    def visit(E, S, state, w1, w2, p, area, path, last):
        for m, w, (k, t) in ((a, w1, la), (b, w2, lb)):
            for ax, left in ((0, E), (2, S), (1, 0)):
                ds = () if ax != k or state == 2 else (t, -t) if state == 0 else (-t,)
                if need(tuple((r for i, r in w if i == ax)), m, ds) > left:
                    return
        if E + S == 0 and state == 2:
            assert not w1 and (not w2) and (p == scale(c, D))
            cap_area = area if reverse else -area
            if cap_area > 0 and cap_area % (a * b * c) == 0 and (cap_area // (a * b * c) % 2 == 1) and (cap_area // (a * b) <= (2 * a + b) * (a + 2 * b)):
                results.append((path, cap_area // (a * b)))
            return
        for tok in 'ES+-':
            if tok == 'E' and (not E) or (tok == 'S' and (not S)) or (tok == '+' and state != 0) or (tok == '-' and (state != 1 or last == '+')):
                continue
            if tok in 'ES':
                k = 0 if tok == 'E' else 2
                step = scale(c, UNITS[0 if tok == 'E' else 5])
                u = prepend(w1, k, -1, a)
                v2 = prepend(w2, k, -1, b)
            else:
                sign = 1 if tok == '+' else -1
                step = scale(sign, v)
                u = prepend(w1, la[0], -sign * la[1], a)
                v2 = prepend(w2, lb[0], -sign * lb[1], b)
            q = add(p, step)
            if inside(q):
                visit(E - (tok == 'E'), S - (tok == 'S'), state + (tok in '+-'), u, v2, q, area + det(p, q), path + tok, tok)
    visit(a, b, 0, ((2, b % a),), ((0, a % b),), (0, 0), 0, '', '')
    return results
