#!/usr/bin/env python3
"""Signed phase-node population budgets, including exact parity completion.

Dependencies: odd primitive norm-tile phase populations; nodewise edge
characters; and, in strict target mode, the no-remote-gaps theorem.
"""
from __future__ import annotations
import json

from population_search import disjunction, weighted_atmost


def make_signed_population_search_class(base, PhaseBudget):
    class SignedPopulationSearch(base.Search):
        def __init__(self, args):
            self.signed_nodes = [{}, {}]
            self.signed_variables = []
            self.phase_budgets = []
            super().__init__(args)
            assert self.g.a % 2 == self.g.b % 2 == self.g.c % 2 == 1
            if getattr(args,'no_phase_empty',False):
                assert tuple(args.sides) in ((33,7,37),(35,13,43))
            c, d, N = self.g.c, self.g.a-self.g.b, self.g.N
            j = N%c
            core_G = ((self.g.A+self.g.B)*pow(d,-1,c))%c
            inv2 = pow(2,-1,c)
            self.signed_residues = [((j+core_G)*inv2)%c,((j-core_G)*inv2)%c]
            self.signed_totals = [(N-c-d)//2,(N+c+d)//2]
            assert sum(self.signed_totals) == N
            self.signed_caps = []
            for total,residue in zip(self.signed_totals,self.signed_residues):
                assert (total-residue)%c == 0
                self.signed_caps.append((total-residue)//c)
            self.signed_widths = [cap.bit_length() for cap in self.signed_caps]
            assert min(self.signed_widths) >= 2
            self.signed_even_delta = (d+self.signed_residues[0]-self.signed_residues[1])//c
            assert self.signed_even_delta*c == d+self.signed_residues[0]-self.signed_residues[1]
            assert self.signed_even_delta in (0,1)
            assert self.signed_caps[1] == self.signed_caps[0]+self.signed_even_delta+1
            self.phase_budgets = [PhaseBudget(self.g, sign) for sign in (1,-1)]
            for tree in range(2):
                self.signed_node(tree,(0,0,0))

        def options(self):
            super().options()
            for variable in self.signed_variables:
                self.enqueue(f'(declare-const {variable} Bool)')

        def signed_declare(self, variable):
            self.signed_variables.append(variable)
            self.enqueue(f'(declare-const {variable} Bool)')

        def signed_node(self, tree, node):
            if node in self.signed_nodes[tree]:
                return self.signed_nodes[tree][node]
            prefix = f'spn{tree}_{len(self.signed_nodes[tree])}'
            bits = [[f'{prefix}_s{sign}_b{k}' for k in range(self.signed_widths[sign])]
                    for sign in range(2)]
            for group in bits:
                for bit in group:
                    self.signed_declare(bit)
            core = node == (0,0,0)
            higher = disjunction(bits[0][1:]+bits[1][1:])
            positive = disjunction([higher,f'(and {bits[0][0]} {bits[1][0]})'])
            if not core:
                self.assert_(f'(=> {bits[0][0]} (or {higher} {bits[1][0]}))')
                self.assert_(f'(=> {bits[1][0]} (or {higher} {bits[0][0]}))')
            record = dict(node=node,core=core,bits=bits,positive=positive,
                          present=[disjunction(group) for group in bits],
                          own=[[],[]],flag=None,excuse=None)
            if self.phase_budgets[tree].exterior_free(node):
                assert not core
                flag,excuse = prefix+'_f',prefix+'_e'
                self.signed_declare(flag)
                self.signed_declare(excuse)
                record.update(flag=flag,excuse=excuse)
                self.assert_(f'(=> {flag} (or {positive} {excuse}))')
                self.assert_(f'(=> {excuse} {flag})')
                self.assert_(f'(=> {excuse} (not {disjunction(bits[0]+bits[1])}))')
            self.signed_nodes[tree][node] = record
            return record

        @staticmethod
        def tile_sign(tile):
            return 0 if tile[3]*(-1 if tile[2]%2 else 1) == 1 else 1

        def insert(self, tile):
            old = len(self.tiles)
            i = super().insert(tile)
            if len(self.tiles) == old:
                return i
            sign = self.tile_sign(tile)
            for tree,budget in enumerate(self.phase_budgets):
                own = budget.node(tile[0],budget.sign*tile[1])
                record = self.signed_node(tree,own)
                record['own'][sign].append(i)
                if not record['core']:
                    self.assert_(f'(=> x{i} {record["present"][sign]})')
                    self.assert_(f'(=> x{i} {record["positive"]})')
                flags = []
                for node in budget.required(tile):
                    entry = self.signed_node(tree,node)
                    assert entry['flag'] is not None
                    flags.append(entry['flag'])
                if flags:
                    self.assert_(f'(=> x{i} (and '+' '.join(flags)+'))')
            return i

        def signed_query_clauses(self):
            result = []
            for tree,budget in enumerate(self.phase_budgets):
                groups = {(sign,parity):([],[]) for sign in range(2) for parity in range(2)}
                flags,excuses = [],[]
                for record in self.signed_nodes[tree].values():
                    parity = record['node'][0]%2
                    if record['flag']:
                        flags.append(record['flag'])
                        excuses.append(record['excuse'])
                    for sign in range(2):
                        bits = record['bits'][sign]
                        width = len(bits)
                        own = record['own'][sign]
                        residue = self.signed_residues[sign] if record['core'] else 0
                        gw,gb = groups[sign,parity]
                        gw.extend(1<<k for k in range(width))
                        gb.extend(bits)
                        minimum_capacity = residue if record['core'] else self.g.c
                        if len(own) > minimum_capacity:
                            literals = [f'x{i}' for i in own]+[f'(not {bit})' for bit in bits]
                            weights = [1]*len(own)+[self.g.c*(1<<k) for k in range(width)]
                            bound = self.g.c*((1<<width)-1)+residue
                            result.append(weighted_atmost(bound,weights,literals))
                        # A current-pool witness normal form, not a physical
                        # upper bound on the unknown actual node population.
                        if record['core']:
                            extra = max(0,len(own)-residue)
                            cap = (extra+self.g.c-1)//self.g.c
                        else:
                            cap = max(2,(len(own)+self.g.c-1)//self.g.c)
                        cap = min(cap,self.signed_caps[sign])
                        if cap == 0:
                            result.append('(not '+disjunction(bits)+')')
                        elif cap == 1:
                            result.append('(not '+disjunction(bits[1:])+')')
                        elif cap == 2:
                            if bits[2:]:
                                result.append('(not '+disjunction(bits[2:])+')')
                            result.append(base.atmost(1,bits[:2]))
                        elif cap < self.signed_caps[sign]:
                            result.append(weighted_atmost(cap,[1<<k for k in range(width)],bits))
                # Exact elimination of unknown parity-block completion counts.
                specifications = [((0,0),(0,1),self.signed_caps[0]),
                                  ((1,0),(1,1),self.signed_caps[1]),
                                  ((0,0),(1,1),self.signed_caps[0]+1),
                                  ((1,0),(0,1),self.signed_caps[0]+self.signed_even_delta)]
                for first,second,cap in specifications:
                    w0,b0 = groups[first]
                    w1,b1 = groups[second]
                    result.append(weighted_atmost(cap,w0+w1,b0+b1))
                empty_limit = 0 if getattr(self.args,'no_phase_empty',False) else 1
                result.append(base.atmost(empty_limit,excuses))
                # In an actual tiling some odd-height ordinary node has an
                # odd block count, hence at least three blocks. This bounds
                # the actual occupied-node count, independently of whether
                # a normalized partial-pool allocation displays that odd node.
                result.append(base.atmost((sum(self.signed_caps)-1)//2+empty_limit,flags))
            return result

        def flush(self):
            if '(push 1)' in self.stack:
                for clause in self.signed_query_clauses():
                    if clause != 'true':
                        self.enqueue('(assert '+clause+')')
            return super().flush()

        def checkpoint(self, iteration, status):
            super().checkpoint(iteration,status)
            path = self.out/'status.json'
            report = json.loads(path.read_text())
            report.update(signed_population_node_counts=[len(nodes) for nodes in self.signed_nodes],
                          signed_core_residues=getattr(self,'signed_residues',None),
                          signed_block_caps=getattr(self,'signed_caps',None),
                          signed_bit_widths=getattr(self,'signed_widths',None),
                          signed_even_delta=getattr(self,'signed_even_delta',None),
                          population_allows_one_empty_ancestor=not getattr(self.args,'no_phase_empty',False),
                          scope='Necessary signed phase-node projection with exact parity completion; not a tiling certificate.')
            path.write_text(json.dumps(report,indent=2)+'\n')

    return SignedPopulationSearch
