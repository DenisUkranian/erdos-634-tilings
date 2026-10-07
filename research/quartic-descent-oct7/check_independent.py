#!/usr/bin/env python3
"""Independent exact spot checks accompanying the universal proof."""
import itertools
import json
import math

def leg(a, p):
    z = pow(a % p, (p - 1) // 2, p)
    return 0 if z == 0 else (1 if z == 1 else -1)

# Sparse exact polynomials in S,T,C, with integer coefficients.
def add(*polys):
    z = {}
    for poly in polys:
        for key,value in poly.items():
            z[key] = z.get(key,0) + value
    return {key:value for key,value in z.items() if value}

def scale(poly,n):
    return {key:n*value for key,value in poly.items() if n*value}

def mul(a,b):
    out = {}
    for k,v in a.items():
        for l,w in b.items():
            key = tuple(x+y for x,y in zip(k,l))
            out[key] = out.get(key,0) + v*w
    return {key:value for key,value in out.items() if value}

S, T, C = ({(1,0,0):1}, {(0,1,0):1}, {(0,0,1):1})
ST, TT = mul(S,T), mul(T,T)
x = mul(T, add(scale(T,2), scale(S,-3), scale(C,2)))
identity = add(mul(x,x), mul(add(scale(ST,6),scale(TT,-4)),x),
               scale(mul(ST,ST),-3))
norm = add(mul(C,C),scale(mul(S,S),-3),scale(ST,3),scale(TT,-1))
assert identity == scale(mul(TT,norm),4)

qualifying = []
prime_checks = 0
assert pow(3,9,37) == 36  # Important nonqualifying control.
for p in range(5, 5000):
    if any(p % q == 0 for q in range(2,math.isqrt(p)+1)):
        continue
    if p % 24 != 13:
        continue
    prime_checks += 1
    assert leg(2,p) == -1 and leg(3,p) == 1 and leg(-12,p) == 1
    roots = [q for q in range(p) if (q*q+6*q-3) % p == 0]
    assert len(roots) == 2
    eps = 1 if pow(3, (p-1)//4, p) == 1 else -1
    assert all(leg(q,p) == -eps for q in roots)
    if eps == 1:
        qualifying.append(p)

assert qualifying[:3] == [13,109,181]
assert 37 not in qualifying
assert math.prod(qualifying[:3]) == 256477
assert 6*math.prod(qualifying[:3]) == 1538862

# Every squareclass is eliminated by at least one necessary character rule
# for every odd-size subset of the first seven qualifying primes.
products_checked = 0
classes_checked = 0
for n in (1,3,5,7):
    for primes in itertools.combinations(qualifying[:7], n):
        products_checked += 1
        R = math.prod(primes)
        assert (6*R) % 16 == 14
        for mask in range(1 << n):
            A = math.prod(p for i,p in enumerate(primes) if mask >> i & 1)
            B = R // A
            cross_left = math.prod(leg(A,p) for p in primes if B % p == 0)
            cross_right = math.prod(leg(B,p) for p in primes if A % p == 0)
            assert cross_left*cross_right == 1
            conditions = [leg(A,p) == -1 for p in primes if B % p == 0]
            conditions += [leg(B,p) == -1 for p in primes if A % p == 0]
            assert not all(conditions)
            for j in (0,1):
                classes_checked += 1
                e = 2*(3**j)*A
                assert (12*R*R) % e == 0
                for p in primes:
                    if B % p == 0:
                        assert leg(e,p) == -leg(A,p)
                    else:
                        delta, kappa = e//p, 2*R//p
                        assert leg(delta*kappa,p) == leg(B,p)

print(json.dumps({
    'status':'PASS',
    'symbolic_rational_map':True,
    'prime_bound_exclusive':5000,
    'prime_residue_checks':prime_checks,
    'qualifying_primes':qualifying,
    'nonqualifying_control_p37':True,
    'odd_products_checked':products_checked,
    'supported_positive_squareclasses_checked':classes_checked,
    'bounded_checks_prove_universal_theorem':False,
    'full_Erdos634_solved':False
}, indent=2))
