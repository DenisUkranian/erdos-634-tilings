#!/usr/bin/env python3
"""Finite exact checks for the written two-isogeny descent; no rank oracle."""
from pathlib import Path
from math import gcd
import json


def squarefree(n):
    sign = -1 if n < 0 else 1
    n = abs(n)
    p, out = 2, sign
    while p * p <= n:
        parity = 0
        while n % p == 0:
            n //= p
            parity ^= 1
        if parity:
            out *= p
        p += 1
    return out * n


def obstruction(name, coefficients, p):
    modulus = p * p
    squares = {w*w % modulus for w in range(modulus)}
    possible = []
    a, b, c = coefficients
    tested = 0
    for u in range(modulus):
        for v in range(modulus):
            if u % p == v % p == 0:
                continue
            tested += 1
            if (a*u**4 + b*u*u*v*v + c*v**4) % modulus in squares:
                possible.append([u, v])
    assert not possible, (name, possible)
    return dict(name=name, coefficients=coefficients, modulus=modulus,
                primitive_pairs_tested=tested, possible_pairs=possible)


def point_count(p):
    affine = [[x, y] for x in range(p) for y in range(p)
              if (y*y - x*x*x - 125) % p == 0]
    return dict(prime=p, count=1+len(affine), affine_points=affine)


def main():
    covers = [obstruction('E_d5', [5, -15, 15], 5),
              obstruction('Eprime_d3', [3, 30, -25], 3),
              obstruction('Eprime_d5', [5, 30, -15], 5),
              obstruction('Eprime_dm5', [-5, 30, 15], 5)]
    E_candidates = {1, 3, 5, 15}
    E_rejected = {5, squarefree(5*3)}
    Eprime_candidates = {-15, -5, -3, -1, 1, 3, 5, 15}
    Eprime_rejected = {squarefree(d*t) for d in [3, 5, -5] for t in [1, -3]}
    images = [sorted(E_candidates-E_rejected),
              sorted(Eprime_candidates-Eprime_rejected)]
    assert images == [[1, 3], [-3, 1]]
    points = [point_count(7), point_count(17)]
    assert [p['count'] for p in points] == [4, 18]
    assert gcd(*(p['count'] for p in points)) == 2
    assert all((2*v*v-u*u) % 5 for u in range(5) for v in range(5)
               if u or v)
    out = dict(status='PASS', covers=covers, descent_images=images,
               rank_from_two_isogeny_formula=0, good_reduction_counts=points,
               rational_torsion_order=2,
               scope='Finite checks supporting CLASS15_NO_W_F3.md; no geometric135 decision')
    Path(__file__).with_name('class15_overlap_checked.json').write_text(
        json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ['status', 'descent_images',
                                        'rank_from_two_isogeny_formula',
                                        'rational_torsion_order']}))


if __name__ == '__main__':
    main()
