#!/usr/bin/env python3
"""Independent exact replay of data/tiling-322.json.

Does not import or execute the author generator. Uses rational polygon clipping,
not a separating-axis test, for all 51,681 tile pairs. The physical coordinate
map is (X,Y) -> (X/18,Y*sqrt(32)/18).
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json, sys
if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")

from pathlib import Path

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data/tiling-322.json'
data=path.read_bytes(); obj=json.loads(data)
# Fix the mathematical claim independently of the certificate metadata.
assert {k:obj[k] for k in ('u','v','a','b','c','D','Q','P','N','denominator')} == dict(u=2,v=3,a=6,b=5,c=9,D=32,Q=14,P=23,N=322,denominator=18)
ts=[tuple(tuple(p) for p in t) for t in obj['tiles']]
outer=tuple(tuple(p) for p in obj['target'])
assert len(ts)==322
assert len(outer)==3 and all(len(t)==3 for t in ts)
assert all(len(p)==2 and all(type(x)==int for x in p) for t in ts+[outer] for p in t)

def turn(a,b,p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
def area2(poly):
    return sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))
def sides2(poly):
    return sorted((poly[i][0]-poly[(i+1)%3][0])**2+32*(poly[i][1]-poly[(i+1)%3][1])**2 for i in range(3))
def clip(poly,a,b):
    """Closed halfplane clip, retaining both crossings and boundary contact."""
    ans=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        fp,fq=turn(a,b,p),turn(a,b,q)
        if fp>=0:
            ans.append(p)
        if (fp<0 and fq>0) or (fp>0 and fq<0):
            r=F(fp,fp-fq)
            ans.append((p[0]+r*(q[0]-p[0]),p[1]+r*(q[1]-p[1])))
    return ans

def intersection(a,b):
    p=list(a)
    for x,y in zip(b,b[1:]+b[:1]):
        if not p: break
        p=clip(p,x,y)
    return p

assert area2(outer)>0
assert sides2(outer)==sorted((18*s)**2 for s in (81,115,126))
for i,t in enumerate(ts):
    assert area2(t)==1620,(i,area2(t))
    assert sides2(t)==sorted((18*s)**2 for s in (5,6,9)),(i,sides2(t))
    # Each tile is wholly in the convex outer triangle iff its vertices are.
    assert all(turn(outer[k],outer[(k+1)%3],p)>=0 for k in range(3) for p in t),i
assert sum(map(area2,ts))==area2(outer)==521640
pair_count=contact_pairs=0
for i,j in combinations(range(322),2):
    polygon=intersection(ts[i],ts[j]); pair_count+=1
    if polygon:
        contact_pairs+=1
        assert area2(polygon)==0,(i,j,polygon,area2(polygon))
assert pair_count==51681

# Independent boundary-chain consistency. Split every tile edge at *every*
# certificate vertex lying on it, so T-junctions are explicitly accommodated.
vertices=set(p for t in ts for p in t)|set(outer)
def atoms(poly):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1]
        on=[p for p in vertices if turn(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])]
        on.sort(key=lambda p:(p[0]-a[0])*dx+(p[1]-a[1])*dy)
        out.extend(zip(on,on[1:]))
    return out
counts=Counter(e for t in ts for e in atoms(t))
boundary=Counter(atoms(outer))
interior_atoms=boundary_atoms=0
for a,b in set(tuple(sorted(e)) for e in counts):
    ab,ba=counts[a,b],counts[b,a]
    if boundary[a,b] or boundary[b,a]:
        assert (ab,ba)==(boundary[a,b],boundary[b,a]),((a,b),ab,ba)
        boundary_atoms+=1
    else:
        assert (ab,ba)==(1,1),((a,b),ab,ba)
        interior_atoms+=1
assert boundary_atoms==len(boundary)
# Count distinct T-junction vertices using the original, unsplit tile edges.
t_vertices=set()
for t in ts:
    for a,b in zip(t,t[1:]+t[:1]):
        t_vertices.update(p for p in vertices if p not in (a,b) and turn(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]))
result=dict(verdict='PASS',certificate_sha256=sha256(data).hexdigest(),tile_count=322,tile_sides=[5,6,9],target_sides=[81,115,126],coordinate_denominator=18,metric_y_square=32,each_tile_area='10*sqrt(2)',target_area='3220*sqrt(2)',all_tile_pair_intersections_tested=pair_count,zero_area_contact_pairs=contact_pairs,positive_area_pair_intersections=0,distinct_certificate_vertices=len(vertices),distinct_t_junction_vertices=len(t_vertices),interior_atomic_edges=interior_atoms,boundary_atomic_edges=boundary_atoms,author_code_imported=False,author_sat_used=False)
print(json.dumps(result,indent=2))

