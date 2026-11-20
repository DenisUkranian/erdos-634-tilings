#!/usr/bin/env python3
"""Replay exact common-obstruction controls without rerunning optimization.

Passing these checks does not decide either original F2 tiling question.
The optional coupled control requires NumPy and SciPy; default checks use
the standard library and existing exact project geometry modules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--coupled-control', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    joint = ['joint/replay.py']
    if args.coupled_control:
        joint.append('--coupled-control')
    jobs = [
        ('mixed_height_cycle_geometry', ['boundary/verify_mixed_cycle_controls.py']),
        ('known_143_phase_gates', ['boundary/check_known143_gates.py']),
        ('charged_terminal_polygon', ['terminal/verify_charged_patch.py']),
        ('integer_residue_witness_and_timeout_scope', ['terminal/verify_terminal_torus_witness.py']),
        ('joint_charges_and_exact_native_duals', joint),
    ]
    results = []
    for name, command in jobs:
        start = time.monotonic()
        result = subprocess.run([sys.executable, '-B', *command], cwd=HERE,
                                text=True, capture_output=True, timeout=180)
        results.append(dict(name=name, command=command,
                            exit_code=result.returncode,
                            seconds=round(time.monotonic()-start, 3),
                            stdout=result.stdout, stderr=result.stderr))
        print(name + ': ' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise SystemExit(result.returncode)
    sources = list(HERE.rglob('*.py'))
    sources += list((HERE/'boundary').glob('mixed_cycle_*.json'))
    sources += [HERE/'terminal/charged_patch_certificate.json']
    sources += list((HERE/'terminal').glob('torus_*_3.json'))
    sources += list((HERE/'joint').glob('torus*/exact_dual.json'))
    hashes = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(sources)}
    report = dict(format='common-obstruction-exact-controls-v1', status='PASS',
                  coupled_control=args.coupled_control, checks=results,
                  source_sha256=hashes,
                  target_status={'3431': 'OPEN', '5063': 'OPEN'},
                  unrestricted_nonexistence_certificate=False,
                  complete_target_tiling_certificate=False,
                  full_Erdos634_solved=False,
                  scope='Exact finite arithmetic and local geometric controls. '
                        'The 555/731 population bounds require the native two-height '
                        'hypotheses. Partial packings and timeouts do not decide a target.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: five exact control suites; 3431 and 5063 remain OPEN.')


if __name__ == '__main__':
    main()
