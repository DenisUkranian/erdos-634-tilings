#!/usr/bin/env python3
"""I120 signature and local checks; no geometric existence claim."""
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    'f3_signature_polynomials',
    HERE.parent / 'f3-descent-attempt' / 'check_full_signature.py')
POLY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLY)
add, mul, term = POLY.add, POLY.mul, POLY.term


def boundary_counts(length, a, b, c):
    return [[i, j, (length-a*i-b*j)//c]
            for i in range(length//a+1)
            for j in range(length//b+1)
            if length-a*i-b*j >= c and (length-a*i-b*j) % c == 0]


def fans(alpha_coefficient, pi_over_three_coefficient):
    return [[r, s, t]
            for r in range(7) for s in range(7) for t in range(4)
            if r-s == alpha_coefficient
            and s+2*t == pi_over_three_coefficient]


def replay():
    a, b, c = term(a=1), term(b=1), term(c=1)
    T, X, Xi, neg = term(t=1), term(x=1), term(x=-1), term(-1)
    T2 = mul(T, T)
    P = add(a, mul(b, T), mul(neg, mul(c, X)))
    Q = add(mul(neg, a), mul(b, T2), mul(c, Xi))
    boundary = add(mul(b, add(a, mul(term(2), b))),
                   mul(mul(b, c), mul(T2, X)),
                   mul(neg, mul(mul(b, c), mul(T, Xi))))
    formal = add(mul(mul(neg, a), P),
                 mul(add(mul(c, X), mul(neg, mul(b, T))), Q))
    discrepancy = add(formal, mul(neg, boundary))
    if discrepancy:
        raise ValueError(discrepancy)
    corner_fans = {'base': fans(1, 0), 'apex': fans(-2, 3)}
    if corner_fans != {'base': [[1,0,0]], 'apex': [[1,3,0]]}:
        raise ValueError(corner_fans)
    fixtures = []
    for aa, bb, cc in ((8,7,13), (5,3,7), (3,5,7),
                       (24,11,31), (11,24,31), (112,75,163)):
        if cc*cc != aa*aa+aa*bb+bb*bb:
            raise ValueError('Invalid norm fixture')
        for m in (1,2,3,7):
            count = bb*(aa+2*bb)*m*m
            unplaced = m*(aa+bb+cc)
            if count < unplaced or (count-unplaced) % 2:
                raise ValueError('Invalid padding')
            fixtures.append({'tile': [aa,bb,cc], 'scale': m,
                             'target_count': count,
                             'unplaced_inventory_count': unplaced,
                             'half_turn_pairs': (count-unplaced)//2})
    counts = {str(length): boundary_counts(length, 8, 7, 13)
              for length in (91,154)}
    if len(counts['91']) != 6 or len(counts['154']) != 17:
        raise ValueError('Boundary enumeration changed')
    pure_beta_fans = {str(k): fans(-k, k) for k in range(4)}
    if pure_beta_fans != {str(k): [[0,k,0]] for k in range(4)}:
        raise ValueError('Pure-beta fan enumeration changed')
    adjacency_counts = {
        length: [row for row in rows if row[2] >= 2]
        for length, rows in counts.items()}
    if adjacency_counts['91'] != [[0,0,7], [2,7,2], [3,4,3], [4,1,4]]:
        raise ValueError('I120 two-longest-edge enumeration changed')
    if len(adjacency_counts['154']) != 14:
        raise ValueError('I120 base enumeration changed')
    return {'status': 'PASS', 'symbolic_remainder_terms': 0,
            'corner_fans': corner_fans,
            'boundary_counts_154': counts,
            'pure_beta_fans': pure_beta_fans,
            'boundary_counts_after_adjacency_154': adjacency_counts,
            'boundary_adjacency_scope':
                'Necessary condition only; see BOUNDARY_ADJACENCY.md',
            'fixtures': fixtures,
            'geometric_status_154': 'UNRESOLVED',
            'geometric_tiling_claimed': False,
            'full_Erdos634_solved': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    output = json.dumps(replay(), indent=2)+'\n'
    if args.report is not None:
        args.report.write_text(output)
    print(output, end='')
