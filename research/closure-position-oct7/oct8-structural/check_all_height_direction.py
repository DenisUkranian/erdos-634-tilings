#!/usr/bin/env python3
"""Replay all six-height exclusions and five-height formal controls."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'dual'))
from check_directional_supports import replay
from all_height_direction_dp import run_variable


def main():
    records = []
    for k in (6, 5):
        for lo in range(1 - k, 1):
            record = run_variable(lo, lo + k - 1, seconds=300)
            expected = 'EXACT_UNSAT' if k == 6 else 'EXACT_FORMAL_FEASIBLE'
            assert record['status'] == expected
            if k == 5:
                replay(record)
                assert all(b['n'] >= 26 for b in record['witness'] if b['h'] != 0)
            records.append(record)
        print(json.dumps({'status': 'PASS', 'height_count': k,
                          'supports': k}), flush=True)
    (HERE / 'all_height_direction_probe.json').write_text(
        json.dumps({'records': records}, indent=2) + '\n')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O so exact assertions execute.')
    main()
