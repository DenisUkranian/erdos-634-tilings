#!/usr/bin/env python3
"""Integer cylinder with actual nonoverlap discovery, finite hexagon scope."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def vertices(a,b,label):
    x,y,j,s=label[:4];u=(x-a*U[j][0],y-a*U[j][1]);w=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
    return ((x,y),w,u) if s==1 else ((x,y),u,w)

def overlap(A,B):
    for P in (A,B):
        for i in range(3):
            p=P[i];q=P[(i+1)%3];d=(q[0]-p[0],q[1]-p[1])
            aa=[d[0]*v[1]-d[1]*v[0] for v in A];bb=[d[0]*v[1]-d[1]*v[0] for v in B]
            if max(aa)<=min(bb) or max(bb)<=min(aa):return False
    return True

def run(a,b,c,radius,blocks,seconds,rounds,gate_parity):
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
                    for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):d[row(axis,p)]+=v
                    for n,v in d.items():
                        if v:rr.append(n);cc.append(k);vv.append(v)
    n=len(labels);base=len(rid);extra=2+2*c if gate_parity else 2;cols=n+2*c if gate_parity else n
    for k,label in enumerate(labels):
        x,y,j,s,eps=label;rr.append(base+(eps<0));cc.append(k);vv.append(1)
        if gate_parity:
            u=x-a*U[j][0],y-a*U[j][1];gate=(a*u[1]-b*u[0])%c if s==1 else (a*u[0]-b*u[1])%c
            rr.append(base+2+(0 if s==1 else c)+gate);cc.append(k);vv.append(eps)
    if gate_parity:
        for k in range(2*c):rr.append(base+2+k);cc.append(n+k);vv.append(-(a-b))
    A=coo_matrix((vv,(rr,cc)),shape=(base+extra,cols)).tocsc()
    rhs=np.zeros(base+extra);rhs[base:base+2]=[(blocks+1)*c//2,(blocks-1)*c//2]
    if gate_parity:rhs[base+2]=2*c;rhs[base+2+c]=-c
    polygons=[vertices(a,b,p) for p in labels];P=np.asarray(polygons,dtype=np.int64)
    points=np.unique(P.sum(axis=1),axis=0)
    pr=[];pc=[]; rown=0;seen=set()
    for point in points:
        v=point[None,None,:]-3*P;edges=np.roll(P,-1,axis=1)-P
        inside=np.all(edges[:,:,0]*v[:,:,1]-edges[:,:,1]*v[:,:,0]>0,axis=1)
        idx=tuple(np.flatnonzero(inside).tolist())
        if len(idx)>1 and idx not in seen:
            seen.add(idx);pr.extend([rown]*len(idx));pc.extend(idx);rown+=1
    C=coo_matrix((np.ones(len(pr)),(pr,pc)),shape=(rown,cols)).tocsc()
    lo=np.r_[np.zeros(n),np.full(cols-n,-blocks*c)];hi=np.r_[np.ones(n),np.full(cols-n,blocks*c)]
    out={'tile':[a,b,c],'anchor_radius':radius,'odd_blocks':blocks,'gate_congruences':gate_parity,'columns':cols,'cylinder_rows':base,'initial_point_cliques':rown,'scope':'Finite hexagon anchor pool. An exact accepted point is a real nonoverlapping partial packing with cylinder equations, not a full tiling. Infeasibility has only finite-pool scope.','rounds':[]}
    start=time.monotonic()
    for step in range(rounds):
        res=milp(np.zeros(cols),integrality=np.ones(cols),bounds=Bounds(lo,hi),constraints=[LinearConstraint(A,rhs,rhs),LinearConstraint(C,0,1)],options={'time_limit':seconds})
        record={'round':step,'status':int(res.status),'message':res.message,'point_cliques_and_pair_cuts':C.shape[0]};out['rounds'].append(record)
        print(json.dumps(record),flush=True)
        if res.x is None:break
        x=np.rint(res.x).astype(np.int64);assert np.array_equal(A.astype(np.int64)@x,rhs.astype(np.int64));assert np.all(C@x<=1)
        support=np.flatnonzero(x[:n]);bad=[]
        for i,k in enumerate(support):
            for l in support[i+1:]:
                if overlap(polygons[k],polygons[l]):bad.append((int(k),int(l)))
        record['overlapping_pairs']=len(bad)
        if not bad:
            out['exact_nonoverlapping_integer_point']=True;out['support']=[labels[k] for k in support];out['gate_charge_units']=x[n:].tolist();break
        br=[];bc=[]
        for k,(i,j) in enumerate(bad):br.extend([k,k]);bc.extend([i,j])
        C=vstack([C,coo_matrix((np.ones(len(br)),(br,bc)),shape=(len(bad),cols))]).tocsc()
    out['seconds']=time.monotonic()-start
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--radius',type=int,required=True);p.add_argument('--blocks',type=int,default=3);p.add_argument('--seconds',type=float,default=60);p.add_argument('--rounds',type=int,default=10);p.add_argument('--gate-congruences',action='store_true');p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    out=run(args.a,args.b,args.c,args.radius,args.blocks,args.seconds,args.rounds,args.gate_congruences);args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='support'},indent=2))
