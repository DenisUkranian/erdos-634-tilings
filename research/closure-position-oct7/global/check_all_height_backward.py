#!/usr/bin/env python3
"""Independent reverse-height inventory check with every nonzero level >=26.

The edge model comes from exact coordinates in the frozen independent model.
The forward strengthened producer is not imported. No resource cutoff.
"""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import json
import time
import check_full_inventory_backward as model

HERE = Path(__file__).resolve().parent


def floor_population(height):
    return 11 if height == 0 else 26


@lru_cache(maxsize=None)
def population(height, size):
    for n in range(floor_population(height), 155, 13):
        if n >= size and (n-size) % 2 == 0:
            return n
    return 155


def backward(L, U, groups):
    top_b = model.solve_long(model.LONG_B, model.target(U+1))
    assert top_b is not None
    states = {(model.ZERO, top_b): 0}
    layers = []
    for h in range(U, L-1, -1):
        remaining_minimum = sum(floor_population(k) for k in range(L, h))
        new = {}
        for (a_next, b), used in states.items():
            known = model.plus(model.apply(model.SHORT_B, b), model.apply(model.LONG_A, a_next))
            required = tuple(x % 13 for x in model.minus(model.target(h), known))
            available = 154-used-remaining_minimum
            b_size = model.norm(b)
            for a, a_size, short in groups.get(required, ()):
                n = population(h, a_size+b_size)
                if n > available:
                    continue
                rest = model.minus(model.minus(model.target(h), known), short)
                b_previous = model.solve_long(model.LONG_B, rest)
                assert b_previous is not None
                if h == L and (b_previous != model.ZERO or model.apply(model.LONG_A, a) != model.target(L-1)):
                    continue
                key = a, b_previous
                total = used+n
                if total < new.get(key, 155):
                    new[key] = total
        states = new
        layers.append({'height': h, 'states': len(states)})
        if not states:
            return {'support': [L, U], 'status': 'EXACT_UNSAT', 'layers': layers}
    return {'support': [L, U], 'status': 'FORMAL_FEASIBLE', 'layers': layers}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--witness-source', type=Path,
                        default=HERE.parent/'oct8-structural'/'all_height_direction_probe.json')
    args = parser.parse_args()
    started = time.monotonic()
    assert 11+6*26 == 167 > 154  # Seven or more heights are already impossible.
    K = 6
    bound = 154-(11+26*(K-1))+26
    assert bound == 39
    groups = defaultdict(list)
    for a in model.vectors_l1(bound):
        short = model.apply(model.SHORT_A, a)
        groups[tuple(x % 13 for x in short)].append((a, model.norm(a), short))
    negatives = []
    for L in range(-5, 1):
        record = backward(L, L+5, groups)
        assert record['status'] == 'EXACT_UNSAT', record
        negatives.append(record)
    raw = args.witness_source.read_bytes()
    source = json.loads(raw)
    candidates = [r for r in source['records'] if r['support'][1]-r['support'][0]+1 == 5]
    assert {tuple(r['support']) for r in candidates} == {(L, L+4) for L in range(-4, 1)}
    positives = []
    for record in candidates:
        model.replay_witness(record)  # Adds exact-coordinate-derived oriented edge signatures.
        for block in record['witness']:
            assert block['n'] >= floor_population(block['h'])
        positives.append({'support': record['support'], 'population': 154, 'status': 'PASS'})
    report = {'status': 'PASS', 'full_Erdos634_solved': False, 'N154_solved': False,
              'scope': 'Exact inventories strengthened by the independently reviewed nonzero-height >=26 theorem',
              'resource_cutoffs': False, 'excluded_six_height_supports': len(negatives),
              'positive_five_height_formal_controls': len(positives),
              'seven_height_minimum': 167, 'max_occupied_short_heights': 5,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'geometry_source_sha256': hashlib.sha256(Path(model.__file__).read_bytes()).hexdigest(),
              'witness_source_name': args.witness_source.name,
              'witness_source_sha256': hashlib.sha256(raw).hexdigest(),
              'seconds': round(time.monotonic()-started, 6),
              'negative_records': negatives, 'positive_records': positives}
    (HERE/'all_height_backward_verified.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'excluded_six_height_supports', 'positive_five_height_formal_controls', 'seconds')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O so exact assertions execute.')
    main()
