"""Exact polynomial replay for the three boundary rows and their minors."""
from collections import Counter
from itertools import product
from math import gcd

def poly(terms=()):
    out = Counter()
    for i, j, k in terms:
        out[i, j] += k
    return {key: value for key, value in out.items() if value}

def terms(f):
    return [(i, j, a) for (i, j), a in f.items()]

def add(*fs):
    return poly(t for f in fs for t in terms(f))

def shift(f, i, j, sign=1):
    return poly((x+i, y+j, sign*a) for (x, y), a in f.items())

def mul(f, g):
    return poly((i+x, j+y, a*b) for (i,j),a in f.items() for (x,y),b in g.items())

def sub(f, g):
    return add(f, shift(g, 0, 0, -1))

def det(a,b,c,d):
    return sub(mul(a,d), mul(b,c))

def boundary(up,down):
    return [sub(up, shift(down,0,1)), sub(shift(down,1,0),up), sub(up,down)]

def pcheck(n):
    up = poly((i,j,1) for i,j in product(range(n),repeat=2) if i+j<n)
    down = poly((i,j,1) for i,j in product(range(n),repeat=2) if i+j<n-1)
    back_up = poly((i,j,1) for i,j in product(range(n),repeat=2) if i+j>=n)
    back_down = poly((i,j,1) for i,j in product(range(n),repeat=2) if i+j>=n-1)
    v, w = boundary(up,down), boundary(back_up,back_down)
    a = poly((i,0,1) for i in range(n))
    b = poly((0,i,1) for i in range(n))
    c = poly((n-1-i,i,1) for i in range(n))
    if v != [a, shift(b,0,0,-1), c]:
        raise ValueError(f"forward boundary at {n}")
    if w != [shift(a,0,n,-1),shift(b,n,0),shift(c,0,0,-1)]:
        raise ValueError(f"reverse boundary at {n}")
    abc = mul(mul(a,b),c)
    values = [det(v[i],w[i],v[j],w[j]) for i,j in [(0,1),(0,2),(1,2)]]
    predictions = [sub(shift(abc,1,0),shift(abc,0,1)),
                   sub(shift(abc,0,1),abc),sub(abc,shift(abc,1,0))]
    if values != predictions or len(up)*len(back_down)-len(back_up)*len(down) != n**3:
        raise ValueError(f"minor at {n}")

def fieldcheck(scales, prime, x, y):
    if x == y == 1:
        return any(n**3 % prime for n in scales)
    columns = []
    for n in scales:
        a = sum(pow(x,k,prime) for k in range(n)) % prime
        b = sum(pow(y,k,prime) for k in range(n)) % prime
        c = sum(pow(x,n-1-k,prime)*pow(y,k,prime) for k in range(n)) % prime
        columns.extend(((a,-b,c), (-pow(y,n,prime)*a,pow(x,n,prime)*b,-c)))
    for i,j in [(0,1),(0,2),(1,2)]:
        if any((u[i]*v[j]-u[j]*v[i])%prime for u in columns for v in columns):
            return True
    return False

def main():
    for n in range(1, 33):
        pcheck(n)
    seed_sets = [(2,3), (4,9), (6,10,15), (6,14,21), (15,21,35)]
    for seed in seed_sets:
        if gcd(*seed) != 1:
            raise ValueError("nonprimitive control")
        for prime in [2,3,5,7,11,13,17,19,23,29,31]:
            for x,y in product(range(1,prime),repeat=2):
                if not fieldcheck(seed,prime,x,y):
                    raise ValueError((seed,prime,x,y))
    print("PASS: exact Laurent coefficients, both board boundaries, three minors and integer counts for n=1,...,32.")
    print("PASS: five gcd-one scale sets at all nonzero coordinate pairs over eleven prime fields.")

if __name__ == "__main__":
    main()
