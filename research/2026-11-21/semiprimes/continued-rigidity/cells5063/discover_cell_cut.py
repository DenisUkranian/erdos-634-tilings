#!/usr/bin/env python3
"""Discover an integer-checkable endpoint inequality for one cell current list."""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import eye, hstack

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
BASE=ROOT/'research/2026-11-21/semiprimes'
spec=importlib.util.spec_from_file_location('old_additive_marginals',BASE/'global-invariant/additive_gate_model.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def discover(currents, seconds=30):
    a,b,c=35,13,43
    M,shapes=old.make(a,b,c)
    gb=6*c
    rhs=np.zeros(M.shape[0]);rhs[gb:gb+2*c]=currents
    objective=np.r_[np.ones(12*c),np.zeros(12*c)]
    start=time.monotonic()
    res=linprog(objective,A_eq=M,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'time_limit':seconds})
    out={'tile':[a,b,c],'cell_gate_currents':list(map(int,currents)),
         'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,
         'scope':'Integer endpoint inequality discovered from a necessary marginal relaxation; independent all-column verification required. No whole-target exclusion.'}
    if res.status!=0:return out
    du=np.rint(res.eqlin.marginals*1000000).astype(np.int64)
    ep=np.zeros((3,c,c),dtype=np.int64)
    for axis in range(3):
        for x in range(c):
            for y in range(c):
                ep[axis,x,y]=du[axis*c+(a*y-b*x)%c]+du[3*c+axis*c+(a*x-b*y)%c]
    up=du[gb:gb+c];down=du[gb+c:gb+2*c]
    maximum=-10**30
    for x in range(c):
        for y in range(c):
            for j,s in shapes:
                eps=s*(-1)**j
                ux=x-a*old.U[j][0];uy=y-a*old.U[j][1]
                wx=x+b*old.U[(j+s)%6][0];wy=y+b*old.U[(j+s)%6][1]
                score=s*(int(ep[j%3,x,y])-int(ep[j%3,ux%c,uy%c])
                         +int(ep[(j+s)%3,wx%c,wy%c])-int(ep[(j+s)%3,x,y]))
                gate=(a*uy-b*ux)%c if s>0 else (a*ux-b*uy)%c
                score+=eps*int((up if s>0 else down)[gate])
                maximum=max(maximum,score)
    D=max(1,maximum)
    num=int(np.dot(np.asarray(currents,dtype=np.int64),np.r_[up,down]))
    out.update(floating_minimum_population=float(res.fun),D=D,
               endpoint_tables=ep.tolist(),up_weights=up.tolist(),down_weights=down.tolist(),
               lower_numerator=num,lower_denominator=D)
    return out


@lru_cache(maxsize=1)
def full_endpoint_model():
    source=ROOT/'research/2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py'
    spec=importlib.util.spec_from_file_location('full_endpoint_columns',source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    matrix,_,_,_,_,labels=module.make_model(35,13,43)
    equations=matrix[:3*43*43+2*43,:len(labels)].astype(np.int64)
    return equations,labels


def discover_full(currents, seconds=60):
    """Solve the full 22,188-column endpoint relaxation for this gate list.

    Only the exported integral dual becomes an exact claim after independent
    polygon verification. Floating primal support is retained for possible
    later rational reconstruction, never called a tiling.
    """
    a,b,c=35,13,43
    equations,labels=full_endpoint_model()
    base=3*c*c
    rhs=np.zeros(equations.shape[0]);rhs[base:]=currents
    start=time.monotonic()
    res=linprog(np.ones(len(labels)),A_eq=equations,b_eq=rhs,bounds=(0,None),
                method='highs-ipm',options={'time_limit':seconds})
    out={'tile':[a,b,c],'cell_gate_currents':list(map(int,currents)),
         'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,
         'oracle':'full_endpoint_columns',
         'scope':'Necessary full periodic endpoint relaxation. Only independently verified integral dual inequalities are exact; floating primal feasibility is not a tiling.'}
    penalty=False
    if res.status==2:
        # This auxiliary LP is always feasible. Its dual still scores every
        # genuine tile column by at most one, and can provide a certificate
        # even when the prescribed current list is outside the endpoint cone.
        penalty=True
        identity=eye(equations.shape[0],format='csc')
        extended=hstack((equations,identity,-identity),format='csc')
        cost=np.r_[np.ones(len(labels)),np.full(2*equations.shape[0],100.0)]
        res=linprog(cost,A_eq=extended,b_eq=rhs,bounds=(0,None),
                    method='highs-ipm',options={'time_limit':seconds})
        out.update(status=int(res.status),message=res.message,
                   seconds=time.monotonic()-start,penalty_oracle=True)
    if res.x is not None:
        primal=res.x[:len(labels)]
        out.update(maximum_equality_residual=float(np.max(abs(equations@primal-rhs))),
                   floating_support=[list(labels[i])+[float(v)] for i,v in enumerate(primal) if v>1e-8])
        out['floating_penalized_objective' if penalty else 'floating_minimum_population']=float(res.fun)
    if res.status!=0:return out
    dual=np.rint(res.eqlin.marginals*1000000).astype(np.int64)
    scores=np.asarray(equations.T@dual,dtype=np.int64)
    D=max(1,int(scores.max()))
    num=int(np.asarray(currents,dtype=np.int64)@dual[base:])
    out.update(D=D,endpoint_tables=dual[:base].reshape(3,c,c).tolist(),
               up_weights=dual[base:base+c].tolist(),down_weights=dual[base+c:].tolist(),
               lower_numerator=num,lower_denominator=D)
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('witness',type=Path);p.add_argument('--cell',type=int,required=True)
    p.add_argument('--seconds',type=float,default=30);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--full',action='store_true')
    ar=p.parse_args();data=json.loads(ar.witness.read_text())
    currents=data.get('cell_currents',data.get('finite_pool_witness',{}).get('cell_currents'))
    assert currents is not None
    out=(discover_full if ar.full else discover)(currents[ar.cell],ar.seconds)
    ar.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('endpoint_tables','up_weights','down_weights','floating_support')},indent=2))
