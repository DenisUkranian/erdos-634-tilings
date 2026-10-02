"""Reproduce finite regression. These checks do not replace PROOF.md.
Standard library only. No files are fetched, no code is imported from dependencies.
"""
from __future__ import annotations
import argparse
import copy
import json
from math import gcd, isqrt
from pathlib import Path
from arithmetic import bounds, classify, norm2_test, norm3_test, parameters, plan
from generate import generate
from verify_geometry import check


def require(value, message):
    if not value:
        raise AssertionError(message)


def norm_checks(limit):
    # Independent sieve of prime factors; no calls to arithmetic.factor.
    spf = list(range(limit+1))
    for p in range(2,isqrt(limit)+1):
        if spf[p] == p:
            for k in range(p*p,limit+1,p):
                if spf[k] == k: spf[k] = p
    squarefree=[]
    for d in range(1,limit+1):
        n=d; fs=[]; valid=True
        while n>1:
            p=spf[n];n//=p;fs.append(p)
            if n%p == 0:
                valid=False;break
        if valid: squarefree.append((d,fs))
    # Independent forward quadratic enumeration, including only 0<u<v.
    represented={2:set(),3:set()}; witnesses={2:{},3:{}}
    for v in range(2,isqrt(limit)+1):
        for u in range(1,v):
            if gcd(u,v)!=1: continue
            for k in (2,3):
                d=k*v*v-u*u
                if d<=limit:
                    represented[k].add(d)
                    witnesses[k].setdefault(d,[]).append((u,v))
    matches=0
    for d,fs in squarefree:
        local2=all(p==2 or p%8 in (1,7) for p in fs)
        local3=(all(p<=3 or p%12 in (1,11) for p in fs)
                and ((d%3==2) if 3 not in fs else ((d//3)%3==1)))
        require(norm2_test(d)==local2 and norm3_test(d)==local3,'Norm test implementation')
        require(local2==((d in (1,2)) or d in represented[2]),f'Norm2 equivalence at {d}')
        require(local3==((d in (2,3)) or d in represented[3]),f'Norm3 equivalence at {d}')
        for fam,k in [('W',2),('beta',3)]:
            require(set(parameters(d,fam))==set(witnesses[k].get(d,[])),f'Complete finite parameters {d} {fam}')
            matches+=1
    return dict(max_d=limit,squarefree_kernels=len(squarefree),family_equivalence_checks=matches,
                method='Independent sieve and forward primitive-parameter enumeration')


def threshold_checks(max_v):
    pairs=plans=strip_cases=0
    for v in range(2,max_v+1):
        for u in range(1,v):
            if gcd(u,v)!=1: continue
            pairs+=1;k=bounds(u,v);a,b,c=[k[x] for x in ('a','b','c')]
            require(k['H']<=k['Q'] and k['C']<2*k['Q'],'Uniform bound')
            oldH=(a*a+b*b+(b-1)*(c-1)+u*b-1)//(u*b)
            require(k['H']<=oldH,'New motif threshold no worse than old one')
            for m in range(k['C'],k['C']+2*v+1):
                p=plan(u,v,m)
                require(p['seed_scale']%v==0 and p['seed_scale']>=v,'Seed congruence')
                require(p['seed_scale']+p['steps']*u==m and 0<=p['steps']<v,'Scale sum')
                if p['steps']: require(p['seed_scale']>=k['H'],'Unsafe shell')
                plans+=1
            # Direct coin enumeration near the exact threshold, not its formula.
            if v<=22:
                for T in sorted(set([max(1,k['H']-2),max(1,k['H']-1),k['H'],k['H']+1,k['H']+2])):
                    L=u*b*T-a*a-b*b
                    choices=[]
                    if L>=0:
                        choices=[(L-y*c)//b for y in range(L//c+1) if (L-y*c)%b==0]
                    require(bool(choices)==(T>=k['H']),f'Coin threshold {u,v,T}')
                    strip_cases+=1
    return dict(max_v=max_v,primitive_pairs=pairs,scale_plans=plans,direct_coin_checks=strip_cases)


def geometry_checks(max_v, out):
    cases=regions=pairs=0; max_count=0
    for v in range(2,max_v+1):
        for u in range(1,v):
            if gcd(u,v)!=1: continue
            C=bounds(u,v)['C']
            for family in ('W','beta'):
                for m in sorted(set([v,C,C+1])):
                    report=check(generate(u,v,m,family))
                    cases+=1;regions+=report['macroregions'];pairs+=report['macro_pairs']
                    max_count=max(max_count,report['tile_count'])
    fixtures=[('W14_m11',2,3,11,'W'),('W46_m29',2,5,29,'W'),
              ('W62_m59',6,7,59,'W'),('beta23_m11',2,3,11,'beta'),
              ('W94_m55',2,7,55,'W'),('W142_m157',10,11,157,'W'),('beta122_m53',5,7,53,'beta')]
    example_reports={}
    for name,u,v,m,family in fixtures:
        data=generate(u,v,m,family); result=check(data)
        cases+=1;regions+=result['macroregions'];pairs+=result['macro_pairs']
        max_count=max(max_count,result['tile_count'])
        if out is not None:
            (out/'examples'/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
        example_reports[name]=result | {'u':u,'v':v,'m':m,'family':family}
    base=generate(2,3,11,'W'); corrupt=[]
    c=copy.deepcopy(base);c['tile_count']+=1;corrupt.append(c)
    c=copy.deepcopy(base);c['blocks'][0]['n']+=1;corrupt.append(c)
    c=copy.deepcopy(base);c['blocks'].pop();corrupt.append(c)
    c=copy.deepcopy(base);c['blocks'][0]['vertices'][0][0][0]+=1;corrupt.append(c)
    c=copy.deepcopy(base)
    next(b for b in c['blocks'] if b['type']=='parallelogram_grid')['rows']+=1
    corrupt.append(c)
    c=copy.deepcopy(base)
    next(b for b in c['blocks'] if b['type']=='parallelogram_grid')['diagonal']='sum'
    corrupt.append(c)
    c=copy.deepcopy(base);c['blocks'].append(copy.deepcopy(c['blocks'][0]));corrupt.append(c)
    for bad in corrupt:
        try: check(bad)
        except (ValueError,TypeError,KeyError): pass
        else: raise AssertionError('Corrupt certificate accepted')
    return dict(max_v=max_v,complete_macrocertificates=cases,macroregions_checked=regions,
                macro_pairs_checked=pairs,largest_compressed_tile_count=max_count,
                corrupt_certificates_rejected=len(corrupt),examples=example_reports,
                individual_tiles_expanded=False)


def classifier_checks():
    queries={14:'UNKNOWN',154:'UNKNOWN',1694:'YES',38686:'YES',215822:'YES',2783:'YES',
             110:'NO',13310:'NO',990:'UNKNOWN',1:'YES',2:'YES',3:'YES',6:'YES'}
    records=[]
    for n,status in queries.items():
        result=classify(n)
        require(result['status']==status,f'Expected {status} on {n}: {result}')
        if result['status']=='YES' and 'parameters' in result:
            u,v=result['parameters']; check(generate(u,v,result['multiplier'],result['family']))
        records.append(result)
    rejected=0
    for n in (0,-1,True,1.5,'14'):
        try: classify(n)
        except (ValueError,TypeError): rejected+=1
        else: raise AssertionError('Invalid input accepted')
    return dict(queries=records,invalid_inputs_rejected=rejected,unknown_is_not_nonexistence=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-d',type=int,default=20000)
    parser.add_argument('--max-v',type=int,default=80)
    parser.add_argument('--geometry-max-v',type=int,default=10)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(); root=Path(__file__).resolve().parent
    if args.output is not None: (root/'examples').mkdir(exist_ok=True)
    result={'status':'PASS','scope':'Finite regressions, not proofs of universal statements',
            'norms':norm_checks(args.max_d),'thresholds':threshold_checks(args.max_v),
            'geometry':geometry_checks(args.geometry_max_v,root if args.output else None),
            'classifier':classifier_checks()}
    text=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text)

if __name__=='__main__': main()
