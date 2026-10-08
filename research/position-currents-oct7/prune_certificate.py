#!/usr/bin/env python3
"""Retain only the propagation dependencies needed for a final contradiction.
This is proof compression, not a new geometric assumption. The independent
row-by-row verifier must be run again on its output.
"""
if not __debug__:
    raise RuntimeError('Python optimization disables required checks')
from pathlib import Path
import json
import numpy as np
from scipy.sparse import load_npz
root=Path(__file__).resolve().parent
original=root/'twolevel154_steps_full.txt'
if not original.exists():
    (root/'twolevel154_steps.txt').rename(original)
steps=np.loadtxt(original,dtype=np.int64)
B=load_npz(root/'twolevel154_matrix.npz').tocsr()
q=np.load(root/'twolevel154_rhs.npy')
order=np.full(B.shape[1],len(steps),dtype=np.int64)
values=np.full(B.shape[1],-1,dtype=np.int8)
order[steps[:,0]]=np.arange(len(steps));values[steps[:,0]]=steps[:,1]
conflict=json.loads((root/'twolevel154_propagation.json').read_text())['conflict_row']

def dependencies(row,before,lower):
    i=B.indices[B.indptr[row]:B.indptr[row+1]]
    a=B.data[B.indptr[row]:B.indptr[row+1]]
    # Only previously fixed variables which differ from the chosen free
    # extreme can alter that extreme. The others are unnecessary premises.
    extreme=(a<0) if lower else (a>0)
    return i[(order[i]<before)&(values[i]!=extreme)]
ids=B.indices[B.indptr[conflict]:B.indptr[conflict+1]]
sign=B.data[B.indptr[conflict]:B.indptr[conflict+1]]
known=values[ids]>=0
rem=int(q[conflict])-int(np.dot(sign[known].astype(np.int64),values[ids[known]].astype(np.int64)))
mn=int(np.minimum(sign[~known],0).sum());mx=int(np.maximum(sign[~known],0).sum())
assert rem<mn or rem>mx
pending=list(dependencies(conflict,len(steps),rem<mn))
needed=np.zeros(B.shape[1],dtype=bool)
while pending:
    i=int(pending.pop())
    if needed[i]:continue
    needed[i]=True
    k=int(order[i]);assert k<len(steps)
    _,v,r=steps[k]
    inds=B.indices[B.indptr[r]:B.indptr[r+1]]
    signs=B.data[B.indptr[r]:B.indptr[r+1]]
    where=np.flatnonzero(inds==i);assert len(where)==1
    s=int(signs[where[0]])
    lower=int(v)==int(s<0)
    pending.extend(dependencies(int(r),k,lower))
kept=steps[needed[steps[:,0]]]
np.savetxt(root/'twolevel154_steps.txt',kept,fmt='%d')
report={'status':'PRUNED_PENDING_INDEPENDENT_REPLAY','original_steps':len(steps),'retained_steps':len(kept),'retained_ones':int(kept[:,1].sum()),'unique_rows':len(np.unique(kept[:,2])),'conflict_row':int(conflict)}
(root/'proof_compression.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
