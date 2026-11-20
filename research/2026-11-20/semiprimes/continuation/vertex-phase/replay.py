#!/usr/bin/env python3
"""Replay finite controls; --solver additionally requires libz3.so.4.

These checks do not decide either target or formally verify the written proofs.
All search outputs are kept outside the frozen research package.
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
BASE = HERE.parent / 'global-endpoints' / 'integer'


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    jobs = [
        ('supported_cycle_geometry', ['pure_cycles/check_remote_cycles.py']),
        ('strict_phase_bounds', ['verify_no_phase_gaps.py']),
        ('signed_characters_and_residues', ['verify_signed_arithmetic.py']),
        ('terminal_node_arithmetic', ['verify_terminal_node_balance.py']),
        ('independent_phase_arithmetic', ['check_phase_independent.py']),
        ('constructive_143_compact', ['constructive-control/verify_macro.py',
                                    'constructive-control/control143_compact.txt', '5', '3', '7']),
        ('constructive_143_perimeter', ['constructive-control/verify_macro.py',
                                      'constructive-control/control143_perimeter.txt', '5', '3', '7']),
    ]
    if args.solver:
        jobs += [
            ('unrestricted_corner_143', ['verify_corners.py', str(BASE)]),
            ('unsigned_population_143', ['verify_populations.py', str(BASE), str(HERE)]),
            ('population_scope_and_rebuild', ['check_population_scope.py']),
            ('signed_joint_population_143', ['verify_signed_solver.py', str(BASE), str(HERE), '--joint-heights']),
            ('signed_scope_and_rebuild', ['check_signed_scope.py']),
            ('joint_height_scope_and_rebuild', ['check_joint_height_scope.py']),
        ]
    results = []
    for name, command in jobs:
        start = time.monotonic()
        result = subprocess.run([sys.executable, '-B', *command], cwd=HERE,
                                text=True, capture_output=True, timeout=180)
        record = dict(name=name, command=command, exit_code=result.returncode,
                      seconds=round(time.monotonic()-start, 3),
                      stdout=result.stdout, stderr=result.stderr)
        results.append(record)
        print(name + ': ' + ('PASS' if result.returncode == 0 else 'FAIL'), flush=True)
        if result.returncode:
            sys.stderr.write(result.stdout + result.stderr)
            raise SystemExit(result.returncode)
    sources = list(HERE.rglob('*.py')) + [BASE/'global_core_sat.py', BASE.parent/'tiling_143.json']
    hashes = {os.path.relpath(p, HERE): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(sources)}
    report = dict(format='vertex-phase-finite-controls-v1', status='PASS',
                  solver_controls=args.solver, checks=results, source_sha256=hashes,
                  target_status={'3431': 'OPEN', '5063': 'OPEN'},
                  full_Erdos634_solved=False,
                  scope='Finite exact arithmetic, positive and rejection controls only; '
                        'not a target tiling, unrestricted UNSAT proof, or formal verification of the notes.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: ' + str(len(results)) + ' finite controls; both targets remain open.')


if __name__ == '__main__':
    main()
