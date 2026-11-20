"""A surrounding packing for the two-stage rhombus exchange on the control boards."""
from fractions import Fraction as F
from itertools import product
from math import ceil, floor


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def shift(p, q):
    return p[0]+q[0], p[1]+q[1]


def scale(x,p):
    return x*p[0], x*p[1]


def run(a,b,c,k):
    p,q=a+2*b,2*a+b
    # Physical axial coordinates are recorded after multiplication by c.
    board=[(0,0),(b*q*c,0),(0,a*p*c)]
    origin=(a*b*c,c)
    e=(-a*b,b*(a+b))
    f=(a*b,a*a)
    index=det(e,f)
    def lattice(P):
        v=shift(P,scale(-1,origin))
        return F(det(v,f),index),F(det(e,v),index)
    def coordinate(P):
        return shift(origin,shift(scale(P[0],e),scale(P[1],f)))
    def inside(P):
        x,y=coordinate(P)
        return x>=0 and y>=0 and a*p*x+b*q*y<=a*p*b*q*c
    def in_strip(P):
        i,j=P
        return 0<=j<=k*b and 0<=i-j<=c
    us,vs=zip(*(lattice(P) for P in board))
    packed=switched=0
    for i,j in product(range(floor(min(us))-1,ceil(max(us))+1),
                       range(floor(min(vs))-1,ceil(max(vs))+1)):
        o=(i,j)
        d=(i+1,j+1)
        for middle in ((i+1,j),(i,j+1)):
            T=[o,middle,d]
            on_board=all(inside(P) for P in T)
            packed+=on_board
            if all(in_strip(P) for P in T):
                assert on_board
                switched+=1
    assert switched==2*k*b*c
    print(f'{p*q}: {packed} whole tiles, {switched} in the exchange, {packed-switched} outside.')
    return packed,switched


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    run(33,7,37,2)
    run(35,13,43,2)
