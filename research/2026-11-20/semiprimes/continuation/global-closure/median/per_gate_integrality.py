#!/usr/bin/env python3
"""All-residue necessary model for a hypothetical 3c odd population.

Placements have continuous nonnegative multiplicity. Exact-node signed
charges at the two families of neighboring gates are integer. This model
has no position box. Feasibility is not a geometric tiling.
"""
import argparse,json,time,math
from pathlib import Path
from collections import Counter
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def make_model(a,b,c):
    d=a-b;labels=[];ii=[];jj=[];vv=[];signs=[]
    base=3*c*c;signbase=base+2*c
    def row(j,p):return (j%3)*c*c+(p[0]%c)*c+p[1]%c
    for x in range(c):
        for y in range(c):
            q=x,y
            for j in range(6):
                for s in(-1,1):
                    eps=s*(-1 if j%2 else 1)
                    u=x-a*U[j][0],y-a*U[j][1]
                    w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
                    gate=(a*u[1]-b*u[0])%c if s>0 else (a*u[0]-b*u[1])%c
                    k=len(labels);labels.append((x,y,j,s,gate));signs.append(eps)
                    for axis,p,v in((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                        ii.append(row(axis,p));jj.append(k);vv.append(v)
                    ii.extend((base+(0 if s>0 else c)+gate,signbase+(eps<0)))
                    jj.extend((k,k));vv.extend((eps,1))
    nc=len(labels);lo=[0.0]*nc;hi=[float(2*c if eps>0 else c) for eps in signs]
    for hand in('up','down'):
        for gate in range(c):
            k=len(lo);rownum=base+(0 if hand=='up' else c)+gate
            ii.append(rownum);jj.append(k);vv.append(-d)
            offset=(2*c if hand=='up' else -c) if gate==0 else 0
            lo.append(math.ceil((-c-offset)/d));hi.append(math.floor((2*c-offset)/d))
    nr=signbase+2
    A=coo_matrix((vv,(ii,jj)),shape=(nr,len(lo))).tocsc()
    rhs=np.zeros(nr);rhs[base]=2*c;rhs[base+c]=-c;rhs[-2:]=[2*c,c]
    integrality=np.r_[np.zeros(nc),np.ones(2*c)]
    return A,rhs,np.asarray(lo),np.asarray(hi),integrality,labels

def run(a,b,c,seconds):
    A,rhs,lo,hi,integ,labels=make_model(a,b,c);t=time.monotonic()
    res=milp(np.zeros(len(lo)),integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,rhs,rhs),options={'time_limit':seconds,'mip_rel_gap':0.0})
    out={'tile':[a,b,c],'odd_population':3*c,'rows':A.shape[0],'continuous_placement_columns':len(labels),'integer_gate_charges':2*c,'status':int(res.status),'message':res.message,'seconds':time.monotonic()-t,'scope':'All-residue necessary relaxation with continuous tile multiplicities and integer actual-node charges; feasibility is not a geometric tiling, numerical infeasibility is not an exported exact proof.'}
    if getattr(res,'mip_node_count',None) is not None:out['mip_nodes']=int(res.mip_node_count)
    if res.x is not None:
        x=res.x;nc=len(labels)
        out['maximum_equality_residual']=float(np.max(abs(A@x-rhs)))
        out['maximum_gate_integrality_error']=float(np.max(abs(x[nc:]-np.rint(x[nc:]))))
        out['up_gate_charges']=np.rint(x[nc:nc+c]).astype(int).tolist()
        out['down_gate_charges']=np.rint(x[nc+c:]).astype(int).tolist()
        out['support']=[list(labels[i])+[float(v)] for i,v in enumerate(x[:nc]) if v>1e-8]
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--seconds',type=float,default=60);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    out=run(args.a,args.b,args.c,args.seconds);args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='support'}),flush=True)
