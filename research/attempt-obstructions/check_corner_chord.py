"""Exact partial-corner configuration; emphatically not a full tiling.
Coordinates (x,y) have Euclidean metric diag(1,h2). Target equal side 1.
A chord endpoint contains sqrt(z), isolated by rational arithmetic.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path
u=51;v=u+1;a=u*v;b=v*v-u*u;c=v*v;S=F(b*v*v,2)
r=F(u,v);h2=1-r*r/4;e=F(b,S);f=F(c,S);ell=F(u*v*v,S)
A=(F(0),F(1));B=(-r/2,F(0));C=(r/2,F(0))
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def mul(t,p):return tuple(t*x for x in p)
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def orient(p,q,r):return cross(sub(q,p),sub(r,p))
def square(p,q):
 d=sub(p,q);return d[0]*d[0]+h2*d[1]*d[1]
E=add(A,mul(e,sub(B,A)));K=add(A,mul(f,sub(C,A)))
def corner_fan(O,leg,base):
 U=add(O,mul(F(b,S),sub(leg,O))) # Equal side has length 1.
 V=add(O,mul(F(a,S*r),sub(base,O))) # Base has length r.
 W=sub(add(U,V),O)
 return [(O,U,W),(O,W,V)]
tiles=[(A,E,K)]+corner_fan(B,A,C)+corner_fan(C,A,B)
want=sorted([F(a,S)**2,F(b,S)**2,F(c,S)**2])
for tri in tiles:
 assert sorted(square(tri[i],tri[(i+1)%3]) for i in range(3))==want
 for p in tri:
  assert all(orient((A,B,C)[i],(A,B,C)[(i+1)%3],p)>=0 for i in range(3))
def disjoint(P,Q):
 for T in [P,Q]:
  for i in range(3):
   edge=sub(T[(i+1)%3],T[i]);n=(-edge[1],edge[0])
   pp=[p[0]*n[0]+p[1]*n[1] for p in P];qq=[p[0]*n[0]+p[1]*n[1] for p in Q]
   if max(pp)<=min(qq) or max(qq)<=min(pp):return True
 return False
for i in range(5):
 for j in range(i):assert disjoint(tiles[i],tiles[j])
# X=(E.x+sqrt(z),0). Chord length is ell in the Euclidean metric.
z=ell*ell-h2*E[1]*E[1]
assert z>0
precision=10**50;root=isqrt(z.numerator*precision**2//z.denominator)
lo=F(root,precision);hi=F(root+1,precision)
assert lo*lo<z<hi*hi
# Certified interval for p+q sqrt(z).
def iv(p,q=F(0)):
 return (p+q*lo,p+q*hi) if q>=0 else (p+q*hi,p+q*lo)
def positive(p,q=F(0)):assert iv(p,q)[0]>0,(p,q,iv(p,q))
def negative(p,q=F(0)):assert iv(p,q)[1]<0,(p,q,iv(p,q))
# X lies strictly within the target base, to the right of its midpoint.
positive(E[0],1);positive(C[0]-E[0],-1)
# Signed line value cross(X-E,P-E) = E.y*(P.x-E.x) +(P.y-E.y)*sqrt(z).
def side(p):return E[1]*(p[0]-E[0]),p[1]-E[1]
# Apex tile touches the chord only at E; two C tiles are strictly on positive side;
# both B tiles are strictly on negative side. Hence all five interiors avoided.
for p in tiles[0]:
 if p!=E:positive(*side(p))
for tri in tiles[1:3]:
 for p in tri:negative(*side(p))
for tri in tiles[3:5]:
 for p in tri:positive(*side(p))
# First check the ambient quadrilateral after only the apex tile is removed.
# Its width is not the width of the actual unfilled region after all five tiles.
positive(*(sub(side(C),side(K))))
# -line(B) > line(C).
positive(-side(B)[0]-side(C)[0],-side(B)[1]-side(C)[1])
# Distances divide line values by ell and multiply by sqrt(h2).
# c sin(theta)/S = (c/S)*sqrt(h2) = f*sqrt(h2).
positive(side(C)[0]-f*ell,side(C)[1])
ratio_interval=iv(side(C)[0]/(f*ell),side(C)[1]/(f*ell))
# Actual unfilled polygon after removing all five corner tiles. Each corner fan
# is a parallelogram O,U,W,V. Its exposed boundary replaces O by U,W,V.
UB,WB,VB=tiles[1][1],tiles[1][2],tiles[2][2]
UC,WC,VC=tiles[3][1],tiles[3][2],tiles[4][2]
complement=[E,UB,WB,VB,VC,WC,UC,K]
def area2(P):return sum(cross(P[i],P[(i+1)%len(P)]) for i in range(len(P)))
assert area2(complement)>0
assert area2(complement)+sum(abs(area2(T)) for T in tiles)==area2([A,B,C])
# Check that the displayed complement boundary is simple. Nonadjacent edges
# have no proper crossing or collinear contact (all orientation signs strict
# except intentionally adjacent target-boundary pieces).
def between(p,q,x):
 return orient(p,q,x)==0 and all(min(p[i],q[i])<=x[i]<=max(p[i],q[i]) for i in [0,1])
def edges_intersect(p,q,r,s):
 o1,o2,o3,o4=orient(p,q,r),orient(p,q,s),orient(r,s,p),orient(r,s,q)
 return o1*o2<0 and o3*o4<0 or any([between(p,q,r),between(p,q,s),between(r,s,p),between(r,s,q)])
for i in range(len(complement)):
 for j in range(i):
  if (i-j)%len(complement) in (1,len(complement)-1):continue
  assert not edges_intersect(complement[i],complement[(i+1)%len(complement)],complement[j],complement[(j+1)%len(complement)])
# Exact ear triangulation additionally checks disjointness from the occupied
# corner tiles. Together with target containment and the area identity above,
# this certifies that the polygon is the closure of the actual unfilled region.
pending=list(complement);complement_triangles=[]
while len(pending)>3:
 for j in range(len(pending)):
  ear=(pending[j-1],pending[j],pending[(j+1)%len(pending)])
  if area2(ear)<=0:continue
  others=[p for p in pending if p not in ear]
  if any(all(orient(ear[k],ear[(k+1)%3],p)>=0 for k in range(3)) for p in others):continue
  complement_triangles.append(ear);pending.pop(j);break
 else:raise AssertionError('No exact ear found')
complement_triangles.append(tuple(pending))
assert sum(area2(T) for T in complement_triangles)==area2(complement)
for T in complement_triangles:
 for occupied in tiles:assert disjoint(T,occupied)
# Linear support extrema over a polygon occur at vertices. Intersecting it
# with either closed half-plane introduces only zero-distance vertices.
for p in complement:
 if p!=UC:positive(*sub(side(UC),side(p)))
 if p!=UB:positive(*sub(side(p),side(UB)))
positive(*side(UC));negative(*side(UB))
positive(-side(UB)[0]-side(UC)[0],-side(UB)[1]-side(UC)[1])
positive(side(UC)[0]-f*ell,side(UC)[1])
complement_ratio_interval=iv(side(UC)[0]/(f*ell),side(UC)[1]/(f*ell))
record={
 'status':'exactly verified partial configuration; not a complete tiling',
 'u':u,'v':v,'tile_sides':[a,b,c], 'target_equal_side':str(S),
 'seam_length':u*v*v,'corner_tiles':5,
 'normalized_metric_h2':str(h2),'z':str(z),
 'sqrt_z_lower':str(lo),'sqrt_z_upper':str(hi),
 'ambient_quadrilateral_width_over_required_height_lower':str(ratio_interval[0]),
 'ambient_quadrilateral_width_over_required_height_upper':str(ratio_interval[1]),
 'approximate_ambient_quadrilateral_ratio':float(sum(ratio_interval)/2),
 'complement_polygon':[[str(x) for x in p] for p in complement],
 'complement_width_over_required_height_lower':str(complement_ratio_interval[0]),
 'complement_width_over_required_height_upper':str(complement_ratio_interval[1]),
 'approximate_complement_ratio':float(sum(complement_ratio_interval)/2),
 'claims_checked':['five congruent corner tiles','target containment','all 10 tile pairs have disjoint interiors','chord length exact','chord avoids all five tile interiors','actual complement boundary is simple and has the correct area','exact complement triangulation is disjoint from all five corner tiles','actual complement closure has support extrema at U_C and U_B','its smaller-side width exceeds c sin(theta)'],
 'not_claimed':['the chord is an actual tile-edge chain','a swapped alpha-gap tile fits in the complement','the five tiles extend to a complete tiling']}
Path(__file__).with_name('corner_chord_certificate.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if 'lower' not in k and 'upper' not in k},indent=2))
