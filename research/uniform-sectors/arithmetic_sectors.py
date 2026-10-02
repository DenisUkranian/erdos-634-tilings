#!/usr/bin/env python3
"""Exact arithmetic sector theorems for Erdos 634 (2026-10-01).

No floating point, geometry search, conjectural prime-case lemma, or external
package is used. A NOT_COVERED result is deliberately not a negative answer.
Trial-division factorization is exact, but is not optimized for large primes.
The mathematical scope and dependencies are in PROOF.md.
"""
from __future__ import annotations

import argparse
import json
from math import gcd, isqrt
from typing import Dict, List, Optional, Tuple


def factor(n: int) -> Dict[int, int]:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("A positive integer is required")
    out: Dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors_from_factors(f: Dict[int, int]) -> List[int]:
    out = [1]
    for p, e in sorted(f.items()):
        old = out[:]
        for j in range(1, e + 1):
            out.extend(d * p**j for d in old)
    return sorted(out)


def square_decomposition(n: int, f: Optional[Dict[int, int]] = None) -> Tuple[int, int]:
    """Return the unique squarefree k and m with n=k*m*m."""
    if f is None:
        f = factor(n)
    k = m = 1
    for p, e in f.items():
        if e % 2:
            k *= p
        m *= p ** (e // 2)
    if k * m * m != n:
        raise ValueError("Incorrect supplied factorization")
    return k, m


def legendre(a: int, p: int) -> int:
    """p must be an odd prime obtained from exact factorization."""
    if p < 3 or p % 2 == 0:
        raise ValueError("Odd prime required")
    r = pow(a % p, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def alpha_local_partitions(D: int) -> List[dict]:
    """Necessary (NOT sufficient) square-class partitions for alpha-isosceles.

    Intended sector: D odd squarefree, D=3 mod 8, and 3 does not divide D.
    An empty list rules the branch out at every odd scale not divisible by 3.
    """
    fs = factor(D)
    if D % 8 != 3 or D % 3 == 0 or any(e != 1 for e in fs.values()):
        raise ValueError("D must be squarefree, 3 mod 8, and prime to 3")
    accepted = []
    for A in divisors_from_factors(fs):
        B = D // A
        if A % 8 != 7 or B % 8 != 5:
            continue
        pa = [p for p in fs if A % p == 0]
        pb = [p for p in fs if B % p == 0]
        if any(legendre(2, p) != 1 or legendre(-B, p) != 1 for p in pa):
            continue
        if any(legendre(2 * A, p) != 1 for p in pb):
            continue
        accepted.append({"A": A, "B": B})
    return accepted


def qp_representations(n: int, f: Optional[Dict[int, int]] = None) -> Tuple[List[dict], int]:
    """Exhaust the constructive QP forms using divisors and integer squares.

    n=t^2*Q*P; v^2=P-Q; u^2=2P-3Q; 0<u<v; gcd(u,v)=1.
    Returns all representations and the number of tested unordered factor pairs.
    Positive results are globally sufficient for ANY n, not only the sector.
    """
    if f is None:
        f = factor(n)
    scales = divisors_from_factors({p: e // 2 for p, e in f.items() if e >= 2})
    result = []
    tested = 0
    for t in scales:
        tf = factor(t)
        df = {p: e - 2 * tf.get(p, 0) for p, e in f.items() if e - 2 * tf.get(p, 0) > 0}
        d = n // (t * t)
        for Q in divisors_from_factors(df):
            P = d // Q
            if Q >= P:
                continue
            tested += 1
            if gcd(Q, P) != 1 or not (3 * Q < 2 * P < 4 * Q):
                continue
            u2, v2 = 2 * P - 3 * Q, P - Q
            u, v = isqrt(u2), isqrt(v2)
            if u * u != u2 or v * v != v2 or not (0 < u < v) or gcd(u, v) != 1:
                continue
            a, b, c = u * v, v * v - u * u, v * v
            if (b + c) != Q or (b + 2 * c) != P or n != Q * P * t * t:
                raise ArithmeticError("Representation reconstruction failed")
            result.append({"u": u, "v": v, "t": t, "Q": Q, "P": P,
                           "tile_sides": [a, b, c],
                           "target_sides": [t * c * c, t * c * Q, t * b * P],
                           "tile_count": n})
    return sorted(result, key=lambda z: (z["v"], z["u"], z["t"])), tested


def solve(n: int) -> dict:
    """Decide the proved exact sector; never infer NO outside that sector."""
    f = factor(n)
    k, m = square_decomposition(n, f)
    out = {"N": n, "factorization": {str(p): e for p, e in f.items()},
           "squarefree_kernel": k, "square_multiplier": m,
           "full_Erdos634_solved": False}
    if n % 3 == 0 or n % 16 not in (6, 14):
        out.update(status="NOT_COVERED", reason="Outside the 3-coprime residue sector")
        return out
    D = k // 2
    out["D"] = D
    kernel_primes = [p for p, e in f.items() if p != 2 and e % 2]
    if n % 16 == 14:
        bad = [p for p in kernel_primes if legendre(2, p) == -1]
        if bad:
            out.update(status="NO", reason="Only W survives mod 16; inert-2 kernel prime rules W out",
                       obstructing_primes=bad)
        else:
            out.update(status="NOT_COVERED", reason="W branch not eliminated")
        return out
    partitions = alpha_local_partitions(D)
    out["alpha_local_partitions"] = partitions
    if partitions:
        # A QP construction is still a valid positive answer, but absence of
        # such a construction does NOT refute an alpha-isosceles candidate.
        reps, tested = qp_representations(n, f)
        out.update(qp_representations=reps, factor_pairs_tested=tested)
        if reps:
            out.update(status="YES", reason="Explicit QP construction")
        else:
            out.update(status="NOT_COVERED", reason="Local alpha test survives; geometry unresolved by this module")
        return out
    reps, tested = qp_representations(n, f)
    out.update(qp_representations=reps, factor_pairs_tested=tested,
               status="YES" if reps else "NO",
               reason="Exact QP equivalence: all other branches excluded")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("N", type=int, nargs="+")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    try:
        data = [solve(n) for n in args.N]
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as h:
            h.write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
