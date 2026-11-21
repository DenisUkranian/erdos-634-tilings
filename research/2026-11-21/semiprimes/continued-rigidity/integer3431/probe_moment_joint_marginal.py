#!/usr/bin/env python3
"""Expose necessary integer first moments in the 3431 marginal probe.

This changes only the solver formulation. For each unoriented axis i,
33 M_i - 7 L_i is divisible by 37. Equivalently -4 M_i - 7 L_i is
divisible by 37. M and L are the signed a- and b-edge inventories.
The original integral marginal endpoint equations already imply this.
No infeasibility status is used as a certificate of target exclusion.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, hstack, vstack

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('joint_marginal_probe',
    HERE.parent / 'joint-marginals/probe_joint_marginal_integer.py')
joint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(joint)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixed-native-profile', action='store_true')
    parser.add_argument('--seconds', type=float, default=45)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    audit = {}

    def augmented_milp(objective, *, integrality, bounds, constraints, options):
        n = len(objective)
        rows, cols, vals = [], [], []
        for o, (j, s) in enumerate(joint.old.make(33, 7, 37)[1]):
            eps = s*(-1 if j % 2 else 1)
            for residue in range(37):
                for axis, coeff in ((j % 3, -4*eps), ((j+s) % 3, -7*eps)):
                    rows.append(axis); cols.append(o*37+residue); vals.append(coeff)
        for axis in range(3):
            rows.append(axis); cols.append(n+axis); vals.append(-37)
        moments = coo_matrix((vals, (rows, cols)), shape=(3, n+3)).tocsc()
        A = vstack((hstack((constraints.A, coo_matrix((constraints.A.shape[0], 3)))),
                    moments)).tocsc()
        low = np.r_[constraints.lb, [0]*3]
        high = np.r_[constraints.ub, [0]*3]
        # Every cell has 111 tiles; |(-4 M_i-7 L_i)/37| <= 33.
        lower = np.r_[bounds.lb, [-33]*3]
        upper = np.r_[bounds.ub, [33]*3]
        result = milp(np.r_[objective, [0]*3],
            integrality=np.r_[integrality, [1]*3],
            bounds=Bounds(lower, upper), constraints=LinearConstraint(A, low, high),
            options=options)
        audit['added_integer_quotients'] = 3
        audit['added_rows'] = 3
        if result.x is not None:
            x = [int(round(v)) for v in result.x]
            totals = [0]*A.shape[0]
            entries = A.tocoo()
            for row, col, coeff in zip(entries.row, entries.col, entries.data):
                assert int(coeff) == coeff
                totals[row] += int(coeff)*x[col]
            assert all(a <= v <= b for a, v, b in zip(low, totals, high))
            assert all(a <= v <= b for a, v, b in zip(lower, x, upper))
            audit['augmented_integer_rows_and_bounds_checked'] = True
            audit['moment_quotients'] = x[n:]
            result.x = result.x[:n]
        return result

    joint.milp = augmented_milp
    params = argparse.Namespace(target=3431, kind='one', x=21, native_row=0,
        native_col=0, integer_marginals=True,
        fixed_native_profile=args.fixed_native_profile, seconds=args.seconds)
    output = joint.run(params)
    output['moment_formulation'] = audit
    args.out.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in
        ('cell_currents', 'node_charge_units', 'marginal_support')}, indent=2))


if __name__ == '__main__':
    main()
