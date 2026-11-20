#!/usr/bin/env python3
"""Exact upper-median controls on two complete 143 tilings; no target search."""
from collections import defaultdict, Counter, deque
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent

def find_continuation():
    for ancestor in HERE.parents:
        for candidate in (ancestor,ancestor/'repo/research/2026-11-20/semiprimes/continuation'):
            if (candidate/'global-endpoints/integer/global_core_sat.py').exists():return candidate
    raise FileNotFoundError('Pass --continuation with the repository continuation directory.')


def eps(t):return t[3]*(-1 if t[2]%2 else 1)
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def point(g,p):return F(p[0],g.c**p[2]),F(p[1],g.c**p[2])
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def inside(poly,p):
    winding=0
    for u,v in zip(poly,poly[1:]+poly[:1]):
        t=cross(sub(v,u),sub(p,u))
        assert t or not (min(u[0],v[0])<=p[0]<=max(u[0],v[0]) and min(u[1],v[1])<=p[1]<=max(u[1],v[1])),('centroid on boundary',p)
        if u[1]<=p[1]<v[1] and t>0:winding+=1
        if v[1]<=p[1]<u[1] and t<0:winding-=1
    return winding!=0

def get_tiles(g,which,continuation,macro):
    if which=='known':
        raw=json.loads((continuation/'global-endpoints/tiling_143.json').read_text())['tiles']
        return [(tuple(t[0]),*t[1:]) for t in raw]
    raw=json.loads(macro.read_text())
    D=raw['denominator'];e=0
    while g.c**e<D:e+=1
    assert g.c**e==D
    tiles=[]
    for triangle in raw['triangles']:
        vertices={g.point(x,y,e) for x,y in triangle};found=[]
        for q in vertices:
            for h in (0,1):
                for j in range(6):
                    for s in (-1,1):
                        tile=q,h,j,s
                        if set(g.vertices(tile))==vertices:found.append(tile)
        assert len(found)==1
        tiles.append(found[0])
    assert len(tiles)==143 and len(set(tiles))==143
    return tiles

def verify_complete(g,tiles):
    """Positive exact chain equality proves containment and one-fold coverage."""
    assert len(set(tiles))==len(tiles)==g.N
    events=defaultdict(Counter)
    board=[(F(0),F(0)),(F(g.A),F(0)),(F(0),F(g.B))]
    polygons=[]
    for tile in tiles:
        assert g.admissible(tile)
        vs=[point(g,v) for v in g.vertices(tile)]
        assert sum(cross(u,v) for u,v in zip(vs,vs[1:]+vs[:1]))==g.a*g.b
        polygons.append((vs,1))
    polygons.append((board,-1))
    for vs,sign in polygons:
        for u,v in zip(vs,vs[1:]+vs[:1]):
            dx,dy=sub(v,u)
            if dx:
                direction=(F(1),dy/dx)
            else:
                assert dy;direction=(F(0),F(1))
            line=(direction,cross(direction,u))
            events[line][u]+=sign;events[line][v]-=sign
    assert all(all(n==0 for n in row.values()) for row in events.values())
    return {'tiles':len(tiles),'tile_area_and_containment':'PASS',
            'positive_boundary_chain_equals_board':'PASS'}

def convert(g,tiles):
    C=g.scale(g.a*(g.a+2*g.b),g.unit(2,0))
    def iso(q):return g.sub(C,g.mult(g.unit(2,1),(q[0]+q[1],-q[1],q[2])))
    return [(iso(q),2-h,(4-j)%6,-s) for q,h,j,s in tiles]

def graph(g,tiles):
    arrows=defaultdict(list)
    for i,(q,h,j,s) in enumerate(tiles):
        if (h,s) not in ((1,1),(2,-1)):continue
        u=g.add(q,g.scale(-g.a,g.unit(h,j)))
        v=g.add(q,g.scale(g.b,g.unit(h,j+s)))
        arrows[u,v].append((i,h+s,j))
    done=set()
    for u,v in list(arrows):
        if (u,v) in done:continue
        n=min(len(arrows[u,v]),len(arrows[v,u]))
        arrows[u,v]=arrows[u,v][n:];arrows[v,u]=arrows[v,u][n:]
        done.update(((u,v),(v,u)))
    adj=defaultdict(list)
    for (u,v),items in arrows.items():
        for item in items:adj[u].append((v,item))
    return adj

