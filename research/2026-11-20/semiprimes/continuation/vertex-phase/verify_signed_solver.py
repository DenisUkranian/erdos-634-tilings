#!/usr/bin/env python3
"""Exact signed-node and parity-completion controls on the known 143 tiling."""
import argparse
from collections import Counter
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile

from corner_search import make_search_class
from signed_population_search import make_signed_population_search_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir')
    parser.add_argument('phase_dir')
    parser.add_argument('--joint-heights',action='store_true')
    args = parser.parse_args()
    base = Path(args.base_dir).resolve()
    sys.path[:0] = [str(base),args.phase_dir]
    import global_core_sat as core
    from phase_budget import PhaseBudget
    SignedSearch = make_signed_population_search_class(core,PhaseBudget)
    if args.joint_heights:
        from joint_height_search import make_joint_height_search_class
        SignedSearch = make_joint_height_search_class(SignedSearch)
    CombinedSearch = make_search_class(SimpleNamespace(Search=SignedSearch,atmost=core.atmost))
    data = json.loads((base.parent/'tiling_143.json').read_text())
    tiles = [(tuple(t[0]),*t[1:]) for t in data['tiles']]
    selected = set(tiles)
    with tempfile.TemporaryDirectory(prefix='signed143-') as tmp:
        opts = SimpleNamespace(sides=[5,3,7],out=tmp,random_seed=1776,
                               point_checkpoint=None,proof=False,timeout_ms=30000,
                               minimize_core=False,angular_cliques=False,
                               no_phase_empty=False,corner_checkpoint=None)
        search = CombinedSearch(opts)
        assert search.signed_residues == [4,6]
        assert search.signed_totals == [67,76]
        assert search.signed_caps == [9,10]
        for tile in tiles:
            search.insert(tile)
        search.boundary()
        for row in search.g.needs:
            search.install(row)
        for tile in tiles:
            for p in search.g.vertices(tile):
                search.install_corner_tile(tile,p)
        fixed = [f'(assert x{i})' if tile in selected else f'(assert (not x{i}))'
                 for i,tile in enumerate(search.tiles)]
        summaries = []
        for tree,budget in enumerate(search.phase_budgets):
            counts = Counter((budget.node(tile[0],budget.sign*tile[1]),search.tile_sign(tile)) for tile in tiles)
            required = {node for tile in tiles for node in budget.required(tile)}
            total_blocks = [0,0]
            parity_blocks = Counter()
            empty = []
            for node,record in search.signed_nodes[tree].items():
                population = sum(counts[node,sign] for sign in range(2))
                if not record['core']:
                    assert population == 0 or population >= 2*search.g.c
                for sign in range(2):
                    residue = search.signed_residues[sign] if record['core'] else 0
                    n = counts[node,sign]
                    assert n >= residue and (n-residue)%search.g.c == 0
                    blocks = (n-residue)//search.g.c
                    total_blocks[sign] += blocks
                    parity_blocks[sign,node[0]%2] += blocks
                    for k,bit in enumerate(record['bits'][sign]):
                        fixed.append('(assert '+(bit if blocks&(1<<k) else '(not '+bit+')')+')')
                if record['flag']:
                    flag = node in required
                    excuse = flag and not population
                    if excuse:
                        empty.append(node)
                    for symbol,value in ((record['flag'],flag),(record['excuse'],excuse)):
                        fixed.append('(assert '+(symbol if value else '(not '+symbol+')')+')')
            assert total_blocks == search.signed_caps
            assert parity_blocks[1,0]-parity_blocks[0,0] == search.signed_even_delta
            assert parity_blocks[1,1]-parity_blocks[0,1] == 1
            assert len(empty) <= 1
            summaries.append(dict(sign=budget.sign,generated_nodes=len(search.signed_nodes[tree]),
                                  positive_blocks=total_blocks[0],negative_blocks=total_blocks[1],
                                  empty_required_nodes=len(empty)))
        if args.joint_heights:
            height_counts = Counter((tile[1],search.tile_sign(tile)) for tile in tiles)
            for h,groups in search.joint_heights.items():
                for sign,bits in enumerate(groups):
                    residue = search.signed_residues[sign] if h == 0 else 0
                    n = height_counts[h,sign]
                    assert n >= residue and (n-residue)%search.g.c == 0
                    blocks = (n-residue)//search.g.c
                    for k,bit in enumerate(bits):
                        fixed.append('(assert '+(bit if blocks&(1<<k) else '(not '+bit+')')+')')
        fixed = '\n'.join(fixed)
        for attempt in range(2):
            if attempt:
                search.rebuild(attempt)
            search.enqueue('(push 1)')
            search.flush()
            assert search.smt.run(fixed) == ''
            status = search.smt.run('(check-sat)')
            assert status == 'sat',(status,search.smt.run('(get-info :reason-unknown)'))
            search.smt.run('(pop 1)')
        record = next(r for r in search.signed_nodes[0].values() if not r['core'])
        search.enqueue('(push 1)')
        search.flush()
        bad = '(assert '+record['bits'][0][0]+')\n'
        bad += '\n'.join('(assert (not '+bit+'))' for bit in record['bits'][0][1:]+record['bits'][1])
        assert search.smt.run(bad) == ''
        assert search.smt.run('(check-sat)') == 'unsat'
        search.smt.run('(pop 1)')
        # Independently exhaust all four partial-block counts in a small box.
        K,delta = search.signed_caps[0],search.signed_even_delta
        cases = 0
        for Pe in range(K+3):
            for Po in range(K+3):
                for Qe in range(K+3):
                    for Qo in range(K+3):
                        bounds = Pe+Po<=K and Qe+Qo<=K+delta+1 and Pe+Qo<=K+1 and Qe+Po<=K+delta
                        completion = any(E>=Pe and E+delta>=Qe and K-E>=Po and K-E+1>=Qo for E in range(K+1))
                        assert bounds == completion
                        cases += 1
        print('PASS: signed counts, combined SMT witness, rebuild, one-block rejection, and parity completion.')
        print(json.dumps(summaries,sort_keys=True))
        print(json.dumps(dict(placements=len(search.tiles),corner_roots=len(search.corner_roots),
                              signed_population_symbols=len(search.signed_variables),
                              parity_completion_cases=cases,
                              joint_heights=sorted(search.joint_heights) if args.joint_heights else None),sort_keys=True))
        search.smt.close()
        search.journal.close()


if __name__=='__main__':
    main()
