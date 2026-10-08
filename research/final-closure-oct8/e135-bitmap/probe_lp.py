#!/usr/bin/env python3
"""Scoped floating-point LP diagnostic; never an exact negative certificate."""
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
prefix=sys.argv[1];start=time.monotonic();ri=[];ci=[];va=[];rhs=[]
with open(prefix+'.model.txt') as f:
 nv,nsel=map(int,next(f).split())
 for _ in range(nv+nsel):next(f)
 for row,line in enumerate(f):
  b,n,*lits=map(int,line.split());rhs.append(b)
  for z in lits:ri.append(row);ci.append(abs(z)-1);va.append(1 if z>0 else -1)
B=coo_matrix((np.array(va,dtype=np.float64),(np.array(ri,dtype=np.int32),np.array(ci,dtype=np.int32))),shape=(len(rhs),nv)).tocsr()
del ri,ci,va
r=linprog(np.zeros(nv),A_eq=B,b_eq=np.array(rhs),bounds=(0,1),method='highs',options={'time_limit':30})
j={'status':int(r.status),'message':r.message,'variables':nv,'rows':len(rhs),'seconds':time.monotonic()-start,'exact_certificate':False,'global_E135_decided':False}
if r.x is not None:j['max_equation_error']=float(np.max(np.abs(B@r.x-rhs)))
Path(prefix+'.lp.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
