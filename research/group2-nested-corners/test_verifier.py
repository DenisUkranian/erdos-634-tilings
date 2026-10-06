#!/usr/bin/env python3
"""A retained positive certificate and an area-preserving overlap mutation."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

from verify import verify


def main():
    if not __debug__:
        raise SystemExit('Run without -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    original = json.loads(Path(__file__).with_name('f3-990.json').read_text())
    positive = verify(original)
    mutated = deepcopy(original)
    mutated['triangles'][1] = deepcopy(mutated['triangles'][0])
    try:
        verify(mutated)
    except ValueError as exc:
        if 'Positive-area overlap' not in str(exc):
            raise RuntimeError(f'Mutation failed at an unexpected gate: {exc}') from exc
        rejected = str(exc)
    else:
        raise RuntimeError('Duplicate tile preserving count and area was accepted')
    report = {'status': 'PASS', 'positive_N': positive['N'],
              'negative_duplicate_preserves_count_congruence_containment_and_area': True,
              'negative_rejection': rejected, 'full_Erdos634_solved': False}
    output = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
