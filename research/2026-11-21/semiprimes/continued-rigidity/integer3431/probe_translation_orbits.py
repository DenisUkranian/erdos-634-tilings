#!/usr/bin/env python3
"""Small integral torus kernels constrained to complete translation orbits.

A point is a valid unrestricted positive integer endpoint kernel if found.
An absence applies only to this translation-invariant search family.
Neither packing nor compatibility with neighboring gate charges is imposed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import time

U = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def run(a, b, c, total):
    start = time.monotonic()
    results = []
    for lx, ly in [(1, t) for t in range(c)]+[(0,1)]:
        labels, columns, incidence = [], [], defaultdict(list)
        for r in range(c):
            for j in range(6):
                for s in (-1,1):
                    du = -a*(lx*U[j][0]+ly*U[j][1])
                    dw = b*(lx*U[(j+s)%6][0]+ly*U[(j+s)%6][1])
                    terms = Counter()
                    for axis, t, value in ((j,r,s),(j,r+du,-s),
                                           (j+s,r+dw,s),(j+s,r,-s)):
                        terms[(axis%3,t%c)] += value
                    terms = {key:value for key,value in terms.items() if value}
                    k = len(labels)
                    labels.append((r,j,s)); columns.append(terms)
                    for key,value in terms.items():
                        incidence[key,value].append(k)
        states = 0
        seen = set()
        def visit(selected, residual, charge):
            nonlocal states
            key = tuple(sorted(selected))
            if key in seen:
                return None
            seen.add(key); states += 1
            left = total-len(selected)
            if abs(1-charge)>left or (left-(1-charge))%2:
                return None
            if not residual:
                return key if left==0 and charge==1 else None
            if not left or sum(abs(v) for v in residual.values())>4*left:
                return None
            row, value = max(residual.items(), key=lambda pair:abs(pair[1]))
            for k in incidence[row,-1 if value>0 else 1]:
                updated = dict(residual)
                for p,d in columns[k].items():
                    updated[p] = updated.get(p,0)+d
                    if not updated[p]:
                        del updated[p]
                _,j,s = labels[k]
                result = visit(selected+(k,), updated, charge+s*(-1)**j)
                if result is not None:
                    return result
            return None
        answer = None
        # Every charged solution contains a positive tile; translating its
        # quotient residue to zero preserves all projected endpoint rows.
        for j in range(6):
            s = (-1)**j
            k = labels.index((0,j,s))
            answer = visit((k,),columns[k],1)
            if answer is not None:
                break
        entry = {'quotient':[lx,ly], 'states':states, 'found':answer is not None}
        if answer is not None:
            entry['orbit_support'] = [labels[k] for k in answer]
            support = []
            for r,j,s in entry['orbit_support']:
                for x in range(c):
                    for y in range(c):
                        if (lx*x+ly*y)%c==r:
                            support.append((x,y,j,s))
            endpoint = Counter(); gate_up = Counter(); gate_down = Counter()
            charge = 0
            for x,y,j,s in support:
                ux,uy = x-a*U[j][0],y-a*U[j][1]
                wx,wy = x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
                for axis,p,v in ((j,(x,y),s),(j,(ux,uy),-s),
                                  (j+s,(wx,wy),s),(j+s,(x,y),-s)):
                    endpoint[axis%3,p[0]%c,p[1]%c] += v
                eps = s*(-1)**j; charge += eps
                if s>0:
                    gate_up[(a*uy-b*ux)%c] += eps
                else:
                    gate_down[(a*ux-b*uy)%c] += eps
            assert len(support)==total*c and charge==c
            assert not any(endpoint.values())
            entry['full_torus_support'] = support
            entry['up_currents'] = [gate_up[r] for r in range(c)]
            entry['down_currents'] = [gate_down[r] for r in range(c)]
            entry['integer_endpoint_rows_checked'] = True
        results.append(entry)
        if answer is not None:
            break
    return {'tile':[a,b,c], 'orbit_count':total, 'population':total*c,
        'charge':c, 'seconds':time.monotonic()-start, 'quotients':results,
        'scope':'Full integer torus witness if found; negative results only concern the displayed first-return translation-orbit family. No packing or gate compatibility is imposed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('a',type=int); parser.add_argument('b',type=int)
    parser.add_argument('c',type=int); parser.add_argument('--orbits',type=int,default=3)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    output = run(args.a,args.b,args.c,args.orbits)
    args.out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'population':output['population'],
        'found':any(q['found'] for q in output['quotients']),
        'quotients_checked':len(output['quotients']), 'seconds':output['seconds']}))
