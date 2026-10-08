#!/usr/bin/env python3
"""Regenerate and independently verify the restricted 154 certificate.
No network access or mathematical optimizer is used.
"""
from __future__ import annotations
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED_PROOF_SHA256 = '946841daa87f519949d1a882b7ebdb5f1d30aec9f4e897dc7b55f361b8af59e3'

def command(*args: str) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)

def main() -> None:
    if not __debug__:
        raise RuntimeError('Python optimization disables required checks')
    if sys.byteorder != 'little':
        raise RuntimeError('The binary exchange format in this package is little-endian')
    compiler = shutil.which('g++')
    if compiler is None:
        raise RuntimeError('A C++17-capable g++ compiler is required')
    for script in ('twolevel154_build.py', 'independent_geometry_check.py',
                   'twolevel154_matrix.py', 'audit_matrix.py', 'export_sparse.py'):
        command(sys.executable, str(ROOT / script))
    proof = ROOT / 'twolevel154_steps.txt'
    with gzip.open(ROOT / 'twolevel154_steps.txt.gz', 'rb') as inp, proof.open('wb') as out:
        shutil.copyfileobj(inp, out)
    digest = hashlib.sha256(proof.read_bytes()).hexdigest()
    if digest != EXPECTED_PROOF_SHA256:
        raise RuntimeError('The retained proof transcript failed its integrity check')
    command(compiler, '-O2', '-std=c++17', str(ROOT / 'verify_twolevel.cpp'),
            '-o', str(ROOT / 'verify_twolevel'))
    command(str(ROOT / 'verify_twolevel'))
    command(sys.executable, str(ROOT / 'positive_controls.py'))
    reports = {}
    for name in ('twolevel154_geometry_audit.json', 'matrix_audit.json',
                 'twolevel154_replay.json', 'positive_controls.json'):
        reports[name] = json.loads((ROOT / name).read_text())
    if reports['twolevel154_replay.json']['steps_checked'] != 678493:
        raise RuntimeError('Unexpected retained proof length')
    result = {
        'status': 'ALL_RETAINED_EXACT_CHECKS_PASS',
        'scope': 'No tiling in the prescribed adjacent short-height band for the fixed 154 candidate; see PROOF.md for the three-height corollary.',
        'N154_fully_decided': False,
        'N4830_decided': False,
        'full_Erdos634_solved': False,
        'external_referee_review': False,
        'proof_sha256': digest,
        'reports': reports,
    }
    (ROOT / 'REPLAY_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])

if __name__ == '__main__':
    main()
