#!/usr/bin/env python3
"""Independent rational checks of the supported-long-cycle cut helper.

The production detector uses integer c-power points and graph traversal.
Every reported witness is reconstructed here using Fraction coordinates,
independent multiplication, metric and signed-area checks. Synthetic
three-side cycles are contained nonoverlapping partial packings, not full
tilings. The target theorem excludes their extension to a full tiling.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
sys.path.insert(0, str(PACKAGE / 'owned'))
from legacy import core, ROOT
from long_cycles import long_edge, raw_selected_long_cycles, selected_long_cycles

U = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def scale(t,p): return t*p[0],t*p[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def norm(p): return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def mul(p,q): return p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1]


def power(z,h):
    if h<0: z=(z[0]+z[1],-z[1]);h=-h
    answer=(Q(1),Q(0))
    for _ in range(h): answer=mul(answer,z)
    return answer


def point(g,p): return Q(p[0],g.c**p[2]),Q(p[1],g.c**p[2])


def reconstruct(g,t):
    q,h,j,s=t;q=point(g,q);z=(Q(g.a,g.c),Q(g.b,g.c))
    first=add(q,scale(-g.a,mul(power(z,h),U[j%6])))
    last=add(q,scale(g.b,mul(power(z,h),U[(j+s)%6])))
    triangle=(first,q,last)
    if det(sub(q,first),sub(last,first))<0:triangle=triangle[::-1]
    assert sorted(norm(sub(triangle[i],triangle[(i+1)%3])) for i in range(3))==sorted((g.a*g.a,g.b*g.b,g.c*g.c))
    assert all(x>=0 and y>=0 and g.B*x+g.A*y<=g.A*g.B for x,y in triangle)
    return triangle,(h+s,tuple(sorted((first,last))))


def disjoint(first,second):
    for left,right in ((first,second),(second,first)):
        for i,p in enumerate(left):
            d=sub(left[(i+1)%3],p)
            if max(det(d,sub(q,p)) for q in right)<=0:return True
    return False


def witness_check(g,tiles,chosen,witness):
    indices=witness['indices'];h=witness['height'];vertices=[point(g,p) for p in witness['vertices']]
    assert len(indices)>=3 and len(set(indices))==len(indices)
    assert set(indices)<=set(chosen)
    assert len(vertices)==len(indices)+1 and vertices[0]==vertices[-1]
    assert len(set(vertices[:-1]))==len(indices)
    assert len(witness['edges'])==len(indices)
    z=(Q(g.a,g.c),Q(g.b,g.c));unit=power(z,h)
    inverse=(unit[0]+unit[1],-unit[1])
    distinct=set()
    for i,(index,edge) in enumerate(zip(indices,witness['edges'])):
        _,(height,endpoints)=reconstruct(g,tiles[index])
        assert height==h and endpoints==tuple(sorted((vertices[i],vertices[i+1])))
        assert edge['representative']==index
        assert point(g,edge['from'])==vertices[i] and point(g,edge['to'])==vertices[i+1]
        delta=sub(vertices[i+1],vertices[i]);assert norm(delta)==g.c*g.c
        assert scale(Q(1,g.c),mul(inverse,delta)) in U
        assert endpoints not in distinct;distinct.add(endpoints)
        all_owners=[]
        for owner in chosen:
            _,(H,ends)=reconstruct(g,tiles[owner])
            if H==h and ends==endpoints:all_owners.append(owner)
        assert edge['selected_owners']==sorted(all_owners)
        assert index==min(all_owners)
    area=sum(det(p,q) for p,q in zip(vertices,vertices[1:]))
    assert area!=0
    return {'edge_count':len(indices),'height':h,'twice_axial_area':str(abs(area))}


def support(g,first,last,height,direction,right=True):
    candidates=[]
    for off,H,J,s,_ in g.inverse(height,direction%3):
        tile=(g.add(first,off),H,J,s)
        hh,ends=long_edge(g,tile)
        if hh!=height or ends!=tuple(sorted((first,last))):continue
        triangle=g.vertices(tile)
        third=next(p for p in triangle if p not in ends)
        side=det(sub(point(g,last),point(g,first)),sub(point(g,third),point(g,first)))
        if (side<0)==right and g.admissible(tile):candidates.append(tile)
    assert len(set(candidates))==2
    return min(candidates)


def triangle_fixture(g,height,shift=0):
    origin=(g.A//4+shift,g.B//4,0)
    first=g.add(origin,g.scale(g.c,g.unit(height,0)))
    second=g.add(origin,g.scale(g.c,g.unit(height,1)))
    points=(origin,first,second)
    tiles=[support(g,points[i],points[(i+1)%3],height,j)
           for i,j in enumerate((0,2,4))]
    polygons=[reconstruct(g,t)[0] for t in tiles]
    assert all(disjoint(p,q) for p,q in combinations(polygons,2))
    return tiles,points


def main():
    reports=[]
    for sides in ((33,7,37),(35,13,43)):
        g=core.Geometry(*sides);cases=[]
        for h in (-5,-1,0,1,7):
            tiles,points=triangle_fixture(g,h)
            cycles=selected_long_cycles(g,tiles,range(3));assert len(cycles)==1
            cases.append(witness_check(g,tiles,range(3),cycles[0]))
            assert not selected_long_cycles(g,tiles,[0,1])
            mate=support(g,points[0],points[1],h,0,right=False)
            doubled=tiles+[mate]
            assert not selected_long_cycles(g,doubled,[0,3])
            cycles=selected_long_cycles(g,doubled,range(4));assert len(cycles)==1
            witness_check(g,doubled,range(4),cycles[0])
            assert any(len(e['selected_owners'])==2 for e in cycles[0]['edges'])
            alternate=selected_long_cycles(g,doubled,[1,2,3]);assert len(alternate)==1
            witness_check(g,doubled,[1,2,3],alternate[0])
        first,_=triangle_fixture(g,0);second,_=triangle_fixture(g,0,shift=4*g.c)
        separate=first+second
        cycles=selected_long_cycles(g,separate,range(6));assert len(cycles)==2
        for w in cycles:witness_check(g,separate,range(6),w)
        # Two triangles sharing a mesh edge give two cycles in one component.
        p=(g.A//4,g.B//4,0)
        v=g.add(p,g.scale(g.c,g.unit(0,0)))
        w=g.add(p,g.scale(g.c,g.unit(0,1)))
        x=g.add(v,g.scale(g.c,g.unit(0,1)))
        paths=[(p,v,0),(v,x,1),(x,w,3),(w,p,4),(v,w,2)]
        connected=[support(g,u,v,0,j) for u,v,j in paths]
        cycles=selected_long_cycles(g,connected,range(5));assert len(cycles)==1
        witness_check(g,connected,range(5),cycles[0])
        roots=json.loads((PACKAGE/'corners'/('ROOTS_%d.json'%g.N)).read_text())
        assert all(not selected_long_cycles(g,r['tiles'],range(6)) for r in roots['surviving_roots'])
        reports.append({'N':g.N,'synthetic_contained_nonoverlapping_cycles':cases,
                        'two_bank_duplicates_do_not_create_two_edge_cycles':True,
                        'alternative_edge_owner_checked':True,
                        'two_disjoint_components_yield_two_cycles':True,
                        'one_cycle_per_component_checked':True,
                        'initial_corner_roots_checked':128,'initial_root_exclusions':0})
    control=json.loads((ROOT/'research/2026-11-20/semiprimes/continuation/global-endpoints/tiling_143.json').read_text())
    g=core.Geometry(*control['sides']);tiles=control['tiles']
    raw=raw_selected_long_cycles(g,tiles,range(len(tiles)))
    assert not raw and not selected_long_cycles(g,tiles,range(len(tiles)))
    report={'status':'PASS','targets':reports,
            'control143':{'all143_long_sides_scanned':True,'raw_cycles':len(raw),
                          'target_specific_no_good_disabled':True},
            'scope':'The helper exports exact selected-index necessary no-goods under the existing all-height supported-cycle theorem. No target completion or root exclusion is asserted by these controls.'}
    (HERE/'LONG_CYCLE_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
