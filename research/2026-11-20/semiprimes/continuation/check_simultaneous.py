"""Audit the arithmetic obstruction, possible overlaps, and the scope of the tripling theorem."""
from math import gcd, isqrt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent/'counting'))
# Use the module's input format without introducing command-line parameters here.
from replay_3pq import positive_square, prime_list


def f2_candidate(p,q):
    if (p+q)%3 or q>=2*p:
        return False
    a,b=(2*q-p)//3,(2*p-q)//3
    return a>b>0 and positive_square(a*a+a*b+b*b)


def paliy_triple(p,q):
    return 3*p<2*q<4*p and positive_square(3*p-q) and positive_square(3*(2*p-q))


if __name__=='__main__':
    # Independent coefficient identity in the two variables p, s**2.
    # After dividing by p**3 this is a polynomial of degree <=3 in s**2/p.
    for b in range(4):
        p=1
        assert (p*p-3*p*b+3*b*b)*(p+3*b)-b*(p-3*b)**2==p*p*(p-b)
    L=3_000_000
    from bisect import bisect_right
    primes=prime_list(L//15)
    tests=possible=triple=0
    for i,p in enumerate(primes):
        if 3*p*p>=L:break
        for q in primes[i+1:bisect_right(primes,L//(3*p))]:
            tests+=1
            f2=f2_candidate(p,q)
            positive=paliy_triple(p,q)
            assert not (f2 and positive), (p,q)
            possible+=f2
            triple+=positive
    print(f'3pq <= {L}: {tests} prime pairs, {possible} F2 inputs, {triple} Paliy triples, zero overlaps.')
    # A positive control when the smaller factor has several prime divisors.
    a,b,c=6319,1521,7201
    s,t=39,118
    p,q=a+2*b,2*a+b
    assert gcd(a,b)==1 and c*c==a*a+a*b+b*b
    assert b==s*s and t*t==a+5*b and a>4*b
    assert p==11*23*37 and q in prime_list(q)
    u,v=80,9
    assert (a,b,c)==(u*u-v*v,v*(2*u+v),u*u+u*v+v*v)
    assert u<=4*v*v and (u-v)%3!=0
    assert 2*t*t-(3*s)**2==q and 3*t*t-(3*s)**2==3*p
    U,V=c*t,s*(p-3*s*s)
    assert 0<U-V<U+V<p*p and (U-V)*(U+V)==p*p*(p-s*s)
    sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'staircase'))
    from staircase import make
    from check_staircase import check
    steps=[(v+(u+v)*m,u-v*m) for m in ([3]*10+[4]*8)]
    witness=make(a,b,c,steps)
    check(witness)
    assert witness['count']==p*q and len(witness['blocks'])>0
    print(f'Four-prime positive control: N={p*q} ({len(witness["blocks"])} verified grids), triple={3*p*q}.')
