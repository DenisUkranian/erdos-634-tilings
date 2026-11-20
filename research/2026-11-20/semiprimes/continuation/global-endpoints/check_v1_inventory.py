#!/usr/bin/env python3
"""Check an unplaced direction inventory. This is NOT a geometric tiling."""
from collections import Counter
from math import gcd


def inventory(a, b, c):
    assert a > b > 0 and a % 2 and b % 2 and c % 2
    assert a*a + a*b + b*b == c*c
    N = (a + 2*b) * (2*a + b)
    count = Counter({(0, 3, 1): 2*a, (0, 4, 1): a, (0, 2, 1): b,
                     (1, 4, 1): c, (1, 0, -1): 2*c})
    pads = ((0, (N - c*c - 3*a - b)//2), (1, (c*c - 3*c)//2))
    assert 2*pads[0][1] == N - c*c - 3*a - b
    assert 2*pads[1][1] == c*c - 3*c
    for h, n in pads:
        assert n >= 0
        count[h, 0, 1] += n
        count[h, 3, 1] += n
    return count


def signature(a, b, c, h, j, s):
    result = Counter()
    def add(H, J, length):
        J %= 6
        result[H, J % 3] += length if J < 3 else -length
    add(h, j, s*a)
    add(h, j+s, s*b)
    add(h+s, j, -s*c)
    return result


def check(a, b, c):
    counts = inventory(a, b, c)
    total = Counter()
    height = Counter()
    for (h, j, s), n in counts.items():
        height[h] += n
        for row, value in signature(a, b, c, h, j, s).items():
            total[row] += n*value
    total = {r: v for r, v in total.items() if v}
    N = (a + 2*b) * (2*a + b)
    assert total == {(0, 0): b*(2*a+b), (0, 1): -a*(a+2*b), (2, 1): c*c}
    assert sum(counts.values()) == N
    assert height == {0: c*c + 3*a*b, 1: c*c}
    return N, dict(height)


if __name__ == '__main__':
    for u in range(4, 206, 2):
        g = gcd(3, u-1)
        check((u*u-1)//g, (2*u+1)//g, (u*u+u+1)//g)
    print('101 v=1 orientation inventories passed; no placements or tilings asserted.')
    for triple in ((33, 7, 37), (35, 13, 43)):
        print(triple, check(*triple))
