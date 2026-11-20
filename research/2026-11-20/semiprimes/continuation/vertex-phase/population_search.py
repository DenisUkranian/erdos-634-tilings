#!/usr/bin/env python3
"""Exact per-node population budgets for endpoint projection searches.

The mathematical input is PHASE_BRANCHES.md.  Each ordinary nonempty phase
node has a population divisible by c and at least 2c; the single level-zero
core node has population N mod c modulo c.  At most one required exterior-free
ancestor node may be empty.  The two valuation trees are constrained separately.
"""
from __future__ import annotations

import json


def disjunction(variables):
    if not variables:
        return 'false'
    if len(variables) == 1:
        return variables[0]
    return '(or ' + ' '.join(variables) + ')'


def weighted_atmost(bound, weights, literals):
    assert len(weights) == len(literals)
    assert all(weight > 0 for weight in weights)
    if not literals or sum(weights) <= bound:
        return 'true'
    if bound < 0:
        return 'false'
    return '((_ pble ' + str(bound) + ' ' + ' '.join(map(str, weights)) + ') ' + ' '.join(literals) + ')'


def make_population_search_class(base, PhaseBudget):
    class PopulationSearch(base.Search):
        def __init__(self, args):
            self.population_nodes = [{}, {}]
            self.population_variables = []
            self.phase_budgets = []
            super().__init__(args)
            self.population_residue = self.g.N % self.g.c
            assert self.population_residue
            if getattr(args, 'no_phase_empty', False):
                assert tuple(args.sides) in ((33,7,37),(35,13,43)), 'Strict mode is scoped to the two audited target boards.'
            self.population_cap = (self.g.N-self.population_residue)//self.g.c
            self.population_bits = self.population_cap.bit_length()
            self.phase_budgets = [PhaseBudget(self.g, sign) for sign in (1,-1)]
            for tree in range(2):
                self.population_node(tree, (0,0,0))

        def options(self):
            super().options()
            # Search.rebuild calls options before restoring permanent clauses.
            for variable in self.population_variables:
                self.enqueue(f'(declare-const {variable} Bool)')

        def population_declare(self, variable):
            self.population_variables.append(variable)
            self.enqueue(f'(declare-const {variable} Bool)')

        def population_node(self, tree, node):
            if node in self.population_nodes[tree]:
                return self.population_nodes[tree][node]
            prefix = f'pn{tree}_{len(self.population_nodes[tree])}'
            bits = [f'{prefix}_b{k}' for k in range(self.population_bits)]
            for bit in bits:
                self.population_declare(bit)
            core = node == (0,0,0)
            higher = disjunction(bits[1:])
            if not core:
                # Exactly the forbidden value one has b0 true and every higher bit false.
                self.assert_(f'(=> {bits[0]} {higher})')
            record = dict(node=node, core=core, bits=bits, higher=higher,
                          own=[], flag=None, excuse=None)
            if self.phase_budgets[tree].exterior_free(node):
                assert not core
                flag, excuse = prefix+'_f', prefix+'_e'
                self.population_declare(flag)
                self.population_declare(excuse)
                record.update(flag=flag, excuse=excuse)
                self.assert_(f'(=> {flag} (or {higher} {excuse}))')
                self.assert_(f'(=> {excuse} {flag})')
                self.assert_(f'(=> {excuse} (not {disjunction(bits)}))')
            self.population_nodes[tree][node] = record
            return record

        def insert(self, tile):
            old = len(self.tiles)
            i = super().insert(tile)
            if len(self.tiles) == old:
                return i
            for tree, budget in enumerate(self.phase_budgets):
                own = budget.node(tile[0], budget.sign*tile[1])
                record = self.population_node(tree, own)
                record['own'].append(i)
                if not record['core']:
                    self.assert_(f'(=> x{i} {record["higher"]})')
                flags = []
                for node in budget.required(tile):
                    entry = self.population_node(tree, node)
                    assert entry['flag'] is not None
                    flags.append(entry['flag'])
                if flags:
                    self.assert_(f'(=> x{i} (and ' + ' '.join(flags) + '))')
            return i

        def population_query_clauses(self):
            result = []
            for tree, budget in enumerate(self.phase_budgets):
                weights, bits, flags, excuses = [], [], [], []
                for record in self.population_nodes[tree].values():
                    weights.extend(1 << k for k in range(self.population_bits))
                    bits.extend(record['bits'])
                    if record['flag']:
                        flags.append(record['flag'])
                        excuses.append(record['excuse'])
                    # WLOG use the smallest allocated count compatible with
                    # selected known tiles and the (possible) ancestor demand.
                    # Reducing this auxiliary count preserves every other
                    # condition and only decreases the global upper-bound sum.
                    # These are current-pool query bounds, not physical upper
                    # bounds on the unknown population of an actual tiling.
                    if record['core']:
                        excess = max(0, len(record['own'])-self.population_residue)
                        allocation_cap = (excess+self.g.c-1)//self.g.c
                    else:
                        allocation_cap = max(2, (len(record['own'])+self.g.c-1)//self.g.c)
                    allocation_cap = min(allocation_cap,self.population_cap)
                    if not record['core'] and allocation_cap == 2:
                        forbidden = [record['bits'][0]]+record['bits'][2:]
                        if forbidden:
                            result.append('(not '+disjunction(forbidden)+')')
                    elif allocation_cap == 0:
                        result.append('(not '+disjunction(record['bits'])+')')
                    elif allocation_cap < self.population_cap:
                        result.append(weighted_atmost(allocation_cap,
                                      [1<<k for k in range(self.population_bits)],record['bits']))
                    minimum_capacity = self.population_residue if record['core'] else 2*self.g.c
                    if len(record['own']) > minimum_capacity:
                        # m_v <= residue_v + c*k_v, with positive PB coefficients.
                        own = [f'x{i}' for i in record['own']]
                        negated = [f'(not {bit})' for bit in record['bits']]
                        costs = [1]*len(own) + [self.g.c*(1 << k) for k in range(self.population_bits)]
                        bound = self.g.c*((1 << self.population_bits)-1)
                        if record['core']:
                            bound += self.population_residue
                        result.append(weighted_atmost(bound, costs, own+negated))
                result.append(weighted_atmost(self.population_cap, weights, bits))
                empty_limit = 0 if getattr(self.args, 'no_phase_empty', False) else 1
                result.append(base.atmost(empty_limit, excuses))
                # This redundant cardinality inequality helps Boolean propagation.
                limit = self.population_cap//2 + empty_limit
                result.append(base.atmost(limit, flags))
            return result

        def flush(self):
            # Like the base tile-count cap, current population caps belong to
            # the live query scope. Re-emit on every query; never accumulate
            # obsolete subset population inequalities permanently.
            if '(push 1)' in self.stack:
                for clause in self.population_query_clauses():
                    if clause != 'true':
                        self.enqueue('(assert '+clause+')')
            return super().flush()

        def checkpoint(self, iteration, status):
            super().checkpoint(iteration, status)
            path = self.out/'status.json'
            report = json.loads(path.read_text())
            report.update(population_node_counts=[len(nodes) for nodes in self.population_nodes],
                          population_bit_width=getattr(self, 'population_bits', None),
                          population_residue=getattr(self, 'population_residue', None),
                          population_block_cap=getattr(self, 'population_cap', None),
                          population_allows_one_empty_ancestor=not getattr(self.args, 'no_phase_empty', False),
                          scope='Necessary phase-node population projection; not a tiling certificate.')
            path.write_text(json.dumps(report,indent=2)+'\n')

    return PopulationSearch
