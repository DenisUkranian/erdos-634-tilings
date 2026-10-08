#!/usr/bin/env python3
"""Alternative Boolean solver for the same bounded placement model.

Only an independently checked positive certificate decides a tiling here.
The CP-SAT negative status is retained as a scoped solver diagnostic.
Install scipy, numpy and ortools; an optional ERDOS_ORTOOLS_PATH may point
to a separate installation. Reports are written under cpsat/.
"""
import importlib.util
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import scipy.optimize

if os.environ.get('ERDOS_ORTOOLS_PATH'):
    sys.path.insert(0, os.environ['ERDOS_ORTOOLS_PATH'])
from ortools.sat.python import cp_model


def boolean_solver(c, integrality, bounds, constraints, options):
    assert np.all(integrality == 1), 'This driver searches integer placements.'
    matrix = constraints.A.tocsr()
    rhs = np.asarray(constraints.lb)
    assert np.array_equal(rhs, constraints.ub)
    assert np.all(rhs == np.rint(rhs))
    assert np.all(matrix.data == np.rint(matrix.data))
    model = cp_model.CpModel()
    variables = [model.new_bool_var('') for _ in range(matrix.shape[1])]
    for row in range(matrix.shape[0]):
        first, last = matrix.indptr[row:row+2]
        indices = matrix.indices[first:last]
        coefficients = [int(v) for v in matrix.data[first:last]]
        model.add(cp_model.LinearExpr.weighted_sum(
            [variables[int(k)] for k in indices], coefficients) == int(rhs[row]))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(options['time_limit'])
    solver.parameters.num_search_workers = 1
    solver.parameters.linearization_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.random_seed = 634
    solver.parameters.log_search_progress = True
    status = solver.solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        x = np.array([solver.value(v) for v in variables], dtype=np.int8)
        assert np.array_equal(matrix @ x, rhs)
        return SimpleNamespace(status=0, x=x, message=solver.status_name(status))
    return SimpleNamespace(status=2 if status == cp_model.INFEASIBLE else 1,
                           x=None, message='CP-SAT: '+solver.status_name(status))


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('placement_model', here/'search.py')
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    model.milp = boolean_solver
    out = here/'cpsat'
    out.mkdir(exist_ok=True)
    model.__file__ = str(out/'search.py')
    model.main()
