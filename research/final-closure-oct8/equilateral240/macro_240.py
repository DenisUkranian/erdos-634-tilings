#!/usr/bin/env python3
"""Exact reconstruction from 15 convex triangular-grid polygons, no unit seed import."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
TARGET=[(0,0),(420,0),(0,420)]
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def turn(a,b,c):return det(sub(b,a),sub(c,a))
def norm(a):return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]
def edges(p):return zip(p,p[1:]+p[:1])
def area2(p):return sum(det(a,b) for a,b in edges(p))
def separated(a,b):
 return any(all(turn(p,q,r)<=0 for r in b) for p,q in edges(a)) or any(all(turn(p,q,r)<=0 for r in a) for p,q in edges(b))
def construct():
 data=json.loads((HERE/'macro_grid_regions.json').read_text());require(data['denominator']==7 and data['count']==240,'Unexpected normalization')
 patches=data['regions'];require(len(patches)==15,'Expected 15 macroregions')
 polygons=[];triangles=[];counts=[]
 for k,g in enumerate(patches):
  o,u,v=g['origin'],g['u'],g['v'];p=[tuple(q)for q in g['polygon']];dd=det(u,v)
  require([norm(u),norm(v),norm(sub(u,v))]==[441,1225,2401],f'Region{k}: wrong tile vectors')
  require(len(p) in (3,4) and len(set(p))==len(p),f'Region{k}: malformed polygon')
  require(area2(p)>0 and all(turn(a,b,c)>=0 for a,b in edges(p) for c in p) and all(turn(p[j-1],p[j],p[(j+1)%len(p)])>0 for j in range(len(p))),f'Region{k}: nonconvex')
  require(all(turn(a,b,q)>=0 for a,b in edges(TARGET) for q in p),f'Region{k}: outside target')
  gp=[]
  for q in p:
   w=sub(q,o);ni,nj=det(w,v),det(u,w);require(ni%dd==nj%dd==0,f'Region{k}: nonlattice corner');gp.append((ni//dd,nj//dd))
  require(gp==[tuple(q) for q in g['grid_polygon']],f'Region{k}: inconsistent grid-coordinate table')
  require(all(a[0]==b[0] or a[1]==b[1] or sum(a)==sum(b) for a,b in edges(gp)),f'Region{k}: nongrid edge')
  def at(i,j):return(o[0]+i*u[0]+j*v[0],o[1]+i*u[1]+j*v[1])
  part=[]
  for i in range(min(q[0] for q in gp),max(q[0] for q in gp)):
   for j in range(min(q[1] for q in gp),max(q[1] for q in gp)):
    for t in [[at(i,j),at(i+1,j),at(i,j+1)],[at(i+1,j+1),at(i,j+1),at(i+1,j)]]:
     centroid3=(sum(q[0] for q in t),sum(q[1] for q in t))
     if not all(turn((3*a[0],3*a[1]),(3*b[0],3*b[1]),centroid3)>=0 for a,b in edges(p)):continue
     if area2(t)<0:t=t[::-1]
     require(all(turn(a,b,q)>=0 for a,b in edges(p) for q in t),f'Region{k}: clipped grid triangle')
     require(area2(t)==735,f'Region{k}: wrong unit area')
     part.append(t)
  require(len(part)==g['count'] and area2(p)==735*len(part),f'Region{k}: wrong grid coverage')
  polygons.append(p);triangles.extend(part);counts.append(len(part))
 for i,p in enumerate(polygons):
  for q in polygons[:i]:require(separated(p,q),'Macroregions overlap')
 require(sum(map(area2,polygons))==area2(TARGET)==240*735,'Wrong total area')
 require(len(triangles)==240,'Wrong triangle count')
 return triangles,counts
if __name__=='__main__':
 triangles,counts=construct()
 certificate={'format':'exact_polygon_unit_v1','denominator':7,'tile':[3,5,7],'target':TARGET,'triangles':triangles,'tile_count':240}
 (HERE/'macro_240_certificate.json').write_text(json.dumps(certificate,separators=(',',':'))+'\n')
 report={'status':'PASS','regions':15,'tiles':240,'macro_pairwise_disjointness_checks':105,'counts':counts,'method':'Convex grid polygons: integer lattice coordinates, grid edges, containment, disjoint macro interiors, equal areas. No solver or unit-coordinate seed imported.'}
 (HERE/'macro_240_verified.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
