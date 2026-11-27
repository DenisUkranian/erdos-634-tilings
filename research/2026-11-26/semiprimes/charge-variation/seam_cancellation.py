"""Exact mesh, word-projection and native-bank checks for a cancelled middle bank."""
from collections import Counter
from fractions import Fraction
import json
from math import gcd


def mesh(a,b,c):
    end = (a+b,-b)
    H = a*(a+2*b)
    peak = (Fraction(H*a,c*c),Fraction(H*b,c*c))
    corners = ((0,0),end,peak)
    def inside(x,y):
        for (u,v),(s,t) in zip(corners,corners[1:]+corners[:1]):
            if (s-u)*(y-v)-(t-v)*(x-u)<0:
                return False
        return True
    vertices = {(x,y) for x in range(int(max(end[0],peak[0]))+1)
                for y in range(-b,int(peak[1])+1) if inside(x,y)}
    # Second membership calculation from barycentric coordinates.
    for x in range(int(max(end[0],peak[0]))+1):
        for y in range(-b,int(peak[1])+1):
            det = end[0]*peak[1]-end[1]*peak[0]
            u,v = (x*peak[1]-y*peak[0])/det,(end[0]*y-end[1]*x)/det
            assert ((x,y) in vertices)==(u>=0 and v>=0 and u+v<=1)
    differences = {(x-u,y-v) for x,y in vertices for u,v in vertices
                   if (x-u)%a==0 and (y-v)%a==0}
    assert differences=={(0,0),(a,0),(-a,0)}
    exceptional = set()
    width = 0
    for y in range(-b,int(peak[1])):
        for dx in (0,-1):
            starts = {x for x,j in vertices if j==y and (x+dx,y+1) in vertices}
            canonical = {a-y} if y<0 and dx==-1 else set()
            assert canonical<=starts
            residues = Counter(x%a for x in starts)
            available = {x for x in starts if residues[x%a]>1 or
                         any((x-u)%a==0 for u in canonical)}
            if available!=canonical:
                exceptional.add(y)
            # Linear independence of the two residue projections, checked
            # directly by leaf elimination in their bipartite incidence graph.
            remaining = set(starts)
            while remaining:
                left = Counter(t%a for t in remaining)
                right = Counter(t%b for t in remaining)
                leaves = {t for t in remaining if left[t%a]==1 or right[t%b]==1}
                assert leaves
                remaining -= leaves
            if starts:
                width = max(width,max(starts)-min(starts))
    assert gcd(a,b)==1 and width<a+b-1
    if exceptional:
        assert max(exceptional)-min(exceptional)+1<b
        assert min(exceptional)<=0<=max(exceptional)+1
    return dict(vertices=len(vertices),ambiguous_lower_rows=sorted(exceptional),
                maximum_heading_span=width,lcm_degree=a+b-1)


def bank_displacements(a,b,c):
    # In the short chart of B either relative rotation gives the same
    # smallest hex distance, by conjugation of the unit mesh.
    unit = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
    attainable = {(0,0)}
    for n in range(1,c+1):
        attainable = {(x+u,y+v) for x,y in attainable for u,v in unit}
        allowed = {(x,y) for x,y in attainable if (x or y) and
                   (a*x-b*y)%c==0 and (b*x+(a+b)*y)%c==0}
        if allowed:
            return n


def control(name):
    from verify import geom, reconstruct, cell, step
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polys,centroids,centre,*_ = geom.check_full_tiling(g,tiles)
    matched,_ = geom.long_pairs(g,tiles,polys,centroids,centre)
    lifts,T = reconstruct(g,tiles,polys)
    C,B = T[:1],T[:-1]
    banks = Counter()
    for i,tile in enumerate(tiles):
        v = lifts[i]
        w = step(v,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))
        if v==B and i not in matched:
            banks[w]+=1
    assert banks[C] and banks[T]
    threshold = bank_displacements(5,3,7)
    for gate in (C,T):
        signs = sum(-geom.eps(tile) for i,tile in enumerate(tiles) if i not in matched
                    and lifts[i]==B and step(B,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))==gate)
        assert signs%3==0 or banks[gate]>=threshold
    origin = g.scale(g.B,g.unit(2,0))
    def middle_coordinates(p):
        image = g.sub(origin,g.mult(g.unit(2,1),(p[0]+p[1],-p[1],p[2])))
        return tuple(coord/g.c for coord in geom.point(g,g.mult(image,g.unit(-1,0))))
    long_edges = set()
    inside_cap = 0
    for tile in tiles:
        poly = [middle_coordinates(p) for p in g.vertices(tile)]
        long_edges.add(tuple(sorted((poly[-1],poly[0]))))
        # The cap is bounded by the board base, y=0 and x+y=a.
        within = [y<=0 and x+y<=g.a for x,y in poly]
        inside_cap += all(within)
    path = [(x,0) for x in range(g.a+1)]+[(g.a+j,-j) for j in range(1,g.b+1)]
    count = sum(tuple(sorted((p,q))) in long_edges for p,q in zip(path,path[1:]))
    return dict(unmatched=[banks[C],banks[T]],canonical_whole_long_steps=count,
                canonical_length=g.a+g.b,tiles_entirely_in_cap=inside_cap)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    print(json.dumps(dict(mesh={str(c):mesh(a,b,c) for a,b,c in
                                ((5,3,7),(33,7,37),(35,13,43))},
                          minimum_nonzero_middle_displacement_steps={str(c):bank_displacements(a,b,c) for a,b,c in
                                ((5,3,7),(33,7,37),(35,13,43))},
                          controls_143={s:control(s) for s in ('known','macro')}),
                     indent=2))
