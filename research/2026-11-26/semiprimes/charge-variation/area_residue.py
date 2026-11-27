"""Native-cut area modulo the middle mesh cell, measured in exact coordinates."""
from collections import Counter
from fractions import Fraction as F
import json

from verify import branch, cell, geom, reconstruct, step


def det(p,q):
    return p[0]*q[1]-p[1]*q[0]


def add(p,q):
    return p[0]+q[0],p[1]+q[1]


def sub(p,q):
    return p[0]-q[0],p[1]-q[1]


def residue(edge):
    p,q = edge
    P,Q = tuple(int(v//1) for v in p),tuple(int(v//1) for v in q)
    t,s = sub(p,P),sub(q,Q)
    return det(add(P,Q),sub(s,t))+det(t,s)


def native(name):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polys,centres,centre,*_ = geom.check_full_tiling(g,tiles)
    paired,_ = geom.long_pairs(g,tiles,polys,centres,centre)
    lifts,T = reconstruct(g,tiles,polys)
    B,C = T[:-1],T[:1]
    def chart(p):
        return tuple(x/g.c for x in geom.point(g,g.mult(g.unit(-1,0),p)))
    long = [step(lifts[i],cell(g,t[1]+t[3],g.vertices(t)[-1])) for i,t in enumerate(tiles)]
    results = []
    for gate in (C,T):
        inside = {i for i in range(len(tiles)) for v in (lifts[i],)
                  if (v!=B and branch(B,v)==gate)==(gate==T)}
        bank = []
        pure = [(chart(g.point(g.A,0,0)),chart(g.point(0,g.B,0)))]
        for i,t in enumerate(tiles):
            if {lifts[i],long[i]}!={B,gate} or i in paired:
                continue
            points = g.vertices(t)
            edge = chart(points[-1]),chart(points[0])
            if i not in inside:
                edge = edge[::-1]
            (bank if lifts[i]==B else pure).append(edge)
        assert all(all(x.denominator==1 for x in sub(q,p)) for p,q in pure)
        ends = Counter()
        for p,q in bank+pure:
            ends[p]+=1
            ends[q]-=1
        assert not any(ends.values())
        area = F(len(inside)*g.a*g.b,g.c**2)
        assert sum(det(p,q) for p,q in bank+pure)==area
        value = sum(map(residue,bank))%1
        assert value==area%1
        results.append([len(inside),len(bank),str(value)])
    return results


def local():
    # The two-parent 5063 strip from the terminal-contact coordinate certificate.
    a,b,c = 35,13,43
    from pathlib import Path
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'terminal-contact'))
    from patch5063 import turn
    word = [0]+[1]*6+[9,3]+[4]*6+[6]
    # Divide physical coordinates by D=(a+b)-b*rho to make the other bank integral.
    def chart(p):
        x,y=p
        return F(a*x-b*y,c*c),F(b*x+(a+b)*y,c*c)
    pure,bank = [],[]
    p=(0,0)
    for token in word:
        unit=(a+b,-b) if token<6 else (c,0)
        q=add(p,turn(unit,token%6))
        (pure if token<6 else bank).append((chart(p),chart(q)))
        p=q
    assert p==(0,0)
    (p,r),(s,q)=bank
    v,L=sub(r,p),sub(q,p)
    assert sub(s,q)==v and all(x.denominator==1 for x in L)
    assert all(all(x.denominator==1 for x in sub(t,u)) for u,t in pure)
    area=F(2*c*a*b,c*c)
    assert sum(det(u,t) for u,t in bank+pure)==area
    assert area%1==2*det(v,L)%1==sum(map(residue,bank))%1
    return dict(population=2*c,separation=list(map(int,L)),area_residue=str(area%1))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    print(json.dumps(dict(controls={s:native(s) for s in ('known','macro')},
                          two_owner_local=local()),indent=2))
