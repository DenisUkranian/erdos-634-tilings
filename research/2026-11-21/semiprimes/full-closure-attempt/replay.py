#!/usr/bin/env python3
"""Replay exact conditional certificates; do not claim target closure."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents
            if (p / 'research').is_dir() and (p / 'scripts').is_dir())
CHECKS = (
    'core-budget/verify_core_budget.py',
    'target3431/verify_gate_excess.py',
    'target5063/verify_empty_remote_profile.py',
    'target5063/verify_monochromatic_controls.py',
    'target5063/verify_core_budget_audit.py',
    'global/verify_balanced_two_parent.py',
    'global/verify_empty_gate_budget.py',
    '../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/check_remote_cycles.py',
)


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    records = []
    for command in CHECKS:
        start = time.monotonic()
        result = subprocess.run(
            [sys.executable, str(HERE / command)], cwd=ROOT,
            text=True, capture_output=True, timeout=300)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise RuntimeError(f'Failed exact replay: {command}')
        records.append({
            'command': command,
            'sha256': hashlib.sha256((HERE / command).read_bytes()).hexdigest(),
            'status': 'PASS',
            'seconds': round(time.monotonic() - start, 3),
            'stdout': result.stdout,
            'stderr': result.stderr,
        })
        print('PASS ' + command, flush=True)
    report = {
        'status': 'ALL_EXACT_CONTROLS_PASS',
        'checks': records,
        'full_3431_excluded': False,
        'full_5063_excluded': False,
        'full_3431_minimal_odd_mode_excluded': False,
        'full_5063_215_odd_mode_excluded': False,
        'scope': (
            'Exact conditional native-profile and core bounds, paired-model '
            'rational and signed-integer witnesses, finite charge-budget '
            'arithmetic, and rigid controls. No full target exclusion, '
            'exhaustive target packing search, or nonnegative integer '
            'realization of the surviving profiles is claimed.'),
    }
    (HERE / 'REPLAY.json').write_text(json.dumps(report, indent=2) + '\n')
    print('NATIVE_BOUNDARY_WHOLE_GATE_AND_RELAXATION_REPLAY=PASS', flush=True)


if __name__ == '__main__':
    main()
