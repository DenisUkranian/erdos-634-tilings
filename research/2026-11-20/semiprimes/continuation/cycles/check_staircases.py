"""Exact companion checks for the staircase construction and the mesh bound."""
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt


def row_lengths(a, b, c):
    u, v = a*(a+2*b), b*(2*a+b)
    return [(u*v-c*u*j)//(c*v) for j in range(1, v//c+1)]


def check_bars(a, b, c, bars):
    u, v = a*(a+2*b), b*(2*a+b)
    area, prev_x, prev_y = 0, 0, v//c+1
    for x,y in bars:
        assert x>prev_x and 0<y<prev_y
        assert c*(v*x+u*y)<u*v
        area+=(x-prev_x)*y
        prev_x,prev_y=x,y
    assert area==a*b
    polygon=[(0,0),(bars[-1][0],0)]
    for index in range(len(bars)-1,-1,-1):
        x,y=bars[index]
        polygon.extend([(x,y),(bars[index-1][0] if index else 0,y)])
    masses=[Counter(),Counter()]
    for (x0,y0),(x1,y1) in zip(polygon,polygon[1:]+polygon[:1]):
        assert (x0==x1) != (y0==y1)
        mass=masses[int(x0==x1)]
        mass[x1%a,y1%a]+=1
        mass[x0%a,y0%a]-=1
    variation=[sum(abs(weight) for weight in mass.values()) for mass in masses]
    assert variation==([12,12] if a==33 else [6,6])
    print(f'{(a+2*b)*(2*a+b)}: {area} whole rhombi, {len(bars)-1} reflex corners, endpoint variations {variation}')


def main():
    small=[]
    for b in (1,3,5,7):
        for a in range(b+2, (3*b*b)//4+1, 2):
            c=isqrt(a*a+a*b+b*b)
            if gcd(a,b)==1 and c*c==a*a+a*b+b*b:
                small.append((a,b,c,sum(row_lengths(a,b,c))))
    assert small==[(5,3,7,16),(33,7,37,260)]
    print('Small primitive odd cases and available rhombi:',small)
    check_bars(33,7,37,[(5,12),(14,9),(20,7),(26,5),(32,3)])
    check_bars(35,13,43,[(12,19),(23,13),(35,7)])
    a,b,c=35,13,43
    n=(a+2*b)*(2*a+b)
    sqrt3_lower=Fraction(433,250)
    assert sqrt3_lower**2<3
    scale=1-Fraction(8*c,3*a*b)/sqrt3_lower
    lower=Fraction(n*a*b,2*c*c)*scale**2
    assert scale>0 and lower>a*b-1
    print(f'{n}: all mesh rotations and translations, strict area lower bound {lower} > {a*b-1}')


if __name__=='__main__':
    main()
