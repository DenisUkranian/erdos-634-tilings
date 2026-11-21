#!/usr/bin/env python3
"""One fixed continuous residue profile; discovery only, never a tiling."""
from pathlib import Path
import gzip
import importlib.util
import json
import time

import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'research').is_dir() and (p / 'scripts').is_dir())
SOURCE = ROOT / 'research/2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py'


def main():
    spec = importlib.util.spec_from_file_location('existing_residue_columns', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    a, b, c = 35, 13, 43
    matrix, rhs, _, _, _, labels = module.make_model(a, b, c)
    columns = len(labels)
    matrix = matrix[:-2, :columns]
    rhs = rhs[:-2]
    rhs[3*c*c] = 42
    rhs[3*c*c+c] = 1
    start = time.monotonic()
    result = linprog(np.ones(columns), A_eq=matrix, b_eq=rhs,
                     bounds=(0, None), method='highs-ipm',
                     options={'time_limit': 90})
    report = {'tile': [a, b, c], 'gate_currents': [42, 1],
              'status': int(result.status), 'message': result.message,
              'seconds': time.monotonic()-start,
              'scope': 'Numerical discovery of one full periodic fractional profile. No physical tiling, no exact certificate in this file.'}
    if result.x is not None:
        values = result.x
        population = float(values.sum())
        uniform = (215-population)/columns
        padded = values+uniform
        positive_bins = np.zeros(2*c)
        for value, (_, _, j, hand, gate) in zip(padded, labels):
            if hand * (-1 if j % 2 else 1) > 0:
                positive_bins[(0 if hand > 0 else c)+gate] += value
        report.update(population=population,
                      maximum_equality_residual=float(np.max(abs(matrix@values-rhs))),
                      uniform_padding=uniform,
                      padded_population=float(padded.sum()),
                      minimum_padded_coordinate=float(padded.min()),
                      maximum_positive_gate_population=float(positive_bins.max()),
                      target_positive_gate_capacity=94,
                      support=[list(label)+[float(value)] for label, value in zip(labels, values) if value > 1e-12])
    encoded = (json.dumps(report, sort_keys=True, separators=(',', ':'))+'\n').encode()
    (HERE / 'N5063_NATIVE_215_PROFILE_IPM.json.gz').write_bytes(gzip.compress(encoded, compresslevel=9, mtime=0))
    print(json.dumps({k: v for k, v in report.items() if k != 'support'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
