#!/usr/bin/env python3
"""Two marginal endpoint projection of the complete residue model.

One phi and one psi marginal per orientation; equate their totals.
This is a necessary continuous relaxation, not a geometric tiling model.
"""
from pathlib import Path
from collections import defaultdict
import argparse,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def make(a,b,c):
    shapes=[(j,s) for j in range(6) for s in [-1,1]]
    coeff=[(-b,a),(a,-b)];nc=24*c;ii=[];jj=[];vv=[]
    gatebase=6*c;shapebase=gatebase+2*c
    def put(row,col,val):
        if val:ii.append(row);jj.append(col);vv.append(val)
    for kind,(lx,ly) in enumerate(coeff):
        for k,(j,s) in enumerate(shapes):
            eps=s*(-1)**j;u=(-a*U[j][0],-a*U[j][1]);w=(b*U[(j+s)%6][0],b*U[(j+s)%6][1])
            du=(lx*u[0]+ly*u[1])%c;dw=(lx*w[0]+ly*w[1])%c
            for r in range(c):
                col=(kind*12+k)*c+r
                for axis,t,val in [(j,r,s),(j,r+du,-s),(j+s,r+dw,s),(j+s,r,-s)]:
                    put(kind*3*c+(axis%3)*c+t%c,col,val)
                if (kind==0 and s>0) or (kind==1 and s<0):
                    put(gatebase+kind*c+(r+du)%c,col,eps)
                put(shapebase+k,col,1 if kind==0 else -1)
    M=coo_matrix((vv,(ii,jj)),shape=(shapebase+12,nc)).tocsc()
    return M,shapes

def solve(a,b,c,up,down):
    M,shapes=make(a,b,c);gb=6*c;sb=8*c;d=a-b
    rhs=np.zeros(M.shape[0]);rhs[gb:gb+c]=d*np.array(up);rhs[gb+c:gb+2*c]=d*np.array(down)
    rhs[gb]+=2*c;rhs[gb+c]-=c
    obj=np.r_[np.ones(12*c),np.zeros(12*c)]
    start=time.monotonic();res=linprog(obj,A_eq=M,b_eq=rhs,bounds=(0,None),method='highs',options={'time_limit':45})
    out={'tile':[a,b,c],'up_gate_charges':list(map(int,up)),'down_gate_charges':list(map(int,down)),
         'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,
         'rows':M.shape[0],'columns':M.shape[1],
         'scope':'Necessary continuous additive marginal relaxation; neither a physical tiling nor full two-coordinate endpoint feasibility.'}
    if res.x is not None:
        out.update(floating_population=float(res.fun),maximum_equality_residual=float(np.max(abs(M@res.x-rhs))))
    if res.status==0:
        scale=1000000;du=np.rint(res.eqlin.marginals*scale).astype(np.int64)
        endpoint=np.zeros((3,c,c),dtype=np.int64)
        for axis in range(3):
            for x in range(c):
                for y in range(c):endpoint[axis,x,y]=du[axis*c+(a*y-b*x)%c]+du[3*c+axis*c+(a*x-b*y)%c]
        wu=du[gb:gb+c];wd=du[gb+c:gb+2*c]
        # Exhaustively reconstruct original 12c^2 tile inequalities.
        maximum=-10**100;minimum=10**100
        for x in range(c):
            for y in range(c):
                for j,s in shapes:
                    eps=s*(-1)**j;ux=x-a*U[j][0];uy=y-a*U[j][1]
                    wx=x+b*U[(j+s)%6][0];wy=y+b*U[(j+s)%6][1]
                    score=s*(int(endpoint[j%3,x,y])-int(endpoint[j%3,ux%c,uy%c])
                             +int(endpoint[(j+s)%3,wx%c,wy%c])-int(endpoint[(j+s)%3,x,y]))
                    gate=(a*uy-b*ux)%c if s>0 else (a*ux-b*uy)%c
                    score+=eps*int((wu if s>0 else wd)[gate])
                    maximum=max(maximum,score);minimum=min(minimum,score)
        D=max(1,maximum);num=int(np.dot(rhs.astype(np.int64),du))
        out.update(D=D,lower_numerator=num,lower_denominator=D,exact_column_inequalities=True,
                   endpoint_tables=endpoint.tolist(),up_weights=wu.tolist(),down_weights=wd.tolist(),
                   phi_endpoint_tables=du[:3*c].reshape(3,c).tolist(),psi_endpoint_tables=du[3*c:6*c].reshape(3,c).tolist(),
                   orientation_multipliers=du[sb:].tolist(),maximum_column_score=maximum,minimum_column_score=minimum)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);ar=p.parse_args()
    old=json.loads(ar.source.read_text());out=solve(*old['tile'],old['up_gate_charges'],old['down_gate_charges']);ar.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['endpoint_tables','up_weights','down_weights','phi_endpoint_tables','psi_endpoint_tables','orientation_multipliers']},indent=2))
