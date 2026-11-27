"""Measure all gate displacements and formal-pair cancellations on full controls."""
from collections import Counter, defaultdict
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'joint-cell-tree'))
from controls import cell, geom, reconstruct, step


def check(name):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polys,centres,origin,*_ = geom.check_full_tiling(g,tiles)
    matched,pairs = geom.long_pairs(g,tiles,polys,centres,origin)
    lifts,T = reconstruct(g,tiles,polys)
    actual = defaultdict(lambda:g.point(0,0,0))
    headings = defaultdict(lambda:g.point(0,0,0))
    for i,t in enumerate(tiles):
        q,h,j,hand = t
        p,_,r = g.vertices(t)
        key = lifts[i],step(lifts[i],cell(g,h+hand,p))
        # The oriented CCW long side is r-to-p in the original geometry.
        headings[key] = g.add(headings[key],g.scale(-hand*g.c,g.unit(h+hand,j)))
        if i not in matched:
            actual[key] = g.add(actual[key],g.sub(p,r))
    ordinary = 0
    nonzero = 0
    for (v,w),z in headings.items():
        assert actual[v,w]==z
        if v==T[:1]:
            continue
        xy = geom.point(g,g.mult(g.unit(-v[-1][0],0),z))
        assert all((n/g.c).denominator==1 for n in xy)
        ordinary += 1
        nonzero += any(xy)
    for i,j in pairs:
        p,q,r = g.vertices(tiles[i])
        p1,q1,r1 = g.vertices(tiles[j])
        assert q1==g.sub(g.add(p,r),q)
        assert tiles[i][1]==tiles[j][1] and tiles[i][3]==tiles[j][3]
        assert (tiles[i][2]-tiles[j][2])%6==3
    return dict(ordinary_gates=ordinary,nonzero_ordinary_vectors=nonzero,actual_pairs=len(pairs))


if __name__=='__main__':
    import json
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps({s:check(s) for s in ('known','macro')},indent=2))
