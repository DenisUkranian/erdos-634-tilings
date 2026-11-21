#!/usr/bin/env python3
"""Numerical discovery with exhaustive pricing and exact integer dual export.

The restricted master is never an infeasibility certificate.  Every dual
bound reported as exact is re-priced, after integer rounding, against
ALL contained placements.  verify_cylinder_dual.py independently checks
the exported certificate with a different containment enumeration.
"""
from pathlib import Path
import argparse
import gzip
import json
import time
import numpy as np
from scipy.optimize._highspy._core import (
    _Highs, HighsLp, HighsSparseMatrix, MatrixFormat, HighsModelStatus)
from cylinder_model import build


def export_integer(cat, dual, rhs, path, f, scale, iteration, elapsed):
    q = np.rint(dual*scale).astype(np.int64)
    if max(abs(int(q.min())), abs(int(q.max()))) > 2**50:
        raise ArithmeticError('Integer pricing safety bound exceeded')
    scores = cat.score(q)
    D = int(scores.max())
    numerator = sum(int(q[i])*int(rhs[i]) for i in np.flatnonzero(rhs))
    if D <= 0:
        raise ArithmeticError('Nonpositive column maximum: handle separately')
    ids = np.flatnonzero(q)
    data = {
        'format': 'contained-native-h1-cylinder-dual-v1',
        'tile': [cat.a, cat.b, cat.c],
        'native_base_charge_units': f,
        'scope': 'Necessary continuous cylinder projection for the stated fixed gate profile; not a physical tiling or a global semiprime exclusion.',
        'endpoint_row_count': cat.endpoint_rows,
        'row_count': cat.row_count,
        'raw_contained_placements': cat.count,
        'native_gate_currents': [int(rhs[cat.endpoint_rows]),
                                 int(rhs[cat.endpoint_rows+cat.c])],
        'all_remote_gate_currents': 0,
        'integer_row_potentials': [[int(i), int(q[i])] for i in ids],
        'maximum_column_score': D,
        'gate_objective': numerator,
        'population_lower_bound': {'numerator': numerator, 'denominator': D},
        'excludes_population_3c': numerator > 3*cat.c*D,
        'maximizing_placement': cat.labels([int(np.argmax(scores))])[0],
        'discovery': {'iteration': iteration, 'elapsed_seconds': elapsed,
                      'rounding_scale': scale},
    }
    payload = (json.dumps(data, separators=(',', ':'))+'\n').encode()
    if path.suffix == '.gz':
        path.write_bytes(gzip.compress(payload, mtime=0))
    else:
        path.write_bytes(payload)
    return numerator/D, numerator, D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tile', nargs=3, type=int, default=(33, 7, 37))
    ap.add_argument('--f', type=int, default=2)
    ap.add_argument('--iterations', type=int, default=12)
    ap.add_argument('--batch', type=int, default=6000)
    ap.add_argument('--seconds', type=float, default=20)
    ap.add_argument('--solver', choices=('simplex', 'ipm'), default='simplex')
    ap.add_argument('--seed-radius', type=int, default=37)
    ap.add_argument('--seed-x', type=int, default=800)
    ap.add_argument('--seed-y', type=int, default=0)
    ap.add_argument('--scale', type=int, default=10**7)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    t0 = time.monotonic()
    cat = build(*args.tile)
    rhs = cat.rhs(args.f)
    nart = 4*cat.c
    lp = HighsLp()
    lp.num_col_, lp.num_row_ = nart, cat.row_count
    lp.col_cost_ = np.full(nart, 1000., dtype=np.float64)
    lp.col_lower_ = np.zeros(nart)
    lp.col_upper_ = np.full(nart, np.inf)
    lp.row_lower_, lp.row_upper_ = rhs, rhs
    mat = HighsSparseMatrix()
    mat.format_ = MatrixFormat.kColwise
    mat.num_col_, mat.num_row_ = nart, cat.row_count
    mat.start_ = np.arange(nart+1, dtype=np.int32)
    mat.index_ = np.tile(np.arange(cat.endpoint_rows, cat.row_count,
                                   dtype=np.int32), 2)
    mat.value_ = np.r_[np.ones(2*cat.c), -np.ones(2*cat.c)]
    lp.a_matrix_ = mat
    h = _Highs()
    for k, v in [('output_flag', False), ('threads', 1),
                 ('parallel', 'off'), ('solver', args.solver),
                 ('presolve', 'on')]:
        h.setOptionValue(k, v)
    if args.solver == 'ipm':
        h.setOptionValue('run_crossover', 'off')
    h.passModel(lp)
    chosen = np.zeros(cat.count, dtype=bool)
    seed = np.flatnonzero((abs(cat.x.astype(np.int32)-args.seed_x) < args.seed_radius)
                         & (abs(cat.y.astype(np.int32)-args.seed_y) < args.seed_radius))
    ids_added = []

    def add(ids):
        if len(ids) == 0:
            return
        starts, rows, values = cat.sparse_columns(ids)
        h.addCols(len(ids), np.ones(len(ids)), np.zeros(len(ids)),
                  np.full(len(ids), np.inf), len(rows), starts, rows, values)
        chosen[ids] = True
        ids_added.extend(map(int, ids))

    add(seed)
    args.out.mkdir(parents=True, exist_ok=True)
    log = []
    best = -np.inf
    rng = np.random.default_rng(3431)
    print(json.dumps({'stage': 'catalogue', 'raw_columns': cat.count,
                      'rows': cat.row_count, 'initial_columns': len(seed),
                      'seconds': time.monotonic()-t0}), flush=True)
    for iteration in range(args.iterations):
        h.setOptionValue('time_limit', h.getRunTime()+args.seconds)
        h.run()
        status = h.getModelStatus()
        sol, info = h.getSolution(), h.getInfo()
        item = {'iteration': iteration, 'master_columns': len(ids_added),
                'status': str(status),
                'master_objective': float(info.objective_function_value),
                'primal_valid': bool(sol.value_valid),
                'dual_valid': bool(sol.dual_valid),
                'elapsed_seconds': time.monotonic()-t0}
        if not sol.dual_valid or len(sol.row_dual) != cat.row_count:
            log.append(item)
            print(json.dumps(item), flush=True)
            break
        dual = np.asarray(sol.row_dual)
        scores = cat.score(dual)
        mx = float(scores.max())
        objective = float(rhs@dual)
        item.update({'all_column_maximum': mx,
                     'unscaled_dual_objective': objective,
                     'global_pricing_bound': objective/mx if mx > 0 else None,
                     'priced_columns': cat.count})
        if mx > 0 and objective/mx > best+1e-7:
            exact, num, den = export_integer(cat, dual, rhs,
                 args.out/'BEST_CYLINDER_DUAL.json', args.f,
                 args.scale, iteration, time.monotonic()-t0)
            best = exact
            item.update({'exact_integer_bound': exact,
                         'exact_numerator': num, 'exact_denominator': den})
        if sol.value_valid:
            cv = np.asarray(sol.col_value)
            item['artificial_mass'] = float(cv[:nart].sum())
            item['real_tile_mass'] = float(cv[nart:].sum())
            item['maximum_primal_residual'] = float(info.max_primal_infeasibility)
            if cv[:nart].sum() < 1e-8 and info.max_primal_infeasibility < 1e-7:
                use = np.flatnonzero(cv[nart:] > 1e-9)
                support = [lab+[float(cv[nart+i])]
                           for i, lab in zip(use, cat.labels(np.asarray(ids_added)[use]))]
                (args.out/'NUMERICAL_PRIMAL.json').write_text(json.dumps({
                    'scope': 'Numerical necessary cylinder primal; neither exact nor a physical tiling.',
                    'tile': list(args.tile), 'f': args.f,
                    'population': item['real_tile_mass'], 'support': support})+'\n')
        log.append(item)
        (args.out/'DISCOVERY_LOG.json').write_text(json.dumps(log, indent=2)+'\n')
        print(json.dumps(item), flush=True)
        if best > 3*cat.c:
            print('Exact integer pricing has crossed 3c; independent verification required.', flush=True)
            break
        violating = np.flatnonzero((scores > 1+1e-8) & ~chosen)
        if len(violating) == 0:
            break
        # Equal scores at different positions should not concentrate a batch
        # in a single orientation or supporting line.
        if len(violating) > args.batch:
            perturb = rng.uniform(0., 1e-9, len(violating))
            top = np.argpartition(scores[violating]+perturb, -args.batch)[-args.batch:]
            violating = violating[top]
        add(violating)
    (args.out/'DISCOVERY_LOG.json').write_text(json.dumps(log, indent=2)+'\n')


if __name__ == '__main__':
    main()
