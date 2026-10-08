#!/usr/bin/env python3
"""Replay the positionally strengthened 154 direction inventory."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'dual'))
from check_directional_supports import replay
from extreme_direction_dp import run_variable


def main():
    records = []
    for k in (8, 7):
        for lo in range(1 - k, 1):
            hi = lo + k - 1
            record = run_variable(lo, hi, seconds=300)
            expected = 'EXACT_UNSAT' if k == 8 else 'EXACT_FORMAL_FEASIBLE'
            assert record['status'] == expected
            if k == 7:
                replay(record)
                for block in record['witness']:
                    h = block['h']
                    if (h == lo and lo < 0) or (h == hi and hi > 0):
                        assert block['n'] >= 26
            records.append(record)
        print(json.dumps({'status': 'PASS', 'height_count': k,
                          'supports': k}), flush=True)
    report = {
        'status': 'PASS', 'full_Erdos634_solved': False, 'N154_solved': False,
        'excluded_height_8_supports': 8, 'formal_height_7_controls': 7,
        'max_occupied_short_heights': 7, 'records': records,
    }
    (HERE / 'extreme_direction_verified.json').write_text(
        json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O so exact assertions execute.')
    main()
