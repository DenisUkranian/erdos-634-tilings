"""Exact macro-lozenge collar for the nonconvex pure-island counterexample."""
from collections import deque,Counter
from pathlib import Path
import json,hashlib,argparse

if not __debug__:
 raise SystemExit("Run this exact verifier without Python optimization (-O).")
P=[(0,0),(0,25),(15,10),(6,10),(6,-15),(-9,0)]
L=27
ROOT=Path(__file__).resolve().parent
def inside3(x,y,poly):
 # x,y are three times the query point. No centroid lies on the lattice boundary.
 winding=0
 for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]):
  z=(c-a)*(y-3*b)-(d-b)*(x-3*a)
  if 3*b<=y<3*d and z>0:winding+=1
  if 3*d<=y<3*b and z<0:winding-=1
 return winding!=0

def domain():
 U=set(); D=set();holeU=set();holeD=set()
 for i in range(-L,L):
  for j in range(-L,L):
   for q,S,H in [(1,U,holeU),(2,D,holeD)]:
    x=3*i+q;y=3*j+q
    if max(abs(x),abs(y),abs(x+y))<3*L:
     (H if inside3(x,y,P) else S).add((i,j))
 return U,D,holeU,holeD

def find_matching():
 U,D,_,_=domain()
 adj={u:[v for v in [u,(u[0]-1,u[1]),(u[0],u[1]-1)] if v in D] for u in U}; pu={};pd={}
 while True:
  dist={u:0 for u in U if u not in pu}; q=deque(sorted(dist));hit=False
  while q:
   u=q.popleft()
   for v in adj[u]:
    if v not in pd:hit=True
    elif pd[v] not in dist:
     uu=pd[v];dist[uu]=dist[u]+1;q.append(uu)
  if not hit:break
  def dfs(u):
   for v in adj[u]:
    if v not in pd or (dist.get(pd[v])==dist[u]+1 and dfs(pd[v])):
     pu[u]=v;pd[v]=u;return True
   dist[u]=-1;return False
  for u in sorted(U):
   if u not in pu:dfs(u)
 assert len(pu)==len(U)
 return {'L':L,'P':P,'lozenges':[[*u,*v] for u,v in sorted(pu.items())]}

def check(data):
 assert data['L']==L and data['P']==[list(p) for p in P]
 U,D,HU,HD=domain(); seenU=set();seenD=set();cnt=Counter();edge=Counter()
 def emit(t):
  for x,y in zip(t,t[1:]+t[:1]):
   if x<y:edge[(x,y)]+=1
   else:edge[(y,x)]-=1
 for i,j,k,l in data['lozenges']:
  u=(i,j);v=(k,l)
  assert u in U and v in D and u not in seenU and v not in seenD
  assert v in [u,(i-1,j),(i,j-1)]
  seenU.add(u);seenD.add(v);cnt[(k-i,l-j)]+=1
  emit([(i,j),(i+1,j),(i,j+1)])
  emit([(k+1,l),(k+1,l+1),(k,l+1)])
 assert seenU==U and seenD==D
 # Hole + shell cell boundaries equal the six exact outer sides.
 for i,j in HU:emit([(i,j),(i+1,j),(i,j+1)])
 for i,j in HD:emit([(i+1,j),(i+1,j+1),(i,j+1)])
 H=[(L,0),(0,L),(-L,L),(-L,0),(0,-L),(L,-L)]
 for p,q in zip(H,H[1:]+H[:1]):
  dx=(q[0]-p[0])//L;dy=(q[1]-p[1])//L
  for t in range(L):
   x=(p[0]+t*dx,p[1]+t*dy);y=(x[0]+dx,x[1]+dy)
   if x<y:edge[(x,y)]-=1
   else:edge[(y,x)]+=1
 assert all(v==0 for v in edge.values())
 # Hole union boundary equals P. P orientation is clockwise here.
 holeedges=Counter()
 def hemit(t):
  for x,y in zip(t,t[1:]+t[:1]):
   if x<y:holeedges[(x,y)]+=1
   else:holeedges[(y,x)]-=1
 for i,j in HU:hemit([(i,j),(i+1,j),(i,j+1)])
 for i,j in HD:hemit([(i+1,j),(i+1,j+1),(i,j+1)])
 for p,q in zip(P,P[1:]+P[:1]):
  s=max(abs(q[0]-p[0]),abs(q[1]-p[1]));dx=(q[0]-p[0])//s;dy=(q[1]-p[1])//s
  for t in range(s):
   x=(p[0]+t*dx,p[1]+t*dy);y=(x[0]+dx,x[1]+dy)
   if x<y:holeedges[(x,y)]+=1
   else:holeedges[(y,x)]-=1
 assert all(v==0 for v in holeedges.values())
 return {'result':'PASS','exact_integer_arithmetic':True,'collar_lozenges':len(U),'hole_unit_triangles':[len(HU),len(HD)],'lozenge_direction_counts':{str(k):v for k,v in sorted(cnt.items())},'hexagon_radius':L,'all_cells_matched_exactly_once':True,'hole_boundary_checked':True,'outer_boundary_checked':True}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--regenerate',action='store_true',help='Regenerate collar.json using the deterministic matching search.')
 ap.add_argument('--report',type=Path,help='Optionally save the verification report.')
 args=ap.parse_args()
 path=ROOT/'collar.json'
 if args.regenerate:
  path.write_text(json.dumps(find_matching(),separators=(',',':'))+'\n')
 report=check(json.loads(path.read_text()))
 report['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
