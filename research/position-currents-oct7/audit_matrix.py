#!/usr/bin/env python3
"""Independently rebuild every boundary atom using coordinates in a lattice basis.
The generator uses the ambient-coordinate gcd; this audit uses integer
(i,j) coordinates of Lambda and their gcd. No numerical optimization occurs.
"""
if not __debug__:
    raise RuntimeError('Do not use Python optimization')
import json
import math
from pathlib import Path
import numpy as np
from scipy.sparse import load_npz
root=Path(__file__).resolve().parent
meta=json.loads((root/'twolevel154_meta.json').read_text())
G=np.load(root/'twolevel154_geometry.npz')
B=load_npz(root/'twolevel154_matrix.npz')
keys=np.load(root/'twolevel154_rowkeys.npy')
rhs=np.load(root/'twolevel154_rhs.npy')
dirs=[tuple(x) for x in json.loads((root/'twolevel154_dirs.json').read_text())]
assert B.shape==(550333,873496) and B.nnz==19222288
assert len(keys)==B.shape[0] and np.all(keys[1:]>keys[:-1])
assert meta['c']==13 and meta['r']==3

def lattice(p):
    x,y=p
    assert (x-3*y)%13==0
    return (x-3*y)//13,y

def physical(p):
    i,j=p
    return 13*i+3*j,j

def atoms(poly):
    for p,q in zip(poly,poly[1:]+poly[:1]):
        I,J=lattice(p),lattice(q)
        di,dj=J[0]-I[0],J[1]-I[1]
        g=math.gcd(di,dj)
        assert g>0
        du,dv=di//g,dj//g
        for j in range(g):
            f=physical((I[0]+j*du,I[1]+j*dv))
            t=physical((I[0]+(j+1)*du,I[1]+(j+1)*dv))
            if f<t:yield f,(t[0]-f[0],t[1]-f[1]),1
            else:yield t,(f[0]-t[0],f[1]-t[1]),-1

col=0
for v,ct,num in zip(meta['variants'],meta['counts'],range(24)):
    shift=G[f'g{num}'].astype(np.int64)
    template=list(atoms([tuple(p) for p in v[-3:]]))
    width=len(template)
    lo,hi=int(B.indptr[col]),int(B.indptr[col+ct])
    assert hi-lo==ct*width
    assert np.all(np.diff(B.indptr[col:col+ct+1])==width)
    actual_keys=keys[B.indices[lo:hi]].reshape(ct,width)
    actual_signs=B.data[lo:hi].reshape(ct,width)
    actperm=np.argsort(actual_keys,axis=1)
    actual_keys=np.take_along_axis(actual_keys,actperm,axis=1)
    actual_signs=np.take_along_axis(actual_signs,actperm,axis=1)
    assert np.all(actual_keys[:,1:]>actual_keys[:,:-1])
    expected_keys=np.empty((ct,width),dtype=np.int64)
    expected_signs=np.empty((ct,width),dtype=np.int8)
    for j,(p,d,sg) in enumerate(template):
        x=shift[:,0]+p[0];y=shift[:,1]+p[1]
        assert np.all((0<=x)&(x<=2002)&(0<=y)&(y<=728))
        expected_keys[:,j]=(dirs.index(d)*2003+x)*729+y
        expected_signs[:,j]=sg
    # Sparse storage may sort row IDs. Compare the sorted signed columns.
    perm=np.argsort(expected_keys,axis=1)
    expected_keys=np.take_along_axis(expected_keys,perm,axis=1)
    expected_signs=np.take_along_axis(expected_signs,perm,axis=1)
    assert np.array_equal(actual_keys,expected_keys)
    assert np.array_equal(actual_signs,expected_signs)
    col+=ct
assert col==B.shape[1]
q=np.zeros(len(keys),dtype=np.int32)
for p,d,sg in atoms([tuple(p) for p in meta['target']]):
    k=(dirs.index(d)*2003+p[0])*729+p[1]
    j=int(np.searchsorted(keys,k));assert j<len(keys) and int(keys[j])==k
    q[j]+=sg
assert np.array_equal(q,rhs)
report={'status':'EXACT_POSITIONED_CURRENT_MATRIX_PASS','columns_checked':B.shape[1], 'nonzero_entries_checked':B.nnz, 'rows':B.shape[0], 'method':'independent lattice-coordinate gcd, exact sorted signed-atom comparison, independent target boundary'}
(root/'matrix_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
