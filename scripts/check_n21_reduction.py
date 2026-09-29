#!/usr/bin/env python3
"""Exact finite arithmetic for the all-branch N=21 reduction; no geometry search."""
import json
from math import gcd, isqrt

if not __debug__:
    raise SystemExit('Run without -O: proof assertions must remain enabled.')

N = 21

def issquare(x):
    return x >= 0 and isqrt(x)**2 == x

def record_square(x):
    return {'value':x,'square':issquare(x), 'lower_root':isqrt(x) if x>=0 else None}

pairs = [(s,3*N//s) for s in range(1,isqrt(3*N)+1) if 3*N%s==0]
eq60=[{'s':s,'t':t,**record_square((t-s)**2-4*N)} for s,t in pairs]
eq120=[{'s':s,'t':t,**record_square((t-s)**2+16*N)} for s,t in pairs]
assert not any(r['square'] for r in eq60+eq120)

# a+2b | N, and k² = N*b/(a+2b).
iso120=[]
for A in [1,3,7,21]:
    for b in range(1,(A-1)//2+1):
        a=A-2*b
        k2=N*b//A
        if issquare(k2):
            c2=a*a+a*b+b*b
            iso120.append({'a':a,'b':b,'k':isqrt(k2),**record_square(c2)})
assert not any(r['square'] for r in iso120)

# F1: a+b | N, k²=N*b/(a+b). Includes all divisors,
# so the elementary lemma a+b >= 8 is not needed for this enumeration.
f1_120=[]
for S in [1,3,7,21]:
    for b in range(1,S):
        a=S-b
        k2=N*b//S
        c2=a*a+a*b+b*b
        if gcd(a,b)==1 and issquare(k2) and issquare(c2):
            c=isqrt(c2);k=isqrt(k2)
            f1_120.append({'a':a,'b':b,'c':c,'k':k,
                           'flux_numerator':k*(2*a+b-c),
                           'flux_denominator':c+a-b})
assert f1_120==[{'a':5,'b':16,'c':19,'k':4,'flux_numerator':28,'flux_denominator':8}]
assert f1_120[0]['flux_numerator']%f1_120[0]['flux_denominator']!=0

# A direct primitive triple check for a+b <=7, a finite lemma used
# to dismiss the other three 120-degree product formulas.
small_120=[(a,b,isqrt(a*a+a*b+b*b)) for a in range(1,7) for b in range(1,8-a)
           if gcd(a,b)==1 and issquare(a*a+a*b+b*b)]
assert small_120==[]

# beta P=21 => 2v² <21, hence v <=3.
beta=[(u,v,3*v*v-u*u) for v in range(2,4) for u in range(1,v) if gcd(u,v)==1]
assert not any(P==21 for u,v,P in beta)

# alpha bQ=21, Q>b; v²=Q-b, u²=Q-2b.
alpha=[]
for b in [1,3,7,21]:
    Q=N//b
    v2=Q-b;u2=Q-2*b
    if b<Q and u2>0 and issquare(v2) and issquare(u2):
        u=isqrt(u2);v=isqrt(v2)
        if gcd(u,v)==1:
            alpha.append({'u':u,'v':v,'tile':[u*v,b,v*v],
                          'target':[b*v*v,b*v*v,b*Q]})
assert alpha==[{'u':1,'v':2,'tile':[2,3,4],'target':[12,12,21]}]
print(json.dumps({'status':'PASS','scope':'finite arithmetic only; external shape classification and exact flux arguments are mathematical inputs; final alpha21 geometry is separate',
 'equilateral_60':eq60,'equilateral_120':eq120,
 'isosceles_120_candidates_with_square_k':iso120,'F1_120_structural_candidates':f1_120,
 'primitive_120_triples_with_a_plus_b_at_most_7':small_120,
 'beta_parameter_checks':beta,'unique_remaining_instance':alpha},indent=2))
