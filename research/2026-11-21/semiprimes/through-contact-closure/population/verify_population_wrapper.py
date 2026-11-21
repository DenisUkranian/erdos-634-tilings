#!/usr/bin/env python3
"""Exact143 allocation controls, optionally including full solver/restart checks.

The default uses the standard library only. The SMT controls exercise the
unchanged population factory inside the new whole-edge wrapper; they are not
target searches and do not certify either target's nonexistence.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import tempfile

from population_whole_edge_search import (
    PACKAGE,ROOT,PopulationWholeEdgeSearch,PhaseBudget,core)
from owned_search import defaults
from verify_owned_controls import exact_physical_control

sys.path.insert(0,str(PACKAGE/'audit'))
from proof_cnf import parse


def evaluate(node,assignment):
    """Direct Boolean/PB semantics; does not use a solver or the CNF encoder."""
    if isinstance(node,str):
        return node=='true' if node in ('true','false') else assignment[node]
    op,*args=node
    if isinstance(op,tuple):
        assert op[0]=='_'
        kind,bound=op[1],int(op[2])
        weights=[1]*len(args) if kind=='at-most' else list(map(int,op[3:]))
        assert len(weights)==len(args) and all(w>0 for w in weights)
        count=sum(w*evaluate(arg,assignment) for w,arg in zip(weights,args))
        return count==bound if kind=='pbeq' else count<=bound
    values=[evaluate(arg,assignment) for arg in args]
    if op=='not':
        assert len(values)==1
        return not values[0]
    if op=='and':return all(values)
    if op=='or':return any(values)
    if op=='=>':
        assert len(values)==2
        return not values[0] or values[1]
    if op=='=':
        assert len(values)==2
        return values[0]==values[1]
    raise AssertionError(('Unsupported operator',op))


def conjuncts(node):
    if isinstance(node,tuple) and node and node[0]=='and':
        return {part for arg in node[1:] for part in conjuncts(arg)}
    return {node}


def arithmetic_controls(g,tiles):
    exact_physical_control(g,tiles)
    result=[]
    samples=0
    for sign in (1,-1):
        budget=PhaseBudget(g,sign)
        counts=Counter(budget.node(t[0],sign*t[1]) for t in tiles)
        required={node for t in tiles for node in budget.required(t)}
        residue=g.N%g.c
        cap=(g.N-residue)//g.c
        blocks={node:(count-residue)//g.c if node==(0,0,0) else count//g.c
                for node,count in counts.items()}
        assert counts[(0,0,0)]%g.c==residue
        assert all(count%g.c==0 and count>=2*g.c
                   for node,count in counts.items() if node!=(0,0,0))
        assert len(required-set(counts))<=1
        assert sum(blocks.values())==cap==20
        # Prefix and regular-stride subsets test minimal auxiliary allocation.
        for subset in [tiles[:k] for k in range(len(tiles)+1)]+[tiles[r::s] for s in range(2,10) for r in range(s)]:
            partial=Counter(budget.node(t[0],sign*t[1]) for t in subset)
            demand={node for t in subset for node in budget.required(t)}
            allocated={}
            for node in set(partial)|demand|{(0,0,0)}:
                m=partial[node]
                if node==(0,0,0):
                    k=(max(0,m-residue)+g.c-1)//g.c
                    assert m<=residue+g.c*k
                elif m or node in counts and node in demand:
                    k=max(2,(m+g.c-1)//g.c)
                    assert m<=g.c*k
                else:k=0
                allocated[node]=k
                assert k<=blocks.get(node,0)
            assert sum(allocated.values())<=cap
            samples+=1
        result.append(dict(sign=sign,node_populations=[dict(key=node,population=count,blocks=blocks[node])
                     for node,count in sorted(counts.items())],required_ancestors=len(required),
                     empty_required_ancestors=len(required-set(counts)),allocated_blocks=sum(blocks.values()),
                     available_blocks=cap))
    # Direct integer identity underlying the positive-weight capacity clause.
    identities=0
    for n,c in ((143,7),(3431,37),(5063,43)):
        residue=n%c
        cap=(n-residue)//c
        width=cap.bit_length()
        allbits=(1<<width)-1
        for r in (0,residue):
            for k in range(cap+1):
                for m in sorted({0,1,max(0,r+c*k-1),r+c*k,r+c*k+1,n}):
                    lhs=m+c*sum((1<<i)*(not ((k>>i)&1)) for i in range(width))
                    assert (lhs<=c*allbits+r)==(m<=r+c*k)
                    identities+=1
    return dict(physical143_verified=True,trees=result,subset_allocations=samples,
                weighted_capacity_identities=identities,trees_are_bounded_separately=True)


def allocation_assignment(search,selected,override=None):
    assignment={f'x{i}':t in selected for i,t in enumerate(search.tiles)}
    for tree,budget in enumerate(search.phase_budgets):
        counts=Counter(budget.node(t[0],budget.sign*t[1]) for t in selected)
        required={node for t in selected for node in budget.required(t)}
        for node,record in search.population_nodes[tree].items():
            m=counts[node]
            if record['core']:
                blocks=(max(0,m-search.population_residue)+search.g.c-1)//search.g.c
            else:
                blocks=max(2,(m+search.g.c-1)//search.g.c) if m else 0
            if override and (tree,node) in override:blocks=override[tree,node]
            for k,bit in enumerate(record['bits']):assignment[bit]=bool((blocks>>k)&1)
            if record['flag']:
                assignment[record['flag']]=node in required
                assignment[record['excuse']]=node in required and not m
    return assignment


def check_source_export(search,assignment):
    snapshot=search.necessary_snapshot()
    population=snapshot['phase_population_allocation']
    source=population['query_source_clauses']
    exported=conjuncts(parse(snapshot['query_count_bound']))
    assert all(parse(clause) in exported for clause in source if clause!='true')
    assert not population['query_caps_are_permanent']
    assert population['costs_of_trees_are_not_added']
    assert population['empty_ancestor_allowance_per_tree']==1
    permanent=set(snapshot['permanent_assertions'])
    assert not any('(_ pble ' in clause for clause in permanent)
    assert not any(clause in permanent for clause in source if clause!='true')
    for tree in population['trees']:
        for node in tree['nodes']:
            for clause in node['permanent_source_clauses']:
                assert clause in permanent and evaluate(parse(clause),assignment)
    for tile in population['tile_sources']:
        for clause in tile['clauses']:
            assert clause in permanent and evaluate(parse(clause),assignment)
    assert all(evaluate(parse(clause),assignment) for clause in source)
    assert evaluate(parse(snapshot['query_count_bound']),assignment)
    return len(source)


def fixed_query(search,selected,expected='sat',override=None):
    search.flush()
    permanent=set(search.clauses)
    _,_,bound=search.query_bounds()
    assignment=allocation_assignment(search,selected,override)
    commands=['(push 1)',f'(assert {bound})']
    commands.extend('(assert '+(symbol if value else f'(not {symbol})')+')'
                    for symbol,value in assignment.items())
    offset=search.journal.tell()
    for command in commands:search.enqueue(command)
    search.flush()
    journal=(search.out/'model.smt2').read_text()
    assert journal[offset:]=='\n'.join(commands)+'\n','Legacy flush injected duplicate query caps.'
    status=search.smt.run('(check-sat)')
    assert status==expected,(status,expected,search.smt.run('(get-info :reason-unknown)'))
    search.enqueue('(pop 1)')
    search.flush()
    assert search.clauses==permanent,'A query modified permanent assertions.'
    return assignment


def journal_scope(search):
    depth=weighted=0
    for line in (search.out/'model.smt2').read_text().splitlines():
        if line=='(push 1)':depth+=1
        elif line=='(pop 1)':depth-=1
        elif '(_ pble ' in line:
            assert depth==1,'A population allocation bound escaped query scope.'
            weighted+=1
        assert depth in (0,1)
    assert depth==0 and weighted
    return weighted


def solver_controls(g,tiles,out):
    options=dict(sides=(5,3,7),grid_step=1,no_grid=False,
                 edge_tiles_per_round=8,vertex_fans_per_round=0,max_columns=0,time_limit=0,
                 root_file=str(PACKAGE/'corners/ROOTS_143.json'),root_id='O1-X2-Y2')
    search=PopulationWholeEdgeSearch(defaults(out=str(out),**options))
    selected=set(tiles)
    try:
        # Query the small current pool before growth. These normalized caps
        # must disappear on pop; the later actual allocation uses 5/15 blocks.
        search.insert(next(t for t in tiles if t[1]%2))
        fixed_query(search,set())
        for tile in tiles:search.insert(tile)
        search.load_root()
        search.boundary()
        for tile in tiles:
            for row,_ in g.rows(tile):search.install(row)
            search.install_tile_edges(tile)
        assignment=fixed_query(search,selected)
        source_count=check_source_export(search,assignment)
        ordinary=next(node for node,record in search.population_nodes[0].items()
                      if sum(search.tiles[i] in selected for i in record['own'])==105)
        fixed_query(search,selected,'unsat',{(0,ordinary):14})
        before=journal_scope(search)
        search.rebuild(1)
        assignment=fixed_query(search,selected)
        assert check_source_export(search,assignment)==source_count
        after=journal_scope(search)
        search.checkpoint(1,'exact143-population-whole-edge-control')
        status=json.loads((out/'status.json').read_text())
        assert status['scope']=='explicit-root-branch'
        assert status['population_query_caps_exported']
        assert not status['population_query_caps_permanent']
        result=dict(positive='sat',after_equivalent_rebuild='sat',underallocated_ordinary_node='unsat',
                    early_pool_caps_popped_before_growth=True,root_scope_preserved=True,
                    root_id='O1-X2-Y2',columns=len(search.tiles),complete_rows=len(search.exact),
                    whole_edge_obligations=len(search.edge_obligations),
                    population_node_counts=[len(nodes) for nodes in search.population_nodes],
                    population_variables=len(search.population_variables),
                    population_query_clauses=source_count,
                    permanent_assertions=len(search.clauses),
                    weighted_query_scopes_before_rebuild=before,
                    weighted_query_scopes_after_rebuild=after,
                    duplicate_legacy_flush_injection=False)
    finally:search.close()
    restarted=PopulationWholeEdgeSearch(defaults(out=str(out/'restart'),
        model_checkpoint=str(out/'necessary_model.json'),**options))
    try:
        restarted.load_root()
        restarted.boundary()
        assignment=fixed_query(restarted,selected)
        check_source_export(restarted,assignment)
        assert len(restarted.edge_obligations)==429 and len(restarted.exact)==335
        assert not restarted.restart_metadata['prior_root_assumptions_imported']
        assert restarted.root_metadata['id']=='O1-X2-Y2'
        journal_scope(restarted)
        result['after_geometric_restart']='sat'
        result['restart_regenerates_population_from_placements']=True
        result['prior_root_literals_not_imported']=True
        result['restarted_columns']=len(restarted.tiles)
    finally:restarted.close()
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--with-solver',action='store_true')
    mode.add_argument('--geometry-only',action='store_true',help='Default: no native solver required.')
    parser.add_argument('--out')
    parser.add_argument('--workdir')
    args=parser.parse_args()
    source=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    raw=source.read_bytes()
    data=json.loads(raw)
    assert data['N']==143 and data['sides']==[5,3,7]
    tiles=tuple((tuple(t[0]),*t[1:]) for t in data['tiles'])
    assert len(tiles)==len(set(tiles))==143
    g=core.Geometry(5,3,7)
    report=dict(status='PASS',control_sha256=hashlib.sha256(raw).hexdigest(),
                arithmetic=arithmetic_controls(g,tiles),full_target_excluded=False)
    if args.with_solver:
        if args.workdir:report['solver']=solver_controls(g,tiles,Path(args.workdir))
        else:
            with tempfile.TemporaryDirectory(prefix='population143-') as directory:
                report['solver']=solver_controls(g,tiles,Path(directory))
    if args.out:Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O: exact controls require assertions.')
    main()
