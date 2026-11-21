#!/usr/bin/env python3
"""Retain geometric restart sources, not an asserted SAT formula or refutation.

The unrestricted driver regenerates all local candidate catalogues and budgets.
Generated-only columns, solver assertions and current-pool auxiliary variables
are deliberately omitted. An independent semantic audit applies to the newly
generated full snapshot, never to this compact source file itself.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path


def compact(data, source_sha256):
    needed = set()
    for record in data.get('corner_roots', []):
        needed.add(record['tile'])
    for record in data.get('whole_edge_obligations', []):
        needed.add(record['tile'])
    needed.update(data.get('whole_edge_complete_tiles', []))
    for pair in data.get('overlap_pairs', []):
        needed.update(pair)
    for record in data.get('supported_long_cycle_cuts', []):
        needed.update(record['indices'])
    for record in data.get('general_area_cycle_cuts', []):
        needed.update(record['indices'])
        for edge in record['edges']:
            needed.add(edge['representative'])
            needed.update(edge['selected_owners'])
    old_ids = sorted(needed)
    renumber = {old: new for new, old in enumerate(old_ids)}
    result = dict(
        format='geometric-restart-sources-v1',
        sides=data['sides'],
        root=data.get('root'),
        tiles=[data['tiles'][i] for i in old_ids],
        complete_rows=data.get('complete_rows', []),
        corner_roots=[dict(tile=renumber[r['tile']], point=r['point'])
                      for r in data.get('corner_roots', [])],
        whole_edge_obligations=[dict(tile=renumber[r['tile']], edge_index=r['edge_index'])
                               for r in data.get('whole_edge_obligations', [])],
        whole_edge_complete_tiles=[renumber[i] for i in data.get('whole_edge_complete_tiles', [])],
        overlap_pairs=[[renumber[i] for i in pair] for pair in data.get('overlap_pairs', [])],
        supported_long_cycle_cuts=[dict(indices=[renumber[i] for i in r['indices']])
                                  for r in data.get('supported_long_cycle_cuts', [])],
        general_area_cycle_cuts=[],
        general_area_cycle_rule='integral-tile-area-and-two-signed-characters-v1',
        restart_scope=dict(
            original_snapshot_sha256=source_sha256,
            original_candidate_count=len(data['tiles']),
            stored_geometric_tile_count=len(old_ids),
            arbitrary_assertions_included=False,
            previous_root_literals_imported=False,
            original_formula_reproduced_bit_for_bit=False,
            catalogue_and_budget_regeneration_required=True,
            target_exclusion=False))
    for record in data.get('general_area_cycle_cuts', []):
        new = deepcopy(record)
        new['indices'] = sorted(renumber[i] for i in record['indices'])
        for edge in new['edges']:
            edge['representative'] = renumber[edge['representative']]
            edge['selected_owners'] = sorted(renumber[i] for i in edge['selected_owners'])
        result['general_area_cycle_cuts'].append(new)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    if args.source.suffix == '.gz':
        raw = gzip.decompress(raw)
    source = json.loads(raw)
    result = compact(source, hashlib.sha256(raw).hexdigest())
    encoded = (json.dumps(result, separators=(',', ':')) + '\n').encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(gzip.compress(encoded, mtime=0) if args.output.suffix == '.gz' else encoded)
    print(json.dumps(dict(status='GEOMETRIC_SOURCES_EXPORTED', **result['restart_scope'],
                          compressed_bytes=args.output.stat().st_size), sort_keys=True))


if __name__ == '__main__':
    main()
