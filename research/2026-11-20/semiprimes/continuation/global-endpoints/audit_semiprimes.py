"""Independent arithmetic audit of the semiprime reduction, not a tiling solver.

NO conclusions use the recorded geometric overlist and small-factor rules.
MANUSCRIPT_DEPENDENT keeps the distant BQ/I120 cases separate.  Some retained
cases, such as 161, have independent individual exclusions; this conservative
program deliberately does not incorporate those certificates.
"""
from collections import Counter
from math import gcd, isqrt
import argparse
import json


def primes_through(bound):
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[:2] = b"\x00\x00"
    for n in range(2, isqrt(bound) + 1):
        if sieve[n]:
            sieve[n*n:bound+1:n] = b"\x00" * ((bound - n*n)//n + 1)
    return [n for n in range(2, bound + 1) if sieve[n]]


def square(n):
    return n >= 0 and isqrt(n)**2 == n


def classify(p, q):
    assert p <= q
    if p == q:
        return "YES_square", None
    if p == 2:
        return ("YES_classical" if q == 3 or q % 4 == 1
                else "NO_small_factor"), None
    if p == 3:
        return "NO_small_factor", None
    if p % 4 == q % 4 == 1:
        return "YES_classical", None
    if p % 4 == q % 4 == 3:
        if 3*p < 2*q < 4*p and square(q-p) and square(2*q-3*p):
            return "YES_Paliy", None
        if q > 2*p and 4*q in (p*p+6*p+1, 3*p*p+6*p-1, p*p+6*p-3):
            return "MANUSCRIPT_DEPENDENT", (p*q, p, q)
        return "NO_overlist", None
    discriminant = p*p - p*q + q*q
    if q >= 2*p or (p+q) % 3 or discriminant % 3 or not square(discriminant//3):
        return "NO_overlist", None
    a, b, c = (2*q-p)//3, (2*p-q)//3, isqrt(discriminant//3)
    divisor = gcd(a+c, b)
    u, v = (a+c)//divisor, b//divisor
    g = gcd(3, u-v)
    assert gcd(a,b) == 1 and a > b > 0
    assert (a,b,c) == ((u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g)
    threshold = 4*v*(v-1) if g == 3 and v % 3 == 2 else 4*v*v
    if u <= threshold:
        return "YES_staircase", None
    return "OPEN_F2", dict(N=p*q, p=p, q=q, a=a, b=b, c=c, u=u, v=v, g=g)


def run(bound):
    primes = primes_through(bound)
    counts, residual, distant = Counter(), [], []
    for i, p in enumerate(primes):
        if p*p > bound:
            break
        for q in primes[i:]:
            if p*q > bound:
                break
            status, record = classify(p, q)
            counts[status] += 1
            if status == "OPEN_F2":
                residual.append(record)
            elif status == "MANUSCRIPT_DEPENDENT":
                distant.append(record)
    return dict(bound=bound, total_semiprimes=sum(counts.values()),
                counts=dict(counts), residual_F2=sorted(residual, key=lambda r:r["N"]),
                distant_manuscript_dependent=sorted(distant))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", type=int, default=1_000_000)
    parser.add_argument("--output")
    args = parser.parse_args()
    report = run(args.bound)
    if args.bound == 1_000_000:
        assert report["total_semiprimes"] == 210_035
        assert [r["N"] for r in report["residual_F2"]] == [3431,5063,19367,60023,64367,271151,641591]
        assert sum(v for k,v in report["counts"].items() if k.startswith("YES")) == 55_359
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        with open(args.output, "w") as f:
            f.write(text)
    print(text, end="")
