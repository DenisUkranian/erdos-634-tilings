#!/usr/bin/env python3
"""Exact integer/rational verification for a restricted Erdős 634 result.
See PROOF.md and README.md for the complete scope and dependencies.
"""
if not __debug__:
    raise RuntimeError("Do not run this verifier with Python optimization enabled.")
import numpy as np,json
from pathlib import Path
R=Path(__file__).resolve().parent;M=json.loads((R/'twolevel154_meta.json').read_text());G=np.load(R/'twolevel154_geometry.npz')
x,y=np.meshgrid(np.arange(2003,dtype=np.int64),np.arange(729,dtype=np.int64));mask=(8*x>=7*y)&(8*x+15*y<=16016)&((x-3*y)%13==0)
pts=np.stack([x[mask],y[mask]],axis=1)
assert len(pts)==56183

def norm(v):return v[...,0]**2+v[...,0]*v[...,1]+v[...,1]**2
count=0
for i,V in enumerate(M['variants']):
 sh=np.array(V[-3:],dtype=np.int64);mask=np.ones(len(pts),dtype=bool)
 for p in sh:
  v=pts+p;mask&=(v[:,1]>=0)&(8*v[:,0]>=7*v[:,1])&(8*v[:,0]+15*v[:,1]<=16016)
 z=pts[mask];assert np.array_equal(z,G[f'g{i}'])
 sq=sorted(int(norm(sh[(j+1)%3]-sh[j])) for j in range(3));assert sq==sorted([(13*7)**2,(13*8)**2,(13*13)**2])
 assert int(sh[1,0]*sh[2,1]-sh[1,1]*sh[2,0])==13**2*56
 count+=len(z)
assert count==873496
report={'status':'EXACT_GEOMETRY_AND_COMPLETENESS_PASS','lattice_anchors':len(pts),'variants':24,'placements':count,'primitive_tile_squared_sides':[49,64,169],'target_scaled_vertices':M['target'],'scale_of_integer_coordinates':13,'enumeration':'independent Cartesian scan and explicit integer half-plane inequalities'}
(R/'twolevel154_geometry_audit.json').write_text(json.dumps(report,indent=2));print(report)
