"""Exact unconditional minimum number of steps in the two consecutive height alphabets.

Congruence and displacement only. A minimizing ordered path need not fit the board.
"""
from math import gcd


def hexnorm(p):
    x, y = p
    return max(abs(x), abs(y), abs(x+y))


def minimum(a, b, c, lower=False):
    # Frame divided by c*z with x+y*rho. Middle directions are units.
    # An upper off-middle net displacement is z*(x+y*rho); the lower one is conjugate(z)*(x+y*rho).
    A, D = (a+b, -b) if lower else (a,b)
    target = (a+b, -b)
    best = hexnorm(target)
    minimizers = []
    for x in range(-best,best+1):
        # A*x-D*y=0 modulo c; the other component is then 0 by the norm equation.
        offset = A*x*pow(D,-1,c) % c
        for y in range(offset-((offset+best)//c)*c, best+1,c):
            if y < -best:
                continue
            first = A*x-D*y
            second = D*x+(A+D)*y
            assert first % c == second % c == 0
            t, u = target[0]-first//c, target[1]-second//c
            cost = hexnorm((t,u))+hexnorm((x,y))
            if cost < best:
                best = cost
                minimizers = []
            if cost == best:
                minimizers.append((t,u,x,y))
    return best,minimizers


if __name__ == '__main__':
    for u,v in [(4,1),(10,1),(6,1),(16,1),(12,1),(22,1),(18,1),(40,1),(44,3),(122,5)]:
        g=gcd(3,u-v)
        a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
        low,_=minimum(a,b,c,True)
        high,nets=minimum(a,b,c)
        assert low==c
        print((a+2*b)*(2*a+b),a,b,c,low,high,len(nets),flush=True)
