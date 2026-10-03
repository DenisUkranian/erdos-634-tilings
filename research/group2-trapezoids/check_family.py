#!/usr/bin/env python3
"""Replay the stated finite macro survey and small independent expansions."""

import copy
import json
from math import gcd
from pathlib import Path

from generate import certificate
from verify import verify

HERE=Path(__file__).resolve().parent


def main():
    triples=set()
    for m in range(2,31):
        for n in range(1,m):
            if gcd(m,n)>1:
                continue
            a,b,c=m*m-n*n,n*(2*m+n),m*m+m*n+n*n
            g=gcd(a,gcd(b,c));a,b,c=a//g,b//g,c//g
            triples.add((a,b,c));triples.add((b,a,c))
    for a,b,c in sorted(triples):
        verify(certificate(a,b,c))
    fixtures=[("seed_3_5_7.json",certificate(3,5,7),True),
              ("seed_5_3_7.json",certificate(5,3,7),True),
              ("counterexample_x2509.json",certificate(32,45,67,t=12),False),
              ("beta_corner_8_7_13_m2.json",certificate(7,8,13,t=1,m=2,kind="corner"),False),
              ("beta_corner_8_7_13_m3.json",certificate(7,8,13,t=1,m=3,kind="corner"),False)]
    results=[]
    for name,cert,expand in fixtures:
        result=verify(cert,expand)
        (HERE/"certificates"/name).write_text(json.dumps(cert,indent=2)+"\n")
        results.append({"certificate":name,**result})
    balanced=0
    for a,b,c in sorted(triples):
        if not b<a or 3*a>4*b:
            continue
        for m in [2,3]:
            verify(certificate(b,a,c,t=a-b,m=m,kind="corner"))
            balanced+=1
    # These are meaningful corruption checks of the independent checker.
    source=fixtures[0][1]
    corruptions=[]
    bad=copy.deepcopy(source);bad["blocks"][0]["columns"]+=1;corruptions.append(bad)
    bad=copy.deepcopy(source);bad["blocks"][1]["scale"]+=1;corruptions.append(bad)
    bad=copy.deepcopy(source);bad["blocks"][3]["width_coefficients"][0]+=1;corruptions.append(bad)
    bad=copy.deepcopy(source);bad["target_data"]["short_base"]+=1;corruptions.append(bad)
    bad=copy.deepcopy(source);bad["blocks"][1]["polygon"][0][0]="999";corruptions.append(bad)
    rejected=0
    for bad in corruptions:
        try:
            verify(bad)
        except (ValueError,ZeroDivisionError):
            rejected+=1
        else:
            raise RuntimeError("A corrupted certificate was accepted")
    report={"status":"verified","universal_proof_not_replaced_by_finite_tests":True,
            "default_seed_ordered_triples":len(triples),"default_seed_macro_pairs":15*len(triples),
            "balanced_beta_corner_macro_instances":balanced,
            "fixtures":results,"corrupted_certificates_rejected":rejected,
            "full_Erdos634_solved":False}
    (HERE/"VERIFIED_RESULTS.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
