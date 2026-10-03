#!/usr/bin/env python3
"""Replay symbolic identities, positive certificates and corrupted-certificate rejection."""
import argparse
import copy
import json
from math import gcd, isqrt
from pathlib import Path
from construct import construct
from verify import verify
from check_macro import check


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    macros = 0
    for a in range(1, 301):
        for b in range(a+1, 501):
            if gcd(a, b) != 1:
                continue
            c = isqrt(a*a+a*b+b*b)
            if c*c == a*a+a*b+b*b:
                check(a, b, c)
                macros += 1
    positives = []
    for a, b, c, m in [(3, 5, 7, 1), (3, 5, 7, 2), (5, 16, 19, 1)]:
        positives.append(verify(construct(a, b, c, m)))
    base = construct(3, 5, 7)
    bads = []
    bad = copy.deepcopy(base)
    bad['triangles'][0] = bad['triangles'][1]
    bads.append(('duplicate unit triangle', bad))
    bad = copy.deepcopy(base)
    bad['triangles'].pop()
    bads.append(('missing unit triangle', bad))
    bad = copy.deepcopy(base)
    bad['triangles'][0][0][0] = '1/10'
    bads.append(('moved vertex', bad))
    bad = copy.deepcopy(base)
    bad['target'][0][0] = '1/10'
    bads.append(('altered target', bad))
    bad = copy.deepcopy(base)
    bad['multiplier'] = 2
    bads.append(('wrong multiplier', bad))
    rejected = []
    for label, data in bads:
        try:
            verify(data)
        except ValueError:
            rejected.append(label)
        else:
            raise RuntimeError(f'Invalid certificate accepted: {label}')
    try:
        construct(5, 3, 7)
    except ValueError:
        rejected.append('reversed unproved orientation')
    else:
        raise RuntimeError('Unproved orientation accepted')
    report = {'status': 'PASS', 'macro_triples': macros,
              'expanded_checks': positives, 'rejected_mutations': rejected,
              'full_Erdos634_solved': False, 'external_peer_review': False,
              'scope': 'Finite regression checks support, but do not replace, PROOF.md.'}
    text = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
