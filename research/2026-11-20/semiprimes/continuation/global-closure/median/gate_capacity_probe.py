#!/usr/bin/env python3
"""One-prime endpoint gate capacity for arbitrary native h1 populations."""
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from extreme_gate_quotient import U

def model(a,b,c):
    labs=[];ii=[];jj=[];vv=[]
    phi=lambda p:(a*p[1]-b*p[0])%c
    def row(j,p):return (j%3)*c+phi(p)
    for r in range(c):
        q=((-pow(b,-1,c)*r)%c,0)
        for j in range(6):
            for s in (-1,1):
                eps=s*(-1 if j%2 else 1)
                u=q[0]-a*U[j][0],q[1]-a*U[j][1]
                w=q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1]
                gate=s==1 and phi(u)==0
                k=len(labs);labs.append((r,j,s,eps,gate))
                for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                    ii.append(row(axis,p));jj.append(k);vv.append(v)
                ii.append(3*c+(eps<0));jj.append(k);vv.append(1)
    A=coo_matrix((vv,(ii,jj)),shape=(3*c+2,len(labs))).tocsc()
    return A,labs

def probe(a,b,c):
    A,labs=model(a,b,c);rhs=np.zeros(A.shape[0]);rhs[-2:]=[2*c,c]
    cost=np.array([-1 if eps>0 and gate else 0 for r,j,s,eps,gate in labs])
    res=linprog(cost,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs')
    out={'tile':[a,b,c],'rows':A.shape[0],'columns':A.shape[1],'status':int(res.status)}
    if res.x is not None:
        out['maximum_positive_native_up_gate_population']=float(-res.fun)
        out['dual_sign_coefficients']=(-res.eqlin.marginals[-2:]).tolist()
        out['dual']=(-res.eqlin.marginals).tolist()
        out['support']=[list(labs[i])+[float(x)] for i,x in enumerate(res.x) if x>1e-8]
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    r=probe(args.a,args.b,args.c);args.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('support','dual')}))
