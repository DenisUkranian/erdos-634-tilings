#!/usr/bin/env python3
"""Numerical necessary height/first-moment projection; never a tiling decision."""
import argparse, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix, vstack, hstack

def model(a,b,c,L,H):
    A=b*(2*a+b)/c; B=a*(a+2*b)/c; N=(a+2*b)*(2*a+b)
    z=complex(a+b/2,b*np.sqrt(3)/2)/c
    rho=complex(.5,np.sqrt(3)/2)
    def axial(w): return np.array([w.real-w.imag/np.sqrt(3),2*w.imag/np.sqrt(3)])
    nr=(H-L+3)*3*5
    row=lambda h,j,k: ((h-(L-1))*3+j%3)*5+k
    def mon(q):
        x,y=q
        return np.array([x,y,x*x,x*y,y*y])
    rhs=np.zeros(nr+3)
    boundary=[(np.array([0.,0.]),np.array([A,0.]),0,0),(np.array([A,0.]),np.array([0.,B]),2,1),(np.array([0.,B]),np.array([0.,0.]),0,1)]
    for p,q,h,j in boundary:
        for k,v in enumerate(mon(q)-mon(p)):rhs[row(h,j,k)]+=v
    rhs[-3:]=[N,-c,-(a-b)]
    ii=[]; jj=[]; vv=[]; meta=[]
    for h in range(L,H+1):
      for j in range(6):
       for s in [-1,1]:
        u=axial(-a/c*z**h*rho**j); w=axial(b/c*z**h*rho**((j+s)%6))
        off=np.array([u,np.zeros(2),w])
        lx=-min(off[:,0]); ly=-min(off[:,1]); ub=A*B-max(B*off[:,0]+A*off[:,1]); gap=ub-B*lx-A*ly
        if gap < -1e-8:continue
        anchors=[np.array([lx,ly]),np.array([lx+gap/B,ly]),np.array([lx,ly+gap/A])]
        for q in anchors:
         kcol=len(meta);eps=s*(-1)**j
         poly=[q+u,q,q+w] if s>0 else [q+w,q,q+u]
         labels=[(h,j),(h,j+s),(h+s,j)] if s>0 else [(h,j+s),(h,j),(h+s,j)]
         for p,t,(edgeh,edgej) in zip(poly,poly[1:]+poly[:1],labels):
          vals=mon(t)-mon(p)
          for k,v in enumerate(vals):
           if abs(v)>1e-13:ii.append(row(edgeh,edgej,k));jj.append(kcol);vv.append(v)
         for r,v in [(nr,1),(nr+1 if h%2 else nr+2,eps)]:
          ii.append(r);jj.append(kcol);vv.append(v)
         meta.append((h,j,s,*q))
    M=coo_matrix((vv,(ii,jj)),shape=(len(rhs),len(meta))).tocsc()
    # Row scaling has no bearing on validity of the projection; this remains numerical.
    scale=np.maximum(1,np.asarray(abs(M).max(axis=1).toarray()).ravel())
    M=M.multiply((1/scale)[:,None]).tocsc();rhs=rhs/scale
    return M,rhs,meta

def main():
 p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--lo',type=int,default=-2);p.add_argument('--hi',type=int,default=4);p.add_argument('--odd',type=int);p.add_argument('--seconds',type=float,default=30);p.add_argument('--out',type=Path);args=p.parse_args()
 start=time.monotonic();M,r,meta=model(args.a,args.b,args.c,args.lo,args.hi)
 odd=np.array([h%2 for h,j,s,x,y in meta],dtype=float)
 if args.odd is not None:M=vstack([M,odd[None,:]],format='csc');r=np.r_[r,args.odd]
 sol=linprog(odd,A_eq=M,b_eq=r,bounds=(0,None),method='highs',options={'time_limit':args.seconds})
 out={'tile':[args.a,args.b,args.c],'height_interval':[args.lo,args.hi],'fixed_odd_population':args.odd,'rows':M.shape[0],'columns':M.shape[1],'status':int(sol.status),'message':sol.message,'seconds':time.monotonic()-start,'scope':'Numerical first-moment height relaxation; no infeasibility certificate or tiling claimed.'}
 if sol.x is not None:
  out['objective']=float(sol.fun);out['max_residual']=float(max(abs(M@sol.x-r)));out['height_population']={str(h):float(sum(x for x,t in zip(sol.x,meta)if t[0]==h))for h in range(args.lo,args.hi+1)}
  out['nonzeros']=[{'template':list(t),'weight':float(x)}for t,x in zip(meta,sol.x)if x>1e-9]
 if args.out:args.out.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items()if k!='nonzeros'},indent=2),flush=True)
if __name__=='__main__':main()
