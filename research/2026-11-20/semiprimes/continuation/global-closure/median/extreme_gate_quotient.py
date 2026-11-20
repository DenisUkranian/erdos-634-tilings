#!/usr/bin/env python3
"""One-prime quotient of the saturated actual upper path K=2c.

Certificate inequalities apply to every native h1 placement, with no box.
"""
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def model(a,b,c):
    labels=[];ii=[];jj=[];vv=[]
    phi=lambda p:(a*p[1]-b*p[0])%c
    def row(j,p):return (j%3)*c+phi(p)
    for r in range(c):
        q=((-pow(b,-1,c)*r)%c,0)
        for j in range(6):
            for s in (-1,1):
                eps=s*(-1 if j%2 else 1)
                u=q[0]-a*U[j][0],q[1]-a*U[j][1]
                w=q[0]+b*U[(j+s)%6][0],q[1]+b*U[(j+s)%6][1]
                if eps>0:
                    if s<0 or phi(u):continue
                    cat=0
                else:cat=1 if s>0 else 2
                k=len(labels);labels.append((r,j,s,cat))
                for axis,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
                    ii.append(row(axis,p));jj.append(k);vv.append(v)
    A=coo_matrix((vv,(ii,jj)),shape=(3*c,len(labels))).tocsc()
    categories=np.array([label[-1] for label in labels])
    return A,categories,labels

def solve(a,b,c,x):
    A,cats,labs=model(a,b,c);nr,nc=A.shape
    counts=np.array([2*c,(a-b)*x,c-(a-b)*x])
    # Farkas dual: A.T f + C_category >= 0, minimize counts.C.
    B=np.zeros((nc,nr+3));B[:,:nr]=-A.T.toarray()
    for i,cat in enumerate(cats):B[i,nr+cat]=-1
    cost=np.r_[np.zeros(nr),counts]
    res=linprog(cost,A_ub=B,b_ub=np.zeros(nc),bounds=[(-1,1)]*nr+[(None,None)]*3,method='highs')
    report={'tile':[a,b,c],'x':x,'rows':nr,'classes':nc,'status':int(res.status),'message':res.message,'scope':'All-residue necessary projection; no geometric realization claimed.'}
    if res.x is not None:
        report['dual_objective']=float(res.fun)
        f=np.rint(res.x[:nr]*1000000).astype(np.int64)
        vals=np.asarray(A.T@f,dtype=np.int64)
        C=np.array([max(-vals[cats==i]) for i in range(3)],dtype=np.int64)
        exact=bool(np.all(vals+C[cats]>=0))
        deficit=int(counts@C)
        report.update(exact_inequalities=exact,exact_weighted_count=deficit,
                      certificate={'endpoint_tables':f.reshape(3,c).tolist(),'category_bounds':C.tolist(),'counts':counts.tolist()})
        report['exclusion_certificate']=bool(exact and deficit<0)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('x',type=int);p.add_argument('--out',required=True,type=Path);args=p.parse_args()
    r=solve(args.a,args.b,args.c,args.x);args.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='certificate'}),flush=True)
