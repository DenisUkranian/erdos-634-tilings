"""Compare native bank currents of the complete 143 tilings to the reference path."""
from pathlib import Path
import sys
from native_owners import UNITS, add, offsets, scale

ROOT = Path(__file__).resolve().parents[2]
# The original boundary-word support imports its own control module by name.
sys.path.insert(0,str(ROOT/'boundary-word'))
sys.path.insert(0,str(ROOT/'joint-cell-tree'))
from controls import cell, geom, reconstruct, step


def check(which):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,which)
    polys,centres,origin,*_ = geom.check_full_tiling(g,tiles)
    paired,_ = geom.long_pairs(g,tiles,polys,centres,origin)
    lifts,T = reconstruct(g,tiles,polys)
    B,C = T[:-1],T[:1]
    offset = g.scale(g.B,g.unit(2,0))
    def chart(p):
        reflected = g.sub(offset,g.mult(g.unit(2,1),(p[0]+p[1],-p[1],p[2])))
        xy = geom.point(g,g.mult(g.unit(-1,0),reflected))
        assert all(t.denominator==1 for t in xy)
        return tuple(map(int,xy))
    result = []
    for gate,hand in ((C,1),(T,-1)):
        currents = set()
        def toggle(p,q,j,exception):
            for m in (g.a,g.b):
                axis = (j + (hand if exception and m==g.a else 0))%3
                for x,y in (p,q):
                    currents.symmetric_difference_update([(m,axis,x%m,y%m)])
        bank = 0
        for i,t in enumerate(tiles):
            p,_,q = g.vertices(t)
            inside = lifts[i]
            other = step(inside,cell(g,t[1]+t[3],p))
            if {inside,other}!={gate,B} or i in paired:
                continue
            p,q = chart(p),chart(q)
            axes = offsets(g.a,g.b,g.c,hand,0)[0][:6]
            if inside==B:
                axes = [offsets(g.a,g.b,g.c,hand,j)[0][6] for j in range(6)]
            j = next(j for j,d in enumerate(axes) if add(p,d)==q)
            toggle(p,q,j,inside==B)
            bank += 1
        p = (0,0)
        for j in [0]*g.a+[5]*g.b:
            q = add(p,scale(g.c,UNITS[j]))
            toggle(p,q,j,False)
            p = q
        assert not currents
        result.append(bank)
    return result


if __name__=='__main__':
    import json
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps({k:check(k) for k in ('known','macro')},indent=2))
