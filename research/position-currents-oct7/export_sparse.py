#!/usr/bin/env python3
"""Exact integer/rational verification for a restricted Erdős 634 result.
See PROOF.md and README.md for the complete scope and dependencies.
"""
if not __debug__:
    raise RuntimeError("Do not run this verifier with Python optimization enabled.")
import numpy as np,json
from scipy.sparse import load_npz
from pathlib import Path
r=Path(__file__).resolve().parent;B=load_npz(r/'twolevel154_matrix.npz');C=B.tocsr()
for prefix,M in [('col',B),('row',C)]:
 np.asarray(M.indptr,dtype=np.int64).tofile(r/(prefix+'_ptr.bin'));np.asarray(M.indices,dtype=np.int32).tofile(r/(prefix+'_idx.bin'));np.asarray(M.data,dtype=np.int8).tofile(r/(prefix+'_dat.bin'))
np.asarray(np.load(r/'twolevel154_rhs.npy'),dtype=np.int32).tofile(r/'rhs.bin')
(r/'dimensions.txt').write_text(f'{B.shape[0]} {B.shape[1]} {B.nnz}\n')
print(B.shape,B.nnz)
