#!/usr/bin/env python3
"""Search positive integer periodic short-endpoint kernels of prescribed charge.

Any returned integer point is verified exactly. Solver status alone is not an
independent mathematical certificate. Periodic closure does not assert an
actual-cylinder lift, nonoverlap, board containment, or gate compatibility.
"""
from collections import Counter
import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_array

U = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def build(a,b,c):
    labels=[]; columns=[]; charges=[]
    rr=[]; cc=[]; vv=[]
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in (-1,1):
                    q=x,y
                    u=x-a*U[j][0],y-a*U[j][1]
                    w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
                    col=Counter()
                    for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                        col[(axis%3)*c*c+(p[0]%c)*c+p[1]%c]+=v
                    col={r:v for r,v in col.items() if v}
                    k=len(labels); labels.append((x,y,j,s)); columns.append(col)
                    eps=s*(-1)**j; charges.append(eps)
                    for r,v in col.items():rr.append(r);cc.append(k);vv.append(v)
                    rr.append(3*c*c);cc.append(k);vv.append(eps)
                    rr.append(3*c*c+1);cc.append(k);vv.append(1)
    mat=coo_array((np.array(vv,dtype=float),(np.array(rr,dtype=np.int32),np.array(cc,dtype=np.int32))),shape=(3*c*c+2,len(labels))).tocsc()
    return labels,columns,charges,mat


def run(a,b,c,charge,limit,seconds,binary=False,normalize=False):
    labels,cols,eps,A=build(a,b,c)
    n=len(labels)
    lo=np.zeros(A.shape[0]); hi=np.zeros(A.shape[0])
    lo[-2]=hi[-2]=charge; lo[-1]=abs(charge); hi[-1]=limit
    lb=np.zeros(n); ub=np.ones(n) if binary else np.full(n,limit)
    if normalize:lb[labels.index((0,0,0,1))]=1
    start=time.monotonic()
    result=milp(np.ones(n),integrality=np.ones(n),bounds=Bounds(lb,ub),constraints=LinearConstraint(A,lo,hi),options={'time_limit':seconds,'mip_rel_gap':0,'presolve':True})
    out={'tile':[a,b,c],'charge':charge,'population_limit':limit,'binary':binary,'normalized_positive_tile':normalize,'seconds':time.monotonic()-start,'status':int(result.status),'message':str(result.message),'objective':float(result.fun) if result.fun is not None else None,'dual_bound':float(result.mip_dual_bound) if getattr(result,'mip_dual_bound',None) is not None else None,'scope':__doc__.strip()}
    if result.x is not None:
        xx=np.rint(result.x).astype(np.int64)
        residual=Counter();support=[]
        for k,v in enumerate(xx):
            if v:
                support.append([*labels[k],int(v)])
                for r,d in cols[k].items():residual[r]+=int(v)*d
        exact=(not any(residual.values()) and sum(int(v)*e for v,e in zip(xx,eps))==charge and int(xx.sum())<=limit and np.all(xx>=lb) and np.all(xx<=ub))
        out.update({'support':support,'population':int(xx.sum()),'integer_endpoint_check':bool(exact),'maximum_rounding_error':float(np.max(np.abs(result.x-xx)))})
        if not exact:raise RuntimeError('Returned point failed exact verification')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('a','b','c'):p.add_argument(name,type=int)
    p.add_argument('--charge',type=int);p.add_argument('--limit',type=int)
    p.add_argument('--seconds',type=float,default=40)
    p.add_argument('--binary',action='store_true');p.add_argument('--normalize',action='store_true')
    p.add_argument('--out',type=Path,required=True)
    q=p.parse_args();o=run(q.a,q.b,q.c,q.charge or q.c,q.limit or 3*q.c-2,q.seconds,q.binary,q.normalize)
    q.out.write_text(json.dumps(o,indent=2)+'\n')
    print(json.dumps({k:v for k,v in o.items() if k!='support'},indent=2))
