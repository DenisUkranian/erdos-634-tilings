#!/usr/bin/env python3
"""Eleven ordinary grid polygons tile T(30,30); exact integer verification.
No solver or prior unit-coordinate certificate is imported.
Coordinates below are Eisenstein-coordinate numerators, denominator 7.
"""
import json
import sys
if not __debug__:
    raise SystemExit("Verification requires Python without -O/-OO.")
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DEN=7
TARGET=[(0,0),(420,0),(210,210),(0,210)]
# (name, origin, length-3 vector, length-5 vector, polygon, unit count)
PATCHES=[
 ('right_strip',(378,0),(21,0),(-35,35),[(168,210),(378,0),(420,0),(210,210)],24),
 ('low_rectangle',(98,0),(0,21),(-35,0),[(63,0),(133,0),(133,63),(63,63)],12),
 ('upper_triangle',(175,168),(-21,21),(35,0),[(63,210),(231,147),(168,210)],9),
 ('left_rectangle',(21,0),(-21,0),(0,35),[(0,0),(63,0),(63,210),(0,210)],36),
 ('notch_tile',(133,63),(-21,0),(0,35),[(112,63),(133,63),(133,98)],1),
 ('lower_triangle',(182,0),(9,15),(-40,15),[(133,0),(378,0),(178,75)],25),
 ('thin_trapezoid',(112,63),(9,15),(-40,15),[(63,63),(112,63),(148,123),(108,138)],9),
 ('notched_triangle',(148,25),(-15,24),(-15,-25),[(133,0),(178,75),(148,123),(133,98)],8),
 ('left_triangle',(78,88),(-15,24),(-15,-25),[(63,63),(108,138),(63,210)],9),
 ('right_trapezoid',(329,49),(-24,9),(25,-40),[(183,165),(258,45),(378,0),(231,147)],21),
 ('staircase',(243,69),(15,-24),(-40,15),[(63,210),(108,138),(148,123),(178,75),(258,45),(183,165)],26),
]

def sub(a,b):return a[0]-b[0],a[1]-b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]
def area2(p):return sum(cross(a,b) for a,b in zip(p,p[1:]+p[:1]))
def edges(p):return list(zip(p,p[1:]+p[:1]))
def onseg(p,a,b):return cross(sub(p,a),sub(b,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))

def intersects(a,b,c,d):
 x,y=cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(d,a))
 z,w=cross(sub(d,c),sub(a,c)),cross(sub(d,c),sub(b,c))
 return x*y<0 and z*w<0 or x==0 and onseg(c,a,b) or y==0 and onseg(d,a,b) or z==0 and onseg(a,c,d) or w==0 and onseg(b,c,d)

def interior_centroid(t,p):
 # Coordinates multiplied by 3 keep all ray-crossing operations integral.
 q=(sum(a[0] for a in t),sum(a[1] for a in t));poly=[(3*x,3*y) for x,y in p];wn=0
 for a,b in edges(poly):
  det=cross(sub(b,a),sub(q,a))
  if a[1]<=q[1]<b[1] and det>0:wn+=1
  if b[1]<=q[1]<a[1] and det<0:wn-=1
 return wn!=0

def atom_current(polygons):
 vertices=set(v for p,sign in polygons for v in p);result=Counter()
 for p,sign in polygons:
  for a,b in edges(p):
   d=sub(b,a);vs=sorted((q for q in vertices if onseg(q,a,b)),key=lambda q:sum(x*y for x,y in zip(sub(q,a),d)))
   for u,v in zip(vs,vs[1:]):result[min(u,v),max(u,v)]+=sign*(1 if u<v else -1)
 return {edge:value for edge,value in result.items() if value}

def construct():
 tiles=[];report=[]
 for name,o,u,v,p,count in PATCHES:
  assert [norm(u),norm(v),norm(sub(u,v))]==[9*49,25*49,49*49]
  det=cross(u,v);gp=[]
  for q in p:
   d=sub(q,o);ni,nj=cross(d,v),cross(u,d)
   assert ni%det==nj%det==0,(name,'nonlattice vertex')
   gp.append((ni//det,nj//det))
  for a,b in edges(gp):
   d=sub(b,a);assert d[0]==0 or d[1]==0 or d[0]+d[1]==0,(name,'non-grid edge')
  assert area2(p)>0
  ee=edges(p)
  for i,(a,b) in enumerate(ee):
   for j,(c,d) in enumerate(ee):
    if j<=i+1 or i==0 and j==len(ee)-1:continue
    assert not intersects(a,b,c,d),(name,'nonsimple polygon')
  assert all(cross(sub(b,a),sub(q,a))>=0 for q in p for a,b in edges(TARGET))
  def at(i,j):return(o[0]+i*u[0]+j*v[0],o[1]+i*u[1]+j*v[1])
  patch=[]
  for i in range(min(q[0] for q in gp),max(q[0] for q in gp)):
   for j in range(min(q[1] for q in gp),max(q[1] for q in gp)):
    for t in [[at(i,j),at(i+1,j),at(i,j+1)],[at(i+1,j+1),at(i,j+1),at(i+1,j)]]:
     if not interior_centroid(t,p):continue
     if area2(t)<0:t=t[::-1]
     patch.append(t)
  assert len(patch)==count and area2(p)==count*735
  assert not atom_current([(t,1) for t in patch]+[(p,-1)])
  tiles.extend(patch)
  report.append({'name':name,'count':count,'grid_polygon':gp,'origin':o,'u':u,'v':v,'polygon':p})
 assert sum(r['count'] for r in report)==180
 assert not atom_current([(p,1) for _,_,_,_,p,_ in PATCHES]+[(TARGET,-1)])
 assert area2(TARGET)==180*735
 return tiles,report

if __name__=='__main__':
 triangles,patches=construct()
 cert={'format':'exact_trapezoid_unit_v1','denominator':DEN,'tile':[3,5,7],'target':TARGET,'triangles':triangles,'levels':[0,1]}
 (ROOT/'macro_seed_certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
 report={'status':'PASS','method':'eleven grid polygons and exact oriented-boundary cancellation','tiles':180,'patches':patches,'macro_boundaries_cancel':True,'unit_boundaries_cancel_in_each_macro':True}
 (ROOT/'macro_seed_verified.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 11 grid polygons, 180 congruent triangles, exact macro and unit boundary cancellation.')
