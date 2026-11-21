#!/usr/bin/env python3
"""Necessary contained height-one projection retaining first transverse moments.

Numerical exploratory probe only. An optimizer status is not a certificate.
The path frame is used; positive odd charge is c.
"""
from pathlib import Path
from collections import defaultdict
import argparse,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def ceildiv(a,b):return -((-a)//b)
def cross(a,b,o=(0,0)):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def hull(points):
    p=sorted(set(points))
    if len(p)<=2:return p
    lo=[];hi=[]
    for q in p:
        while len(lo)>1 and cross(lo[-1],q,lo[-2])<=0:lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(hi)>1 and cross(hi[-1],q,hi[-2])<=0:hi.pop()
        hi.append(q)
    return lo[:-1]+hi[:-1]

def build(a,b,c,additive=False):
    B=a*(a+2*b)
    # Coordinates are normalized by z, then multiplied by c.
    board=((0,0),(c*c*(a+b),-c*c*b),(B*a,B*b))
    inequalities=[]
    for p,q in zip(board,board[1:]+board[:1]):
        dx,dy=q[0]-p[0],q[1]-p[1]
        # Cross(q-p, c*(x,y)-p)>=0.
        inequalities.append((dy*c,-dx*c,dy*p[0]-dx*p[1]))
    xmin=ceildiv(min(p[0] for p in board),c);xmax=max(p[0] for p in board)//c
    ymin=ceildiv(min(p[1] for p in board),c);ymax=max(p[1] for p in board)//c
    labels=[];raw=0
    for j in range(6):
      for s in (-1,1):
        off=((0,0),(-a*U[j][0],-a*U[j][1]),(b*U[(j+s)%6][0],b*U[(j+s)%6][1]))
        ineq=[(p,q,r-max(p*x+q*y for x,y in off)) for p,q,r in inequalities]
        byres=defaultdict(list)
        for y in range(ymin,ymax+1):
            lo,hi=xmin,xmax
            for p,q,r in ineq:
                v=r-q*y
                if p>0:hi=min(hi,v//p)
                elif p<0:lo=max(lo,ceildiv(v,p))
                elif v<0:hi=lo-1;break
            if lo>hi:continue
            raw+=hi-lo+1
            for r in range(c):
                xx=lo+(r-lo)%c
                if xx>hi:continue
                zz=hi-(hi-r)%c
                byres[(r,y%c)].append((xx,y))
                if zz!=xx:byres[(r,y%c)].append((zz,y))
        for res,pts in byres.items():
            for x,y in hull(pts):labels.append((x,y,j,s))
    block=6*c if additive else 3*c*c
    nr=2*block+2*c
    ii=[];jj=[];vv=[]
    for col,(x,y,j,s) in enumerate(labels):
        eps=s*(-1 if j%2 else 1)
        u=(x-a*U[j][0],y-a*U[j][1]);w=(x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1])
        for axis,p,k in ((j,(x,y),s),(j,u,-s),(j+s,w,s),(j+s,(x,y),-s)):
            axis%=3
            rows=[axis*2*c+(a*p[1]-b*p[0])%c,axis*2*c+c+(a*p[0]-b*p[1])%c] if additive else [axis*c*c+(p[0]%c)*c+p[1]%c]
            transverse=(p[1],p[0],p[0]+p[1])[axis]
            for row in rows:
                ii.extend((row,row+block));jj.extend((col,col));vv.extend((k,k*transverse/c))
        gate=(a*u[1]-b*u[0])%c if s>0 else (a*u[0]-b*u[1])%c
        ii.append(2*block+(0 if s>0 else c)+gate);jj.append(col);vv.append(eps)
    A=coo_matrix((vv,(ii,jj)),shape=(nr,len(labels))).tocsc()
    A.sum_duplicates();A.eliminate_zeros()
    return A,labels,raw,board

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tile',nargs=3,type=int,default=(33,7,37));ap.add_argument('--f',type=int,default=2);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--additive',action='store_true')
    args=ap.parse_args();a,b,c=args.tile;t0=time.monotonic()
    A,labels,raw,board=build(a,b,c,args.additive)
    print(json.dumps({'stage':'matrix','rows':A.shape[0],'columns':A.shape[1],'nnz':A.nnz,'raw_placements':raw,'seconds':time.monotonic()-t0}),flush=True)
    rhs=np.zeros(A.shape[0]);rhs[-2*c]=2*c-(a-b)*args.f;rhs[-c]=-c+(a-b)*args.f
    t1=time.monotonic()
    result=linprog(np.ones(len(labels)),A_eq=A,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'time_limit':args.seconds})
    out={'tile':[a,b,c],'native_base_charge_units':args.f,'additive_endpoint_fields':args.additive,'scope':'Necessary continuous contained height-one model at native phase; exact supporting-line first moments retained. Solver output alone is not a certificate or a tiling.','rows':A.shape[0],'extreme_columns':A.shape[1],'raw_contained_placements':raw,'status':int(result.status),'message':result.message,'seconds':time.monotonic()-t1}
    if result.x is not None:
        out['population']=float(result.fun);out['maximum_residual']=float(np.max(np.abs(A@result.x-rhs)));out['support']=[list(labels[i])+[float(v)] for i,v in enumerate(result.x) if v>1e-9]
    if result.status==0:
        out['dual']=[float(x) for x in result.eqlin.marginals]
    args.out.write_text(json.dumps(out)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('support','dual')},indent=2),flush=True)
if __name__=='__main__':main()
