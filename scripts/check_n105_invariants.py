#!/usr/bin/env python3
"""Exact finite invariant checks and a universal F1 formal-boundary identity.
No geometric search and no claim of a tiling or global N=105 exclusion.
"""
from math import gcd, isqrt
import json

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")

def factor_pairs(n):
    return [(s,n//s) for s in range(1,isqrt(n)+1) if n%s==0]

def invariant_candidates(n, angle):
    out=[]
    for s,t in factor_pairs(3*n):
        if angle==60 and s*s>=n:
            continue # equality is the equilateral tile, not this irrational branch
        rad=(t-s)**2+(16*n if angle==120 else -4*n)
        q=isqrt(rad) if rad>=0 else -1
        row={'s':s,'t':t,'radicand':rad,'is_square':q>=0 and q*q==rad}
        if row['is_square']:
            if angle==120:
                an,bn=q+t-s,q-t+s
            else:
                an,bn=s+t+q,s+t-q
            g=gcd(an,bn); a,b=an//g,bn//g
            c2=a*a+b*b+(a*b if angle==120 else -a*b)
            c=isqrt(c2)
            assert c*c==c2
            S=isqrt(n*a*b)
            assert S*S==n*a*b
            row['primitive_candidate']=(min(a,b),max(a,b),c,S)
        out.append(row)
    return out

def E(n,j,length):
    j%=6
    return {(n,j%3):length*(1 if j<3 else -1)}

def add(*terms):
    out={}
    for term in terms:
        for key,val in term.items():out[key]=out.get(key,0)+val
    return {k:v for k,v in out.items() if v}

def scale(k,d):return {p:k*v for p,v in d.items()}

def R(a,b,c,n,j):
    return add(E(n,j,c),E(n+1,j+2,a),E(n+1,j,-b))

def S(a,b,c,n,j):
    return add(E(n,j,c),E(n-1,j+1,-a),E(n-1,j,-b))

def check_F1(a,b,c):
    assert c*c==a*a+a*b+b*b
    target=add(E(0,0,b*(a+b)),E(0,1,-a*b),E(-1,0,-b*c))
    formal=add(scale(a,R(a,b,c,-1,1)),scale(c,S(a,b,c,0,0)))
    assert formal==target
    N=b*(a+b)
    assert (N-a-c)%2==0
    assert N>=a+c
    return {'tile':[a,b,c],'target_sides':[N,a*b,b*c],
            'N':N,'seed_count':a+c,'cancelling_pairs':(N-a-c)//2,
            'boundary':{str(k):v for k,v in target.items()}}

if __name__=='__main__':
    data={'N105_120':invariant_candidates(105,120),'N105_60':invariant_candidates(105,60),
          'F1_105':check_F1(8,7,13)}
    assert not any(r['is_square'] for r in data['N105_120'])
    assert {tuple(r['primitive_candidate']) for r in data['N105_60'] if r['is_square']}=={(5,21,19,105),(7,15,13,105)}
    tested=0
    for a in range(1,101):
        for b in range(1,101):
            c=isqrt(a*a+a*b+b*b)
            if c*c==a*a+a*b+b*b and gcd(a,b)==1:
                check_F1(a,b,c);tested+=1
    data['F1_primitive_examples_checked']=tested
    print(json.dumps(data,indent=2))
