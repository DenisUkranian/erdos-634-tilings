#!/usr/bin/env python3
"""Reproduce finite regression evidence for the universal proofs in PROOF.md."""
from __future__ import annotations
import argparse
import copy
import json
import time
from itertools import product
from math import gcd,isqrt
from pathlib import Path
from arithmetic_sectors import factor, square_decomposition, legendre, alpha_local_partitions, qp_representations, solve
from generate_macro import generate
from verify_macro import verify
from check_expanded import expand_and_check
from elliptic_witness import verify_witness


def ensure(ok,msg):
    if not ok:raise AssertionError(msg)


def check_factorization(bound=20000):
    spf=list(range(bound+1))
    for p in range(2,isqrt(bound)+1):
        if spf[p]==p:
            for n in range(p*p,bound+1,p):
                if spf[n]==n:spf[n]=p
    for n in range(1,bound+1):
        m=n;ref={}
        while m>1:
            p=spf[m];ref[p]=ref.get(p,0)+1;m//=p
        ensure(factor(n)==ref,'Trial factorization/SPF mismatch')
        k,m=square_decomposition(n)
        ensure(k*m*m==n and all(e==1 for e in factor(k).values()),'Wrong square decomposition')
    return {'integers_checked':bound,'status':'PASS'}


def check_residues():
    g1={
        'W':lambda u,v:2*v*v-u*u,
        'beta':lambda u,v:3*v*v-u*u,
        'theta':lambda u,v:v*v-u*u,
        'alpha':lambda u,v:(v*v-u*u)*(2*v*v-u*u),
        'QP':lambda u,v:(2*v*v-u*u)*(3*v*v-u*u),
    }
    out={}
    for name,f in g1.items():
        out[name]=sorted({(f(u,v)*t*t)%16 for u,v in product(range(16),repeat=2)
                          if u%2 or v%2 for t in range(1,16,2)})
    ensure(set(out['W'])&{6,14}=={14},'W residue failure')
    ensure(set(out['alpha'])&{6,14}=={6},'Alpha residue failure')
    ensure(set(out['QP'])&{6,14}=={6},'QP residue failure')
    ensure(not ((set(out['theta'])|set(out['beta']))&{6,14}),'Theta/beta residue failure')
    sq={k*k%16 for k in range(16)}
    norm={
        'equi':lambda a,b:a*b,
        'F1':lambda a,b:b*(a+b),
        'iso':lambda a,b:b*(a+2*b),
        'F2':lambda a,b:(a+2*b)*(2*a+b),
        'F3':lambda a,b:3*(a+2*b)*(a+b),
        'F4':lambda a,b:(2*a+b)*(a+b),
    }
    for sign in (1,-1):
        for name,f in norm.items():
            if sign==-1 and name!='equi':continue
            residues={(f(a,b)*t*t)%16 for a,b in product(range(16),repeat=2)
                      if (a%2 or b%2) and (a*a+sign*a*b+b*b)%16 in sq for t in range(1,16,2)}
            out[str(sign)+'_'+name]=sorted(residues)
            if name!='F3':ensure(not residues&{6,14},'Norm-family residue failure')
            else:ensure(residues&{6,14}=={6,14},'F3 accounting failure')
    classical={(r*r+s*s)%16 for r,s in product(range(16),repeat=2)}
    classical|={(2*r*r)%16 for r in range(16)}
    ensure(not classical&{6,14},'Classical residue failure')
    return {'status':'PASS','modulus':16,'odd_square_multipliers_included':True,'residue_sets':out,
            'F3_note':'F3 always divisible by 3, and therefore outside the 3-coprime sector'}


