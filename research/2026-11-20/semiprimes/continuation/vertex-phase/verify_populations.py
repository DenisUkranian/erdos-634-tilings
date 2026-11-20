#!/usr/bin/env python3
"""Exact 143 control for the two independent node-population PB systems."""
import argparse
from collections import Counter
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile

from corner_search import make_search_class
from population_search import make_population_search_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir')
    parser.add_argument('phase_dir')
    args = parser.parse_args()
    base = Path(args.base_dir).resolve()
    sys.path[:0] = [str(base), args.phase_dir]
    import global_core_sat as core
    from phase_budget import PhaseBudget
    PopulationSearch = make_population_search_class(core, PhaseBudget)
    CombinedSearch = make_search_class(SimpleNamespace(Search=PopulationSearch,atmost=core.atmost))
    data = json.loads((base.parent/'tiling_143.json').read_text())
    tiles = [(tuple(t[0]),*t[1:]) for t in data['tiles']]
    selected = set(tiles)
    with tempfile.TemporaryDirectory(prefix='population143-') as tmp:
        opts = SimpleNamespace(sides=[5,3,7], out=tmp, random_seed=1776,
                               point_checkpoint=None, proof=False,timeout_ms=30000,
                               minimize_core=False,angular_cliques=False,
                               no_phase_empty=False,corner_checkpoint=None)
        search = CombinedSearch(opts)
        for tile in tiles:
            search.insert(tile)
        search.boundary()
        for row in search.g.needs:
            search.install(row)
        # Also test the large combined graph with arbitrary generated neighbors.
        for tile in tiles:
            for p in search.g.vertices(tile):
                search.install_corner_tile(tile,p)
        fixed = []
        for i,tile in enumerate(search.tiles):
            fixed.append(f'(assert x{i})' if tile in selected else f'(assert (not x{i}))')
        summaries = []
        for tree,budget in enumerate(search.phase_budgets):
            counts = Counter(budget.node(tile[0],budget.sign*tile[1]) for tile in tiles)
            required = {node for tile in tiles for node in budget.required(tile)}
            empty = []
            total_blocks = 0
            for node,record in search.population_nodes[tree].items():
                population = counts[node]
                if record['core']:
                    assert population >= search.population_residue
                    assert (population-search.population_residue) % search.g.c == 0
                    blocks = (population-search.population_residue)//search.g.c
                else:
                    assert population % search.g.c == 0
                    blocks = population//search.g.c
                    assert blocks != 1
                total_blocks += blocks
                for k,bit in enumerate(record['bits']):
                    fixed.append('(assert '+(bit if blocks & (1<<k) else '(not '+bit+')')+')')
                if record['flag']:
                    flag = node in required
                    excuse = flag and not population
                    if excuse:
                        empty.append(node)
                    for symbol,value in ((record['flag'],flag),(record['excuse'],excuse)):
                        fixed.append('(assert '+(symbol if value else '(not '+symbol+')')+')')
            assert total_blocks == search.population_cap
            assert len(empty) <= 1
            summaries.append(dict(sign=budget.sign, actual_nodes=len(counts),
                                  required_nodes=len(required),empty_required_nodes=len(empty),
                                  generated_nodes=len(search.population_nodes[tree]),
                                  sum_blocks=total_blocks))
        fixed = '\n'.join(fixed)
        for attempt in range(2):
            if attempt:
                search.rebuild(attempt)
            search.enqueue('(push 1)')
            search.flush()
            assert search.smt.run(fixed) == ''
            status = search.smt.run('(check-sat)')
            assert status == 'sat', (status,search.smt.run('(get-info :reason-unknown)'))
            search.smt.run('(pop 1)')
        ordinary = next(record for record in search.population_nodes[0].values() if not record['core'])
        search.enqueue('(push 1)')
        search.flush()
        source = '(assert '+ordinary['bits'][0]+')\n'
        source += '\n'.join('(assert (not '+bit+'))' for bit in ordinary['bits'][1:])
        assert search.smt.run(source) == ''
        assert search.smt.run('(check-sat)') == 'unsat'
        search.smt.run('(pop 1)')
        print('PASS: exact node counts, combined 143 SMT witness, rebuild, and rejection of one c-block.')
        print(json.dumps(summaries,sort_keys=True))
        print(json.dumps(dict(placements=len(search.tiles),corner_roots=len(search.corner_roots),
                              corner_symbols=search.corner_symbols,
                              population_symbols=len(search.population_variables)),sort_keys=True))
        search.smt.close()
        search.journal.close()


if __name__=='__main__':
    main()
