#!/usr/bin/env python3
"""Constructive search: fixed one-height boundary collar plus paired tiles.
Failure concerns only this recipe, never the entire F3 target.
"""
from pathlib import Path
import json,math,os,sys,time,argparse
import numpy as np
from scipy.sparse import csc_matrix
from collections import deque
from one_level import P,V,forced,add,sub,rot,mul,det
start=time.monotonic();parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=120);arg=parser.parse_args()
root=Path(__file__).resolve().parent
points=np.array([(x,y) for y in range(265) for x in range(650)],dtype=np.int64)
polys=[]
for a,b in ((24,11),(11,24)):
 u,v=(a,0),(-b,b)
 for r in range(3):
  T=[(0,0),u,add(u,v),v]
  shift=min(T);T=[sub(t,shift) for t in T];polys.append(T)
  u,v=rot(u),rot(v)
blocks=[]
for T in polys:
 mask=np.ones(len(points),bool)
 for q in T:
  X=points+q
  for u,v in zip(P,P[1:]+P[:1]):
   d=sub(v,u);w=X-u;mask &=d[0]*w[:,1]-d[1]*w[:,0]>=0
 B=points[mask]
 for C in forced:
  # Exact separating-axis theorem on two convex polygons.
  separated=np.zeros(len(B),bool)
  for p,q in zip(T,T[1:]+T[:1]):
   d=sub(q,p)
   maxC=max(det(d,sub(c,p)) for c in C)
   offset=d[0]*B[:,1]-d[1]*B[:,0]
   separated|=maxC-offset<=0
  for p,q in zip(C,C[1:]+C[:1]):
   d=sub(q,p)
   maxT=max(det(d,sub(t,p)) for t in T)
   offset=d[0]*B[:,1]-d[1]*B[:,0]
   separated|=maxT+offset<=0
  B=B[separated]
 blocks.append(B)
