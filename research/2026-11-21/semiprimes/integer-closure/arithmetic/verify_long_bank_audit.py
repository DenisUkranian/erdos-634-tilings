#!/usr/bin/env python3
"""Independent regression audit of exact long-bank reconstruction and 2-SAT.

Checks the complete 143 tiling, rational isometries and all three-variable
binary-clause systems with zero or one forbidden literal. No target search
or claimed exclusion of 3431/5063 is performed.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir())
spec=importlib.util.spec_from_file_location('audited_long_bank',HERE.parent/'long-banks/long_bank_completion.py')
bank=importlib.util.module_from_spec(spec);spec.loader.exec_module(bank)
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def plus(p,q):return p[0]+q[0],p[1]+q[1]
def minus(p,q):return p[0]-q[0],p[1]-q[1]
def times(k,p):return k*p[0],k*p[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def length(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def multiply(p,q):
    x,y=p;u,v=q
    return x*u-y*v,x*v+y*u+y*v


def power(z,h):
    if h<0:z,h=(z[0]+z[1],-z[1]),-h
    result=(F(1),F(0))
    for _ in range(h):result=multiply(result,z)
    return result


def oriented(poly):
    poly=tuple(poly)
    return poly if cross(minus(poly[1],poly[0]),minus(poly[2],poly[0]))>0 else poly[::-1]


def decode(data):
    a,b,c=data['sides'];z=F(a,c),F(b,c);records=[]
    for q,h,j,s in data['tiles']:
        tip=F(q[0],c**q[2]),F(q[1],c**q[2])
        axis=multiply(power(z,h),U[j])
        other=multiply(power(z,h),U[(j+s)%6])
        poly=oriented((plus(tip,times(-a,axis)),tip,plus(tip,times(b,other))))
        assert sorted(length(minus(q,p)) for p,q in zip(poly,poly[1:]+poly[:1]))==[b*b,a*a,c*c]
        records.append((h,poly))
    return records


def full_current(polygons):
    result=Counter()
    for poly in polygons:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            dx,dy=minus(q,p)
            axis=(F(1),dy/dx) if dx else (F(0),F(1))
            result[p,axis]+=1;result[q,axis]-=1
    return result


def actual_long_edges(polygons,c):
    answer=Counter()
    for poly in polygons:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            if length(minus(q,p))==c*c:
                answer[min(p,q),max(p,q)]+=1 if p<q else -1
    return {key:value for key,value in answer.items() if value}


def brute_sat(n,forbidden,pairs):
    for bits in product((0,1),repeat=n):
        selected={2*i+bits[i] for i in range(n)}
        if selected.intersection(forbidden):continue
        if any(u in selected and v in selected for u,v in pairs):continue
        return selected
    return None


def check_solver():
    checked=0;satisfiable=0
    for n in (0,1,2,3):
        literals=list(range(2*n))
        possible=[(u,v) for u in literals for v in literals if u<v and u//2!=v//2]
        forbidden_sets=([set()] if n==0 else
            [{u for u in literals if mask>>u&1} for mask in range(1<<(2*n))] if n<=2 else
            [set()]+[{u} for u in literals])
        for mask in range(1<<len(possible)):
            pairs=[pair for i,pair in enumerate(possible) if mask>>i&1]
            for forbidden in forbidden_sets:
                expected=brute_sat(n,forbidden,pairs)
                actual=bank.solve_2sat(n,forbidden,pairs)
                assert actual['satisfiable']==(expected is not None)
                if actual['satisfiable']:
                    chosen=set(actual['chosen'])
                    assert all(sum(2*i+j in chosen for j in (0,1))==1 for i in range(n))
                    assert not chosen.intersection(forbidden)
                    assert all(not(u in chosen and v in chosen) for u,v in pairs)
                    satisfiable+=1
                checked+=1
    # A long implication chain checks the nonrecursive traversal and both
    # directions of a deliberately contradictory SCC.
    n=2000
    pairs=[(2*i,2*(i+1)+1) for i in range(n-1)]
    assert bank.solve_2sat(n,{1},pairs)['satisfiable']
    assert not bank.solve_2sat(n,{1,2*(n-1)},pairs)['satisfiable']
    return {'exhaustive_small_formulas':checked,'satisfiable_small_formulas':satisfiable,
        'long_chain_variables':n,'long_chain_cases':2}


def check_control():
    path=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    data=json.loads(path.read_text());assert data['sides']==[5,3,7] and data['N']==143
    records=decode(data);a,b,c=data['sides'];A,B=b*(2*a+b),a*(a+2*b)
    board=((F(0),F(0)),(F(A),F(0)),(F(0),F(B)))
    current=full_current([poly for h,poly in records]);current.subtract(full_current([board]))
    assert not any(current.values())
    assert sum(cross(minus(poly[1],poly[0]),minus(poly[2],poly[0])) for h,poly in records)==A*B
    odd=[poly for h,poly in records if h%2];even=[poly for h,poly in records if not h%2]
    assert (len(odd),len(even))==(105,38)
    transforms=[(0,(F(0),F(0))),(-3,(F(-13,11),F(7,13))),(4,(F(137,17),F(-221,19)))]
    cases=[]
    for height,shift in transforms:
        z=power((F(a,c),F(b,c)),height)
        def transformed(poly):return tuple(plus(multiply(z,p),shift) for p in poly)
        O=list(map(transformed,odd));E=list(map(transformed,even))
        expected=actual_long_edges(E,c)
        segments,residual=bank.reconstruct(O,a,b,c)
        assert not residual
        actual=Counter()
        actual_polygons={tuple(sorted(poly)) for poly in E}
        matching_choices=0
        for segment in segments:
            p,q,k=segment['p'],segment['q'],segment['coefficient']
            assert p<q and length(minus(q,p))==c*c
            actual[p,q]+=k
            choices=bank.triangle_choices(segment,a,b,c)
            assert any(tuple(sorted(poly)) in actual_polygons for poly in choices)
            matching_choices+=1
        assert dict(actual)==expected
        assert not bank.capacity_conflicts(segments)
        cases.append({'rotation_height':height,'rational_translation':[str(v) for v in shift],
            'mandatory_segments':len(segments),'matched_actual_even_tiles':matching_choices,
            'all_net_even_long_edges_recovered':True})
    completed=bank.complete_bank(odd,a,b,c,board)
    assert completed['status']=='compatible_mandatory_bank'
    # Geometry checks include touching, same-side interval overlap, opposite
    # banks, and multiplicity. Equality of edges must not count as overlap.
    base={'line':(1,0,F(0)),'p':(F(0),F(0)),'q':(F(c),F(0)),
          't':F(0),'coefficient':1}
    touching=dict(base,t=F(1),p=(F(c),F(0)),q=(F(2*c),F(0)))
    overlap=dict(base,t=F(1,2),p=(F(c,2),F(0)),q=(F(3*c,2),F(0)))
    opposite=dict(overlap,coefficient=-1)
    assert not bank.capacity_conflicts([base,touching])
    assert bank.capacity_conflicts([base,overlap])
    assert not bank.capacity_conflicts([base,opposite])
    assert bank.capacity_conflicts([dict(base,coefficient=2)])
    above=bank.triangle_choices(base,a,b,c)[0]
    below=bank.triangle_choices(dict(base,coefficient=-1),a,b,c)[0]
    assert bank.overlaps(above,above)
    assert not bank.overlaps(above,below)
    assert bank.contained(above,above)
    return {'full_positive_control_verified':True,'odd_tiles':len(odd),'even_tiles':len(even),
        'isometry_reconstruction_cases':cases,'complete_bank_report':completed,
        'additional_exact_geometry_cases':7}


def main():
    if not __debug__:raise RuntimeError('Run this exact audit without -O')
    report={'status':'PASS','solver_audit':check_solver(),'physical_control_audit':check_control(),
        'scope':'Independent exact positive-control and algorithm checks; no 3431/5063 target exclusion is asserted.'}
    (HERE/'LONG_BANK_AUDIT_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
