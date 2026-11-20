#!/usr/bin/env python3
"""Generate local directed mixed-height c-cycle controls, not full tilings."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
CONTINUATION = ROOT if (ROOT / 'global-endpoints').exists() else ROOT / 'repo/research/2026-11-20/semiprimes/continuation'
BASE = CONTINUATION / 'global-endpoints/integer'
sys.path.insert(0, str(BASE))
from global_core_sat import Geometry


def make(a, b, c):
    g = Geometry(a, b, c)
    # One extra 1/c makes the interior node spatially remote at the positive
    # prime, while the whole cluster is still strictly inside the board.
    shift = ((-(-a * b // c) + 1) * c + 1, c, 1)
    across, along = (b, a, 0), (0, a * c, 0)
    placements = []

    def insert(q, h, j, s, role):
        tile = q, h, j, s
        placements.append(dict(q=q, h=h, j=j, s=s, role=role,
                               vertices=g.vertices(tile)))

    for k in range(c):
        insert(g.add(shift, (0, (k + 1) * a, 0)), 0, 1, -1, 'interior')
        insert(g.add(shift, g.add(across, (0, k * a, 0))), 0, 4, -1, 'interior')
    for k in range(a):
        beta = g.add(shift, (0, (k + 1) * c, 0))
        insert(g.add(beta, g.scale(a, g.unit(-1, 4))), -1, 4, 1, 'left_bank')
    for k in range(a):
        beta = g.add(shift, g.add(across, (0, k * c, 0)))
        insert(g.add(beta, g.scale(a, g.unit(-1, 1))), -1, 1, 1, 'right_bank')

    # Every listed long edge is directed beta -> alpha. Its supporting bank
    # is interior at the two ends and exterior on the two long sides.
    cycle_tiles = [0] + list(range(2 * c + a, 2 * c + 2 * a))
    cycle_tiles += [2 * c - 1] + list(range(2 * c + a - 1, 2 * c - 1, -1))
    cycle = []
    for i in cycle_tiles:
        tile = placements[i]
        q, h, j, s = tile['q'], tile['h'], tile['j'], tile['s']
        beta = g.add(q, g.scale(-a, g.unit(h, j)))
        alpha = g.add(q, g.scale(b, g.unit(h, j + s)))
        cycle.append(dict(tile=i, start=beta, end=alpha, height=h + s))

    result = dict(
        scope='Local partial packing and directed mixed-height cycle; no full-board completion claimed.',
        tile=[a, b, c], N=g.N, shift=shift,
        board=[(0, 0, 0), (g.A, 0, 0), (0, g.B, 0)],
        region=[shift, g.add(shift, across), g.add(shift, g.add(across, along)),
                g.add(shift, along)],
        placements=placements, cycle=cycle,
        expected=dict(interior_tiles=2 * c, bank_tiles=2 * a,
                      cycle_edges=2 * a + 2, interior_long_pairs=c - 1,
                      interior_unpaired=2, interior_sign_counts=[c, c]),
    )
    path = Path(__file__).with_name(f'mixed_cycle_{g.N}.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(path.name, 'placements', len(placements), 'cycle edges', len(cycle))


if __name__ == '__main__':
    for shape in ((5, 3, 7), (33, 7, 37), (35, 13, 43)):
        make(*shape)
