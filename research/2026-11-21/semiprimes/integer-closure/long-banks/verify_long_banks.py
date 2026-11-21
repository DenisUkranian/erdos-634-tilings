#!/usr/bin/env python3
"""Exact positive and negative controls of the mandatory long-bank theorem."""
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

import long_bank_completion as bank

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SEMIPRIMES=HERE.parents[1]
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def normalized_polygons(a,b,labels):
    result=[]
    for x,y,j,s in labels:
        q=(F(x),F(y));u=(F(x-a*U[j][0]),F(y-a*U[j][1]))
        w=(F(x+b*U[(j+s)%6][0]),F(y+b*U[(j+s)%6][1]))
        result.append(bank.ccw((q,u,w)))
    return result


def positive_control():
    source=SEMIPRIMES/'continued-rigidity/physical/CONTROL_143.json'
    spec=importlib.util.spec_from_file_location('independent_positive_geometry',
        ROOT/'research/2026-11-20/semiprimes/continuation/global-endpoints/verify_endpoint_tiling.py')
    geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
    data=json.loads(source.read_text());verified=geometry.check(data)
    assert verified['verified_positive_tiling']
    a,b,c=data['sides'];z=(F(a,c),F(b,c));odd=[];even=[]
    for (x,y,e),h,j,s in data['tiles']:
        q=(F(x,c**e),F(y,c**e))
        u=geometry.mul(geometry.power(z,h),U[j])
        w=geometry.mul(geometry.power(z,h),U[(j+s)%6])
        poly=bank.ccw((bank.add(q,bank.scale(-a,u)),q,bank.add(q,bank.scale(b,w))))
        if h%2:odd.append(poly)
        else:even.append((poly,s*(-1 if j%2 else 1)))
    board=((0,0),(b*(2*a+b),0),(0,a*(a+2*b)))
    result=bank.complete_bank(odd,a,b,c,board)
    assert result['status']=='compatible_mandatory_bank'
    segments,residual=bank.reconstruct(odd,a,b,c);assert not residual
    expected={(s['line'],s['t']):s['coefficient'] for s in segments}
    actual=defaultdict(list)
    for poly,sign in even:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            if bank.norm(bank.sub(q,p))!=c*c:continue
            line,direction,origin,t=bank.line_data(p,q,c)
            coordinate=0 if direction[0] else 1
            end=q[coordinate]/direction[coordinate]
            assert abs(end-t)==1
            actual[line,min(t,end)].append((1 if end>t else -1,sign,poly))
    pairs=0;mandatory_charge=0
    for key,entries in actual.items():
        assert sum(x[0] for x in entries)==expected.get(key,0)
        if key in expected:
            assert len(entries)==1
            mandatory_charge+=entries[0][1]
        else:
            assert len(entries)==2 and entries[0][0]==-entries[1][0]
            assert entries[0][1]==-entries[1][1]
            pairs+=1
    assert set(expected)<=set(actual)
    for i,segment in enumerate(segments):
        candidates=bank.triangle_choices(segment,a,b,c)
        actual_poly=actual[segment['line'],segment['t']][0][2]
        choice=next(k for k,p in enumerate(candidates) if sorted(p)==sorted(actual_poly))
        assert 2*i+choice in result['choice_indices']
    assert len(odd)==105 and len(even)==38 and len(segments)==2 and pairs==18
    assert mandatory_charge==-(a-b)
    assert data['N']==len(odd)+len(segments)+2*pairs
    return dict(**result,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                full_tiling_independently_verified=True,even_tiles=len(even),
                neutral_even_pairs=pairs,mandatory_even_charge=mandatory_charge,
                full_population_identity='143 = 105 + 2 + 2*18')


