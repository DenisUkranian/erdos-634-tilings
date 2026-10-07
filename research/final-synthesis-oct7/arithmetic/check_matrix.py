#!/usr/bin/env python3
"""Exact finite checks for the written local matrix obstruction.

No consistent matrix is reported as a realizable tiling count.
Run from any directory; --R gives one factored square class 6R.
"""
import argparse
import itertools
import json
import math


def prime(n):
    return n >= 2 and all(n % q for q in range(2, math.isqrt(n) + 1))


def legendre(a, p):
    z = pow(a % p, (p - 1) // 2, p)
    return 0 if z == 0 else (1 if z == 1 else -1)


def bit(sign):
    assert sign in (-1, 1)
    return int(sign == -1)


def quartic3(p):
    assert prime(p) and p % 12 == 1
    z = pow(3, (p - 1) // 4, p)
    assert z in (1, p - 1)
    return 1 if z == 1 else -1


def matrix(primes):
    selected, rows, rhs = [], [], []
    for i, p in enumerate(primes):
        if p % 12 != 1:
            continue
        off = sum(bit(legendre(q, p)) << j
                  for j, q in enumerate(primes) if j != i)
        diagonal = (off.bit_count() + bit(quartic3(p))) % 2
        selected.append(p)
        rows.append(off | (diagonal << i))
        rhs.append(bit(legendre(2, p)))
    return selected, rows, rhs


def elimination(rows, rhs, n):
    """Return consistency, rank, and a left-null contradiction witness."""
    augmented = [[r, b, 1 << i] for i, (r, b) in enumerate(zip(rows, rhs))]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(augmented))
                      if (augmented[i][0] >> col) & 1), None)
        if pivot is None:
            continue
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        for i in range(len(augmented)):
            if i != rank and (augmented[i][0] >> col) & 1:
                augmented[i] = [x ^ y for x, y in zip(augmented[i], augmented[rank])]
        rank += 1
    for row, b, witness in augmented:
        if row == 0 and b == 1:
            return False, rank, witness
    return True, rank, None


def matrix_accepts(rows, rhs, assignment):
    return all((r & assignment).bit_count() % 2 == b
               for r, b in zip(rows, rhs))


def partition_conditions(primes, assignment):
    A = math.prod(p for j, p in enumerate(primes) if assignment >> j & 1)
    B = math.prod(primes) // A
    return all(legendre(B, p) == legendre(2, p) * quartic3(p)
               if assignment >> i & 1 else legendre(A, p) == legendre(2, p)
               for i, p in enumerate(primes) if p % 12 == 1)


def verify_dual(rows, rhs, witness):
    rsum = bsum = 0
    for i, (r, b) in enumerate(zip(rows, rhs)):
        if witness >> i & 1:
            rsum ^= r
            bsum ^= b
    assert rsum == 0 and bsum == 1


def report(primes):
    R = math.prod(primes)
    assert len(set(primes)) == len(primes) and all(prime(p) for p in primes)
    assert R % 8 == 5 and R % 3 != 0
    selected, rows, rhs = matrix(primes)
    consistent, rank, dual = elimination(rows, rhs, len(primes))
    if dual is not None:
        verify_dual(rows, rhs, dual)
    return {
        "R": R,
        "squarefree_kernel": 6 * R,
        "column_primes": list(primes),
        "row_primes": selected,
        "matrix": [[(r >> j) & 1 for j in range(len(primes))] for r in rows],
        "rhs": rhs,
        "rank": rank,
        "matrix_consistent": consistent,
        "dual_certificate": None if dual is None else
            [(dual >> i) & 1 for i in range(len(rows))],
        "all_odd_multipliers_excluded": not consistent,
        "consistency_proves_tiling": False,
    }


