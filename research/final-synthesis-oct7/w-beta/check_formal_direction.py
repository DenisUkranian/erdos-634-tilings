#!/usr/bin/env python3
"""Coefficientwise direction identities and exact population padding."""
from pathlib import Path
from math import gcd
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'w-beta-caps'))
from laurent import Polynomial as Poly, u, v, T as X

def run():
    a, b, c = u*v, v*v-u*u, v*v
    Q, P = 2*v*v-u*u, 3*v*v-u*u
    f = a-b*X-c*X**3
    f_inv = a-b/X-c/(X**3)
    U = v/X-u/(X**2)
    Vw = v*X
    Vb = v*X-v/X
    Bw = v*b/(X**2)+u*Q/X-v**3*X**2
    Bb = -v**3*X**2+u*P/X-v**3/(X**4)
    assert not (U*f-Vw*f_inv-Bw)
    assert not (U*f-Vb*f_inv-Bb)
    assert not (f+(v*X-u)*(v*X**2+u*X+v))
    cases = 0
    for vi in range(2, 101):
        for ui in range(1, vi):
            if gcd(ui,vi) != 1:
                continue
            qi, pi = 2*vi*vi-ui*ui, 3*vi*vi-ui*ui
            assert qi-ui-2*vi >= vi*(vi-1)
            assert pi-ui-3*vi >= 2*vi*(vi-1)
            for mi in range(1, 21):
                for coefficient, sparse in [(qi, ui+2*vi),(pi,ui+3*vi)]:
                    n = coefficient*mi*mi
                    n0 = sparse*mi
                    assert n >= n0 and (n-n0)%2 == 0
                    assert n0+2*((n-n0)//2) == n
                cases += 1
    return {'status':'PASS', 'symbolic_identities':3,
            'symbolic_ring':'Q[u,v,X,X^-1]; arbitrary common integer factor m',
            'integer_parameter_scale_cases':cases,
            'v_max':100, 'm_max':20,
            'W7_sparse_tiles':5, 'W7_half_turn_pairs':1,
            'beta11_sparse_tiles':7, 'beta11_half_turn_pairs':2,
            'geometry_or_nonoverlap_claimed':False,
            'new_tiling_count_claimed':False,
            'full_Erdos634_solved':False}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
