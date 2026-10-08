#!/usr/bin/env python3
"""An actual equilateral tiling with just14tiles at its extreme short-edge height.
A local positive trade is embedded in an ordinary grid of the verified E60seed.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('bands',ROOT/'research/closure-position-oct8/equilateral-small/construct_new.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
SEED=HERE.parent/'equilateral240/equilateral_240.json'
def need(x,s):
 if not x:raise ValueError(s)
def mul(u,v):return(u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]+u[1]*v[1])
def turn(a,c,d):return b.det(b.sub(c,a),b.sub(d,a))
def inside(t,p):return all(turn(a,c,q)>=0 for a,c in zip(p,p[1:]+p[:1]) for q in t)
def parallelogram_grid(x,width,height,stepx,stepy):
 need(width%stepx==height%stepy==0,'Nonintegral grid')
 out=[]
 for i in range(width//stepx):
  for j in range(height//stepy):
   p=(F(x+i*stepx),F(j*stepy));u=(F(stepx),F(0));v=(F(0),F(stepy))
   out.extend([b.ccw((p,b.add(p,u),b.add(b.add(p,u),v))),b.ccw((p,b.add(b.add(p,u),v),b.add(p,v)))])
 return out

def local_trade():
 # Central c-by-ac-z parallelogram, split into c cells:2c=14tiles.
 out=[];cvec=(F(7),F(0));step=(F(9,7),F(15,7))
 for j in range(7):
  p=b.scale(step,j);q=b.add(p,cvec);r=b.add(p,step);s=b.add(q,step)
  out.extend([b.ccw((p,q,r)),b.ccw((q,s,r))])
 out.extend(b.grid(((0,0),(9,15),(0,15)),3))
 out.extend(b.grid(((7,0),(16,0),(16,15)),3))
 # Complete width30 with14=5+3+3+3.
 x=16
 for width,stepy in [(5,3),(3,5),(3,5),(3,5)]:
  out.extend(parallelogram_grid(x,width,15,width,stepy));x+=width
 need(len(out)==60,'Wrong patch count')
 return out

def height(t):
 dirs={};z=(F(3,7),F(5,7));rho=(F(0),F(1));zh=(F(1),F(0))
 for h in range(3):
  r=zh
  for j in range(6):dirs[r]=h;r=mul(r,rho)
  zh=mul(zh,z)
 for i in range(3):
  w=b.sub(t[(i+1)%3],t[i]);q=w[0]*w[0]+w[0]*w[1]+w[1]*w[1]
  if q in(9,25):return dirs[b.scale(w,F(1,3 if q==9 else 5))]
 raise ValueError('No short edge')

def build():
 source=json.loads(SEED.read_text());seed=[tuple(tuple(F(x,7)for x in p)for p in t)for t in source['triangles']]
 enlarged=[]
 for t in seed:enlarged.extend(b.grid([b.scale(p,3)for p in t],3))
 # A15-fold height1triangle: gamma vertexG, shortedge vectors(-225,-375)/7 and(-225,360)/7.
 z=(F(3,7),F(5,7));G=(F(225,7),F(900,7))
 def place(p):return b.add(G,mul(z,b.add(p,(-30,0))))
 region=[place(p)for p in[(0,0),(30,0),(30,15),(0,15)]]
 removed=[t for t in enlarged if inside(t,region)];remaining=[t for t in enlarged if not inside(t,region)]
 need(len(removed)==60,'Grid-aligned patch not found')
 need(all(height(t)==1 for t in removed),'Removed patch has wrong height')
 replacement=[tuple(place(p)for p in t)for t in local_trade()]
 result=remaining+replacement;need(len(result)==2160,'Wrong complete count')
 counts={h:sum(height(t)==h for t in result)for h in range(3)}
 need(counts=={0:774,1:1372,2:14},f'Unexpected height populations:{counts}')
 def encode(ts):
  out=[]
  for t in ts:
   v=[]
   for p in t:
    q=[49*x for x in p];need(all(x.denominator==1 for x in q),'Denominator overflow');v.append([int(x)for x in q])
   out.append(v)
  return out
 certificate={'format':'exact_polygon_unit_v1','denominator':49,'tile':[3,5,7],'target':[[0,0],[8820,0],[0,8820]],'triangles':encode(result),'tile_count':2160,'target_side':180,'short_height_populations':counts,'claim':'Counterexample to a universal extreme-population lower bound c*min(a,b); not an E45 construction.'}
 patch={'format':'exact_polygon_unit_v1','denominator':49,'tile':[3,5,7],'target':encode([region])[0],'triangles':encode(replacement),'tile_count':60}
 return certificate,patch
if __name__=='__main__':
 certificate,patch=build()
 (HERE/'equilateral_2160_extreme14.json').write_text(json.dumps(certificate,separators=(',',':'))+'\n')
 (HERE/'local_trade_60.json').write_text(json.dumps(patch,separators=(',',':'))+'\n')
 print('Constructed2160tiling:height populations774,1372,14;60tilepositive replacement.')
