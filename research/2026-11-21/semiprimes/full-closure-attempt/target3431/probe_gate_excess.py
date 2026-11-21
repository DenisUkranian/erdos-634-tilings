#!/usr/bin/env python3
"""Minimize necessary repeated-gate/native minority in full periodic model."""
from pathlib import Path
import json,time,argparse
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack
from probe_full_gate_pairs import old

def run(seconds=60,profile=(22,15)):
 a,b,c=33,7,37;A,rhs,lo,hi,ints,labels=old.make_model(a,b,c);n=len(labels);A=A[:,:n];rhs[3*c*c]=profile[0];rhs[3*c*c+c]=profile[1];ng=2*(c-1);A=hstack((A,coo_matrix((A.shape[0],ng)))).tocsc()
 rows=[];cols=[];vals=[];objective=np.zeros(n+ng);objective[n:]=1
 for i,(x,y,j,s,g) in enumerate(labels):
  eps=s*(-1)**j
  if eps>0:continue
  if g==0:objective[i]=1
  else:rows.append(int(s<0)*(c-1)+g-1);cols.append(i);vals.append(1)
 for k in range(ng):rows.append(k);cols.append(n+k);vals.append(-1)
 C=coo_matrix((vals,(rows,cols)),shape=(ng,n+ng)).tocsc();start=time.monotonic();res=linprog(objective,A_eq=A,b_eq=rhs,A_ub=C,b_ub=np.ones(ng),bounds=(0,None),method='highs-ipm',options={'time_limit':seconds});out={'tile':[a,b,c],'profile':list(profile),'population':111,'status':res.status,'message':res.message,'seconds':time.monotonic()-start,'scope':__doc__.strip()}
 if res.x is not None:out.update(excess=float(res.fun),support=[[k,float(v)] for k,v in enumerate(res.x) if v>1e-9])
 if res.status==0:
  scale=10**9;w=np.rint(res.eqlin.marginals*scale).astype(np.int64);v=np.maximum(-scale,np.minimum(0,np.rint(res.ineqlin.marginals*scale).astype(np.int64)));scores=A.astype(np.int64).T@w+C.astype(np.int64).T@v
  # Shift both signpopulation potentials down by maximum positive tile error.
  err=max(0,int(max(scores[:n]-objective[:n]*scale)));w[-2:]-=err
  assert np.all((A.astype(np.int64).T@w+C.astype(np.int64).T@v)<=objective*scale)
  num=int(rhs.astype(np.int64)@w+v.sum());out.update(integer_eq_weights=w.tolist(),integer_cap_weights=v.tolist(),D=scale,numerator=num,denominator=scale,rounding_repair=err)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=60);p.add_argument('--out',type=Path,required=True);ar=p.parse_args();o=run(ar.seconds);ar.out.write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({k:v for k,v in o.items() if k not in ('support','integer_eq_weights','integer_cap_weights')},indent=2))
