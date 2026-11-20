#!/usr/bin/env python3
"""Positive control of phase gates on the complete known 143 certificate."""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
CONTINUATION = ROOT if (ROOT / 'global-endpoints').exists() else ROOT / 'repo/research/2026-11-20/semiprimes/continuation'
BASE = CONTINUATION / 'global-endpoints/integer'
PHASE = ROOT / 'phase_search' if (ROOT / 'phase_search').exists() else CONTINUATION / 'vertex-phase'
sys.path[:0] = [str(BASE), str(PHASE)]
from global_core_sat import Geometry
from phase_budget import PhaseBudget


def main():
    data = json.loads((BASE.parent / 'tiling_143.json').read_text())
    tiles = [(tuple(t[0]), *t[1:]) for t in data['tiles']]
    selected = set(tiles)
    assert len(selected) == len(tiles) == 143
    g = Geometry(5, 3, 7)

    def mate(tile):
        q, h, j, s = tile
        offset = g.add(g.scale(-g.a, g.unit(h, j)), g.scale(g.b, g.unit(h, j + s)))
        return g.add(q, offset), h, (j + 3) % 6, s

    assert all(mate(mate(tile)) == tile for tile in tiles)
    matched = {tile for tile in tiles if mate(tile) in selected}
    assert len(matched) % 2 == 0
    results = []
    for direction in (1, -1):
        budget = PhaseBudget(g, direction)
        counts = Counter(budget.node(q, direction * h) for q, h, _, _ in tiles)
        gates = Counter()
        for tile in tiles:
            q, h, j, s = tile
            if s != direction:
                continue
            endpoint = g.add(q, g.scale(-g.a, g.unit(h, j)))
            gate = budget.node(endpoint, direction * (h + s))
            if not budget.exterior_free(gate):
                gates['exterior_gate_tiles'] += 1
            elif counts[gate]:
                gates['occupied_gate_tiles'] += 1
            else:
                assert tile in matched
                assert not any(direction * t[1] >= gate[0]
                               and budget.node(t[0], gate[0]) == gate for t in tiles)
                gates['closed_gate_paired_tiles'] += 1
        for node, count in counts.items():
            if not budget.exterior_free(node):
                continue
            own = [tile for tile in tiles if budget.node(tile[0], direction * tile[1]) == node]
            unmatched = len([tile for tile in own if tile not in matched])
            assert unmatched >= (2 if count % 2 == 0 else 1)
        results.append(dict(tree=direction, counts=dict(gates)))
    print(json.dumps(dict(scope='Known complete 143 positive control.',
                          long_pairs=len(matched) // 2, unmatched=143 - len(matched),
                          trees=results), sort_keys=True))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
