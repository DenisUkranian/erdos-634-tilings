"""Exact two-corner obstruction for six specified placements of (35,13,43)."""
from fractions import Fraction as F
from itertools import combinations, permutations

def add(p,q):
    return p[0]+q[0],p[1]+q[1]

def sub(p,q):
    return p[0]-q[0],p[1]-q[1]

def scale(p,k):
    return p[0]*k,p[1]*k

def product(p,q):
    return p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*q[0]+p[1]*q[1]

def det(p,q):
    return p[0]*q[1]-p[1]*q[0]

def norm2(p):
    x,y=p
    return x*x+x*y+y*y

def edges(tr):
    return zip(tr,tr[1:]+tr[:1])

def overlapping(t,u):
    return not any(all(det(sub(q,p),sub(x,p))<=0 for x in other)
                   for bank,other in ((t,u),(u,t)) for p,q in edges(bank))

def supports(tr,p,ray,sign):
    # A positive prefix of the ray lies on the triangle. Its interior is
    # strictly on the designated side of that ray.
    delta=[sub(v,p) for v in tr]
    heights=[sign*det(ray,w) for w in delta]
    axis=0 if ray[0] else 1
    offsets=[F(w[axis],ray[axis]) for w,h in zip(delta,heights) if h==0]
    return (min(heights)==0 and max(heights)>0 and len(offsets)==2
            and min(offsets)<=0<max(offsets))

def right_placements(p,left,right):
    assert norm2(right)==1 and det(left,right)>0
    for R,S,T in permutations((13,35,43)):
        # The CCW triangle has determinant area 455. Before rotation
        # the right ray is horizontal and the apex lies below it.
        y=F(-455,R)
        x=(F(R*R+S*S-T*T,R)-y)/2
        tr=(p,add(p,product(right,(x,y))),add(p,scale(right,R)))
        assert sorted(norm2(sub(v,u)) for u,v in edges(tr))==[13**2,35**2,43**2]
        if all(det(left,sub(v,p))>=0 and det(right,sub(v,p))<=0 for v in tr):
            yield R,S,T,tr

# A through F. Numerators of the six local triangles, at denominator 43.
data=[
    [(1505,0),(0,0),(0,-559)],
    [(-1505,0),(0,0),(0,559)],
    [(-262,2694),(193,1014),(817,559)],
    [(817,559),(362,2239),(-262,2694)],
    [(1155,3009),(1610,1329),(2234,874)],
    [(-93,3919),(362,2239),(986,1784)],
]
tiles={chr(65+i):tuple(scale(v,F(1,43)) for v in row) for i,row in enumerate(data)}

def obstruction():
    P=(0,0)
    Q=(19,13)
    horizontal=(1,0)
    vertical=(0,1)
    ray=(F(-13,43),F(48,43))
    for t in tiles.values():
        assert det(sub(t[1],t[0]),sub(t[2],t[0]))==455
        assert sorted(norm2(sub(v,u)) for u,v in edges(t))==[169,1225,1849]
    assert all(not overlapping(t,u) for t,u in combinations(tiles.values(),2))
    A,B,C,D,E,Ftile=tiles.values()
    assert supports(A,P,horizontal,-1) and supports(B,P,vertical,1)
    first=list(right_placements(P,horizontal,vertical))
    survivors=[tr for R,S,T,tr in first if not overlapping(C,tr)]
    assert len(first)==4 and len(survivors)==1
    forced=survivors[0]
    assert forced==(P,(35,13),(0,13))
    assert all(not overlapping(forced,t) for t in tiles.values())
    assert supports(forced,Q,horizontal,-1) and supports(D,Q,ray,1)
    second=list(right_placements(Q,horizontal,ray))
    assert len(second)==4
    assert all(any(overlapping(tr,f) and set(tr)!=set(f) for f in (E,Ftile))
               for R,S,T,tr in second)
    for label,rows,blockers in [('P',first,{'C':C}),('Q',second,{'E':E,'F':Ftile})]:
        print(label,[(R,S,T,''.join(k for k,t in blockers.items() if overlapping(tr,t)) or 'forced')
                     for R,S,T,tr in rows])
    assert all(set(tr)!=set(C) for R,S,T,tr in first)

