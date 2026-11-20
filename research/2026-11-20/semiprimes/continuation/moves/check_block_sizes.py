"""Independently enumerate short side-count relations for the primitive F2 triples."""
from math import gcd


def check(u, v, g):
    a = (u*u-v*v)//g
    b = v*(2*u+v)//g
    c = (u*u+u*v+v*v)//g
    assert gcd(a, b) == 1 and a*a+a*b+b*b == c*c
    m = u+2*v if g == 1 else u
    best = None
    for x in range(-m,m+1):
        for y in range(abs(x)-m,m-abs(x)+1):
            num = -(a*x+b*y)
            if num%c:
                continue
            z = num//c
            size = abs(x)+abs(y)+abs(z)
            if size and (best is None or size<best):
                best = size
    assert best == m
    if u < 6*v:
        return
    limit = u*b
    smallest = None
    shortest = set()
    for x in range(-(limit//a),limit//a+1):
        for y in range(-(limit//b),limit//b+1):
            num = -(a*x+b*y)
            if num%c:
                continue
            z = num//c
            length = (a*abs(x)+b*abs(y)+c*abs(z))//2
            if length and (smallest is None or length <= smallest):
                if length != smallest:
                    shortest.clear()
                smallest = length
                shortest.add((x,y,z))
    assert smallest == limit
    assert shortest == {(v,-u,v),(-v,u,-v)}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    tests = 0
    for u in range(2,69):
        for v in range(1,u):
            if gcd(u,v)==1:
                check(u,v,gcd(3,u-v))
                tests+=1
    print(f'Checked shortest count relations for {tests} primitive parameter pairs.')
    print('On every tested pair with u >= 6v the unique metric minimizers were +/-R.')
