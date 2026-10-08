#!/usr/bin/env python3
"""MILP exploration of all directional length inventories, exact witness replay.

Only a replayed feasible inventory is a certificate here. Solver failures or
infeasibility messages are exploratory until separately certified.
"""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

def instance(L,U):
    H=list(range(L,U+1));K=len(H);d=13*K
    keys=[(h,j) for h in range(L-1,U+2) for j in range(3)]
    rows={key:i for i,key in enumerate(keys)}
    A=np.zeros((len(keys)+K+1,d),dtype=np.int64);b=np.zeros(len(A),dtype=np.int64)
    for h,j,le in [(0,0,154),(1,2,91),(-1,4,91)]:b[rows[h,j%3]]+=(1 if j<3 else -1)*le
    for i,h in enumerate(H):
        for t,(x,y) in enumerate([(8,7),(7,8)]):
            for j in range(6):
                col=12*i+6*t+j
                ed=[(h,j,x),(h-1,j+3,13),(h,j+5,y)] if t==0 else [(h,j,x),(h+1,j+2,13),(h,j+5,y)]
                for eh,ej,le in ed:
                    ej%=6;A[rows[eh,ej%3],col]+=(1 if ej<3 else -1)*le
        A[len(keys)+i,12*i:12*i+12]=1;A[len(keys)+i,12*K+i]=-13;b[len(keys)+i]=11 if h==0 else 0
    A[-1,:12*K]=1;b[-1]=154
    lo=np.zeros(d);hi=np.full(d,154.)
    for i,h in enumerate(H):lo[12*K+i]=0 if h==0 else 1
    r=milp(np.zeros(d),integrality=np.ones(d),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,b,b),options={'time_limit':4})
    out={'support':[L,U],'solver_status':int(r.status)}
    if r.x is not None:
        x=np.rint(r.x).astype(np.int64);assert np.array_equal(A@x,b) and np.all(x>=lo) and np.all(x<=hi)
        out.update(exact_replay=True,inventory=[{'h':h,'counts':x[12*i:12*i+12].tolist()} for i,h in enumerate(H)])
    return out

if __name__=='__main__':
    exact=json.loads(Path(__file__).with_name('inventory_exact.json').read_text())
    rows=[]
    for r in exact['records']:
        if r['status']=='EXACT_FORMAL_WITNESS':
            out=instance(*r['support']);rows.append(out)
            print(json.dumps({k:v for k,v in out.items() if k!='inventory'}),flush=True)
    out={'scope':'FULL DIRECTION INVENTORIES; NO POSITIONAL OR GLUING SUFFICIENCY','supports':len(rows),'exact_witnesses':sum('exact_replay' in r for r in rows),'records':rows}
    Path(__file__).with_name('full_direction_inventory.json').write_text(json.dumps(out,indent=2)+'\n')
