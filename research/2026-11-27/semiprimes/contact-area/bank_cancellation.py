"""Check parity and physical displacement after bankwise directional cancellation."""
from collections import Counter, defaultdict
import json
from check import geom,cell,step,reconstruct


def control(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polys,centres,origin,_,_=geom.check_full_tiling(g,tiles)
    paired,_=geom.long_pairs(g,tiles,polys,centres,origin)
    lifts,spine=reconstruct(g,tiles,polys)
    directions=defaultdict(Counter)
    signed=Counter()
    count=Counter()
    for i,t in enumerate(tiles):
        if i in paired:
            continue
        v=lifts[i]
        u=step(v,cell(g,t[1]+t[3],g.vertices(t)[-1]))
        delta=geom.sub(polys[i][0],polys[i][-1])
        directions[v,u][delta]+=1
        signed[v,u]+=geom.eps(t)
        count[v,u]+=1
    rows=[]
    for depth in (2,3):
        far=spine[:depth]
        parent=far[:-1]
        energies=[]
        both=[]
        for key in ((far,parent),(parent,far)):
            vectors=directions[key]
            old=[sum(k*p[t] for p,k in vectors.items()) for t in (0,1)]
            net=[(p,k-vectors[(-p[0],-p[1])]) for p,k in vectors.items()
                 if k>vectors[(-p[0],-p[1])]]
            bare=sum(k for p,k in net)
            assert old==[sum(k*p[t] for p,k in net) for t in (0,1)]
            assert count[key]>=bare>=abs(signed[key]) and (bare-signed[key])%2==0
            energies.append([count[key],bare,abs(signed[key])])
            both.append(old)
        assert geom.sub(both[0],both[1])==(g.A,-g.B)
        assert sum(x[1] for x in energies)>=g.c
        rows.append(energies)
    return rows


if __name__=='__main__':
    print(json.dumps({w:control(w) for w in ('known','macro')},indent=2))