def compact_obstruction():
    source=HERE.parent/'charged-cells/COMPACT_C7_LIFTS.json'
    labels=json.loads(source.read_text())['best']['support']
    polygons=normalized_polygons(5,3,labels)
    result=bank.complete_bank(polygons,5,3,7)
    assert result['status']=='mandatory_bank_2sat_obstruction'
    assert result['mandatory_long_segments']==32 and result['line_capacity_conflicts']==0
    segments,residual=bank.reconstruct(polygons,5,3,7);assert not residual
    # This particular certificate has a stronger, direct geometric contradiction:
    # both candidate triangles on one compulsory whole edge meet the odd packing.
    for i,segment in enumerate(segments):
        choices=bank.triangle_choices(segment,5,3,7)
        blockers=[[j for j,p in enumerate(polygons) if bank.overlaps(candidate,p)]
                  for candidate in choices]
        if all(blockers):
            result['direct_two_choice_obstruction']={
                'segment_index':i,'segment':[segment['p'],segment['q']],
                'oriented_coefficient':segment['coefficient'],
                'candidate_triangles':choices,'blocking_odd_indices':blockers,
                'blocking_odd_triangles':[[polygons[j] for j in indices] for indices in blockers]}
            break
    assert 'direct_two_choice_obstruction' in result
    result['scope']='This exact complete proposed cell cannot occur; not all 13-tile packings are excluded.'
    return result


def main():
    if not __debug__:raise RuntimeError('Run with assertions enabled, without -O.')
    checks=[]
    source=HERE.parent/'charged-cells/CHARGED_COUNTERCONTROLS.json'
    data=json.loads(source.read_text())['unit_charge_small']
    result=bank.complete_bank(normalized_polygons(5,3,data['support']),5,3,7)
    assert result['status']=='line_capacity_obstruction'
    assert result['mandatory_long_segments']==522 and result['line_capacity_conflicts']==63
    checks.append(dict(name='separated_charged_13',tile=[5,3,7],**result))
    checks.append(dict(name='compact_charged_13',tile=[5,3,7],**compact_obstruction()))
    for a,b,c in ((5,3,7),(33,7,37),(35,13,43)):
        L=2*c;anchors=((-L,L),(0,L),(L,0),(L,-L),(0,-L),(-L,0))
        turns=((0,1),(0,-1),(4,1),(4,-1),(2,1),(2,-1))
        labels=[(*q,*turn) for q,turn in zip(anchors,turns)]
        result=bank.complete_bank(normalized_polygons(a,b,labels),a,b,c)
        assert result['status']=='mandatory_bank_2sat_obstruction'
        assert result['mandatory_long_segments']==24 and result['line_capacity_conflicts']==0
        assert result['forbidden_choices']==0
        checks.append(dict(name='separated_balanced_hexagon',tile=[a,b,c],**result))
        for k in (0,1,2):
            labels=[(0,0,j,s) for j,s in ((0,1),(2,-1),(2,1))]
            labels += [(-(a+b)-k*c,0,j,s) for j,s in ((3,1),(5,-1),(5,1))]
            result=bank.complete_bank(normalized_polygons(a,b,labels),a,b,c)
            assert result['status']=='compatible_mandatory_bank'
            assert result['mandatory_long_segments']==2*k
            checks.append(dict(name='compatible_two_fan_patch',tile=[a,b,c],gap_units=k,**result))
        labels=[(0,(2*c+1)*r,j,s) for r in range(c) for j,s in ((0,-1),(0,1),(4,1))]
        result=bank.complete_bank(normalized_polygons(a,b,labels),a,b,c)
        assert result['status']=='line_capacity_obstruction'
        checks.append(dict(name='uniform_charged_fan',tile=[a,b,c],**result))
    source=SEMIPRIMES/'continued-rigidity/global/BALANCED_16_NONOVERLAP.json'
    data=json.loads(source.read_text())['strict_board_containment_control']
    polygons=[bank.ccw([(F(x,43),F(y,43)) for x,y in row])
              for row in data['physical_vertex_numerators']]
    result=bank.complete_bank(polygons,35,13,43,data['standard_board_vertices'])
    assert result['status']=='line_capacity_obstruction'
    assert result['mandatory_long_segments']==86 and result['line_capacity_conflicts']==34
    checks.append(dict(name='contained_balanced_16',tile=[35,13,43],**result))
    output=dict(status='PASS',positive_control=positive_control(),exact_configurations=checks,
                full_3431_excluded=False,full_5063_excluded=False,
                scope='Exact tests of the stated complete proposed cells and one full positive tiling. No enumeration of every target odd packing or tiling is asserted.')
    (HERE/'LONG_BANK_REPLAY.json').write_text(json.dumps(output,indent=2,default=str)+'\n')
    print(json.dumps({'status':'PASS','exact_configurations':len(checks),
                      'positive_control':output['positive_control'],
                      'full_3431_excluded':False,'full_5063_excluded':False},indent=2))


if __name__=='__main__':main()
