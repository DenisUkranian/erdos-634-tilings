#!/usr/bin/env python3
"""Discovery search for the four-macro ansatz v=u+1, scale v+t.

The remaining positions use right coordinate triangles of legs u,v;
the physical coordinate basis is oblique. Negative results apply only to
this ansatz and this lattice. A positive result exports a full unit tiling.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
from math import gcd, lcm
from pathlib import Path
import argparse
import json
import os
import sys
import numpy as np
from scipy.sparse import coo_matrix


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def area2(poly):
    return sum(cross(a, b) for a, b in zip(poly, poly[1:]+poly[:1]))


def ccw(poly):
    return list(poly) if area2(poly) > 0 else list(reversed(poly))


def shape(u, t):
    assert isinstance(u, int) and u >= 2
    assert 1 <= t <= u-1
    v, m = u+1, u+1+t
    a, b, c = u*v, 2*u+1, v*v
    O = (F(u*m*v**3, b), F(-u*u*m*v*v, b))
    X = (F(0), F(0))
    A = (F(-u*v*m), F(u*u*m))
    C = (F(-u*v*m), F(v*v*m))
    V = (F(-u*u*m), F(u*v*m))
    U = (F(-u*u*m+t*v*v), F(u*v*v))
    Rr = (F(-u*u*v+b*(t-1)), F(u*v*v))
    S = (F(u*b-u*u*t), F(u*v*t))
    Q = (F(u*b), F(0))
    P = (Q[0]+F(u*t*v**3, b), Q[1]-F(u*u*t*v*v, b))
    R = (S[0]+F(t*u*v*v, b), S[1]-F(t*u*u*v, b))
    T = (U[0]+F((u-t)*v**3, b), U[1]-F((u-t)*u*v*v, b))
    macros = [([O, X, Q, P], u*m, u*t),
              ([P, Q, S, R], v*t, t),
              ([R, Rr, U, T], b-t, u-t),
              ([T, V, C], m, 0)]
    remainder = ccw([X, A, C, V, U, Rr, S, Q])
    target = ccw([O, A, C])
    return target, [(ccw(p), r, s) for p, r, s in macros], remainder


def contained_batch(points, polygon):
    mask = np.ones(len(points), dtype=bool)
    for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
        e = b-a
        mask &= e[0]*(points[:, 1]-a[1])-e[1]*(points[:, 0]-a[0]) >= 0
    return mask


def separated_batch(anchors, template, polygon):
    mask = np.zeros(len(anchors), dtype=bool)
    for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
        e = b-a
        tt = np.ones(len(anchors), dtype=bool)
        for p in template:
            pp = anchors+p-a
            tt &= e[0]*pp[:, 1]-e[1]*pp[:, 0] <= 0
        mask |= tt
    for a, b in zip(template, np.roll(template, -1, axis=0)):
        e = b-a
        tt = np.ones(len(anchors), dtype=bool)
        for p in polygon:
            pp = p-anchors-a
            tt &= e[0]*pp[:, 1]-e[1]*pp[:, 0] <= 0
        mask |= tt
    return mask


def unit_grid(polygon, r, s):
    # Recover geometric bottom endpoints and apex from the un-reordered
    # macro specification: in ccw form we identify the two parallel edges.
    if len(polygon) == 3:
        origin, left, right = polygon
        e = tuple((left[k]-origin[k])/r for k in range(2))
        f = tuple((right[k]-origin[k])/r for k in range(2))
    else:
        candidates = []
        for i in range(4):
            left, right = polygon[i], polygon[(i+1) % 4]
            tr, tl = polygon[(i+2) % 4], polygon[(i+3) % 4]
            if all((right[k]-left[k])*s == (tr[k]-tl[k])*r for k in range(2)):
                candidates.append((left, right, tl))
        assert len(candidates) == 1
        left, right, tl = candidates[0]
        origin = tuple((r*tl[k]-s*left[k])/(r-s) for k in range(2))
        e = tuple((left[k]-origin[k])/r for k in range(2))
        f = tuple((right[k]-origin[k])/r for k in range(2))

    def p(i, j):
        return tuple(origin[k]+i*e[k]+j*f[k] for k in range(2))

    tiles = []
    for i in range(r):
        for j in range(r-i):
            if i+j >= s:
                tiles.append(ccw([p(i, j), p(i+1, j), p(i, j+1)]))
            if i+j < r-1 and i+j >= s-1:
                tiles.append(ccw([p(i+1, j), p(i+1, j+1), p(i, j+1)]))
    assert len(tiles) == r*r-s*s
    return tiles


def export(u, t, target, macros, selected, path):
    v, m = u+1, u+1+t
    a, b, c, D = u*v, 2*u+1, v*v, 4*v*v-u*u
    # Coordinates above multiply v*E and v*F, where E=z^-2, F=z.
    E = (F(u*u-2*v*v, 2*v*v), F(u, 2*v*v))
    FF = (F(-u, 2*v), F(1, 2*v))
    O = (F(u*m*v**3, b), F(-u*u*m*v*v, b))

    def physical(p):
        x, y = p[0]-O[0], p[1]-O[1]
        return (v*(x*E[0]+y*FF[0]), v*(x*E[1]+y*FF[1]))

    tiles = list(selected)
    for polygon, r, s in macros:
        tiles.extend(unit_grid(polygon, r, s))
    expected = (2*v*v-u*u)*m*m
    assert len(tiles) == expected
    tiles = [ccw([physical(p) for p in t]) for t in tiles]
    goal = ccw([physical(p) for p in target])
    den = lcm(*(x.denominator for t in tiles+[goal] for p in t for x in p))
    data = {'metric': f'x^2+{D}y^2', 'metric_y_coefficient': D,
            'denominator': den, 'tile': [a, b, c],
            'u': u, 'v': v, 'scale': m,
            'target': [[int(x*den), int(y*den)] for x, y in goal],
            'triangles': [[[int(x*den), int(y*den)] for x, y in t] for t in tiles]}
    path.write_text(json.dumps(data, indent=2)+'\n')


def run(u, t, seconds, prefix):
    offset = t
    target, macros, remainder = shape(u, offset)
    b, v = 2*u+1, u+1
    scaled_target = np.array([[int(b*x) for x in p] for p in target], dtype=np.int64)
    scaled_macros = [np.array([[int(b*x) for x in p] for p in poly], dtype=np.int64)
                     for poly, _, _ in macros]
    xmin, xmax = int(min(p[0] for p in remainder)), int(max(p[0] for p in remainder))
    ymin, ymax = int(min(p[1] for p in remainder)), int(max(p[1] for p in remainder))
    xx, yy = np.meshgrid(np.arange(xmin, xmax+1), np.arange(ymin, ymax+1))
    anchors = np.column_stack((xx.ravel(), yy.ravel()))
    placements = []
    for w, h in [(u, v), (v, u)]:
        for sign in [-1, 1]:
            t = np.array([(0, 0), (sign*w, 0), (0, sign*h)], dtype=np.int64)
            keep = np.ones(len(anchors), dtype=bool)
            for p in t:
                keep &= contained_batch(b*(anchors+p), scaled_target)
            for poly in scaled_macros:
                keep &= separated_batch(b*anchors, b*t, poly)
            placements.extend((a+t).tolist() for a in anchors[keep])
    print(json.dumps({'u': u, 'positions': len(placements)}), flush=True)
    row_ids = {}

    def edge_rows(a, b):
        dx, dy = int(b[0]-a[0]), int(b[1]-a[1])
        dd = gcd(dx, dy)
        dx, dy = dx//dd, dy//dd
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        keys = [(dx, dy, int(p[0]), int(p[1])) for p in [a, b]]
        return [row_ids.setdefault(k, len(row_ids)) for k in keys]

    colrows = []
    for tri in placements:
        colrows.append(sum((edge_rows(a, b) for a, b in zip(tri, tri[1:]+tri[:1])), []))
    rr = []
    for a, b in zip(remainder, remainder[1:]+remainder[:1]):
        rr.extend(edge_rows(a, b))
    colrows = np.array(colrows, dtype=np.int64)
    signs = np.array([1, -1, 1, -1, 1, -1], dtype=np.int8)
    J, K = len(placements), len(row_ids)
    rhs = np.zeros(K, dtype=np.int32)
    np.add.at(rhs, rr, np.tile([1, -1], len(remainder)))
    matrix = coo_matrix((np.tile(signs, J), (colrows.ravel(), np.repeat(np.arange(J), 6))),
                        shape=(K, J)).tocsr()
    if os.environ.get('ERDOS_ORTOOLS_PATH'):
        sys.path.insert(0, os.environ['ERDOS_ORTOOLS_PATH'])
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    xx = [model.new_bool_var('') for _ in range(J)]
    for k in range(K):
        start, end = matrix.indptr[k:k+2]
        model.add(cp_model.LinearExpr.weighted_sum([xx[int(c)] for c in matrix.indices[start:end]],
                                                   [int(x) for x in matrix.data[start:end]]) == int(rhs[k]))
    expected = int(abs(area2(remainder))/(u*v))
    model.add(sum(xx) == expected)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.linearization_level = 0
    answer = solver.solve(model)
    report = {'u': u, 'v': v, 'scale': u+1+offset, 't': offset, 'positions': J, 'rows': K,
              'scope': 'Four fixed macros plus two-orientation integer-lattice residual only',
              'remainder_count': expected, 'solver': solver.status_name(answer),
              'seconds': solver.wall_time}
    if answer in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [tri for x, tri in zip(xx, placements) if solver.value(x)]
        prefix.with_suffix('.residual.json').write_text(json.dumps({'u': u, 'v': v, 't': offset,
                'triangles': chosen, 'target': [[int(x), int(y)] for x, y in remainder]}, indent=2)+'\n')
        export(u, offset, target, macros, chosen, prefix.with_suffix('.certificate.json'))
        report['status'] = 'EXPORTED_REQUIRES_INDEPENDENT_GEOMETRY'
    else:
        report['status'] = 'NO_GENERAL_CONCLUSION'
    prefix.with_suffix('.report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O.')
    ap = argparse.ArgumentParser()
    ap.add_argument('--u', type=int, required=True)
    ap.add_argument('--t', type=int, required=True)
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--prefix', type=Path, required=True)
    args = ap.parse_args()
    run(args.u, args.t, args.seconds, args.prefix)
