#!/usr/bin/env python3
"""Exact finite part of the multiplier-one 1 < a/b <= 7/5 theorem.

Default: read and verify the retained integer witnesses. --write regenerates
them from reduced rational parameters before the independent side scan.
No floating-point arithmetic or tiling-generation code is used.
"""

import argparse
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
PATH = HERE / "balanced-7-5-small-witnesses.json"


def parameter_triples():
    result = set()
    # For b < 4900, b > n^2 gives n <= 69; m/n < 7/2 gives m < 245.
    for n in range(1, 70):
        for m in range(n + 1, 245):
            if gcd(m, n) != 1:
                continue
            aa, bb, cc = m*m-n*n, n*(2*m+n), m*m+m*n+n*n
            divisor = gcd(gcd(aa, bb), cc)
            assert divisor in (1, 3)
            a, b, c = aa//divisor, bb//divisor, cc//divisor
            if b < 4900 and b < a and 5*a <= 7*b:
                result.add((a, b, c))
    return result


def side_triples():
    # Independent exhaustive enumeration in (a,b), without the parametrization.
    result = set()
    for b in range(1, 4900):
        for a in range(b + 1, (7*b)//5 + 1):
            if gcd(a, b) != 1:
                continue
            norm = a*a + a*b + b*b
            c = isqrt(norm)
            if c*c == norm:
                result.add((a, b, c))
    return result


def witness(a, b, c):
    remainder = b*c-a*a
    inverse = pow(b, -1, a)
    for s in range(remainder//c + 1):
        rest = remainder-s*c
        B = (rest*inverse) % a
        if B*b <= rest:
            return [(rest-B*b)//a, B, s]
    raise AssertionError(f"No ternary witness for {(a,b,c)}")


def main():
    if not __debug__:
        raise RuntimeError("Proof checks require assertions; do not run Python with -O.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    parameters = parameter_triples()
    if args.write:
        rows = [dict(tile=list(t), coefficients=witness(*t))
                for t in sorted(parameters)]
        payload = {
            "scope": "All primitive plus-norm triples with 1<a/b<=7/5 and b<4900",
            "identity": "bc-a^2 = A*a+B*b+s*c; coefficients=[A,B,s]",
            "count": len(rows),
            "witnesses": rows,
        }
        PATH.write_text(json.dumps(payload, indent=2) + "\n")
    payload = json.loads(PATH.read_text())
    rows = payload["witnesses"]
    retained = set()
    for row in rows:
        a, b, c = row["tile"]
        A, B, s = row["coefficients"]
        assert all(type(x) is int and x >= 0 for x in (A, B, s))
        assert 0 < b < a and 5*a <= 7*b and b < 4900
        assert gcd(a, b) == 1 and c*c == a*a+a*b+b*b
        assert b*c-a*a == A*a+B*b+s*c
        assert (a, b, c) not in retained
        retained.add((a, b, c))
    sides = side_triples()
    assert retained == parameters == sides
    assert payload["count"] == len(rows) == len(retained) == 240
    print(json.dumps({
        "status": "PASS", "primitive_triples": len(retained),
        "full_Erdos634_solved": False,
        "all_integer_witnesses_valid": True,
        "independent_parameter_and_side_enumerations_agree": True,
        "scope": "Finite part b<4900; combine with TERNARY_SEMIGROUP_TAIL.md",
    }, indent=2))


if __name__ == "__main__":
    main()
