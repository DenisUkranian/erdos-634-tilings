"""Independent extremal polygons and exact boundary controls on both 143 boards."""
from itertools import combinations
from collections import Counter, defaultdict
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT / "2026-11-26/semiprimes/joint-cell-tree"))
from controls import geom, cell, reconstruct, step

def supported_words(edges,q):
    paths=defaultdict(list)
    for p,r in edges:
        paths[p].append(r)
    lengths=[]
    for origin in list(paths):
        while paths[origin]:
            pos=origin
            stack=[]
            length=0
            while paths[pos]:
                nxt=paths[pos].pop()
                delta=geom.sub(nxt,pos)
                x,y=(v.numerator*pow(v.denominator,-1,q)%q for v in delta)
                if x or y:
                    if not y:
                        f,e=0,x
                    elif not x:
                        f,e=1,y
                    else:
                        assert (x+y)%q==0
                        f,e=2,y
                    if stack and stack[-1][0]==f:
                        e+=stack.pop()[1]
                    if e%q:
                        stack.append((f,e%q))
                pos=nxt
                length+=1
            assert pos==origin and not stack
            lengths.append(length)
    return sorted(lengths)

def controls(which):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,which)
    polygons,centres,origin,_,_ = geom.check_full_tiling(g,tiles)
    paired,_ = geom.long_pairs(g,tiles,polygons,centres,origin)
    lifts,spine = reconstruct(g,tiles,polygons)
    result = []
    for depth in (2,3):
        v = spine[:depth]
        p,q,_,_ = g.walls()[1]
        edges = [(geom.point(g,p),geom.point(g,q))]
        for i,t in enumerate(tiles):
            if i in paired:
                continue
            short = lifts[i]
            long = step(short,cell(g,t[1]+t[3],g.vertices(t)[-1]))
            e = polygons[i][-1],polygons[i][0]
            if (short,long)==(v,v[:-1]):
                edges.append(e)
            if (long,short)==(v,v[:-1]):
                edges.append(e[::-1])
        n = sum(lifts[i][:depth]==v for i in range(g.N))
        area2 = sum(geom.det(p,q) for p,q in edges)
        assert area2 == n*g.a*g.b
        # The slant may pass through intermediate vertices. The signed chain
        # need only represent the actual region; opposite overlaps can cancel.
        vectors = [geom.sub(q,p) for p,q in edges]
        score = sum(abs(geom.det(u,v)) for u,v in combinations(vectors,2))
        assert 2*area2 <= score
        result.append(dict(tiles=n,owners=len(edges)-1,twice_doubled_area=str(2*area2),
                           zonotope_area=str(score),
                           supported_word_lengths={q:supported_words(edges,q) for q in (g.a,g.b)}))
    return result

def equality_review(a,b,c,m,n):
    # Enumerate half-side counts, build the CCW polygon, check its area directly.
    # This scan needs no bank-character equations or determinant optimization.
    from itertools import combinations_with_replacement
    u = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
    rejects = Counter()
    for multi in combinations_with_replacement(range(6),m//2):
        counts = Counter(multi)
        x = y = area2 = 0
        for j,(ux,uy) in enumerate(u):
            vx,vy = u[(j-1)%6]
            for dx,dy,k in [(a*ux+b*vx,a*uy+b*vy,counts[j%3]),
                            (c*ux,c*uy,counts[3+j%3])]:
                area2 += k*(x*dy-y*dx)
                x += k*dx
                y += k*dy
        assert (x,y)==(0,0)
        if area2 != n*a*b:
            continue
        # In the cyclic order-a projection high(j) is followed by low(j+1).
        # Every aggregate syllable survives even at the cyclic join.
        powers = [(c*counts[3+j%3]+b*counts[(j+1)%3])%a for j in range(3)]
        assert all(powers)
        rejects[tuple(sorted(powers))] += 1
    assert rejects
    return {str(k):v for k,v in rejects.items()}

if __name__=='__main__':
    print(json.dumps(dict(controls={w:controls(w) for w in ('known','macro')},
                          extremal_syllables={3431:equality_review(33,7,37,24,592),
                                              5063:equality_review(35,13,43,22,344)}),indent=2))
