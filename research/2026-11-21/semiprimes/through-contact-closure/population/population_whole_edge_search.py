#!/usr/bin/env python3
"""Optional per-node population allocations around unrestricted whole geometry.

Reuse the historical audited allocation factory unchanged. Its dynamic
current-pool caps are included exactly once in the exported query bound,
not injected by its historical flush hook or made permanent.
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
from population_search import disjunction,make_population_search_class
from legacy import core,and_


AllocatedBase=make_population_search_class(
    SimpleNamespace(Search=PhaseWholeEdgeSearch,atmost=core.atmost),PhaseBudget)


class PopulationWholeEdgeSearch(AllocatedBase):
    def __init__(self,args):
        self.population_node_sources={}
        self.population_tile_sources={}
        args.no_phase_empty=tuple(args.sides) in ((33,7,37),(35,13,43))
        super().__init__(args)

    def population_node(self,tree,node):
        if node in self.population_nodes[tree]:
            return self.population_nodes[tree][node]
        record=super().population_node(tree,node)
        clauses=[]
        if not record['core']:
            clauses.append(f'(=> {record["bits"][0]} {record["higher"]})')
        if record['flag']:
            clauses.extend([
                f'(=> {record["flag"]} (or {record["higher"]} {record["excuse"]}))',
                f'(=> {record["excuse"]} {record["flag"]})',
                f'(=> {record["excuse"]} (not {disjunction(record["bits"])}))'])
        assert all(clause in self.clauses for clause in clauses)
        self.population_node_sources[tree,node]=tuple(clauses)
        return record

    def insert(self,tile):
        # The historical factory reads the argument again after super().insert;
        # normalize JSON lists before its cached phase-node lookup.
        tile=self.canonical_tile(tile)
        old=len(self.tiles)
        index=super().insert(tile)
        if len(self.tiles)==old:
            return index
        tile=self.tiles[index]
        clauses=[]
        for tree,budget in enumerate(self.phase_budgets):
            own=budget.node(tile[0],budget.sign*tile[1])
            record=self.population_nodes[tree][own]
            if not record['core']:
                clauses.append(f'(=> x{index} {record["higher"]})')
            flags=[self.population_nodes[tree][node]['flag'] for node in budget.required(tile)]
            if flags:
                clauses.append(f'(=> x{index} (and '+' '.join(flags)+'))')
        assert all(clause in self.clauses for clause in clauses)
        self.population_tile_sources[index]=tuple(clauses)
        return index

    def query_bounds(self):
        total,reserves,bound=PhaseWholeEdgeSearch.query_bounds(self)
        return total,reserves,and_([bound,*self.population_query_clauses()])

    def flush(self):
        # Bypass PopulationSearch.flush: the exact query conjunction above
        # already contains every allocation cap. This preserves one copy
        # inside each live query scope and exposes all of it to proof export.
        return PhaseWholeEdgeSearch.flush(self)

    def necessary_snapshot(self):
        snapshot=PhaseWholeEdgeSearch.necessary_snapshot(self)
        snapshot['phase_population_allocation']={
            'enabled':True,
            'hypotenuse':self.g.c,
            'core_residue':self.population_residue,
            'block_cap_per_tree':self.population_cap,
            'bit_width':self.population_bits,
            'strict_no_empty_ancestor':bool(self.args.no_phase_empty),
            'empty_ancestor_allowance_per_tree':0 if self.args.no_phase_empty else 1,
            'variables':list(self.population_variables),
            'trees':[
                dict(sign=budget.sign,nodes=[
                    dict(key=node,core=record['core'],bits=list(record['bits']),
                         higher=record['higher'],own=list(record['own']),
                         flag=record['flag'],excuse=record['excuse'],
                         permanent_source_clauses=list(self.population_node_sources[tree,node]))
                    for node,record in self.population_nodes[tree].items()])
                for tree,budget in enumerate(self.phase_budgets)],
            'tile_sources':[dict(tile=i,clauses=list(clauses))
                            for i,clauses in sorted(self.population_tile_sources.items())],
            'query_source_clauses':self.population_query_clauses(),
            'allocation_caps_are_current_pool_normalizations':True,
            'query_caps_are_permanent':False,
            'costs_of_trees_are_not_added':True,
            'source_factory':'research/2026-11-20/semiprimes/continuation/vertex-phase/population_search.py'}
        return snapshot

    def checkpoint(self,iteration,status):
        # Keep the whole-board/root-branch scope. The historical factory's
        # checkpoint replaces that scope with a generic population label.
        PhaseWholeEdgeSearch.checkpoint(self,iteration,status)
        path=self.out/'status.json'
        report=json.loads(path.read_text())
        report.update(population_node_counts=[len(nodes) for nodes in self.population_nodes],
                      population_bit_width=self.population_bits,
                      population_residue=self.population_residue,
                      population_block_cap=self.population_cap,
                      population_strict_no_empty_ancestor=bool(self.args.no_phase_empty),
                      population_query_caps_exported=True,
                      population_query_caps_permanent=False)
        path.write_text(json.dumps(report,indent=2)+'\n')


def main():
    driver.WholeEdgeSearch=PopulationWholeEdgeSearch
    driver.main()


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact geometry assertions are required.')
    main()
