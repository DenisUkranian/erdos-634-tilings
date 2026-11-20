"""Independent bounded lattice minimizations checking the symbolic odd upper bound."""
from math import gcd
from check_upper_odd import solve

def check(u, v):
    g = gcd(3, u-v)
    a = (u*u-v*v)//g
    b = v*(2*u+v)//g
    c = (u*u+u*v+v*v)//g
    F = (u-v)//g
    if g == 1:
        extra = 2*v*(v+1)
    elif v == 1:
        extra = 2*F
    else:
        extra = 2*v*((v+2)//3)
    measured, witnesses = solve(a,b,c)
    assert witnesses and measured == a+b+v*F+extra

if __name__ == '__main__':
    count = 0
    for v in (1,3,5,7):
        first = max(6*v, v*v+3*v+1)
        for u in range(first, first+38):
            if u % 2 == 0 and gcd(u,v) == 1:
                check(u,v)
                count += 1
    print('Verified', count, 'independent integer minimizations.')
