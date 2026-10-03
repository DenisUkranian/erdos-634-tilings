#!/usr/bin/env python3
"""Independent exact macro audit of the free-k reflected-corner construction.

No constructor from the norm-completion agent is imported. Degenerate
zero-width blocks are omitted, and duplicate vertices are merged.
"""

import json
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
if not (HERE/"exact_geometry.py").exists():
    PACKAGE=HERE.parents[1]/"erdos-634-tilings/research/group2-trapezoids"
    sys.path.insert(0,str(PACKAGE))
from exact_geometry import (add,area2,ccw,contains,convex,encode,
                            intersection_area2,norm,scale,sub)


def require(ok,msg):
    if not ok:
        raise ValueError(msg)


def clean(poly):
    out=[]
    for p in poly:
        if not out or p!=out[-1]:
            out.append(p)
    if len(out)>1 and out[-1]==out[0]:
        out.pop()
    if len(out)<3 or area2(out)==0:
        return []
    return ccw(out)


def audit(a,b,c,m,k):
    require(a>b>0 and c*c==a*a+a*b+b*b and gcd(a,b)==1,"Bad primitive tile")
    require(m>=1 and k>=1,"Bad scales")
    t=a-b;r=m*b*c-a*a*k
    require(k*c>=m*t and r>=0,"Fit/remainder condition fails")
    x=r*pow(a,-1,b)%b;y=(r-a*x)//b
    require(y>=0,"Remainder is outside the semigroup")
    require(m*c>a*k,"Positive outer triangle does not follow")
    z=(F(a,c),F(b,c))
    F0=(F(0),F(0));O=(F(m*a*t),F(0));A=(F(m*c*c),F(0))
    B=scale(m*a*c,z);C=scale(m*t*c,z)
    E=(F(a*k*c),F(0));D=add(E,C)
    U=add(C,scale(a*a*k,z));V=add(E,scale(a*(m*c-a*k),z))
    target=clean([O,A,B,C]);outer=clean([F0,A,B]);removed=clean([F0,O,C])
    require(convex(target) and convex(outer) and convex(removed),"Invalid target geometry")
    require(all(contains(outer,p) for p in target+removed),"Corner partition leaves outer triangle")
    require(intersection_area2(target,removed)==0,"Removed corner overlaps target")
    require(area2(target)+area2(removed)==area2(outer),"Corner area identity fails")
    counts=[2*k*c*m*t-m*m*t*t,(a*k)**2,(m*c-a*k)**2,2*k*r]
    raw=[[O,E,D,C],[C,D,U],[E,A,V],[U,B,V,D]]
    pieces=[]
    for j,(poly,n) in enumerate(zip(raw,counts)):
        poly=clean(poly)
        if not poly:
            require(n==0,"Nonzero count on omitted block")
            continue
        require(n>0 and convex(poly),"Invalid nondegenerate macro")
        require(area2(poly)==n*a*b,"Wrong macro area")
        require(all(contains(target,p) for p in poly),"Macro leaves target")
        pieces.append((j,poly,n))
    for (_,p,_),(_,q,_) in combinations(pieces,2):
        require(intersection_area2(p,q)==0,"Macro interiors overlap")
    require(sum(n for _,_,n in pieces)==3*a*b*m*m,"Wrong count identity")
    require(sum(area2(p) for _,p,_ in pieces)==area2(target),"Macro area coverage mismatch")
    for j,n in [(1,a*k),(2,m*c-a*k)]:
        poly=clean(raw[j])
        lengths=sorted(norm(sub(q,p)) for p,q in zip(poly,poly[1:]+poly[:1]))
        require(lengths==sorted([(n*a)**2,(n*b)**2,(n*c)**2]),"Triangle block not similar")
    # The low cells use u=(a,0),v=(a,b); their difference is a b-edge.
    u=(F(a),F(0));v=(F(a),F(b))
    require(norm(u)==a*a and norm(v)==c*c and norm(sub(v,u))==b*b,"Bad low unit cell")
    require(k*c>=m*t,"The removed mt-triangle does not fit the kc by mt grid")
    if r:
        require(norm(sub(B,U))==r*r and norm(sub(D,U))==(a*b*k)**2,
                "Wrong high parallelogram lengths")
        unit_u=scale(F(1,r),sub(B,U));unit_v=scale(F(1,a*b*k),sub(D,U))
        require(norm(add(scale(a,unit_u),scale(b,unit_v)))==c*c,
                "High strip cell does not split into original tiles")
    return {"tile":[a,b,c],"multiplier":m,"free_k":k,"t":t,"remainder":r,
            "semigroup_coefficients":[x,y],"fit_slack":k*c-m*t,
            "count":3*a*b*m*m,"macro_counts":counts,"macro_pairs_checked":len(pieces)*(len(pieces)-1)//2,
            "zero_blocks_omitted":len(raw)-len(pieces),
            "low_block_vertices":len(clean(raw[0])),
            "target":encode(target),"blocks":[{"index":j,"count":n,"polygon":encode(p)} for j,p,n in pieces],
            "verified":True}


def run_campaign():
    triples=set()
    for p in range(2,51):
        for q in range(1,p):
            if gcd(p,q)>1:
                continue
            a,b,c=p*p-q*q,q*(2*p+q),p*p+p*q+q*q
            g=gcd(a,gcd(b,c));a,b,c=a//g,b//g,c//g
            a,b=max(a,b),min(a,b)
            if 3*c>=4*a:
                triples.add((a,b,c))
    instances=0
    for a,b,c in sorted(triples):
        for m in [2,3,4,5,7]:
            audit(a,b,c,m,(m+1)//2)
            instances+=1
    fixtures=[audit(5,3,7,2,1),audit(5,3,7,3,2),
              audit(5,3,7,7,2),audit(5,3,7,25,21)]
    (HERE/"certificates/free_k_macro_fixtures.json").write_text(json.dumps(fixtures,indent=2)+"\n")
    report={"primitive_triples_checked":len(triples),"strict_uniform_instances_checked":instances,
            "multipliers_checked":[2,3,4,5,7],"fixtures":[{k:v for k,v in r.items() if k not in ["target","blocks"]} for r in fixtures],
            "verification_scope":"Exact macrogeometry and positive grid recipes; no unit expansion in this audit",
            "all_checks_passed":True}
    (HERE/"free_k_audit_results.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


if __name__=="__main__":
    print(json.dumps(run_campaign(),indent=2))
