#!/usr/bin/env python3
"""Replay the full positive control and audit saved negative-search scopes.

This is deliberately not an infeasibility verifier for either target.
The target files contain only resource stops and portable restart rows.
"""
from collections import Counter
import gzip
import importlib.util
import json
from pathlib import Path

import scoped_physical_search as scoped
import permanent_physical_search as permanent

HERE = Path(__file__).resolve().parent
ROOT = scoped.ROOT
spec = importlib.util.spec_from_file_location('independent_positive_geometry',
    ROOT / 'research/2026-11-20/semiprimes/continuation/global-endpoints/verify_endpoint_tiling.py')
positive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(positive)


def main():
    data = json.loads((HERE/'CONTROL_143.json').read_text())
    result = positive.check(data)
    assert result['verified_positive_tiling'] and result['endpoint_residual_count'] == 0
    scoped.ScopedGeometry.mode = '143-control'
    geometry = scoped.ScopedGeometry(*data['sides'])
    tiles = [(tuple(q), h, j, s) for q, h, j, s in data['tiles']]
    assert all(geometry.admissible(tile) for tile in tiles)
    assert permanent.overlaps(geometry, tiles, range(len(tiles))) == []
    # The positive geometry replay proves the packing is disjoint; this
    # cross-check therefore catches an incompatible orientation convention.
    inventory = Counter((h % 2, s*(-1 if j % 2 else 1)) for q,h,j,s in tiles)
    assert inventory == {(0,1):18, (0,-1):20, (1,1):49, (1,-1):56}
    triangle = permanent.integer_vertices(geometry, tiles[0])
    assert permanent.overlap(triangle, triangle)
    reports = []
    for folder in sorted((HERE/'checkpoints').iterdir()):
        status = json.loads((folder/'status.json').read_text())
        rows = json.loads(gzip.decompress((folder/'complete_rows.json.gz').read_bytes()))
        row_tuples = [(tuple(p),h,j) for p,h,j in rows['complete_rows']]
        assert len(row_tuples) == len(set(row_tuples))
        assert len(row_tuples) == status.get('complete_rows', status.get('rows'))
        assert all(len(p)==3 and all(type(v) is int for v in (*p,h,j))
                   and p[2]>=0 and 0<=j<3 for p,h,j in row_tuples)
        assert status['full_target_excluded'] is False
        assert status['status'] in ('round-limit','column-resource-limit','solver-inconclusive')
        if 'row_count' in rows:
            assert rows['row_count'] == len(row_tuples)
            assert rows['mode'] == status['mode']
            assert rows['odd_population'] == status['odd_population']
        reports.append({'path':str(folder.relative_to(HERE)), 'mode':status['mode'],
            'status':status['status'], 'columns':status['columns'],
            'complete_rows':len(row_tuples), 'target_excluded':False})
    output = {'status':'PASS', 'positive_control':result,
        'positive_control_sign_populations':{str(k):v for k,v in sorted(inventory.items())},
        'scope_records':reports, 'full_3431_excluded':False, 'full_5063_excluded':False,
        'scope':'Independent exact metric, containment, area and full physical current verification of the complete 143 control; conditional-filter and overlap cross-checks; format and honest-scope audit of saved inconclusive target runs. No target search or infeasibility certificate is replayed.'}
    (HERE/'PHYSICAL_CONTROLS_REPLAY.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
