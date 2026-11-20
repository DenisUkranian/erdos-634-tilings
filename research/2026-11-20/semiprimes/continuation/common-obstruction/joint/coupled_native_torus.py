#!/usr/bin/env python3
"""Two native meshes, periodic endpoints and line currents, all CRT gate couplings.
Scope: short heights1,2 with vertices in zR,z^2R respectively. Not global.
"""
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
from verify_native_torus import U,events,pair_events,gate,root,add,mul

def line(axis,q,c):return(q[1]if axis==0 else q[0]if axis==1 else q[0]+q[1])%c

def build(a,b,c):
    local=3*c*c+3*c;flowstart=2*local;signstart=flowstart+12
    def row_endpoint(h,axis,q):return(h-1)*local+axis*c*c+q[0]*c+q[1]
    def row_line(h,axis,t):return(h-1)*local+3*c*c+axis*c+t
    def short(h,j,s,q):
        es=[(row_endpoint(h,axis,p),v)for(axis,p),v in events(a,b,c,j,s,q)]
        for J,L in((j,a),((j+s)%6,b)):
            es.append((row_line(h,J%3,line(J%3,q,c)),s*(1 if J<3 else-1)*L))
        return es
    def pair(h,j,s,q):
        mate=add(add(q,mul(-a,U[j],c),c),mul(b,U[(j+s)%6],c),c)
        return short(h,j,s,q)+short(h,(j+3)%6,s,mate)
    def ingress(h,j,q):
        u=add(q,mul(-a,U[j],c),c);r=root(a,b,c)
        if h==2:r=(1-r)%c
        return(u[0]+r*u[1])%c==0
    columns=[];cost=[];labels=[]
    for h,s in((1,1),(2,-1)):
        for j in range(6):
            flow=flowstart+(h-1)*6+j
            for x in range(c):
                for y in range(c):
                    q=x,y
                    if ingress(h,j,q):
                        columns.append(short(h,j,s,q)+[(flow,1),(signstart+h-1,s*(-1)**j)])
                        cost.append(1);labels.append(('gate_short',h,j,q))
            for t in range(c):
                columns.append([(row_line(3-h,j%3,t),-s*(1 if j<3 else-1)*c),(flow,-1)])
                cost.append(0);labels.append(('gate_long',h,j,t))
    for h in(1,2):
        for s in(-1,1):
            for j in range(3):
                for x in range(c):
                    for y in range(c):
                        columns.append(pair(h,j,s,(x,y)));cost.append(2);labels.append(('pair',h,j,s,(x,y)))
    rhs=np.zeros(signstart+2,dtype=np.int64)
    # Fixed negative-sign h1 teeth on the entire base.
    for i in range(c):
        q=((i*(a+b)+a)%c,(-i*b)%c)
        for r,v in short(1,0,-1,q):rhs[r]-=v
    # Remaining native boundary in h2 coordinates: B=(ap,-bq), C=(ap,0), O=0.
    A=a*(a+2*b);B=b*(2*a+b);X=(A%c,(-B)%c);Y=(A%c,0);O=(0,0)
    for P,Q,J,L in((X,Y,1,B),(Y,O,3,A)):
        rhs[row_endpoint(2,J%3,P)]-=1;rhs[row_endpoint(2,J%3,Q)]+=1
        rhs[row_line(2,J%3,line(J%3,P,c))]+=(1 if J<3 else-1)*L
    rhs[signstart]=2*c;rhs[signstart+1]=a-b
    entries=[(i,j,v)for j,es in enumerate(columns)for i,v in es]
    ii,jj,vv=zip(*entries);matrix=coo_matrix((vv,(ii,jj)),shape=(len(rhs),len(columns))).tocsc()
    return matrix,rhs,np.array(cost),labels,{'local_rows':local,'flowstart':flowstart,'signstart':signstart}

def solve(a,b,c,seconds=120):
    matrix,rhs,cost,labels,meta=build(a,b,c);start=time.monotonic()
    res=linprog(cost,A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs',options={'time_limit':seconds})
    record={'tile':[a,b,c],'rows':matrix.shape[0],'columns':matrix.shape[1],'nonzeros':matrix.nnz,'status':res.status,'message':res.message,'seconds':round(time.monotonic()-start,3),'N':(a+2*b)*(2*a+b),'scope':'Native short heights1,2 and native meshes zR,z^2R only; no unrestricted conclusion.'}
    if res.success:
        n=[0.,0.]
        for t,x in zip(labels,res.x):
            if t[0]=='gate_short':n[t[1]-1]+=x
            elif t[0]=='pair':n[t[1]-1]+=2*x
        n[0]+=c
        record.update(minimum_total=float(res.fun+c),height_populations=n,positive_columns=int(np.count_nonzero(res.x>1e-7)))
    print(json.dumps(record),flush=True)
    return res,labels,record,meta
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('sides',type=int,nargs=3);p.add_argument('--seconds',type=float,default=120);p.add_argument('--out');args=p.parse_args()
    res,labels,record,meta=solve(*args.sides,seconds=args.seconds)
    if args.out:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True);(out/'status.json').write_text(json.dumps(record,indent=2)+'\n')
        if res.success:
            (out/'primal.json').write_text(json.dumps([(t,float(x))for t,x in zip(labels,res.x)if x>1e-8],separators=(',',':'))+'\n')
            (out/'dual.json').write_text(json.dumps({'meta':meta,'weights':res.eqlin.marginals.tolist()},separators=(',',':'))+'\n')
