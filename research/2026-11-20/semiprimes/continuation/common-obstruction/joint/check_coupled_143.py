#!/usr/bin/env python3
"""Replay all 143 exact tiles through the coupled finite residue projection."""
from pathlib import Path
from collections import Counter
import argparse,json,sys
import numpy as np
from coupled_native_torus import build,line
from verify_native_torus import U,root

def check(base):
    base=Path(base);sys.path[:0]=[str(base/'global-endpoints/integer')]
    from global_core_sat import Geometry
    g=Geometry(5,3,7);a,b,c=g.a,g.b,g.c;z2=g.unit(2,0);rho=g.unit(0,1)
    shift=g.scale(a*(a+2*b),z2);tiles={1:set(),2:set()}
    for q,h,j,s in json.loads((base/'global-endpoints/tiling_143.json').read_text())['tiles']:
        qn=g.sub(shift,g.mult(g.mult(rho,z2),(q[0]+q[1],-q[1],q[2])))
        H=2-h;J=(4-j)%6;S=-s;qr=g.mult(qn,g.unit(-H,0));assert qr[2]==0
        tiles[H].add((qr[:2],J,S))
    fixed={((i*(a+b)+a,-i*b),0,-1)for i in range(c)};assert fixed<=tiles[1]
    counts=Counter();partitions=[]
    for h in(1,2):
        seen=set(fixed if h==1 else());base_set=set(seen);r=root(a,b,c)if h==1 else(1-root(a,b,c))%c
        for tile in sorted(tiles[h]-base_set):
            if tile in seen:continue
            q,j,s=tile;u=(q[0]-a*U[j][0],q[1]-a*U[j][1]);gated=(u[0]+r*u[1])%c==0
            if s==(1 if h==1 else-1)and gated:
                qm=(q[0]%c,q[1]%c);counts['gate_short',h,j,qm]+=1
                other=g.mult((u[0],u[1],0),g.unit(2*h-3,0));assert other[2]==0
                t=line(j%3,other[:2],c);counts['gate_long',h,j,t]+=1;seen.add(tile)
            else:
                mateq=(u[0]+b*U[(j+s)%6][0],u[1]+b*U[(j+s)%6][1]);mate=(mateq,(j+3)%6,s)
                assert mate in tiles[h]and mate not in seen,(tile,mate,h)
                if j>=3:q,j=mateq,j-3
                counts['pair',h,j,s,(q[0]%c,q[1]%c)]+=1;seen.update((tile,mate))
        assert seen==tiles[h]
        partitions.append({'height':h,'tiles':len(seen),'fixed':len(base_set)})
    M,rhs,cost,labels,meta=build(a,b,c)
    v=np.array([counts[t]for t in labels],dtype=np.int64)
    assert sum(v)==sum(counts.values())
    residual=M@v-rhs;assert np.issubdtype(residual.dtype,np.integer)
    assert not np.any(residual),[(int(i),int(residual[i]))for i in np.flatnonzero(residual)[:20]]
    assert int(cost@v)+c==143
    return {'status':'PASS','N':143,'partitions':partitions,'rows':M.shape[0],'columns':M.shape[1],'exact_integer_residual':0,'selected_projection_columns':int(np.count_nonzero(v))}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('base');args=p.parse_args();print(json.dumps(check(args.base)))
