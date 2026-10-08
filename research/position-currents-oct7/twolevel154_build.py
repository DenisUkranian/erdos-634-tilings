#!/usr/bin/env python3
"""Exact integer/rational verification for a restricted Erdős 634 result.
See PROOF.md and README.md for the complete scope and dependencies.
"""
if not __debug__:
    raise RuntimeError("Do not run this verifier with Python optimization enabled.")
import numpy as np,math,time,json
from pathlib import Path
def rho(p): return (-p[1],p[0]+p[1])
root=Path(__file__).resolve().parent
start=time.time();c=13;a=8;b=7;r=3
P=np.array([(0,0),(2002,0),(637,728)],dtype=np.int32)
points=[]
for j in range(729):
 lo=(7*j+7)//8;hi=(16016-15*j)//8
 i=(lo-r*j+c-1)//c
 points.extend([(c*k+r*j,j) for k in range(i,(hi-r*j)//c+1)])
points=np.array(points,dtype=np.int32)
print('points',len(points),flush=True)
variants=[]
for h in [0,1]:
 for x,y in[(a,b),(b,a)]:
  u=(c*x,0) if h==0 else(a*x,b*x)
  v=(-c*y,c*y) if h==0 else(-(a+b)*y,a*y)
  for rot in range(6):
   variants.append((h,rot,x,y,(0,0),u,v));u=rho(u);v=rho(v)
# triangular entries with gamma anchor
blocks=[];counts=[]
for z in variants:
 V=np.array(z[-3:],dtype=np.int32)
 mask=np.ones(len(points),dtype=bool)
 for sh in V:
  shifted=points+sh
  for i in range(3):
   e=P[(i+1)%3]-P[i];w=shifted-P[i]
   mask &= e[0]*w[:,1]-e[1]*w[:,0]>=0
 blocks.append(points[mask]);counts.append(sum(mask))
print('triangles',sum(counts),counts,'seconds',time.time()-start,flush=True)
np.savez_compressed(root/'twolevel154_geometry.npz',**{f'g{i}':b for i,b in enumerate(blocks)})
(root/'twolevel154_meta.json').write_text(json.dumps({'variants':variants,'counts':[int(x) for x in counts],'target':P.tolist(),'r':r,'c':c}))
