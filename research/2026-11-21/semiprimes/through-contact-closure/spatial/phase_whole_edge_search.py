#!/usr/bin/env python3
"""Whole-edge physical closure with two separate ordinary-node budgets.

The target-specific no-empty-ancestor theorem is applied only at 3431/5063.
Every ordinary occupied node costs at least 2c tiles; the integral core
costs at least j=N mod c, and signed parity requires one extra c block.
The two trees' costs are NEVER added together.
"""
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PACKAGE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'CONTRIBUTING.md').exists())
sys.path[:0]=[str(PACKAGE/'whole-edges'),str(PACKAGE/'owned'),
             str(ROOT/'research/2026-11-20/semiprimes/continuation/vertex-phase')]
import whole_edge_search as driver
from whole_edge_search import WholeEdgeSearch
from legacy import core,and_
from phase_budget import PhaseBudget


class PhaseWholeEdgeSearch(WholeEdgeSearch):
    def __init__(self,args):
        self.phase_enabled=tuple(args.sides) in ((33,7,37),(35,13,43))
        self.phase_nodes=[{},{}]
        self.phase_implications={}
        g=core.Geometry(*args.sides)
        self.phase_oracles=[PhaseBudget(g,sign) for sign in (1,-1)] if self.phase_enabled else []
        # The odd global signed total additionally forces one ordinary
        # occupied node to use at least 3c tiles (NO_PHASE_GAPS.md, section 6).
        self.phase_limit=(g.N-g.N%g.c-g.c)//(2*g.c)
        super().__init__(args)

    def options(self):
        super().options()
        for nodes in self.phase_nodes:
            for symbol in nodes.values():
                self.enqueue(f'(declare-const {symbol} Bool)')

    def insert(self,tile):
        old=len(self.tiles)
        index=super().insert(tile)
        if len(self.tiles)==old or not self.phase_enabled:
            return index
        tile=self.tiles[index]
        flags=[]
        for tree,oracle in enumerate(self.phase_oracles):
            own=oracle.node(tile[0],oracle.sign*tile[1])
            nodes=set(oracle.required(tile))
            if own!=(0,0,0):nodes.add(own)
            assert (0,0,0) not in nodes
            for node in sorted(nodes):
                if node not in self.phase_nodes[tree]:
                    symbol=f'pn{tree}_{len(self.phase_nodes[tree])}'
                    self.phase_nodes[tree][node]=symbol
                    self.enqueue(f'(declare-const {symbol} Bool)')
                flags.append(self.phase_nodes[tree][node])
        if flags:
            clause=f'(=> x{index} {and_(flags)})'
            self.phase_implications[index]=clause
            self.assert_(clause)
        return index

    def query_bounds(self):
        total,reserves,bound=super().query_bounds()
        phase_caps=[core.atmost(self.phase_limit,list(nodes.values())) for nodes in self.phase_nodes]
        return total,reserves,and_([bound,*phase_caps])

    def necessary_snapshot(self):
        snapshot=super().necessary_snapshot()
        snapshot['ordinary_phase_budget']={
            'enabled':self.phase_enabled,'limit_per_tree':self.phase_limit,
            'core_minimum':self.g.N%self.g.c,
            'ordinary_node_minimum':2*self.g.c,
            'additional_odd_sign_block':self.g.c,
            'trees':[
                {'sign':sign,'nodes':[{'key':node,'symbol':symbol} for node,symbol in nodes.items()]}
                for sign,nodes in zip((1,-1),self.phase_nodes)],
            'tile_implications':[{'tile':index,'clause':clause} for index,clause in sorted(self.phase_implications.items())],
            'costs_of_trees_are_not_added':True}
        return snapshot


if __name__=='__main__':
    driver.WholeEdgeSearch=PhaseWholeEdgeSearch
    driver.main()
