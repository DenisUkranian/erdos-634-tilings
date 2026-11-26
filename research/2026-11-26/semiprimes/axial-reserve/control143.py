"""Reconstruct both axial wall partitions and gate currents from the complete controls."""
from collections import Counter, defaultdict
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"joint-cell-tree"))
from controls import geom, reconstruct
from geometry import UNITS, det, multiply, subtract


def control(name):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,name)
    polys,*_=geom.check_full_tiling(g,tiles)
    lifts,spine=reconstruct(g,tiles,polys)
    root=spine[:1]
    edges=[[],[]]
    short_currents=defaultdict(Counter)
    expected=defaultdict(Counter)
    owned=Counter()
    population=Counter()
    signed=Counter()
    bank=defaultdict(Counter)
    def record(row,h,p,q):
        R=geom.point(g,g.unit(-h,0))
        u,w=multiply(R,p),multiply(R,q)
        k=next(i for i in range(3) if det(UNITS[i],subtract(w,u))==0)
        row[k,u[0]%7,u[1]%7]-=1
        row[k,w[0]%7,w[1]%7]+=1
    for i,(tile,poly) in enumerate(zip(tiles,polys)):
        _,h,j,hand=tile
        marker=lifts[i]
        population[marker]+=1
        signed[marker]+=geom.eps(tile)
        for k,(p,q) in enumerate(zip(poly,poly[1:]+poly[:1])):
            if k<2:
                record(short_currents[marker],h,p,q)
            else:
                pp=multiply(geom.point(g,g.unit(-h,0)),p)
                rx,ry=marker[-1][1:]
                x,y=subtract(pp,(rx,ry))
                assert x.denominator==y.denominator==1
                z=(8,-3) if hand==1 else (5,3)
                bank[marker][hand,int(multiply(z,(x,y))[0])%7]+=geom.eps(tile)
            side=0 if p[1]==q[1]==0 else 1 if p[0]==q[0]==0 else None
            if side is None:
                continue
            start,end=(p[0],q[0]) if side==0 else (g.B-p[1],g.B-q[1])
            length=int(end-start)
            assert end-start==length and length in (5,3,7)
            if length!=7:
                assert marker==root and geom.eps(tile)==(1 if length==5 else -1)
                heading=0 if side==0 else 4
                if length==5:
                    apex,index=(q,heading) if hand==1 else (p,heading+3)
                else:
                    apex,index=(p,heading-1) if hand==1 else (q,heading+4)
                assert geom.point(g,tile[0])==apex and j==index%6
                owned[i]+=1
            edges[side].append((start,end,length))
    assert all(n==1 for n in owned.values())
    for p,q,h,_ in g.walls():
        key=root if h==0 else spine
        record(expected[key],h,geom.point(g,p),geom.point(g,q))
    for marker in population:
        keys=set(short_currents[marker])|set(expected[marker])
        assert all(short_currents[marker][k]==expected[marker][k] for k in keys)
        assert sum(bank[marker].values())==signed[marker]
    inventory=[]
    for row,L in zip(edges,(g.A,g.B)):
        cursor=0
        for p,q,length in sorted(row):
            assert p==cursor
            cursor=q
        assert cursor==L
        inventory.append([sum(n==length for _,_,n in row) for length in (5,3,7)])
    return dict(axial_wall_counts_a_b_c=inventory,root_tiles=population[root],
                root_charge=signed[root],middle_tiles=population[spine[:2]],
                middle_nonzero_gate_currents=sorted(x for x in bank[spine[:2]].values() if x))


def controls():
    return {name:control(name) for name in ('known','macro')}
