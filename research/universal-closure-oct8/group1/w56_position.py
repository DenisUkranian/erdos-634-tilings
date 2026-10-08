#!/usr/bin/env python3
"""Complete positions in a specified edge-height band for W_(u,v)=(2,3).

Metric x*x+2*y*y, z=(-1+2 sqrt(-2))/3. A bounded-band negative is not
an unrestricted W56 decision. A positive result exports exact coordinates.
"""
from collections import deque
from math import gcd
from pathlib import Path
import argparse
import json
import os
import sys
import time
import numpy as np
from scipy.sparse import coo_matrix


def mul(p, q):
    x, y = p
    u, v = q
    return (x*u-2*y*v, x*v+y*u)


def power(p, n):
    assert n >= 0
    out = (1, 0)
    for _ in range(n):
        out = mul(out, p)
    return out


def norm(p):
    return p[0]*p[0]+2*p[1]*p[1]


def direction(v):
    d = gcd(abs(int(v[0])), abs(int(v[1])))
    x, y = int(v[0])//d, int(v[1])//d
    return (-x, -y) if x < 0 or (x == 0 and y < 0) else (x, y)


def run(L, U, scale, seconds, prefix):
    assert L <= -3 and U >= 1
    started = time.monotonic()
    eta, bar = (1, 1), (1, -1)
    G = mul(power(eta, -L), power(bar, U))
    nG = norm(G)
    target_original = [(0, 0), (28*scale, 0), (23*scale, 10*scale)]
    target = np.array([mul(G, p) for p in target_original], dtype=np.int64)
    unit = {h: mul(power(eta, h-L), power(bar, U-h)) for h in range(L, U+1)}
    templates = []
    labels = []
    for kind, js, a, b in [('A', range(L, U-2), 6, 5),
                           ('B', range(L+2, U), 5, 6)]:
        for j in js:
            for sign in (-1, 1):
                tri = np.array([(0, 0), tuple(sign*a*x for x in unit[j]),
                                tuple(sign*b*x for x in unit[j+1])], dtype=np.int64)
                vectors = np.roll(tri, -1, axis=0)-tri
                assert sorted(norm(v) for v in vectors) == [25*nG, 36*nG, 81*nG]
                assert int(np.cross(tri[1], tri[2])) == 20*nG
                templates.append(tri)
                labels.append((kind, j, sign))
    dirs = sorted({direction(v) for t in templates for v in np.roll(t, -1, axis=0)-t}
                  | {direction(v) for v in np.roll(target, -1, axis=0)-target})
    dir_id = {d: i for i, d in enumerate(dirs)}
    xmin, ymin = target.min(axis=0)
    xmax, ymax = target.max(axis=0)
    width, height = int(xmax-xmin+1), int(ymax-ymin+1)
    space = width*height

    def contained(points):
        mask = np.ones(len(points), dtype=bool)
        for a, b in zip(target, np.roll(target, -1, axis=0)):
            e = b-a
            mask &= e[0]*(points[:, 1]-a[1])-e[1]*(points[:, 0]-a[0]) >= 0
        return mask

    def codes(points, d):
        return dir_id[direction(d)]*space+(points[:, 1]-ymin)*width+points[:, 0]-xmin

    xs, ys = np.meshgrid(np.arange(xmin, xmax+1), np.arange(ymin, ymax+1))
    points = np.column_stack((xs.ravel(), ys.ravel()))
    points = points[contained(points)]
    anchors, types, columns = [], [], []
    for i, tri in enumerate(templates):
        keep = contained(points+tri[1]) & contained(points+tri[2])
        pp = points[keep]
        anchors.append(pp)
        types.append(np.full(len(pp), i, dtype=np.int16))
        rows = []
        for a, b in zip(tri, np.roll(tri, -1, axis=0)):
            rows.extend([codes(pp+a, b-a), codes(pp+b, b-a)])
        columns.append(np.column_stack(rows))
    anchors, types, codes_all = np.concatenate(anchors), np.concatenate(types), np.concatenate(columns)
    J = len(anchors)
    target_codes = []
    for a, b in zip(target, np.roll(target, -1, axis=0)):
        target_codes.extend([codes(np.array([a]), b-a)[0], codes(np.array([b]), b-a)[0]])
    keys, inverse = np.unique(np.concatenate((codes_all.ravel(), target_codes)), return_inverse=True)
    colrows = inverse[:6*J].reshape((J, 6))
    signs = np.array([1, -1, 1, -1, 1, -1], dtype=np.int8)
    target_rhs = np.zeros(len(keys), dtype=np.int32)
    np.add.at(target_rhs, inverse[6*J:], signs)
    matrix = coo_matrix((np.tile(signs, J), (colrows.ravel(), np.repeat(np.arange(J), 6))),
                        shape=(len(keys), J)).tocsr()
    rhs = target_rhs.copy()
    hi = np.bincount(colrows[:, ::2].ravel(), minlength=len(keys)).astype(np.int32)
    lo = -np.bincount(colrows[:, 1::2].ravel(), minlength=len(keys)).astype(np.int32)
    values = np.full(J, -1, dtype=np.int8)
    queue = deque(np.flatnonzero((rhs <= lo) | (rhs >= hi)))
    assigned = 0
    conflict = None
    while queue:
        row = int(queue.popleft())
        b = int(rhs[row])
        if b < lo[row] or b > hi[row]:
            conflict = {'row': row, 'rhs': b, 'lower': int(lo[row]), 'upper': int(hi[row])}
            break
        if b != lo[row] and b != hi[row]:
            continue
        at_low = b == lo[row]
        start, end = matrix.indptr[row:row+2]
        for idx in range(start, end):
            col = int(matrix.indices[idx])
            if values[col] != -1:
                continue
            sign = int(matrix.data[idx])
            val = int(sign < 0) if at_low else int(sign > 0)
            values[col] = val
            assigned += 1
            for rr, ss in zip(colrows[col], signs):
                rr, ss = int(rr), int(ss)
                if ss > 0:
                    hi[rr] -= 1
                else:
                    lo[rr] += 1
                rhs[rr] -= ss*val
                if rhs[rr] <= lo[rr] or rhs[rr] >= hi[rr]:
                    queue.append(rr)
    report = {'scope': 'All contained positions in prescribed edge-height band only',
              'u': 2, 'v': 3, 'scale': scale, 'tile_count': 14*scale*scale,
              'edge_band': [L, U], 'whole_W56_decided': False,
              'anchors': len(points), 'orientations': len(templates),
              'placements': J, 'rows': len(keys), 'forced_assignments': assigned,
              'forced_one': int(np.sum(values == 1)), 'unknown': int(np.sum(values < 0)),
              'propagation_conflict': conflict, 'solver_status': None,
              'status': 'RESTRICTED_PROPAGATION_CONFLICT' if conflict else 'INCOMPLETE'}
    print(json.dumps(report), flush=True)
    if not conflict:
        if os.environ.get('ERDOS_ORTOOLS_PATH'):
            sys.path.insert(0, os.environ['ERDOS_ORTOOLS_PATH'])
        from ortools.sat.python import cp_model
        unknown = np.flatnonzero(values < 0)
        variables = {}
        model = cp_model.CpModel()
        for i in unknown:
            variables[int(i)] = model.new_bool_var('')
        for row in np.flatnonzero((hi > 0) | (lo < 0)):
            start, end = matrix.indptr[row:row+2]
            vv, cc = [], []
            for k in range(start, end):
                col = int(matrix.indices[k])
                if values[col] < 0:
                    vv.append(variables[col])
                    cc.append(int(matrix.data[k]))
            model.add(cp_model.LinearExpr.weighted_sum(vv, cc) == int(rhs[row]))
        model.add(sum(variables.values()) == 14*scale*scale-int(np.sum(values == 1)))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_search_workers = 1
        solver.parameters.random_seed = 634
        solver.parameters.linearization_level = 0
        solver.parameters.symmetry_level = 0
        answer = solver.solve(model)
        report['solver_status'] = solver.status_name(answer)
        if answer in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            for col in unknown:
                values[col] = solver.value(variables[int(col)])
            assert np.array_equal(matrix @ values, target_rhs)
            selected = np.flatnonzero(values == 1)
            assert len(selected) == 14*scale*scale
            conjugate_G = (G[0], -G[1])
            tris = [[mul(tuple(p), conjugate_G) for p in anchors[i]+templates[types[i]]]
                    for i in selected]
            certificate = {'metric': 'x^2+2y^2', 'denominator': int(nG),
                           'tile': [6, 5, 9], 'target': [[int(nG*x), int(nG*y)] for x, y in target_original],
                           'triangles': [[[int(x), int(y)] for x, y in t] for t in tris]}
            prefix.with_suffix('.certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
            report['status'] = 'TILING_CANDIDATE_REQUIRES_GEOMETRIC_REPLAY'
        elif answer == cp_model.INFEASIBLE:
            report['status'] = 'RESTRICTED_SOLVER_INFEASIBLE_NOT_CERTIFIED'
    report['seconds'] = time.monotonic()-started
    prefix.with_suffix('.report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O.')
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=int, default=-3)
    ap.add_argument('--U', type=int, default=1)
    ap.add_argument('--scale', type=int, default=2)
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--prefix', type=Path, required=True)
    args = ap.parse_args()
    run(args.L, args.U, args.scale, args.seconds, args.prefix)
