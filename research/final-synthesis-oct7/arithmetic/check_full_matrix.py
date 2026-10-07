#!/usr/bin/env python3
"""Check the augmented system against direct local quartic calculations."""
import itertools
import json
import math
from check_matrix import prime, legendre, bit, quartic3, matrix, elimination, matrix_accepts, verify_dual


def full_matrix(primes):
    n = len(primes)
    selected, rows, rhs = matrix(primes)
    labels = [f"split p={p}" for p in selected]
    for i, p in enumerate(primes):
        if p % 12 in (5, 7):
            rows.append(1 << i)
            rhs.append(0)
            labels.append(f"inert p={p}: a=0")
            if p % 12 == 7:
                rows.append((1 << n) | sum(bit(legendre(q, p)) << j
                                          for j, q in enumerate(primes) if j != i))
                rhs.append(bit(legendre(2, p)))
                labels.append(f"inert p={p}: unit character")
    rows.append((1 << n) | sum(1 << i for i, p in enumerate(primes) if p % 4 == 3))
    rhs.append(1)
    labels.append("2-adic/3-adic parity")
    return rows, rhs, labels


def direct_at_odd_prime(A, B, eps, p):
    R, e = A * B, 2 * eps * A
    if A % p == 0:
        # W=0 lifts iff the divided quartic has a nonzero simple root.
        delta, kappa = e // p, 2 * R // p
        coeff = (12 * R * R) // (e * p)
        roots = [u for u in range(1, p)
                 if (delta*u**4 + 6*kappa*u*u - coeff) % p == 0]
        assert all((4*delta*u**3 + 12*kappa*u) % p != 0 for u in roots)
        return bool(roots)
    # The two possible normalized valuations of u give these characters.
    return legendre(e, p) == 1 or legendre(-12 * pow(e, -1, p), p) == 1


def direct_at_three(A, eps):
    return (eps == 1 and A % 3 == 2) or (eps == 3 and A % 3 == 1)


def direct_at_two(A, B, eps):
    def F(u):
        return 2 * A * (eps*u**4 + 6*B*u*u - (3//eps)*B*B)
    necessary = eps * A % 4 == 3
    if not necessary:
        assert F(1) % 16 == 8
        return False
    assert F(1) % 16 == 0 and F(1)//16 % 4 == 1
    assert (F(3) - F(1))//16 % 8 == 4
    return any(F(u)//16 % 8 == 1 for u in (1, 3))


def certificate(primes):
    rows, rhs, labels = full_matrix(primes)
    consistent, rank, witness = elimination(rows, rhs, len(primes) + 1)
    if witness is not None:
        verify_dual(rows, rhs, witness)
    return {
        "R": math.prod(primes), "kernel": 6*math.prod(primes),
        "primes": list(primes), "columns": [f"a_{p}" for p in primes] + ["f"],
        "rows": [[(r >> i) & 1 for i in range(len(primes)+1)] for r in rows],
        "rhs": rhs, "row_labels": labels, "rank": rank,
        "consistent": consistent,
        "dual_certificate": None if witness is None else
             [(witness >> j) & 1 for j in range(len(rows))],
        "all_odd_multipliers_excluded": not consistent,
        "consistency_proves_tiling": False,
    }


def main():
    universe = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 61, 73)
    products = covers = direct_checks = excluded = 0
    strictly_stronger = []
    for size in range(1, 5):
        for ps in itertools.combinations(universe, size):
            R = math.prod(ps)
            if R % 8 != 5:
                continue
            rows, rhs, labels = full_matrix(ps)
            solved, rank, witness = elimination(rows, rhs, size + 1)
            found = False
            for assignment in range(1 << (size + 1)):
                A = math.prod(p for j, p in enumerate(ps) if assignment >> j & 1)
                B = R // A
                eps = 3 if assignment >> size & 1 else 1
                local2 = direct_at_two(A, B, eps)
                local3 = direct_at_three(A, eps)
                locals_odd = [direct_at_odd_prime(A, B, eps, p) for p in ps]
                direct_checks += len(ps)
                actual = local2 and local3 and all(locals_odd)
                encoded = matrix_accepts(rows, rhs, assignment)
                assert actual == encoded, (ps, A, B, eps, actual, encoded)
                found |= encoded
                covers += 1
            assert solved == found
            if witness is not None:
                verify_dual(rows, rhs, witness)
                excluded += 1
                _, oldrows, oldrhs = matrix(ps)
                if elimination(oldrows, oldrhs, size)[0]:
                    strictly_stronger.append((6*R, ps))
            products += 1
    two_adic = 0
    for A in range(1, 128, 2):
        for B in range(1, 128, 2):
            if A*B % 8 == 5:
                for eps in (1, 3):
                    assert direct_at_two(A, B, eps) == (eps*A % 4 == 3)
                    two_adic += 1
    examples = [certificate(ps) for ps in (
        (13,), (13, 17), (13, 313), (13, 521), (7, 19),
        (13, 61, 157), (13, 37, 61, 109, 181), (37,),
    )]
    assert all(e["all_odd_multipliers_excluded"] for e in examples[:-1])
    assert examples[-1]["consistent"]
    print(json.dumps({
        "status": "PASS", "mixed_products": products, "covers": covers,
        "direct_odd_prime_cover_checks": direct_checks,
        "two_adic_residue_checks": two_adic,
        "excluded_products": excluded,
        "strictly_more_exclusions_than_selected_prime_matrix": len(strictly_stronger),
        "first_strictly_stronger_kernels": sorted(strictly_stronger)[:15],
        "examples": examples,
        "locally_soluble_cover_implies_tiling": False,
        "full_Erdos634_solved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
