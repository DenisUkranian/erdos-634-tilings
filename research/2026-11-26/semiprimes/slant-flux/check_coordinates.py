"""Verify the slant cut by physical contact lifts in each full 143 control."""
from collections import Counter
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'joint-cell-tree'))
from controls import geom, reconstruct, step, cell


def control(name):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, name)
    polygons, *_ = geom.check_full_tiling(g, tiles)
    lifts, slant = reconstruct(g, tiles, polygons)
    middle = slant[:-1]
    origin = g.scale(g.B, g.unit(2, 0))

    def reflect(p):
        return g.sub(origin, g.mult(g.unit(2, 1), (p[0]+p[1], -p[1], p[2])))

    banks = {'B': g.point(0,0,0), 'T': g.point(0,0,0)}
    currents = Counter()
    core = middle[:-1]
    outgoing = Counter()
    charges = Counter()
    wall_edges = [[], []]
    for i, (q, h, j, s) in enumerate(tiles):
        u = g.add(q, g.scale(-g.a, g.unit(h,j)))
        long = step(lifts[i], cell(g, h+s, u))
        cut = lifts[i], long
        charges[lifts[i],h%2] -= geom.eps(tiles[i])
        if lifts[i] == core:
            assert h == 0
            x,y = geom.point(g,u)
            assert x.denominator == y.denominator == 1
            native = s == 1 and (g.a*y-g.b*x-g.a*g.B)%g.c == 0
            assert native == (long == middle)
            outgoing[long] -= geom.eps(tiles[i])
        used = 0
        for poly_index,(p,t) in enumerate(zip(polygons[i],polygons[i][1:]+polygons[i][:1])):
            if p[1]==t[1]==0:
                side,start,end=0,p[0],t[0]
            elif p[0]==t[0]==0:
                side,start,end=1,g.B-p[1],g.B-t[1]
            else:
                continue
            assert start.denominator==end.denominator==1
            length=int(end-start)
            assert length in (g.a,g.b,g.c)
            if length != g.c:
                assert poly_index<2 and lifts[i]==core
                assert geom.eps(tiles[i])==(1 if length==g.a else -1)
                used+=1
            wall_edges[side].append((int(start),int(end)))
        assert used<=1
        if cut not in ((middle, slant), (slant, middle)):
            continue
        bank = 'B' if cut[0] == middle else 'T'
        h1, j1, s1 = 2-h, (4-j)%6, -s
        assert (h1, s1) == ((1,-1) if bank == 'B' else (0,1))
        up = g.mult(g.unit(-h1, 0), reflect(u))
        x, y = geom.point(g, up)
        assert x.denominator == y.denominator == 1
        assert ((g.a*x-g.b*y) if s1 == -1 else (g.a*y-g.b*x)) % g.c == 0
        amount = g.scale(g.c, g.unit(h1+s1,j1))
        actual = g.sub(reflect(g.vertices(tiles[i])[-1]), reflect(g.vertices(tiles[i])[0]))
        # Reflection reverses the CCW long edge; compare its directed displacement.
        assert actual == g.scale(-s1,amount)
        banks[bank] = g.add(banks[bank], amount)
        currents[bank] += s1*(-1)**j1
    for direction in set(p[:2] for p,_ in charges if len(p)>=2) - {middle}:
        even=sum(G for (p,k),G in charges.items() if p[:2]==direction and k==0)
        odd=sum(G for (p,k),G in charges.items() if p[:2]==direction and k==1)
        assert g.c*outgoing[direction]==(g.a-g.b)*odd-g.c*even
    for wall,length in zip(wall_edges,(g.A,g.B)):
        cursor=0
        for left,right in sorted(wall):
            assert left==cursor
            cursor=right
        assert cursor==length
    assert g.add(banks['B'], banks['T']) == g.point(g.c**2,0,0)
    return {k:dict(displacement=[str(t) for t in geom.point(g,v)], signed=currents[k])
            for k,v in banks.items()}


if __name__ == '__main__':
    print(control('known'), control('macro'))
