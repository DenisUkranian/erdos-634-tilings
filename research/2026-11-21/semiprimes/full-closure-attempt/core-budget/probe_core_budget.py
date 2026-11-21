#!/usr/bin/env python3
"""Discover exact periodic lower bounds for the exceptional native even core.

Conditional on the one odd native mesh and short heights 0,1,2.
Numerical discovery is not a target nonexistence certificate.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'research/2026-11-20/semiprimes/continuation/global-closure/median'))
from per_gate_integrality import make_model,U


def generate(a,b,c,g,seconds):
    original,*rest=make_model(a,b,c)
    labels=rest[-1];n=len(labels);base=3*c*c
    endpoints=original[:base,:n]
    index={tuple(label[:4]):k for k,label in enumerate(labels)}
    singles=[k for k,label in enumerate(labels) if label[3]==-1 and label[4]==0]
    pairs=[]
    for k,(x,y,j,s,gate) in enumerate(labels):
        xp=(x-a*U[j][0]+b*U[(j+s)%6][0])%c
        yp=(y-a*U[j][1]+b*U[(j+s)%6][1])%c
        other=index[xp,yp,(j+3)%6,s]
        if k<other:pairs.append((k,other))
    A=hstack([endpoints[:,singles],endpoints[:,[k for k,l in pairs]]+endpoints[:,[l for k,l in pairs]]],format='csc')
    charge=np.r_[[labels[k][3]*(-1)**labels[k][2] for k in singles],np.zeros(len(pairs))]
    A=vstack([A,csc_matrix(charge.reshape(1,-1))],format='csc')
    rhs=np.zeros(base+1,dtype=np.int64)
    # Path board / z^2 has vertices 0,(B,-A),(B,0).
    aa=b*(2*a+b);bb=a*(a+2*b)
    for ax,p,val in ((1,(bb,0),1),(1,(bb,-aa),-1),(0,(0,0),1),(0,(bb,0),-1)):
        rhs[ax*c*c+(p[0]%c)*c+p[1]%c]+=val
    rhs[-1]=a-b+c*g
    objective=np.r_[np.ones(len(singles)),2*np.ones(len(pairs))]
    start=time.monotonic()
    res=linprog(objective,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'time_limit':seconds})
    out=dict(tile=[a,b,c],native_charge_units=g,charge=int(rhs[-1]),status=int(res.status),message=str(res.message),seconds=time.monotonic()-start,scope=__doc__)
    if res.x is not None:out.update(population=float(res.fun),max_residual=float(np.max(np.abs(A@res.x-rhs))))
    if res.success:
        scale=10**8
        dual=np.rint(res.eqlin.marginals*scale).astype(np.int64)
        scores=np.asarray(A.T@dual,dtype=np.int64)
        D=max(1,int(max(scores[:len(singles)])),int(max((scores[len(singles):]+1)//2)))
        assert np.all(scores<=objective*D)
        out.update(denominator=D,numerator=int(rhs@dual),endpoint_weights=dual[:base].tolist(),charge_weight=int(dual[-1]),rhs_nonzero=[[i,int(v)] for i,v in enumerate(rhs) if v])
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('g',type=int)
    p.add_argument('--seconds',type=float,default=60);p.add_argument('--out',type=Path,required=True)
    q=p.parse_args();out=generate(q.a,q.b,q.c,q.g,q.seconds);q.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='endpoint_weights'},indent=2),flush=True)
