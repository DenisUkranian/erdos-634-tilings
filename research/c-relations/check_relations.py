#!/usr/bin/env python3
"""Finite regression check of exact positive whole-edge relations.

The mathematical proof is in audit.md. This finite check is not a proof
of a geometric nonexistence result, an induction, or Erdős problem 634.
Uses only Python's standard library and exact integer arithmetic.
"""
from __future__ import annotations
import argparse
import json
from math import gcd
from pathlib import Path
from time import perf_counter


def decompositions(length: int, a: int, b: int, c: int) -> set[tuple[int, int, int]]:
    """Enumerate every nonnegative (A,B,C) with a*A+b*B+c*C=length.

    Enumeration is independent of the proposed c-relation parameterization.
    Since gcd(b,c)=1, each A gives a single B residue class modulo c.
    """
    inverse_b = pow(b, -1, c)
    answer: set[tuple[int, int, int]] = set()
    for A in range(length // a + 1):
        remaining = length - a * A
        B0 = (remaining * inverse_b) % c
        for B in range(B0, remaining // b + 1, c):
            C = (remaining - b * B) // c
            assert C >= 0 and a * A + b * B + c * C == length
            answer.add((A, B, C))
    return answer


def parameterized(n: int, u: int, v: int) -> set[tuple[int, int, int]]:
    a, b, c, d = u*v, v*v-u*u, v*v, v-u
    answer: set[tuple[int, int, int]] = set()
    for ell in range((n*c) // (v*b) + 1):
        first_h = (d*ell + v-1) // v
        last_h = (n-d*ell) // u
        for h in range(first_h, last_h+1):
            answer.add((v*h-d*ell, v*ell, n-u*h-d*ell))
    return answer


def run(max_v: int) -> dict:
    start = perf_counter()
    counts = {"primitive_pairs": 0, "c_lengths_tested": 0,
              "c_decompositions_tested": 0, "short_a_lengths_tested": 0,
              "short_b_lengths_tested": 0, "sharpness_checks": 0}
    for v in range(2, max_v+1):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            counts["primitive_pairs"] += 1
            a,b,c = u*v, v*v-u*u, v*v
            for n in range(0, 2*v+1):
                got = decompositions(n*c,a,b,c)
                expected = parameterized(n,u,v)
                assert got == expected, (u,v,n,got,expected)
                if n < u:
                    assert got == {(0,0,n)}, (u,v,n,got)
                if n < v:
                    assert all(B==0 for A,B,C in got), (u,v,n,got)
                if n == v:
                    assert {t for t in got if t[1]>0} == {(u,v,0)}
                counts["c_lengths_tested"] += 1
                counts["c_decompositions_tested"] += len(got)
            for i in range(1,v):
                assert decompositions(i*a,a,b,c) == {(i,0,0)}, (u,v,i,"a")
                assert decompositions(i*b,a,b,c) == {(0,i,0)}, (u,v,i,"b")
                counts["short_a_lengths_tested"] += 1
                counts["short_b_lengths_tested"] += 1
            assert u*c == v*a
            assert v*c == u*a+v*b
            assert v*b == (v-u)*(a+c)
            counts["sharpness_checks"] += 3
    return {"status": "PASS", "max_v": max_v,
            "c_range": "0 <= n <= 2*v for each primitive pair",
            "short_a_b_range": "1 <= i < v for each primitive pair",
            "arithmetic": "exact integers; exhaustive nonnegative decompositions",
            **counts, "elapsed_seconds": round(perf_counter()-start,3),
            "scope": "Finite arithmetic regression only. No geometric tiling or complete induction is certified."}


def main() -> None:
    if not __debug__:
        raise SystemExit("Use ordinary Python without -O; the arithmetic regression uses assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-v",type=int,default=40)
    parser.add_argument("--output",type=Path,default=None)
    args = parser.parse_args()
    if args.max_v < 2:
        parser.error("--max-v must be at least 2")
    result = run(args.max_v)
    text = json.dumps(result, indent=2)+"\n"
    print(text,end="")
    if args.output:
        args.output.write_text(text,encoding="utf-8")

if __name__ == "__main__":
    main()
