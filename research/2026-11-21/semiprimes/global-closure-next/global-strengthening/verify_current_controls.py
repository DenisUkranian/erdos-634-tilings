#!/usr/bin/env python3
"""Exact controls distinguishing physical currents, periodic rows and integers.

The controls use a nine-piece right-isosceles triangle, not either target.
They validate the logical distinctions of the general polygon theorem.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


def sub(x, y):
    return x[0]-y[0], x[1]-y[1]


def det(x, y):
    return x[0]*y[1]-x[1]*y[0]


def axis(v):
    return (F(1), F(v[1], v[0])) if v[0] else (F(0), F(1))


def current(polygons, periodic=False):
    out = Counter()
    for tri, weight in polygons:
        for p, q in zip(tri, tri[1:]+tri[:1]):
            a = axis(sub(q, p))
            pp = tuple(F(x) % 1 for x in p) if periodic else tuple(map(F, p))
            qq = tuple(F(x) % 1 for x in q) if periodic else tuple(map(F, q))
            out[pp,a] += weight
            out[qq,a] -= weight
    return {key:value for key,value in out.items() if value}


def overlaps(P, Q):
    for poly in (P,Q):
        for p,q in zip(poly,poly[1:]+poly[:1]):
            u,v = sub(q,p)
            normal = (-v,u)
            pp = [normal[0]*x+normal[1]*y for x,y in P]
            qq = [normal[0]*x+normal[1]*y for x,y in Q]
            if max(pp) <= min(qq) or max(qq) <= min(pp):
                return False
    return True


def interior(tri, point):
    return all(det(sub(q,p),sub(point,p)) > 0
               for p,q in zip(tri,tri[1:]+tri[:1]))


def build(flip):
    out = []
    for x,y in ((0,0),(1,0),(0,1)):
        p,q,r,s = (x,y),(x+1,y),(x+1,y+1),(x,y+1)
        out += [(p,q,s),(q,r,s)] if flip and (x,y)==(0,0) else [(p,q,r),(p,r,s)]
    out += [((x,2-x),(x+1,2-x),(x,3-x)) for x in range(3)]
    return out


def check_metrics(tiles):
    for tri in tiles:
        assert det(sub(tri[1],tri[0]),sub(tri[2],tri[0])) == 1
        lengths = sorted(sum(a*a for a in sub(q,p)) for p,q in zip(tri,tri[1:]+tri[:1]))
        assert lengths == [1,1,2]
        assert all(x>=0 and y>=0 and x+y<=3 for x,y in tri)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=Path(__file__).with_name('CURRENT_CONTROLS_REPLAY.json'))
    args = p.parse_args()
    if not __debug__:
        raise RuntimeError('Run without -O.')
    board = ((0,0),(3,0),(0,3))
    B = current([(board,1)])
    tilings = [build(False),build(True)]
    for tiles in tilings:
        assert len(tiles)==len({tuple(sorted(t)) for t in tiles})==9
        check_metrics(tiles)
        assert current([(tri,1) for tri in tiles]) == B
        assert not any(overlaps(P,Q) for i,P in enumerate(tiles) for Q in tiles[i+1:])
    # An exact full physical fractional current with overlapping selected tiles.
    fractional = [(tri,F(1,2)) for tiles in tilings for tri in tiles]
    assert current(fractional) == B
    probe = (F(1,4),F(1,8))
    contained_at_probe = [(tri,w) for tri,w in fractional if interior(tri,probe)]
    assert len(contained_at_probe)==2 and sum(w for _,w in contained_at_probe)==1
    assert overlaps(tilings[0][0],tilings[1][0])
    # Nine distinct, congruent, contained integer placements: periodic rows
    # and area pass, but an overlap and a hole remain physically.
    bad = tilings[0][:-1]+[tilings[1][0]]
    assert len(bad)==len({tuple(sorted(t)) for t in bad})==9
    check_metrics(bad)
    assert current([(t,1) for t in bad],True) == current([(board,1)],True) == {}
    physical_bad = current([(t,1) for t in bad]+[(board,-1)])
    assert physical_bad
    assert sum(interior(t,probe) for t in bad)==2
    hole_probe = (F(9,4),F(1,4))
    assert interior(board,hole_probe) and sum(interior(t,hole_probe) for t in bad)==0
    report = {
      'scope':'General polygon-current controls on a nine-piece right-isosceles triangle; no target decision.',
      'two_full_integer_tilings':{'counts':[9,9],'physical_currents':'PASS','containment_and_congruence':'PASS','pairwise_interior_disjointness':'PASS'},
      'fractional_average':{'physical_current':'PASS','weighted_cover_at_overlap_point':1,'distinct_selected_interiors_at_overlap_point':2,'positive_integrality_required_for_hard_body_conclusion':True},
      'integer_periodic_countercontrol':{'distinct_congruent_contained_tiles':9,'area_matches_board':True,'periodic_residual_rows':0,'physical_residual_rows':len(physical_bad),'multiplicity_at_overlap_point':2,'multiplicity_at_hole_point':0,'is_tiling':False},
      'conclusion':'Full physical current plus nonnegative integrality gives a tiling; periodic current alone does not, even for Boolean actual placements with the right area.'}
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
