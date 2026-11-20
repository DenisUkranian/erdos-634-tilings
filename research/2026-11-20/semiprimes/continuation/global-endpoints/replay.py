#!/usr/bin/env python3
"""Finite exact checks only; no large inconclusive search is launched."""
from copy import deepcopy
import json
from pathlib import Path
from audit_semiprimes import run
from verify_endpoint_dual import self_test
from verify_endpoint_tiling import check


def main():
    if not __debug__:
        raise RuntimeError('Run exact verification without -O.')
    root = Path(__file__).resolve().parent
    self_test()
    data = json.loads((root/'tiling_143.json').read_text())
    positive = check(data)
    for corruption in ('remove', 'duplicate', 'translate'):
        changed = deepcopy(data)
        if corruption == 'remove':
            changed['tiles'].pop()
        elif corruption == 'duplicate':
            changed['tiles'][0] = deepcopy(changed['tiles'][1])
        else:
            changed['tiles'][0][0][0] += 1
        try:
            check(changed)
        except AssertionError:
            pass
        else:
            raise AssertionError('Corrupted data accepted: '+corruption)
    expected = json.loads((root/'census_million.json').read_text())
    census = run(1_000_000)
    # JSON normalizes tuple records to lists.
    assert json.loads(json.dumps(census)) == expected
    print(json.dumps(dict(
        positive_control=positive,
        rejected_corruptions=3,
        independently_enumerated_semiprimes=census['total_semiprimes'],
        residual_F2=[r['N'] for r in census['residual_F2']],
        target3431='OPEN', target5063='OPEN',
        scope='Finite exact checks; no target tiling or global obstruction supplied'
    ), indent=2))


if __name__ == '__main__':
    main()
