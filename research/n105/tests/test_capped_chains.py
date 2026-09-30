#!/usr/bin/env python3
"""Positive-witness regression for capped straight-chain restrictions.
Actual finite patches of congruent (5,16,19) triangles include a half-shifted
interface with genuine T-junctions. Random subsets of the known tiling are
removed. The true remaining tiles must never violate the new restrictions.
These tests are not a proof of the lemma or a substitute for certificate replay.
"""
import json,random
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"search"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine_16_5_19 as g
from replay_16 import Checker


def patch(offset, m=4,n=2):
    x,y=offset
    def p(i,j):return g.point(x+5*i-16*j,y+16*j)
    ts=[]
    for i in range(m):
        for j in range(n):
            ts.extend([g.triangle((p(i,j),p(i+1,j),p(i,j+1))),
                       g.triangle((p(i+1,j),p(i+1,j+1),p(i,j+1)))])
    return ts


def run():
    a=patch((F(0),F(0)))
    b=patch((F(-32)+F(5,2),F(32)))
    alltiles=tuple(sorted(set(a+b)))
    if len(alltiles)!=32:raise AssertionError('wrong witness size')
    for i,t in enumerate(alltiles):
        if sorted(g.norm2(g.TRI[t][j],g.TRI[t][(j+1)%3]) for j in range(3))!=[25,256,361]:raise AssertionError('noncongruent witness')
        if any(g.overlap(t,u) for u in alltiles[:i]):raise AssertionError('overlap in positive witness')
    # add_tiles subtracts tiles; reversing gives the outer union boundary.
    outer=tuple((q,p) for p,q in g.add_tiles((),alltiles))
    original=g.OUT_EDGES;g.OUT_EDGES=outer;g.bounded_sides.cache_clear()
    data={'points':[[str(x),str(y)] for x,y in g.XY], 'triangles':g.TRI,
          'outer':g.OUT,'tile':[5,16,19]}
    c=Checker(data)
    rng=random.Random(6341051630)
    cases=edges=positive_rays=0
    known_interior_edge_points=set()
    for t in alltiles:
        for j,p in enumerate(g.TRI[t]):
            q=g.TRI[t][(j+1)%3]
            for u in alltiles:
                for r in g.TRI[u]:
                    if r not in(p,q) and g.on_segment(p,q,r):known_interior_edge_points.add(r)
    if not known_interior_edge_points:raise AssertionError('T-junction witness missing')
    try:
        subsets=[(),alltiles]
        subsets += [tuple(t for t in alltiles if rng.randrange(5)<k) for k in range(1,5) for _ in range(64)]
        for placed in subsets:
            remaining=set(alltiles)-set(placed)
            boundary=g.add_tiles(outer,placed)
            bounds=g.bounded_sides(tuple(sorted(placed)))
            c.boundary=lambda unused, boundary=boundary:boundary
            limits=c.whole_side_bounds(placed)
            if bounds is None or limits is None:raise AssertionError('false rejection of a known completion')
            if bounds!=limits:raise AssertionError('two chain-bound implementations disagree')
            for (v,ray),L in bounds.items():
                found=False
                for t in remaining:
                    if v not in g.TRI[t]:continue
                    # Every actual remaining tile incident at the convex endpoint
                    # must satisfy each bound ray it uses.
                    if not g.bound_fan(v,(t,),bounds) or not c.permitted_fan(v,(t,),limits):
                        raise AssertionError('true remaining tile was discarded')
                    for w in g.TRI[t]:
                        if w!=v and g.direction(v,w)==ray:found=True;positive_rays+=1
                if not found:raise AssertionError('known completion does not support capped ray')
                edges+=1
            cases+=1
    finally:g.OUT_EDGES=original;g.bounded_sides.cache_clear()
    result={'result':'PASS','known_congruent_tiles':len(alltiles),
            'strict_edge_interior_vertices':len(known_interior_edge_points),
            'positive_completion_subsets':cases,'capped_endpoint_rays_checked':edges,
            'true_tile_incident_edges_checked':positive_rays,
            'scope':'Regression only. Convex caps and whole-edge lemma require mathematical proof.'}
    return result

if __name__=='__main__':
    result=run();print(json.dumps(result,indent=2))
    (Path(__file__).resolve().parents[1]/'verification/capped_chain_tests.json').write_text(json.dumps(result,indent=2)+'\n')
