#!/usr/bin/env python3
"""Signed/shared-height wrapper controls on the exact143 construction."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import tempfile

from joint_whole_edge_search import PACKAGE,ROOT,JointWholeEdgeSearch,PhaseBudget,core
from owned_search import defaults
from verify_population_wrapper import evaluate,conjuncts,journal_scope,parse
from verify_owned_controls import exact_physical_control


def tile_sign(tile):
    return 0 if tile[3]*(-1 if tile[2]%2 else 1)==1 else 1


def arithmetic_controls(g,tiles):
    exact_physical_control(g,tiles)
    c,d,N=g.c,g.a-g.b,g.N
    j=N%c
    core_G=((g.A+g.B)*pow(d,-1,c))%c
    residues=[((j+core_G)*pow(2,-1,c))%c,((j-core_G)*pow(2,-1,c))%c]
    totals=[(N-c-d)//2,(N+c+d)//2]
    caps=[(total-residue)//c for total,residue in zip(totals,residues)]
    delta=(d+residues[0]-residues[1])//c
    assert residues==[4,6] and totals==[67,76] and caps==[9,10] and delta==0
    assert [sum(tile_sign(t)==s for t in tiles) for s in range(2)]==totals
    height_counts=Counter((t[1],tile_sign(t)) for t in tiles)
    height_blocks={(h,s):(m-(residues[s] if h==0 else 0))//c
                   for (h,s),m in height_counts.items()}
    trees=[]
    for sign in (1,-1):
        budget=PhaseBudget(g,sign)
        counts=Counter((budget.node(t[0],sign*t[1]),tile_sign(t)) for t in tiles)
        groups=Counter()
        for (node,s),m in counts.items():
            residue=residues[s] if node==(0,0,0) else 0
            assert (m-residue)%c==0
            k=(m-residue)//c
            assert k>=0
            groups[sign*node[0],s]+=k
        assert dict(groups)==height_blocks
        assert [sum(v for (h,s),v in groups.items() if s==signindex) for signindex in range(2)]==caps
        assert all(sum(m for (at,_),m in counts.items() if at==node)>=2*c
                   for node,_ in counts if node!=(0,0,0))
        required={node for t in tiles for node in budget.required(t)}
        assert not required
        trees.append(dict(sign=sign,node_sign_populations=[
            dict(key=node,epsilon=1 if s==0 else -1,population=m,
                 blocks=(m-(residues[s] if node==(0,0,0) else 0))//c)
            for (node,s),m in sorted(counts.items())]))
    # Independently eliminate the one unknown even positive block total.
    cases=0
    for positive_cap in range(5):
        for delta in (0,1):
            negative_cap=positive_cap+delta+1
            for A,B,C,D in itertools.product(range(negative_cap+2),repeat=4):
                inequalities=(A+B<=positive_cap and C+D<=negative_cap
                              and A+D<=positive_cap+1 and C+B<=positive_cap+delta)
                completion=any(E>=A and positive_cap-E>=B and E+delta>=C
                               and positive_cap-E+1>=D for E in range(positive_cap+1))
                assert inequalities==completion
                cases+=1
    return dict(physical143_verified=True,core_residues=residues,signed_totals=totals,
                block_caps=caps,trees=trees,
                physical_height_blocks=[dict(height=h,epsilon=1 if s==0 else -1,blocks=k)
                                        for (h,s),k in sorted(height_blocks.items())],
                exact_parity_completion_cases=cases,physical_height_cost_counted_once=True)


def fixed_assignment(search,selected,node_override=None,height_override=None):
    assignment={f'x{i}':t in selected for i,t in enumerate(search.tiles)}
    height_allocations={h:[0,0] for h in search.joint_heights}
    for tree,budget in enumerate(search.phase_budgets):
        counts=Counter((budget.node(t[0],budget.sign*t[1]),tile_sign(t)) for t in selected)
        required={node for t in selected for node in budget.required(t)}
        this_height=Counter()
        for node,record in search.signed_nodes[tree].items():
            values=[]
            for sign in range(2):
                residue=search.signed_residues[sign] if record['core'] else 0
                values.append((max(0,counts[node,sign]-residue)+search.g.c-1)//search.g.c)
            if not record['core'] and sum(values)==1:
                # Only needed for arbitrary partial selections. The exact143
                # positive control and the empty small-pool query avoid it.
                values[0 if values[0] else 1]+=1
            for sign,bits in enumerate(record['bits']):
                value=values[sign]
                if node_override and (tree,node,sign) in node_override:
                    value=node_override[tree,node,sign]
                for k,bit in enumerate(bits):assignment[bit]=bool((value>>k)&1)
                this_height[budget.sign*node[0],sign]+=value
            if record['flag']:
                assignment[record['flag']]=node in required
                assignment[record['excuse']]=node in required and not sum(values)
        for (height,sign),value in this_height.items():
            height_allocations[height][sign]=max(height_allocations[height][sign],value)
    for height,groups in search.joint_heights.items():
        for sign,bits in enumerate(groups):
            value=height_allocations[height][sign]
            if height_override and (height,sign) in height_override:value=height_override[height,sign]
            for k,bit in enumerate(bits):assignment[bit]=bool((value>>k)&1)
    return assignment


def check_source_export(search,assignment):
    snapshot=search.necessary_snapshot()
    signed=snapshot['signed_phase_population_allocation']
    source=signed['query_source_clauses']
    assert source==signed['uncoupled_query_source_clauses']+signed['joint_query_source_clauses']
    assert signed['joint_physical_heights_enabled']
    assert signed['core_residues']==[4,6] and signed['block_caps']==[9,10]
    assert signed['empty_ancestor_allowance_per_tree']==1
    assert signed['tree_populations_are_not_added'] and not signed['query_caps_are_permanent']
    exported=conjuncts(parse(snapshot['query_count_bound']))
    assert all(parse(clause) in exported for clause in source if clause!='true')
    permanent=set(snapshot['permanent_assertions'])
    assert not any('(_ pble ' in clause for clause in permanent)
    assert not any(clause in permanent for clause in source if clause!='true')
    for tree in signed['trees']:
        for node in tree['nodes']:
            for clause in node['permanent_source_clauses']:
                assert clause in permanent and evaluate(parse(clause),assignment)
    for record in signed['tile_sources']:
        for clause in record['clauses']:
            assert clause in permanent and evaluate(parse(clause),assignment)
    assert all(evaluate(parse(clause),assignment) for clause in source)
    assert evaluate(parse(snapshot['query_count_bound']),assignment)
    return len(source)


def fixed_query(search,selected,expected='sat',node_override=None,height_override=None):
    search.flush()
    permanent=set(search.clauses)
    _,_,bound=search.query_bounds()
    assignment=fixed_assignment(search,selected,node_override,height_override)
    commands=['(push 1)',f'(assert {bound})']
    commands.extend('(assert '+(symbol if value else f'(not {symbol})')+')'
                    for symbol,value in assignment.items())
    offset=search.journal.tell()
    for command in commands:search.enqueue(command)
    search.flush()
    assert (search.out/'model.smt2').read_text()[offset:]=='\n'.join(commands)+'\n'
    status=search.smt.run('(check-sat)')
    assert status==expected,(status,expected,search.smt.run('(get-info :reason-unknown)'))
    search.enqueue('(pop 1)')
    search.flush()
    assert search.clauses==permanent
    return assignment


def solver_controls(g,tiles,out):
    options=dict(sides=(5,3,7),grid_step=1,no_grid=False,
                 edge_tiles_per_round=8,vertex_fans_per_round=0,max_columns=0,time_limit=0,
                 root_file=str(PACKAGE/'corners/ROOTS_143.json'),root_id='O1-X2-Y2')
    search=JointWholeEdgeSearch(defaults(out=str(out),**options))
    selected=set(tiles)
    try:
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
        ordinary=next(node for node,record in search.signed_nodes[0].items()
                      if sum(search.tiles[i] in selected for i in record['own'][0])==49)
        fixed_query(search,selected,'unsat',node_override={(0,ordinary,0):6})
        fixed_query(search,selected,'unsat',height_override={(1,0):6})
        before=journal_scope(search)
        search.rebuild(1)
        assignment=fixed_query(search,selected)
        assert check_source_export(search,assignment)==source_count
        after=journal_scope(search)
        search.checkpoint(1,'exact143-signed-joint-whole-edge-control')
        status=json.loads((out/'status.json').read_text())
        assert status['scope']=='explicit-root-branch'
        assert status['signed_query_caps_exported'] and not status['signed_query_caps_permanent']
        result=dict(positive='sat',after_equivalent_rebuild='sat',
                    underallocated_positive_node='unsat',underallocated_common_height='unsat',
                    early_pool_caps_popped_before_growth=True,root_scope_preserved=True,
                    root_id='O1-X2-Y2',columns=len(search.tiles),complete_rows=len(search.exact),
                    whole_edge_obligations=len(search.edge_obligations),
                    signed_node_counts=[len(nodes) for nodes in search.signed_nodes],
                    signed_and_joint_variables=len(search.signed_variables),
                    joint_physical_heights=sorted(search.joint_heights),
                    signed_and_joint_query_clauses=source_count,permanent_assertions=len(search.clauses),
                    weighted_query_scopes_before_rebuild=before,
                    weighted_query_scopes_after_rebuild=after,duplicate_legacy_flush_injection=False)
    finally:search.close()
    restarted=JointWholeEdgeSearch(defaults(out=str(out/'restart'),
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
        result['restart_regenerates_signed_nodes_and_joint_heights']=True
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
            with tempfile.TemporaryDirectory(prefix='joint143-') as directory:
                report['solver']=solver_controls(g,tiles,Path(directory))
    if args.out:Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O: exact controls require assertions.')
    main()
