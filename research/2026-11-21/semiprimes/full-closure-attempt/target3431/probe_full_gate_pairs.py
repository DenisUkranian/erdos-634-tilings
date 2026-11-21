#!/usr/bin/env python3
"""Full periodic endpoint LP with explicit empty-gate half-turn pairing.
Only fixed gate patterns are searched. Returned exact duals need separate
verification; numerical statuses and incomplete patterns do not close a target.
"""
from pathlib import Path
import importlib.util,json,argparse,time
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'research').is_dir())
spec=importlib.util.spec_from_file_location('full',ROOT/'research/2026-11-20/semiprimes/continuation/global-closure/median/per_gate_integrality.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def model(a,b,c,active):
 A,rhs,lo,hi,integ,labels=old.make_model(a,b,c);n=len(labels);A=A[:-2,:n];rhs=rhs[:-2];rhs[3*c*c]-=2*(a-b);rhs[3*c*c+c]+=2*(a-b)
 index={lab[:4]:i for i,lab in enumerate(labels)};mates=[]
 for i,(x,y,j,s,g) in enumerate(labels):
  xx=(x-a*old.U[j][0]+b*old.U[(j+s)%6][0])%c;yy=(y-a*old.U[j][1]+b*old.U[(j+s)%6][1])%c
  k=index[xx,yy,(j+3)%6,s];assert labels[k][-1]==g;mates.append(k)
 assert all(mates[k]==i and k!=i for i,k in enumerate(mates))
 groups=[]
 for i,lab in enumerate(labels):
  s,g=lab[-2:];gate=g+(0 if s>0 else c)
  if g==0 or gate in active:groups.append([i])
  elif i<mates[i]:groups.append([i,mates[i]])
 rr=[];cc=[]
 for k,group in enumerate(groups):
  for i in group:rr.append(i);cc.append(k)
 C=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(n,len(groups))).tocsc();B=(A@C).tocsc();cost=np.array([len(g) for g in groups],float)
 return B,rhs,cost,labels,groups,mates

def run(a,b,c,active,seconds=60,profile=None,method="highs"):
 profile = profile or (2*c-2*(a-b),-c+2*(a-b))
 B,rhs,cost,labels,groups,mates=model(a,b,c,active);rhs[3*c*c]=profile[0];rhs[3*c*c+c]=profile[1];start=time.monotonic();r=linprog(cost,A_eq=B,b_eq=rhs,bounds=(0,None),method=method,options={'time_limit':seconds})
 out={'tile':[a,b,c],'active_remote_gates':sorted(active),'native_gate_profile':[int(rhs[3*c*c]),int(rhs[3*c*c+c])],'rows':B.shape[0],'columns':B.shape[1],'status':r.status,'message':r.message,'seconds':time.monotonic()-start,'scope':__doc__.strip()}
 if r.x is not None:
  out.update(population=float(r.fun),support=[[k,float(v)] for k,v in enumerate(r.x) if v>1e-9],max_residual=float(np.max(abs(B@r.x-rhs))))
 if r.status==0:
  scale=10**8;dual=np.rint(r.eqlin.marginals*scale).astype(np.int64);assert max(abs(int(v)) for v in dual)<2**56;scores=B.astype(np.int64).T@dual;D=max(1,max((int(s)+int(v)-1)//int(v) for s,v in zip(scores,cost)));num=int(rhs.astype(np.int64)@dual)
  out.update(integer_row_potentials=dual.tolist(),D=D,lower_numerator=num,lower_denominator=D,exact_lp_column_scores=True)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('a',type=int);p.add_argument('b',type=int);p.add_argument('c',type=int);p.add_argument('--active',type=int,nargs='*',default=[]);p.add_argument('--seconds',type=int,default=60);p.add_argument('--out',type=Path,required=True);ar=p.parse_args();out=run(ar.a,ar.b,ar.c,set(ar.active),ar.seconds);ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('support','integer_row_potentials')},indent=2))
