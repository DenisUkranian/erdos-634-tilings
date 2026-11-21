#!/usr/bin/env python3
"""Replay exact bank, pair-reserve, and integer-image certificates only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
CHECKS=(
    'charged-cells/verify_charged_countercontrols.py',
    'charged-cells/verify_balanced_six_patch.py',
    'arithmetic/verify_integer_gate_image.py',
    'long-banks/verify_long_banks.py',
    'global-geometry/verify_bank_pair_reserves.py',
    'arithmetic/verify_long_bank_audit.py',
)


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run ordinary Python with assertions enabled.')
    records=[]
    for command in CHECKS:
        start=time.monotonic()
        result=subprocess.run([sys.executable,str(HERE/command)],cwd=ROOT,
                              text=True,capture_output=True,timeout=180)
        if result.returncode:
            sys.stderr.write(result.stdout+result.stderr)
            raise RuntimeError(f'Failed exact replay: {command}')
        records.append(dict(command=command,status='PASS',
                            seconds=round(time.monotonic()-start,3),
                            stdout=result.stdout,stderr=result.stderr))
        print('PASS '+command,flush=True)
    report=dict(status='ALL_EXACT_CONTROLS_PASS',checks=records,
                full_3431_excluded=False,full_5063_excluded=False,
                scope='Exact certificates, positive tilings, and specified packing controls. No exhaustive target packing enumeration, external refereeing, or proof-assistant verification is claimed.')
    (HERE/'REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print('INTEGER_CLOSURE_BANK_AND_IMAGE_REPLAY=PASS',flush=True)


if __name__=='__main__':main()
