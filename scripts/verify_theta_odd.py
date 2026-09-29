#!/usr/bin/env python3
"""Exact geometry replay for the 147- and 243-tile theta constructions.

Independent of the author's generator and separating-axis verifier. Uses convex
polygon clipping over Fraction, then atomizes all tile edges at every vertex.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json, argparse
from pathlib import Path

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")


def cross(a, b, p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])


def area(poly):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))


def metric(poly):
    return sorted((a[0]-b[0])**2+15*(a[1]-b[1])**2
                  for a,b in zip(poly,poly[1:]+poly[:1]))


def intersect(subject, boundary):
    out=list(subject)
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):
        inp=out; out=[]
        for p,q in zip(inp,inp[1:]+inp[:1]):
            fp,fq=cross(a,b,p),cross(a,b,q)
            if fp>=0:
                out.append(p)
            if fp*fq<0:
                t=F(fp,fp-fq)
                out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        if not out:
            break
    return out


def check(t, data_dir):
    count=3*t*t
    path=data_dir/f'theta-{count}.json'
    data=path.read_bytes(); obj=json.loads(data)
    assert {k:obj[k] for k in ('u','v','a','b','c','D','N')} == dict(u=1,v=2,a=2,b=3,c=4,D=15,N=count)
    den=obj['denominator']; assert type(den)==int and den>0
    outer=tuple(tuple(p) for p in obj['target'])
    tiles=[tuple(tuple(p) for p in tr) for tr in obj['tiles']]
    assert len(tiles)==count
    assert all(len(tr)==3 and all(len(p)==2 and all(type(x)==int for x in p) for p in tr) for tr in [outer]+tiles)
    assert area(outer)>0
    assert metric(outer)==sorted((den*s)**2 for s in (3*t,6*t,6*t))
    tile_area=F(3,2)*den*den
    assert tile_area.denominator==1
    for i,tr in enumerate(tiles):
        assert area(tr)==tile_area,(i,area(tr))
        assert metric(tr)==sorted((den*s)**2 for s in (2,3,4)),i
        assert all(cross(a,b,p)>=0 for a,b in zip(outer,outer[1:]+outer[:1]) for p in tr),i
    assert sum(area(tr) for tr in tiles)==area(outer)==count*tile_area
    pairs=contacts=0
    for i,j in combinations(range(count),2):
        poly=intersect(tiles[i],tiles[j]); pairs+=1
        if poly:
            contacts+=1
            assert area(poly)==0,(i,j,poly)
    assert pairs==count*(count-1)//2

    vertices=set(p for tr in [outer]+tiles for p in tr)
    def atoms(tr):
        result=[]
        for a,b in zip(tr,tr[1:]+tr[:1]):
            pts=[p for p in vertices if cross(a,b,p)==0
                 and min(a[0],b[0])<=p[0]<=max(a[0],b[0])
                 and min(a[1],b[1])<=p[1]<=max(a[1],b[1])]
            pts.sort(key=lambda p:(p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))
            result.extend(zip(pts,pts[1:]))
        return result
    edges=Counter(e for tr in tiles for e in atoms(tr))
    boundary=Counter(atoms(outer)); inside=outside=0
    for a,b in {tuple(sorted(e)) for e in edges}:
        if boundary[a,b] or boundary[b,a]:
            assert (edges[a,b],edges[b,a])==(boundary[a,b],boundary[b,a])
            outside+=1
        else:
            assert (edges[a,b],edges[b,a])==(1,1)
            inside+=1
    assert outside==len(boundary)
    return dict(verdict='PASS',t=t,N=count,sha256=sha256(data).hexdigest(),
                tile_sides=[2,3,4],target_sides=[3*t,6*t,6*t],
                denominator=den,metric_y_square=15,
                each_tile_area='3*sqrt(15)/4',target_area=f'{3*count}*sqrt(15)/4',
                tested_pairs=pairs,zero_area_contact_pairs=contacts,
                positive_area_pair_intersections=0,vertices=len(vertices),
                interior_atomic_edges=inside,boundary_atomic_edges=outside,
                generator_imported=False,author_sat_used=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'data')
    args=parser.parse_args()
    print(json.dumps([check(t,args.data_dir) for t in (7,9)],indent=2))
