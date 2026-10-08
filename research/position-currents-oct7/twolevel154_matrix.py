#!/usr/bin/env python3
"""Exact integer/rational verification for a restricted Erdős 634 result.
See PROOF.md and README.md for the complete scope and dependencies.
"""
if not __debug__:
    raise RuntimeError("Do not run this verifier with Python optimization enabled.")
import numpy as np,math,time,json
from scipy.sparse import csc_matrix,save_npz
from pathlib import Path
root=Path(__file__).resolve().parent;M=json.loads((root/'twolevel154_meta.json').read_text());G=np.load(root/'twolevel154_geometry.npz');c=M['c'];r=M['r'];P=M['target'];v=M['variants'];counts=M['counts'];start=time.time()
def segments(T):
 for p,q in zip(T,T[1:]+T[:1]):
  dx=q[0]-p[0];dy=q[1]-p[1];g=math.gcd(dx,dy);ux=dx//g;uy=dy//g;k=c//math.gcd(c,ux-r*uy);assert g%k==0;n=g//k
  d=(ux*k,uy*k);sg=1
  if d<(0,0):d=(-d[0],-d[1]);sg=-1
  for j in range(n):
   a=(p[0]+j*ux*k,p[1]+j*uy*k)
   if sg<0:a=(a[0]-d[0],a[1]-d[1])
   yield a,d,sg
V=[list(segments(z[-3:])) for z in v];tar=list(segments(P));dirs=sorted({d for S in V+[tar] for a,d,s in S});D={d:i for i,d in enumerate(dirs)}
def key(d,x,y):return(D[d]*2003+x)*729+y
nnz=sum(n*len(S) for n,S in zip(counts,V));n=sum(counts)
keys=np.empty(nnz,dtype=np.int64);data=np.empty(nnz,dtype=np.int8);indptr=np.empty(n+1,dtype=np.int64);indptr[0]=0
ptr=col=0
for i,(ct,S) in enumerate(zip(counts,V)):
 pts=G[f'g{i}'];k=len(S);block=keys[ptr:ptr+ct*k].reshape(ct,k);val=data[ptr:ptr+ct*k].reshape(ct,k)
 for j,(p,d,sg) in enumerate(S):block[:,j]=key(d,pts[:,0].astype(np.int64)+p[0],pts[:,1].astype(np.int64)+p[1]);val[:,j]=sg
 indptr[col+1:col+ct+1]=ptr+k*np.arange(1,ct+1,dtype=np.int64);ptr+=ct*k;col+=ct
trgkeys=np.array([key(d,p[0],p[1]) for p,d,s in tar],dtype=np.int64)
allkeys=np.concatenate([keys,trgkeys]);del keys
uniq,inv=np.unique(allkeys,return_inverse=True);del allkeys
q=np.zeros(len(uniq),dtype=np.int32)
for ri,(_,_,sg) in zip(inv[nnz:],tar):q[ri]+=sg
B=csc_matrix((data,inv[:nnz],indptr),shape=(len(uniq),n))
print('matrix',B.shape,'nnz',B.nnz,'seconds',time.time()-start,flush=True)
save_npz(root/'twolevel154_matrix.npz',B);np.save(root/'twolevel154_rhs.npy',q);np.save(root/'twolevel154_rowkeys.npy',uniq)
(root/'twolevel154_dirs.json').write_text(json.dumps(dirs))
print('saved',time.time()-start,flush=True)
