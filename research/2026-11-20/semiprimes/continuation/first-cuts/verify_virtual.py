"""Recompute possible transversal cuts by the exact sine rule, without using the orientation table."""
from fractions import Fraction
from itertools import product
from math import gcd, lcm

from verify import multiply, semigroup_test


def possible_cuts(u, v):
    g = gcd(3,u-v)
    a,b,c = (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g
    h = b//v
    w = a+b
    A,B = a*(a+2*b), b*(2*a+b)
    L = A-c*w
    t0 = Fraction(L,b)
    assert t0.denominator == h
    membership = semigroup_test(a,b,c)

    def sine(angle):
        vector = (1,0)
        for exponent, factor in zip(angle, ((Fraction(b,c),Fraction(a,c)),
                                            (Fraction(a,c),Fraction(b,c)))):
            for _ in range(exponent):
                vector = multiply(vector, factor)
        return vector[1]

    def area_and_currents(t, sides, first_angle):
        x,y,chord = sides
        mass = Fraction(x*y,a*c)*t*t
        ordinary = x+(-1)**(3-first_angle[0])*chord-y
        alternating = x+(-1)**(3-first_angle[1])*chord+y
        return mass, t*ordinary/(a-b-c), t*alternating/(a-b+c)

    inner = area_and_currents(t0, (c,a,b), (1,0))
    found = set()
    for at_left in product(range(4),range(3)):
        at_right = 3-at_left[0], 2-at_left[1]
        if (0,0) in (at_left,at_right):
            continue
        sines = [sine(angle) for angle in (at_right,at_left,(0,1))]
        den = lcm(*(value.denominator for value in sines))
        raw = [int(den*value) for value in sines]
        common = gcd(*raw)
        x,y,chord = sides = [value//common for value in raw]
        low = max((c*L//v)//x,(a*L//v)//y)+1
        high = min((c*L//v+h*B-1)//x,(a*L//v+h*B-1)//y)
        if low > high:
            continue
        # Check every integral multiple of 1/h with integral chord and offsets.
        for residue in range(h):
            if any(z%h for z in (residue*x-c*(L//v),residue*y-a*(L//v),residue*chord)):
                continue
            for k in range(low+(residue-low)%h, high+1, h):
                dx,dy = (k*x-c*(L//v))//h, (k*y-a*(L//v))//h
                if not all(membership(length) for length in (dx,dy,B-dx,B-dy,k*chord//h)):
                    continue
                outer = area_and_currents(Fraction(k,h), sides, at_left)
                mass,first,second = [t-s for s,t in zip(inner,outer)]
                if any(val.denominator != 1 for val in (mass,first,second)):
                    continue
                if mass>0 and all(abs(z)<=mass and (mass-z)%2==0 for z in (first,second)):
                    found.add((at_left,dx,dy,k*chord//h))
    predicted = {((1,0),j*h*c,j*h*a,L+j*h*b) for j in range(1,2*v)}
    # Equality here concerns these finite inputs and the necessary tests above.
    assert predicted == found, (u,v,predicted ^ found)
    print(f"u={u} v={v} N={(a+2*b)*(2*a+b)} possible_transversals={len(found)}")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    for params in [(44,3),(70,3),(122,5),(82,3),(104,3),(106,3),(188,5),(268,7)]:
        possible_cuts(*params)
