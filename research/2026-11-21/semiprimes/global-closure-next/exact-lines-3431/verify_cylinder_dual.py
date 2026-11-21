#!/usr/bin/env python3
"""Exact, optimizer-free independent box enumeration of a cylinder dual.

This checker does not import the discovery catalogue or its row-interval
generator.  It visits every anchor in the integer bounding box for every
orientation and tests all three actual vertices against all board sides.
All pricing uses bounded int64 arithmetic; final comparisons use Python
integers.  A complete 143 tiling is a positive geometric control.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys
import time
import numpy as np

U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def ceildiv(x, d):
    return -((-x)//d)


def control_143():
    """Transform a complete standard-frame tiling into the path frame."""
    where = ROOT/'research/2026-11-20/semiprimes/continuation'
    sys.path.insert(0, str(where/'global-closure/spine'))
    from native_spine import SpineCatalogue, control_143 as physical_control
    source = where/'global-endpoints/tiling_143.json'
    source_report = physical_control(source)
    cat = SpineCatalogue(5, 3, 7)
    balances = Counter()
    gates = Counter()
    count = 0
    for point, h, old_j, old_s in json.loads(source.read_text())['tiles']:
        if h != 1:
            continue
        px, py, e = point
        p = tuple(Fraction(v*cat.D, cat.c**e) for v in (px, py))
        check(all(v.denominator == 1 for v in p), 'Control scaling failed')
        r = cat.native_anchor(tuple(map(int, p)), 1)
        check(r is not None, 'Control h1 is not native')
        # Reflection sending B*rho to 0 and A to c^2; h becomes 2-h.
        x, y = cat.c*(cat.a+cat.b)-r[1], -cat.c*cat.b-r[0]
        j, s = (4-old_j) % 6, -old_s
        u = x-cat.a*U[j][0], y-cat.a*U[j][1]
        w = x+cat.b*U[(j+s)%6][0], y+cat.b*U[(j+s)%6][1]
        for axis, (X, Y), value in ((j, (x, y), s), (j, u, -s),
                                     (j+s, w, s), (j+s, (x, y), -s)):
            axis %= 3
            key = ((0, Y, X % cat.c) if axis == 0 else
                   (1, X, Y % cat.c) if axis == 1 else
                   (2, X+Y, Y % cat.c))
            balances[key] += value
        g = ((cat.a*u[1]-cat.b*u[0]) if s > 0 else
             (cat.a*u[0]-cat.b*u[1])) % cat.c
        gates[s, g] += s*(-1 if j % 2 else 1)
        count += 1
    check(not any(balances.values()), '143 cylinder endpoint residual')
    return {'physical_tiling': source_report,
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'height_one_tiles': count,
            'cylinder_endpoint_residuals': 0,
            'signed_gate_currents': [[s, r, v] for (s, r), v
                                    in sorted(gates.items()) if v]}


def verify(path, skip_control=False):
    started = time.monotonic()
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
    check(data['format'] == 'contained-native-h1-cylinder-dual-v1', 'Format')
    a, b, c = map(int, data['tile'])
    check(a*a+a*b+b*b == c*c, 'Tile side equation')
    B = a*(a+2*b)
    board = ((0, 0), (c*c*(a+b), -c*c*b), (B*a, B*b))
    xmin, xmax = ceildiv(min(x for x, y in board), c), max(x for x, y in board)//c
    ymin, ymax = ceildiv(min(y for x, y in board), c), max(y for x, y in board)//c
    tmin, tmax = ceildiv(min(x+y for x, y in board), c), max(x+y for x, y in board)//c
    off1 = (ymax-ymin+1)*c
    off2 = off1+(xmax-xmin+1)*c
    ep = off2+(tmax-tmin+1)*c
    check(ep == data['endpoint_row_count'], 'Endpoint row count')
    check(ep+2*c == data['row_count'], 'Total row count')
    potential = np.zeros(ep+2*c, dtype=np.int64)
    seen = set()
    for i, value in data['integer_row_potentials']:
        check(type(i) is int and type(value) is int, 'Noninteger potential')
        check(i not in seen and 0 <= i < len(potential), 'Repeated or invalid row')
        check(abs(value) <= 2**50, 'Potential outside overflow-safe bound')
        seen.add(i)
        potential[i] = value
    # Each column sums five signed terms, hence magnitude < 2^53.
    # All geometric products are also bounded before int64 conversion.
    maxcoord = max(abs(v) for p in board for v in p)
    check(16*maxcoord*maxcoord < 2**63, 'Geometry exceeds int64 safe bound')
    xx, yy = np.meshgrid(np.arange(xmin, xmax+1, dtype=np.int64),
                         np.arange(ymin, ymax+1, dtype=np.int64))
    xx, yy = xx.ravel(), yy.ravel()

    def index(axis, x, y):
        axis %= 3
        if axis == 0:
            return (y-ymin)*c+x % c
        if axis == 1:
            return off1+(x-xmin)*c+y % c
        return off2+(x+y-tmin)*c+y % c

    counts = []
    maximum = None
    maximizer = None
    for j in range(6):
        for s in (-1, 1):
            k = (j+s) % 6
            offsets = ((0, 0), (-a*U[j][0], -a*U[j][1]),
                       (b*U[k][0], b*U[k][1]))
            mask = np.ones(len(xx), dtype=bool)
            for dx, dy in offsets:
                X, Y = c*(xx+dx), c*(yy+dy)
                for P, Q in zip(board, board[1:]+board[:1]):
                    det = (Q[0]-P[0])*(Y-P[1])-(Q[1]-P[1])*(X-P[0])
                    mask &= det >= 0
            x, y = xx[mask], yy[mask]
            ux, uy = x-a*U[j][0], y-a*U[j][1]
            wx, wy = x+b*U[k][0], y+b*U[k][1]
            score = s*(potential[index(j, x, y)]-potential[index(j, ux, uy)]
                       +potential[index(k, wx, wy)]-potential[index(k, x, y)])
            gate = (a*uy-b*ux) % c if s > 0 else c+(a*ux-b*uy) % c
            score += s*(-1 if j % 2 else 1)*potential[ep+gate]
            value = int(score.max())
            if maximum is None or value > maximum:
                maximum = value
                i = int(np.argmax(score))
                maximizer = [int(x[i]), int(y[i]), j, s]
            counts.append({'rotation': j, 'hand': s, 'placements': len(x),
                           'maximum_score': value})
    raw = sum(r['placements'] for r in counts)
    check(raw == data['raw_contained_placements'], 'Raw catalogue count')
    expected = {(33, 7, 37): 4207420, (35, 13, 43): 12830527}
    if (a, b, c) in expected:
        check(raw == expected[a, b, c], 'Established catalogue count')
    f = int(data['native_base_charge_units'])
    Qup, Qdown = 2*c-(a-b)*f, -c+(a-b)*f
    check([Qup, Qdown] == data['native_gate_currents'], 'Gate profile')
    check(data['all_remote_gate_currents'] == 0, 'Remote gate profile')
    numerator = Qup*int(potential[ep])+Qdown*int(potential[ep+c])
    check(maximum == data['maximum_column_score'] and maximum > 0, 'Column maximum')
    check(numerator == data['gate_objective'], 'Gate objective')
    check(data['population_lower_bound'] == {
        'numerator': numerator, 'denominator': maximum}, 'Stored fraction')
    exclusion = numerator > 3*c*maximum
    check(exclusion == data['excludes_population_3c'], 'Exclusion flag')
    result = {'checks': 'PASS',
              'certificate': str(path.relative_to(ROOT)),
              'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'scope': 'Exact lower bound only for the fixed native gate profile stated in the certificate. No full tiling or all-profile exclusion is claimed.',
              'tile': [a, b, c], 'raw_contained_placements': raw,
              'endpoint_rows': ep, 'all_column_pricing': 'EXACT INTEGER',
              'population_lower_bound': {'numerator': numerator, 'denominator': maximum},
              'decimal_for_display_only': numerator/maximum,
              'excludes_population_3c': exclusion,
              'maximizing_placement': maximizer,
              'orientation_counts': counts}
    if not skip_control:
        result['positive_control_143'] = control_143()
    result['elapsed_seconds'] = time.monotonic()-started
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--skip-control', action='store_true')
    args = parser.parse_args()
    report = verify(args.certificate.resolve(), args.skip_control)
    text = json.dumps(report, indent=2)+'\n'
    if args.out:
        args.out.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O; the imported positive control uses asserts.')
    main()
