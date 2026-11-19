"""Catalog T(hq) relative to the sum-of-two-squares baseline. Python 3.9+."""
import json
from collections import defaultdict
from math import gcd, isqrt


def square(n):
    return n >= 0 and isqrt(n) ** 2 == n


def primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[:2] = b'\0\0'
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            count = 1 + (n - p*p) // p
            sieve[p*p::p] = bytes(count)
    return [i for i in range(2, n + 1) if sieve[i]]


def norm_rows(limit):
    """Register all nine t=1 product coefficients with their parameters."""
    rows = defaultdict(set)

    def add(value, branch, a, b, c=0):
        if value <= limit:
            rows[value].add((branch, a, b, c))

    for v in range(2, isqrt(limit) + 1):
        # b >= 2v-1 and both bQ and QP exceed v^3.
        if v**3 >= limit:
            break
        for u in range(1, v):
            if gcd(u, v) > 1:
                continue
            b = v*v - u*u
            q, p = b + v*v, b + 2*v*v
            add(b*q, 'alpha', u, v)
            add(q*p, 'Paliy', u, v)
    for low in range(1, isqrt(limit) + 1):
        for high in range(low, limit // low + 1):
            if gcd(low, high) > 1:
                continue
            ab = low * high
            z = low**2 + high**2
            if low != high and square(z-ab):
                add(ab, 'equilateral60', low, high, isqrt(z-ab))
            if not square(z+ab):
                continue
            c = isqrt(z+ab)
            add(ab, 'equilateral120', low, high, c)
            for a, b in ((low, high), (high, low)):
                add(b*(a+b), 'F1', a, b, c)
                add(b*(a+2*b), 'iso120', a, b, c)
                add((a+2*b)*(2*a+b), 'F2', a, b, c)
                add(3*(a+b)*(a+2*b), 'F3', a, b, c)
                add((2*a+b)*(a+b), 'F4', a, b, c)
    return rows


def recover_product_rows(d):
    """An independent inversion of all nine product rows using divisors of d."""
    def ordered_divisors(n):
        for x in range(1, isqrt(n) + 1):
            if n % x:
                continue
            yield x, n//x
            if x*x != n:
                yield n//x, x

    recovered = set()

    def add_group1(name, u2, v2):
        if 0 < u2 < v2 and square(u2) and square(v2):
            u, v = isqrt(u2), isqrt(v2)
            if gcd(u, v) == 1:
                recovered.add((name, u, v, 0))

    def add_norm(name, a, b, sign=1):
        if min(a, b) > 0 and gcd(a, b) == 1:
            c2 = a*a + sign*a*b + b*b
            if square(c2):
                recovered.add((name, a, b, isqrt(c2)))

    for x, y in ordered_divisors(d):
        if x <= y:
            add_norm('equilateral120', x, y)
            if x < y:
                add_norm('equilateral60', x, y, -1)
        add_group1('alpha', y-2*x, y-x)
        add_group1('Paliy', 2*y-3*x, y-x)
        add_norm('F1', y-x, x)
        add_norm('iso120', y-2*x, x)
        add_norm('F4', y-x, 2*x-y)
        if (x+y) % 3 == 0:
            add_norm('F2', (2*y-x)//3, (2*x-y)//3)
    if d % 3 == 0:
        for x, y in ordered_divisors(d//3):
            add_norm('F3', 2*x-y, y-x)
    return recovered


def exceptional_families(n, rows):
    candidates = set()
    for t in range(1, isqrt(n) + 1):
        if n % (t*t):
            continue
        d = n // (t*t)
        candidates.update((name, a, b, c, t) for name, a, b, c in rows.get(d, ()))
        if t == 1:
            continue
        for v in range(2, isqrt(d) + 1):
            for u in range(1, v):
                if gcd(u, v) != 1:
                    continue
                for name, D in [('W', 2), ('beta', 3)]:
                    if D*v*v-u*u == d:
                        candidates.add((name, u, v, 0, t))
        for small in range(1, isqrt(d) + 1):
            if d % small:
                continue
            big = d // small
            if (big-small) % 2:
                continue
            u, v = (big-small)//2, (big+small)//2
            if not (u > 0 and gcd(u, v) == 1):
                continue
            if u*u <= t*d:
                candidates.add(('double', u, v, 0, t))
            if u*v <= t*d:
                candidates.add(('theta', u, v, 0, t))
    return sorted(candidates)


def in_semigroup(value, a, b, c):
    if value < 0:
        return False
    return any((value-x*a-y*b) % c == 0 for x in range(value//a + 1)
               for y in range((value-x*a)//b + 1))


def constructive(row):
    name, a, b, c, t = row
    if name == 'Paliy' or (name in ('W', 'beta') and t >= b):
        return True
    if name == 'F4' and a < b:
        return True
    if name not in ('F2', 'F3', 'F4'):
        return False
    if name in ('F2', 'F3') and a < b:
        a, b = b, a
    if a <= b:
        return False
    return any(k*c >= t*(a-b) and in_semigroup(t*b*c - a*a*k, a, b, c)
               for k in range(1, t*b*c//(a*a) + 1))


# Exact list extracted from Bonfioli's Spectrum200 theorem, restricted to values
# h*q queried by this script. The independent n=231 result is linked in the note.
POSITIVE_TO_200 = {12,18,20,28,44,45,50,52,63,68,75,84,90,98,99,117,126,
                   130,147,150,170,175}
OTHER_NEGATIVES = {231}
OTHER_POSITIVES = {345, 506}


def is_sum_of_squares(n):
    return any(square(n-x*x) for x in range(isqrt(n)+1))


def evaluate(n, rows):
    if is_sum_of_squares(n):
        return 'sum of two squares', []
    if (n % 3 == 0 and square(n//3)) or (n % 6 == 0 and square(n//6)):
        return 'yes', ['classical 3 or 6 times a square']
    if n <= 200:
        return ('yes' if n in POSITIVE_TO_200 else 'no'), ['Spectrum200']
    if n in OTHER_NEGATIVES:
        return 'no', ['231 positioned-current certificate']
    if n in OTHER_POSITIVES:
        return 'yes', ['explicit Paliy/Bonfioli layout']
    shapes = exceptional_families(n, rows)
    if any(constructive(s) for s in shapes):
        return 'yes', shapes
    return ('unresolved' if shapes else 'no'), shapes


def main():
    bound = 50
    small_primes = primes_up_to(bound)
    hs = [h for h in range(4,bound+1) if h not in small_primes and
          all(h%(p*p) for p in small_primes if p*p <= h)]
    primes = primes_up_to((3*bound**2+6*bound-1)//4)
    scannable = {h: (3*h*h+6*h-1)//4 for h in hs}
    rows = norm_rows(max(h*scannable[h] for h in hs))
    result = {}
    for h in hs:
        record = {'cutoff':scannable[h], 'positive_exceptions':[], 'positive_evidence':{},
                  'unresolved':{}, 'prime_divisors_of_h':{}}
        for q in primes:
            if q > scannable[h]:
                break
            status, evidence = evaluate(h*q, rows)
            if h%q == 0:
                record['prime_divisors_of_h'][q] = status
            if status == 'yes':
                record['positive_exceptions'].append(q)
                record['positive_evidence'][q] = evidence
            if status == 'unresolved':
                record['unresolved'][q] = evidence
        result[h] = record
    coefficients = {h*q//(t*t) for h in hs for q in primes if q <= scannable[h]
                    for t in range(1, isqrt(h*q)+1) if h*q % (t*t) == 0}
    assert len(coefficients) == 1802
    assert all(recover_product_rows(d) == rows.get(d, set()) for d in coefficients)
    return result


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError("Run with assertions enabled.")
    result = main()
    assert [h for h in result if h in (6,10,14,22) and not result[h]['unresolved']] == [6,10,14,22]
    assert result[6]['positive_exceptions']==[2]
    assert result[14]['positive_exceptions']==[2,23]
    assert result[22]['positive_exceptions']==[2,23]
    assert set(result[21]['unresolved'])=={37}
    print(json.dumps(result, indent=2))
