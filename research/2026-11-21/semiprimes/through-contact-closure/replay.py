#!/usr/bin/env python3
"""Replay exact contact geometry and frozen proof controls, not target exclusion."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CONTRIBUTING.md').is_file())
CHECKS=(
    ('corners/verify_corner_roots.py',),
    ('owned/verify_owned_controls.py','--geometry-only'),
    ('spatial/verify_spatial.py',),
    ('whole-edges/verify_whole_edges.py','--geometry-only'),
    ('corner-tests/verify_long_cycles.py',),
    ('corner-tests/verify_area_cycles.py',),
    ('corner-tests/verify_pattern_isometries.py',),
    ('population/verify_population_wrapper.py',),
    ('population/verify_joint_wrapper.py',),
    ('population/verify_contact_budget_theorem.py',),
    ('audit/verify_through_geometry.py',),
    ('audit/verify_proof_pipeline.py','--replay-only'),
    ('audit/verify_snapshot_controls.py',),
    ('audit/verify_area_audit_controls.py',),
    ('../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/check_remote_cycles.py',),
)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--with-solver',action='store_true',help='Also repeat the integrated libz3 positive controls.')
    args=p.parse_args()
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    checks=list(CHECKS)
    if args.with_solver:
        checks.extend((('owned/verify_owned_controls.py',),
                       ('whole-edges/verify_whole_edges.py','--with-solver'),
                       ('population/verify_population_wrapper.py','--with-solver'),
                       ('population/verify_joint_wrapper.py','--with-solver'),
                       ('corner-tests/verify_joint_encoding.py','--with-phase')))
    reports=[]
    for command in checks:
        started=time.monotonic()
        path=HERE/command[0]
        run=subprocess.run([sys.executable,str(path),*command[1:]],cwd=ROOT,
                           capture_output=True,text=True,timeout=600)
        if run.returncode:
            sys.stderr.write(run.stdout+run.stderr)
            raise RuntimeError('Failed control: '+' '.join(command))
        reports.append(dict(command=list(command),status='PASS',
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                            seconds=round(time.monotonic()-started,3),
                            stdout=run.stdout,stderr=run.stderr))
        print('PASS '+' '.join(command),flush=True)
    report=dict(status='ALL_CONTACT_AND_PROOF_CONTROLS_PASS',checks=reports,
                solver_integration_included=args.with_solver,
                full_3431_excluded=False,full_5063_excluded=False,
                complete_target_tiling_found=False,
                scope='Exact unrestricted contact catalogues, corner root coverage, geometry cuts and finite proof-checker controls. No whole-target refutation or construction.')
    name='SOLVER_REPLAY.json' if args.with_solver else 'REPLAY.json'
    (HERE/name).write_text(json.dumps(report,indent=2)+'\n')
    print('UNRESTRICTED_WHOLE_CONTACT_CONTROLS=PASS',flush=True)


if __name__=='__main__':main()
