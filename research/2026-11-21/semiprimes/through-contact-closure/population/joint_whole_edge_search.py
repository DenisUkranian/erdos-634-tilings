#!/usr/bin/env python3
"""Optional signed population and shared-height budgets around whole geometry.

Both allocation factories are reused unchanged. All current-pool and
completion constraints are explicit parts of the exported live query.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from types import SimpleNamespace

PACKAGE=Path(__file__).resolve().parents[1]
ROOT=next(p for p in PACKAGE.parents if (p/'CONTRIBUTING.md').exists())
PHASE=ROOT/'research/2026-11-20/semiprimes/continuation/vertex-phase'
sys.path[:0]=[str(PACKAGE/'spatial'),str(PACKAGE/'whole-edges'),str(PACKAGE/'owned'),str(PHASE)]
import whole_edge_search as driver
from phase_whole_edge_search import PhaseWholeEdgeSearch
from phase_budget import PhaseBudget
from population_search import disjunction
from signed_population_search import make_signed_population_search_class
from joint_height_search import make_joint_height_search_class
from legacy import core,and_


SignedBase=make_signed_population_search_class(
    SimpleNamespace(Search=PhaseWholeEdgeSearch,atmost=core.atmost),PhaseBudget)
JointBase=make_joint_height_search_class(SignedBase)


class JointWholeEdgeSearch(JointBase):
    def __init__(self,args):
        self.signed_node_sources={}
        self.signed_tile_sources={}
        args.no_phase_empty=tuple(args.sides) in ((33,7,37),(35,13,43))
        super().__init__(args)

    def signed_node(self,tree,node):
        if node in self.signed_nodes[tree]:
            return self.signed_nodes[tree][node]
        record=super().signed_node(tree,node)
        clauses=[]
        if not record['core']:
            bits=record['bits']
            higher=disjunction(bits[0][1:]+bits[1][1:])
            clauses.extend([
                f'(=> {bits[0][0]} (or {higher} {bits[1][0]}))',
                f'(=> {bits[1][0]} (or {higher} {bits[0][0]}))'])
        if record['flag']:
            clauses.extend([
                f'(=> {record["flag"]} (or {record["positive"]} {record["excuse"]}))',
                f'(=> {record["excuse"]} {record["flag"]})',
                f'(=> {record["excuse"]} (not {disjunction(record["bits"][0]+record["bits"][1])}))'])
        assert all(clause in self.clauses for clause in clauses)
        self.signed_node_sources[tree,node]=tuple(clauses)
        return record

    def insert(self,tile):
        # The legacy signed factory reads its argument after super().insert.
        tile=self.canonical_tile(tile)
        old=len(self.tiles)
        index=super().insert(tile)
        if len(self.tiles)==old:
            return index
        tile=self.tiles[index]
        sign=self.tile_sign(tile)
        clauses=[]
        for tree,budget in enumerate(self.phase_budgets):
            own=budget.node(tile[0],budget.sign*tile[1])
            record=self.signed_nodes[tree][own]
            if not record['core']:
                clauses.extend([f'(=> x{index} {record["present"][sign]})',
                                f'(=> x{index} {record["positive"]})'])
            flags=[self.signed_nodes[tree][node]['flag'] for node in budget.required(tile)]
            if flags:clauses.append(f'(=> x{index} (and '+' '.join(flags)+'))')
        assert all(clause in self.clauses for clause in clauses)
        self.signed_tile_sources[index]=tuple(clauses)
        return index

    def query_bounds(self):
        total,reserves,bound=PhaseWholeEdgeSearch.query_bounds(self)
        return total,reserves,and_([bound,*self.signed_query_clauses()])

    def flush(self):
        # Bypass the historical signed flush hook: query_bounds already
        # includes all signed and common-height allocation constraints.
        return PhaseWholeEdgeSearch.flush(self)

    def necessary_snapshot(self):
        snapshot=PhaseWholeEdgeSearch.necessary_snapshot(self)
        uncoupled=SignedBase.signed_query_clauses(self)
        complete=self.signed_query_clauses()
        assert complete[:len(uncoupled)]==uncoupled
        snapshot['signed_phase_population_allocation']={
            'enabled':True,'joint_physical_heights_enabled':True,
            'hypotenuse':self.g.c,
            'core_residues':list(self.signed_residues),
            'signed_totals':list(self.signed_totals),
            'block_caps':list(self.signed_caps),'bit_widths':list(self.signed_widths),
            'even_delta':self.signed_even_delta,
            'sign_index_epsilon':[1,-1],
            'strict_no_empty_ancestor':bool(self.args.no_phase_empty),
            'empty_ancestor_allowance_per_tree':0 if self.args.no_phase_empty else 1,
            'variables':list(self.signed_variables),
            'trees':[
                dict(sign=budget.sign,nodes=[
                    dict(key=node,core=record['core'],bits=[list(group) for group in record['bits']],
                         positive=record['positive'],present=list(record['present']),
                         own=[list(group) for group in record['own']],
                         flag=record['flag'],excuse=record['excuse'],
                         permanent_source_clauses=list(self.signed_node_sources[tree,node]))
                    for node,record in self.signed_nodes[tree].items()])
                for tree,budget in enumerate(self.phase_budgets)],
            'tile_sources':[dict(tile=i,clauses=list(clauses))
                            for i,clauses in sorted(self.signed_tile_sources.items())],
            'joint_heights':[dict(height=h,bits=[list(group) for group in groups])
                             for h,groups in self.joint_heights.items()],
            'uncoupled_query_source_clauses':uncoupled,
            'joint_query_source_clauses':complete[len(uncoupled):],
            'query_source_clauses':complete,
            'allocation_caps_are_current_pool_normalizations':True,
            'query_caps_are_permanent':False,
            'tree_populations_are_not_added':True,
            'independent_semantic_audit_required':True,
            'source_factories':[
                'research/2026-11-20/semiprimes/continuation/vertex-phase/signed_population_search.py',
                'research/2026-11-20/semiprimes/continuation/vertex-phase/joint_height_search.py']}
        return snapshot

    def checkpoint(self,iteration,status):
        # Preserve unrestricted-board versus explicit-root-branch scope.
        PhaseWholeEdgeSearch.checkpoint(self,iteration,status)
        path=self.out/'status.json'
        report=json.loads(path.read_text())
        report.update(signed_population_node_counts=[len(nodes) for nodes in self.signed_nodes],
                      signed_core_residues=self.signed_residues,
                      signed_block_caps=self.signed_caps,
                      signed_bit_widths=self.signed_widths,
                      signed_even_delta=self.signed_even_delta,
                      joint_physical_heights=sorted(self.joint_heights),
                      signed_strict_no_empty_ancestor=bool(self.args.no_phase_empty),
                      signed_query_caps_exported=True,signed_query_caps_permanent=False,
                      signed_independent_semantic_audit_required=True)
        path.write_text(json.dumps(report,indent=2)+'\n')


def main():
    driver.WholeEdgeSearch=JointWholeEdgeSearch
    driver.main()


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact geometry assertions are required.')
    main()
