"""Triangle perimeter profile and exact tests on connected physical 143 patches."""
from collections import defaultdict
from fractions import Fraction as F
from math import isqrt
import json
from check import geom

def cap(N,ab,p):
    assert F(545,100)*ab<=p<=N
    return N-F((N-p)**2)/(N-F(543,100)*ab)

def norm(p,q):
    x,y=geom.sub(q,p)
    v=F(x*x+x*y+y*y)
    n,d=isqrt(v.numerator),isqrt(v.denominator)
    assert n*n==v.numerator and d*d==v.denominator
    return F(n,d)

def test(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polygons,_,_,_,_=geom.check_full_tiling(g,tiles)
    lines=defaultdict(list)
    for i,poly in enumerate(polygons):
        for p,q in zip(poly,poly[1:]+poly[:1]):
            x,y=geom.sub(q,p)
            L=((1,y/x) if x else (0,1))
            lines[L,geom.det(L,p)].append((min(p,q),max(p,q),i))
    neighbors=defaultdict(dict)
    boundary=defaultdict(F)
    for entries in lines.values():
        pts=sorted({p for lo,hi,_ in entries for p in (lo,hi)})
        for p,q in zip(pts,pts[1:]):
            ids=[i for lo,hi,i in entries if lo<=p<q<=hi]
            if not ids: continue
            length=norm(p,q)
            if len(ids)==1:
                boundary[ids[0]]+=length
            else:
                i,j=ids
                neighbors[i][j]=neighbors[i].get(j,0)+length
                neighbors[j][i]=neighbors[j].get(i,0)+length
    assert sum(boundary.values())==g.N
    for i in range(g.N): assert sum(neighbors[i].values())+boundary[i]==15
    # Grow a connected patch by choosing the neighbor sharing the most
    # boundary. Ties use tile indices, which makes the sequence reproducible.
    used=set()
    shared=defaultdict(F)
    p=0
    checked=[]
    for _ in tiles:
        i=0 if not used else max((j for j in shared if j not in used),key=lambda j:(shared[j],-j))
        assert not used or shared[i]>0
        p+=15-2*shared[i]
        used.add(i)
        for j,x in neighbors[i].items(): shared[j]+=x
        if F(545,100)*15<=p<g.N:
            upper=cap(g.N,15,p)
            assert len(used)<=upper<g.N
            checked.append((len(used),p,upper))
    assert p==g.N and len(used)==143 and checked
    best=min(checked,key=lambda row:row[2]-row[0])
    return dict(checked=len(checked),tightest=dict(tiles=best[0],perimeter=str(best[1]),upper=str(best[2])))

if __name__=='__main__':
    out={'controls':{w:test(w) for w in ('known','macro')},'saturated':{}}
    for N,a,b,c in [(3431,33,7,37),(5063,35,13,43)]:
        p=c*(c+a-b)
        upper=cap(N,a*b,p)
        blocks=int(upper/c)
        out['saturated'][N]=dict(perimeter=p,upper=str(upper),odd_cap=c*(blocks-(blocks+1)%2))
    print(json.dumps(out,indent=2))
