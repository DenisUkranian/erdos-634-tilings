#!/usr/bin/env python3
"""Check finite arithmetic samples of the squarefree primitive F3 front."""
import argparse
from math import gcd
import json
from pathlib import Path

from check_other_split_branches import factors

if not __debug__:
    raise SystemExit("Verification requires assertions; run without -O or PYTHONOPTIMIZE.")


def check(max_h=20000):
    count=0
    squarefree_count=0
    examples=[]
    for h in range(5,max_h+1,24):
        a,b,c=h*h-1,2*h+1,h*h+h+1
        q=h*h+4*h+1
        D=3*h*(h+2)*q
        assert a>b>0 and gcd(a,b)==1 and c*c==a*a+a*b+b*b
        assert D==3*(a+2*b)*(a+b)
        assert gcd(h,h+2)==gcd(h,q)==gcd(h+2,q)==1
        assert h%3 and (h+2)%3 and q%3
        assert q%16==14 and D%16==14
        fs=[factors(h),factors(h+2),factors(q)]
        inert=[p for p,e in fs[0].items() if e%2 and pow(2,(p-1)//2,p)==p-1]
        assert inert and all(p!=3 and (h+2)%p and q%p for p in inert)
        sf=all(all(e==1 for e in part.values()) for part in fs)
        if sf:
            squarefree_count+=1
            if len(examples)<10:
                factorization={3:1}
                for part in fs:
                    assert not factorization.keys() & part.keys()
                    factorization.update(part)
                examples.append({"h":h,"tile":[a,b,c],"coefficient":D,
                                 "factorization":dict(sorted(factorization.items())),
                                 "inert_for_2_prime":inert[0],
                                 "residual_scale_forced":1})
        count+=1
    assert examples[0]["coefficient"]==4830
    assert examples[1]["coefficient"]==2583726
    return {"status":"PASS","full_Erdos634_solved":False,
            "scope":"Arithmetic candidates only; no positive or negative tiling decisions",
            "infinitude_basis":"Written squarefree-sieve proof, not this finite sample",
            "max_h":max_h,"parameters_checked":count,
            "squarefree_candidates_in_sample":squarefree_count,"examples":examples}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report",type=Path)
    args=parser.parse_args()
    output=json.dumps(check(),indent=2,sort_keys=True)+"\n"
    if args.report is not None:
        args.report.write_text(output)
    print(output,end="")


if __name__=="__main__":
    main()
