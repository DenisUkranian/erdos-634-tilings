"""An exact local 5063-shape control with two parent owners. No completion asserted."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"boundary-word"))
from control import geom
from terminal import UNITS,add,scale,det


def turn(p,j):
    x,y=p
    for _ in range(j%6):
        x,y=-y,x+y
    return x,y


def ccw(P):
    p,q,r=P
    return (p,q,r) if det(geom.sub(q,p),geom.sub(r,p))>0 else (p,r,q)


def intersections(P,Q):
    for poly,other in ((P,Q),(Q,P)):
        for p,q in zip(poly,poly[1:]+poly[:1]):
            if all(det(geom.sub(q,p),geom.sub(v,p))<=0 for v in other):
                return False
    return True


def current(edges):
    rows=defaultdict(Counter)
    for p,q in edges:
        dx,dy=geom.sub(q,p)
        u=(F(1),F(dy,dx)) if dx else (F(0),F(1))
        row=rows[u,det(u,p)]
        row[p]+=1
        row[q]-=1
    return {line:{p:n for p,n in values.items() if n}
            for line,values in rows.items() if any(values.values())}


def verify():
    a,b,c=35,13,43
    g=geom.Geometry(a,b,c)
    word=[0]+[1]*6+[9,3]+[4]*6+[6]
    root=[];parents=[];contour=[]
    p=(0,0)
    for letter in word:
        j=letter%6
        if letter<6:
            end=add(p,turn((a+b,-b),j))
            apex=add(p,scale(a,UNITS[j]))
            root.append(ccw((p,end,apex)))
        else:
            end=add(p,scale(c,UNITS[j]))
            apex=add(p,turn((F(a*(a+b),c),F(-a*b,c)),j))
            parents.append(ccw((p,end,apex)))
        contour.append((p,end))
        p=end
    assert p==(0,0) and len(root)==14 and len(parents)==2
    def pair(p,u,v):
        q,r,s=add(p,u),add(p,v),add(add(p,u),v)
        if geom.norm(add(u,v))==c*c:
            root.extend((ccw((p,q,s)),ccw((p,s,r))))
        else:
            assert geom.norm(geom.sub(u,v))==c*c
            root.extend((ccw((p,q,r)),ccw((q,s,r))))
    for k in range(6):
        pair((35,35*k),(13,-13),(0,35))
    for i in range(5):
        for k in range(i+1):
            pair((-30+13*i,35*k),(13,0),(0,35))
        for k in range(5-i):
            pair((48+13*i,22+35*i+35*k),(13,0),(0,35))
    assert len(root)==86
    rings=root+parents
    assert all(not intersections(P,Q) for P,Q in combinations(rings,2))
    def edges(P):
        return list(zip(P,P[1:]+P[:1]))
    assert current(edge for P in root for edge in edges(P))==current(contour)
    outside=current(edge for P in rings for edge in edges(P))
    parent_units=[turn((a+b,-b),j) for j in range(3)]
    assert all(any(det(axis,u)==0 for u in parent_units) for axis,_ in outside)
    shift=(F(400*c+1,c),F(100))
    def point(p):
        x,y=add(p,shift)
        assert (x*c).denominator==(y*c).denominator==1
        assert x>0 and y>0 and g.B*x+g.A*y<g.A*g.B
        return g.point(int(c*x),int(c*y),1)
    tiles=[]
    for idx,P in enumerate(rings):
        pos={point(p) for p in P}
        h=0 if idx<86 else -1
        options=[(q,h,j,s) for q in pos for j in range(6) for s in (-1,1)
                 if set(g.vertices((q,h,j,s)))==pos]
        assert len(options)==1
        tiles.append(options[0])
    assert sum(geom.eps(t) for t in tiles[:86])==sum(geom.eps(t) for t in tiles[86:])==0
    tree=geom.PhaseBudget(g,1)
    nodes={tree.node(t[0],0) for t in tiles[:86]}
    assert len(nodes)==1
    node=next(iter(nodes))
    assert all(tree.node(p,0)!=node for p,_,_,_ in g.walls())
    assert all(tree.node(g.vertices(t)[-1],0)==node for t in tiles[86:])
    groups=defaultdict(list)
    for i,t in enumerate(tiles):
        P=g.vertices(t)
        key=t[1],t[3],tuple(sorted((P[0],P[-1])))
        groups[key].append(i)
    singles=set()
    for (_,_,(p,q)),ids in groups.items():
        if len(ids)==1:
            singles.add(ids[0])
        else:
            assert len(ids)==2 and g.add(tiles[ids[0]][0],tiles[ids[1]][0])==g.add(p,q)
    assert singles==set(range(14))|{86,87}
    print("5063 local control: 86 terminal tiles, 14 unmatched inside, 2 parent owners.")
    return {"scope":"Local terminal polygon strictly inside the standard F2 board; no full-board completion.",
            "tile":[a,b,c],"coordinate":"[x,y,e] represents (x+y*rho)/43^e",
            "encoding":"[obtuse vertex, short height, rotation, hand]; the final two entries are parent owners",
            "tiles":tiles}


if __name__=="__main__":
    data=json.dumps(verify(),separators=(",",":"))+"\n"
    path=Path(__file__).with_name("patch5063.json")
    if sys.argv[1:]==["--write"]:
        path.write_text(data)
    else:
        assert data==path.read_text()
