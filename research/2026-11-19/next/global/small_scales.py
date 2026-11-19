"""Find finite interval covers that work for every negative norm at small scale."""

from fractions import Fraction
from math import isqrt
import json


def cover(d, m, h, reps):
    lo, hi = Fraction(1, m), 1 - Fraction(1, m - 1)
    intervals = []
    for a, b in reps:
        for y0, y1 in ((lo, hi), (-hi, -lo)):
            x0 = (a*y0-d*b) / (a-b*y0)
            x1 = (a*y1-d*b) / (a-b*y1)
            if x1 >= 0 and x0 <= 1:
                intervals.append((max(0, x0), min(1, x1), a, b))
    intervals.sort()
    chosen, right, i = [], 0, 0
    while right < 1:
        best = None
        while i < len(intervals) and intervals[i][0] <= right:
            if best is None or intervals[i][1] > best[1]:
                best = intervals[i]
            i += 1
        if best is None or best[1] <= right:
            return None
        left, right, a, b = best
        assert a*a-d*b*b == h
        chosen.append(dict(a=a, b=b, left=str(left), right=str(right)))
    return chosen


def first_certificates(d, bound=200000):
    # Every useful conjugate or associate has |log(alpha/sqrt(h))| <= log(epsilon).
    # Thus a <= cosh(log(epsilon))*sqrt(h), where the constant is 3 or 2.
    c = 3 if d == 2 else 2
    candidates = {}
    for a in range(1, isqrt(c*c*bound) + 1):
        for b in range(isqrt((a*a-1)//d) + 1):
            h = a*a - d*b*b
            if h > bound or a*a > c*c*h:
                continue
            reps = candidates.setdefault(h, [])
            reps.append((a,b))
            if b:
                reps.append((a,-b))
    squarefree = bytearray(b"\x01") * (bound+1)
    for p in range(2, isqrt(bound)+1):
        squarefree[p*p::p*p] = bytes(bound // (p*p))
    answer = []
    for m in (3, 4, 5, 6):
        first = True
        for h, reps in sorted(candidates.items()):
            if not first and not squarefree[h]:
                continue
            result = cover(d, m, h, reps)
            if result is not None:
                answer.append(dict(D=d, M=m, h=h, multiplier=m*m*h, intervals=result))
                first = False
                if squarefree[h]:
                    break
    return answer


if __name__ == "__main__":
    print(json.dumps(first_certificates(2) + first_certificates(3), indent=2))
