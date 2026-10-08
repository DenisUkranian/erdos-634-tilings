#!/usr/bin/env python3
"""Exact arithmetic regression for the finite-band lattice identity."""
import json
from math import gcd, isqrt
from functools import reduce
from itertools import combinations
from pathlib import Path


def mul(p,q):
    a,b=p; c,d=q
    return a*c-b*d,a*d+b*c+b*d


def norm(p):
    a,b=p
    return a*a+a*b+b*b


def power(p,k):
    ans=(1,0)
    for _ in range(k):
        ans=mul(ans,p)
    return ans


def scale(p,s):
    return p[0]*s,p[1]*s


units=[power((0,1),j) for j in range(6)]
triples=[]
checks=0
for a in range(1,201):
    for b in range(1,201):
        if gcd(a,b)!=1:
            continue
        n=a*a+a*b+b*b
        c=isqrt(n)
        if c*c!=n:
            continue
        triples.append((a,b,c))
        # Norm omega=c confines both coordinates to |coordinate|<=2sqrt(c/3).
        bound=isqrt(4*c//3)+2
        candidates=[]
        for u in range(-bound,bound+1):
            for v in range(-bound,bound+1):
                w=(u,v)
                if norm(w)==c and any(mul(e,mul(w,w))==(a,b) for e in units):
                    candidates.append(w)
        assert candidates,(a,b,c)
        for k in range(8):
            columns=[]
            for h in range(k+1):
                p=scale(power((a,b),h),c**(k-h))
                columns.extend([p,mul(p,(0,1))])
            determinant_gcd=reduce(gcd,(abs(p[0]*q[1]-p[1]*q[0])
                                       for p,q in combinations(columns,2)),0)
            # Actual covolume = determinant_gcd / c^(2k).
            assert determinant_gcd==c**k,(a,b,c,k,determinant_gcd)
            checks+=1
assert power((3,1),2)==(8,7)
assert 13**11==1792160394037
report={"status":"PASS","primitive_ordered_triples":len(triples),
        "lattice_checks":checks,"bands_k":list(range(8)),
        "full_Erdos634_solved":False,
        "scope":"Finite arithmetic regression; no geometric decision of 154 or 4830."}
print(json.dumps(report,indent=2))
Path(__file__).with_name('verification.json').write_text(json.dumps(report,indent=2)+'\n')
