"""Check the projected short currents directly on both complete 143 tilings."""
from collections import Counter
import json

from check import geom, reconstruct
from two_current import U


def check(which):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, which)
    polygons, centers, origin, _, _ = geom.check_full_tiling(g, tiles)
    matched, pairs = geom.long_pairs(g, tiles, polygons, centers, origin)
    lifts, _ = reconstruct(g, tiles, polygons)
    currents = Counter()
    ordinary = Counter()
    for i, tile in enumerate(tiles):
        lift = lifts[i]
        if len(lift) == 1:
            continue
        ordinary[lift] += 1
        _, height, _, _ = tile
        points = [geom.point(g, g.mult(g.unit(-height, 0), p)) for p in g.vertices(tile)]
        _, ox, oy = lift[-1]

        def residue(p):
            x, y = p[0] - ox, p[1] - oy
            assert x.denominator == y.denominator == 1
            return int(x) % g.c, int(y) % g.c

        for p, q in zip(points, points[1:]):
            axis, = [j for j in range(3) if geom.det(U[j], geom.sub(q, p)) == 0]
            currents[lift,axis,residue(p)] -= 1
            currents[lift,axis,residue(q)] += 1
    assert ordinary and not any(currents.values())
    for i, j in pairs:
        p, h, k, s = tiles[i]
        q, H, K, S = tiles[j]
        assert lifts[i] == lifts[j] and h == H and s == S and (k-K) % 6 == 3
        vertices = g.vertices(tiles[i])
        assert g.add(p,q) == g.add(vertices[0],vertices[-1])
    assert len(matched) == 2*len(pairs)
    return dict(ordinary_tiles=sum(ordinary.values()), ordinary_lifts=len(ordinary),
                endpoint_rows=len(currents), checked_pairs=len(pairs))


def owner_templates():
    from positioned_mixed import SOURCE
    from geometry import HEADINGS, shapes
    checks = 0
    for a,b,c in ((33,7,37),(35,13,43)):
        g = geom.Geometry(a,b,c)
        for s in (-1,1):
            for i,(_,q,w) in enumerate(shapes(a,b,c,s)):
                height, hand = (s,-s) if i<3 else (0,s)
                for exceptional in (False,True):
                    rotate = (i>=3) != exceptional
                    factor = -1 if rotate else 1
                    apex = g.point(q[0]*factor,q[1]*factor,1)
                    j = (HEADINGS[i]+3*(s==-1)+3*rotate)%6
                    tile = apex,height,j,hand
                    expected_sign = (-1 if i<3 else 1) * (-1 if exceptional else 1)
                    assert geom.eps(tile)==expected_sign
                    verts = g.vertices(tile)
                    tail,head = (verts[-1],verts[0]) if i<3 else (verts[0],verts[-1])
                    assert geom.point(g,tail)==(0,0)
                    assert tuple(c*x for x in geom.point(g,head))==tuple(factor*x for x in w)
                    checks += 1
    return checks


if __name__ == '__main__':
    result = {which:check(which) for which in ('known','macro')}
    result['oriented_mixed_templates'] = owner_templates()
    print(json.dumps(result, indent=2))
