"""Arithmetic regression for POWERS.md. Run with Python 3, without -O."""
import json
from math import gcd, isqrt


def ceil_div(a, b):
    return (a + b - 1) // b


def notch(e, f):
    assert 0 < e < f and gcd(e, f) == 1
    b = f * f - e * e
    h = ceil_div(e, f - e)
    j = ceil_div(h * e, b)
    m = max(ceil_div(f * h, e), h + ceil_div(e * h, f))
    return h, j, m, f * j + m


def heron16(sides):
    x, y, z = sides
    return (x+y+z) * (-x+y+z) * (x-y+z) * (x+y-z)


def sample_geometry(e, f, t):
    b = f*f-e*e
    assert heron16([t*b*f, t*b*f, t*b*e]) == (b*t*t)**2 * heron16([e*f,b,f*f]) > 0


def prime_sieve(limit):
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = bytes(2)
    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            flags[p*p::p] = bytes((limit-p*p)//p + 1)
    return flags


def check(limit=200_000, prime_limit=1_000_000):
    samples = {}
    for n in range(3, limit+1):
        if n % 2:
            e = (n-1)//2
            f = e+1
            h, j, m, t0 = notch(e, f)
            assert (h,j,m) == (e,ceil_div(e,2),2*e)
            threshold = (e*e+5*e+2)//2 if e >= 3 and e%2 else t0
            assert n+n*n//8-threshold == (e%2==0)
            t = n*n
        else:
            e, f = n-1, n+1
            h, j, m, t0 = notch(e, f)
            assert (h,j,m) == (n//2,ceil_div(n-1,8),n)
            if n==4:
                assert 4**5 == 32**2
                continue
            t = n*n//2
        assert t0 <= t and (f*f-e*e)*t*t == n**5
        if n in {3,5,6,7,10,19,43,99,200_000}:
            sample_geometry(e, f, t)
            samples[n] = dict(e=e, f=f, t0=t0, t=t, tile_count=n**5)
    balanced = 0
    for x in range(3,150,2):
        for y in range(x+2,min(4*x*x*(x-2),1500)+1,2):
            if gcd(x,y)==1:
                e,f=(y-x)//2,(x+y)//2
                assert notch(e,f)[-1] <= x*y
                balanced+=1
    assert notch(12,31) == (1,1,3,34)
    primes = prime_sieve(prime_limit)
    seen = {2:set(),3:set()}
    for v in range(2,isqrt(prime_limit)+1):
        for u in range(1,v):
            for d in (2,3):
                p = d*v*v-u*u
                if p <= prime_limit and primes[p]:
                    assert gcd(u,v)==1 and p==(d*v-u)*v+(v-u)*u
                    seen[d].add(p)
    for p in range(5,prime_limit+1):
        if not primes[p] or p%4==1:
            continue
        if p%24==19:
            assert all(p not in data for data in seen.values())
        elif p%24==11:
            assert p in seen[3]
        else:
            assert p%24 in (7,23) and p in seen[2]
    for e in range(2,limit):
        assert e+1+ceil_div(e*e*(e+1),2*e+1)>2*e+1
    return dict(
        n_checked_through=limit, balanced_coprime_pairs=balanced,
        prime_norms_checked_through=prime_limit,
        D2_prime_representatives=len(seen[2]), D3_prime_representatives=len(seen[3]),
        explicit_examples=samples, all_assertions_passed=True,
    )


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
