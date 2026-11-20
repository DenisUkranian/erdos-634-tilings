#!/usr/bin/env python3
"""Generate exact dual candidates with all remote signed gate currents zero.

Every native h1 placement remains a single column. No mate condition is
imposed. Only the endpoint equations, zero remote signed currents, and
total charge c are imposed; there is no population cap or fixed native f.
"""
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack
from per_gate_integrality import make_model


def generate(a,b,c,seconds,method):
    source,_,_,_,_,labels=make_model(a,b,c)
    nc=len(labels);base=3*c*c
    single=source[:,:nc]
    endpoint=single[:base]
    up_indices=list(range(base+1,base+c))
    down_indices=list(range(base+c+1,base+2*c))
    charge=single[-2]-single[-1]
    equations=vstack((endpoint,single[up_indices],single[down_indices],charge)).tocsc()
    rhs=np.r_[np.zeros(equations.shape[0]-1),c]
    start=time.monotonic()
    solution=linprog(np.ones(nc),A_eq=equations,b_eq=rhs,bounds=(0,None),
                     method=method,options={'time_limit':seconds})
    report={'tile':[a,b,c],'rows':equations.shape[0],'columns':nc,
            'status':int(solution.status),'message':solution.message,
            'seconds':time.monotonic()-start,
            'method':method,
            'scope':'All native h1 placements; all remote signed gate currents zero; charge c; no forced mates, no fixed native parameter and no population upper bound.'}
    if solution.x is not None:
        report['floating_population']=float(solution.fun)
        report['floating_blocks']=float(solution.fun/c)
    if solution.status==0:
        scale=1000000
        y=np.rint(np.asarray(solution.eqlin.marginals)*scale).astype(np.int64)
        scores=np.asarray(equations.T@y,dtype=np.int64)
        D=max(1,int(max(scores)))
        assert np.all(scores<=D)
        t=int(y[-1])
        up=[0]+[int(v) for v in y[base:base+c-1]]
        down=[0]+[int(v) for v in y[base+c-1:base+2*(c-1)]]
        report.update(D=D,charge_multiplier_t=t,
                      endpoint_tables=y[:base].reshape(3,c,c).tolist(),
                      up_remote_weights=up,down_remote_weights=down,
                      exact_lower_numerator=c*t,exact_lower_denominator=D,
                      exact_column_inequalities=True,
                      excludes_population_3c=(t>3*D))
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int)
    p.add_argument('--seconds',type=float,default=40)
    p.add_argument('--method',choices=('highs','highs-ipm','highs-ds'),default='highs-ipm')
    p.add_argument('--out',required=True,type=Path)
    args=p.parse_args()
    result=generate(args.a,args.b,args.c,args.seconds,args.method)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    hidden={'endpoint_tables','up_remote_weights','down_remote_weights'}
    print(json.dumps({k:v for k,v in result.items() if k not in hidden},indent=2))


if __name__=='__main__':
    main()
