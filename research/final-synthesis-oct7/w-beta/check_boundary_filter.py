#!/usr/bin/env python3
"""Exact checks of formal boundary words; never a geometric tiling certificate."""
from math import gcd
import json

ALPHA, BETA, GAMMA, PI = (1, 0), (0, 1), (2, 1), (3, 2)

def complement(left, right):
    return tuple(PI[i] - left[i] - right[i] for i in range(2))

def run():
    # Each entry is (edge label, start angle, end angle, multiplicity).
    cases = 0
    first_example = None
    for v in range(2, 51):
        for u in range(1, v):
            if gcd(u, v) != 1:
                continue
            a, b, c = u*v, v*v-u*u, v*v
            lengths = {'a': a, 'b': b, 'c': c}
            for m in range(1, 13):
                if m == 1 and (u < 2 or v-u < 2):
                    continue
                equal = [('a', BETA, GAMMA, v),
                         ('c', BETA, ALPHA, m*v-u)]
                middle = [('c', BETA, ALPHA, m*u),
                          ('b', GAMMA, ALPHA, m*u)]
                short = [('c', ALPHA, BETA, m*(v-u)),
                         ('a', GAMMA, BETA, m*(v-u))]
                base = [('c', BETA, ALPHA, m*u),
                        ('b', GAMMA, ALPHA, m*u),
                        ('c', ALPHA, BETA, m*u)]
                words = [equal, middle, short, base]
                targets = [m*v**3, m*u*(2*v*v-u*u),
                           m*v*b, m*u*(3*v*v-u*u)]
                allowed = {ALPHA, BETA, GAMMA, (1, 2)}
                for word, target in zip(words, targets):
                    assert sum(lengths[s]*count for s,_,_,count in word) == target
                    assert all(count > 0 for _,_,_,count in word)
                    assert any(s == 'c' and count >= 2 for s,_,_,count in word)
                    for _, start, end, count in word:
                        if count >= 2:
                            assert complement(end, start) in allowed
                    for left, right in zip(word, word[1:]):
                        assert complement(left[2], right[1]) in allowed
                # W's beta corner uses one tile with incident a,c edges.
                assert (equal[0][0], middle[0][0]) == ('a', 'c')
                assert equal[0][1] == middle[0][1] == BETA
                assert equal[-1][2] == short[0][1] == ALPHA
                assert middle[-1][2] == ALPHA and short[-1][2] == BETA
                # The beta-isosceles base ends both have beta.
                assert base[0][1] == base[-1][2] == BETA
                assert base[0][0] == base[-1][0] == 'c'
                cases += 1
                if (u,v,m) == (2,3,2):
                    first_example = {'u':u, 'v':v, 'm':m,
                                     'W_side_lengths':targets[:3],
                                     'beta_base_length':targets[3]}
    return {'status':'PASS', 'cases':cases, 'v_max':50, 'm_max':12,
            'checks':'side lengths, c adjacency, formal endpoint angles and straight fans',
            'example':first_example,
            'geometric_placement_checked':False,
            'new_tiling_count_claimed':False,
            'full_Erdos634_solved':False}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
