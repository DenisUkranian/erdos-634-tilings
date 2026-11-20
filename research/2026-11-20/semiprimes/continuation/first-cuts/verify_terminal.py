"""Exhaust the two short sides for every Q_j in several exact parameter controls."""
from fractions import Fraction
from itertools import product
from math import gcd, lcm
from verify import multiply


def check(u,v):
    g = gcd(3,u-v)
    a,b,c = (u*u-v*v)//g, v*(2*u+v)//g, (u*u+u*v+v*v)//g
    w = a+b
    p,q = a+2*b, 2*a+b
    A,B,C = a*p, b*q, c*c
    L = A-c*w
    h = b//v

    def sine(angle):
        unit = (1,0)
        for count,factor in zip(angle, ((Fraction(b,c),Fraction(a,c)),
                                        (Fraction(a,c),Fraction(b,c)))):
            for _ in range(count):
                unit = multiply(unit,factor)
        return unit[1]

    apex = (0,2)

    def invariants(t, sides, at_first):
        x,y,chord = sides
        area = t*t*x*y*sine(apex)/(a*b)
        first = x+(-1)**(3-at_first[0])*chord-y
        second = x+(-1)**(3-at_first[1])*chord-y
        return area, t*first/(a-b-c), t*second/(a-b+c)

    lower = None
    for j in range(1,2*v):
        r = 1-Fraction(j*c,v*q)
        outer = 1-Fraction(j*a,v*q)
        min_x,min_y = r*a*c,r*c*w
        max_x,max_y = outer*C,outer*A
        D = lcm(min_x.denominator,min_y.denominator)
        inner_data = invariants(r, (a*c,c*w,B), (2,1))
        outer_data = invariants(outer,(C,A,B),(2,0))
        lower = B-2*j*(L//v)-j*j*h*h
        assert lower == outer_data[0]-inner_data[0] > 0
        for first_angle in product(range(4),range(2)):
            last_angle = 3-first_angle[0], 1-first_angle[1]
            if (0,0) in (first_angle,last_angle):
                continue
            ratios = [sine(z) for z in (last_angle,first_angle,apex)]
            den = lcm(*(z.denominator for z in ratios))
            nums = [int(den*z) for z in ratios]
            common = gcd(*nums)
            x,y,chord = sides = [z//common for z in nums]
            # One radius is invertible modulo D for each candidate in these controls.
            if gcd(x,D)==1:
                residue = int(min_x*D)*pow(x,-1,D)%D
            else:
                assert gcd(y,D)==1
                residue = int(min_y*D)*pow(y,-1,D)%D
            if any(z%D for z in (residue*x-int(min_x*D),
                                 residue*y-int(min_y*D),residue*chord)):
                continue
            first = max(int(min_x*D)//x, int(min_y*D)//y)+1
            last = min((int(max_x*D)-1)//x,(int(max_y*D)-1)//y)
            for m in range(first+(residue-first)%D,last+1,D):
                between = invariants(Fraction(m,D),sides,first_angle)
                assert any((x-y).denominator != 1
                           for reference in (inner_data,outer_data)
                           for x,y in zip(between,reference)), (u,v,j,first_angle,m)
    print(f"u={u} v={v} N={p*q} terminal_bound={lower}")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    for u,v in [(44,3),(70,3),(122,5),(82,3),(104,3),(106,3),(188,5),(268,7)]:
        check(u,v)
