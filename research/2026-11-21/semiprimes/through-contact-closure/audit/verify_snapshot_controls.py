#!/usr/bin/env python3
"""Stdlib semantic audit of one frozen physical143 model and corrupt controls."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from verify_snapshot import SnapshotAudit,logical


HERE = Path(__file__).resolve().parent


def main():
    assert logical('((_ pble 1 1 2) x0 x1)') == logical('((_ pble 1 2 1) x1 x0)')
    assert logical('((_ pble 1 1 2) x0 x1)') != logical('((_ pble 1 1 2) x1 x0)')
    raw = (HERE/'CONTROL_143_BOUNDARY_MODEL.json').read_bytes()
    model = json.loads(raw)
    valid = SnapshotAudit(model).run()
    controls = {}
    bad = deepcopy(model)
    bad['permanent_assertions'].append('(=> x0 false)')
    controls['unjustified_permanent_assertion'] = bad
    bad = deepcopy(model)
    bad['charge_reserves'][0]['bound'] += 1
    controls['incorrect_global_charge_capacity'] = bad
    bad = deepcopy(model)
    next(r for r in bad['fan_paths'] if r['term'].startswith('cf'))['expression'] = 'false'
    controls['altered_complete_fan_recursion'] = bad
    bad = deepcopy(model)
    bad['complete_rows'].append([[10,10,0],3,0])
    controls['incomplete_endpoint_catalogue'] = bad
    bad = deepcopy(model)
    bad['interior_point_cliques'] = [dict(point=[0,0],indices=[0,1])]
    controls['false_strict_interior_clique'] = bad
    bad = deepcopy(model)
    bad['root_assumptions'] = []
    controls['lost_root_assumptions'] = bad
    bad = deepcopy(model)
    bad['tiles'][0] = bad['tiles'][1]
    controls['duplicate_whole_tile_variable'] = bad
    rejected = []
    for name,bad in controls.items():
        try:
            SnapshotAudit(bad).run()
        except (AssertionError,ValueError,KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Accepted corrupt model: '+name)
    result = dict(status='PASS',frozen_model_sha256=hashlib.sha256(raw).hexdigest(),
                  weighted_literal_pairing_checks=2,
                  positive_model=valid,rejected_corrupt_models=rejected,
                  scope='Full clause regeneration for the frozen143 boundary/root model, plus seven corrupt-model rejections; no SMT solver or target exclusion.')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
