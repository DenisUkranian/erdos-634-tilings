"""On complete tilings, infer each pair orientation count from unmatched owners."""
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"boundary-word"))
from control import geom
from terminal import det,UNITS


def check(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polys,centres,origin,_,_=geom.check_full_tiling(g,tiles)
    matched,pairs=geom.long_pairs(g,tiles,polys,centres,origin)
    charges = Counter()
    for i,(q,h,j,hand) in enumerate(tiles):
        if i not in matched:
            charges[(h,hand)] += geom.eps(tiles[i])
    assert set(charges) <= {(1,-1),(0,1),(2,-1),(1,1)}
    assert tuple(charges[key] for key in ((1,-1),(0,1),(2,-1),(1,1))) == (-14,-2,0,7)
    # For each parallel class, use the normal coordinate in its own frame.
    classes=defaultdict(Counter)
    endpoints=Counter()
    def edge(p,q,h,mult):
        dx,dy=geom.sub(q,p)
        for axis in range(3):
            u=geom.point(g,g.unit(h,axis))
            if det(u,(dx,dy))==0:
                length=dx/u[0] if u[0] else dy/u[1]
                classes[h,axis][det(u,p)]+=mult*length
                rx,ry=geom.point(g,g.unit(-h,0))
                for point,sign in ((p,-mult),(q,mult)):
                    x,y=point
                    local=(rx*x-ry*y,rx*y+ry*x+ry*y)
                    for period in (g.a,g.b):
                        endpoints[h,axis,period,local[0]%period,local[1]%period]+=sign
                return
        raise AssertionError("side does not have the assigned physical height")
    for p,q,h,_ in g.walls():
        edge(geom.point(g,p),geom.point(g,q),h,1)
    for i,t in enumerate(tiles):
        if i not in matched:
            for j in range(3):
                edge(polys[i][j],polys[i][(j+1)%3],t[1]+(t[3] if j==2 else 0),-1)
    assert not any(endpoints.values())
    observed=defaultdict(list)
    for i,j in pairs:
        for idx in (0,1):
            t=tiles[i];p,q=polys[i][idx:idx+2];delta=geom.sub(q,p)
            axis=next(k for k in range(3) if det(geom.point(g,g.unit(t[1],k)),delta)==0)
            u=geom.point(g,g.unit(t[1],axis))
            length=abs(delta[0]/u[0] if u[0] else delta[1]/u[1])
            points=[det(u,x) for x in polys[i]+polys[j]]
            left,right=min(points),max(points)
            assert (right-left)*length==g.a*g.b
            observed[t[1],axis].append((left,right,length))
    for key in set(classes)|set(observed):
        levels=sorted(set(classes[key])|{x for lo,hi,_ in observed[key] for x in (lo,hi)})
        integral=active=0
        for j,x in enumerate(levels):
            active+=classes[key][x]
            assert active==sum(w for lo,hi,w in observed[key] if lo<=x<hi)
            if j+1<len(levels):
                integral+=(levels[j+1]-x)*active
        assert active==0 and integral==g.a*g.b*len(observed[key])
    assert sum(map(len,observed.values()))==2*len(pairs)
    print(which, "complete 143 control:",len(pairs),"pairs and",len(classes),"direction classes")


if __name__=="__main__":
    check("known")
    check("macro")