def find_paths(g,adj):
    start=(0,0,0);end=(g.c*g.c,0,0)
    paths=[];visited={start}
    def dfs(u,seq):
        if u==end:
            paths.append(seq);return
        assert len(paths)<10000
        for v,item in adj[u]:
            if v not in visited:
                visited.add(v);dfs(v,seq+[(u,v,item)]);visited.remove(v)
    dfs(start,[])
    assert paths
    return paths

def verify_path(g,tiles,path):
    d=g.a-g.b;c=g.c
    J=sum((-1 if j%2 else 1) for u,v,(i,h,j) in path if h==1)
    K=sum((-1 if j%2 else 1) for u,v,(i,h,j) in path if h==2)
    ii=F(J+K-d,c-d);jj=F(J-K-d,c+d);t=(ii-jj)/2
    assert ii.denominator==jj.denominator==t.denominator==1
    poly=[point(g,path[0][0])]+[point(g,v) for u,v,item in path]
    area=-sum(cross(u,v) for u,v in zip(poly,poly[1:]+poly[:1]))/g.a/g.b
    assert area>0 and area.denominator==1
    lower=[];upper=[]
    for tile in tiles:
        vs=[point(g,v) for v in g.vertices(tile)]
        centroid=tuple(sum(v[i] for v in vs)/3 for i in (0,1))
        (lower if inside(poly,centroid) else upper).append(tile)
    assert len(lower)==area
    lower_set=set(lower)
    for u,v,(idx,long_height,j) in path:
        assert (tiles[idx] in lower_set)==(long_height==2)
    def data(ts):
        return {'n':len(ts),'G_even':sum(eps(x) for x in ts if x[1]%2==0),
                'G_odd':sum(eps(x) for x in ts if x[1]%2),
                'heights':dict(sorted(Counter(x[1] for x in ts).items()))}
    lo=data(lower);hi=data(upper)
    assert lo['G_odd']==c*(t-1) and hi['G_odd']==c*(2-t)
    assert lo['G_even']==c*(jj+t)
    assert all(v%c==0 and v>=2*c for v in lo['heights'].values())
    assert all(tile[1]==1 and g.mult(tile[0],g.unit(-1,0))[2]==0 for tile in lower)
    assert all(tile[1]==2 and g.mult(tile[0],g.unit(-2,0))[2]==0 for tile in upper)
    return {'length':len(path),'J':J,'K':K,'i':int(ii),'j':int(jj),'t':int(t),'lower':lo,'upper':hi,
            'steps':[[h,j] for u,v,(i,h,j) in path]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--continuation',type=Path)
    parser.add_argument('--macro',type=Path,default=HERE/'macro143_certificate.json')
    parser.add_argument('--out',type=Path,default=HERE/'ACTUAL_MEDIAN_REPLAY.json')
    args=parser.parse_args()
    continuation=args.continuation or find_continuation()
    sys.path.insert(0,str(continuation/'global-endpoints/integer'))
    from global_core_sat import Geometry
    g=Geometry(5,3,7);out={'scope':'Exact actual-median cuts of two complete positive 143 tilings. Neither target is decided.'}
    for which in ('known','macro'):
        original=get_tiles(g,which,continuation,args.macro)
        complete=verify_complete(g,original)
        tiles=convert(g,original)
        assert sum(eps(t) for t in tiles if t[1]%2)==g.c
        adj=graph(g,tiles);paths=find_paths(g,adj)
        source=continuation/'global-endpoints/tiling_143.json' if which=='known' else args.macro
        out[which]={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'complete_certificate':complete,
                    'unmatched_upper_edges':sum(map(len,adj.values())),
                    'paths':[verify_path(g,tiles,p) for p in paths]}
        print(which,json.dumps(out[which],sort_keys=True))
    args.out.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
