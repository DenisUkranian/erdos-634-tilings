#!/usr/bin/env python3
"""Independent through-owner and charge-reserve controls on full143 tilings."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from through_geometry import ExactGeometry, canonical, det, sub, scale

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
CONT=ROOT/'research/2026-11-20/semiprimes/continuation'
sys.path.insert(0,str(CONT/'global-endpoints/integer'))
from global_core_sat import Geometry


def complete_control(path):
    raw=path.read_bytes();data=json.loads(raw)
    tiles=[(tuple(t[0]),*t[1:]) for t in data['tiles']]
    assert data['sides']==[5,3,7] and len(tiles)==len(set(tiles))==143
    g=ExactGeometry(5,3,7);production=Geometry(5,3,7)
    polygons=[g.polygon(t) for t in tiles]
    vertices=set(p for polygon in polygons for p in polygon)
    incidences=[];owners=Counter();catalogues={}
    for index,(tile,polygon) in enumerate(zip(tiles,polygons)):
        assert g.admissible_polygon(polygon)
        for v,w in zip(polygon,polygon[1:]+polygon[:1]):
            # Reverse CCW edge so selected through tile occupies the right bank.
            start,end=w,v;vector=sub(end,start)
            decoded=[(h,j,L) for h in (tile[1]-1,tile[1],tile[1]+1)
                     for j in range(6) for L in (g.a,g.b,g.c)
                     if vector==scale(L,g.unit(h,j))]
            assert len(decoded)==1
            h,j,length=decoded[0]
            for p in vertices:
                dp=sub(p,start)
                if det(vector,dp):continue
                t=dp[0]/vector[0] if vector[0] else dp[1]/vector[1]
                if not 0<t<1:continue
                offset=t*length
                assert offset.denominator==1 and 1<=offset<=length-1
                catalogues[p,(h,j)]=g.owners(p,(h,j))
                assert canonical(polygon) in catalogues[p,(h,j)]
                owners[index]+=1
                incidences.append((index,p,h,j,int(offset)))
    odd=sum(t[3]*(-1 if t[2]%2 else 1) for t in tiles if t[1]%2)
    even=sum(t[3]*(-1 if t[2]%2 else 1) for t in tiles if not t[1]%2)
    assert (odd,even)==(-7,-2)
    reserves=[]
    for sigma in (-1,1):
        for tau in (-1,1):
            chosen=sum(t[3]*(-1 if t[2]%2 else 1)==(-sigma if t[1]%2 else -tau) for t in tiles)
            cap=(g.N+sigma*g.c+tau*(g.a-g.b))//2
            assert chosen==cap
            reserves.append(dict(sigma=sigma,tau=tau,full_population=chosen,capacity=cap))
    # Compare the independently constructed metric catalogue with production's
    # inverse catalogue, not just membership of the known selected owner.
    compared=0
    for p,ray in catalogues:
        encoded=next(q for t in tiles for q in production.vertices(t) if g.point(q)==p)
        rawset=set();u=production.unit(*ray)
        for off,h,j,s,_ in production.inverse(ray[0],ray[1]%3):
            reference=(production.add(encoded,off),h,j,s)
            vs=production.vertices(reference)
            for length in (g.a,g.b,g.c):
                end=production.add(encoded,production.scale(length,u))
                if end not in vs:continue
                third,=[q for q in vs if q not in (encoded,end)]
                if det(g.unit(*ray),sub(g.point(third),p))>=0:continue
                for offset in range(1,length):
                    candidate=(production.sub(reference[0],production.scale(offset,u)),h,j,s)
                    if production.admissible(candidate):rawset.add(canonical(g.polygon(candidate)))
        assert rawset==catalogues[p,ray]
        compared+=1
    return dict(source=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest(),
                through_incidences=len(incidences),distinct_through_tiles=len(owners),
                maximum_contacts_on_one_owner=max(owners.values()),
                independently_reconstructed_catalogues=compared,
                largest_contained_catalogue=max(map(len,catalogues.values())),
                odd_charge=odd,even_charge=even,charge_reserves=reserves)


def main():
    controls=[ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json',
              CONT/'global-endpoints/tiling_143.json']
    results=[complete_control(p) for p in controls]
    target_limits=[]
    for a,b,c in ((33,7,37),(35,13,43)):
        g=ExactGeometry(a,b,c)
        # Independent analytic shape checks at different directions/heights.
        shapes=0
        for h in range(-4,5):
            for j in range(6):
                assert len(g.six_shapes((0,0),(h,j)))==6
                shapes+=6
        target_limits.append(dict(tile=[a,b,c],raw_owner_limit=2*(a+b+c-3),metric_shapes_checked=shapes))
    result=dict(status='PASS',controls=results,target_raw_limits=target_limits,
                scope='Independent metric construction of six through shapes, complete integer-offset owner lists on actual143 contacts, and global charge capacities. No target exclusion.')
    (HERE/'THROUGH_GEOMETRY_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
