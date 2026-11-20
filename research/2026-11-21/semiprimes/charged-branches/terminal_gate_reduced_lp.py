#!/usr/bin/env python3
"""One-residue version of the isolated-gate diagnostic LP.

This generator uses fewer rows by taking endpoint functions of psi only.
The saved dual is lifted to full two-coordinate tables for the independent
integer verifier. A primal below is a fractional residue witness only.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix,coo_matrix,hstack,vstack

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def generate(a,b,c,return_model=False):
    psi=lambda p:(a*p[0]-b*p[1])%c
    labels=[];ii=[];jj=[];vv=[]
    for r in range(c):
        for j in range(6):
            for s in (-1,1):
                gate=(r-a*psi(U[j]))%c
                k=len(labels);labels.append((r,j,s,gate))
                for axis,rr,value in ((j,r,s),(j,r-a*psi(U[j]),-s),(j+s,r+b*psi(U[(j+s)%6]),s),(j+s,r,-s)):
                    ii.append((axis%3)*c+rr%c);jj.append(k);vv.append(value)
    endpoint=coo_matrix((vv,(ii,jj)),shape=(3*c,len(labels))).tocsc()
    index={label[:3]:k for k,label in enumerate(labels)}
    singles=[k for k,label in enumerate(labels) if label[2]==-1 and label[3]==0]
    pairs=[]
    for k,(r,j,s,gate) in enumerate(labels):
        mate_r=(r-a*psi(U[j])+b*psi(U[(j+s)%6]))%c
        l=index[mate_r,(j+3)%6,s]
        if k<l:pairs.append((k,l))
    paircols=endpoint[:,[k for k,l in pairs]]+endpoint[:,[l for k,l in pairs]]
    A=hstack([endpoint[:,singles],paircols],format='csc')
    charge=np.r_[[(-1 if labels[k][1]%2==0 else 1) for k in singles],np.zeros(len(pairs))]
    A=vstack([A,csc_matrix(charge.reshape(1,-1))],format='csc')
    rhs=np.r_[np.zeros(3*c),c]
    objective=np.r_[np.ones(len(singles)),np.repeat(2.,len(pairs))]
    if return_model:
        return A,rhs,objective,labels,singles,pairs
    start=time.monotonic()
    result=linprog(objective,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs-ds')
    out={'tile':[a,b,c],'status':int(result.status),'message':result.message,'seconds':time.monotonic()-start,'scope':__doc__,'rows':A.shape[0],'single_columns':len(singles),'paired_columns':len(pairs)}
    if result.status!=0:return out
    out['floating_population']=float(result.fun)
    expected_D=13 if c==43 else 506
    dual=np.rint(result.eqlin.marginals*expected_D).astype(np.int64)
    scores=A.T@dual
    D=max(expected_D,int(max(scores[:len(singles)])),int(max(np.ceil(scores[len(singles):]/2))))
    assert np.all(scores<=objective*D)
    tab=dual[:-1].reshape(3,c)
    tables=[[[int(tab[j,psi((x,y))]) for y in range(c)] for x in range(c)] for j in range(3)]
    out.update(D=D,charge_multiplier=int(dual[-1]),endpoint_tables=tables,reduced_endpoint_tables=tab.tolist(),exact_lower_numerator=c*int(dual[-1]),exact_lower_denominator=D)
    primal=[Fraction(float(v)).limit_denominator(1000000) for v in result.x]
    sums=[Fraction(0)]*A.shape[0]
    coo=A.tocoo()
    for row,col,value in zip(coo.row,coo.col,coo.data):
        sums[row]+=int(value)*primal[col]
    if all(value==int(target) for value,target in zip(sums,rhs)) and all(v>=0 for v in primal):
        population=sum((1 if i<len(singles) else 2)*v for i,v in enumerate(primal))
        support=[]
        for i,v in enumerate(primal):
            if not v:continue
            indices=[singles[i]] if i<len(singles) else list(pairs[i-len(singles)])
            support.append([[list(labels[k]) for k in indices],v.numerator,v.denominator])
        out.update(exact_periodic_primal_population=str(population),exact_periodic_primal_blocks=str(population/c),periodic_primal_support=support)
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--out',required=True,type=Path);args=p.parse_args()
    out=generate(args.a,args.b,args.c);args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('endpoint_tables','reduced_endpoint_tables','periodic_primal_support')},indent=2))
