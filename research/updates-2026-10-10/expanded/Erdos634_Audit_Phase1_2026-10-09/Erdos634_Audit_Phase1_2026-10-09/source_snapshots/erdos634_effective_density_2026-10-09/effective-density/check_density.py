#!/usr/bin/env python3
"""Exact arithmetic for the all-branch fixed-square-class density theorem.

No tiling decision is inferred from a primitive coefficient.  This file checks
finite algebra and supplies exact lower approximations to the limiting density.
The infinite theorem and the meaning of its error bound are in PROOF.md.
Only the Python standard library is used.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt, lcm
from pathlib import Path
import json

ROWS = ('alpha', 'QP', 'E60', 'E120', 'F1', 'I120', 'F2', 'F3', 'F4')

@lru_cache(maxsize=150000)
def factor(n: int) -> tuple[tuple[int, int], ...]:
    if n < 1:
        raise ValueError('factor expects a positive integer')
    out = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p,e))
        p = 3 if p == 2 else p + 2
    if n > 1:
        out.append((n,1))
    return tuple(out)

def divs_from_factor(fac: tuple[tuple[int,int], ...]) -> list[int]:
    result = [1]
    for p,e in fac:
        result = [x * p**j for x in result for j in range(e+1)]
    return sorted(result)

def divisors(n: int) -> list[int]:
    return divs_from_factor(factor(n))

def tau(n: int) -> int:
    ans = 1
    for _,e in factor(n): ans *= e+1
    return ans

def square_root(n: int) -> int | None:
    if n < 0: return None
    r = isqrt(n)
    return r if r*r == n else None

def square_class(n: int) -> tuple[int,int]:
    d,s = 1,1
    for p,e in factor(n):
        d *= p**(e%2)
        s *= p**(e//2)
    return d,s

@dataclass(frozen=True, order=True)
class Witness:
    row: str
    a: int
    b: int
    c: int
    # For alpha and QP, a=u, b=v, c=0, not triangle side lengths.


def inverse_witnesses(D: int, divs: list[int] | None = None) -> tuple[Witness,...]:
    if D < 1: raise ValueError('D must be positive')
    if divs is None: divs = divisors(D)
    out: set[Witness] = set()
    def norm(row: str, a: int, b: int, sign: int = 1) -> None:
        if a <= 0 or b <= 0 or gcd(a,b) != 1: return
        c = square_root(a*a + sign*a*b + b*b)
        if c is not None and c > 0:
            out.add(Witness(row,a,b,c))
    def uv(row: str, u2: int, v2: int) -> None:
        u,v = square_root(u2),square_root(v2)
        if u is not None and v is not None and 0 < u < v and gcd(u,v)==1:
            out.add(Witness(row,u,v,0))
    for A in divs:
        B = D//A
        uv('alpha', B-2*A, B-A)
        uv('QP', 2*B-3*A, B-A)
        norm('E60', A,B,-1)
        norm('E120', A,B)
        norm('F1', B-A,A)
        norm('I120', B-2*A,A)
        if (2*B-A)%3==0 and (2*A-B)%3==0:
            norm('F2', (2*B-A)//3,(2*A-B)//3)
        norm('F4', B-A,2*A-B)
    if D%3==0:
        M = D//3
        for A in divs:
            if M%A==0:
                B=M//A
                norm('F3',2*A-B,B-A)
    return tuple(sorted(out))


def coefficient(w: Witness) -> int:
    a,b=w.a,w.b
    if w.row in ('alpha','QP'):
        u,v=a,b
        q,p=2*v*v-u*u,3*v*v-u*u
        return (v*v-u*u)*q if w.row=='alpha' else q*p
    return {
        'E60':a*b,'E120':a*b,'F1':b*(a+b),'I120':b*(a+2*b),
        'F2':(a+2*b)*(2*a+b),'F3':3*(a+b)*(a+2*b),
        'F4':(a+b)*(2*a+b),
    }[w.row]


def factors_for_witness(w: Witness) -> tuple[int,int,int]:
    """Return g,L1,L2 with D=g*L1*L2 and gcd(L1,L2)=1."""
    a,b=w.a,w.b
    if w.row in ('alpha','QP'):
        u,v=a,b
        B,Q,P=v*v-u*u,2*v*v-u*u,3*v*v-u*u
        return (1,B,Q) if w.row=='alpha' else (1,Q,P)
    pairs={
        'E60':(1,a,b), 'E120':(1,a,b), 'F1':(1,b,a+b),
        'I120':(1,b,a+2*b), 'F2':(1,a+2*b,2*a+b),
        'F3':(3,a+b,a+2*b), 'F4':(1,a+b,2*a+b)}
    return pairs[w.row]


def easy_cofinal_conditions(d: int) -> dict[str,bool]:
    if square_class(d)[0] != d: raise ValueError('d must be squarefree')
    primes=[p for p,_ in factor(d)]
    classical=d in (1,2,3,6) or all(p%4==1 for p in primes if p!=2)
    w=all(p%8 in (1,7) for p in primes if p!=2)
    beta=(all(p%12 in (1,11) for p in primes if p>3)
          and (d%3==2 if d%3 else (d//3)%3==1))
    return {'odd_kernel':d%2==1,'classical':classical,'W':w,'beta':beta}


def effective_constant(d: int) -> int:
    h=3*d//gcd(3,d)**2
    return 32*tau(d)*tau(3*d*d)+4*tau(h)*tau(3*h*h)


def tail_bound_dyadic(d: int, j: int) -> Fraction:
    """Certified rational upper bound for sum_{s>2^(2j)}1/s.

    ln(2)<1 gives 1+ln(sqrt(K)) < 1+j.  No floating point
    value is used as a certified bound.
    """
    if j < 0: raise ValueError('j must be nonnegative')
    t=1+j
    P=t**4+4*t**3+12*t*t+24*t+24
    return Fraction(2*effective_constant(d)*P,2**j)


def precision_plan(d: int, epsilon: Fraction) -> dict:
    """Give a terminating cutoff plan; do not silently execute a huge search."""
    if epsilon <= 0: raise ValueError('epsilon must be positive')
    easy=easy_cofinal_conditions(d)
    if any(easy.values()) or inverse_witnesses(d):
        return {'density': '1', 'reason': 'Existing finite cofinal test succeeds.'}
    j=0
    while tail_bound_dyadic(d,j) >= epsilon: j+=1
    return {'d':d, 'epsilon':str(epsilon), 'j':j, 'K':2**(2*j),
            'certified_odd_density_tail_bound':str(tail_bound_dyadic(d,j)),
            'warning':'This is a cutoff plan, not execution of the coefficient enumeration to K.'}


def minimal_generators(B: list[int]) -> list[int]:
    result=[]
    for s in sorted(set(B)):
        if not any(s%a==0 for a in result): result.append(s)
    return result


def finite_union_density(B: list[int]) -> Fraction:
    """CRT/inclusion-exclusion density, relative to odd integers for odd B."""
    coeff: dict[int,int]={}
    for s in minimal_generators(B):
        delta=Counter({s:1})
        for k,v in coeff.items(): delta[lcm(k,s)] -= v
        for k,v in delta.items():
            coeff[k]=coeff.get(k,0)+v
            if not coeff[k]: del coeff[k]
    return sum((Fraction(v,k) for k,v in coeff.items()),Fraction(0))


def coefficient_list(d: int, K: int) -> dict[int,tuple[Witness,...]]:
    if d < 1 or square_class(d)[0]!=d: raise ValueError('positive squarefree d required')
    out={}
    fd=dict(factor(d))
    for s in range(1,K+1,2):
        f=fd.copy()
        for p,e in factor(s): f[p]=f.get(p,0)+2*e
        ds=divs_from_factor(tuple(sorted(f.items())))
        found=inverse_witnesses(d*s*s,ds)
        if found: out[s]=found
    return out


def check_fixed_factor_counts(max_L: int) -> dict[str,int]:
    """Complete, not box-truncated, tests of the fixed-factor estimates."""
    tested=Counter()
    for L in range(1,max_L+1):
        # Difference of squares, and compact Pell sectors Q and P.
        nb=0
        for r in divisors(L):
            z=L//r
            if z>r and (z+r)%2==0:
                nb+=1
        assert nb<=tau(L)
        tested['difference_of_squares']+=1
        for q in (2,3):
            count=0
            # q v^2-u^2=L with 0<u<v implies v^2<L/(q-1).
            for v in range(2,isqrt(L//(q-1))+1):
                u=square_root(q*v*v-L)
                if u is not None and 0<u<v: count+=1
            assert count<=tau(L),(q,L,count,tau(L))
            tested[f'Pell_{q}']+=1
        for sign in (-1,1):
            # Enumerate ALL possibilities using positive divisor factors,
            # including those with the other side larger than max_L.
            found=set()
            for p in divisors(3*L*L):
                q=3*L*L//p
                if (p+q)%4: continue
                c=(p+q)//4
                num=q-p-2*sign*L
                if num%4: continue
                A=num//4
                if A>0 and c*c==A*A+sign*A*L+L*L: found.add((A,c))
            assert len(found)<=tau(3*L*L)
            tested[f'fixed_side_sign_{sign}']+=1
        # A+B=L and A+2B=L are bounded ranges, so direct enumeration is complete.
        count1=sum(square_root(a*a+a*(L-a)+(L-a)**2) is not None for a in range(1,L))
        count2=sum(square_root((L-2*b)**2+(L-2*b)*b+b*b) is not None for b in range(1,(L+1)//2))
        assert count1<=tau(3*L*L),(L,count1)
        assert count2<=tau(L*L),(L,count2)
        tested['fixed_sum']+=1;tested['fixed_weighted_sum']+=1
    return dict(tested)


def regression(max_uv: int, max_side: int) -> dict:
    stats=Counter()
    all_w=[]
    for v in range(2,max_uv+1):
        for u in range(1,v):
            if gcd(u,v)>1: continue
            for row in ('alpha','QP'): all_w.append(Witness(row,u,v,0))
    for a in range(1,max_side+1):
        for b in range(1,max_side+1):
            if gcd(a,b)>1: continue
            for sign,rows in [(-1,('E60',)),(1,('E120','F1','I120','F2','F3','F4'))]:
                c=square_root(a*a+sign*a*b+b*b)
                if c is not None:
                    all_w.extend(Witness(row,a,b,c) for row in rows)
    for w in all_w:
        D=coefficient(w)
        assert w in inverse_witnesses(D),(w,D)
        if w.row not in ('alpha','QP'):
            a,b,c=w.a,w.b,w.c
            sign=-1 if w.row=='E60' else 1
            assert (2*c-2*a-sign*b)*(2*c+2*a+sign*b)==3*b*b
            if sign==1:
                assert (2*c-(a-b))*(2*c+(a-b))==3*(a+b)**2
                assert 4*c*c-3*a*a==(a+2*b)**2
                assert 4*c*c-3*b*b==(2*a+b)**2
        g,L1,L2=factors_for_witness(w)
        assert g*L1*L2==D and gcd(L1,L2)==1,(w,L1,L2)
        d,s=square_class(D)
        if g==3:
            h=3*d//gcd(3,d)**2
            f=1 if d%3==0 else 3
            assert s%f==0
            k=s//f
        else: h,k=d,s
        d1,x=square_class(L1);d2,y=square_class(L2)
        assert d1*d2==h and x*y==k and min(x,y)<=isqrt(k)
        assert tau(3*(d1*x*x)**2)<=tau(3*h*h)*tau(x**4)
        stats[w.row]+=1
    # Several independently counted CRT periods and the association inequality.
    lists=[[3],[3,5],[9,15,21],[15,21,35],[3,9,15],[5,7,9,11],[1]]
    for B in lists:
        period=lcm(*B)
        direct=Fraction(sum(any(n%b==0 for b in B) for n in range(period)),period)
        calc=finite_union_density(B)
        assert direct==calc,(B,direct,calc)
        prod=Fraction(1)
        for b in set(B): prod*=Fraction(b-1,b)
        assert 1-calc>=prod,(B,calc,prod)
    # Local divisor majorant tau(z^4)<=d_5(z) and its summation.
    from math import comb
    for z in range(1,3001):
        dt=1
        for _,e in factor(z): dt*=comb(e+4,4)
        assert tau(z**4)<=dt
    return {'forward_inverse_witnesses':dict(stats),
            'total_forward_inverse_witnesses':len(all_w),
            'exact_period_tests':len(lists),'divisor_majorant_tests':3000,
            'fixed_factor_counts':check_fixed_factor_counts(300)}


def main() -> None:
    if not __debug__: raise RuntimeError('Do not use Python -O; assertions are part of the finite checks.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=3000)
    parser.add_argument('--classes',type=int,nargs='+',default=[22,38,78,110,1302])
    parser.add_argument('--max-uv',type=int,default=40)
    parser.add_argument('--max-side',type=int,default=220)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.limit<1: parser.error('--limit must be positive')
    report={'scope':'Exact arithmetic regressions; not an exhaustive geometric tiling decision.',
            'regression':regression(args.max_uv,args.max_side),'classes':{}}
    for d in args.classes:
        data=coefficient_list(d,args.limit)
        B=list(data);basis=minimal_generators(B)
        rho=finite_union_density(B)
        report['classes'][str(d)]={
            'K':args.limit,'easy_cofinal':easy_cofinal_conditions(d),
            'primitive_odd_coefficient_multipliers':B,'minimal_finite_generators':basis,
            'finite_odd_relative_density':str(rho),
            'decimal_for_orientation_only':float(rho),
            'effective_constant_Cd':effective_constant(d),
            'witnesses':{str(s):[asdict(w) for w in ws] for s,ws in data.items()},
            'warning':'Finite density is a lower approximation to the limiting odd density in the non-cofinal even case. It is not an exact density or proof of small-scale realizability.'}
    text=json.dumps(report,indent=2,ensure_ascii=False)
    if args.output: args.output.write_text(text+'\n',encoding='utf-8')
    print(text)

if __name__=='__main__': main()
