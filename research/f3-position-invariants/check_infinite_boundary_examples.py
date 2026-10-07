#!/usr/bin/env python3
"""Finite exact examples of a separately proved infinite obstruction family."""
from decimal import Decimal, localcontext
from math import gcd
import json

def representations(E,a,b,c):
    return [(A,B,(E-A*a-B*b)//c)
            for A in range(E//a+1)
            for B in range((E-A*a)//b+1)
            if (E-A*a-B*b)%c==0]

def first_boundary_multiplier(E,a,b,c,limit=200):
    # gcd(a,b)=1 for a primitive norm triple. For each C this residue is
    # the smallest possible A; all others are larger by b.
    inverse=pow(a,-1,b)
    for t in range(1,limit+1):
        for C in range(t*E//c+1):
            remainder=t*E-C*c
            A=(remainder*inverse)%b
            if A*a<=remainder:
                return {'multiplier':t,'A':A,'B':(remainder-A*a)//b,'C':C}
    return None

def main():
    examples=[]
    # Decimal arithmetic only proposes convergents. Every reported geometric
    # positivity and semigroup exclusion is checked in exact integer arithmetic.
    with localcontext() as ctx:
        ctx.prec=200
        x=1+Decimal(3)*Decimal(2).sqrt()/2+Decimal(3).sqrt()+Decimal(6).sqrt()/2
        pm2,pm1,qm2,qm1=0,1,1,0
        for index in range(22):
            digit=int(x);m=digit*pm1+pm2;n=digit*qm1+qm2
            pm2,pm1,qm2,qm1=pm1,m,qm1,n
            x=1/(x-digit)
            a0,b0,c0=m*m-n*n,2*m*n+n*n,m*m+m*n+n*n
            g=gcd(gcd(a0,b0),c0)
            a,b,c=a0//g,b0//g,c0//g
            E=2*a*b+2*b*b-a*a
            if E<=0:continue
            assert gcd(m,n)==1 and g in (1,3)
            assert a>2*b>0 and c*c==a*a+a*b+b*b
            assert gcd(gcd(a,b),c)==1 and E<48*b
            reps=representations(E,a,b,c)
            assert not reps
            examples.append({'convergent_index':index,'m':m,'n':n,'g':g,
                             'tile':[a,b,c], 'E':E,
                             'E_representations':reps,
                             'first_boundary_multiplier_up_to_200':
                                 first_boundary_multiplier(E,a,b,c),
                             'gamma_tiling':'IMPOSSIBLE_BY_BOUNDARY',
                             'full_F3_status':'NOT_DECIDED_BY_THIS_TEST'})
    assert len(examples)>=5
    assert [e['first_boundary_multiplier_up_to_200']['multiplier']
            for e in examples[:3]]==[3,37,131]
    assert all(e['first_boundary_multiplier_up_to_200'] is None
               for e in examples[3:])
    a,b,c=2024,741,2479
    E=2*a*b+2*b*b-a*a
    assert E==1154 and a//b==2 and not representations(6*E,a,b,c)
    residue_checks=[]
    for C in range(6*E//c+1):
        remaining=6*E-C*c
        A=(remaining*pow(a,-1,b))%b
        assert A*a>remaining
        residue_checks.append({'C':C,'remaining':remaining,
                               'least_nonnegative_A_mod_b':A})
    return {'status':'PASS', 'examples':examples,
            'gamma_necessity_counterexample':{
                'tile':[a,b,c],'multiplier':6,'E':E,
                'full_F3_count':3*(a+b)*(a+2*b)*36,
                'full_F3_exists_by':'square-class-tails.md Appendix A, threshold6',
                'gamma_filler':'IMPOSSIBLE_BY_BOUNDARY',
                'residue_checks':residue_checks},
            'infinite_claim_basis':'separate proof using Siegel, not finite tests',
            'full_Erdos634_solved':False}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
