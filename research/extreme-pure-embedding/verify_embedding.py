"""Independent integer boundary-chain and corner-direction verifier.

Does not import verify_collar or its matching/winding routines.
The separate general-spectra checker verifies corner_base macrogeometry.
"""
from pathlib import Path
from collections import Counter
import json

if not __debug__:
 raise SystemExit("Run this exact verifier without Python optimization (-O).")
ROOT=Path(__file__).resolve().parent
c=json.loads((ROOT/'collar.json').read_text())
L=27
assert c['L']==L
P=[(0,0),(0,25),(15,10),(6,10),(6,-15),(-9,0)]
H=[(27,0),(0,27),(-27,27),(-27,0),(0,-27),(27,-27)]
T=[(27,27),(-54,27),(27,-54)]
assert c['P']==[list(p) for p in P]
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def area2(p):return sum(cross(x,y) for x,y in zip(p,p[1:]+p[:1]))
def rot60(v):return -v[1],v[0]+v[1]
def norm(v):return v[0]*v[0]+v[0]*v[1]+v[1]*v[1]
def minus(u,v):return u[0]-v[0],u[1]-v[1]
def emit(edges,p,sign=1):
 for x,y in zip(p,p[1:]+p[:1]):
  length=max(abs(y[0]-x[0]),abs(y[1]-x[1]))
  dx,dy=(y[0]-x[0])//length,(y[1]-x[1])//length
  assert norm((dx,dy))==1
  for k in range(length):
   a=(x[0]+k*dx,x[1]+k*dy); b=(a[0]+dx,a[1]+dy)
   edges[(a,b)]+=sign;edges[(b,a)]-=sign
edges=Counter();cells=set()
for i,j,k,l in c['lozenges']:
 up=((i,j),(i+1,j),(i,j+1)); down=((k+1,l),(k+1,l+1),(k,l+1))
 assert len(set(up)&set(down))==2
 for tri in (up,down):
  assert tri not in cells;cells.add(tri)
  assert area2(list(tri))==1
  assert all(max(abs(x),abs(y),abs(x+y))<=L for x,y in tri)
  emit(edges,list(tri))
emit(edges,H,-1);emit(edges,P,-1) # P is clockwise => shell boundary H+P
assert all(n==0 for n in edges.values())
assert len(cells)==area2(H)+area2(P)==3804
assert area2(P)==-570
# The corner interiors are separated from H by x=-L, y=-L, or x+y=L.
# Their positive boundary chains sum with H to the target boundary.
corners=[[(27,27),(0,27),(27,0)],
 [(27,-54),(27,-27),(0,-27)],
 [(-54,27),(-27,0),(-27,27)]]
edges=Counter();emit(edges,H)
for q in corners:
 assert area2(q)==L*L
 assert len({norm(minus(q[(i+1)%3],q[i])) for i in range(3)})==1
 emit(edges,q)
emit(edges,T,-1)
assert all(n==0 for n in edges.values())
assert area2(T)==81**2
# Exact direction-class test against class 0 and alpha=arg(5+3rho).
zdirs=[];v=(1,0)
for _ in range(6):zdirs.append(v);v=rot60(v)
adirs=[];v=(5,3)
for _ in range(6):adirs.append(v);v=rot60(v)
def cl(v):
 if any(cross(v,w)==0 for w in zdirs):return 0
 if any(cross(v,w)==0 for w in adirs):return -1
 raise AssertionError(('unexpected direction',v))
def tile_classes(tri,scale):
 shorts=[];long=[]
 for p,q in zip(tri,tri[1:]+tri[:1]):
  d=minus(q,p);n=norm(d)
  assert n in [9*scale*scale,25*scale*scale,49*scale*scale]
  (long if n==49*scale*scale else shorts).append(cl(d))
 assert len(long)==1 and len(shorts)==2 and shorts[0]==shorts[1]
 return shorts[0],long[0]
base=json.loads((ROOT/'corner_base.json').read_text())
count=0;types=Counter();strips=0
for r in base['regions']:
 if r['kind']=='similar_triangle':
  typ=tile_classes([tuple(p) for p in r['vertices']],r['scale'])
  assert typ in [(0,-1),(-1,0)]
  count+=(3*r['scale'])**2;types[typ]+=1
 else:
  A,B,C,D=map(tuple,r['vertices'])
  U=minus(B,A);V=minus(D,A)
  R=sum(x*y for x,y in zip(r['counts'],[5,3]))
  assert norm(U)==R*R and norm(V)==225
  # Scaled strip: length 3R along original U, length45 along original V.
  # Unit cells width3 along U/R and height5 along V/15.
  u=(3*U[0]//R,3*U[1]//R);v=(V[0]//3,V[1]//3)
  assert (R*u[0],R*u[1])==(3*U[0],3*U[1])
  assert tile_classes([(0,0),u,v],1)==(0,-1)
  assert norm(minus(u,v))==49
  assert tile_classes([u,(u[0]+v[0],u[1]+v[1]),v],1)==(0,-1)
  count+=18*R;strips+=1
assert count==535815
island=1862*225;shell=len(c['lozenges'])*1470;total=island+shell+3*count
assert total==4822335==(3*2835)**2//15
print(json.dumps({'result':'PASS','shell_lozenges':len(c['lozenges']),'shell_unit_cells':len(cells),'corner_macro_triangles':sum(types.values()),'corner_strips':strips,'corner_tile_count':count,'corner_short_long_levels':{str(k):v for k,v in types.items()},'strip_explicit_vectors':[[3,0],[-5,5],[8,-5]],'bad_island_tiles':island,'shell_tiles':shell,'all_tiles':total,'target_side':8505},indent=2))
