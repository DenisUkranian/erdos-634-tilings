#!/usr/bin/env python3
"""Exact finite arithmetic in TERMINAL_NODE_BALANCE.md; no tiling search."""


def pairs(m_max, l_max):
    return [
        (m, ell)
        for m in range(1, m_max + 1)
        for ell in range(1, l_max + 1)
        if (33 * m - 7 * ell) % 37 == 0
    ]


def main():
    # The universal integer substitutions, tested across residue classes.
    for m in range(3 * 43 + 1):
        for ell in range(3 * 43 + 1):
            if (35 * m - 13 * ell) % 43:
                continue
            t = (8 * m + 13 * ell) // 43
            assert (2 * m - t) % 13 == 0
            s = (2 * m - t) // 13
            assert 2 * ell == 6 * t - 8 * s
            assert (s - t) % 2 == 0
            if m + ell:
                assert t >= 1 and s <= t - 2
    assert (8 + 13) * 86 // 43 == 42
    assert (2 * 86 - 42) // 13 == 10
    assert (42 - 10) // 2 == 16
    assert 16 * 16 // 3 == 85 < 86

    for m in range(3 * 37 + 1):
        for ell in range(3 * 37 + 1):
            if (33 * m - 7 * ell) % 37:
                continue
            t = (11 * m + 10 * ell) // 37
            assert (2 * ell - 3 * t) % 11 == 0
            s = (2 * ell - 3 * t) // 11
            assert 2 * m == 4 * t - 10 * s
            assert (s - t) % 2 == 0
            if m + ell:
                assert t >= 1 and s <= t - 2
    assert (11 + 10) * 74 // 37 == 42
    assert (2 * 74 - 3 * 42) // 11 == 2
    assert (42 - 2) // 2 == 20
    assert all(ell != 1 for _, ell in pairs(19, 19))
    assert pairs(9, 9) == [(4, 3), (8, 6)]
    assert pairs(8, 8) == [(4, 3), (8, 6)]
    assert pairs(8, 10) == [(1, 10), (4, 3), (8, 6)]
    assert pairs(10, 4) == [(4, 3)]
    # The family-2 aggregate (4,40) has the asserted unique decomposition.
    solutions = []
    for first in range(5):
        for second in range(2):
            for third in range(1):
                if first + 4 * second + 8 * third == 4 and \
                        10 * first + 3 * second + 6 * third == 40:
                    solutions.append((first, second, third))
    assert solutions == [(4, 0, 0)]
    assert 4 % 3 != 0
    print("Verified terminal-node arithmetic for 3431 and 5063.")


if __name__ == "__main__":
    main()
