"""Independently invert every multiplier-one count row on all 3pq up to LIMIT."""
from bisect import bisect_right
from collections import Counter
from itertools import combinations
from math import gcd, isqrt, prod
import sys

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000


def prime_list(bound):
    sieve = bytearray([1]) * (bound + 1)
    sieve[:2] = bytes(2)
    for i in range(2, isqrt(bound) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytes((bound-i*i)//i+1)
    return [i for i in range(5, bound+1) if sieve[i]]


def positive_square(n):
    return n > 0 and isqrt(n)**2 == n


def norm(a, b, sign=1):
    return a > 0 and b > 0 and gcd(a,b)==1 and positive_square(a*a+sign*a*b+b*b)


def row_pairs(p, q):
    n = 3*p*q
    divisors = [prod(c) for i in range(4) for c in combinations((3,p,q), i)]
    for t in divisors:
        s = n//t
        if norm(t,s,1):
            yield 'E+', (t,s)
        if norm(t,s,-1):
            yield 'E-', (t,s)
        if norm(s-t,t):
            yield 'F1', (s-t,t)
        if norm(s-2*t,t):
            yield 'I120', (s-2*t,t)
        if norm(s-t,2*t-s):
            yield 'F4', (s-t,2*t-s)
        if (2*s-t)%3==0 and (2*t-s)%3==0 and norm((2*s-t)//3,(2*t-s)//3):
            yield 'F2', ((2*s-t)//3,(2*t-s)//3)
        # F3 has leading coefficient 3. Its two factors are t and (pq)/t.
        if (p*q)%t==0:
            other=p*q//t
            if norm(2*t-other,other-t):
                yield 'F3', (2*t-other,other-t)
        for tag, k2,m2 in [('BQ',s-t,s-2*t),('QP',s-t,2*s-3*t)]:
            if positive_square(k2) and positive_square(m2) and m2<k2:
                k,m=isqrt(k2),isqrt(m2)
                if gcd(k,m)==1:
                    yield tag,(k,m)


def candidate_labels(p,q):
    n=3*p*q
    for name,params in set(row_pairs(p,q)):
        if name=='BQ' and params[0]-params[1]==1:
            continue
        if name=='I120':
            a,b=params
            h=(b-1)//2
            if h>=3 and b==2*h+1 and a==h*(3*h+2):
                continue
        yield name,params


def expected(p,q):
    n=3*p*q
    if 2*q>3*p and q<2*p and positive_square(3*p-q) and positive_square(6*p-3*q):
        yield 'QP'
    if p%4==1 and p*p+18*p+9==4*q:
        yield 'BQ'
    if p%4==3 and p>9 and p*p+18*p-27==4*q:
        yield 'I120'
    if n in (345,777):
        yield 'F4'
    if n==105:
        yield 'E-'
        yield 'F1'
    if n==231:
        yield 'E+'


def main():
    primes=prime_list(LIMIT//15)
    tests=0
    counts=Counter()
    for i,p in enumerate(primes):
        if 3*p*p >= LIMIT:
            break
        end=bisect_right(primes,LIMIT//(3*p))
        for q in primes[i+1:end]:
            tests+=1
            actual={name for name,_ in candidate_labels(p,q)}
            prediction=set(expected(p,q))
            assert actual==prediction, (3*p*q, p,q,actual,prediction)
            counts.update(actual)
    print(f'All {tests} squarefree products 3pq ≤ {LIMIT:,} with 3<p<q passed.')
    print('Primitive count-row support after adjacent BQ and defect-one I120 removal:',dict(sorted(counts.items())))
    print('The replay verifies arithmetic compatibility. Geometric exclusions and constructions are inputs.')


if __name__=='__main__':
    main()
