#!/usr/bin/env python3
"""Exact geometry, full 143 preservation, ownership deletion, and SMT controls.

No negative target search is performed. libz3 is needed for the optional
encoding/integration portion; --geometry-only runs the arithmetic portion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import gcd, lcm
from pathlib import Path
import tempfile

from legacy import ROOT, core, CornerOracle
from owned_oracle import OwnedCornerOracle
from owned_search import OwnedSearch, defaults
from exact_geometry import polygon_record, records_overlap, overlap_pairs


def rational(p,c):
    return F(p[0],c**p[2]),F(p[1],c**p[2])


def exact_physical_control(g,tiles):
    polygons = [tuple(rational(p,g.c) for p in g.vertices(t)) for t in tiles]
    currents = Counter()
    area = F(0)
    def edge(p,q,multiplicity):
        dx,dy = q[0]-p[0],q[1]-p[1]
        denominator = lcm(dx.denominator,dy.denominator)
        x,y = int(dx*denominator),int(dy*denominator)
        divisor = gcd(abs(x),abs(y))
        x,y = x//divisor,y//divisor
        if x<0 or (x==0 and y<0):
            x,y=-x,-y
        line = x*p[1]-y*p[0]
        currents[x,y,line,p] -= multiplicity
        currents[x,y,line,q] += multiplicity
    for polygon in polygons:
        norms=[]
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            dx,dy=q[0]-p[0],q[1]-p[1]
            norms.append(dx*dx+dx*dy+dy*dy)
            edge(p,q,1)
        assert sorted(norms)==sorted((g.a*g.a,g.b*g.b,g.c*g.c))
        signed=sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(polygon,polygon[1:]+polygon[:1]))
        assert signed==g.a*g.b
        area += signed
        assert all(x>=0 and y>=0 and g.B*x+g.A*y<=g.A*g.B for x,y in polygon)
    board=((F(0),F(0)),(F(g.A),F(0)),(F(0),F(g.B)))
    for p,q in zip(board,board[1:]+board[:1]):
        edge(p,q,-1)
    assert not any(currents.values())
    assert area==g.A*g.B==g.N*g.a*g.b
    assert not overlap_pairs(g,tiles,range(len(tiles)))
    return polygons


def through_incidents(g,tiles):
    points={p for t in tiles for p in g.vertices(t)}
    roots_at={p:[t for t in tiles if p in g.vertices(t)] for p in points}
    result=[]
    for through in tiles:
        polygon=g.vertices(through)
        for k in range(3):
            q0,q1=polygon[(k+1)%3],polygon[k]
            side=g.sub(q1,q0)
            decoded=[(h,j,L) for h in (through[1]-1,through[1],through[1]+1)
                     for j in range(6) for L in (g.a,g.b,g.c)
                     if side==g.scale(L,g.unit(h,j))]
            assert len(decoded)==1
            h,j,L=decoded[0]
            vx,vy=rational(side,g.c)
            for p in points:
                dx,dy=rational(g.sub(p,q0),g.c)
                if vx*dy!=vy*dx:
                    continue
                lam=dx/vx if vx else dy/vy
                if 0<lam<1:
                    offset=lam*L
                    assert offset.denominator==1 and 1<=offset<=L-1
                    result.append((through,p,(h,j),L,int(offset),roots_at[p]))
    return result


def geometry_checks(tiles,g):
    selected=set(tiles)
    oracle=OwnedCornerOracle(g)
    old=CornerOracle(g)
    exact_physical_control(g,tiles)
    charges=Counter()
    counts=Counter()
    for _,h,j,s in tiles:
        charges[h%2]+=s*(-1 if j%2 else 1)
        counts[h%2]+=1
    assert (counts[1],charges[1],counts[0],charges[0])==(105,-7,38,-2)
    for t in tiles:
        for p in g.vertices(t):
            assert oracle.owned_satisfied(t,p,selected)
    incidents=through_incidents(g,tiles)
    assert len(incidents)==38
    deleted_checks=0
    for through,p,ray,L,offset,roots in incidents:
        assert through in oracle.through_candidates(p,ray)
        for t in roots:
            assert through not in old.candidates(t,p)
            assert old.satisfied(t,p,selected-{through})
            assert not oracle.owned_satisfied(t,p,selected-{through})
            deleted_checks+=1
    assert deleted_checks==114
    # Check the arbitrary-denominator overlap code at negative and high
    # short heights, including a genuine overlap and a whole long-side mate.
    large=core.Geometry(35,13,43)
    overlap_checks=0
    for h in range(-4,5):
        tile=((500,500,0),h,0,1)
        shifted=(large.add(tile[0],large.unit(h,0)),h,0,1)
        q=tile[0]
        u=large.sub(q,large.scale(large.a,large.unit(h,0)))
        w=large.add(q,large.scale(large.b,large.unit(h,1)))
        mate=(large.sub(large.add(u,w),q),h,3,1)
        assert records_overlap(polygon_record(large,tile),polygon_record(large,shifted))
        assert not records_overlap(polygon_record(large,tile),polygon_record(large,mate))
        overlap_checks+=2
    # Any selected subset extends by its actual omitted control tiles.
    reserve_checks=0
    for modulus in range(1,12):
        for residue in range(modulus):
            subset=[t for i,t in enumerate(tiles) if i%modulus==residue]
            Go=sum(s*(-1 if j%2 else 1) for _,h,j,s in subset if h%2)
            Ge=sum(s*(-1 if j%2 else 1) for _,h,j,s in subset if not h%2)
            assert len(subset)+abs(-g.c-Go)+abs(-(g.a-g.b)-Ge)<=g.N
            for sigma in (-1,1):
                for tau in (-1,1):
                    m=sum(s*(-1 if j%2 else 1)==(-sigma if h%2 else -tau)
                          for _,h,j,s in subset)
                    assert 2*m<=g.N+sigma*g.c+tau*(g.a-g.b)
                    reserve_checks+=1
    return oracle,incidents,dict(physical_tiles=len(tiles),local_owned_fans=3*len(tiles),
        through_incidences=len(incidents),distinct_through_tiles=len({v[0] for v in incidents}),
        integer_offsets=True,deleted_owner_local_rejections=deleted_checks,
        arbitrary_height_overlap_checks=overlap_checks,charge_reserve_subset_checks=reserve_checks)


def local_smt_control(g,tiles,oracle,incident):
    through,p,ray,L,offset,roots=incident
    tile=roots[0]
    registry={}
    def insert(t):
        if t not in registry:
            registry[t]=len(registry)
        return registry[t]
    old=CornerOracle(g)
    old_term=old.constraint(tile,p,insert)
    new_term=oracle.owned_constraint(tile,p,insert)
    assert through in registry
    smt=core.SMT()
    try:
        assert smt.run('(set-option :timeout 30000)')==''
        assert smt.run('\n'.join(f'(declare-const x{i} Bool)' for i in registry.values()))==''
        def check(term,selection):
            assert smt.run('(push 1)')==''
            lines=[f'(assert {term})']
            lines.extend('(assert '+(f'x{i}' if t in selection else f'(not x{i})')+')'
                         for t,i in registry.items())
            assert smt.run('\n'.join(lines))==''
            result=smt.run('(check-sat)')
            assert smt.run('(pop 1)')==''
            return result
        selected=set(tiles)
        assert check(new_term,selected)=='sat'
        assert check(old_term,selected-{through})=='sat'
        assert check(new_term,selected-{through})=='unsat'
    finally:
        smt.close()
    return dict(local_positive='sat',old_local_deleted_owner='sat',new_local_deleted_owner='unsat',
                local_variables=len(registry))


def integrated_smt_control(tiles,g,workdir):
    rootfile=Path(__file__).resolve().parents[1]/'corners/ROOTS_143.json'
    args=defaults(out=str(workdir),sides=(5,3,7),root_file=str(rootfile),root_id='O1-X2-Y2',
                  max_columns=0,time_limit=0,rounds=0)
    search=OwnedSearch(args)
    selected=set(tiles)
    try:
        for tile in tiles:
            search.insert(tile)
        search.load_root()
        search.boundary()
        for tile in tiles:
            for row,_ in g.rows(tile):
                search.install(row)
            for p in g.vertices(tile):
                search.install_corner_tile(tile,p)
        search.flush()
        chosen=[search.index[t] for t in tiles]
        assert not search.add_overlap_conflicts(chosen)
        assert not search.selected_owner_rows(chosen)
        assert not search.guards and not search.guard_rows
        assert len(set(chosen)&search.owner_ids)==29
        for i in search.owner_ids:
            for row,sign in g.rows(search.tiles[i]):
                assert i in search.inc[row][(1-sign)//2]
        def fixed_check():
            _,_,bound=search.query_bounds()
            search.enqueue('(push 1)')
            search.enqueue(f'(assert {bound})')
            for i,t in enumerate(search.tiles):
                search.enqueue('(assert '+(f'x{i}' if t in selected else f'(not x{i})')+')')
            search.flush()
            status=search.smt.run('(check-sat)')
            assert status=='sat',(status,search.smt.run('(get-info :reason-unknown)'))
            search.enqueue('(pop 1)')
            search.flush()
        fixed_check()
        search.rebuild(1)
        search.flush()
        fixed_check()
        search.checkpoint(1,'exact-143-fixed-selection-control')
        return dict(integrated_positive='sat',after_equivalent_rebuild='sat',
                    canonical_actual_owners=29,full_selected_physical_rows=True,
                    columns=len(search.tiles),complete_rows=len(search.exact),
                    owned_fan_roots=len(search.corner_roots),permanent_assertions=len(search.clauses),
                    root_id='O1-X2-Y2',temporary_rows=False)
    finally:
        search.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--geometry-only',action='store_true')
    parser.add_argument('--out',help='Optional replay JSON; otherwise print only.')
    parser.add_argument('--workdir',help='Optional persistent directory for the integrated control model.')
    args=parser.parse_args()
    source=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    raw=source.read_bytes()
    data=json.loads(raw)
    assert data['sides']==[5,3,7] and data['N']==143
    tiles=tuple((tuple(t[0]),*t[1:]) for t in data['tiles'])
    assert len(tiles)==len(set(tiles))==143
    g=core.Geometry(5,3,7)
    oracle,incidents,geometry=geometry_checks(tiles,g)
    result=dict(status='PASS',control_sha256=hashlib.sha256(raw).hexdigest(),geometry=geometry,
                full_target_excluded=False)
    if not args.geometry_only:
        result['local_encoding']=local_smt_control(g,tiles,oracle,incidents[0])
        if args.workdir:
            result['integrated_encoding']=integrated_smt_control(tiles,g,Path(args.workdir))
        else:
            with tempfile.TemporaryDirectory(prefix='owned143-') as temp:
                result['integrated_encoding']=integrated_smt_control(tiles,g,Path(temp))
    if args.out:
        Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O: verification assertions are required.')
    main()
