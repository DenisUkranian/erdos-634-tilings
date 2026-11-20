#!/usr/bin/env python3
"""Independent logical controls for the signed population projection.

The deliberately overlapping placements exercise capacity witnesses and SMT
scope, not a geometric tiling. Separate parity controls allow omitted nodes.
"""
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'global-endpoints'/'integer'
sys.path[:0] = [str(BASE), str(HERE)]

import global_core_sat as base
from phase_budget import PhaseBudget
from signed_population_search import make_signed_population_search_class

SignedSearch = make_signed_population_search_class(base, PhaseBudget)


def options(out, sides=(33, 7, 37), strict=False):
    return SimpleNamespace(sides=list(sides), out=out, random_seed=1776,
                           point_checkpoint=None, proof=False, timeout_ms=10000,
                           minimize_core=False, no_phase_empty=strict)


def fix(record, plus, minus):
    result = []
    for sign, value in enumerate((plus, minus)):
        for k, bit in enumerate(record['bits'][sign]):
            literal = bit if value & (1 << k) else '(not ' + bit + ')'
            result.append('(assert ' + literal + ')')
    return result


def query(search, assertions, expected):
    search.enqueue('(push 1)')
    search.flush()
    answer = search.smt.run('\n'.join(assertions) + '\n(check-sat)')
    assert answer == expected, (expected, answer)
    # Follow the real base loop: declarations inserted next must follow pop.
    search.enqueue('(pop 1)')


def close(search):
    search.smt.close()
    search.journal.close()


def check_scope():
    with tempfile.TemporaryDirectory(prefix='signed-scope-') as tmp:
        search = SignedSearch(options(tmp))
        c = search.g.c

        def ordinary(i, sign=1):
            return ((c * (40 + i) + 1, c * 200, 1), 0, 0, sign)

        first = search.insert(ordinary(0))
        own = search.phase_budgets[0].node(ordinary(0)[0], 0)
        record = search.signed_nodes[0][own]
        core = search.signed_nodes[0][(0, 0, 0)]
        selected = [f'(assert x{first})']

        query(search, selected + fix(record, 0, 2), 'unsat')
        query(search, selected + fix(record, 1, 0), 'unsat')
        query(search, selected + fix(record, 1, 1), 'sat')
        query(search, selected + fix(record, 2, 0), 'sat')
        query(search, fix(record, 3, 0), 'unsat')
        query(search, fix(core, 1, 0), 'unsat')
        query(search, fix(core, 0, 1), 'unsat')

        # Positive demand moves its cap from two blocks to three.
        for i in range(1, 2 * c + 1):
            search.insert(ordinary(i))
        selected = [f'(assert x{i})' for i in range(len(search.tiles))]
        query(search, selected + fix(record, 3, 0), 'sat')
        query(search, selected + fix(record, 2, 1), 'unsat')

        # Negative demand crosses the own-capacity PB threshold at c+1.
        for i in range(c + 1):
            search.insert(ordinary(i, -1))
        selected = [f'(assert x{i})' for i in range(len(search.tiles))]
        query(search, selected + fix(record, 3, 2), 'sat')
        query(search, selected + fix(record, 3, 1), 'unsat')

        # Independent residues matter: core populations 20 and 9 need one
        # block of each sign beyond residues 19 and 8.
        for sign, residue in zip((1, -1), search.signed_residues):
            for i in range(residue + 1):
                search.insert(((40 + i, 220, 0), 0, 0, sign))
        selected = [f'(assert x{i})' for i in range(len(search.tiles))]
        witness = selected + fix(record, 3, 2) + fix(core, 1, 1)
        query(search, witness, 'sat')
        query(search, selected + fix(core, 0, 1), 'unsat')
        query(search, selected + fix(core, 1, 0), 'unsat')
        search.rebuild(1)
        query(search, witness, 'sat')
        query(search, fix(record, 4, 0), 'unsat')
        query(search, fix(record, 0, 3), 'unsat')

        excuse = [f'(assert {record["flag"]})', f'(assert {record["excuse"]})']
        query(search, excuse + fix(record, 0, 0), 'sat')
        close(search)

    # No-empty is an explicit target-only strengthening.
    for sides in ((33, 7, 37), (35, 13, 43)):
        with tempfile.TemporaryDirectory(prefix='signed-strict-') as tmp:
            search = SignedSearch(options(tmp, sides, strict=True))
            node = search.phase_budgets[0].node((1, 0, 1), 0)
            record = search.signed_node(0, node)
            excuse = [f'(assert {record["flag"]})', f'(assert {record["excuse"]})']
            query(search, excuse + fix(record, 0, 0), 'unsat')
            search.rebuild(1)
            query(search, excuse + fix(record, 0, 0), 'unsat')
            close(search)


def check_partial_parity():
    # No selected tiles are needed here: allocate logical capacities at valid
    # nodes, with all remaining population reserved for unlisted completion.
    # Two ordinary blocks per occupied node satisfy occupancy and pool caps.
    for sides in ((33, 7, 37), (35, 13, 43)):
        for tree in range(2):
            with tempfile.TemporaryDirectory(prefix='signed-parity-') as tmp:
                search = SignedSearch(options(tmp, sides))
                budget = search.phase_budgets[tree]
                K, delta = search.signed_caps[0], search.signed_even_delta
                even = [search.signed_node(tree, budget.node((i, 0, 1), 0))
                        for i in range(1, (K + delta) // 2 + 1)]
                odd = [search.signed_node(tree, budget.node((i, 0, 1), 1))
                       for i in (1, 2)]

                def allocation(ne_plus, ne_minus, no_plus, no_minus):
                    assert not ne_plus or not ne_minus
                    assert not no_plus or not no_minus
                    result = fix(search.signed_nodes[tree][(0, 0, 0)], 0, 0)
                    for i, record in enumerate(even):
                        result += fix(record, 2 * (i < ne_plus), 2 * (i < ne_minus))
                    for i, record in enumerate(odd):
                        result += fix(record, 2 * (i < no_plus), 2 * (i < no_minus))
                    return result

                # Partial signed parity need not be the final exact parity:
                # omitted nodes can supply the additional negative odd blocks.
                query(search, allocation(0, 0, 1, 0), 'sat')

                # These pass the separate total budgets but each violates one
                # cross-parity inequality. The other cross bound is satisfied.
                assert 2 <= K and K + delta <= search.signed_caps[1]
                assert K + delta + 2 > K + delta
                query(search, allocation(0, (K + delta) // 2, 1, 0), 'unsat')
                assert 2 * (K // 2) <= K and 4 <= search.signed_caps[1]
                assert 2 * (K // 2) + 4 > K + 1
                query(search, allocation(K // 2, 0, 0, 2), 'unsat')
                close(search)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    check_scope()
    check_partial_parity()
    print('PASS: mixed-sign occupancy, sign-specific own capacities and core residues;')
    print('pool-cap growth, queued-pop scope, rebuild and both strict target gates;')
    print('omitted-node parity slack and both cross bounds in both trees and targets.')
