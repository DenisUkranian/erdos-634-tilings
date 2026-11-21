#!/usr/bin/env python3
"""Exploratory joint integral gate model with complete additive marginals.

Every actual cell induces the two orientation/residue marginals used here.
They retain every additive endpoint row, exact sign populations, and whole
node gate congruences. This remains a relaxation of physical placement.
Numerical infeasibility, timeout, or a floating feasible point is not a
mathematical decision about either target.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and (p / 'scripts').is_dir())
spec = importlib.util.spec_from_file_location('additive_marginals',
    ROOT / 'research/2026-11-21/semiprimes/global-invariant/additive_gate_model.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def run(args):
    a, b, c = (33, 7, 37) if args.target == 3431 else (35, 13, 43)
    d = a - b
    if args.kind == 'one':
        cells, nr, nc = [(0, 0, 2*c if c == 37 else 3*c, c if c == 37 else 2*c)], 1, 1
        assert args.native_row == args.native_col == 0
    elif args.kind == 'two':
        assert c == 43
        cells, nr, nc = [(0, 0, 43, 43), (0, 1, 86, 43)], 1, 2
        assert args.native_row == 0 and args.native_col in (0, 1)
    else:
        assert c == 43 and 1 <= args.x <= 42
        x = args.x
        cells, nr, nc = [(0, 0, x, x), (0, 1, 43-x, 43-x),
                         (1, 0, 43-x, 43-x), (1, 1, 43+x, x)], 2, 2
    ncell = len(cells)
    local, shapes = old.make(a, b, c)
    local = local.tocoo()
    per = local.shape[1]
    qbase = per*ncell
    ebase = qbase + 2*c*ncell
    nvars = ebase + (nr+nc)*c
    lower = np.zeros(nvars)
    upper = np.full(nvars, np.inf)
    integrality = np.zeros(nvars)
    if args.integer_marginals:
        integrality[:qbase] = 1
    integrality[qbase:] = 1
    lower[ebase:] = -20
    upper[ebase:] = 20
    ii, jj, vv, lows, highs = [], [], [], [], []
    def add(terms, lo, hi):
        r = len(lows)
        for k, v in terms:
            if v:
                ii.append(r); jj.append(k); vv.append(v)
        lows.append(lo); highs.append(hi)
    for h, (row, col, positive, negative) in enumerate(cells):
        rowbase = len(lows)
        ii.extend((local.row + rowbase).tolist())
        jj.extend((local.col + h*per).tolist())
        vv.extend(local.data.tolist())
        lows.extend([0]*local.shape[0]); highs.extend([0]*local.shape[0])
        for g in range(2*c):
            ii.append(rowbase + 6*c + g)
            jj.append(qbase + 2*c*h + g)
            vv.append(-1)
        upper[h*per:(h+1)*per] = positive+negative
        lower[qbase+2*c*h:qbase+2*c*(h+1)] = -negative
        upper[qbase+2*c*h:qbase+2*c*(h+1)] = positive
        for sign, count in ((1, positive), (-1, negative)):
            terms = [(h*per + o*c + residue, 1)
                     for o, (j, s) in enumerate(shapes)
                     if s*(-1 if j % 2 else 1) == sign
                     for residue in range(c)]
            add(terms, count, count)
    for part, count, native, offset in ((0, nr, args.native_row, 2*c),
                                      (1, nc, args.native_col, -c)):
        for node in range(count):
            for g in range(c):
                ei = ebase + (node if part == 0 else nr+node)*c + g
                terms = [(ei, -d)]
                terms.extend((qbase+h*2*c+part*c+g, 1)
                    for h, cell in enumerate(cells) if cell[part] == node)
                rhs = offset if node == native and g == 0 else 0
                add(terms, rhs, rhs)
                if args.fixed_native_profile:
                    lower[ei] = upper[ei] = ((-2 if part == 0 else 2)
                        if node == native and g == 0 else 0)
    A = coo_matrix((vv, (ii, jj)), shape=(len(lows), nvars)).tocsc()
    # Feasibility only. The zero objective avoids favoring a special gate
    # inventory; every recorded integral candidate is checked below.
    start = time.monotonic()
    result = milp(np.zeros(nvars), integrality=integrality,
        bounds=Bounds(lower, upper),
        constraints=LinearConstraint(A, np.array(lows), np.array(highs)),
        options={'time_limit':args.seconds, 'mip_rel_gap':0.0})
    output = {'tile':[a,b,c], 'target':args.target, 'kind':args.kind,
        'x':args.x, 'native_row':args.native_row, 'native_col':args.native_col,
        'integer_marginals':args.integer_marginals,
        'fixed_native_profile':args.fixed_native_profile,
        'cells':[list(cell) for cell in cells], 'status':int(result.status),
        'message':result.message, 'seconds':time.monotonic()-start,
        'rows':len(lows), 'columns':nvars,
        'scope':'Necessary marginal projection only. No full endpoint kernel, physical tiling, or target exclusion is asserted.'}
    if result.x is not None:
        solution = result.x.copy()
        solution[integrality != 0] = np.rint(solution[integrality != 0])
        residual = A @ solution
        output['maximum_row_error_after_integer_rounding'] = float(max(
            np.max(np.array(lows)-residual), np.max(residual-np.array(highs)), 0))
        output['maximum_bound_error_after_integer_rounding'] = float(max(
            np.max(lower-solution), np.max(solution-upper), 0))
        output['cell_currents'] = solution[qbase:ebase].astype(int).reshape(ncell, 2*c).tolist()
        output['node_charge_units'] = solution[ebase:].astype(int).tolist()
        output['marginal_support'] = [[int(k), int(v) if args.integer_marginals else float(v)]
            for k, v in enumerate(solution[:qbase]) if abs(v) > 1e-9]
        if args.integer_marginals:
            # Every matrix entry is integral; bounded counts make this
            # integer accumulator exact, independently of floating tolerances.
            integer_solution = [int(v) for v in solution]
            totals = [0]*len(lows)
            for r, k, value in zip(ii, jj, vv):
                assert int(value) == value
                totals[r] += int(value)*integer_solution[k]
            assert all(lo <= value <= hi for lo, value, hi in zip(lows, totals, highs))
            assert all(lo <= value <= hi for lo, value, hi in zip(lower, integer_solution, upper))
            output['integer_matrix_and_bounds_checked'] = True
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=int, choices=(3431, 5063), required=True)
    parser.add_argument('--kind', choices=('one','two','four'), default='one')
    parser.add_argument('--x', type=int, default=21)
    parser.add_argument('--native-row', type=int, default=0)
    parser.add_argument('--native-col', type=int, default=0)
    parser.add_argument('--integer-marginals', action='store_true')
    parser.add_argument('--fixed-native-profile', action='store_true')
    parser.add_argument('--seconds', type=float, default=45)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    output = run(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in
        ('cell_currents', 'node_charge_units', 'marginal_support')}, indent=2))


if __name__ == '__main__':
    main()
