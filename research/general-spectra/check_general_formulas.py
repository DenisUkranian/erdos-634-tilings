#!/usr/bin/env python3
"""Supplementary finite checks; the universal results are proved in PROOF.md.
No finite sample is represented as a proof of an all-parameter statement.
"""
from fractions import Fraction as F
from math import gcd,isqrt
import json
from pathlib import Path
from build_certificate import construct
from verify_certificate import verify


def require(ok,msg):
    if not ok:raise ValueError(msg)
def whole(x):return x.denominator==1
def compatible(u,v,n):
    return whole(u) and whole(v) and whole(n) and (u.numerator-n.numerator)%2==0 and (v.numerator-n.numerator)%2==0

def main():
    rows=[];eqtests=ratiotests=construction_tests=pairtests=0
    for angle in [60,120]:
      for a in range(3,251):
       for b in range(2,a):
        if gcd(a,b)!=1:continue
        z=a*a+b*b+(1 if angle==120 else -1)*a*b;c=isqrt(z)
        if c*c!=z:continue
        require(gcd(c,a*b)==1,'pairwise primitivity')
        X,Y=(c+a-b,c+b-a) if angle==120 else (a+b-c,a+b+c)
        require(X*Y==3*a*b,'flux product')
        # Test integralities at their minimal common denominator and its multiples,
        # as well as ordinary small lengths. The proof itself uses half sums.
        d1=X//gcd(3,X);d2=Y//gcd(3,Y);step=d1*d2//gcd(d1,d2)
        Svals=set(range(1,41))|{step*j for j in range(1,9)}|{a*b*j for j in range(1,4)}
        for S in Svals:
            u,v=F(3*S,X),F(3*S,Y);n=F(S*S,a*b)
            half=(u+v)/2
            require(half==F(S*(c if angle==120 else a+b),a*b),'equilateral half sum')
            require(compatible(u,v,n)==(S%(a*b)==0),'equilateral admissibility')
            eqtests+=1
        if angle==120:
          for k in range(1,2*b+1):
            u=F(k*(2*a+b-c),X);v=F(k*(2*a+b+c),Y)
            require(u==F(k*(c-a),b) and v==F(k*(c+a),b),'F1 flux identities')
            require((v-u)/2==F(k*a,b),'F1 half difference')
            require(compatible(u,v,F(k*k*(a+b),b))==(k%b==0),'F1 admissibility')
            u=F(k*(a+2*b-2*c),X);v=F(k*(a+2*b+2*c),Y)
            require(u==F(k*(c-a-b),b) and v==F(k*(c+a+b),b),'isosceles identities')
            require((v-u)/2==F(k*(a+b),b),'isosceles half difference')
            require(compatible(u,v,F(k*k*(a+2*b),b))==(k%b==0),'isosceles admissibility')
            ratiotests+=2
        q,r=divmod(a,b);k0=q+(2 if angle==120 else 1)
        K=a*a+b*b-(a*b if angle==60 else 0)
        # The residue calculation is checked by a separate exhaustive coin test.
        for k in range(max(0,k0-2),k0+4):
            R=k*a*b-K
            exists=R>=0 and any((R-i*a)>=0 and (R-i*a)%b==0 for i in range(max(0,R//a)+1))
            require(exists==(k>=k0),'sharp short-base threshold in this band method')
            if k>=k0:
                na=b-r;nb=a*(k+(angle==60)-q-1)-b
                require(R==na*a+nb*b and min(na,nb)>=0,'explicit strip formula')
        # Moderate examples in both angle families and with non-symmetric sectors.
        if a<=65 and k0<=7:
          for m in (3*k0,3*k0+1):
            certificate=construct(a,b,c,angle,m)
            report=verify(certificate)
            construction_tests+=1;pairtests+=report['macro_pairs_checked']
        rows.append([a,b,c,angle])
    data=json.loads(Path('construction_116640.json').read_text())
    mutations=[]
    import copy
    for name,edit in [
      ('coordinate',lambda d:d['regions'][0]['vertices'][1].__setitem__(0,d['regions'][0]['vertices'][1][0]+1)),
      ('scale',lambda d:d['regions'][0].__setitem__('scale',44)),
      ('strip count',lambda d:d['regions'][3]['counts'].__setitem__(0,18)),
      ('delete region',lambda d:d['regions'].pop()),
      ('duplicate region',lambda d:d['regions'].append(copy.deepcopy(d['regions'][0]))),
      ('wrong tile count',lambda d:d.__setitem__('expected_tile_count',116641)),
      ('wrong target',lambda d:d.__setitem__('target_side',12961)),
    ]:
        bad=copy.deepcopy(data);edit(bad)
        try:verify(bad)
        except (ValueError,KeyError,TypeError):mutations.append(name)
        else:raise ValueError('mutation accepted: '+name)
    result=dict(result='PASS_SUPPLEMENTARY_CHECKS',parameter_bound_a=250,
                primitive_triples=len(rows),equilateral_scale_tests=eqtests,
                ratio_scale_tests=ratiotests,macro_constructions=construction_tests,
                macro_pair_intersections=pairtests,mutations_rejected=mutations,
                universal_proofs='PROOF.md; numerical checks are supplementary, not extrapolated proofs.',
                full_Erdos634_solved=False)
    Path('general_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
