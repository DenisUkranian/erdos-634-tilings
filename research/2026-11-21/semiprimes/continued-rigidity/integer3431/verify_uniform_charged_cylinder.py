#!/usr/bin/env python3
"""Exact rigid cylinder countercontrol, without a board or gate congruences."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

U = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
HERE = Path(__file__).resolve().parent


def separated(A, B):
    for polygon in (A,B):
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            nx,ny = p[1]-q[1],q[0]-p[0]
            left = [nx*x+ny*y for x,y in A]
            right = [nx*x+ny*y for x,y in B]
            if max(left)<=min(right) or max(right)<=min(left):
                return True
    return False


def check(a,b,c):
    assert a>b>0 and a*a+a*b+b*b==c*c
    assert a<c
    step = 2*c+1
    columns = [(0,step*r,j,s) for r in range(c)
               for j,s in ((0,-1),(0,1),(4,1))]
    cylinder = Counter(); physical = Counter(); up = Counter(); down = Counter()
    polygons = []; positive = negative = 0
    for x,y,j,s in columns:
        u = x-a*U[j][0],y-a*U[j][1]
        w = x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
        polygons.append([(x,y),u,w])
        eps = s*(-1)**j
        positive += eps==1; negative += eps==-1
        if s>0:
            up[(a*u[1]-b*u[0])%c] += eps
        else:
            down[(a*u[0]-b*u[1])%c] += eps
        for axis,p,value in ((j,(x,y),s),(j,u,-s),
                              (j+s,w,s),(j+s,(x,y),-s)):
            axis %= 3
            physical[axis,*p] += value
            transverse = p[1] if axis==0 else p[0] if axis==1 else sum(p)
            longitudinal = p[0] if axis==0 else p[1]
            cylinder[axis,transverse,longitudinal%c] += value
    assert positive==2*c and negative==c
    assert not any(cylinder.values())
    assert [up[r] for r in range(c)]==[2]*c
    assert [down[r] for r in range(c)]==[-1]*c
    assert sum(v!=0 for v in physical.values())==2*c
    pairs = 0
    for i,A in enumerate(polygons):
        for B in polygons[:i]:
            assert separated(A,B)
            pairs += 1
    d = a-b
    incompatible = [(part,r,value) for part,table in (('up',up),('down',down))
                    for r,value in sorted(table.items()) if r and value%d]
    assert incompatible
    return {'tile':[a,b,c], 'population':len(columns), 'positive':positive,
        'negative':negative, 'charge':positive-negative, 'vertical_step':step,
        'all_actual_cylinder_rows_zero':True,
        'pairs_separated_exactly':pairs,
        'unreduced_physical_endpoint_nonzero_rows':2*c,
        'up_current_every_residue':2, 'down_current_every_residue':-1,
        'remote_gate_divisibility_failed':True,
        'remote_failures':len(incompatible),
        'scope':'A nonoverlapping partial packing in the unbounded plane; no target-board containment, complete tiling, or neighboring-gate compatibility.'}


def main():
    results = [check(*shape) for shape in ((5,3,7),(33,7,37),(35,13,43))]
    output = {'status':'PASS', 'checks':results,
        'conclusion':'Integrality, exact cylinder rows and pairwise interior nonoverlap alone permit charge c at population 3c. Actual gate congruences and board geometry remain necessary.'}
    (HERE/'UNIFORM_CHARGED_CYLINDER_REPLAY.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
