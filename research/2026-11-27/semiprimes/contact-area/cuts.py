"""Physical boundary budgets for arbitrary subsets of lifts on both complete controls."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from check import geom,cell,step,reconstruct
from triangle import norm

def check(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    poly,centres,origin,_,_=geom.check_full_tiling(g,tiles)
    paired,_=geom.long_pairs(g,tiles,poly,centres,origin)
    lifts,_=reconstruct(g,tiles,poly)
    mass=Counter(lifts[i] for i in range(g.N))
    walls=Counter()
    owners=Counter()
    for j,(lo,hi,_,_) in enumerate(g.walls()):
        walls[lifts[g.N+j]]+=norm(geom.point(g,lo),geom.point(g,hi))
    for i,t in enumerate(tiles):
        if i in paired: continue
        v=lifts[i]
        u=step(v,cell(g,t[1]+t[3],g.vertices(t)[-1]))
        owners[v,u]+=1
    support=set(mass)|set(walls)|{u for edge in owners for u in edge}
    rows=[]
    for bits in product((0,1),repeat=len(support)):
        selected={u for u,b in zip(sorted(support),bits) if b}
        n=sum(mass[u] for u in selected)
        w=sum(walls[u] for u in selected)
        m=sum(v for (u,t),v in owners.items() if (u in selected)!=(t in selected))
        # H=pi*sqrt(3)*ab. Replacing it by a rational lower bound weakens
        # both branches, including the interval that crosses their junction.
        H=F(543,100)*g.a*g.b
        for v,length in ((n,w+g.c*m),(g.N-n,g.N-w+g.c*m)):
            if v<=H:
                assert length**2>=H*v
            elif length<g.N:
                assert (g.N-length)**2<=(g.N-H)*(g.N-v)
        rows.append([n,int(w),m])
    return dict(support=len(support),subsets=len(rows),distinct=sorted(map(list,set(map(tuple,rows)))))

if __name__=='__main__':
    print(json.dumps({w:check(w) for w in ('known','macro')},indent=2))
