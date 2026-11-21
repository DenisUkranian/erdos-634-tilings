#!/usr/bin/env python3
"""Discover a periodic dual, then price it on every contained cylinder column.

This is a reproducible numerical discovery control.  Its exported bound
is independently certified by verify_cylinder_dual.py.  The exact
convolution lift, not this optimizer, proves cylinder feasibility at 111.
"""
from pathlib import Path
import importlib.util
import json
import time
import numpy as np
from scipy.optimize import linprog
from cylinder_model import build
from column_generation import export_integer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
source = ROOT/'research/2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py'
spec = importlib.util.spec_from_file_location('old_periodic_columns', source)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def main():
    started = time.monotonic()
    a, b, c = 33, 7, 37
    A, rhs, lo, hi, integrality, labels = old.make_model(a, b, c)
    nr = 3*c*c+2*c
    rhs = np.zeros(nr)
    rhs[3*c*c], rhs[3*c*c+c] = 22, 15
    result = linprog(np.ones(12*c*c), A_eq=A[:nr, :12*c*c], b_eq=rhs,
                     bounds=(0, None), method='highs-ipm',
                     options={'time_limit': 20.0})
    if result.status != 0:
        raise RuntimeError(f'No optimal numerical control point: {result.message}')
    periodic = np.asarray(result.eqlin.marginals)
    cat = build(a, b, c)
    dual = np.zeros(cat.row_count)
    xmin, xmax, ymin, ymax, tmin, tmax = cat.bounds
    for y in range(ymin, ymax+1):
        for r in range(c):
            dual[(y-ymin)*c+r] = periodic[r*c+y % c]
    for x in range(xmin, xmax+1):
        for r in range(c):
            dual[cat.offsets[1]+(x-xmin)*c+r] = periodic[c*c+(x % c)*c+r]
    for t in range(tmin, tmax+1):
        for r in range(c):
            dual[cat.offsets[2]+(t-tmin)*c+r] = periodic[2*c*c+((t-r) % c)*c+r]
    dual[cat.endpoint_rows:] = periodic[3*c*c:]
    bound, numerator, denominator = export_integer(
        cat, dual, cat.rhs(2), HERE/'PERIODIC_DUAL_FULL_CATALOGUE.json.gz',
        2, 10**9, 0, time.monotonic()-started)
    report = {'scope': 'Numerical discovery of a dual; integer pricing covers the full contained cylinder catalogue. Independent replay required for the bound.',
              'numerical_torus_status': int(result.status),
              'numerical_torus_objective': float(result.fun),
              'numerical_torus_max_residual': float(np.max(np.abs(A[:nr, :12*c*c]@result.x-rhs))),
              'raw_contained_columns_priced': cat.count,
              'exact_integer_bound': {'numerator': numerator, 'denominator': denominator},
              'decimal_bound_for_display': bound,
              'elapsed_seconds': time.monotonic()-started}
    (HERE/'PERIODIC_DUAL_DISCOVERY.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
