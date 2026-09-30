#!/usr/bin/env python3
"""Exact finite candidate sieve for congruent triangle tilings.

A returned candidate is NOT a tiling. The exhaustive geometric/rationality
inputs and the derivation of this finite list are stated in PROOF.md.
No candidate scale-one W/beta nonexistence theorem is used.
Standard library only. All checks remain active under python -O.
"""
from __future__ import annotations
import argparse
import json
from math import gcd, isqrt
from dataclasses import dataclass, asdict
from typing import Iterable


def square_root(n: int) -> int | None:
    if n < 0:
        return None
    r = isqrt(n)
    return r if r*r == n else None


def divisors(n: int) -> list[int]:
    if n < 1:
        raise ValueError('n must be positive')
    low, high = [], []
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            low.append(d)
            if d*d != n:
                high.append(n//d)
    return low + high[::-1]


def heron16(sides: Iterable[int]) -> int:
    a, b, c = sides
    return (a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c)


def classical(n: int) -> dict | None:
    """Only explicitly constructed classical families, not a converse test."""
    if n < 1:
        raise ValueError('n must be positive')
    for c in (1, 2, 3, 6):
        if n % c == 0:
            r = square_root(n//c)
            if r:
                return {'type': f'{c} times a square', 'multiplier': r}
    for a in range(1, isqrt(n)+1):
        b = square_root(n-a*a)
        if b:
            return {'type': 'sum of two squares', 'a': a, 'b': b}
    return None


@dataclass(frozen=True)
class Instance:
    branch: str
    tile: tuple[int, int, int]
    target: tuple[int, int, int]
    n: int
    parameters: tuple[int, ...]
    multiplier: int

    def validate(self) -> None:
        if min(self.tile + self.target) < 1:
            raise ValueError('Nonpositive side')
        if gcd(gcd(*self.tile[:2]), self.tile[2]) != 1:
            raise ValueError('Tile not primitive')
        h, H = heron16(self.tile), heron16(self.target)
        if h <= 0 or H != self.n*self.n*h:
            raise ValueError(f'Area mismatch: {self}')


def enumerate_candidates(n: int, *, remove_scale_one: bool = True) -> list[Instance]:
    """A complete OVERLIST of irrational-angle, nonsimilar, nonright cases.

    The optional removal uses the elementary theta and double-angle m=1
    obstructions proved in PROOF.md. It does not remove W/beta m=1.
    The list can be used on classical n as well, to test fixed instances.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    out: dict[tuple, Instance] = {}

    def add(branch, tile, shape, factor, parameters, min_m=1):
        if factor < 1 or n % factor:
            return
        t = square_root(n//factor)
        if t is None or t < min_m:
            return
        obj = Instance(branch, tuple(tile), tuple(x*t for x in shape), n, tuple(parameters), t)
        obj.validate()
        # Keep branch labels: coincident instances can have distinct provenance.
        out[(branch, tuple(sorted(tile)), tuple(sorted(obj.target)))] = obj

    div = divisors(n)
    cores = [b for b in div if square_root(n//b) is not None]

    # b divides n for theta and double-angle; factor b=(v-u)(v+u).
    pairs = set()
    for b in cores:
        for r in divisors(b):
            s = b//r
            if r >= s or (r+s) % 2:
                continue
            u, v = (s-r)//2, (s+r)//2
            if u < 1 or gcd(u, v) != 1:
                continue
            pairs.add((u, v))
            tile = (u*v, b, v*v)
            add('G1-theta', tile, (b*v, b*v, b*u), b, (u, v), 2 if remove_scale_one else 1)
            if v < 2*u:
                add('double-angle', (u*u, b, u*v), (b*u, b*u, b*v), b, (u, v), 2 if remove_scale_one else 1)

    # Other four Group-1 rows have Q>v^2 and their count factor >= Q.
    for v in range(2, isqrt(n)+1):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            a, b, c = u*v, v*v-u*u, v*v
            Q, P = b+c, b+2*c
            add('G1-W', (a,b,c), (v**3,u*Q,v*b), Q, (u,v))
            add('G1-beta', (a,b,c), (v**3,v**3,u*P), P, (u,v))
            add('G1-alpha', (a,b,c), (b*c,b*c,b*Q), b*Q, (u,v))
            add('G1-other-scalene', (a,b,c), (c*c,c*Q,b*P), Q*P, (u,v))

    # Equilateral 60/120: ab divides n, n/(ab) is an integer square.
    eq_pairs = set()
    for ab in cores:
        for a in divisors(ab):
            b = ab//a
            if a > b or a < 2 or gcd(a,b) != 1:
                continue
            eq_pairs.add((a,b))
            for sign, branch in ((1, 'E120'), (-1, 'E60')):
                c = square_root(a*a + sign*a*b + b*b)
                if c:
                    add(branch, (a,b,c), (ab,ab,ab), ab, (a,b))

    # F1 and isosceles 120: stronger parity-derived b(a+j b)|n.
    p120 = set()
    for core in cores:
        for b in divisors(core):
            for j in (1,2):
                a = core//b-j*b
                if a > 0 and gcd(a,b) == 1:
                    p120.add((a,b))

    # Product rows. Factoring the coefficient avoids arbitrary tile-size cutoffs.
    for core in cores:
        if core % 3 == 0:
            for x in divisors(core//3):
                y = core//(3*x)
                a, b = 2*x-y, y-x
                if a > 0 and b > 0 and gcd(a,b) == 1:
                    p120.add((a,b))
        for x in divisors(core):
            y = core//x
            # x=a+b, y=2a+b (F4).
            a,b = y-x, 2*x-y
            if a > 0 and b > 0 and gcd(a,b) == 1:
                p120.add((a,b))
            # x=a+2b, y=2a+b (F2).
            if (2*y-x) % 3 == 0 and (2*x-y) % 3 == 0:
                a,b = (2*y-x)//3, (2*x-y)//3
                if a > 0 and b > 0 and gcd(a,b) == 1:
                    p120.add((a,b))

    for a,b in sorted(p120):
        c = square_root(a*a+a*b+b*b)
        if c is None:
            continue
        tile=(a,b,c)
        add('F1-120',tile,(a*b,b*c,b*(a+b)),b*(a+b),(a,b))
        add('I120',tile,(b*c,b*c,b*(a+2*b)),b*(a+2*b),(a,b))
        add('F3-120',tile,(c*c,c*(a+2*b),3*b*(a+b)),3*(a+2*b)*(a+b),(a,b))
        add('F4-120',tile,(a*c,b*(2*a+b),c*(a+b)),(2*a+b)*(a+b),(a,b))
        add('F2-120',tile,(a*(a+2*b),b*(2*a+b),c*c),(a+2*b)*(2*a+b),(a,b))
    return sorted(out.values(), key=lambda z:(z.branch,z.tile,z.target))


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('n',type=int)
    ap.add_argument('--keep-scale-one',action='store_true')
    ap.add_argument('--output')
    args=ap.parse_args()
    rows=enumerate_candidates(args.n,remove_scale_one=not args.keep_scale_one)
    report={'n':args.n,'classical_witness':classical(args.n),'candidate_count':len(rows),
            'candidates':[asdict(x) for x in rows],
            'meaning':'Overlist, not an existence proof. Empty list excludes only after the stated exhaustive classification inputs.',
            'full_problem_solved':False}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
