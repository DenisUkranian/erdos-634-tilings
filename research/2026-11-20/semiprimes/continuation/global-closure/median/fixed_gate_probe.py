#!/usr/bin/env python3
"""Continuous full-residue test with one explicitly fixed integer gate profile."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from per_gate_integrality import make_model

p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--n',type=int,default=2);p.add_argument('--seconds',type=float,default=30);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
a,b,c=args.a,args.b,args.c
A,rhs,lo,hi,integ,labels=make_model(a,b,c);nc=len(labels)
g=np.zeros(2*c);g[0]=-args.n;g[c]=args.n
rhs=rhs-A[:,nc:]@g;A=A[:,:nc]
t=time.monotonic()
r=linprog(np.zeros(nc),A_eq=A,b_eq=rhs,bounds=(0,None),method='highs-ipm',options={'time_limit':args.seconds})
out={'tile':[a,b,c],'fixed_native_parameter':args.n,'remote_gate_charges':'all zero','native_gate_currents':[2*c-(a-b)*args.n,-c+(a-b)*args.n],'rows':A.shape[0],'columns':nc,'status':int(r.status),'message':r.message,'seconds':time.monotonic()-t,'scope':'Continuous all-residue necessary projection with fixed integral gate charges. Feasibility is not a geometric tiling.'}
if r.x is not None:
 out['maximum_equality_residual']=float(np.max(abs(A@r.x-rhs)))
 out['support']=[list(labels[i])+[float(v)]for i,v in enumerate(r.x)if v>1e-8]
args.out.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='support'}),flush=True)
