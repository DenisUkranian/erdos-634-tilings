#!/usr/bin/env python3
"""Diagnostic necessary residue relaxation for the minimal odd mode.

Not a geometric tiling model. Numerical solver outcomes are diagnostics
unless accompanied by an independently verified exact certificate.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, hstack, vstack

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / '2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py'
spec = importlib.util.spec_from_file_location('old_gate_model', SOURCE)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def run(a, b, c, seconds):
    A, rhs, lo, hi, integ, labels = old.make_model(a, b, c)
    nc = len(labels)
    d = a-b
    # Positive and negative charge units for remote gates. A signed charge
    # is their difference; their sums count disjoint long-side bins.
    remote = [i for i in range(2*c) if i not in (0,c)]
    ext = 2*len(remote)
    A = hstack((A, coo_matrix((A.shape[0],ext)))).tocsc()
    lo = np.r_[lo, np.zeros(ext)]
    hi = np.r_[hi, np.full(len(remote), (2*c)//d), np.full(len(remote), c//d)]
    integ = np.r_[integ, np.ones(ext)]
    ii=[];jj=[];vv=[];lows=[];highs=[]
    def add(entries, low, high):
        r=len(lows)
        for j,v in entries:
            if v:
                ii.append(r);jj.append(j);vv.append(v)
        lows.append(low);highs.append(high)
    base=nc+2*c
    for i,g in enumerate(remote):
        add([(nc+g,1),(base+i,-1),(base+len(remote)+i,1)],0,0)
    add([(base+i,1) for i in range(len(remote))],0,(2*c)//d)
    add([(base+len(remote)+i,1) for i in range(len(remote))],0,c//d)
    # The previously certified single-gate capacity applies to either hand.
    cap=44 if c==37 else 51
    bins=[[] for _ in range(2*c)]
    for i,(_,_,j,s,g) in enumerate(labels):
        eps=s*(-1 if j%2 else 1)
        if eps>0:
            bins[(0 if s>0 else c)+g].append((i,1))
    for entries in bins:
        add(entries,0,cap)
    for g in remote:
        lo[nc+g]=-1
        hi[nc+g]=cap//d
    for g,offset in ((0,2*c),(c,-c)):
        lo[nc+g]=int(np.ceil((-c-offset)/d))
        hi[nc+g]=int(np.floor((cap-offset)/d))
    E=coo_matrix((vv,(ii,jj)),shape=(len(lows),len(lo))).tocsc()
    matrix=vstack((A,E)).tocsc()
    start=time.monotonic()
    obj=np.zeros(len(lo))
    obj[base:]=1
    result=milp(obj,integrality=integ,bounds=Bounds(lo,hi),
        constraints=LinearConstraint(matrix,np.r_[rhs,lows],np.r_[rhs,highs]),
        options={'time_limit':seconds,'mip_rel_gap':0.0})
    out={'tile':[a,b,c],'odd_population':3*c,'seconds':time.monotonic()-start,
         'rows':matrix.shape[0],'columns':matrix.shape[1],
         'status':int(result.status),'message':result.message,
         'scope':'Necessary continuous-placement residue relaxation with integer gate charges; feasibility is not a tiling and numerical infeasibility is not an exact proof.'}
    for key in ('mip_node_count','mip_gap','mip_dual_bound','fun'):
        value=getattr(result,key,None)
        if value is not None: out[key]=float(value)
    if result.x is not None:
        x=result.x
        out['up_gate_charges']=np.rint(x[nc:nc+c]).astype(int).tolist()
        out['down_gate_charges']=np.rint(x[nc+c:nc+2*c]).astype(int).tolist()
        out['max_equality_residual']=float(np.max(abs(A@x-rhs)))
        out['support']=[list(labels[i])+[float(v)] for i,v in enumerate(x[:nc]) if v>1e-8]
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int)
    p.add_argument('--seconds',type=float,default=240)
    p.add_argument('--out',type=Path,required=True)
    ar=p.parse_args()
    out=run(ar.a,ar.b,ar.c,ar.seconds)
    ar.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='support'},indent=2))
