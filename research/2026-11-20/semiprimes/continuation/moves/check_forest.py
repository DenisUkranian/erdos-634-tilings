"""Confirm the support calculation using exact coordinates in every candidate orientation."""
from fractions import Fraction as F
from math import gcd,isqrt

def product(u,v):
    x,y=u
    r,s=v
    return (x*r-y*s, x*s+y*r+y*s)


def check(a,b,c):
    p,q=a+2*b,2*a+b
    H,V=b*q,a*p
    def gauge(w):
        x,y=w
        return max(abs(x/H),abs(y/V),abs(x/H+y/V))
    s=F(b,c),F(a,c)
    bar=F(a+b,c),F(-a,c)
    axes=[(F(1),F(0)),(F(0),F(1)),(F(-H,c*c),F(V,c*c))]
    costs=[b*c*(gauge(u)+gauge(product(u,v))) for u in axes for v in (s,bar)]
    assert 2*min(costs)>1
    if a>=2*b:
        assert min(costs)==costs[-1]==F(b,c)+F(c*c,p*q)
    return 1/min(costs)

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    for triple in [(33,7,37),(35,13,43)]:
        print(triple, 'maximum side / (bc):',check(*triple))
    count=0
    for a in range(2,601):
        for b in range(1,a):
            if gcd(a,b)!=1:
                continue
            c=isqrt(a*a+a*b+b*b)
            if c*c==a*a+a*b+b*b:
                check(a,b,c)
                count+=1
    print('Tested',count,'primitive triples.')
