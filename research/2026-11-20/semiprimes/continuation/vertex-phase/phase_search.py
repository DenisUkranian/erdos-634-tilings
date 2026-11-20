#!/usr/bin/env python3
"""Global endpoint SAT with a separate budget on each p-adic phase tree."""
import argparse
from collections import Counter
from pathlib import Path
import sys

try:
    from global_core_sat import Geometry, Search, SMT, atmost
except ModuleNotFoundError:
    preliminary=argparse.ArgumentParser(add_help=False)
    preliminary.add_argument('--base-dir',default=str(Path(__file__).resolve().parent.parent/'global-endpoints'/'integer'))
    known,_=preliminary.parse_known_args()
    sys.path.insert(0,known.base_dir)
    from global_core_sat import Geometry, Search, SMT, atmost
from phase_budget import PhaseBudget


class PhaseSearch(Search):
    def __init__(self, args):
        self.phase_nodes = [{}, {}]
        self.phase_outside = [[], []]
        self.phase_dirty = True
        self.phase_budgets = []
        super().__init__(args)
        self.phase_budgets = [PhaseBudget(self.g, s) for s in (1, -1)]

    def insert(self, tile):
        existed = tile in self.index
        i = super().insert(tile)
        if existed:
            return i
        self.phase_dirty = True
        for tree, budget in enumerate(self.phase_budgets):
            own=budget.node(tile[0],budget.sign*tile[1])
            if not budget.exterior_free(own):
                self.phase_outside[tree].append(i)
            variables = []
            for node in budget.required(tile):
                if node not in self.phase_nodes[tree]:
                    var = f'p{tree}_{len(self.phase_nodes[tree])}'
                    self.phase_nodes[tree][node] = var
                    self.enqueue(f'(declare-const {var} Bool)')
                    self.phase_dirty = True
                variables.append(self.phase_nodes[tree][node])
            if variables:
                self.assert_(f'(=> x{i} (and ' + ' '.join(variables) + '))')
        return i

    def flush(self):
        # Search.run opens one temporary scope for the current tile-count cap.
        # Install the current four phase caps in that same scope on EVERY
        # query.  Old subset caps are implied by the new caps, so retaining
        # them permanently only wastes solver memory.
        if '(push 1)' in self.stack:
            for tree, budget in enumerate(self.phase_budgets):
                phases=list(self.phase_nodes[tree].values())
                outside=[f'x{i}' for i in self.phase_outside[tree]]
                costs=[2*self.g.c]*len(phases)+[1]*len(outside)
                weighted=f'((_ pble {self.g.N+2*self.g.c} '+ ' '.join(map(str,costs))+') '+ ' '.join(phases+outside)+')'
                for clause in [atmost(budget.limit,phases),weighted]:
                    if clause!='true':
                        self.enqueue('(assert '+clause+')')
            self.phase_dirty = False
        return super().flush()

    def rebuild(self, iteration):
        self.checkpoint(iteration, 'rebuilding-equivalent-context')
        self.smt.close()
        self.smt = SMT()
        self.journal.close()
        self.journal = (self.out/'model.smt2').open('w')
        self.stack.clear()
        self.options()
        for i in range(len(self.tiles)):
            self.enqueue(f'(declare-const x{i} Bool)')
        for tree in self.phase_nodes:
            for var in tree.values():
                self.enqueue(f'(declare-const {var} Bool)')
        for clause in sorted(self.clauses):
            self.enqueue('(assert '+clause+')')
        self.guard_clauses = {guard:self.guard_clauses[guard] for guard in self.guard_rows}
        self.clause_guard = {clause:guard for guard,clause in self.guard_clauses.items()}
        for guard, clause in self.guard_clauses.items():
            self.enqueue(f'(declare-const {guard} Bool)')
            self.enqueue(f'(assert (=> {guard} {clause}))')
        print('rebuild', iteration, 'phase nodes', [len(t) for t in self.phase_nodes],
              'active guards', len(self.guard_rows), flush=True)

    def checkpoint(self, iteration, status):
        super().checkpoint(iteration, status)
        import json
        path=self.out/'status.json'
        report=json.loads(path.read_text())
        report['phase_node_counts']=[len(t) for t in self.phase_nodes]
        report['phase_node_limits']=[t.limit for t in self.phase_budgets]
        report['scope']='Conditional on the cited phase-tree theorem; no height or placement bound imposed.'
        path.write_text(json.dumps(report,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sides',type=int,nargs=3)
    parser.add_argument('--base-dir',help='Base endpoint package; normally found relative to this package.')
    parser.add_argument('--out',required=True)
    parser.add_argument('--seed-json')
    parser.add_argument('--rows')
    parser.add_argument('--timeout-ms',type=int,default=45000)
    parser.add_argument('--rounds',type=int,default=1000)
    parser.add_argument('--expand',type=int,default=100)
    parser.add_argument('--random-seed',type=int,default=1776)
    parser.add_argument('--proof',action='store_true')
    parser.add_argument('--minimize-core',action='store_true')
    parser.add_argument('--max-columns',type=int,default=300000)
    parser.add_argument('--core-policy',choices=('random','defect'),default='defect')
    parser.add_argument('--point-checkpoint')
    parser.add_argument('--rebuild-every',type=int,default=10)
    PhaseSearch(parser.parse_args()).run()


if __name__=='__main__':
    main()
