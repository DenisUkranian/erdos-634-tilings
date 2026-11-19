"""Three-way arithmetic/constructive decision for Erdős 634. Python 3.10+."""
from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from functools import lru_cache
from itertools import product
import json
from math import gcd, isqrt, prod


def factor(n):
    result = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            n //= p
            result[p] = result.get(p, 0) + 1
        p = 3 if p == 2 else p + 2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def divisors(factors):
    powers = [[p ** e for e in range(v + 1)] for p, v in factors.items()]
    return sorted(prod(values) for values in product(*powers))


def ceil_div(n, d):
    return (n + d - 1) // d


@dataclass(frozen=True)
class Witness:
    row: str
    parameters: tuple
    threshold: int


@lru_cache(maxsize=4096)
def witnesses(D):
    facts = factor(D)
    result = []
    for f in divisors(facts):
        g = D // f
        if g > f:
            v2 = g - f
            for row, u2 in [('alpha', v2 - f), ('Paliy', 2 * v2 - f)]:
                if u2 <= 0:
                    continue
                u, v = isqrt(u2), isqrt(v2)
                if u*u != u2 or v*v != v2 or not 0 < u < v or gcd(u, v) != 1:
                    continue
                b = v2 - u2
                h = ceil_div(u, v - u)
                j = ceil_div(h*u, b)
                M = max(ceil_div(v*h, u), h + ceil_div(u*h, v))
                t = 1 if row == 'Paliy' else j + ceil_div(M, v)
                result.append(Witness(row, (u, v), t))

        norm_pairs = [('E60', f, g, -1), ('E120', f, g, 1),
                      ('F1', g - f, f, 1), ('iso120', g - 2*f, f, 1),
                      ('F4', g - f, 2*f - g, 1)]
        if (2*g - f) % 3 == 0 and (2*f - g) % 3 == 0:
            norm_pairs.append(('F2', (2*g - f)//3, (2*f - g)//3, 1))
        if g % 3 == 0:
            n = g // 3
            norm_pairs.append(('F3', 2*f - n, n - f, 1))
        for row, a, b, sign in norm_pairs:
            if min(a, b) <= 0 or gcd(a, b) != 1:
                continue
            norm = a*a + sign*a*b + b*b
            c = isqrt(norm)
            if c*c != norm:
                continue
            ratio = max(a, b) // min(a, b)
            t = 3*(ratio + (1 if row == 'E60' else 2))
            if row in ('F2', 'F3'):
                t = ceil_div(t, 2)
            result.append(Witness(row, (a, b, c), t))
    return tuple(result)


def classify(N):
    if N < 1:
        raise ValueError('N must be a positive integer')
    facts = factor(N)
    d = prod(p for p, e in facts.items() if e % 2)
    mfacts = {p: e//2 for p, e in facts.items() if e >= 2}
    m = prod(p**e for p, e in mfacts.items())
    odds = [p for p, e in facts.items() if e % 2 and p > 2]
    def answer(status, reason, **kw):
        return dict(N=N, d=d, m=m, status=status, reason=reason, **kw)
    if d in (1, 2, 3, 6) or all(p % 4 == 1 for p in odds):
        return answer('YES', 'classical')
    if facts.get(2) == 1 and all(p == 2 or p % 24 in (5, 19) for p in facts):
        return answer('NO', 'simultaneously inert prime sector')
    W = all(p % 8 in (1, 7) for p in odds)
    beta = (all(p % 12 in (1, 11) for p in odds if p > 3)
            and (d % 3 == 2 if d % 3 else (d//3) % 3 == 1))
    if (W or beta) and m >= 2*d:
        return answer('YES', 'quadratic norm saturation', threshold=2*d)
    if d % 2:
        theta = d + d*d//8
    else:
        theta = 2*(d+1)*ceil_div(d-1, 8) + 2*d
    if (d % 2 or m % 2 == 0) and m >= theta:
        return answer('YES', 'theta tail', threshold=theta)
    found = []
    for s in divisors(mfacts):
        for w in witnesses(d*s*s):
            entry = dict(s=s, residual=m//s, **asdict(w))
            if m//s >= w.threshold:
                return answer('YES', 'table construction', witness=entry)
            found.append(entry)
    if not (d % 2 or m % 2 == 0 or W or beta or found):
        return answer('NO', 'exhausted all primitive coefficients')
    return answer('UNRESOLVED', 'below available construction thresholds', small_witnesses=found)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('N', type=int, nargs='+')
    args = parser.parse_args()
    print(json.dumps([classify(N) for N in args.N], indent=2))
