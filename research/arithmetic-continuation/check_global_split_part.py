#!/usr/bin/env python3
"""Compare bounded and direct coefficient lists in all eight surviving rows.

This verifies arithmetic formulas, not geometric realization below tails.
"""
import argparse
from functools import lru_cache
import json
from math import gcd, isqrt
from pathlib import Path

import check_other_split_branches as norms

if not __debug__:
    raise SystemExit("Verification requires assertions; run without -O or PYTHONOPTIMIZE.")

GROUP_ROWS=("W","beta","alpha","QP")
ALL_ROWS=GROUP_ROWS+norms.ROWS


def global_part(m):
    H=1
    for p,e in norms.factors(m).items():
        if p>3 and p%24 not in (5,19):
            H*=p**e
    return H


def square_root(z):
    if z<0:
        return None
    r=isqrt(z)
    return r if r*r==z else None


def classical(d):
    return d in (2,6) or all(p%4==1 for p in norms.factors(d) if p>2)


@lru_cache(None)
def bounded_group_list(d,H):
    out={row:set() for row in GROUP_ROWS}
    B=d*H*H
    for v in range(2,isqrt(B)+1):
        for u in range(1,v):
            if gcd(u,v)!=1:
                continue
            b,Q,P=v*v-u*u,2*v*v-u*u,3*v*v-u*u
            for row,D in (("W",Q),("beta",P),("alpha",b*Q),("QP",Q*P)):
                if D%d:
                    continue
                s=square_root(D//d)
                if s is not None and s%2 and H%global_part(s)==0:
                    out[row].add((u,v,s))
    return out


def direct_group_list(row,d,m):
    out=set()
    def add(u2,v2,s):
        u,v=square_root(u2),square_root(v2)
        if u is not None and v is not None and 0<u<v and gcd(u,v)==1:
            out.add((u,v,s))
    for s in norms.divisors(m):
        D=d*s*s
        if row in ("W","beta"):
            j=2 if row=="W" else 3
            # Q>v² and P>2v²; v²<=D safely contains both cases.
            for v in range(2,isqrt(D)+1):
                add(j*v*v-D,v*v,s)
        else:
            for x in norms.divisors(D):
                y=D//x
                if row=="alpha":
                    add(y-2*x,y-x,s)
                else:
                    add(2*y-3*x,y-x,s)
    return out


def check():
    comparisons={row:0 for row in ALL_ROWS}
    positives={row:0 for row in ALL_ROWS}
    witnesses={row:set() for row in ALL_ROWS}
    classical_cases=0
    cases=[]
    for d in range(2,101,2):
        if any(e!=1 for e in norms.factors(d).values()):
            continue
        for m in range(1,42,2):
            if global_part(m)<=13:
                cases.append((d,m))
    # Each row has a separate positive arithmetic control. None is being
    # declared geometrically realizable at the displayed residual scale.
    controls={"W":(14,1),"beta":(26,1),"alpha":(70,1),"QP":(322,1),
              "I120":(154,1),"F2":(506,1),"F3":(110,3),"F4":(330,1)}
    cases.extend(controls.values())
    for d,m in cases:
        H=global_part(m)
        B=d*H*H
        classical_cases+=classical(d)
        grouped=bounded_group_list(d,H)
        normed=norms.restricted_lists(d,H)
        for row in ALL_ROWS:
            if row in GROUP_ROWS:
                bounded={entry for entry in grouped[row] if m%entry[-1]==0}
                direct=direct_group_list(row,d,m)
            else:
                bounded={entry for entry in normed[row] if m%entry[-1]==0}
                direct=norms.direct_list(row,d,m)
            assert bounded==direct,(row,d,m,bounded,direct)
            comparisons[row]+=1
            positives[row]+=bool(direct)
            for entry in direct:
                witnesses[row].add((d,)+entry)
                if row in GROUP_ROWS:
                    u,v,s=entry
                    assert v*v<B
                    factor=3*v*v-u*u if row=="beta" else 2*v*v-u*u
                    assert B%factor==0
                else:
                    a,b,c,s=entry
                    factor=2*a+b if row=="F4" else a+2*b
                    assert B%factor==0 and a<=B and b<=B
    control_report=[]
    for row,(d,m) in controls.items():
        result=(direct_group_list(row,d,m) if row in GROUP_ROWS
                else norms.direct_list(row,d,m))
        assert result,(row,d,m)
        control_report.append({"row":row,"d":d,"m":m,"coefficient_witnesses":sorted(result)})
    assert not any(direct_group_list(row,38,3) for row in GROUP_ROWS)
    assert not any(norms.direct_list(row,38,3) for row in norms.ROWS)
    return {"status":"PASS","full_Erdos634_solved":False,
            "scope":"All-eight-row arithmetic comparison; no small-scale geometric decisions",
            "kernel_max_regular_grid":100,"odd_multiplier_max_regular_grid":41,
            "global_split_part_max_regular_grid":13,
            "total_input_pairs":len(cases),"classical_flag_true_input_pairs":classical_cases,
            "comparisons_by_row":comparisons,
            "total_independent_comparisons":sum(comparisons.values()),
            "positive_comparisons_by_row":positives,
            "distinct_coefficient_witnesses_by_row":{row:len(entries) for row,entries in witnesses.items()},
            "positive_arithmetic_controls":control_report}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path,help="write the arithmetic comparison report here")
    args=parser.parse_args()
    output=json.dumps(check(),indent=2,sort_keys=True)+"\n"
    if args.report is not None:
        args.report.write_text(output)
    print(output,end="")


if __name__=="__main__":
    main()