def check_direct_qp(bound=30000):
    reference={}
    # Independent bounded parameter enumeration, without using factor pairs.
    for v in range(2,isqrt(isqrt(bound))+3):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            q,p=2*v*v-u*u,3*v*v-u*u
            d=q*p
            for t in range(1,isqrt(bound//d)+1):
                reference.setdefault(d*t*t,set()).add((u,v,t))
    tested=0;no=0;yes=0;outside=0
    values=set(reference)
    values.update(n for n in range(1,bound+1) if n%16 in (6,14) and n%3)
    for n in sorted(values):
        actual,_=qp_representations(n)
        got={(x['u'],x['v'],x['t']) for x in actual}
        ensure(got==reference.get(n,set()),'Factor criterion/direct parameter mismatch')
        tested+=1
        if n%16 in (6,14) and n%3:
            answer=solve(n)
            if answer['status']=='YES':
                ensure(bool(got),'YES without a construction');yes+=1
            elif answer['status']=='NO':
                ensure(not got,'False negative against direct construction');no+=1
            else:outside+=1
    return {'status':'PASS','N_bound':bound,'N_values_checked':tested,'direct_QP_counts':len(reference),
            'sector_YES':yes,'sector_NO':no,'sector_NOT_COVERED':outside}


def check_partitions(max_v=100):
    alpha=0;w=0;qp=0;parameters=0
    for v in range(2,max_v+1):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            parameters+=1
            b=v*v-u*u;Q=2*v*v-u*u;P=3*v*v-u*u
            n=b*Q
            if n%16==6 and n%3:
                k,_=square_decomposition(n);D=k//2
                kb,_=square_decomposition(b);kq,_=square_decomposition(Q)
                ensure({'A':kq//2,'B':kb} in alpha_local_partitions(D),'A genuine alpha arithmetic candidate was locally excluded')
                alpha+=1
            if Q%16==14 and Q%3:
                k,_=square_decomposition(Q)
                ensure(all(legendre(2,p)==1 for p in factor(k) if p!=2),'W inert-prime contradiction')
                w+=1
            if Q*P%16==6 and Q*P%3:
                for x in factor(P):
                    if x not in (2,3):ensure(legendre(3,x)==1,'QP quadratic character failure')
                qp+=1
    return {'status':'PASS','primitive_pairs':parameters,'max_v':max_v,'alpha_partitions_checked':alpha,
            'W_characters_checked':w,'QP_P_characters_checked':qp}


def check_forbidden(max_p=500,max_m=49):
    checks=0;ps=[]
    for p in range(19,max_p+1,24):
        if factor(p)!={p:1}:continue
        ps.append(p)
        for m in range(1,max_m+1):
            if gcd(m,6)!=1:continue
            n=2*p*m*m
            ensure(solve(n)['status']=='NO','Violation of the inert-2/inert-3 family')
            checks+=1
    return {'status':'PASS','prime_bound':max_p,'multiplier_bound':max_m,'primes':ps,'instances_checked':checks,
            'scope':'Regression only; the unrestricted prime/multiplier statement is proved in PROOF.md'}


def check_conic_and_growth(side_bound=150):
    brute=set()
    for a in range(1,side_bound+1):
        for b in range(1,side_bound+1):
            if gcd(a,b)!=1:continue
            c=isqrt(a*a+a*b+b*b)
            if c*c==a*a+a*b+b*b:brute.add((a,b,c))
    max_c=isqrt(3*side_bound*side_bound)+1
    parameter=set();inequalities=0
    for k in range(2,2*isqrt(max_c)+3):
        for h in range(k//2+1,k):
            if gcd(h,k)!=1:continue
            A=k*k-h*h;B=k*(2*h-k);C=h*h-h*k+k*k;g=gcd(A,B)
            ensure(g in (1,3) and C%g==0,'Conic gcd bound failure')
            a,b,c=A//g,B//g,C//g
            ensure(c*c==a*a+a*b+b*b and gcd(a,b)==1,'Conic identity failure')
            delta,epsilon=k-h,2*h-k
            ensure(27*a*b>=min(delta,epsilon)*k**3,'Sparse counting inequality failure')
            inequalities+=1
            if a<=side_bound and b<=side_bound:parameter.add((a,b,c))
    ensure(parameter==brute,'Conic parametrization misses a primitive triple')
    g1=0
    for v in range(2,151):
        for u in range(1,v):
            b=v*v-u*u;Q=2*v*v-u*u;P=3*v*v-u*u
            ensure(b*Q >= (v-u)*v**3 and Q*P>2*v**4,'Group-1 sparse bound failure');g1+=1
    return {'status':'PASS','primitive_plus_triples_checked':len(brute),'side_bound':side_bound,
            'conic_growth_instances':inequalities,'G1_growth_instances':g1}


def check_difference_envelope(bound=100000, coefficient_bound=1000):
    # Enumerate primitive (u,v) directly; b=(v-u)(v+u) bounds v by (b+1)/2.
    brute=set()
    for v in range(2,(coefficient_bound+1)//2+1):
        for u in range(1,v):
            b=v*v-u*u
            if b<=coefficient_bound and gcd(u,v)==1:brute.add(b)
    expected={b for b in range(1,coefficient_bound+1) if (b>=3 and b%2) or b%8==0}
    ensure(brute==expected,'Primitive difference-coefficient classification failed')
    envelope=bytearray(bound+1)
    for t in range(2,isqrt(bound//3)+1):
        for b in range(3,bound//(t*t)+1,2):envelope[t*t*b]=1
        for b in range(8,bound//(t*t)+1,8):envelope[t*t*b]=1
    # Independent squarefree sieve and prime sieve for the complement identity.
    sf=bytearray([1])*(bound+1)
    prime=bytearray([1])*(bound+1);prime[0:2]=bytes([0,0])
    for p in range(2,isqrt(bound)+1):
        if prime[p]:
            for k in range(p*p,bound+1,p):prime[k]=0
            for k in range(p*p,bound+1,p*p):sf[k]=0
    for n in range(1,bound+1):
        U=(n%2==1 and bool(sf[n])) or n%4==2 or (n%16==8 and bool(sf[n//8]))
        r=isqrt(n)
        odd_prime_square=(r*r==n and r%2==1 and bool(prime[r]))
        ensure(bool(envelope[n])==not_in_complement(U,odd_prime_square,n),'Arithmetic envelope complement identity failed')
    return {'status':'PASS','coefficient_bound':coefficient_bound,'primitive_coefficients':len(brute),
            'envelope_bound':bound,'envelope_elements':sum(envelope),
            'density_formula':'3/4 - 9/(2*pi^2)',
            'scope':'Arithmetic envelope only; its membership is not sufficient for a geometric tiling'}


def not_in_complement(U,odd_prime_square,n):
    return not (U or odd_prime_square or n in (4,16))


def check_geometry(max_v=30):
    pairs=0;certificates=0;macro_pairs=0
    for v in range(2,max_v+1):
        for u in range(1,v):
            if gcd(u,v)!=1:continue
            pairs+=1
            for t in (1,2):
                r=verify(generate(u,v,t));certificates+=1;macro_pairs+=r['macro_pairs_checked']
    big=verify(generate(10132,22779))
    sample=generate(4,5)
    mutants=[]
    def mutate(fn):
        x=copy.deepcopy(sample);fn(x);mutants.append(x)
    mutate(lambda x:x.update(tile_count=x['tile_count']+1))
    mutate(lambda x:x.update(metric_D=x['metric_D']+1))
    mutate(lambda x:x['tile_sides'].__setitem__(0,x['tile_sides'][0]+1))
    mutate(lambda x:x['blocks'][0].update(subdivision=10))
    mutate(lambda x:x['blocks'][-1].update(rows=10))
    mutate(lambda x:x['blocks'][-1].update(columns=17))
    mutate(lambda x:x['blocks'][-1].update(diagonal='sum'))
    mutate(lambda x:x['blocks'].pop())
    mutate(lambda x:x['blocks'].__setitem__(1,copy.deepcopy(x['blocks'][0])))
    mutate(lambda x:x['points']['H'][0].__setitem__(0,x['points']['H'][0][0]+1))
    mutate(lambda x:x.update(scale=2))
    mutate(lambda x:x['blocks'][0].update(type='unknown'))
    rejected=0
    for x in mutants:
        try:verify(x)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):rejected+=1
        else:raise AssertionError('Invalid macro certificate accepted')
    return {'status':'PASS','primitive_pairs':pairs,'max_v':max_v,'macro_certificates':certificates,
            'macro_pairs_checked':macro_pairs,'invalid_mutations_rejected':rejected,
            'large_squareclass_22_certificate':big}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default='verification.json')
    args=parser.parse_args();started=time.monotonic();report={'date':'2026-10-01','status':'PASS','universal_proofs_in':'PROOF.md',
        'limitations':['No full classification of Erdos 634','No novelty or external review claim','No expansion of the enormous certificate']}
    jobs=[('factorization',check_factorization),('residues',check_residues),('direct_QP_comparison',check_direct_qp),
          ('partition_regression',check_partitions),('forbidden_family',check_forbidden),
          ('sparse_counting_regression',check_conic_and_growth),('difference_envelope',check_difference_envelope),('macro_geometry',check_geometry),
          ('expanded_2006',lambda:expand_and_check(generate(4,5))),('elliptic_witness',verify_witness)]
    for name,job in jobs:
        report[name]=job();print(name, 'PASS',flush=True)
    report['elapsed_seconds']=round(time.monotonic()-started,3)
    with open(args.output,'w',encoding='utf-8') as h:json.dump(report,h,indent=2,sort_keys=True);h.write('\n')
    print(json.dumps({'status':report['status'],'elapsed_seconds':report['elapsed_seconds'],'output':args.output},indent=2))
if __name__=='__main__':main()
