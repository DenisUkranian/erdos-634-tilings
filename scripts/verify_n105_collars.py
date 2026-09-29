#!/usr/bin/env python3
"""Independent exact verification of partial boundary-collar certificates.

No generator imports. Geometry uses Fraction convex clipping for intersection
tests, and an independently atomized oriented boundary for the residual region.
These certificates are partial tilings, never complete 105-tile tilings.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")

REPO = Path(__file__).resolve().parents[1]

def det(p,q,r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])

def area2(p):
    return sum(x[0]*y[1]-x[1]*y[0] for x,y in zip(p,p[1:]+p[:1]))

def clip(polygon,clip_triangle):
    p=[tuple(map(Q,x)) for x in polygon]
    for j in range(3):
        if not p:break
        x,y=clip_triangle[j],clip_triangle[(j+1)%3]
        result=[]
        for u,v in zip(p,p[1:]+p[:1]):
            su,sv=det(x,y,u),det(x,y,v)
            if su>=0:result.append(u)
            if (su<0 and sv>0) or (su>0 and sv<0):
                t=su/(su-sv)
                result.append((u[0]+t*(v[0]-u[0]),u[1]+t*(v[1]-u[1])))
        p=result
    return p

def verify(path, expected):
    raw=path.read_bytes();obj=json.loads(raw)
    expected_tile,expected_count,expected_remaining,expected_vertices,expected_margin=expected
    assert obj['tile']==expected_tile and obj['count']==expected_count
    assert obj['vertices_are_oblique'] is True
    a,b,c=obj['tile'];D=obj['scale'];L=obj['side']*D
    assert type(D) is int and D==a*b*c*c
    assert all(len(t)==3 and all(len(p)==2 and all(type(x) is int for x in p) for p in t) for t in obj['triangles'])
    assert obj['side']==105 and c*c==a*a-a*b+b*b
    triangles=[tuple(map(tuple,t)) for t in obj['triangles']]
    assert len(set(tuple(sorted(t)) for t in triangles))==len(triangles)==obj['count']
    for t in triangles:
        assert det(*t)==a*b*D*D
        assert all(x>=0 and y>=0 and x+y<=L for x,y in t)
        squared=[]
        for p,q in zip(t,t[1:]+t[:1]):
            x,y=q[0]-p[0],q[1]-p[1]
            squared.append(Q(x*x+x*y+y*y,D*D))
        assert sorted(squared)==sorted([a*a,b*b,c*c])
    pair_checks=0
    for i,t in enumerate(triangles):
        for u in triangles[:i]:
            assert area2(clip(t,u))==0
            pair_checks+=1

    outer=((0,0),(L,0),(0,L))
    vertices=set(outer)|{p for t in triangles for p in t}
    edges=list(zip(outer,outer[1:]+outer[:1]))
    edges += [(q,p) for t in triangles for p,q in zip(t,t[1:]+t[:1])]
    atoms=Counter()
    for p,q in edges:
        cuts=[r for r in vertices if det(p,q,r)==0 and
              (r[0]-p[0])*(r[0]-q[0])+(r[1]-p[1])*(r[1]-q[1])<=0]
        cuts.sort(key=lambda r:(r[0]-p[0])*(q[0]-p[0])+(r[1]-p[1])*(q[1]-p[1]))
        atoms.update(zip(cuts,cuts[1:]))
    for p,q in list(atoms):
        n=min(atoms[p,q],atoms[q,p]);atoms[p,q]-=n;atoms[q,p]-=n
    out=defaultdict(list)
    for (p,q),n in atoms.items():
        assert n in (0,1)
        if n:out[p].append(q)
    assert all(len(qs)==1 for qs in out.values())
    assert Counter(qs[0] for qs in out.values())==Counter(out.keys())
    residual_vertices=set(out)
    margin=min(Q(min(x,y,L-x-y),D) for x,y in residual_vertices)
    assert margin>0, 'The residual must stay strictly away from every outer side.'
    loops=[]
    while out:
        start=next(iter(out));cur=start;polygon=[]
        while True:
            polygon.append(cur);cur=out.pop(cur)[0]
            if cur==start:break
        loops.append(polygon)
    assert len(loops)==1
    residual_tiles=Q(area2(loops[0]),a*b*D*D)
    assert residual_tiles>0 and residual_tiles+len(triangles)==105
    assert residual_tiles==expected_remaining
    assert len(loops[0])==expected_vertices and margin==expected_margin
    return dict(verdict='PASS_PARTIAL_COLLAR_ONLY',certificate=path.name,
                sha256=sha256(raw).hexdigest(),tile=[a,b,c],target_side=105,
                placed_tiles=len(triangles),intersection_pairs_checked=pair_checks,
                residual_components=1,residual_boundary_vertices=len(loops[0]),
                residual_area_in_tile_units=str(residual_tiles),
                minimum_oblique_boundary_margin=str(margin),
                exact_metric='(x*x+x*y+y*y)/scale**2',
                coordinate_basis='(1,0),(1/2,sqrt(3)/2)',
                complete_tiling=False)

if __name__=='__main__':
    expected=[([5,21,19],45,60,38,Q(25,19)),
              ([7,15,13],57,48,44,Q(49,13))]
    if len(sys.argv) not in (1,3):
        raise SystemExit("Usage: verify_n105_collars.py [CERTIFICATE_5_21_19 CERTIFICATE_7_15_13]")
    paths=[Path(p) for p in sys.argv[1:]] if len(sys.argv)==3 else [
        REPO/'data/n105-collar-5-21-19.json',
        REPO/'data/n105-collar-7-15-13.json']
    results=[verify(path,claim) for path,claim in zip(paths,expected)]
    print(json.dumps(dict(verdict='PASS',scope='partial_boundary_collars_only',
                          complete_tiling=False,certificates=results),indent=2))
