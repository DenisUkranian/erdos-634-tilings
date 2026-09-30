#!/usr/bin/env python3
"""Independent parameter sweep and exhaustive modular checks.

Finite checks supplement the proofs in PROOF.md. They do not infer universal
claims by testing a finite interval. No nonexistence of W/beta m=1 is assumed.
"""
from math import gcd,isqrt
from fractions import Fraction as F
from collections import defaultdict,Counter
from pathlib import Path
import json,time
from candidates import enumerate_candidates,classical,heron16

def require(x,msg):
    if not x:raise ValueError(msg)

def key(i):return (i.branch,tuple(sorted(i.tile)),tuple(sorted(i.target)))

def brute_sweep(B):
    """Enumerate bounded side/parameter boxes directly, NOT by factor pairs."""
    out=defaultdict(set);parameter_trials=0;area_checks=0
    def emit(branch,tile,target,coefficient,min_t=1):
        nonlocal area_checks
        if not 1<=coefficient<=B:return
        require(heron16(target)==coefficient*coefficient*heron16(tile),('area',branch,tile,target))
        area_checks+=1
        for t in range(min_t,isqrt(B//coefficient)+1):
            out[coefficient*t*t].add((branch,tuple(sorted(tile)),tuple(sorted(t*s for s in target))))
    for v in range(2,(B+1)//2+1):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            parameter_trials+=1
            b=v*v-u*u;a=u*v;c=v*v;Q=b+c;P=b+2*c
            emit('G1-theta',(a,b,c),(b*v,b*v,b*u),b,2)
            if v<2*u:emit('double-angle',(u*u,b,u*v),(b*u,b*u,b*v),b,2)
            emit('G1-W',(a,b,c),(v**3,u*Q,v*b),Q)
            emit('G1-beta',(a,b,c),(v**3,v**3,u*P),P)
            emit('G1-alpha',(a,b,c),(b*c,b*c,b*Q),b*Q)
            emit('G1-other-scalene',(a,b,c),(c*c,c*Q,b*P),Q*P)
    for a in range(1,B+1):
        for b in range(1,B+1):
            if gcd(a,b)!=1:continue
            parameter_trials+=1
            for sign,branch in ((-1,'E60'),(1,'E120')):
                z=a*a+sign*a*b+b*b;c=isqrt(z)
                if c*c!=z:continue
                if min(a,b)>1:emit(branch,(a,b,c),(a*b,a*b,a*b),a*b)
                if sign<0:continue
                tile=(a,b,c)
                emit('F1-120',tile,(a*b,b*c,b*(a+b)),b*(a+b))
                emit('I120',tile,(b*c,b*c,b*(a+2*b)),b*(a+2*b))
                emit('F3-120',tile,(c*c,c*(a+2*b),3*b*(a+b)),3*(a+2*b)*(a+b))
                emit('F4-120',tile,(a*c,b*(2*a+b),c*(a+b)),(2*a+b)*(a+b))
                emit('F2-120',tile,(a*(a+2*b),b*(2*a+b),c*c),(a+2*b)*(2*a+b))
    count=0
    for n in range(1,B+1):
        got={key(x) for x in enumerate_candidates(n)}
        require(got==out[n],('candidate mismatch',n,got-out[n],out[n]-got))
        count+=len(got)
    return {'upper_N':B,'parameter_trials':parameter_trials,'primitive_shape_area_identities_checked':area_checks,'candidate_instances_compared':count,'status':'PASS'}

def modular_tables(M=8):
    sq={i*i%M for i in range(M)}
    g={k:set() for k in ('W','beta','alpha','other-scalene')}
    s={k:set() for k in ('E60','E120','F1','I120','F3','F4','F2')}
    for u in range(M):
        for v in range(M):
            if gcd(gcd(u,v),M)!=1:continue
            b=v*v-u*u;Q=2*v*v-u*u;P=3*v*v-u*u
            for k,z in [('W',Q),('beta',P),('alpha',b*Q),('other-scalene',Q*P)]:g[k].add(z%M)
    for a in range(M):
        for b in range(M):
            if gcd(gcd(a,b),M)!=1:continue
            for sign,k in [(-1,'E60'),(1,'E120')]:
                if (a*a+sign*a*b+b*b)%M not in sq:continue
                s[k].add(a*b%M)
                if sign<0:continue
                for j,z in [('F1',b*(a+b)),('I120',b*(a+2*b)),('F3',3*(a+2*b)*(a+b)),('F4',(2*a+b)*(a+b)),('F2',(a+2*b)*(2*a+b))]:s[j].add(z%M)
    return {'modulus':M,'Group1':{k:sorted(v) for k,v in g.items()},'norm_families':{k:sorted(v) for k,v in s.items()}}

def squarefree(n):
    return all(n%(p*p) for p in range(2,isqrt(n)+1))

def prime_factors(n):
    out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out

def progression_checks(B=6000):
    n19=n35=nlocal=0;examples19=[];examples35=[]
    for n in range(1,B+1):
        if n%24==19:
            cs=enumerate_candidates(n)
            require(classical(n) is None,('classical',n))
            require(all(x.branch in ('G1-theta','double-angle') and x.multiplier>=5 for x in cs),('19mod24 reduction',n))
            if squarefree(n):
                require(not cs,('squarefree19',n));n19+=1
                if len(prime_factors(n))>1 and len(examples19)<12:examples19.append(n)
        if n%120==35 and squarefree(n):
            require(not enumerate_candidates(n) and classical(n) is None,('squarefree35mod120',n));n35+=1
            if len(examples35)<12:examples35.append(n)
        if n%8==3 and n%3 and squarefree(n):
            cs=enumerate_candidates(n)
            require(all(x.branch=='G1-beta' and x.multiplier==1 for x in cs),('beta only',n))
            bad=any(all(x*x%p!=3%p for x in range(p)) for p in prime_factors(n))
            if bad:require(not cs,('prime local obstruction',n));nlocal+=1
    # Explicit countercheck: removing squarefreeness would be invalid.
    require(any(x.branch=='G1-beta' and x.tile==(2,3,4) and x.multiplier==5 for x in enumerate_candidates(275)), 'Lost the 275 control')
    return {'upper_N':B,'squarefree_19mod24_excluded':n19,'composite_examples_19mod24':examples19,'squarefree_35mod120_excluded':n35,'examples_35mod120':examples35,'local_nonresidue_exclusions':nlocal,'squarefreeness_control_275':'RETAINED','status':'PASS'}

def character_checks(B=150):
    checks=0;strengthening=[]
    for v in range(2,B+1):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            b=v*v-u*u
            for lam in range(1,4*b+1):
                # Both integer values with equal parity, exactly b | lambda.
                U=F(lam,v-u);V=-F(lam,v+u)
                admitted=U.denominator==V.denominator==1 and (U-V)%2==0
                require(admitted==(lam%b==0),('half-difference',u,v,lam))
                if lam%b==0:
                    n=lam*lam//b
                    require((U-n)%2==0 and (V-n)%2==0,('parity',u,v,lam))
                checks+=1
            if v<2*u:
                # A square-ratio candidate killed by both character conditions.
                for lam in range(1,min(b,100)):
                    if lam*lam%b==0 and lam%b and len(strengthening)<8:
                        strengthening.append({'u':u,'v':v,'tile':[u*u,b,u*v],'lambda':lam,'area_count':lam*lam//b,'U':str(-F(lam,u+v)),'V':str(F(lam,v-u))})
    return {'v_bound':B,'lambda_checks':checks,'examples_killed_beyond_area_equation':strengthening,'status':'PASS'}

def main():
    started=time.monotonic()
    # Bounded supplementary tests, chosen for repeatable runtime.
    report={'independent_sweep':brute_sweep(300),'mod8':modular_tables(),'progressions':progression_checks(),
            'characters':character_checks(32),'is_universal_proof':False,'proof_location':'PROOF.md'}
    report['seconds']=round(time.monotonic()-started,4)
    Path(__file__).with_name('reduction_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
