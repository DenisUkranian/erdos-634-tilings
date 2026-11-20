#!/usr/bin/env python3
"""Replay the exact global restrictions, without optimization or tile search.

The finite checks support the explicitly scoped proofs. Neither target's
unrestricted tiling question is decided by this package.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
CONTINUATION = HERE.parent
ACTUAL_MEDIAN = CONTINUATION / 'charge-transport/geometry/ACTUAL_MEDIAN_REPLAY.json'


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Use ordinary Python with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    jobs = [
        ('complete_spine_catalogues_and_positive_control',
         'spine/native_spine.py', [], 'spine/SPINE_CATALOGUE.json'),
        ('closed_gate_mates_and_actual_through_contacts',
         'spine/verify_spine_restrictions.py', [],
         'spine/SPINE_RESTRICTIONS_REPLAY.json'),
        ('both_gates_exclude_three_odd_blocks_in_spine',
         'spine/verify_both_gate_torus.py', [], 'spine/BOTH_GATE_REPLAY.json'),
        ('universal_single_cell_gate_capacities',
         'median/verify_gate_capacity.py', [], 'median/GATE_CAPACITY_REPLAY.json'),
        ('5063_minimal_mode_requires_charged_even_branch',
         'median/verify_remote_zero_minimum.py',
         [str(HERE / 'median/REMOTE_ZERO_MIN_43_IPM.json')],
         'median/REMOTE_ZERO_MINIMUM_REPLAY.json'),
        ('joint_quotient_periods_and_actual_path_controls',
         'topology/verify_joint_null.py', ['--known-replay', str(ACTUAL_MEDIAN)],
         'topology/JOINT_NULL_REPLAY.json'),
        ('actual_mixed_syllable_countercontrols',
         'topology/check_mixed_syllable.py',
         ['--continuation', str(CONTINUATION), '--known-replay', str(ACTUAL_MEDIAN)],
         'topology/MIXED_SYLLABLE_REPLAY.json'),
    ]
    checks = []
    with tempfile.TemporaryDirectory(prefix='erdos634-global-closure-') as folder:
        for name, script, fixed, frozen in jobs:
            output = Path(folder) / (name + '.json')
            command = [sys.executable, '-B', str(HERE / script), *fixed,
                       '--out', str(output)]
            started = time.monotonic()
            result = subprocess.run(command, cwd=HERE, text=True,
                                    capture_output=True, timeout=120)
            if result.returncode:
                sys.stderr.write(result.stdout + result.stderr)
                raise SystemExit(result.returncode)
            actual = json.loads(output.read_text())
            expected = json.loads((HERE / frozen).read_text())
            if actual != expected:
                raise AssertionError('Saved exact report differs: ' + frozen)
            checks.append(dict(name=name, script=script,
                               exit_code=result.returncode,
                               seconds=round(time.monotonic() - started, 3),
                               saved_report_equal=True))
            print(name + ': PASS', flush=True)
    sources = [p for p in HERE.rglob('*') if p.is_file()
               and p.suffix in ('.py', '.json', '.md') and p.name != 'REPLAY.json']
    hashes = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(sources)}
    report = dict(
        format='global-geometric-restrictions-exact-replay-v1',
        status='PASS', checks=checks, source_sha256=hashes,
        target_status={'3431': 'OPEN', '5063': 'OPEN'},
        excluded_subclass='No occupied exterior-free short nodes in either '
                          'prime tree, together with odd population 3c.',
        additional_5063_exclusion='Odd population 3c with every exterior-free '
                                  'even terminal node balanced.',
        unrestricted_nonexistence_certificate=False,
        complete_target_tiling_certificate=False,
        full_Erdos634_solved=False,
        scope='Exact arithmetic certificates, complete positive controls, '
              'and the finite parts of the stated global geometric proofs. '
              'No numerical optimization or target placement search is run.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: seven exact suites; original targets 3431 and 5063 remain OPEN.')


if __name__ == '__main__':
    main()
