#!/usr/bin/env python3
"""Replay exact physical-cut controls and the stated abstract relaxation.

No optimizer or target placement search is run. Passing these checks is
not a certificate of nonexistence or a tiling for 3431 or 5063.
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


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Use ordinary Python with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    jobs = [
        ('physical_cut_transport', 'flux/verify_flux.py', 'flux/FLUX_REPLAY.json'),
        ('charged_parent_tradeoff', 'flux/verify_parent_tradeoff.py',
         'flux/CHARGED_PARENT_REPLAY.json'),
        ('two_complete_actual_median_controls', 'geometry/verify_actual_median.py',
         'geometry/ACTUAL_MEDIAN_REPLAY.json'),
        ('even_corner_and_base_gap_controls', 'geometry/verify_even_corner.py',
         'geometry/EVEN_CORNER_REPLAY.json'),
        ('exact_abstract_axis_flow', 'joint/abstract_flow.py', 'joint/ABSTRACT_FLOW.json'),
    ]
    checks = []
    with tempfile.TemporaryDirectory(prefix='erdos634-charge-transport-') as folder:
        for name, script, frozen in jobs:
            output = Path(folder)/(name+'.json')
            command = [sys.executable, '-B', script, '--out', str(output)]
            started = time.monotonic()
            result = subprocess.run(command, cwd=HERE, text=True,
                                    capture_output=True, timeout=120)
            if result.returncode:
                sys.stderr.write(result.stdout+result.stderr)
                raise SystemExit(result.returncode)
            actual = json.loads(output.read_text())
            expected = json.loads((HERE/frozen).read_text())
            if actual != expected:
                raise AssertionError('Exact saved report differs: '+frozen)
            checks.append(dict(name=name, command=[script, '--out', '<temporary>'],
                               exit_code=result.returncode,
                               seconds=round(time.monotonic()-started, 3),
                               saved_report_equal=True,
                               stdout=result.stdout, stderr=result.stderr))
            print(name+': PASS', flush=True)
    sources = [p for p in HERE.rglob('*') if p.is_file()
               and p.suffix in ('.py', '.json') and p.name != 'REPLAY.json']
    hashes = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(sources)}
    report = dict(format='charge-transport-exact-controls-v1', status='PASS',
                  checks=checks, source_sha256=hashes,
                  target_status={'3431': 'OPEN', '5063': 'OPEN'},
                  unrestricted_nonexistence_certificate=False,
                  complete_target_tiling_certificate=False,
                  full_Erdos634_solved=False,
                  scope='Exact finite transport, geometric controls and integer '
                        'axis-flow assignments. The assignments have no common '
                        'endpoint coordinates or planar tiling realization. '
                        'The conditional 3c structure does not exclude that mode.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: five exact suites; 3431 and 5063 remain OPEN.')


if __name__ == '__main__':
    main()
