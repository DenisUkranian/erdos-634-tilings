#!/usr/bin/env python3
"""Replay the exact 19320 certificate and meaningful verifier mutations."""
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    maker = load('staircase_constructor', HERE/'construct_staircase.py')
    verifier = load('staircase_verifier', HERE/'verify_spatial.py')
    legacy = load('legacy_quadratic_verifier',
                  HERE.parent/'group2-nested-corners'/'verify.py')
    raw = (HERE/'f3-19320.json.gz').read_bytes()
    data = json.loads(gzip.decompress(raw))
    report = verifier.verify(data)
    report['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    (HERE/'f3-19320-geometric-report.json').write_text(json.dumps(report, indent=2)+'\n')
    small = maker.construct(5, 3, 7, 1)
    small_spatial = verifier.verify(small)
    small_quadratic = legacy.verify(small)
    mutations = {}
    for name in ('duplicate', 'missing', 'wrong_target', 'moved_vertex'):
        bad = copy.deepcopy(small)
        if name == 'duplicate':
            bad['triangles'][-1] = copy.deepcopy(bad['triangles'][0])
        elif name == 'missing':
            bad['triangles'].pop()
        elif name == 'wrong_target':
            bad['target'][1][0] = '50'
        else:
            bad['triangles'][0][0][0] = '1'
        try:
            verifier.verify(bad)
        except ValueError as error:
            mutations[name] = str(error)
        else:
            raise RuntimeError(f'checker accepted {name} mutation')
    try:
        maker.construct(24, 11, 31, 1)
    except ValueError:
        primitive_rejected_by_recipe = True
    else:
        raise RuntimeError('recipe unexpectedly accepted scale one')
    exact_max_checks = 0
    for a in range(2, 25):
        for b in range(1, a):
            for t in range(1, 60):
                cells = maker.staircase_cells(a, b, t)
                actual = max(b*(i+1)+a*(j+1) for i, j in cells)
                expected = b+a*((t+b-1)//b)
                if actual != expected:
                    raise RuntimeError('closed-form staircase maximum failed')
                exact_max_checks += 1
    result = {
        'status': 'PASS', 'certificate': report,
        'small_control': {'N': 264,
                          'spatial_status': small_spatial['status'],
                          'independent_quadratic_status': small_quadratic['status']},
        'mutations_rejected': mutations,
        'staircase_maximum_integer_controls': exact_max_checks,
        'primitive_4830_rejected_by_this_recipe': primitive_rejected_by_recipe,
        'primitive_4830_status': 'UNRESOLVED',
        'full_Erdos634_solved': False, 'external_peer_review': False}
    (HERE/'VERIFIED_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
