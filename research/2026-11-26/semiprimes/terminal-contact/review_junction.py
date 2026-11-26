"""Independent local certificate at X, using the repository's standard-frame tiles."""
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"boundary-word"))
from rectangle import geom,overlap


def families(g,cut,depth):
    a,b,c=g.a,g.b,g.c
    caps=((c-a,c+b,c-a+b),(c,b,c-a))[cut]
    types=(((1,0,-1),(1,4,-1),(0,0,1)),((2,4,-1),(1,0,1),(1,4,1)))[cut]
    allowed={a*i+b*j for i in range(g.B//a+1) for j in range(g.B//b+1)}
    @lru_cache(None)
    def owner(end,j):
        h,index,hand=types[j]
        shape=g.vertices(((0,0,0),h,index,hand))
        tip=shape[0] if hand==-1 else shape[-1]
        anchor=g.sub(end,tip)
        verts=g.vertices((anchor,h,index,hand))
        poly=tuple(geom.point(g,p) for p in verts)
        start=verts[-1] if hand==-1 else verts[0]
        if any(x<0 or y<0 or g.B*x+g.A*y>g.A*g.B for x,y in poly):
            return start,None
        return start,poly
    def paths(s,end,polys):
        if len(polys)==depth:
            yield polys
            return
        for j in range(3):
            if not s[j]:
                continue
            rest=list(s)
            rest[j]-=1
            i,k,l=rest
            if cut==0 and j!=1 and g.B-c*k+b*l not in allowed:
                continue
            if cut==1:
                width=b*i-c*k
                if j!=1 and width not in allowed:
                    continue
                if j==2 and width%a:
                    continue
            start,poly=owner(end,j)
            if poly is not None and all(not overlap(poly,T) for T in polys):
                yield from paths(tuple(rest),start,polys+(poly,))
    return list(paths(caps,(g.A,0,0),()))


def check_frames(a,b,c):
    from junction import Model
    from rare_core import rotate

    g = geom.Geometry(a,b,c)
    model = Model(a,b,c)
    origin = (0,0,0)
    wall = (0,g.B,0)
    def normalize(v):
        return geom.point(g,g.scale(c,g.mult(g.unit(-1,0),v)))
    assert set(model.board)=={normalize(g.sub(v,wall)) for v in (origin,wall,(g.A,0,0))}
    for cut,types in enumerate((((1,0,-1),(1,4,-1),(0,0,1)),
                                ((2,4,-1),(1,0,1),(1,4,1)))):
        for k,(h,j,hand) in enumerate(types):
            verts=g.vertices((origin,h,j,hand))
            start=verts[-1] if hand==-1 else verts[0]
            finish=verts[0] if hand==-1 else verts[-1]
            assert normalize(g.sub(verts[1],start))==model.apex[cut][k]
            assert normalize(g.sub(finish,start))==tuple(c*x for x in model.moves[cut][k])
    for bank in (0,1):
        for j in (0,2,4):
            h,hand=(0,1) if bank else (1,-1)
            verts=g.vertices((origin,h,j,hand))
            start=verts[-1] if hand==-1 else verts[0]
            finish=verts[0] if hand==-1 else verts[-1]
            assert geom.point(g,g.sub(finish,start))==rotate((a,b) if bank else (c,0),j)
            assert normalize(g.sub(verts[1],start))==rotate((a*(a+b),-a*b) if bank else (a*c,0),j)
    print("Checked native and rotated owner frames for long side",c)


if __name__=="__main__":
    check_frames(33,7,37)
    check_frames(35,13,43)
    g=geom.Geometry(33,7,37)
    first,second=(families(g,k,8) for k in (0,1))
    assert (len(first),len(second))==(13,7)
    assert all(any(overlap(P,Q) for P in one for Q in two) for one in first for two in second)
    print("3431 independent X-corner check: all 13 times 7 suffix pairs conflict.")
