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
    for d,m,expected in ((38,3,"NO"),(110,3,"UNRESOLVED_SMALL_SCALE"),
                         (110,15,"YES"),(2,1,"YES")):
        command=[sys.executable,str(CLI),str(d),str(m)]
        run=subprocess.run(command,text=True,capture_output=True,check=True)
        out=json.loads(run.stdout)
        assert out["status"]==expected,(d,m,out)
        assert out["full_Erdos634_solved"] is False
        assert out["N"]==d*m*m
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
    return {"status":"PASS","full_Erdos634_solved":False,
            "valid_status_checks":successful,"invalid_scope_inputs_rejected":rejected,
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