print('placements',list(map(len,blocks)),flush=True)
def segments(T):
 for p,q in zip(T,T[1:]+T[:1]):
  dx,dy=sub(q,p);g=math.gcd(dx,dy);d=(dx//g,dy//g);sign=1
  if d<(0,0):d=mul(d,-1);sign=-1
  for k in range(g):
   w=add(p,(k*dx//g,k*dy//g))
   if sign<0:w=sub(w,d)
   yield w,d,sign
S=[list(segments(T)) for T in polys]
from collections import Counter
target=Counter()
for sign,T in [(1,P)]+[(-1,t) for t in forced]:
 for p,d,s in segments(T):target[(p,d)]+=sign*s
# Long-edge rows cancel exactly before positions are assembled.
target={k:v for k,v in target.items() if v}
dirs=sorted({d for z in S for _,d,_ in z});D={d:i for i,d in enumerate(dirs)}
assert all(d in D for p,d in target),list(target)[:10]
def key(d,x,y):return (D[d]*650+x)*265+y
N=sum(map(len,blocks));nz=sum(len(B)*len(s) for B,s in zip(blocks,S))
keys=np.empty(nz,np.int64);data=np.empty(nz,np.int8);indptr=np.empty(N+1,np.int64);indptr[0]=0
ptr=col=0
for B,segs in zip(blocks,S):
 ct,z=len(B),len(segs);kb=keys[ptr:ptr+ct*z].reshape(ct,z);db=data[ptr:ptr+ct*z].reshape(ct,z)
 for j,(p,d,s) in enumerate(segs):kb[:,j]=key(d,B[:,0]+p[0],B[:,1]+p[1]);db[:,j]=s
 indptr[col+1:col+ct+1]=ptr+z*np.arange(1,ct+1);ptr+=ct*z;col+=ct
items=list(target.items());tk=np.array([key(d,*p) for (p,d),v in items],np.int64)
uniq,inv=np.unique(np.concatenate([keys,tk]),return_inverse=True)
b=np.zeros(len(uniq),np.int32)
for ri,((p,d),v) in zip(inv[nz:],items):b[ri]+=v
B=csc_matrix((data,inv[:nz],indptr),shape=(len(uniq),N));B.sum_duplicates();del keys,inv,uniq
report={'scope':'Restricted one-short-level filling of the sufficient 792 remainder, not full 4830','placements':N,'rows':B.shape[0],'entries':B.nnz}
R=B.tocsr();lo=R.minimum(0).sum(axis=1).A.ravel().astype(int);hi=R.maximum(0).sum(axis=1).A.ravel().astype(int)
rhs=b.copy();values=np.full(N,-1,np.int8);queue=deque(np.flatnonzero((rhs<=lo)|(rhs>=hi)));queued=np.zeros(len(b),bool);queued[list(queue)]=True;conflict=None
while queue:
 row=queue.popleft();queued[row]=False
 if rhs[row]<lo[row] or rhs[row]>hi[row]:conflict=int(row);break
 if rhs[row]!=lo[row] and rhs[row]!=hi[row]:continue
 low=rhs[row]==lo[row]
 for k in range(R.indptr[row],R.indptr[row+1]):
  col=R.indices[k]
  if values[col]>=0:continue
  val=int(R.data[k]<0) if low else int(R.data[k]>0);values[col]=val
  inds=B.indices[B.indptr[col]:B.indptr[col+1]];sg=B.data[B.indptr[col]:B.indptr[col+1]]
  rhs[inds]-=sg*val;lo[inds]+=(sg<0);hi[inds]-=(sg>0)
  for rr in inds[(~queued[inds])&((rhs[inds]<=lo[inds])|(rhs[inds]>=hi[inds]))]:queue.append(rr);queued[rr]=True
unknown=np.flatnonzero(values<0);report.update(propagation_conflict=conflict,assigned=int(sum(values>=0)),forced_ones=int(sum(values==1)),remaining=len(unknown))
print(json.dumps(report),flush=True)
if conflict is not None:report['status']='RESTRICTED_PROPAGATION_CONFLICT_UNCERTIFIED'
else:
 rr=np.flatnonzero((lo!=0)|(hi!=0)|(rhs!=0));M=B[rr,:][:,unknown].tocsr()
 sys.path.insert(0,os.environ.get('ERDOS_ORTOOLS_PATH','/tmp/erdos634-ortools'))
 from ortools.sat.python import cp_model
 model=cp_model.CpModel();variables=[model.new_bool_var('') for _ in unknown]
 for row in range(M.shape[0]):
  f,l=M.indptr[row:row+2]
  model.add(cp_model.LinearExpr.weighted_sum([variables[int(k)] for k in M.indices[f:l]],[int(v) for v in M.data[f:l]])==int(rhs[rr[row]]))
 solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=arg.seconds;solver.parameters.num_search_workers=1;solver.parameters.linearization_level=0;solver.parameters.symmetry_level=0;solver.parameters.random_seed=634;solver.parameters.log_search_progress=True
 status=solver.solve(model);report['solver_status']=solver.status_name(status)
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  values[unknown]=[solver.value(v) for v in variables];assert np.array_equal(B@values,b)
  chosen=np.flatnonzero(values==1);offset=np.cumsum([0]+list(map(len,blocks)));tris=list(forced);macros=[]
  for col in chosen:
   vi=int(np.searchsorted(offset,col,side='right')-1);p=blocks[vi][col-offset[vi]];T=[tuple(int(x) for x in p+q) for q in polys[vi]]
   macros.append(T);tris.extend([[T[0],T[1],T[3]],[T[1],T[2],T[3]]])
  report['status']='EXACT_BOUNDARY_SOLUTION';report['tiles']=len(tris)
  (root/'q792_one_level_certificate.json').write_text(json.dumps({'denominator':1,'tile':[24,11,31],'target':P,'triangles':tris,'parallelograms':macros},indent=2)+'\n')
 else:report['status']='RESTRICTED_SOLVER_INFEASIBLE_UNCERTIFIED' if status==cp_model.INFEASIBLE else 'INCOMPLETE'
report['seconds']=time.monotonic()-start
(root/'q792_one_level_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
