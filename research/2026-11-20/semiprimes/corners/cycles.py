"""Positive cyclic counting lower bound from PROOF.md, using exact arithmetic."""
from fractions import Fraction
from itertools import accumulate
from math import gcd


def differences(d, e, a, b, c, outer):
    jumps = [0] * e
    if outer:
        jumps[0] = c
        for j in range(c):
            jumps[j % e] -= 1
    else:
        n = a - b
        jumps[0] = -n
        for j in range(1, n + 1):
            jumps[j % e] += 1
    assert sum(jumps) == 0
    return jumps


def residue_price(levels, modulus):
    counts = [0] * modulus
    for value in levels:
        counts[value % modulus] += 1
    total = sum(i * size for i, size in enumerate(counts))
    best = total
    for i in range(modulus - 1, 0, -1):
        total += len(levels) - modulus * counts[i]
        best = min(best, total)
    return best


def projection(a, b, c, v, outer, x_axis):
    d, e = (c, a) if outer == x_axis else (a, c)
    kappa = d * pow(b, -1, e) % e
    levels = list(accumulate(differences(d, e, a, b, c, outer)))
    smooth = [sum(levels[(i-l*kappa) % e] for l in range(v)) for i in range(e)]
    return d, residue_price(smooth, d)


def bound(u, v):
    g = gcd(3, u-v)
    a, b, c = (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g
    assert gcd(u, v) == 1 and a > b and v*(a+c) == b*u
    entries = [projection(a, b, c, v, outer, x_axis)
               for outer in (True, False) for x_axis in (True, False)]
    lower = Fraction(sum(d*cost for d, cost in entries), (a+c)*v)
    budget = (3*a*b-c-(a-b))//2
    return (a, b, c), [cost for d, cost in entries], lower, budget


if __name__ == '__main__':
    for u, v in [(10, 1), (6, 1), (16, 1), (12, 1), (22, 1), (18, 1), (40, 1), (86, 5)]:
        tile, costs, price, budget = bound(u, v)
        a, b, c = tile
        print(f'N={(a+2*b)*(2*a+b)}, (u,v)=({u},{v}), tile={tile}, D={costs}, needed={price}, available={budget}')
        assert price > budget
