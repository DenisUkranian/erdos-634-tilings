#!/usr/bin/env python3
"""Replay the new exact rigidity results; numerical searches are excluded."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
CHECKS = (
    'global/verify_cell_minority.py',
    'global/verify_global_completion_budget.py',
    'global/verify_balanced_16_lift.py',
    'global/verify_uniform_fan_obstruction.py',
    'integer3431/verify_small_balanced_cells.py',
    'integer3431/verify_uniform_charged_cylinder.py',
    'cells5063/verify_phase_coordinates.py',
    'cells5063/verify_finite_cut_witness.py',
    'cells5063/verify_reduced_skeletons.py',
    'cells5063/verify_shared_profile_duals.py',
    'cells5063/verify_two_cell_rational_witness.py',
    'physical/verify_physical_controls.py',
)


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    records = []
    for command in CHECKS:
        start = time.monotonic()
        result = subprocess.run([sys.executable, str(HERE/command)], cwd=ROOT,
                                text=True, capture_output=True, timeout=180)
        if result.returncode:
            sys.stderr.write(result.stdout+result.stderr)
            raise RuntimeError(f'Failed exact replay: {command}')
        records.append({'command':command, 'status':'PASS',
            'seconds':round(time.monotonic()-start,3),
            'stdout':result.stdout, 'stderr':result.stderr})
        print('PASS '+command, flush=True)
    report = {'status':'ALL_EXACT_CONTROLS_PASS', 'checks':records,
        'full_3431_excluded':False, 'full_5063_excluded':False,
        'scope':'New finite exact exclusions and controls only. Universal theorem steps are written and internally audited; numerical target searches, formal proof-assistant verification, and external peer review are not claimed.'}
    (HERE/'REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CONTINUED_RIGIDITY_EXACT_REPLAY=PASS', flush=True)


if __name__ == '__main__':
    main()
