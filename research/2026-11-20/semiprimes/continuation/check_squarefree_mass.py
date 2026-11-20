"""Check the parameter map, Euler factors, automorphisms and finite F2 counts."""
from math import gcd, isqrt, sqrt, prod, pi
from itertools import product


def H(x, y):
    return (x*x+4*x*y+y*y)*(2*x*x+2*x*y-y*y)


def primes(n):
    good = bytearray(b'\1')*(n+1)
    good[:2] = b'\0\0'
    for p in range(2, isqrt(n)+1):
        if good[p]:
            good[p*p::p] = bytes((n-p*p)//p+1)
    return [i for i, val in enumerate(good) if val]


def squarefree_table(n):
    good = bytearray(b'\1')*(n+1)
    for p in primes(isqrt(n)):
        good[::p**2] = bytes(n//(p*p)+1)
    return good


def area(t):
    return 1/(2*sqrt((1+4*t+t*t)*(2+2*t-t*t)))


def density_approx():
    steps = 10000
    integral = (area(0)+area(1)+sum((4 if i%2 else 2)*area(i/steps) for i in range(1,steps)))/(3*steps)
    prime_list = primes(1000000)
    density = prod(1-(p*p+(4 if p%12 in (1,11) else 0)*(p*p-p))/p**4 for p in prime_list if p>3)
    return integral*3/(4*(pi*pi/6)), integral*density/6, integral*density/2


def local_tests():
    for p in (5,7,11,13,17,19,23):
        m = p*p
        killed = sum(H(x,y)%m==0 for x in range(m) for y in range(m))
        assert killed == m+(4 if p%12 in (1,11) else 0)*(m-p)
        if p%12 in (1,11):
            # Of the squarefree residue classes, count those divisible by p.
            divisible_once = sum(H(x,y)%p==0 and H(x,y)%m!=0
                                 for x in range(m) for y in range(m))
            assert divisible_once*(p*p+p-4) == (m*m-killed)*4*(p-1)
    for x,y in product(range(-4,5), repeat=2):
        assert H(-x-2*y,2*x+y) == 9*H(x,y)
        assert H(-x,x+y) == H(x,y)
        assert H(-x-2*y,-x+y) == 9*H(x,y)
    print('Local counts at seven primes and three quartic identities verified.')


def count(limit, odd_only):
    bound = isqrt(isqrt(limit))
    sf = squarefree_table(6*bound**2)
    represented, realized, all_primitive = set(), set(), set()
    pairs = 0
    for x in range(2,bound+1,2 if odd_only else 1):
        for y in range(1,x,2 if odd_only else 1):
            if gcd(x,y)!=1 or (x-y)%3==0:
                continue
            p,q = x*x+4*x*y+y*y, 2*x*x+2*x*y-y*y
            n = p*q
            if n>limit:
                continue
            all_primitive.add(n)
            if not (sf[p] and sf[q]):
                continue
            assert gcd(p,q)==1 and n%24==(23 if n%2 else 2)
            a,b,c = x*x-y*y, y*(2*x+y), x*x+x*y+y*y
            if a<b:
                a,b = b,a
                u,v = x+2*y,x-y
            else:
                u,v = x,y
            g = gcd(3,u-v)
            assert (g*a,g*b,g*c)==(u*u-v*v,v*(2*u+v),u*u+u*v+v*v)
            assert gcd(u,v)==1 and (a+2*b)*(2*a+b)==n
            pairs+=1
            represented.add(n)
            if u <= (4*v*(v-1) if g==3 and v%3==2 else 4*v*v):
                realized.add(n)
    if limit == 10**6:
        direct = set()
        for a in range(2,isqrt(limit//2)+1):
            for b in range(1,a):
                if gcd(a,b)>1:
                    continue
                d = (a+2*b)*(2*a+b)
                n = a*a+a*b+b*b
                if d<=limit and (not odd_only or d%2) and isqrt(n)**2==n:
                    direct.add(d)
        assert direct == all_primitive
    print(f'X={limit} odd_only={odd_only}, all primitive distinct={len(all_primitive)}: {pairs} parameter pairs, {len(represented)} distinct candidates, '
          f'{len(realized)} staircase realizations, {len(represented-realized)} outside; '
          f'coefficient={len(represented)/sqrt(limit):.7f}')


if __name__ == '__main__':
    local_tests()
    print('Unit primitive, odd squarefree, all squarefree numerical constants:',
          ' '.join(format(x,'.9f') for x in density_approx()))
    for limit in (10**6,10**8,10**10,10**12):
        for odd_only in (True,False):
            count(limit,odd_only)
