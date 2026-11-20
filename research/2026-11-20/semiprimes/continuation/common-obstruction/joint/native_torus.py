#!/usr/bin/env python3
"""Finite residue projection for native two-height F2 tilings, no geometry catalogue.
No result from this program alone proves unrestricted nonexistence.
"""
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog

UNITS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
def solve(a,b,c, gate=True, sign=True):
    assert c*c==a*a+a*b+b*b
    roots=[r for r in range(c)if(r*r-r+1)%c==0]
    root=next(r for r in roots if(a+b*r)%c==0)
    def plus(p,q):return((p[0]+q[0])%c,(p[1]+q[1])%c)
    def times(k,p):return(k*p[0]%c,k*p[1]%c)
    def index(j,p):return(j%3)*c*c+p[0]*c+p[1]
    def col(j,s,q):
        u=plus(q,times(-a,UNITS[j]));w=plus(q,times(b,UNITS[(j+s)%6]))
        return[(index(j,q),s),(index(j,u),-s),(index(j+s,w),s),(index(j+s,q),-s)]
    def pair(j,s,q):
        qq=plus(plus(q,times(-a,UNITS[j])),times(b,UNITS[(j+s)%6]))
        return col(j,s,q)+col((j+3)%6,s,qq)
    def in_gate(q,j):
        u=plus(q,times(-a,UNITS[j]));return(u[0]+root*u[1])%c==0
    columns=[];cost=[];eps=[];labels=[]
    points=[(x,y)for x in range(c)for y in range(c)]
    for j in range(6):
        for q in points:
            if not gate or in_gate(q,j):
                columns.append(col(j,1,q));cost.append(1);eps.append((-1)**j);labels.append(('up',j,q))
    for s in (-1,1):
        if not gate and s==1:continue
        for j in range(3):
            for q in points:
                columns.append(pair(j,s,q));cost.append(2);eps.append(0);labels.append(('pair',j,s,q))
    rhs=np.zeros(3*c*c+(1 if sign else 0))
    for i in range(c):
        q=((i*(a+b)+a)%c,(-i*b)%c)
        for r,v in col(0,-1,q):rhs[r]-=v
    if sign:rhs[-1]=2*c
    entries=[(i,j,n)for j,cl in enumerate(columns)for i,n in cl]
    if sign:entries.extend((3*c*c,j,v)for j,v in enumerate(eps)if v)
    ii,jj,nn=zip(*entries);matrix=coo_matrix((nn,(ii,jj)),shape=(len(rhs),len(columns))).tocsc()
    start=time.monotonic()
    res=linprog(cost,A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs')
    record={'tile':[a,b,c],'gate':gate,'sign':sign,'rows':len(rhs),'columns':len(cost),'status':res.status,'message':res.message,'seconds':round(time.monotonic()-start,3),'scope':'Native h1 mesh zR and h2 core mesh z^2R; finite endpoint-residue projection, not unrestricted tilings.'}
    if res.success:
        record.update(minimum_h1=float(res.fun+c),N=(a+2*b)*(2*a+b),positive_columns=int(np.count_nonzero(res.x>1e-7)),integrality_error=float(np.max(np.abs(res.x-np.rint(res.x)))))
    print(json.dumps(record),flush=True)
    return res,matrix,rhs,cost,labels,record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('sides',type=int,nargs=3);p.add_argument('--no-gate',action='store_true');p.add_argument('--no-sign',action='store_true');p.add_argument('--out');args=p.parse_args()
    res,m,rhs,cost,labels,record=solve(*args.sides,gate=not args.no_gate,sign=not args.no_sign)
    if args.out:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
        (out/'status.json').write_text(json.dumps(record,indent=2)+'\n')
        if res.success:
            (out/'primal.json').write_text(json.dumps([(label,float(w))for label,w in zip(labels,res.x)if w>1e-8],separators=(',',':'))+'\n')
            (out/'dual.json').write_text(json.dumps(res.eqlin.marginals.tolist(),separators=(',',':'))+'\n')
