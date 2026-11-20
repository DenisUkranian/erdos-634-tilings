"""Integer dual proof of minimum T-junction counts in the two primitive F2 boards."""
from fractions import Fraction
from pathlib import Path
import json


def check(n, a, b, c):
    cert = json.loads(Path(__file__).with_name(f'tile_weights_{n}.json').read_text())
    period, cap, d, table, lower = (cert[k] for k in ('H','cap','d','Y','K'))
    assert d>0 and len(table)==9*period and len(lower)==3
    def score(h,j,w):
        ix = (h%period)*9+(j%3)*3
        sign = 1 if j%6<3 else -1
        return sign*sum(table[ix+k]*w[k] for k in range(3))
    # The three sides of an oriented tile or its mirror, up to overall reversal.
    for h in range(period):
        for j in range(6):
            for sign in (1,-1):
                assert (score(h,j,(1,0,0)) + score(h,j+sign,(0,1,0))
                        == score(h+sign,j,(0,0,1)))
    tests=0
    for x in range(cap+3):
        for y in range(-cap-2,cap+3):
            t = -(a*x+b*y)
            if t%c:
                continue
            w = x,y,t//c
            cost = sum(abs(v) for v in w)-2
            if w<=(0,0,0) or cost>cap:
                continue
            for h in range(period):
                for j in range(6):
                    assert score(h,j,w)<=d*cost
                    tests+=1
    sides=((b*(2*a+b),0,0),(a*(a+2*b),0,4),(c*c,2,1))
    for bound,(length,h,j) in zip(lower,sides):
        checked=0
        for x in range(length//a+1):
            for y in range((length-a*x)//b+1):
                t=length-a*x-b*y
                if t>=c and t%c==0:
                    assert score(h,j,(x,y,t//c))>=bound
                    checked+=1
        assert checked>0
    total=Fraction(sum(lower),d)
    result=2*((total.numerator+2*total.denominator-1)//(2*total.denominator))
    assert cap>=result
    print(f'{n}: {tests} checked inequalities; virtual boundary weight {total}; at least {result} T-junctions.')
    return result


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    assert check(3431,33,7,37)==138
    assert check(5063,35,13,43)==146
