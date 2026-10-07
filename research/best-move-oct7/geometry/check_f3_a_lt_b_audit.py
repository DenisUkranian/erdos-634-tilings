"""Independent exact macro audit; no constructor imports or floating point."""
from math import gcd, isqrt
import json


def cross(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def area2(poly):
    return sum(p[0] * q[1] - p[1] * q[0] for p, q in zip(poly, poly[1:] + poly[:1]))


def ccw(poly):
    return poly if area2(poly) > 0 else list(reversed(poly))


def squared_lengths(poly):
    out = []
    for p, q in zip(poly, poly[1:] + poly[:1]):
        x, y = q[0] - p[0], q[1] - p[1]
        out.append(x * x + x * y + y * y)
    return sorted(out)


def disjoint_interiors(left, right):
    for p in (left, right):
        q = right if p is left else left
        for u, v in zip(p, p[1:] + p[:1]):
            if all(cross(u, v, w) <= 0 for w in q):
                return True
    return False


def check(a, b, c):
    A, B = a * b, b * b
    X, Y, K = (-a * a, 0), (2 * A, -2 * A - B), (2 * A, A + 2 * B)
    Q, E, L, R = (A, -A), (2 * A, -2 * A), (A, A + B), (2 * A, A + B)
    target = ccw([X, Y, K])
    pieces = list(map(ccw, [[X, Y, Q], [Y, Q, E], [L, R, K], [X, Q, L], [E, Q, L, R]]))
    counts = [c * c, b * b, b * b, (2 * a + b) * (a + b), 5 * a * b + 2 * b * b]
    assert squared_lengths(target) == sorted([c**4, c*c*(a+2*b)**2, 9*b*b*(a+b)**2])
    assert squared_lengths(pieces[0]) == sorted([a*a*c*c, b*b*c*c, c**4])
    for i in (1, 2):
        assert squared_lengths(pieces[i]) == sorted([a*a*b*b, b**4, b*b*c*c])
    assert squared_lengths(pieces[3]) == sorted([a*a*c*c, c*c*(a+b)**2, b*b*(2*a+b)**2])
    for p, n in zip(pieces, counts):
        assert area2(p) == a * b * n
        for u, v in zip(target, target[1:] + target[:1]):
            assert all(cross(u, v, w) >= 0 for w in p)
        for u, v in zip(p, p[1:] + p[:1]):
            assert all(cross(u, v, w) >= 0 for w in p)
    for i in range(len(pieces)):
        for j in range(i):
            assert disjoint_interiors(pieces[i], pieces[j])
    assert sum(map(area2, pieces)) == area2(target)
    assert sum(counts) == 3 * (a + b) * (a + 2 * b)
    assert [(x+y, 2*A-x) for x, y in [E, R, L, Q]] == [(0, 0), (3*A+B, 0), (2*A+B, A), (0, A)]
    d = a + b - c
    s = a*a + b*b - a*d
    assert 0 < d < a < b
    assert 2*A+B-s == a*(3*b-c) > 0


if __name__ == '__main__':
    examples = 0
    for b in range(2, 501):
        for a in range(1, b):
            c = isqrt(a*a+a*b+b*b)
            if c*c == a*a+a*b+b*b and gcd(a, b) == 1:
                check(a, b, c)
                examples += 1
    print(json.dumps({'status': 'PASS', 'primitive_examples': examples, 'maximum_b': 500,
           'pairwise_macro_checks': 10*examples, 'full_Erdos634_solved': False}, indent=2))
