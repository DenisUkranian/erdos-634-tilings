#!/usr/bin/env python3
"""Exact controls separating physical currents, integrality and periodic rows.

Standard library only. The small Cartesian examples are logical controls,
not configurations of the two unresolved target tiles. The 143 control is
an actual project tiling, independently rechecked before its integer native
middle-layer projection is reconstructed.
"""
from collections import Counter
from fractions import Fraction as Q
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OLD = ROOT / 'research/2026-11-20/semiprimes/continuation/global-endpoints'
U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def ccw(poly):
    assert det(*poly)
    return poly if det(*poly)>0 else tuple(reversed(poly))


def current(poly, period=None):
    out = Counter()
    poly = ccw(poly)
    for i, p in enumerate(poly):
        q = poly[(i+1)%3]
        dx, dy = q[0]-p[0], q[1]-p[1]
        direction = (Q(1), Q(dy, dx)) if dx else (Q(0), Q(1))
        if period is not None:
            p = tuple(x % period for x in p)
            q = tuple(x % period for x in q)
        out[p, direction] += 1
        out[q, direction] -= 1
    return out


def strict_inside(poly, p):
    poly = ccw(poly)
    return all(det(poly[i], poly[(i+1)%3], p)>0 for i in range(3))


def residual(board, polygons, weights, period=None):
    out = Counter({r: -v for r, v in current(board, period).items()})
    for poly, weight in zip(polygons, weights):
        for row, value in current(poly, period).items():
            out[row] += weight*value
    return {r:v for r,v in out.items() if v}


def small_controls():
    board = ((0,0), (2,0), (0,2))
    square = [((0,0),(1,0),(1,1)), ((0,0),(1,1),(0,1)),
              ((0,0),(1,0),(0,1)), ((1,0),(1,1),(0,1))]
    outside = [((1,0),(2,0),(1,1)), ((0,1),(1,1),(0,2))]
    all_tiles = square + outside
    for triangle in all_tiles:
        assert abs(det(*triangle)) == 1
        assert all(x>=0 and y>=0 and x+y<=2 for x,y in triangle)
        distances = sorted((triangle[i][0]-triangle[(i+1)%3][0])**2 +
                           (triangle[i][1]-triangle[(i+1)%3][1])**2
                           for i in range(3))
        assert distances == [1,1,2]
    tiling_a, tiling_b = square[:2]+outside, square[2:]+outside
    assert not residual(board, tiling_a, [1]*4)
    assert not residual(board, tiling_b, [1]*4)
    weights = [Q(1,2)]*4+[Q(1)]*2
    assert sum(weights) == 4
    assert not residual(board, all_tiles, weights)
    overlap = (Q(1,4), Q(1,8))
    hole = (Q(5,4), Q(1,4))
    assert sum(strict_inside(p, overlap) for p in square) == 2
    assert sum(w*strict_inside(p, overlap) for p,w in zip(all_tiles,weights)) == 1
    assert sum(strict_inside(p, hole) for p in square) == 0
    # Four distinct contained rigid tiles, Boolean coefficients and the right
    # total area, satisfy every period-one row but overlap and leave a hole.
    assert len(set(tuple(sorted(t)) for t in square)) == 4
    assert not residual(board, square, [1]*4, period=1)
    physical_residual = residual(board, square, [1]*4)
    assert physical_residual
    return {'exact_positive_small_tilings':2,
            'fractional_full_current_weights':[str(x) for x in weights],
            'fractional_point_has_two_overlapping_placements':True,
            'integer_periodic_example_contained_distinct_tiles':4,
            'integer_periodic_example_correct_area':True,
            'integer_periodic_example_residual_rows':0,
            'integer_periodic_example_physical_residual_rows':len(physical_residual),
            'integer_periodic_example_overlap_multiplicity':2,
            'integer_periodic_example_hole_multiplicity':0,
            'scope':'Small Cartesian controls only; neither is a 3431 or 5063 placement.'}


def mul(p, q):
    x,y = p; u,v = q
    return x*u-y*v, x*v+y*u+y*v


def positive_143_projection():
    path = OLD/'tiling_143.json'
    data = json.loads(path.read_text())
    spec = importlib.util.spec_from_file_location('independent_positive_current',
                                                OLD/'verify_endpoint_tiling.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checked = checker.check(data)
    assert checked['verified_positive_tiling']
    a,b,c = data['sides']; B = a*(a+2*b)
    z = (Q(a,c), Q(b,c))
    # Standard board -> path board: F(w)=z^2(B-rho*conjugate(w)).
    # For height one, the new short-lattice anchor is F(q)/z.
    endpoints, gates, signs, placements = Counter(), Counter(), Counter(), Counter()
    for (x,y,e),h,j,s in data['tiles']:
        if h != 1:
            continue
        q = Q(x,c**e), Q(y,c**e)
        conjugate = q[0]+q[1], -q[1]
        term = mul(mul((0,1), z), conjugate)
        anchor = B*z[0]-term[0], B*z[1]-term[1]
        assert all(v.denominator == 1 for v in anchor)
        q = int(anchor[0]), int(anchor[1])
        j,s = (4-j)%6, -s
        eps = s*(-1 if j%2 else 1)
        u = q[0]-a*U[j][0], q[1]-a*U[j][1]
        w = q[0]+b*U[(j+s)%6][0], q[1]+b*U[(j+s)%6][1]
        for axis,p,value in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
            endpoints[axis%3,p[0]%c,p[1]%c] += value
        gate = ((a*u[1]-b*u[0]) if s>0 else (a*u[0]-b*u[1]))%c
        gates[s,gate] += eps
        signs[eps] += 1
        placements[q[0]%c,q[1]%c,j,s,gate] += 1
    assert not any(endpoints.values())
    assert signs == Counter({1:56,-1:49})
    charge_units = []
    for hand in (1,-1):
        for gate in range(c):
            offset = (2*c if hand>0 else -c) if gate==0 else 0
            value = gates[hand,gate]-offset
            assert value%(a-b) == 0
            charge_units.append(value//(a-b))
    assert sum(charge_units) == 0
    return {'full_tiling_verified':True,'N':143,'odd_population':105,
            'odd_blocks':15,'positive':56,'negative':49,
            'periodic_endpoint_residual_rows':0,
            'integer_residue_support':len(placements),
            'largest_integer_residue_multiplicity':max(placements.values()),
            'gate_charge_units':charge_units,
            'scope':'Projection of an independently verified complete 143 tiling; not a target tiling.'}


def verify():
    return {'verified':True,'small_controls':small_controls(),
            'positive_143_integer_projection':positive_143_projection(),
            'theorem_scope':'Finite nonnegative integer actual polygons with full physical current closure tile exactly; incomplete or periodic rows do not suffice.',
            'target_status':{'3431':'OPEN','5063':'OPEN'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=HERE/'RIGID_BODY_REPLAY.json')
    args = parser.parse_args()
    report = verify()
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
