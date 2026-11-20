#!/usr/bin/env python3
"""Replay all 429 local fans of the exact 143 control, including SMT encoding."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction
import sys
import tempfile

from corner_oracle import CornerOracle, angular_groups
from corner_search import make_search_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir')
    args = parser.parse_args()
    base = Path(args.base_dir).resolve()
    sys.path.insert(0, str(base))
    import global_core_sat as core
    data = json.loads((base.parent/'tiling_143.json').read_text())
    tiles = [(tuple(t[0]), *t[1:]) for t in data['tiles']]
    selected = set(tiles)
    g = core.Geometry(5, 3, 7)
    oracle = CornerOracle(g)
    checks = 0
    for tile in tiles:
        for p in g.vertices(tile):
            assert oracle.satisfied(tile, p, selected), (tile, p)
            checks += 1
    assert checks == 429
    print('All 429 known local stars are preserved.')

    def rational(p):
        return Fraction(p[0], g.power(p[2])), Fraction(p[1], g.power(p[2]))

    points = {p for tile in tiles for p in g.vertices(tile)}
    through_count = 0
    for tile in tiles:
        vertices = g.vertices(tile)
        for k in range(3):
            q0, q1 = vertices[k], vertices[(k+1)%3]
            v = g.sub(q0, q1)  # reversed CCW side: through-tile is on its right
            decoded = [(h,j,L) for h in (tile[1]-1,tile[1],tile[1]+1)
                       for j in range(6) for L in (g.a,g.b,g.c)
                       if v == g.scale(L,g.unit(h,j))]
            assert len(decoded) == 1
            h,j,L = decoded[0]
            ux,uy = rational(g.unit(h,j))
            for p in points:
                d = g.sub(p,q1)
                if v[0]*d[1] != v[1]*d[0]:
                    continue
                dx,dy = rational(d)
                t = dx/ux if ux else dy/uy
                if not 0 < t < L:
                    continue
                witnesses = oracle.through_intervals(p,(h,j))
                def matches(item):
                    candidate,lo,hi,length = item
                    if candidate[1:] != tile[1:] or length != L or not lo <= t <= hi:
                        return False
                    ax,ay = rational(g.sub(candidate[0],tile[0]))
                    return (ax,ay) == (t*ux,t*uy)
                assert any(matches(witness) for witness in witnesses), (p,tile,(h,j),t)
                through_count += 1
    assert through_count
    print(f'All {through_count} actual through-edge incidences have exact sliding witnesses.')

    large = core.Geometry(35, 13, 43)
    local = CornerOracle(large)
    for h in range(-4, 5):
        for j in range(6):
            out = local.outgoing((400, 600, 0), h, j)
            assert len(out) == 6
            assert sorted(angle for _, angle in out) == [(0, 1)]*2 + [(1, 0)]*2 + [(2, 2)]*2
    print('54 interior rays each have exactly six incident angle placements.')

    with tempfile.TemporaryDirectory(prefix='corner143-') as tmp:
        opts = SimpleNamespace(sides=[5,3,7], out=tmp, random_seed=1776,
                               point_checkpoint=None, proof=False,
                               timeout_ms=30000, minimize_core=False,
                               angular_cliques=True)
        search = make_search_class(core)(opts)
        for tile in tiles:
            search.insert(tile)
        for tile in tiles:
            for p in g.vertices(tile):
                search.install_corner_tile(tile, p)
        # Verify the permanent corner system itself. The base endpoint guards
        # are a separate optional finite-pool search device, not corner clauses.
        for p in sorted(search.corner_dirty):
            for group in angular_groups(search.g, search.corner_tiles[p], p):
                search.assert_(core.atmost(1, [f'x{search.index[t]}' for t in sorted(group)]))
        search.corner_dirty.clear()
        search.flush()
        search.smt.run('(push 1)')
        fixed = '\n'.join('(assert '+('x'+str(i) if t in selected else '(not x'+str(i)+')')+')'
                          for i,t in enumerate(search.tiles))
        assert search.smt.run(fixed) == ''
        status = search.smt.run('(check-sat)')
        assert status == 'sat', (status, search.smt.run('(get-info :reason-unknown)'))
        search.smt.run('(pop 1)')
        search.rebuild(1)
        search.flush()
        search.smt.run('(push 1)')
        assert search.smt.run(fixed) == ''
        status = search.smt.run('(check-sat)')
        assert status == 'sat', (status, search.smt.run('(get-info :reason-unknown)'))
        search.smt.run('(pop 1)')
        # A single selected interior-corner tile cannot form a full or half fan.
        tile, p = next((t,p) for t in tiles for p in g.vertices(t)
                       if oracle.board_sector(p) is None)
        search.smt.run('(push 1)')
        bad = '\n'.join('(assert '+('x'+str(i) if t == tile else '(not x'+str(i)+')')+')'
                        for i,t in enumerate(search.tiles))
        assert search.smt.run(bad) == ''
        assert search.smt.run('(check-sat)') == 'unsat'
        search.smt.run('(pop 1)')
        print('SMT control, equivalent-context rebuild, and missing-neighbor rejection pass.')
        print(json.dumps(dict(control_tiles=143, roots=len(search.corner_roots),
                              columns=len(search.tiles), auxiliary_symbols=search.corner_symbols,
                              assertions=len(search.clauses)),sort_keys=True))
        search.smt.close()
        search.journal.close()


if __name__ == '__main__':
    main()
