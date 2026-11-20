"""Exact finite dual certificates for whole-board T-junction lower bounds."""
import json
from fractions import Fraction
from pathlib import Path


def rotate(pair, turns):
    x, y = pair
    for _ in range(turns):
        x, y = -y, x+y
    return x, y


def verify(n, sides):
    a,b,c = sides
    cert = json.loads(Path(__file__).with_name(f'dual_{n}.json').read_text())
    period, cap, den, weights = (cert[k] for k in ('H','cap','d','Y'))
    assert den > 0 and len(weights) == 3*period+3

    def value(h,j,word):
        x,y,z = word
        score = weights[2*period+(h%period)]*(-1)**j*(x+y)
        for delta, coefficient in enumerate([(-y,x),(-z,2*z),(y-x,x)],-1):
            u,v = rotate(coefficient,j)
            k = 2*((h+delta)%period)
            score += weights[k]*u + weights[k+1]*v
        return score

    count = 0
    for x in range(cap+3):
        for y in range(-cap-2,cap+3):
            t = -a*x-b*y
            if t%c:
                continue
            w = x,y,t//c
            cost = sum(abs(v) for v in w)-2
            if w <= (0,0,0) or cost>cap:
                continue
            for h in range(period):
                for j in range(6):
                    assert value(h,j,w) <= den*cost
                    count += 1
    for i,(length,h,j) in enumerate(((b*(2*a+b),0,0),(a*(a+2*b),0,4),(c*c,2,1))):
        possibilities = 0
        for x in range(length//a+1):
            for y in range((length-x*a)//b+1):
                t = length-x*a-y*b
                if t<c or t%c:
                    continue
                assert value(h,j,(x,y,t//c)) >= weights[3*period+i]
                possibilities += 1
        assert possibilities>0
    bound = Fraction(sum(weights[-3:]),den)
    assert cap >= bound
    even_bound = 2*((bound.numerator+2*bound.denominator-1)//(2*bound.denominator))
    print(f'{n}: {count} local inequalities; weight {bound}; at least {even_bound} T-junctions.')
    return even_bound


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    assert verify(3431,(33,7,37)) == 88
    assert verify(5063,(35,13,43)) == 106
