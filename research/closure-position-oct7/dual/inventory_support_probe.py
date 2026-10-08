#!/usr/bin/env python3
"""Find and exactly replay signed inventory witnesses; not geometric tilings."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

def instance(L,U):
    heights=list(range(L,U+1));K=len(heights);d=5*K
    rows=[];rhs=[]
    for h in range(L-1,U+2):
        row=np.zeros(d,dtype=int)
        for i,k in enumerate(heights):
            # U=positive-positivechirality minus opposite rotations;
            # V=odd reflected rotations minus even reflected rotations.
            if h==k: row[4*i:4*i+4]+=[1,-1,1,-1]
            if h==k+1:row[4*i:4*i+2]+=[-13,13]
            if h==k-1:row[4*i+2:4*i+4]+=[-13,13]
        rows.append(row);rhs.append(154 if h==0 else 91 if abs(h)==1 else 0)
    for i,h in enumerate(heights):
        row=np.zeros(d,dtype=int);row[4*i:4*i+4]=1;row[4*K+i]=-13
        rows.append(row);rhs.append(11 if h==0 else 0)
    row=np.zeros(d,dtype=int);row[:4*K]=1;rows.append(row);rhs.append(154)
    A=np.array(rows);b=np.array(rhs);lo=np.zeros(d);hi=np.full(d,154.)
    for i,h in enumerate(heights):lo[4*K+i]=0 if h==0 else 1
    res=milp(np.zeros(d),integrality=np.ones(d),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,b,b),options={'time_limit':5})
    out={'support':[L,U],'solver_status':int(res.status)}
    if res.x is not None:
        x=np.rint(res.x).astype(np.int64)
        assert np.array_equal(A@x,b) and np.all(x>=lo) and np.all(x<=hi)
        out.update(exact_integer_witness=x.tolist(),height_counts=[int(sum(x[4*i:4*i+4])) for i in range(K)],exact_replay=True)
    return out

if __name__=='__main__':
    rows=[instance(L,L+K-1) for K in range(3,13) for L in range(1-K,1)]
    out={'scope':'FORMAL INVENTORIES ONLY; no positions or global gluing','supports':len(rows),'exact_witnesses':sum('exact_integer_witness' in r for r in rows),'records':rows}
    p=Path(__file__).with_name('inventory_supports.json');p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))
