#!/usr/bin/env python3
"""Independent Fraction checks of supported polygon-budget witnesses."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
sys.path.insert(0,str(PACKAGE/'owned'))
from legacy import core, ROOT
from area_cycles import selected_area_cycles, selected_skeleton_faces, greedy_nonoverlap
from verify_long_cycles import (
    U, add, sub, scale, det, mul, power, point, reconstruct, disjoint, triangle_fixture)


def independent_simple(vertices):
    assert len(vertices) >= 3 and len(set(vertices)) == len(vertices)
    n = len(vertices)
    for i in range(n):
        a,b,c = vertices[i],vertices[(i+1)%n],vertices[(i+2)%n]
        if det(sub(b,a),sub(c,b)) == 0:
            assert sum(x*y for x,y in zip(sub(b,a),sub(c,b))) > 0
        for j in range(i+1,n):
            if j == i+1 or (i == 0 and j == n-1):
                continue
            c,d = vertices[j],vertices[(j+1)%n]
            u,v,w = sub(b,a),sub(d,c),sub(c,a)
            divisor = det(u,v)
            if divisor:
                first,second = det(w,v)/divisor,det(w,u)/divisor
                assert not (0 <= first <= 1 and 0 <= second <= 1)
            elif det(w,u) == 0:
                axis = 0 if u[0] else 1
                assert (max(a[axis],b[axis]) < min(c[axis],d[axis])
                        or max(c[axis],d[axis]) < min(a[axis],b[axis]))


def on_side(p, a, b):
    assert det(sub(b,a),sub(p,a)) == 0
    assert all(min(a[k],b[k]) <= p[k] <= max(a[k],b[k]) for k in (0,1))


def check_witness(g, tiles, chosen, witness):
    vertices = [point(g,p) for p in witness['vertices']]
    assert vertices[-1] == vertices[0]
    vertices.pop()
    independent_simple(vertices)
    area2 = sum(det(a,b) for a,b in zip(vertices,vertices[1:]+vertices[:1]))
    assert area2 > 0
    area = area2/(g.a*g.b)
    assert F(witness['twice_axial_area']) == area2
    assert F(witness['tile_area_ratio']) == area
    assert len(witness['edges']) == len(vertices)
    selected = set(chosen)
    representative_set = set()
    W0 = W1 = F(0)
    subdivisions = 0
    for i,edge in enumerate(witness['edges']):
        start,end = vertices[i],vertices[(i+1)%len(vertices)]
        assert point(g,edge['start']) == start and point(g,edge['end']) == end
        owner = edge['representative']
        assert owner in selected and owner in edge['selected_owners']
        representative_set.add(owner)
        triangle,_ = reconstruct(g,tiles[owner])
        first,last = triangle[edge['side']],triangle[(edge['side']+1)%3]
        on_side(start,first,last)
        on_side(end,first,last)
        subdivisions += start not in (first,last)
        for other in edge['selected_owners']:
            assert other in selected
            polygon,_ = reconstruct(g,tiles[other])
            assert any(det(sub(q,p),sub(start,p)) == 0
                       and det(sub(q,p),sub(end,p)) == 0
                       and all(min(p[k],q[k]) <= r[k] <= max(p[k],q[k])
                               for r in (start,end) for k in (0,1))
                       for p,q in zip(polygon,polygon[1:]+polygon[:1]))
        h,j = edge['direction']
        length = F(edge['length'])
        assert length > 0
        unit = mul(power((F(g.a,g.c),F(g.b,g.c)),h),U[j])
        assert sub(end,start) == scale(length,unit)
        W0 += length*(-1 if j%2 else 1)
        W1 += length*(-1 if (h+j)%2 else 1)
    assert sorted(representative_set) == witness['indices']
    charge_sum = W0/(g.a-g.b-g.c)
    charge_difference = W1/(g.a-g.b+g.c)
    even,odd = (charge_sum+charge_difference)/2,(charge_sum-charge_difference)/2
    assert F(witness['budget']['W0']) == W0 and F(witness['budget']['W1']) == W1
    assert F(witness['budget']['even_charge']) == even
    assert F(witness['budget']['odd_charge']) == odd
    failures = []
    for value,name in ((area,'nonintegral_area'),(even,'nonintegral_even_charge'),
                       (odd,'nonintegral_odd_charge')):
        if value.denominator != 1:
            failures.append(name)
    if all(x.denominator == 1 for x in (area,even,odd)):
        if abs(even)+abs(odd) > area:
            failures.append('insufficient_area_for_signed_population')
        if (area-even-odd)%2:
            failures.append('incompatible_population_parity')
    assert failures == witness['budget']['violations']
    return subdivisions


def check_physical(g,tiles,chosen):
    polygons = [reconstruct(g,tiles[i])[0] for i in chosen]
    assert all(disjoint(first,second) for first,second in combinations(polygons,2))
    assert greedy_nonoverlap(g,tiles,chosen) == sorted(chosen)


def main():
    negative = []
    for sides in ((33,7,37),(35,13,43)):
        g = core.Geometry(*sides)
        for height in (-5,-1,0,1,7):
            tiles,_ = triangle_fixture(g,height)
            check_physical(g,tiles,range(3))
            cuts = selected_area_cycles(g,tiles,range(3))
            assert len(cuts) == 1
            check_witness(g,tiles,range(3),cuts[0])
            assert F(cuts[0]['tile_area_ratio']) == F(g.c*g.c,g.a*g.b)
            assert 'nonintegral_area' in cuts[0]['budget']['violations']
            assert not selected_area_cycles(g,tiles,range(2))
            # A selected overlapping distractor is discarded, and cannot
            # enter the owner no-good of the retained physical cycle.
            q,h,j,s = tiles[0]
            distractor = g.add(q,g.unit(h,j)),h,j,s
            with_overlap = tiles+[distractor]
            assert greedy_nonoverlap(g,with_overlap,range(4)) == [0,1,2]
            again = selected_area_cycles(g,with_overlap,range(4))
            assert again[0]['indices'] == cuts[0]['indices']
            negative.append(dict(N=g.N,height=height,tiles=tiles,witness=cuts[0],
                                 legal_nonoverlapping_partial_packing=True,
                                 two_supports_not_rejected=True,
                                 overlapping_distractor_not_used=True))

    mixed = []
    directory = ROOT/'research/2026-11-20/semiprimes/continuation/common-obstruction/boundary'
    for N in (143,3431,5063):
        data = json.loads((directory/f'mixed_cycle_{N}.json').read_text())
        g = core.Geometry(*data['tile'])
        tiles = [(tuple(t['q']),t['h'],t['j'],t['s']) for t in data['placements']]
        chosen = sorted({edge['tile'] for edge in data['cycle']})
        check_physical(g,tiles,chosen)
        faces = list(selected_skeleton_faces(g,tiles,chosen))
        for face in faces:
            check_witness(g,tiles,chosen,face)
            assert not face['budget']['violations']
        holes = [face for face in faces if F(face['tile_area_ratio']) > 1]
        assert len(holes) == 1 and F(holes[0]['tile_area_ratio']) == 2*g.c-2
        assert not selected_area_cycles(g,tiles,chosen)
        mixed.append(dict(N=N,supporting_tiles=len(chosen),simple_faces=len(faces),
                          exposed_hole_area=holes[0]['tile_area_ratio'],
                          hole_budget=holes[0]['budget'],rejected=False))

    source = ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    data = json.loads(source.read_text())
    g = core.Geometry(*data['sides'])
    tiles = [(tuple(t[0]),*t[1:]) for t in data['tiles']]
    check_physical(g,tiles,range(143))
    faces = list(selected_skeleton_faces(g,tiles,range(143)))
    assert len(faces) == 143
    splits = 0
    for face in faces:
        splits += check_witness(g,tiles,range(143),face)
        assert F(face['tile_area_ratio']) == 1 and not face['budget']['violations']
    assert splits > 0 and not selected_area_cycles(g,tiles,range(143))
    report = dict(status='PASS',fractional_hole_controls=negative,
                  mixed_height_integer_hole_controls=mixed,
                  control143=dict(tiles=143,simple_faces=143,all_face_areas=1,
                                  strict_side_subdivisions_checked=splits,
                                  exact_metric_containment_nonoverlap=True,rejected=False),
                  scope='Exact local forbidden supports and compatible controls. No target or corner root is excluded.')
    (HERE/'AREA_CYCLE_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v if k != 'fractional_hole_controls' else len(v)
                      for k,v in report.items()},indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact assertions are required.')
    main()
