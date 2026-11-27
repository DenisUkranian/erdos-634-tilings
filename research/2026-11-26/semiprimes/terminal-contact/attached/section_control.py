"""Check every interval between projected vertex coordinates on both 143 controls."""
from fractions import Fraction
import json
from math import lcm
from pathlib import Path
import sys

import numpy as np

from sections import rotate, section

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'joint-cell-tree'))
from controls import geom


def check(name):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polys,centres,origin,*_ = geom.check_full_tiling(g,tiles)
    matched,pairs = geom.long_pairs(g,tiles,polys,centres,origin)
    shapes = [p+[p[0]] for i,p in enumerate(polys) if i not in matched]
    for i,j in pairs:
        shapes.append(polys[i]+[polys[j][1]])
    den = lcm(*(v.denominator for p in polys for point in p for v in point))
    shapes = np.array([[[int(v*den) for v in point] for point in obj] for obj in shapes])
    board = den*np.array([[0,0],[g.A,0],[0,g.B]],dtype=np.int64)
    runs = []
    for axis in range(3):
        x,y = rotate(shapes,axis)
        corners = np.unique(x)
        for left,right in zip(corners,corners[1:]):
            pos = 2*int(left)+1
            kept = section(board,shapes,axis,pos)
            assert np.array_equal(kept,shapes)
            # Independent direct partition. Use physical edge interpolation and
            # cancellation as a signed endpoint multiset, without graph pruning.
            probe = Fraction(pos,2)
            def crossings(poly):
                ans = []
                for (p,v),(q,w) in zip(poly,poly[1:]+poly[:1]):
                    p,v,q,w = map(int,(p,v,q,w))
                    if min(p,q)<probe<max(p,q):
                        ans.append(v+(probe-p)*Fraction(w-v,q-p))
                return sorted(ans)
            spans = []
            for xx,yy in zip(x,y):
                hit = crossings(list(zip(xx,yy)))
                if hit:
                    assert len(hit)==2
                    spans.append(hit)
            spans.sort()
            outline = crossings(list(zip(*rotate(board,axis))))
            assert [spans[0][0],spans[-1][1]]==outline
            assert all(s[1]==t[0] for s,t in zip(spans,spans[1:]))
        runs.append(len(corners)-1)
    return dict(actual_pairs=len(pairs),actual_singles=len(tiles)-len(matched),sections=runs)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps({name:check(name) for name in ('known','macro')},indent=2))