def grids():
    target=((0,0),(1079,0),(0,2135))
    U=(F(624,43),F(-455,43))
    V=(F(455,43),F(-1680,43))
    H=target[1]
    bridge=[[(9,10),(8,10),(8,9)],[(7,10),(8,10),(8,11)]]
    outer=[[(16,5),(16,4),(15,4)],[(15,4),(15,5),(16,5)],
           [(13,6),(13,5),(12,5)],[(15,6),(15,5),(14,5)]]
    copies=[]
    for copy in (0,1):
        place=scale((-260,315),copy)
        origin=add((800,302),place)
        group=[tuple(add(origin,v) for v in tr) for tr in tiles.values()]
        assert all(det(sub(v,u),sub(x,u))>=0 for u,v in edges(target) for tr in group for x in tr)
        assert all(det(sub(v,u),sub(add(origin,local),u))>0 for u,v in edges(target)
                   for local in ((0,0),(19,13)))
        for i,T in enumerate(bridge):
            assert all(0<=x<=y<=11 for x,y in T)
            assert group[i]==tuple(add(place,(520+35*x,172+13*y)) for x,y in T)
        for i,T in enumerate(outer):
            cel=[(x+15*copy,y+4*copy) for x,y in T]
            assert all(y<=x<=43 for x,y in cel)
            assert all(y>=4*(1+copy) and y<=8+35*copy for x,y in cel)
            assert all(x<=28+15*copy for x,y in cel)
            assert group[i+2]==tuple(sub(sub(H,scale(U,x)),scale(V,y)) for x,y in cel)
        copies.append(group)
    assert all(not overlapping(t,u) for t in copies[0] for u in copies[1])
    # The two defect interiors are the only positive-overlap zones.
    defects=[((905,315),(819,315),(F(36465,43),F(12635,43)))]
    defects.append(tuple(add(v,(-260,315))for v in defects[0]))
    assert all(not overlapping(t,u) for group in copies for t in group for u in defects)
    print('two disjoint copies in the ordinary bridge and outer grids, outside both defect interiors')

def left_placements(p,left,right):
    assert norm2(left)==1 and det(left,right)>0
    for R,S,T in permutations((13,35,43)):
        y=F(455,R)
        x=(F(R*R+S*S-T*T,R)-y)/2
        tr=(p,add(p,scale(left,R)),add(p,product(left,(x,y))))
        assert sorted(norm2(sub(v,u)) for u,v in edges(tr))==[169,1225,1849]
        if all(det(left,sub(v,p))>=0 and det(right,sub(v,p))<=0 for v in tr):
            yield R,S,T,tr

def replay_patterns():
    import json,sys
    from pathlib import Path
    # The current directory can contain this module or a path can be supplied.
    if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
    from packing_replay import inventory
    from check_inventory import contained,overlap_pairs
    listing=json.loads(Path(__file__).with_name('corner_trees.json').read_text())
    board,positive,negative,defects=inventory(35,13,43)
    assert len(positive)==5071
    inside={i for i,t in enumerate(positive) if contained(t,board)}
    undirected={i for pair in overlap_pairs(positive,inside) for i in pair}
    lookup={frozenset(map(tuple,t)):i for i,t in enumerate(positive)}
    assert len(lookup)==len(positive)
    selected=set()
    for name,case in listing.items():
        ids=case['first_copy_inventory_ids']
        local=[[sub(scale(tuple(p),F(1,43)),(800,302)) for p in positive[i]] for i in ids]
        if name in ('first','alternate'):
            letters='ABDF' if name=='first' else 'ABDE'
            assert [set(t)for t in local]==[set(tiles[k])for k in letters]
        both=[]
        for origin in ((800,302),(540,617)):
            for t in local:
                cells=[scale(add(origin,p),43) for p in t]
                assert all(x.denominator==y.denominator==1 for x,y in cells)
                key=frozenset((int(x),int(y)) for x,y in cells)
                both.append(lookup[key])
        assert len(both)==len(set(both)) and set(both)<=inside
        assert set(both).isdisjoint(undirected)
        if name!='alternate':
            assert selected.isdisjoint(both)
            selected.update(both)
        tree=case['nodes']
        rows=iter(tree)
        def visit(known,depth):
            d,x,y,lx,ly,rx,ry,side,n=next(rows)
            assert int(d)==depth
            p=(F(x),F(y));left=(F(lx),F(ly));right=(F(rx),F(ry))
            for off in ((800,302),(540,617)):
                pt=scale(add(p,off),43)
                assert all(det(sub(b,a),sub(pt,a))>0 for a,b in edges(board))
            assert any(supports(tr,p,left,-1) for tr in known)
            assert any(supports(tr,p,right,1) for tr in known)
            candidates=[]
            choose=left_placements if side==0 else right_placements
            for R,S,T,tr in choose(p,left,right):
                assert all(set(tr)!=set(u) for u in known)
                if all(not overlapping(tr,u) for u in known):
                    candidates.append(tr)
            assert len(candidates)==n
            for tr in candidates:visit(known+[tr],depth+1)
        visit(local,0)
        assert next(rows,None) is None
        print(name,len(ids),'fixed tiles,',len(tree),'verified split nodes, all leaves impossible')
    assert len(selected)==2*(4+14+16)
    print('6 disjoint impossible groups on 68 isolated inventory placements')

if __name__=='__main__':
    obstruction()
    grids()
    replay_patterns()
