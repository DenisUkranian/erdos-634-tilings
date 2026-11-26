"""Independent finite-field area and gate checks without constructing a covering tree."""
from collections import Counter, defaultdict
from pathlib import Path
import json

from controls import HERE, cell, geom


def roots(a,b,c):
    r=(-a*pow(b,-1,c))%c
    s=(1-r)%c
    assert r!=s and r*s%c==1 and (r*r-r+1)%c==0
    return r,s


def isolate(g,h,anchor,point):
    coords=geom.point(g,g.mult(g.unit(-h,0),g.sub(point,anchor)))
    assert all(x.denominator==1 for x in coords)
    return tuple(map(int,coords))


def verify_cell(a,b,c,edges,walls,population):
    r,s=roots(a,b,c)
    def uv(p):
        return (p[0]+r*p[1])%c,(p[0]+s*p[1])%c
    vertical,horizontal=Counter(),Counter()
    for hand,p,q in edges:
        u,v=uv(p)
        U,V=uv(q)
        if hand==1:
            assert u==U
            vertical[u]+=V-v
        else:
            assert v==V
            horizontal[v]+=U-u
    area=(s-r)*a*b*population
    plus=2*sum(k*v for k,v in vertical.items())
    minus=-2*sum(k*v for k,v in horizontal.items())
    for p,q in walls:
        u,v=uv(p)
        U,V=uv(q)
        plus+=(u+U)*(V-v)
        minus-=(v+V)*(U-u)
    assert (area-plus)%c==(area-minus)%c==0
    return tuple({k:v%c for k,v in flux.items() if v%c} for flux in (vertical,horizontal))


def board(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    classes=defaultdict(list)
    for t in tiles:
        classes[cell(g,t[1],t[0])].append(t)
    for key,group in classes.items():
        h=key[0]
        anchor=group[0][0]
        edges=[]
        for t in group:
            v=g.vertices(t)
            edges.append((t[3],isolate(g,h,anchor,v[-1]),isolate(g,h,anchor,v[0])))
        walls=[(isolate(g,h,anchor,p),isolate(g,h,anchor,q))
               for p,q,H,_ in g.walls() if H==h and cell(g,H,p)==key]
        flux=verify_cell(g.a,g.b,g.c,edges,walls,len(group))
        if (h,key[1],key[2])!=(0,0,0):
            assert flux==({},{})
        print(which,"ordinary" if not walls else "with wall",h,"gate residues",flux)


def partial():
    source=(HERE.parents[2]/"2026-11-21/semiprimes/continued-rigidity/global/BALANCED_16_NONOVERLAP.json")
    data=json.loads(source.read_text())
    g=geom.Geometry(*data["tile"])
    edges=[]
    for x,y,j,hand in data["support"]:
        verts=g.vertices(((x,y,0),0,j,hand))
        edges.append((hand,verts[-1][:2],verts[0][:2]))
    plus,minus=verify_cell(g.a,g.b,g.c,edges,[],len(edges))
    assert len(plus)>=2 and len(minus)>=2
    print("16-tile cylinder obstruction:",sorted(plus.items()),sorted(minus.items()))


if __name__=="__main__":
    for which in ("known","macro"):
        board(which)
    partial()
