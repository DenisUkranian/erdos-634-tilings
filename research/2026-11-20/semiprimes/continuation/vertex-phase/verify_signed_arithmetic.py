#!/usr/bin/env python3
"""Exact replay of the sign convention and population arithmetic."""

from fractions import Fraction as F
import json


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def neg(p):
    return -p[0], -p[1]


def scale(t, p):
    return t * p[0], t * p[1]


def mul(p, q):
    x, y = p
    u, v = q
    return x * u - y * v, x * v + y * u + y * v


def parity(k):
    return 1 if k % 2 == 0 else -1


def norm(p):
    x, y = p
    return x * x + x * y + y * y


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def check(a, b, c, expected):
    rho = (F(0), F(1))
    units = [(F(1), F(0))]
    for _ in range(5):
        units.append(mul(units[-1], rho))
    z = (F(a, c), F(b, c))
    zi = (F(a + b, c), F(-b, c))
    assert norm(z) == 1 and mul(z, zi) == (1, 0)

    def heading(h, j):
        r = units[j % 6]
        base = z if h >= 0 else zi
        for _ in range(abs(h)):
            r = mul(r, base)
        return r

    d = a - b
    checked = 0
    for h in range(-3, 4):
        for j in range(6):
            for s in (-1, 1):
                u = scale(-a, heading(h, j))
                q = (F(0), F(0))
                w = scale(b, heading(h, j + s))
                vertices = [u, q, w] if s == 1 else [w, q, u]
                assert det(add(vertices[1], neg(vertices[0])),
                           add(vertices[2], neg(vertices[0]))) == a * b
                sides = ([(a, h, j), (b, h, j + 1), (c, h + 1, j + 3)]
                         if s == 1 else
                         [(b, h, j + 2), (a, h, j + 3), (c, h - 1, j)])
                for i, (length, height, phase) in enumerate(sides):
                    actual = add(vertices[(i + 1) % 3], neg(vertices[i]))
                    assert actual == scale(length, heading(height, phase))
                    assert norm(actual) == length * length
                eps = s * parity(j)
                current = sum(length * parity(phase) for length, height, phase in sides)
                alternating = sum(length * parity(height + phase)
                                  for length, height, phase in sides)
                assert current == (d - c) * eps
                assert alternating == (d + c) * parity(h) * eps
                checked += 1

    A, B = b * (2 * a + b), a * (a + 2 * b)
    assert scale(c * c, heading(2, 1)) == (-A, B)
    N = (a + 2 * b) * (2 * a + b)
    assert A - c * c + B == 3 * a * b
    assert F(3 * a * b, d - c) == -(c + d)
    assert F(3 * a * b, d + c) == c - d
    P, Q = (N - c - d) // 2, (N + c + d) // 2
    assert P + Q == N and P - Q == -(c + d)
    inv2 = pow(2, -1, c)
    rp, rn = ((N - d) * inv2) % c, ((N + d) * inv2) % c
    assert (rp + rn - N) % c == 0
    assert ((a - b) * (rp - rn) - N) % c == 0
    assert (P - rp) % c == 0 and (Q - rn) % c == 0
    kp, kq = (P - rp) // c, (Q - rn) // c
    assert (d + rp - rn) % c == 0
    delta = (d + rp - rn) // c
    assert kq == kp + delta + 1
    assert [N, rp, rn, P, Q, kp, kq, delta] == expected
    # Odd-height signed blocks sum to -1, so at least one node has
    # an odd population of at least three blocks, rather than two.
    ordinary_node_limit = (N - rp - rn - c) // (2 * c)
    assert rp + rn + 2 * c * ordinary_node_limit + c <= N
    assert rp + rn + 2 * c * (ordinary_node_limit + 1) + c > N
    # A total-sign-feasible allocation rejected by the parity refinement.
    pe, po, qe, qo = 0, 1, kp + delta, 0
    assert pe + po <= kp and qe + qo <= kq
    assert qe + po > kp + delta
    assert max(pe, qe - delta) + max(po, qo - 1) > kp
    return {
        "N": N, "tile": [a, b, c], "checked_oriented_placements": checked,
        "core_residues": [rp, rn], "full_sign_populations": [P, Q],
        "remaining_block_budgets": [kp, kq], "even_block_defect": delta,
        "ordinary_node_limit_with_parity": ordinary_node_limit,
    }


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    cases = [
        check(33, 7, 37, [3431, 19, 8, 1684, 1747, 45, 47, 1]),
        check(35, 13, 43, [5063, 5, 27, 2499, 2564, 58, 59, 0]),
        check(5, 3, 7, [143, 4, 6, 67, 76, 9, 10, 0]),
    ]
    assert [row["ordinary_node_limit_with_parity"] for row in cases] == [45, 58, 9]
    print(json.dumps({
        "scope": "Necessary population constraints; 3431 and 5063 remain undecided.",
        "cases": cases,
    }, indent=2))