def run_checks():
    root_cases = 0
    for p in range(13, 5000, 12):
        if not prime(p):
            continue
        roots = [q for q in range(p) if (q*q + 6*q - 3) % p == 0]
        assert len(roots) == 2
        assert all(legendre(q, p) == legendre(2, p) * quartic3(p) for q in roots)
        root_cases += 1

    universe = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                43, 61, 73, 97, 109, 157, 181, 313, 521)
    products = partitions = exclusions = direct_local_checks = 0
    for count in range(1, 5):
        for primes in itertools.combinations(universe, count):
            R = math.prod(primes)
            if R % 8 != 5:
                continue
            selected, rows, rhs = matrix(primes)
            consistent, rank, dual = elimination(rows, rhs, count)
            accepted = []
            for assignment in range(1 << count):
                yes = matrix_accepts(rows, rhs, assignment)
                assert yes == partition_conditions(primes, assignment)
                accepted.append(yes)
                partitions += 1
                # A separate direct modular cover check on small examples.
                if count <= 2:
                    A = math.prod(p for j, p in enumerate(primes) if assignment >> j & 1)
                    B = R // A
                    for p in selected:
                        for eps in (1, 3):
                            e = 2 * eps * A
                            if A % p == 0:
                                delta, kappa = e // p, 2 * R // p
                                assert (12 * R * R) % (e * p) == 0
                                local = any((delta*u**4 + 6*kappa*u*u
                                             - (12*R*R)//(e*p)) % p == 0
                                            for u in range(1, p))
                                expected = legendre(B, p) == legendre(2, p)*quartic3(p)
                            else:
                                leading = -(12 * (R//p)**2) * pow(e, -1, p)
                                assert legendre(e, p) == legendre(leading, p)
                                local = legendre(e, p) == 1
                                expected = legendre(A, p) == legendre(2, p)
                            assert local == expected
                            direct_local_checks += 1
            assert consistent == any(accepted)
            if dual is not None:
                verify_dual(rows, rhs, dual)
                exclusions += 1
            products += 1

    examples = [report(ps) for ps in (
        (13,), (13, 313), (13, 521), (13, 937),
        (13, 61, 157), (13, 37, 181), (13, 37, 61, 109, 181),
        (37,),  # Consistent control: not a positive tiling certificate.
    )]
    assert all(r["all_odd_multipliers_excluded"] for r in examples[:-1])
    assert examples[-1]["matrix_consistent"]
    five = examples[-2]
    assert five["squarefree_kernel"] == 3473211534
    assert all(any(row) for row in five["matrix"])
    fixed_z = [0, 1, 1, 1, 0]
    assert all(sum(a*b for a, b in zip(row, fixed_z)) % 2 == 0
               for row in five["matrix"])
    assert sum(fixed_z) % 2 == 1

    progression_primes = [q for q in range(105, 10000, 104) if prime(q)]
    assert progression_primes[:3] == [313, 521, 937]
    for q in progression_primes:
        assert report((13, q))["all_odd_multipliers_excluded"]
    mixed_primes = [q for q in range(157, 10000, 312) if prime(q)]
    assert quartic3(61) == -1
    for q in mixed_primes:
        assert report((13, 61, q))["all_odd_multipliers_excluded"]

    return {
        "status": "PASS",
        "selected_prime_root_checks_below_5000": root_cases,
        "mixed_prime_products_checked": products,
        "partitions_checked": partitions,
        "inconsistent_matrices_with_dual_certificates": exclusions,
        "direct_modular_cover_checks": direct_local_checks,
        "q_1_mod_104_below_10000": progression_primes,
        "q_157_mod_312_below_10000": mixed_primes,
        "examples": examples,
        "matrix_consistency_proves_global_solubility": False,
        "bounded_checks_prove_universal_theorem": False,
        "full_Erdos634_solved": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--R", type=int, help="One odd squarefree R=5 mod8, 3∤R")
    args = parser.parse_args()
    if args.R is None:
        result = run_checks()
    else:
        remaining, factors = args.R, []
        for p in range(2, math.isqrt(remaining) + 1):
            if remaining % p == 0:
                factors.append(p)
                remaining //= p
                assert remaining % p != 0, "R must be squarefree"
        if remaining > 1:
            factors.append(remaining)
        result = report(tuple(factors))
    print(json.dumps(result, indent=2))
