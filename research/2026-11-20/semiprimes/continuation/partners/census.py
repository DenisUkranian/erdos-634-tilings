"""Classify F2 mixed-residue partners incident with a prime endpoint <= 1,000,000."""
import argparse
import csv
import hashlib
import io
from collections import Counter
from math import gcd, isqrt
from partners import integer_partner, primes_through


def threshold_row(p, q):
    """p < q, both odd primes; recover the ordered shape and staircase threshold."""
    a, b = (2 * q - p) // 3, (2 * p - q) // 3
    c = isqrt(a * a + a * b + b * b)
    divisor = gcd(a + c, b)
    u, v = (a + c) // divisor, b // divisor
    g = gcd(3, u - v)
    assert a * g == u * u - v * v and b * g == v * (2 * u + v)
    assert c * c == a * a + a * b + b * b
    assert (a + 2 * b, 2 * a + b) == (p, q)
    bound = 4 * v * (v - 1) if g == 3 and v % 3 == 2 else 4 * v * v
    return (p * q, p, q, a, b, c, u, v, int(u <= bound))


def by_endpoints(bound):
    primes = primes_through(2 * bound)
    prime_set = set(primes)
    categories = Counter()
    rows = set()
    for p in primes:
        if p > bound:
            break
        q = integer_partner(p)
        if q is None:
            categories['inert prime'] += 1
        elif q % 2 == 0:
            categories['even partner'] += 1
        elif q not in prime_set:
            categories['odd composite partner'] += 1
        else:
            assert integer_partner(q) == p
            row = threshold_row(min(p, q), max(p, q))
            categories['staircase partner' if row[-1] else 'residual partner'] += 1
            rows.add(row)
    return categories, sorted(rows)


def by_parameters(bound):
    """Separate verification by exhaustive coprime (u,v) enumeration.

    Ordered parameters give p=a+2b=(u^2+4uv+v^2)/g>u^2/3 and g<=3.
    """
    primes = set(primes_through(2 * bound))
    rows = []
    for u in range(2, isqrt(3 * bound) + 1, 2):
        for v in range(1, u // 2 + 1, 2):
            if gcd(u, v) != 1:
                continue
            g = gcd(3, u - v)
            a = (u * u - v * v) // g
            b = v * (2 * u + v) // g
            p, q = a + 2 * b, 2 * a + b
            if not (a > b and p <= bound and p in primes and q in primes):
                continue
            threshold = 4 * v * v
            if g == 3 and v % 3 == 2:
                threshold -= 4 * v
            c = (u * u + u * v + v * v) // g
            rows.append((p * q, p, q, a, b, c, u, v, int(u <= threshold)))
    return sorted(rows)


def csv_text(rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator='\n')
    writer.writerow(('N', 'p', 'q', 'a', 'b', 'c', 'u', 'v', 'unit_staircase'))
    writer.writerows(rows)
    return buf.getvalue()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bound', type=int, default=1000000)
    parser.add_argument('--write-residuals', help='Optional output CSV')
    args = parser.parse_args()
    counts, rows = by_endpoints(args.bound)
    assert rows == by_parameters(args.bound)
    print('endpoint bound', args.bound)
    print('incident primes >3', sum(counts.values()))
    for category in sorted(counts):
        print(category, counts[category])
    print('distinct prime pairs', len(rows))
    residuals = [r for r in rows if not r[-1]]
    print('distinct staircase pairs', len(rows) - len(residuals))
    print('distinct residual pairs', len(residuals))
    print('residual pairs with both endpoints <= bound', sum(r[2] <= args.bound for r in residuals))
    print('largest residual product', max((r[0] for r in residuals), default=None))
    print('all pairs CSV SHA-256', hashlib.sha256(csv_text(rows).encode('ascii')).hexdigest())
    output = csv_text(residuals)
    print('residual CSV SHA-256', hashlib.sha256(output.encode('ascii')).hexdigest())
    if args.write_residuals:
        with open(args.write_residuals, 'w', encoding='ascii', newline='') as handle:
            handle.write(output)
