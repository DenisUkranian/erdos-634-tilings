#!/usr/bin/env python3
"""Exact finite regression checks for README's symbolic I120/F3 dissection.

This checks identities and geometry on a finite family; the universal proof
is the written argument. It produces no tiling or new admissible count.
"""
from fractions import Fraction as Q
from math import gcd, isqrt
import json

def norm2(p,q):
    x,y=p[0]-q[0],p[1]-q[1]
    return x*x+x*y+y*y

def area2(p,q,r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])

def main():
    count=0
    for a in range(1,501):
        for b in range(1,501):
            if gcd(a,b)!=1:continue
            c=isqrt(a*a+a*b+b*b)
            if c*c!=a*a+a*b+b*b:continue
            U=a+2*b;W=a+b
            A=(Q(b*b),Q(a*b));B=(Q(0),Q(0));C=(Q(b*U),Q(0))
            D=(Q(3*b*b*W,U),Q(0))
            assert 0<D[0]<C[0]
            assert norm2(A,B)==norm2(A,C)==(b*c)**2
            assert norm2(A,D)==norm2(C,D)==Q(b*c*c,U)**2
            assert area2(B,D,A)>0 and area2(D,C,A)>0
            assert area2(B,D,A)+area2(D,C,A)==area2(B,C,A)
            assert area2(B,D,A)/Q(a*b)==3*U*W*Q(b,U)**2
            assert area2(D,C,A)/Q(a*b)==b*U*Q(c,U)**2
            T=3*((c+min(a,b)-1)//min(a,b))
            assert U>T
            count+=1
    return {'status':'PASS','ordered_primitive_triples_checked':count,
            'range':'1 <= a,b <= 500','exact_rational_geometry':True,
            'new_I120_counts_claimed':0,'154_status':'UNRESOLVED',
            'full_Erdos634_solved':False}

if __name__=='__main__':print(json.dumps(main(),indent=2))
