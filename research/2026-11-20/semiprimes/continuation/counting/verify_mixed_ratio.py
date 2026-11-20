"""Independent reconstruction from the single-cone quartic parametrization.

Uses SymPy for a second primality implementation. The primary mixed_ratio
enumeration uses only the Python standard library and trial division.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from math import gcd

from sympy import isprime


def conic_rows(bound):
    # This upper bound for u/v follows from 2-f(x)=(6x+3)/(x²+4x+1)<6/x.
    # If f(x)<=R, then x<6/(2-R). On residual rows x>4(v-1).
    upper = (6*bound.denominator)//(2*bound.denominator-bound.numerator)+1
    vmax = upper//4 + 1
    umax = upper*vmax
    answers = set()

    def add(x,y):
        if not 0<y<x or x%2 or y%2!=1 or (x-y)%3==0 or gcd(x,y)!=1:
            return
        c=x*x+x*y+y*y
        a,b=sorted((x*x-y*y,y*(2*x+y)),reverse=True)
        common=gcd(a+c,b)
        u,v=(a+c)//common,b//common
        if u<=4*v*(v-1 if (u-v)%3==0 and v%3==2 else v):
            return
        p,q=a+2*b,2*a+b
        if bound.denominator*q>bound.numerator*p or not (isprime(p) and isprime(q)):
            return
        assert 3*c*c==p*p-p*q+q*q
        answers.add((p*q,p,q,u,v))

    # g=1 gives y=v,x=u. For g=3, x-y=v,x+2y=u.
    for v in range(1,vmax+1,2):
        for x in range(2,min(umax,upper*v)+1,2):
            add(x,v)
        for y in range(1,upper*v//3+1,2):
            add(y+v,y)
    return sorted(answers)


def fingerprint(rows):
    return sha256(''.join(','.join(map(str,r))+'\n' for r in rows).encode('ascii')).hexdigest()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('ratio',nargs='?',type=Fraction,default=Fraction(19,10))
    args=parser.parse_args()
    if not 1<args.ratio<2:
        parser.error('choose a rational strictly between 1 and 2')
    rows=conic_rows(args.ratio)
    print(len(rows),rows[-1] if rows else None,fingerprint(rows))
