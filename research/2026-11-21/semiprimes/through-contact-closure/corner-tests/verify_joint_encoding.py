#!/usr/bin/env python3
"""Check whole-bank/cycle conjunction and permanent assertion lifetimes.

These are small libz3 controls, not a target nonexistence proof. The existing
Fraction-based cycle verifier supplies contained nonoverlapping supports.
No whole-edges implementation or replay file is modified by this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
sys.path[:0] = [str(PACKAGE / 'whole-edges'), str(PACKAGE / 'owned')]
from whole_edge_search import WholeEdgeSearch
from owned_search import defaults
from verify_long_cycles import triangle_fixture, witness_check


def permanent_depth_check(journal, permanent):
    """Check actual serialized command order, not the Python scope flag."""
    depth = 0
    checked = 0
    for line in journal.splitlines():
        line = line.strip()
        if line == '(push 1)':
            depth += 1
        elif line == '(pop 1)':
            depth -= 1
            assert depth >= 0
        elif line.startswith('(assert ') and line.endswith(')'):
            clause = line[len('(assert '):-1]
            if clause in permanent:
                assert depth == 0, ('Permanent assertion inside query', clause)
                checked += 1
    assert depth == 0
    assert checked >= len(permanent)
    return checked


def fixed_query(search, positive):
    search.enqueue('(push 1)')
    search.query_active = True
    search.enqueue('(assert ' + search.query_bounds()[2] + ')')
    for index in positive:
        search.enqueue(f'(assert x{index})')
    search.flush()
    status = search.smt.run('(check-sat)')
    assert status in ('sat', 'unsat'), status
    # Deliberately leave the pop in the queue, as the real driver does.
    # New permanent clauses will follow it in the same eventual batch.
    search.enqueue('(pop 1)')
    search.query_active = False
    return status


def target_control(sides, out, search_class=WholeEdgeSearch):
    search = search_class(defaults(
        sides=sides, out=str(out), no_grid=True, angular_cliques=False,
        edge_tiles_per_round=1, vertex_fans_per_round=0,
        max_columns=0, max_rss_mb=0, time_limit=0, timeout_ms=10000))
    try:
        tiles, _ = triangle_fixture(search.g, 1)
        indices = [search.insert(tile) for tile in tiles]
        for tile in tiles:
            search.install_tile_edges(tile)
        search.flush()

        before_aliases = len(search.tiles)
        for tile, index in zip(tiles, indices):
            q, h, j, sign = tile
            # Same exact point with an uncancelled c denominator, and j+6.
            alias = ((q[0]*search.g.c, q[1]*search.g.c, q[2]+1), h, j+6, sign)
            assert search.insert(alias) == index
        assert len(search.tiles) == before_aliases
        assert len(search.index) == len(search.tiles) == len(set(search.tiles))
        assert len(search.edge_obligations) == 9
        assert all(not record['boundary'] for record in search.edge_obligations.values())
        for bank in search.edge_catalogues.values():
            assert len(bank['indices']) == len(set(bank['indices']))
            for group in bank['intervals']:
                assert len(group) == len(set(group))

        # Opposite banks alone admit a partial Boolean completion of this
        # patch. The theorem adds genuinely stronger global information.
        assert fixed_query(search, indices) == 'sat'
        assert search.install_long_cycle_cuts(indices) == 1
        search.flush()
        assert len(search.long_cycle_records) == 1
        witness = next(iter(search.long_cycle_records.values()))
        witness_check(search.g, search.tiles, indices, witness)
        assert fixed_query(search, indices) == 'unsat'
        search.flush()
        assert fixed_query(search, indices[:2]) == 'sat'
        search.flush()

        before_rebuild = permanent_depth_check(
            (out / 'model.smt2').read_text(), search.clauses)
        search.rebuild(1)
        search.flush()
        assert fixed_query(search, indices) == 'unsat'
        search.flush()
        assert fixed_query(search, indices[:2]) == 'sat'
        search.flush()
        after_rebuild = permanent_depth_check(
            (out / 'model.smt2').read_text(), search.clauses)
        result = dict(
            N=search.g.N, sides=list(sides), columns=len(search.tiles),
            whole_edge_obligations=len(search.edge_obligations),
            bank_cliques=len(search.edge_bank_cliques),
            permanent_assertions=len(search.clauses),
            same_cycle_support_before_cut='sat',
            same_cycle_support_after_cut='unsat',
            two_side_path_after_cut='sat',
            same_cycle_support_after_rebuild='unsat',
            two_side_path_after_rebuild='sat',
            queued_pop_precedes_new_permanent_assertions=True,
            permanent_assertions_checked_before_rebuild=before_rebuild,
            permanent_assertions_checked_after_rebuild=after_rebuild,
            exact_coordinate_and_orientation_aliases_deduplicated=True,
            all_banks_share_the_global_tile_registry=True)
        if getattr(search, 'phase_enabled', False):
            result['ordinary_phase_limit_per_tree'] = search.phase_limit
            result['generated_phase_nodes'] = [len(nodes) for nodes in search.phase_nodes]
            result['phase_trees_are_separately_bounded'] = True
        return result
    finally:
        search.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', default=str(HERE / 'JOINT_ENCODING_REPLAY.json'))
    parser.add_argument('--with-phase', action='store_true',
                        help='Repeat controls with the optional separate phase-tree caps.')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='joint-bank-cycle-') as temporary:
        base = Path(temporary)
        results = [target_control(sides, base / str(sides[0]))
                   for sides in ((33,7,37), (35,13,43))]
        phase_results = []
        if args.with_phase:
            sys.path.insert(0, str(PACKAGE / 'spatial'))
            from phase_whole_edge_search import PhaseWholeEdgeSearch
            phase_results = [target_control(sides, base / ('phase-' + str(sides[0])),
                                            PhaseWholeEdgeSearch)
                             for sides in ((33,7,37), (35,13,43))]
    files = [PACKAGE / 'whole-edges' / name for name in (
        'whole_edge_search.py', 'whole_edge_oracle.py')]
    files += [PACKAGE / 'owned' / 'owned_search.py',
              PACKAGE / 'spatial' / 'spatial_search.py', HERE / 'long_cycles.py']
    if args.with_phase:
        files.append(PACKAGE / 'spatial' / 'phase_whole_edge_search.py')
    report = dict(
        status='PASS', controls=results, optional_phase_controls=phase_results,
        sha256={str(path.relative_to(PACKAGE)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in files},
        full_target_excluded=False, root_exclusions=0,
        scope='Small integration and assertion-lifetime controls; the universal cycle cut uses the separately cited written theorem.')
    Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact checks are required.')
    main()
