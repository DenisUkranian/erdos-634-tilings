"""Exact checks for the F3 split-part reduction; no geometric solver."""
import argparse
from functools import lru_cache
from math import gcd, isqrt
import json
from pathlib import Path

if not __debug__:
    raise SystemExit("Verification requires assertions; run without -O or PYTHONOPTIMIZE.")


def factors(n):
    out={}
    p=2
    while p*p<=n:
        while n%p==0:
            out[p]=out.get(p,0)+1
            n//=p
        p+=1 if p==2 else 2
    if n>1:
        out[n]=out.get(n,0)+1
    return out


def divisors(n):
    out=[1]
    for p,e in factors(n).items():
        old=out[:]
        out=[a*p**j for a in old for j in range(e+1)]
    return sorted(out)


def split_prime(p):
    return p>3 and p%24 in (1,11,13,23)


def split_part(m):
    h=1
    for p,e in factors(m).items():
        if split_prime(p):
            h*=p**e
    return h


def kernel_plus(d):
    z=gcd(d,2)
    for p in factors(d):
        if split_prime(p):
            z*=p
    return z


@lru_cache(None)
def restricted_list(d,h):
    out=set()
    for U in divisors(kernel_plus(d)*h*h):
        for W in range(U//2+1,U):
            if gcd(U,W)!=1 or (3*U*W)%d:
                continue
            ss=3*U*W//d
            s=isqrt(ss)
            if s*s!=ss:
                continue
            cc=U*U-3*U*W+3*W*W
            c=isqrt(cc)
            if c*c==cc:
                a,b=2*W-U,U-W
                assert a>0 and b>0 and gcd(a,b)==1
                out.add((a,b,c,s))
    return out


def direct_list(d,m):
    out=set()
    for s in divisors(m):
        D=d*s*s
        if D%3:
            continue
        for U in divisors(D//3):
            W=D//(3*U)
            if not (U<2*W and W<U and gcd(U,W)==1):
                continue
            cc=U*U-3*U*W+3*W*W
            c=isqrt(cc)
            if c*c==cc:
                out.add((2*W-U,U-W,c,s))
    return out


def check():
    checks=0
    # Diverse small split parts and unbounded-support theorem's first cases.
    for d in range(1,201):
        if any(e>1 for e in factors(d).values()):
            continue
        for m in range(1,100):
            h=split_part(m)
            if h>13:
                continue
            restricted={z for z in restricted_list(d,h) if m%z[3]==0}
            direct=direct_list(d,m)
            assert restricted==direct,(d,m,restricted,direct)
            for a,b,c,s in direct:
                U=a+2*b
                assert kernel_plus(d)*h*h%U==0
                A,B=max(a,b),min(a,b)
                q=2*c-2*A-B
                assert q>0 and 3*B*B==q*(4*A+2*B+q)
                M=3*(A//B+2)
                constant=8 if d==1 else 6
                assert s*M < 2*constant*d*h**3
            checks+=1
    class38=restricted_list(38,1)
    class110=restricted_list(110,1)
    assert not class38
    assert class110=={(8,7,13,3)}
    # Even total multiplier m does not force even coefficient multiplier s.
    # Omitting the factor 2 in d_+ here would incorrectly lose this witness.
    assert kernel_plus(110)==22
    assert direct_list(110,6)=={(8,7,13,3)}
    assert {z for z in restricted_list(110,split_part(6)) if 6%z[3]==0}==direct_list(110,6)
    # General square classes also require even s to remain in the list.
    assert (5,3,7,2) in direct_list(66,2)
    assert (5,3,7,2) in restricted_list(66,1)
    return {'status':'PASS',
            'scope':'Arithmetic checks only; no scale-one geometry claim',
            'independent_comparisons':checks,
            'includes_odd_and_even_kernels_and_multipliers':True,
            'even_multiplier_odd_coefficient_regression':sorted(direct_list(110,6)),
            'even_coefficient_multiplier_regression':[5,3,7,2],
            'class38_split_part_one':sorted(class38),
            'class110_split_part_one':sorted(class110),
            'full_Erdos634_solved':False,
            'passed':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,help='write the arithmetic-check report here')
    args=parser.parse_args()
    output=json.dumps(check(),indent=2)+'\n'
    if args.report is not None:
        args.report.write_text(output)
    print(output,end='')
