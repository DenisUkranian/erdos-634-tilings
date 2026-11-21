#!/usr/bin/env python3
"""Integer multiplicities in the full periodic native-middle projection.

This adds integrality of TILE variables, not just gate charges. A periodic
integer solution still has neither actual locations nor disjoint interiors.
Any returned integer point is checked with integer arithmetic. A numerical
infeasibility or time-limit status is not a proof certificate.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import vstack, coo_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'research/2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py'
spec = importlib.util.spec_from_file_location('periodic_columns', SOURCE)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def run(a, b, c, blocks, seconds, native_up, fixed, binary=False):
    A, rhs, lo, hi, _, labels = old.make_model(a, b, c)
    n = len(labels)
    positive, negative = (blocks + 1) * c // 2, (blocks - 1) * c // 2
    assert blocks % 2 and blocks >= 3
    rhs[-2:] = [positive, negative]
    for k, (_, _, j, s, _) in enumerate(labels):
        hi[k] = 1 if binary else (positive if s * (-1 if j % 2 else 1) > 0 else negative)
    if fixed:
        A = A[:, :n]
        rhs[3*c*c] += (a-b)*native_up
        rhs[3*c*c+c] -= (a-b)*native_up
        lo, hi = lo[:n], hi[:n]
    else:
        d = a-b
        for g in range(2*c):
            offset = (2*c if g == 0 else -c if g == c else 0)
            lo[n+g] = int(np.ceil((-negative-offset)/d))
            hi[n+g] = int(np.floor((positive-offset)/d))
    # Valid single-class sign-specific positive/negative gate capacities.
    caps = {(33, 7, 37): (43, 179, 222),
            (35, 13, 43): (8, 35, 43)}.get((a, b, c))
    bins = [[] for _ in range(4*c)]
    for k, (_, _, j, s, gate) in enumerate(labels):
        eps = s * (-1 if j % 2 else 1)
        bins[(2*c if eps < 0 else 0)+(c if s < 0 else 0)+gate].append(k)
    if caps is not None:
        Cp, Cm, D = caps
        cap_pos = (Cp*positive + Cm*negative)//D
        cap_neg = (Cp*negative + Cm*positive)//D
    else:
        # No target-specific geometric certificate is asserted for other tiles.
        cap_pos, cap_neg = positive, negative
    rr=[];cc=[]
    for row, columns in enumerate(bins):
        rr.extend([row]*len(columns));cc.extend(columns)
    C = coo_matrix((np.ones(len(rr)), (rr,cc)),shape=(4*c,A.shape[1])).tocsc()
    constraints = [LinearConstraint(A, rhs, rhs),
                   LinearConstraint(C, np.zeros(4*c), np.r_[np.full(2*c,cap_pos),np.full(2*c,cap_neg)])]
    start=time.monotonic()
    result=milp(np.zeros(A.shape[1]),integrality=np.ones(A.shape[1]),
                bounds=Bounds(lo,hi),constraints=constraints,
                options={'time_limit':seconds,'mip_rel_gap':0.0})
    out={'tile':[a,b,c], 'odd_blocks':blocks,'odd_population':blocks*c,
         'native_up':native_up if fixed else None,'fixed_gate_profile':fixed,
         'binary_residue_columns':binary,'columns':A.shape[1],
         'integer_tile_columns':n,'rows':A.shape[0]+4*c,
         'sign_gate_caps':[cap_pos, cap_neg],
         'target_gate_capacity_certificate': caps is not None,
         'status':int(result.status),'message':result.message,
         'seconds':time.monotonic()-start,
         'scope':'All-residue integer-multiplicity projection. No spatial embedding, no nonoverlap, no complete tiling. Solver infeasibility is not an exact proof.'}
    for key in ('mip_node_count','mip_gap','mip_dual_bound'):
        value=getattr(result,key,None)
        if value is not None:out[key]=float(value)
    if result.x is not None:
        x=np.rint(result.x).astype(np.int64)
        B=A.astype(np.int64); rhs_int=np.rint(rhs).astype(np.int64)
        exact=bool(np.array_equal(B@x,rhs_int) and np.all(x>=lo) and np.all(x<=hi)
                   and np.all(C.astype(np.int64)@x<=np.r_[np.full(2*c,cap_pos),np.full(2*c,cap_neg)]))
        out['exact_integer_point_verified']=exact
        out['maximum_rounding_change']=float(np.max(abs(result.x-x)))
        if exact:
            out['support']=[list(labels[k])+[int(v)] for k,v in enumerate(x[:n]) if v]
            if not fixed:out['gate_charge_units']=x[n:].tolist()
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int)
    p.add_argument('--blocks',type=int,default=3);p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--native-up',type=int,default=-2);p.add_argument('--free-gates',action='store_true')
    p.add_argument('--binary-residues',action='store_true');p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    result=run(args.a,args.b,args.c,args.blocks,args.seconds,args.native_up,not args.free_gates,args.binary_residues)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('support',)},indent=2),flush=True)


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    main()
