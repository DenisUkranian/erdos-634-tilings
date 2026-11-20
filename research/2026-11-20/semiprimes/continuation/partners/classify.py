"""Certified arithmetic cases for a product of two primes in Erdos problem 634."""
import argparse
from math import gcd, isqrt


def prime(n):
    if n < 2 or n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, isqrt(n) + 1, 2))


def square(n):
    return n >= 0 and isqrt(n) ** 2 == n


def classify(p, q, *, use_bank_exclusions=True):
    if not prime(p) or not prime(q):
        raise ValueError("Both factors must be prime.")
    p, q = sorted((p, q))
    if p == q:
        return "YES", "square grid"
    if p == 2:
        if q == 3 or q % 4 == 1:
            return "YES", "classical dissection"
        return "NO", "twice-prime rule"
    if p == 3:
        return "NO", "three-times-prime rule"
    if p % 4 == q % 4 == 1:
        return "YES", "sum of two squares"
    if p % 4 == q % 4 == 3:
        if 3 * p < 2 * q < 4 * p and square(q - p) and square(2 * q - 3 * p):
            return "YES", "Paliy construction"
        if q < 2 * p:
            return "NO", "prime-pair reduction"
        candidates = (p*p + 6*p + 1, 3*p*p + 6*p - 1, p*p + 6*p - 3)
        if 4*q not in candidates:
            return "NO", "prime-pair reduction"
        if use_bank_exclusions:
            return "NO", "unit BQ or I120 manuscript exclusion"
        return "UNDECIDED BY SELECTED INPUTS", "distant BQ or I120 candidate"
    if q >= 2 * p or (p + q) % 3:
        return "NO", "mixed-residue range or congruence"
    a, b = (2*q - p)//3, (2*p - q)//3
    norm = a*a + a*b + b*b
    if not square(norm):
        return "NO", "F2 norm is not a square"
    c = isqrt(norm)
    d = gcd(a+c, b)
    u, v = (a+c)//d, b//d
    threshold = 4*v*(v-1) if (u-v) % 3 == 0 and v % 3 == 2 else 4*v*v
    if u <= threshold:
        return "YES", "unit F2 staircase"
    return "OPEN", f"unit F2 board with sides {(a*p,b*q,c*c)} and tile {(a,b,c)}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("p", type=int)
    parser.add_argument("q", type=int)
    parser.add_argument("--older-overlist", action="store_true",
                        help="omit the two later moving-bank manuscript exclusions")
    args = parser.parse_args()
    print(*classify(args.p, args.q, use_bank_exclusions=not args.older_overlist), sep="  ")
