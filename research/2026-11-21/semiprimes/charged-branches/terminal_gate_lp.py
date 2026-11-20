#!/usr/bin/env python3
"""Diagnostic periodic endpoint LP for a one-accessible-gate tile class.

This is a necessary relaxation, not a tiling model. Columns are either a
single downward tile at one selected gate or a complete half-turn pair.
No geometric placement or finite support is asserted by feasibility.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "research/2026-11-20/semiprimes/continuation/global-closure/median"
sys.path.insert(0, str(SOURCE))
from per_gate_integrality import make_model, U


def generate(a, b, c, seconds=45):
    original, _, _, _, _, labels = make_model(a, b, c)
    n = len(labels)
    base = 3 * c * c
    endpoints = original[:base, :n]
    index = {tuple(label[:4]): k for k, label in enumerate(labels)}
    singles = [k for k, label in enumerate(labels) if label[3] == -1 and label[4] == 0]
    pairs = []
    for k, (x, y, j, s, gate) in enumerate(labels):
        xp = (x - a * U[j][0] + b * U[(j+s) % 6][0]) % c
        yp = (y - a * U[j][1] + b * U[(j+s) % 6][1]) % c
        other = index[xp, yp, (j+3) % 6, s]
        if k < other:
            pairs.append((k, other))
    paired = endpoints[:, [k for k, l in pairs]] + endpoints[:, [l for k, l in pairs]]
    A = hstack([endpoints[:, singles], paired], format="csc")
    charges = np.r_[[(1 if labels[k][2] % 2 else -1) for k in singles], np.zeros(len(pairs))]
    A = vstack([A, csc_matrix(charges.reshape(1, -1))], format="csc")
    rhs = np.r_[np.zeros(base), c]
    objective = np.r_[np.ones(len(singles)), np.repeat(2., len(pairs))]
    start = time.monotonic()
    result = linprog(objective, A_eq=A, b_eq=rhs, bounds=(0, None), method="highs-ipm", options={"time_limit": seconds})
    output = {"tile": [a,b,c], "scope": __doc__, "rows": A.shape[0], "single_columns":len(singles), "paired_columns":len(pairs), "status":int(result.status), "message":result.message, "seconds":time.monotonic()-start}
    if result.x is not None:
        output["floating_population"] = float(result.fun)
        output["floating_blocks"] = float(result.fun / c)
        output["maximum_equality_residual"] = float(np.max(np.abs(A @ result.x-rhs)))
    if result.status == 0:
        scale = 1000000
        dual = np.rint(np.asarray(result.eqlin.marginals)*scale).astype(np.int64)
        scores = np.asarray(A.T @ dual, dtype=np.int64)
        # Pair scores may consume twice the per-tile allowance.
        D = max(1, int(max(scores[:len(singles)])), int(max((scores[len(singles):]+1)//2)))
        assert np.all(scores <= objective * D)
        output.update(D=D, charge_multiplier=int(dual[-1]), endpoint_tables=dual[:base].reshape(3,c,c).tolist(), exact_lower_numerator=int(c*dual[-1]), exact_lower_denominator=D)
        # A rational primal is only a periodic relaxation witness. It can
        # establish the limit of this LP, but never a geometric tiling.
        primal=[Fraction(float(v)).limit_denominator(100000) for v in result.x]
        sums=[Fraction(0)]*A.shape[0]
        coo=A.tocoo()
        for row,col,value in zip(coo.row,coo.col,coo.data):
            if primal[col]: sums[row]+=int(value)*primal[col]
        if all(value==int(target) for value,target in zip(sums,rhs)) and all(v>=0 for v in primal):
            population=sum((1 if i<len(singles) else 2)*v for i,v in enumerate(primal))
            support=[]
            for i,value in enumerate(primal):
                if not value: continue
                if i<len(singles):
                    tile_labels=[list(labels[singles[i]])]
                else:
                    tile_labels=[list(labels[k]) for k in pairs[i-len(singles)]]
                support.append([tile_labels,value.numerator,value.denominator])
            output.update(exact_periodic_primal_population=str(population),exact_periodic_primal_blocks=str(population/c),periodic_primal_support=support)
    return output


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("a",type=int); p.add_argument("b",type=int); p.add_argument("c",type=int)
    p.add_argument("--seconds", type=float,default=45)
    p.add_argument("--out",type=Path, required=True)
    args=p.parse_args()
    out=generate(args.a,args.b,args.c,args.seconds)
    args.out.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in ("endpoint_tables","periodic_primal_support")},indent=2),flush=True)
