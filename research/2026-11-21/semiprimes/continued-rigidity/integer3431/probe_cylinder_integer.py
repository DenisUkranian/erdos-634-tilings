#!/usr/bin/env python3
"""Finite-window integer cylinder diagnostic; UNSAT has only window scope."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def run(a,b,c,radius,blocks,seconds):
    rid={};rr=[];cc=[];vv=[];labels=[]
    def row(axis,p):
        x,y=p;axis%=3
        key=(axis,y,x%c) if axis==0 else ((axis,x,y%c) if axis==1 else (axis,x+y,y%c))
        return rid.setdefault(key,len(rid))
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            if abs(x+y)>radius:continue
            q=x,y
            for j in range(6):
                for s in (-1,1):
                    k=len(labels);labels.append((x,y,j,s,s*(-1 if j%2 else 1)))
                    u=(x-a*U[j][0],y-a*U[j][1]);w=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
                    d=Counter()
                    for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                        d[row(axis,p)]+=v
                    for n,v in d.items():
                        if v:rr.append(n);cc.append(k);vv.append(v)
    base=len(rid)
    for k,label in enumerate(labels):rr.append(base+(label[-1]<0));cc.append(k);vv.append(1)
    A=coo_matrix((vv,(rr,cc)),shape=(base+2,len(labels))).tocsc()
    rhs=np.zeros(base+2);rhs[-2:]=[(blocks+1)*c//2,(blocks-1)*c//2]
    start=time.monotonic();res=milp(np.zeros(len(labels)),integrality=np.ones(len(labels)),bounds=Bounds(0,1),constraints=LinearConstraint(A,rhs,rhs),options={'time_limit':seconds})
    out={'tile':[a,b,c],'anchor_radius':radius,'odd_blocks':blocks,'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,'columns':len(labels),'rows':base+2,'scope':'Finite-window Boolean actual placements with cylinder currents, not full endpoint currents. No containment board or interior disjointness. Infeasibility cannot exclude an unrestricted target.'}
    if res.x is not None:
        x=np.rint(res.x).astype(np.int64);assert np.array_equal(A.astype(np.int64)@x,rhs.astype(np.int64));assert np.all((x==0)|(x==1))
        out['verified_integer_point']=True;out['support']=[labels[k] for k,v in enumerate(x) if v]
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--radius',type=int,required=True);p.add_argument('--blocks',type=int,default=3);p.add_argument('--seconds',type=float,default=30);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    out=run(args.a,args.b,args.c,args.radius,args.blocks,args.seconds);args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
