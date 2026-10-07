#!/usr/bin/env python3
"""Arithmetic and classifier regressions for the positive gamma staircase."""
from __future__ import annotations

import argparse
import importlib.util
from math import gcd, isqrt
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(ROOT / "research/arithmetic-continuation"))
classifier = load_module("gamma_staircase_classifier", ROOT / "research/arithmetic-continuation/classify_global_sector.py")
candidates = load_module("gamma_staircase_candidates", ROOT / "research/uniform-reduction/candidates.py")


def ceildiv(n, d):
    return -(-n // d)


def score(a, b, m):
    return b+a*ceildiv(m*(a-b),b)-m*(a+2*b)


def run(bound):
    triples = 0
    checks = 0
    exact_below_tail = []
    for b in range(1, bound):
        for a in range(b+1, bound+1):
            if gcd(a,b) != 1:
                continue
            c = isqrt(a*a+a*b+b*b)
            if c*c != a*a+a*b+b*b:
                continue
            triples += 1
            margin = 2*a*b+2*b*b-a*a
            w = {"branch":"F3", "a":a, "b":b, "c":c}
            old = classifier.old_threshold(w)
            tail = classifier.construction_threshold(w)
            assert tail <= old
            for m in range(1, 41):
                t=m*(a-b)
                last=(t-1)//a
                # Independently maximize the far corner over every possible
                # column of intersecting common cells.
                maximum=max(b*(i+1)+a*((t-1-a*i)//b+1)
                            for i in range(last+1))
                assert maximum == b+a*ceildiv(t,b)
                assert score(a,b,m+b) == score(a,b,m)-margin
                assert b*score(a,b,m) <= b*(a+b)-a-m*margin
                for n in range(1, 7):
                    assert score(a,b,m+n) <= score(a,b,m)+score(a,b,n)-b
                exact = classifier.gamma_staircase_at_multiplier(w,m)
                assert (exact is not None) == (score(a,b,m)<=0)
                if margin <= 0:
                    assert exact is None
                else:
                    sufficient=ceildiv(b*(a+b)-a,margin)
                    if m>=sufficient:
                        assert exact is not None
                if 2*b<a and 2*a<=5*b:
                    assert (exact is not None) == (m>=2)
                if exact is not None and m<tail:
                    exact_below_tail.append([a,b,c,m,tail])
                checks += 1

    # Orientation control: this construction never certifies the exchanged
    # order or another norm branch merely from the ordered F3 result.
    for branch,a,b in [("F3",11,24),("F2",24,11),("F4",24,11),
                       ("I120",24,11)]:
        assert classifier.gamma_staircase_at_multiplier(
            {"branch":branch,"a":a,"b":b,"c":31},2) is None
    w={"branch":"F3","a":24,"b":11,"c":31}
    assert classifier.construction_threshold(w)==2
    assert classifier.gamma_staircase_at_multiplier(w,1) is None
    second=classifier.gamma_staircase_at_multiplier(w,2)
    assert second=={"outer_scale":92,"removed_corner_scale":26,
                    "maximum_common_cell_cost":83}
    first_class=classifier.classify(4830,1)
    third_class=classifier.classify(4830,3)
    assert first_class["status"]=="UNRESOLVED_SMALL_SCALE"
    assert first_class["sector_cutoff_C"]==2
    assert third_class["status"]=="YES"
    isolated=classifier.classify(545142,5)
    assert isolated["status"]=="YES"
    assert isolated["reason"]=="proved_gamma_staircase_at_residual_scale"
    assert isolated["witness"]["sufficient_branch_multiplier"]==6
    assert isolated["witness"]["residual_multiplier"]==5
    assert isolated["witness"]["residual_gamma_staircase"]["maximum_common_cell_cost"]==2281
    # The public sector CLI remains intentionally restricted to odd scales.
    try:
        classifier.classify(4830,2)
    except ValueError:
        pass
    else:
        raise AssertionError("Sector CLI scope silently changed")
    controls=[]
    for d,m,expected in [(38,3,"NO"),(110,3,"YES"),(110,15,"YES"),
                          (2,1,"YES"),(154,1,"UNRESOLVED_SMALL_SCALE")]:
        actual=classifier.classify(d,m)["status"]
        assert actual==expected
        controls.append({"d":d,"m":m,"status":actual})
    candidate_lists=[]
    for n,m in [(4830,1),(19320,2)]:
        rows=candidates.enumerate_candidates(n)
        assert len(rows)==1
        row=rows[0]
        assert (row.branch,row.tile,row.multiplier)==("F3-120",(24,11,31),m)
        candidate_lists.append({"N":n,"branch":row.branch,
                                "tile":list(row.tile),"multiplier":m})
    return {
        "status":"PASS", "primitive_short_side_bound":bound,
        "primitive_norm_triples_checked":triples,"scale_checks":checks,
        "class4830":{"all_integer_m_at_least":2,
                     "only_unresolved_count":4830,
                     "m2_constructive_staircase":second,
                     "m1_sector_status":first_class["status"],
                     "m3_sector_status":third_class["status"]},
        "candidate_lists":candidate_lists,"classifier_controls":controls,
        "exact_positive_scales_below_used_uniform_tail":exact_below_tail,
        "isolated_scale_CLI_control":{"d":545142,"m":5,
                                      "status":isolated["status"],
                                      "reason":isolated["reason"]},
        "sector_CLI_odd_multiplier_scope_preserved":True,
        "general_nonexistence_claimed_from_staircase_failure":False,
        "full_Erdos634_solved":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound",type=int,default=300)
    parser.add_argument("--report",type=Path)
    args=parser.parse_args()
    result=run(args.bound)
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.report:
        args.report.write_text(text)
    print(text,end="")


if __name__=="__main__":
    main()
