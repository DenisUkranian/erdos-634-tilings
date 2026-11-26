"""Reconstruct the tree of positioned joint cells from both complete 143 tilings."""
from collections import Counter, defaultdict, deque
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "boundary-word"))
from control import geom


def cell(g, h, point):
    x, y = geom.point(g, g.mult(g.unit(-h, 0), point))
    return h, x % 1, y % 1


def step(path, key):
    if path[-1] == key:
        return path
    assert abs(path[-1][0]-key[0]) == 1
    if len(path) >= 2 and path[-2] == key:
        return path[:-1]
    return (*path, key)


def reconstruct(g, tiles, polys):
    # On each support break the two banks at their common endpoint list.
    lines = defaultdict(list)
    keys = {}
    graph = defaultdict(set)
    def side(owner, h, p, q, start):
        key = cell(g, h, start)
        dx, dy = geom.sub(q,p)
        u = (1, dy/dx) if dx else (0, 1)
        support = u, geom.det(u,p)
        lo, hi = sorted((p[0],q[0]) if dx else (p[1],q[1]))
        lines[support].append((lo,hi,owner,key))
    for i, (q,h,j,s) in enumerate(tiles):
        keys[i] = cell(g,h,q)
        verts = g.vertices(tiles[i])
        for k in range(3):
            side(i,h+(s if k==2 else 0),polys[i][k],polys[i][(k+1)%3],verts[k])
    for i,(p,q,h,_) in enumerate(g.walls(),len(tiles)):
        keys[i]=cell(g,h,p)
        side(i,h,geom.point(g,p),geom.point(g,q),p)
    for line, entries in lines.items():
        cuts = sorted({x for lo,hi,_,_ in entries for x in (lo,hi)})
        for lo,hi in zip(cuts,cuts[1:]):
            banks=[(i,k) for x,y,i,k in entries if x<=lo and hi<=y]
            if not banks:
                continue
            assert len(banks)==2 and banks[0][1]==banks[1][1]
            marker=(line,lo,hi)
            keys[marker]=banks[0][1]
            for i,_ in banks:
                graph[i].add(marker)
                graph[marker].add(i)
    root=len(tiles)
    lifts={root:(keys[root],)}
    queue=deque([root])
    while queue:
        vertex=queue.popleft()
        for nxt in graph[vertex]:
            walk=step(lifts[vertex],keys[nxt])
            if nxt in lifts:
                assert walk==lifts[nxt], "a physical loop changed the joint-cell lift"
            else:
                lifts[nxt]=walk
                queue.append(nxt)
    assert len(lifts)==len(keys)
    assert lifts[root]==lifts[root+2]
    spine=lifts[root+1]
    assert len(spine)==3 and [k[0] for k in spine]==[0,1,2]
    return lifts,spine


def check_vertex_links(g, tiles, polys):
    # Work directly on the physical vertices, independently of the dual BFS.
    vertex_codes={geom.point(g,p):p for tile in tiles for p in g.vertices(tile)}
    through=outside_short=0
    for p,code in vertex_codes.items():
        for tile,poly in zip(tiles,polys):
            q,h,_,hand=tile
            short=cell(g,h,q)
            for j,lo in enumerate(poly):
                hi=poly[(j+1)%3]
                if geom.det(geom.sub(hi,lo),geom.sub(p,lo))!=0 or not min(lo,hi)<=p<=max(lo,hi):
                    continue
                H=h+(hand if j==2 else 0)
                side=cell(g,H,g.vertices(tile)[j])
                assert cell(g,H,code)==side
                if p in (lo,hi):
                    assert cell(g,h,code)==short
                else:
                    through+=1
                    outside_short+=cell(g,h,code)!=short
    assert through and outside_short
    return through,outside_short


def check(which):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polys,_,_,_,_=geom.check_full_tiling(g,tiles)
    junctions=check_vertex_links(g,tiles,polys)
    lifts,spine=reconstruct(g,tiles,polys)
    counts=Counter(lifts[i] for i in range(len(tiles)))
    signs=Counter()
    for i,t in enumerate(tiles):
        signs[lifts[i]]+=geom.eps(t)
    for v in counts:
        assert (counts[v]-(g.N if len(v)==1 else 0))%g.c==0
        assert (signs[v]+(g.a-g.b if len(v)==1 else 0))%g.c==0
    # Check every used edge, even if it has no short tiles on its far side.
    nodes={p[:i] for p in lifts.values() for i in range(2,len(p)+1)}
    for v in nodes:
        parent=v[:-1]
        E=O=P=Q=0
        directed=[]
        includes_slant=spine[:len(v)]==v
        if includes_slant:
            p,q,_,_=g.walls()[1]
            directed.append((geom.point(g,p),geom.point(g,q)))
        for i,t in enumerate(tiles):
            short=lifts[i]
            long=step(short,cell(g,t[1]+t[3],g.vertices(t)[-1]))
            sign=geom.eps(t)
            if short[:len(v)]==v:
                if t[1]%2: O+=sign
                else: E+=sign
            edge=polys[i][-1],polys[i][0]
            if (short,long)==(v,parent):
                P+=sign
                directed.append(edge)
            if (short,long)==(parent,v):
                Q+=sign
                directed.append(edge[::-1])
        area=sum(geom.det(p,q) for p,q in directed)
        enclosed=sum(n for node,n in counts.items() if node[:len(v)]==v)
        assert area==g.a*g.b*enclosed and enclosed%g.c==0
        boundary=-g.c**2*includes_slant
        d=g.a-g.b
        assert g.c*(P-Q)==(g.c-d)*(E+O)+boundary
        parity=1 if v[-1][0]%2==0 else -1
        assert g.c*parity*(P+Q)==(g.c+d)*(E-O)-boundary
        if not includes_slant:
            same,opposite=(O,E) if parent[-1][0]%2 else (E,O)
            assert g.c*(Q+same)==d*opposite
    print(which,"through incidences / outside the through-tile short translate:", *junctions)
    print(which,"143 geometry:",len(nodes),"lifted edges;", sorted((v[-1][0],n,signs[v]) for v,n in counts.items()))


if __name__=="__main__":
    check("known")
    check("macro")
