#!/usr/bin/env python3
"""Exact (3,5,7) pure-island counterexample; standard library only.

Outputs an explicit unit-triangle witness and a verification report beside
this script. This refutes general pure nonconvex chirality exchange, not
Erdos problem 634. No optimizer, floating point, or search is used.
"""
import os
if not __debug__ or os.environ.get("PYTHONOPTIMIZE"):
    raise SystemExit("Use ordinary Python without -O/-OO/PYTHONOPTIMIZE.")

from collections import defaultdict
from fractions import Fraction
from math import gcd
from pathlib import Path
import json

A,B,C = 3,5,7
ROOT=Path(__file__).resolve().parent

def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(k,p):return k*p[0],k*p[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def orient(p,q,r):return cross(sub(q,p),sub(r,p))
def area2(v):return sum(cross(v[i],v[(i+1)%len(v)]) for i in range(len(v)))
def ccw(t):return tuple(t) if area2(t)>0 else tuple(reversed(t))
def rot(p):return -p[1],p[0]+p[1]
def key(t):
    p=min(t)
    return tuple(sorted(sub(q,p) for q in t))

def subdivide(t,n):
    p,q,r=t
    assert all(x%n==0 for x in sub(q,p)+sub(r,p))
    v=tuple(x//n for x in sub(q,p));w=tuple(x//n for x in sub(r,p))
    out=[]
    for i in range(n):
        for j in range(n-i):
            z=add(p,add(mul(i,v),mul(j,w)))
            out.append(ccw((z,add(z,v),add(z,w))))
            if i+j<n-1:
                out.append(ccw((add(z,v),add(z,add(v,w)),add(z,w))))
    assert len(out)==n*n
    return out

def in_triangle(p,t):
    t=ccw(t)
    return all(orient(t[i],t[(i+1)%3],p)>=0 for i in range(3))

def overlap_interior(t,s):
    # Exact separating-axis theorem, including zero-width boundary contacts.
    if max(p[0] for p in t)<=min(p[0] for p in s):return False
    if max(p[0] for p in s)<=min(p[0] for p in t):return False
    if max(p[1] for p in t)<=min(p[1] for p in s):return False
    if max(p[1] for p in s)<=min(p[1] for p in t):return False
    for f,g in ((ccw(t),s),(ccw(s),t)):
        for i in range(3):
            if all(orient(f[i],f[(i+1)%3],p)<=0 for p in g):return False
    return True

def add_edge(events,p,q,weight=1):
    dx,dy=sub(q,p);d=gcd(abs(dx),abs(dy));assert d
    dx//=d;dy//=d
    if dx<0 or (dx==0 and dy<0):dx=-dx;dy=-dy
    line=(dx,dy,dx*p[1]-dy*p[0])
    t0=dx*p[0]+dy*p[1];t1=dx*q[0]+dy*q[1]
    sign=weight if t1>t0 else -weight
    lo,hi=sorted((t0,t1))
    events[line][lo]+=sign;events[line][hi]-=sign

def check_boundary(tiles,polygon):
    events=defaultdict(lambda:defaultdict(int))
    for t in tiles:
        for i in range(3):add_edge(events,t[i],t[(i+1)%3])
    p=tuple(polygon) if area2(polygon)>0 else tuple(reversed(polygon))
    for i in range(len(p)):add_edge(events,p[i],p[(i+1)%len(p)],-1)
    assert all(all(value==0 for value in e.values()) for e in events.values())
    return len(events)

def main():
    a,b,c=A,B,C
    assert a*a+a*b+b*b==c*c
    O=(0,0);P=(b**3,a*b*b);Q=(b**3+a*a*b,-a*a*b)
    S=(b**3-a**3,0);F=(b**3,0)
    polygon=[O,P,Q,S,sub(S,P),sub(S,Q)]
    macros=[((O,P,F),b*b),((P,Q,F),a*b),((Q,S,F),a*a)]
    macros += [(tuple(sub(S,p) for p in t),n) for t,n in macros[:]]
    macro_triangles=[ccw(t) for t,n in macros]
    assert all(not overlap_interior(macro_triangles[i],macro_triangles[j])
               for i in range(6) for j in range(i))
    rotations={}
    ref=((0,0),(a+b,-b),(a,0))
    for j in range(6):
        rotations[key(ref)]=j
        ref=tuple(rot(p) for p in ref)
    assert len(rotations)==6
    tiles=[];macro_ids=[];rotation_ids=[];counts=[0,0,0]
    for k,(t,n) in enumerate(macros):
        pieces=subdivide(t,n)
        assert sum(area2(s) for s in pieces)==abs(area2(t))
        for s in pieces:
            assert area2(s)==a*b
            assert all(in_triangle(p,t) for p in s)
            j=rotations[key(s)]
            counts[j%3]+=1
            tiles.append(s);macro_ids.append(k);rotation_ids.append(j)
    assert counts==[162,1250,450]
    assert len(tiles)==1862
    pair_checks=0
    for i,t in enumerate(tiles):
        for j in range(i):
            assert not overlap_interior(t,tiles[j]),(i,j)
            pair_checks+=1
    assert abs(area2(polygon))==sum(area2(t) for t in tiles)
    line_count=check_boundary(tiles,polygon)
    u=(a+b,-b);w=(b,a);v=(-a,a+b)
    expected=[mul(b*b,w),mul(-a*b,v),mul(-a*a,u),
              mul(-b*b,w),mul(a*b,v),mul(a*a,u)]
    assert [sub(polygon[(i+1)%6],polygon[i]) for i in range(6)]==expected
    M=[[-a*b,a*(a+b),b*(a+b)],
       [b*(a+b),-a*b,a*(a+b)],
       [a*(a+b),b*(a+b),-a*b]]
    opposite=[sum(Fraction(M[i][j],c*c)*counts[j] for j in range(3))
              for i in range(3)]
    assert opposite==[930,-30,962]
    witness={'tile_sides':[a,b,c], 'coordinates':'short Eisenstein basis (1, exp(i*pi/3))',
             'polygon':polygon, 'macro_triangles':macro_triangles,
             'macro_scales':[n for t,n in macros], 'unit_triangles':tiles,
             'macro_index':macro_ids, 'rotation_index':rotation_ids}
    report={'status':'PASS','full_Erdos634_solved':False,'scope':'counterexample to universal nonconvex pure chirality exchange; not a solution of Erdos 634',
            'tile_sides':[a,b,c],'unit_tiles':len(tiles),'orientation_pair_populations':counts,
            'forced_opposite_populations':[int(x) for x in opposite],
            'negative_opposite_population':-30,'unit_pair_checks':pair_checks,
            'macro_pair_checks':15,'boundary_supporting_lines':line_count,
            'signed_coordinate_area_twice':area2(polygon),
            'checks':['six allowed pure rotations only','all unit tile areas exact',
                      'all units contained in their macro triangles','all macro interiors disjoint',
                      'all unit interiors pairwise disjoint','total polygon area equality',
                      'exact atomized boundary cancellation','all outer edges whole long-edge multiples',
                      'negative opposite-state boundary inventory']}
    (ROOT/'witness_3_5_7.json').write_text(json.dumps(witness,separators=(',',':'))+'\n')
    (ROOT/'verified.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
