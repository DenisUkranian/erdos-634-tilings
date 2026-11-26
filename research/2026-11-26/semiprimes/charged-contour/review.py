"""Independent coordinate, ordered-word and max-plus controls."""
from collections import Counter, defaultdict, deque
from itertools import product
from pathlib import Path
import sys

from area import encode, evaluate
from geometry import HEADINGS, UNITS, add, chart, det, exact_divide, multiply, scale, shapes, subtract
from grammar import program, shifted_program


def append(word, k, n, m):
    if word and word[-1][0] == k:
        n += word[-1][1]
        word = word[:-1]
    return word+((k,n%m),) if n%m else word


def full_control(name):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"boundary-word"))
    from control import geom
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polygons,centres,origin,*_ = geom.check_full_tiling(g,tiles)
    from currents import terms
    matched,pairs=geom.long_pairs(g,tiles,polygons,centres,origin)
    currents=Counter()
    def add_side(h,p,q):
        rotation=geom.point(g,g.unit(-h,0))
        u,w=multiply(rotation,p),multiply(rotation,q)
        terms(currents,h,u,w,g.a,g.b)
    for p,q,h,_ in g.walls():
        add_side(h,geom.point(g,p),geom.point(g,q))
    for i,poly in enumerate(polygons):
        if i not in matched:
            for j,(p,q) in enumerate(zip(poly,poly[1:]+poly[:1])):
                add_side(tiles[i][1]+(tiles[i][3] if j==2 else 0),q,p)
    assert not any(currents.values())
    graph = defaultdict(set)
    for tile,poly in zip(tiles,polygons):
        for i,(p,q) in enumerate(zip(poly,poly[1:]+poly[:1])):
            h = tile[1] + (tile[3] if i==2 else 0)
            length = next(n for n in (g.a,g.b,g.c) if n*n==geom.norm(geom.sub(q,p)))
            step = tuple(x/length for x in geom.sub(q,p))
            j = next(j for j in range(6) if geom.point(g,g.unit(h,j))==step)
            for _ in range(length):
                u = add(p,step)
                graph[p].add((u,h,j))
                graph[u].add((p,h,(j+3)%6))
                p = u
            assert p==q
    count = 0
    for m in (g.a,g.b):
        ratio = (g.b if m==g.a else g.a)*pow(g.c,-1,m)%m
        origin = next(iter(graph))
        labels = {origin:()}
        queue = deque([origin])
        while queue:
            p=queue.popleft()
            for q,h,j in graph[p]:
                axis = (j+(h if m==g.a else 0))%6
                exponent = (1 if axis<3 else -1)*pow(ratio,h,m)
                w = append(labels[p],axis%3,exponent,m)
                if q in labels:
                    assert labels[q]==w
                else:
                    labels[q]=w
                    queue.append(q)
        assert len(labels)==len(graph)
        count+=sum(map(len,graph.values()))//2
    return dict(tiles=len(tiles),pairs_in_current_test=len(pairs),unit_vertices=len(graph),undirected_atoms=len(set(
        tuple(sorted((p,q))) for p,neighbors in graph.items() for q,_,_ in neighbors)),
        edge_checks_both_moduli=count)


def triangle_review():
    from control import geom
    count=0
    for a,b,c in [(33,7,37),(35,13,43)]:
        g=geom.Geometry(a,b,c)
        for s in (1,-1):
            for i,(_,q,w) in enumerate(shapes(a,b,c,s)):
                h,hand=(s,-s) if i<3 else (0,s)
                j=(HEADINGS[i]+(3 if s==-1 else 0))%6
                apex=g.point(*q,1)
                poly=tuple(geom.point(g,p) for p in g.vertices((apex,h,j,hand)))
                ends=tuple(scale(c,p) for p in (poly[-1],poly[0]))
                assert ends==(((0,0),w) if i<3 else (w,(0,0)))
                count+=1
    return count


