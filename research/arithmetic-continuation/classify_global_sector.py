#!/usr/bin/env python3
"""Read-only classifier for N=d*m^2, with even squarefree d and odd m.

YES/NO are conclusive under the repository's stated classification and
construction inputs. UNRESOLVED_SMALL_SCALE is not a nonexistence result.
The finite enumeration can be expensive for large d*H(m)^2.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

import check_global_split_part as global_lists
import check_other_split_branches as norms


def load_threshold():
    source=Path(__file__).resolve().parents[1]/"square-class-tails"/"classify.py"
    spec=importlib.util.spec_from_file_location("prior_square_class_thresholds",source)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.threshold


old_threshold=load_threshold()


def three_generator_witness(r,A,B,c):
    """Return nonnegative x,y,q with r=x*A+y*B+q*c, or None."""
    if r<0:
        return None
    if B==1:
        return (0,r,0)
    inverse=pow(A,-1,B)  # Primitive norm sides are coprime.
    for q in range(r//c+1):
        remainder=r-q*c
        x=(remainder*inverse)%B
        if x*A<=remainder:
            return (x,(remainder-x*A)//B,q)
    return None


def construction_threshold(witness):
    """Use proved unit seeds before falling back to prior fixed-tile tails."""
    branch=witness["branch"]
    witness["threshold_source"]="prior_square_class_tail"
    if branch not in ("F2","F3","F4"):
        return old_threshold(witness)
    a,b,c=witness["a"],witness["b"],witness["c"]
    if branch=="F4" and a<b:
        witness["threshold_source"]="oriented_F4_unit_construction"
        return 1
    A,B=max(a,b),min(a,b)
    r=B*c-A*A
    seed=three_generator_witness(r,A,B,c)
    if A>B and c>=A-B and seed is not None:
        # The reflected F4 theorem uses A>B. Its symmetric F2 bridge
        # and the two F3 attachments give both F2/F3 side orders.
        witness["threshold_source"]="nested_corner_unit_construction"
        witness["nested_corner_seed"]={"larger_short_side":A,
                                       "smaller_short_side":B,"k":1,
                                       "remainder":r,"coefficients_a_b_c":list(seed)}
        return 1
    if branch=="F3" and b<a<=2*b:
        witness["threshold_source"]="gamma_corner_unit_construction"
        witness["gamma_corner_seed"]={"outer_scale":a+2*b,
                                      "removed_corner_scale":a-b}
        return 1
    return old_threshold(witness)


def classify(d,m):
    if d<=0 or d%2 or any(e!=1 for e in norms.factors(d).values()):
        raise ValueError("d must be a positive even squarefree integer")
    if m<=0 or m%2==0:
        raise ValueError("m must be a positive odd integer")
    H=global_lists.global_part(m)
    result={"d":d,"m":m,"N":d*m*m,"H":H,
            "primitive_parameter_bound":d*H*H,
            "scope":"even squarefree kernel and odd multiplier",
            "full_Erdos634_solved":False,
            "exact_minimum_scale_claimed":False}
    if global_lists.classical(d):
        witness={"branch":"classical","coefficient":d,
                 "coefficient_multiplier":1,"sufficient_branch_multiplier":1,
                 "divides_multiplier":True,"residual_multiplier":m}
        return dict(result,status="YES",reason="classical_construction",
                    sector_cutoff_C=1,witness=witness,all_witnesses=[witness])

    witnesses=[]
    for branch,entries in global_lists.bounded_group_list(d,H).items():
        for u,v,s in sorted(entries):
            witnesses.append({"branch":branch,"u":u,"v":v,
                              "coefficient":d*s*s,"coefficient_multiplier":s})
    for branch,entries in norms.restricted_lists(d,H).items():
        for a,b,c,s in sorted(entries):
            if s%2==0 or H%global_lists.global_part(s):
                continue
            witnesses.append({"branch":branch,"a":a,"b":b,"c":c,
                              "coefficient":norms.coefficient(branch,a,b),
                              "coefficient_multiplier":s})
    for witness in witnesses:
        s=witness["coefficient_multiplier"]
        assert witness["coefficient"]==d*s*s
        witness["sufficient_branch_multiplier"]=construction_threshold(witness)
        witness["divides_multiplier"]=(m%s==0)
        witness["residual_multiplier"]=m//s if m%s==0 else None
    witnesses.sort(key=lambda w:(w["branch"],w["coefficient"],
                                 w.get("u",w.get("a",0)),
                                 w.get("v",w.get("b",0))))
    C=max([1]+[w["coefficient_multiplier"]*w["sufficient_branch_multiplier"]
               for w in witnesses])
    dividing=[w for w in witnesses if w["divides_multiplier"]]
    constructive=[w for w in dividing
                  if w["residual_multiplier"]>=w["sufficient_branch_multiplier"]]
    result.update(sector_cutoff_C=C,all_witnesses=witnesses,
                  dividing_witness_count=len(dividing))
    if constructive:
        return dict(result,status="YES",reason="proved_construction_threshold",
                    witness=constructive[0])
    if not dividing:
        return dict(result,status="NO",reason="no_necessary_primitive_witness")
    assert m<C
    return dict(result,status="UNRESOLVED_SMALL_SCALE",
                reason="necessary_witnesses_exist_but_no_residual_scale_reaches_the_used_tail",
                unresolved_witnesses=dividing)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("d",type=int,help="positive even squarefree kernel")
    parser.add_argument("m",type=int,help="positive odd multiplier")
    args=parser.parse_args()
    try:
        result=classify(args.d,args.m)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
