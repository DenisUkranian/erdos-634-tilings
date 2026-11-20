"""Enumerate just the odd mixed-residue F2 parameters outside the unit staircase."""
from math import gcd, isqrt
from verify_full_board import shape


def prime(n):
    if n < 2 or n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, isqrt(n)+1, 2))


def residuals(bound):
    rows = []
    u = 2
    # a>b implies v<u/2 and a>u^2/4, hence pq>u^4/8.
    while u**4 < 8*bound:
        for v in range(1, u//2+1, 2):
            if gcd(u,v) != 1:
                continue
            a,b,c = shape(u,v)
            g = gcd(3,u-v)
            threshold = 4*v*(v-1) if g == 3 and v % 3 == 2 else 4*v*v
            p,q = a+2*b, 2*a+b
            if (a>b and u>threshold and p*q<=bound and p%4!=q%4
                    and prime(p) and prime(q)):
                rows.append((p*q,p,q,a,b,c,u,v))
        u += 2
    return sorted(rows)


if __name__ == '__main__':
    import sys
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    print('N p q a b c u v')
    for row in residuals(bound):
        print(*row)
