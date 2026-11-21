#!/usr/bin/env python3
"""Exploratory one-coordinate integer projections; no tiling verdict."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def model(a,b,c,hand):
    labels=[]; rows=[]; cols=[]; vals=[]
    def f(q):
        x,y=q
        return (a*y-b*x if hand==1 else a*x-b*y)%c
    for t in range(c):
        q=(((-pow(b,-1,c)*t)%c,0) if hand==1 else ((pow(a,-1,c)*t)%c,0))
        assert f(q)==t
        for j in range(6):
            for s in (-1,1):
                eps=s*(-1 if j%2 else 1)
                u=(q[0]-a*U[j][0],q[1]-a*U[j][1])
                w=(q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1])
                k=len(labels);labels.append((t,j,s,f(u),eps))
                d=Counter()
                for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                    d[(axis%3)*c+f(p)]+=v
                if s==hand:d[3*c+f(u)]+=eps
                d[4*c+(eps<0)]+=1
                for r,v in d.items():
                    if v:rows.append(r);cols.append(k);vals.append(v)
    A=coo_matrix((vals,(rows,cols)),shape=(4*c+2,len(labels))).tocsc()
    rhs=np.zeros(4*c+2);rhs[3*c]=22 if hand==1 else 15;rhs[-2:]=[74,37]
    return A,rhs,labels

def run(seconds=20):
    out=[]
    for hand in (1,-1):
        A,b,labels=model(33,7,37,hand);t=time.monotonic()
        r=milp(np.zeros(len(labels)),integrality=np.ones(len(labels)),bounds=Bounds(0,74),constraints=LinearConstraint(A,b,b),options={'time_limit':seconds})
        data={'hand':hand,'status':int(r.status),'message':r.message,'seconds':time.monotonic()-t}
        if r.x is not None:
            x=np.rint(r.x).astype(np.int64);assert np.array_equal(A.astype(np.int64)@x,b.astype(np.int64))
            data['verified_integer_point']=True
            data['support']=[[*labels[k],int(v)] for k,v in enumerate(x) if v]
            data['maximum_multiplicity']=int(x.max())
        out.append(data)
    return {'scope':'Separate one-coordinate integer necessary projections, not a simultaneous two-coordinate point or physical tiling.','cases':out}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=20);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    d=run(a.seconds);a.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
