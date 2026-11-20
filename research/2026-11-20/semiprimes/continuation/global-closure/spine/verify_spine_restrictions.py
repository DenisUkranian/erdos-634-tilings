#!/usr/bin/env python3
"""Exact 143 controls for the spine classification and native contact rules."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from math import ceil,floor
from pathlib import Path
import argparse
import json
import sys

from native_spine import SpineCatalogue,find_control
from spine_sat import locate_continuation,install_restriction


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--continuation',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    continuation=args.continuation or locate_continuation()
    sys.path[:0]=[str(continuation/'global-endpoints/integer'),
                  str(continuation/'vertex-phase')]
    import global_core_sat as core
    Geometry=install_restriction(core)
    from phase_budget import PhaseBudget
    from corner_oracle import CornerOracle
    g=Geometry(5,3,7);cat=SpineCatalogue(5,3,7)
    trees=[PhaseBudget(g,sign) for sign in (1,-1)]
    native_count=closed_count=0
    for key in cat.placements():
        m,n,h,j,s=key
        q=cat.vertices(key)[1]
        tile=(g.point(*q,2),h,j,s)
        assert g.on_spine(tile)
        assert all(not tree.exterior_free(tree.node(tile[0],tree.sign*h))
                   for tree in trees)
        endpoint=g.add(tile[0],g.scale(-g.a,g.unit(h,j)))
        free=[]
        for tree in trees:
            short=tree.node(tile[0],tree.sign*h)
            long=tree.node(endpoint,tree.sign*(h+s))
            if tree.exterior_free(long):
                assert long[0]==short[0]+1
                assert tree.node(endpoint,short[0])==short
                free.append(tree.sign)
        assert bool(free)==(not g.long_gate_open(tile))
        native_count+=1
        closed_count+=bool(free)
    data=json.loads((continuation/'global-endpoints/tiling_143.json').read_text())
    tiles=[(tuple(q),h,j,s) for q,h,j,s in data['tiles']]
    selected=set(tiles)
    closed_selected=0
    for tile in tiles:
        assert g.admissible(tile)
        if not g.long_gate_open(tile):
            assert g.mate(tile) in selected
            closed_selected+=1
    oracle=CornerOracle(g)

    @lru_cache(None)
    def candidates(p,ray):
        answers=set();unit=g.unit(*ray)
        for tile,low,high,length in oracle.through_intervals(p,ray):
            q,h,j,s=tile
            if h not in (0,1,2):
                continue
            for t in range(max(1,ceil(low)),min(length-1,floor(high))+1):
                shifted=g.add(q,g.scale(-t,unit)),h,j,s
                if g.admissible(shifted):
                    answers.add(shifted)
        return answers

    def scaled(p):
        x,y,e=p
        return Fraction(x*cat.D,g.c**e),Fraction(y*cat.D,g.c**e)

    all_vertices={p for tile in tiles for p in g.vertices(tile)}
    through_contacts=0;length_counts=Counter()
    for tile in tiles:
        vertices=g.vertices(tile)
        for u,v in zip(vertices,vertices[1:]+vertices[:1]):
            U,V=scaled(u),scaled(v)
            dx,dy=V[0]-U[0],V[1]-U[1]
            norm=(dx*dx+dx*dy+dy*dy)/(cat.D*cat.D)
            length=next(L for L in (g.a,g.b,g.c) if L*L==norm)
            reverse=g.sub(u,v)
            ray=next((H,J) for H in range(tile[1]-1,tile[1]+2)
                     for J in range(6) if g.scale(length,g.unit(H,J))==reverse)
            for p in all_vertices:
                if p in (u,v):
                    continue
                P=scaled(p);px,py=P[0]-U[0],P[1]-U[1]
                if dx*py-dy*px:
                    continue
                ratio=px/dx if dx else py/dy
                if not 0<ratio<1:
                    continue
                offset=ratio*length
                assert offset.denominator==1 and 1<=offset<=length-1
                assert tile in candidates(p,ray)
                through_contacts+=1
                length_counts[length]+=1
    report={'scope':'Exact positive controls of necessary geometric restrictions, not target nonexistence.',
            'native_control_catalogue':native_count,
            'closed_gate_control_placements':closed_count,
            'all_native_placements_nonfree_in_both_trees':True,
            'closed_gate_exactly_free_long_node_in_at_least_one_tree':True,
            'known_143_tiles':143,'known_closed_gate_tiles_with_actual_mates':closed_selected,
            'actual_through_contacts_checked':through_contacts,
            'through_side_lengths':dict(sorted(length_counts.items())),
            'all_actual_offsets_integral':True,
            'all_actual_through_tiles_retained_by_native_oracle':True,
            'checks':'PASS'}
    output=json.dumps(report,indent=2)+'\n'
    if args.out:
        args.out.write_text(output)
    print(output,end='')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
