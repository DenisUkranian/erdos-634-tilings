#!/usr/bin/env python3
"""Export compact, deterministic, nonexecutable row and point checkpoints."""
import argparse
import gzip
import json
from pathlib import Path
import pickle


def save(path, data):
    raw = (json.dumps(data, separators=(',', ':'), sort_keys=True) + '\n').encode()
    Path(path).write_bytes(raw)
    Path(str(path) + '.gz').write_bytes(gzip.compress(raw, mtime=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trusted_pickle')
    parser.add_argument('rows_json')
    parser.add_argument('points_json')
    args = parser.parse_args()
    with Path(args.trusted_pickle).open('rb') as f:
        data = pickle.load(f)
    rows = sorted(data['complete_rows'])
    assert len(rows) == len(set(rows))
    metadata = dict(sides=data['sides'], N=data['N'],
                    source_iteration=data['iteration'], source_status=data['status'])
    save(args.rows_json, dict(format='global-integer-complete-rows-v1',
                             **metadata, row_count=len(rows),
                             source_column_count=len(data['tiles']), complete_rows=rows))
    points = data.get('coverage_points', [])
    save(args.points_json, dict(format='exact-point-coverage-v1',
                               sides=data['sides'], N=data['N'],
                               point_count=len(points), coverage_points=points))
    print(json.dumps(dict(rows=len(rows), points=len(points), **metadata), indent=2))


if __name__ == '__main__':
    main()
