#!/usr/bin/env python3
"""Exploratory shared-node integer gate model for the remaining 5063 cells.

By default every cell gate current is integral; an explicit option relaxes
those currents. The endpoint inequalities are only the existing finite
dual pool. A feasible point is not a tiling. Numerical
infeasibility or a timeout is not an impossibility certificate.
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
ROOT = next(p for p in HERE.parents if (p / "research").is_dir() and (p / "scripts").is_dir())
BASE = ROOT / "research/2026-11-21/semiprimes"
spec = importlib.util.spec_from_file_location("existing_transformed_cuts", BASE / "gate-model/build_profile_cuts.py")
cuts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cuts_module)


def load_cuts(include_new=True):
    index = json.loads((BASE / "gate-model/CERTIFICATES_5063.json").read_text())
    out = []
    for item in index["certificates"]:
        tile, D, up, down = cuts_module.load_cut(ROOT / item["path"])
        out.extend(cuts_module.transforms(*tile, D, up, down))
    if include_new:
        for path in sorted(HERE.glob('shared_profile_cut_*.json')):
            tile,D,up,down=cuts_module.load_cut(path)
            out.extend(cuts_module.transforms(*tile,D,up,down))
    return [(int(D), np.asarray(u, dtype=np.int64), np.asarray(v, dtype=np.int64)) for D, u, v in out]


def case_cells(kind, x):
    if kind == "two":
        # Row tree has one native 215-node. Column zero is the balanced
        # 86-node and column one the charged 129-node.
        return [(0, 0, 43, 43), (0, 1, 86, 43)], 1, 2
    return [(0, 0, x, x), (0, 1, 43-x, 43-x),
            (1, 0, 43-x, 43-x), (1, 1, 43+x, x)], 2, 2


def run(kind, x, native_row, native_col, seconds, fixed_native_profile=False,
        continuous_cell_currents=False):
    c, d = 43, 22
    cells, nr, nc = case_cells(kind, x)
    ncell = len(cells)
    nq = ncell * 2*c
    # q then |positive q|, |negative q| then whole-node charge units.
    ebase = 3*nq
    eend = ebase + (nr+nc)*c
    nvars = eend
    lower = np.zeros(nvars)
    upper = np.full(nvars, np.inf)
    integ = np.zeros(nvars)
    integ[:nq] = 0 if continuous_cell_currents else 1
    integ[ebase:] = 1
    lower[ebase:] = -20
    upper[ebase:] = 20
    objective = np.zeros(nvars)
    objective[nq:3*nq] = 1
    entries = []
    bounds = []
    def add(coeff, lo, hi):
        entries.append(coeff)
        bounds.append((lo, hi))
    for h, (row, col, pos, neg) in enumerate(cells):
        start = h*2*c
        cp = min(pos, (8*pos+35*neg)//43)
        cm = min(neg, (8*neg+35*pos)//43)
        lower[start:start+2*c] = -cm
        upper[start:start+2*c] = cp
        upper[nq+start:nq+start+2*c] = cp
        upper[2*nq+start:2*nq+start+2*c] = cm
        for k in range(start, start+2*c):
            add({k:1,nq+k:-1,2*nq+k:1},0,0)
        add({nq+k:1 for k in range(start,start+2*c)},0,pos)
        add({2*nq+k:1 for k in range(start,start+2*c)},0,neg)
        add({k:1 for k in range(start,start+2*c)},pos-neg,pos-neg)
    for part, count, native, offset in ((0,nr,native_row,86),(1,nc,native_col,-43)):
        for node in range(count):
            for g in range(c):
                ei = ebase + (node if part==0 else nr+node)*c+g
                coeff={ei:-d}
                for h, cell in enumerate(cells):
                    if cell[part]==node:
                        coeff[h*2*c+part*c+g]=1
                rhs = offset if node==native and g==0 else 0
                add(coeff,rhs,rhs)
                if fixed_native_profile:
                    lower[ei]=upper[ei]=((-2 if part==0 else 2)
                        if node==native and g==0 else 0)
    cuts = load_cuts()
    seen = set()
    activated = set()
    def add_cut(cell, ci, su, sv):
        key=(cell,ci,su,sv)
        if key in seen:return False
        seen.add(key)
        D,u,v=cuts[ci]
        shift=np.r_[np.roll(u,-su),np.roll(v,-sv)]
        add({cell*2*c+k:int(w)/D for k,w in enumerate(shift) if w},
            -np.inf,cells[cell][2]+cells[cell][3])
        return True
    def activate_all_shifts(cell, ci):
        """Exact extended formulation of all 43-by-43 shifted inequalities.

        The two unrestricted auxiliary maxima are continuous. Existence of
        them is equivalent to every pair of independently shifted hand cuts.
        Activate a family only when needed, avoiding a large initial matrix.
        """
        nonlocal nvars, lower, upper, integ, objective
        key=(cell,ci)
        if key in activated:return False
        activated.add(key)
        first=nvars
        nvars+=2
        lower=np.r_[lower,[-np.inf,-np.inf]]
        upper=np.r_[upper,[np.inf,np.inf]]
        integ=np.r_[integ,[0,0]]
        objective=np.r_[objective,[0,0]]
        D,u,v=cuts[ci]
        for part,weights in enumerate((u,v)):
            for shift in range(c):
                coeff={cell*2*c+part*c+k:int(w)/D
                       for k,w in enumerate(np.roll(weights,-shift)) if w}
                coeff[first+part]=-1
                add(coeff,-np.inf,0)
        add({first:1,first+1:1},-np.inf,cells[cell][2]+cells[cell][3])
        return True
    for h in range(ncell):
        for ci in range(len(cuts)):
            add_cut(h,ci,0,0)
    start=time.monotonic()
    trace=[]
    final=None
    while time.monotonic()-start < seconds:
        ri=[];ci=[];vv=[]
        for r,coef in enumerate(entries):
            for k,v in coef.items():ri.append(r);ci.append(k);vv.append(v)
        matrix=coo_matrix((vv,(ri,ci)),shape=(len(entries),nvars)).tocsc()
        lows,highs=np.asarray(bounds).T
        remain=seconds-(time.monotonic()-start)
        res=milp(objective,integrality=integ,bounds=Bounds(lower,upper),
                 constraints=LinearConstraint(matrix,lows,highs),
                 options={"time_limit":max(1,min(30,remain)),"mip_rel_gap":0.0})
        row={"status":int(res.status),"message":res.message,
             "seconds":time.monotonic()-start,"rows":len(entries)}
        trace.append(row)
        if res.x is None:
            if res.status==2:break
            continue
        q=(res.x[:nq] if continuous_cell_currents else
           np.rint(res.x[:nq]).astype(np.int64)).reshape((ncell,2*c))
        violations=[]
        for h in range(ncell):
            pop=cells[h][2]+cells[h][3]
            for ci,(D,u,v) in enumerate(cuts):
                U=np.asarray([np.dot(np.roll(u,-s),q[h,:c]) for s in range(c)])
                V=np.asarray([np.dot(np.roll(v,-s),q[h,c:]) for s in range(c)])
                su,sv=int(U.argmax()),int(V.argmax())
                gap=float(U[su]+V[sv]-D*pop)
                if gap>(1e-6*D if continuous_cell_currents else 0):
                    violations.append((gap/D,h,ci,su,sv))
        violations.sort(reverse=True)
        row["violated_shifted_cuts"]=len(violations)
        row["objective"]=float(res.fun)
        if not violations:
            ee=np.rint(res.x[ebase:eend]).astype(np.int64).tolist()
            if not continuous_cell_currents:
                for h,cell in enumerate(cells):
                    pos,neg=cell[2:]
                    assert sum(q[h])==pos-neg
                    assert sum(max(int(v),0) for v in q[h])<=pos
                    assert sum(max(-int(v),0) for v in q[h])<=neg
                    cp=min(pos,(8*pos+35*neg)//43)
                    cm=min(neg,(8*neg+35*pos)//43)
                    assert all(-cm<=v<=cp for v in q[h])
                for part,count,native,offset in ((0,nr,native_row,86),(1,nc,native_col,-43)):
                    for node in range(count):
                        for g in range(c):
                            current=sum(int(q[h,part*c+g]) for h,cell in enumerate(cells) if cell[part]==node)
                            index=(node if part==0 else nr+node)*c+g
                            assert current==(offset if node==native and g==0 else 0)+22*ee[index]
                            if fixed_native_profile:
                                assert ee[index]==((-2 if part==0 else 2) if node==native and g==0 else 0)
            final={"cell_currents":q.tolist(),"node_charge_units":ee,
                   "integer_master_conditions_checked":not continuous_cell_currents}
            break
        added=0
        for _,h,ci,su,sv in violations:
            added+=activate_all_shifts(h,ci)
        row["activated_shift_families"]=added
        print(json.dumps(row),flush=True)
        if not added:break
    return {"tile":[35,13,43],"kind":kind,"x":x,"native_row":native_row,
            "native_col":native_col,"fixed_native_profile":fixed_native_profile,
            "continuous_cell_currents":continuous_cell_currents,
            "cells":cells,"seconds":time.monotonic()-start,"trace":trace,
            "finite_pool_witness":final,
            "scope":"Exploratory necessary shared-node integer gate projection only. No physical tiling or target infeasibility is established."}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind",choices=("two","four"),default="two")
    p.add_argument("--x",type=int,default=21)
    p.add_argument("--native-row",type=int,default=0)
    p.add_argument("--native-col",type=int,default=0)
    p.add_argument("--seconds",type=float,default=90)
    p.add_argument("--fixed-native-profile",action="store_true")
    p.add_argument("--continuous-cell-currents",action="store_true")
    p.add_argument("--out",type=Path,required=True)
    ar=p.parse_args()
    out=run(ar.kind,ar.x,ar.native_row,ar.native_col,ar.seconds,ar.fixed_native_profile,
            ar.continuous_cell_currents)
    ar.out.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="finite_pool_witness"}),flush=True)