def tiny(binary):
    # A small abstract six-letter model. A repeated position cannot delimit a proper
    # one-factor subword in this inventory, by the abelian residue check below.
    a,c,s=2,1,1
    ds=tuple([UNITS[j] for j in HEADINGS[:3]]+
             [add(scale(a,UNITS[j]),UNITS[(j+1)%6]) for j in HEADINGS[3:]])
    v=(0,6,2,0,0,2)
    def disp(vector):
        return tuple(sum(n*d[k] for n,d in zip(vector,ds)) for k in (0,1))
    for q in product(*(range(n+1) for n in v)):
        if disp(q)!=(0,0) or q in ((0,)*6,v):
            continue
        residues=[0]*3
        for i,d in enumerate(ds):
            k=(HEADINGS[i]+(s if i>=3 else 0))%3
            residues[k]+=q[i]*d[0 if k==0 else 1]
        assert sum(x%a!=0 for x in residues)>1
    sites=[(x,y) for y in range(7) for x in range(7) if x+y<10]
    slot={p:p[0]+7*p[1] for p in sites}
    edges=[sum(1<<slot[p] for p in sites if add(p,d) in slot) for d in ds]
    shifts=tuple(x+7*y for x,y in ds)
    vertices=sum(1<<i for i in slot.values())
    rules,displacements=program(v,a,c,s,ds)
    offsets=shifted_program(rules,shifts)
    ids,values=evaluate(binary,encode(rules,displacements,offsets,a,c),rules,shifts,edges,vertices)
    observed=dict(zip(ids,values))
    def walk(p,left,word,area):
        if not any(left):
            return area if not word else None
        best=None
        for i,n in enumerate(left):
            t=add(p,ds[i])
            if not n or t not in slot:
                continue
            tail=list(left)
            tail[i]-=1
            k=(HEADINGS[i]+(s if i>=3 else 0))%3
            direction=ds[i][0 if k==0 else 1]
            z=walk(t,tail,append(word,k,direction,a),area+det(p,t))
            if z is not None and (best is None or z>best):
                best=z
        return best
    valid=0
    for p in sites:
        area=walk(p,v,(),0)
        if area is None:
            assert observed[slot[p]] < -1000000
        else:
            assert observed[slot[p]]*a*c==area
            valid+=1
    assert 0<valid<len(sites)
    return dict(sites=len(sites),nonempty=valid)


def charged_patch(a,b,c):
    # Positive terminal triangle U in the earlier charged-polygon certificate.
    vertices=[(0,0),(c*c,0),(a*a,a*b)]
    vectors=[subtract(q,p) for p,q in zip(vertices,vertices[1:]+vertices[:1])]
    from math import gcd
    pi={37:(3,4),43:(6,1)}[c]
    local=[exact_divide(multiply((pi[0]+pi[1],-pi[1]),p),c) for p in vertices]
    boundary=sum(gcd(abs(x),abs(y)) for x,y in
                 (subtract(q,p) for p,q in zip(local,local[1:]+local[:1])))
    assert boundary==c+a+b
    interior=0
    for x in range(min(x for x,y in local),max(x for x,y in local)+1):
        for y in range(min(y for x,y in local),max(y for x,y in local)+1):
            if all(det(subtract(q,p),subtract((x,y),p))>0 for p,q in zip(local,local[1:]+local[:1])):
                interior+=1
    assert 2*interior+boundary-2==a*b*c
    return dict(population=c*c,contact_edges=boundary,strict_gate_points=interior)


def controls(binary):
    controls={name:full_control(name) for name in ('known','macro')}
    controls['positive_charged_polygons']={str(c):charged_patch(a,b,c) for a,b,c in ((33,7,37),(35,13,43))}
    controls['oriented_owner_checks']=triangle_review()
    controls['exhaustive_small_grammar']=tiny(binary)
    return controls


if __name__=='__main__':
    print(controls(sys.argv[1]))
