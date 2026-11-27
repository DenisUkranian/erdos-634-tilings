"""Exact directional gate estimates and tests against complete coordinate tilings."""
from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "axial-reserve"))
from reserve import UNITS, gate, gate_column, isolated_opposite_support
sys.path.insert(0, str(HERE.parent / "joint-cell-tree"))
from controls import cell, geom, reconstruct, step


def hex_length(v):
    x, y = v
    return max(abs(x), abs(y), abs(x + y))


def gate_estimate(a, b, c):
    w = -b * pow(a, -1, c) % c
    stencil = {c, 2 * c + a}
    maximum = -100
    for r, j, h in product(range(c), range(6), (-1, 1)):
        column = gate_column(a, b, c, r, j, h, w)
        score = 2 * sum(UNITS[j]) * (column[-1][0] == 3 * c)
        score -= sum(n for i, n in column[:-1] if i in stencil)
        maximum = max(maximum, score)
    assert maximum == 1
    return maximum


def heading_support(a, b, c):
    """Single-sign row elimination at two same-hand gates."""
    w = -b * pow(a, -1, c) % c
    survivors = {}
    for offset in range(1, c):
        columns = {}
        for r, j in product(range(c), range(6)):
            entries = gate_column(a, b, c, r, j, -1, w)
            gate, sign = entries.pop()
            if gate != 3 * c + (0 if sign == 1 else offset):
                continue
            col = Counter()
            for i, n in entries:
                col[i] += n
            columns[r, j] = {i: n for i, n in col.items() if n}
        while columns:
            signs = defaultdict(set)
            for col in columns.values():
                for i, n in col.items():
                    signs[i].add(n > 0)
            keep = {t: col for t, col in columns.items() if all(len(signs[i]) == 2 for i in col)}
            if len(keep) == len(columns):
                break
            columns = keep
        if columns:
            assert len(columns) == 2
            headings = sorted(j for r, j in columns)
            assert headings[1] == headings[0] + 3
            survivors[offset] = headings
    for hand in (-1, 1):
        assert isolated_opposite_support(a, b, c, hand)[-1] == 0
    return survivors


def central_offsets(a, b, c):
    path = (HERE.parent / 'terminal-contact' / 'two_gate_potentials.json'
            if c == 37 else HERE / 'central_5063.json')
    labels = set(range(1, c + 1))
    for record in json.loads(path.read_text()):
        first, _, den = gate(a, b, c, record)
        labels = {k for k in labels if (a-b)*(first-record['table'][3*c+k]) <= 2*c*den}
    assert labels == ({3, 4, 30} if c == 37 else {5, 8, 30})
    return sorted(labels)


def native_floor(a, b, c, hand, capacity, wall_error):
    """Minimize a zero-character bank size, certifying all counts at most 14."""
    best = []
    for x, y in product(range(-14, 15), repeat=2):
        h, rem = divmod(y - x, 3)
        if rem:
            continue
        cost = abs(x + h) + abs(y - h) + abs(h)
        if cost > 14:
            continue
        l, r = (a, b) if hand == 1 else (a + b, -b)
        X, rx = divmod(l * x - r * y, c)
        Y, ry = divmod(r * x + (l + r) * y, c)
        if rx or ry or 2 * hex_length((a + b - X, -b - Y)) > capacity + wall_error:
            continue
        best.append((cost, x, y))
    assert best and min(t[0] for t in best) == 14
    return sorted(best)


def control(which):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, which)
    polys, centres, origin, *_ = geom.check_full_tiling(g, tiles)
    pairs, _ = geom.long_pairs(g, tiles, polys, centres, origin)
    lifts, slant = reconstruct(g, tiles, polys)
    root = slant[:1]
    count = Counter(lifts.values())
    headings = defaultdict(lambda: [0, 0])
    physical = defaultdict(lambda: [0, 0])
    for i, t in enumerate(tiles):
        _, h, j, hand = t
        p, _, q = g.vertices(t)
        v = lifts[i]
        edge = v, step(v, cell(g, h + hand, p))
        for axis in (0, 1):
            headings[edge][axis] += UNITS[j][axis]
        if i not in pairs:
            # v_0 to v_2 follows the broken short path on positive-hand tiles.
            diff = g.mult(g.unit(-h-hand, 0), g.sub(q, p))
            delta = geom.point(g, diff)
            for axis in (0, 1):
                physical[edge][axis] += hand * delta[axis] / g.c
    for edge, displacement in headings.items():
        assert physical[edge] == displacement
        v, _ = edge
        assert 2 * hex_length(displacement) <= count[v] + 2 * (v == root)
    return dict(gates=len(headings), nonzero=sum(hex_length(d) > 0 for d in headings.values()),
                core_tiles=count[root], unmatched=len(tiles) - len(pairs))


def main():
    result = {}
    for a, b, c in ((5, 3, 7), (33, 7, 37), (35, 13, 43)):
        entry = dict(maximum_column_score=gate_estimate(a, b, c))
        if c != 7:
            N = (2*a+b)*(a+2*b)
            entry.update(central_two_block_gate_offsets=central_offsets(a, b, c),
                         residual_two_gate_headings=heading_support(a, b, c),
                         zero_current_minimum_core=native_floor(a, b, c, 1, N % c + c, 2),
                         zero_current_two_block_slant=native_floor(a, b, c, -1, 2*c, 0))
        result[c] = entry
    result['full_143_controls'] = {k: control(k) for k in ('known', 'macro')}
    return result


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(main(), indent=2))
