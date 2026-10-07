#!/usr/bin/env python3
"""Exercise the scoped read-only classifier's statuses and input rejection."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise SystemExit("Verification requires assertions; run without -O or PYTHONOPTIMIZE.")

CLI=Path(__file__).with_name("classify_global_sector.py")


def check():
    successful=[]
    for d,m,expected in ((38,3,"NO"),(110,3,"YES"),(110,15,"YES"),
                         (4830,1,"UNRESOLVED_SMALL_SCALE"),(2,1,"YES")):
        command=[sys.executable,str(CLI),str(d),str(m)]
        run=subprocess.run(command,text=True,capture_output=True,check=True)
        out=json.loads(run.stdout)
        assert out["status"]==expected,(d,m,out)
        assert out["full_Erdos634_solved"] is False
        assert out["N"]==d*m*m
        if d==110:
            assert out["witness"]["threshold_source"]=="nested_corner_unit_construction"
            assert out["witness"]["sufficient_branch_multiplier"]==1
            assert out["witness"]["nested_corner_seed"]["coefficients_a_b_c"]==[0,2,1]
        successful.append({"d":d,"m":m,"status":out["status"],
                           "sector_cutoff_C":out["sector_cutoff_C"],
                           "witness_count":len(out["all_witnesses"])})
    rejected=[]
    for d,m in ((3,1),(38,2),(12,1),(0,1),(38,0),(-2,1),(38,-1)):
        run=subprocess.run([sys.executable,str(CLI),str(d),str(m)],
                           text=True,capture_output=True)
        assert run.returncode!=0 and "error:" in run.stderr,(d,m,run)
        assert not run.stdout.strip()
        rejected.append([d,m])
    # Check orientation handling independently of the CLI's even-kernel scope.
    import classify_global_sector as classifier
    seed_controls=[]
    for branch in ("F2","F3","F4"):
        for a,b in ((8,7),(7,8)):
            witness={"branch":branch,"a":a,"b":b,"c":13}
            assert classifier.construction_threshold(witness)==1
            if not (branch=="F4" and a<b):
                assert witness["threshold_source"]=="nested_corner_unit_construction"
            seed_controls.append({"branch":branch,"a":a,"b":b,
                                  "threshold_source":witness["threshold_source"]})
    gamma_controls=[]
    for a,b,c in ((5,3,7),(112,75,163)):
        witness={"branch":"F3","a":a,"b":b,"c":c}
        assert classifier.construction_threshold(witness)==1
        assert witness["threshold_source"]=="gamma_corner_unit_construction"
        gamma_controls.append({"a":a,"b":b,"c":c,"threshold":1})
    for branch,a,b in (("F3",3,5),("F2",5,3),("F4",5,3)):
        witness={"branch":branch,"a":a,"b":b,"c":7}
        assert classifier.construction_threshold(witness)>1
        assert "gamma_corner_seed" not in witness
    rejected_seed={"branch":"F3","a":24,"b":11,"c":31}
    assert classifier.construction_threshold(rejected_seed)==6
    assert "nested_corner_seed" not in rejected_seed
    return {"status":"PASS","full_Erdos634_solved":False,
            "valid_status_checks":successful,"invalid_scope_inputs_rejected":rejected,
            "unit_seed_orientation_controls":seed_controls,
            "gamma_corner_ordered_controls":gamma_controls,
            "4830_retains_prior_threshold":6,
            "scope":"CLI status and scope controls, not a complete geometric solver"}


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
