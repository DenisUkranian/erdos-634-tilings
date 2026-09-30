#!/usr/bin/env python3
"""Exhaustive NECESSARY arithmetic reduction for if not __debug__:raise RuntimeError("Run without -O or PYTHONOPTIMIZE; arithmetic assertions are required.")
N=105, not a tiling search.
The explicit finite bounds and the complete shape list are justified in
PROOF_N105.md. This script does not certify those published/human theorems.
Only the Python standard library is required; all arithmetic is exact.
"""
from fractions import Fraction as F
from math import gcd,isqrt
from pathlib import Path
import json
N=105

def square(n):return n>=0 and isqrt(n)**2==n

def divisors(n):return [d for d in range(1,n+1) if n%d==0]

def norm120(a,b):
    n=a*a+a*b+b*b
    return isqrt(n) if square(n) else None

def run():
    D=divisors(N)
    pairs=[(s,3*N//s) for s in divisors(3*N) if s<=3*N//s]
    eq120=[];eq60=[];targets60=[]
    for s,t in pairs:
        rad=(t-s)**2+16*N
        eq120.append({'s':s,'t':t,'radicand':rad,'square':square(rad)})
        if s*s<N:
            rad=(t-s)**2-4*N
            row={'s':s,'t':t,'radicand':rad,'square':square(rad)}
            eq60.append(row)
            if square(rad):
                q=isqrt(rad);aa=s+t+q;bb=s+t-q;d=gcd(aa,bb)
                a,b=aa//d,bb//d;c2=a*a-a*b+b*b
                assert square(c2) and square(N*a*b)
                c=isqrt(c2);S=isqrt(N*a*b)
                targets60.append({'tile':sorted([a,b,c]),'target':[S,S,S],
                                  'incident_60_edges':[a,b], 'flux_pair':[s,t]})
    assert not any(r['square'] for r in eq120)
    assert [r['tile'] for r in targets60]==[[5,19,21],[7,13,15]]

    f1=[];f1_norm_candidates=[];iso120=[]
    for d in D:
        # F1: d=a+b divides N. Thus this loop has no arbitrary side cutoff.
        for b in range(1,d):
            a=d-b
            if gcd(a,b)!=1:continue
            c=norm120(a,b)
            if c is None:continue
            f1_norm_candidates.append([a,b,c])
            m2=(N//d)*b
            if square(m2):
                lam=isqrt(m2)
                f1.append({'a':a,'b':b,'c':c,'lambda':lam,
                           'tile':sorted([a,b,c]),'target':sorted([lam*a,lam*c,lam*(a+b)])})
        # Isosceles 120: d=a+2b divides N.
        for b in range(1,(d-1)//2+1):
            a=d-2*b
            if gcd(a,b)!=1:continue
            c=norm120(a,b)
            if c is not None and square((N//d)*b):iso120.append([a,b,c,isqrt((N//d)*b)])
    assert [(r['a'],r['b'],r['c'],r['lambda']) for r in f1]==[(8,7,13,7),(16,5,19,5)]
    assert iso120==[]

    other120={};other120_trials={}
    for shape,mult in [('alpha_2alpha_3beta',3),('alpha_2beta_2alpha_beta',1),('2alpha_2beta_60',1)]:
        solutions=[];trials=[]
        # N is squarefree; the integral scale in these three shapes equals one.
        if N%mult:continue
        M=N//mult
        for x in divisors(M):
            y=M//x
            if shape=='alpha_2alpha_3beta':a,b=2*x-y,y-x
            elif shape=='alpha_2beta_2alpha_beta':a,b=y-x,2*x-y
            else:
                if (2*y-x)%3 or (2*x-y)%3:continue
                a,b=(2*y-x)//3,(2*x-y)//3
            if min(a,b)<=0 or gcd(a,b)!=1:continue
            trials.append([a,b,a*a+a*b+b*b])
            c=norm120(a,b)
            if c is not None:solutions.append([a,b,c])
        other120[shape]=solutions;other120_trials[shape]=trials
    assert all(not r for r in other120.values())

    group1={'W':[],'beta_isosceles':[],'other_scalene':[],'alpha_isosceles':[]}
    alpha_trials=[];parameter_trials=0
    # In all these cases Q=2v^2-u^2 > v^2 is <=N, hence v<=sqrt(N-1).
    for v in range(2,isqrt(N-1)+1):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            parameter_trials+=1;b=v*v-u*u;Q=2*v*v-u*u;P=3*v*v-u*u
            for name,k in [('W',Q),('beta_isosceles',P),('other_scalene',P*Q)]:
                if N%k==0 and square(N//k):group1[name].append([u,v,isqrt(N//k)])
            # Do NOT strengthen kappa^2=N*b/Q to N=b*Q*T^2.
            # The weaker exact arithmetic remains valid even if b is nonsquarefree.
            if N%Q==0:
                k2=(N//Q)*b;alpha_trials.append({'u':u,'v':v,'b':b,'Q':Q,'kappa_squared':k2})
                if square(k2):group1['alpha_isosceles'].append([u,v,isqrt(k2)])
    assert all(not r for r in group1.values())
    assert alpha_trials==[{'u':1,'v':2,'b':3,'Q':7,'kappa_squared':45}]
    assert not square(N) and not square(N//3) and N%2==1
    assert not any(x*x+y*y==N for x in range(isqrt(N)+1) for y in range(isqrt(N)+1))
    remaining=[*targets60,*f1]
    return {
        'result':'PASS_EXHAUSTIVE_NECESSARY_ARITHMETIC_REDUCTION','N':N,
        'divisors_N':D,'equilateral_120':eq120,'equilateral_60':eq60,
        'equilateral_60_targets':targets60,'F1_norm_candidates_before_scale':f1_norm_candidates,
        'F1_targets':f1,'isosceles_120_candidates':iso120,
        'other_120_candidates':other120,'other_120_positive_parameter_trials':other120_trials,
        'group1_parameter_pairs_checked':parameter_trials,'group1_candidates':group1,
        'alpha_group1_trials':alpha_trials,
        'theta_group1':'Excluded for squarefree N by the written boundary proof.',
        'gamma_2alpha':'Excluded for squarefree N by the written boundary proof (Beeson Theorem 11.7).',
        'shape_classification_and_rationality':'Published dependencies, not computationally certified here.',
        'remaining_fixed_targets':remaining,'remaining_fixed_target_count':len(remaining),
        'scope':'Necessary reduction only; the four fixed-target certificates and written lemmas supply exclusion.'}

if __name__=='__main__':
    result=run();out=Path(__file__).resolve().parent/'verification/arithmetic.json';out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
