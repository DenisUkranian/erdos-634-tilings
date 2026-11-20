#!/usr/bin/env python3
"""Couple the two signed phase trees through common physical-height capacities."""
import json

from population_search import weighted_atmost


def make_joint_height_search_class(SignedSearch):
    class JointHeightSearch(SignedSearch):
        def __init__(self,args):
            self.joint_heights = {}
            super().__init__(args)

        def signed_node(self,tree,node):
            record = super().signed_node(tree,node)
            h = self.phase_budgets[tree].sign*node[0]
            if h not in self.joint_heights:
                index = len(self.joint_heights)
                bits = [[f'jh{index}_s{sign}_b{k}' for k in range(self.signed_widths[sign])]
                        for sign in range(2)]
                for group in bits:
                    for bit in group:
                        self.signed_declare(bit)
                self.joint_heights[h] = bits
            return record

        def signed_query_clauses(self):
            # The uncoupled bounds are redundant but useful propagation lemmas.
            result = super().signed_query_clauses()
            for tree,budget in enumerate(self.phase_budgets):
                groups = {}
                for record in self.signed_nodes[tree].values():
                    h = budget.sign*record['node'][0]
                    for sign in range(2):
                        weights,literals = groups.setdefault((h,sign),([],[]))
                        weights.extend(1<<k for k in range(len(record['bits'][sign])))
                        literals.extend(record['bits'][sign])
                for (h,sign),(weights,literals) in groups.items():
                    bits = self.joint_heights[h][sign]
                    width = len(bits)
                    # Sum of this tree's included node blocks at h <= H_h,sign.
                    result.append(weighted_atmost((1<<width)-1,
                                  weights+[1<<k for k in range(width)],
                                  literals+[f'(not {bit})' for bit in bits]))
            parity_groups = {(sign,parity):([],[]) for sign in range(2) for parity in range(2)}
            for h,groups in self.joint_heights.items():
                for sign,bits in enumerate(groups):
                    weights,literals = parity_groups[sign,h%2]
                    weights.extend(1<<k for k in range(len(bits)))
                    literals.extend(bits)
            specs = [((0,0),(0,1),self.signed_caps[0]),
                     ((1,0),(1,1),self.signed_caps[1]),
                     ((0,0),(1,1),self.signed_caps[0]+1),
                     ((1,0),(0,1),self.signed_caps[0]+self.signed_even_delta)]
            for first,second,cap in specs:
                w0,b0 = parity_groups[first]
                w1,b1 = parity_groups[second]
                result.append(weighted_atmost(cap,w0+w1,b0+b1))
            return result

        def checkpoint(self,iteration,status):
            super().checkpoint(iteration,status)
            path = self.out/'status.json'
            report = json.loads(path.read_text())
            report['joint_physical_heights'] = sorted(self.joint_heights)
            report['scope'] = 'Necessary signed phase-node projection coupled by common physical-height capacities; not a tiling certificate.'
            path.write_text(json.dumps(report,indent=2)+'\n')

    return JointHeightSearch
