#!/usr/bin/env python3
"""Minimum residue population for explicitly fixed neighboring charges.

This exploratory LP does not assert geometric realizability. Its exported
dual candidates require a separate integer checker before theorem use.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import linprog
from strengthened_gate_model import old


def run(a,b,c,hand,residue,charge,native_up,seconds):
    A, rhs, _, _, _, labels=old.make_model(a,b,c)
    nc=len(labels);base=3*c*c;d=a-b
    equations=A[:base+2*c,:nc]
    g=np.zeros(2*c,dtype=int)
    g[(0 if hand=='up' else c)+residue]=charge
    g[0]=native_up;g[c]=-charge-native_up
    target=np.zeros(base+2*c)
    target[base:]=d*g
    target[base]+=2*c;target[base+c]-=c
    start=time.monotonic()
    result=linprog(np.ones(nc),A_eq=equations,b_eq=target,bounds=(0,None),
                   method='highs-ipm',options={'time_limit':seconds})
    out={'tile':[a,b,c],'hand':hand,'remote_residue':residue,
         'remote_charge_units':charge,'native_up_charge_units':native_up,
         'native_down_charge_units':int(g[c]),'status':int(result.status),
         'message':result.message,'seconds':time.monotonic()-start,
         'scope':'Minimum of a necessary residue projection, not a geometric tiling model.'}
    if result.x is not None:
        out['floating_population']=float(result.fun)
        out['equality_residual']=float(np.max(abs(equations@result.x-target)))
        if result.fun<=3*c+1e-7:
            out['support']=[list(labels[i])+[float(v)] for i,v in enumerate(result.x) if v>1e-8]
    if result.status==0:
        dual=np.rint(np.asarray(result.eqlin.marginals)*1000000).astype(np.int64)
        scores=np.asarray(equations.T@dual,dtype=np.int64)
        D=max(1,int(max(scores)))
        bound=int(np.asarray(target,dtype=np.int64)@dual)
        out.update(endpoint_tables=dual[:base].reshape(3,c,c).tolist(),
                   up_weights=dual[base:base+c].tolist(),
                   down_weights=dual[base+c:].tolist(),D=D,
                   lower_numerator=bound,lower_denominator=D,
                   exact_column_inequalities=bool(np.all(scores<=D)))
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int)
    p.add_argument('--hand',choices=('up','down'),default='up')
    p.add_argument('--residue',type=int,default=1)
    p.add_argument('--charge',type=int,default=1)
    p.add_argument('--native-up',type=int,default=-3)
    p.add_argument('--seconds',type=float,default=45)
    p.add_argument('--out',type=Path,required=True)
    ar=p.parse_args();out=run(ar.a,ar.b,ar.c,ar.hand,ar.residue,ar.charge,ar.native_up,ar.seconds)
    ar.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('support','endpoint_tables','up_weights','down_weights')},indent=2))
