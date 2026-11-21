#!/usr/bin/env python3
"""Recover every actual143 opposite bank; optional full solver integration."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import tempfile

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE/'owned'))
from legacy import ROOT,core
from verify_owned_controls import exact_physical_control,rational
from owned_search import defaults
from whole_edge_oracle import WholeEdgeOracle
from whole_edge_search import WholeEdgeSearch


def actual_bank(g,tiles,polygons,tile,index,edge):
    """Independent rational segment intersection, without candidate templates."""
    p,q=map(lambda v:rational(v,g.c),(edge.start,edge.end))
    ux,uy=(q[0]-p[0])/edge.length,(q[1]-p[1])/edge.length
    answer={}
    for other,polygon in zip(tiles,polygons):
        if other==tile:
            continue
        for k in range(3):
            r,s=polygon[k],polygon[(k+1)%3]
            if any(ux*(v[1]-p[1])-uy*(v[0]-p[0]) for v in (r,s)):
                continue
            third=polygon[(k+2)%3]
            if ux*(third[1]-p[1])-uy*(third[0]-p[0])>=0:
                continue
            tr=(r[0]-p[0])/ux if ux else (r[1]-p[1])/uy
            ts=(s[0]-p[0])/ux if ux else (s[1]-p[1])/uy
            lo,hi=max(F(0),min(tr,ts)),min(F(edge.length),max(tr,ts))
            if lo>=hi:
                continue
            assert tr.denominator==ts.denominator==1
            assert abs(tr-ts) in (g.a,g.b,g.c)
            assert other not in answer
            answer[other]=(int(lo),int(hi))
    return answer


def geometric_checks(g,tiles):
    selected=set(tiles)
    polygons=exact_physical_control(g,tiles)
    oracle=WholeEdgeOracle(g)
    boundary=interior=units=deleted=0
    max_neighbors=0
    example=None
    for tile in tiles:
        for k in range(3):
            edge=oracle.edge(tile,k)
            actual=actual_bank(g,tiles,polygons,tile,k,edge)
            if edge.boundary:
                assert not actual
                boundary+=1
                continue
            interior+=1
            units+=edge.length
            catalogue=oracle.catalogue(edge.start,edge.ray,edge.length)
            recovered={q:span for q,span in zip(catalogue.tiles,catalogue.spans) if q in selected}
            assert recovered==actual
            assert oracle.satisfied(tile,k,selected)
            max_neighbors=max(max_neighbors,len(actual))
            for other in actual:
                assert not oracle.satisfied(tile,k,selected-{other})
                deleted+=1
                if example is None:
                    example=tile,k,other
    assert (boundary,interior,units,deleted)==(25,404,2002,442)
    return oracle,example,dict(tiles=143,boundary_sides=boundary,interior_sides=interior,
        exact_unit_contacts=units,recovered_actual_banks=interior,
        maximum_actual_neighbors_per_side=max_neighbors,deleted_neighbor_rejections=deleted,
        physical_metric_area_current_and_nonoverlap=True)


def local_solver_control(g,tiles,oracle,example):
    tile,k,deleted=example
    selected=set(tiles)
    edge=oracle.edge(tile,k)
    bank=oracle.catalogue(edge.start,edge.ray,edge.length)
    registry={tile:0}
    for t in bank.tiles:
        if t not in registry:
            registry[t]=len(registry)
    groups=[tuple(registry[bank.tiles[i]] for i in group) for group in bank.intervals]
    smt=core.SMT()
    try:
        assert smt.run('(set-option :timeout 30000)')==''
        assert smt.run('\n'.join(f'(declare-const x{i} Bool)' for i in registry.values()))==''
        terms=[]
        for group in groups:
            terms.append('(assert (=> x0 (or '+' '.join(f'x{i}' for i in group)+')))')
            terms.append('(assert '+core.atmost(1,[f'x{i}' for i in group])+')')
        assert smt.run('\n'.join(terms))==''
        def fixed(selection):
            assert smt.run('(push 1)')==''
            assert smt.run('\n'.join('(assert '+(f'x{i}' if t in selection else f'(not x{i})')+')'
                                     for t,i in registry.items()))==''
            status=smt.run('(check-sat)')
            assert smt.run('(pop 1)')==''
            return status
        assert fixed(selected)=='sat'
        assert fixed(selected-{deleted})=='unsat'
        # A neighbor remains allowed when the antecedent tile is absent.
        assert fixed(selected-{tile})=='sat'
    finally:
        smt.close()
    return dict(positive='sat',deleted_neighbor='unsat',antecedent_absent_neighbors_allowed='sat',
                variables=len(registry),unit_intervals=edge.length)


def integrated_solver_control(g,tiles,out):
    args=defaults(sides=(5,3,7),out=str(out),grid_step=1,no_grid=False,
                  edge_tiles_per_round=8,vertex_fans_per_round=0,max_columns=0,time_limit=0,
                  root_file=str(PACKAGE/'corners/ROOTS_143.json'),root_id='O1-X2-Y2')
    search=WholeEdgeSearch(args)
    selected=set(tiles)
    try:
        for tile in tiles:
            search.insert(tile)
        search.load_root()
        search.boundary()
        for tile in tiles:
            for row,_ in g.rows(tile):
                search.install(row)
            search.install_tile_edges(tile)
        chosen=[search.index[t] for t in tiles]
        assert not search.selected_owner_rows(chosen)
        assert not search.add_overlap_conflicts(chosen)
        assert set(chosen)<=search.edge_complete_tiles
        assert len(set(chosen)&search.edge_neighbor_ids)==143
        search.flush()
        def fixed():
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
        fixed()
        search.rebuild(1)
        search.flush()
        fixed()
        search.checkpoint(1,'exact143-whole-edge-control')
        return dict(positive='sat',after_equivalent_rebuild='sat',all_actual_edges_enforced=True,
                    all_actual_endpoint_rows_completed=True,root_id='O1-X2-Y2',
                    columns=len(search.tiles),complete_rows=len(search.exact),
                    whole_edge_obligations=len(search.edge_obligations),
                    whole_edge_catalogues=len(search.edge_catalogues),
                    bank_cliques=len(search.edge_bank_cliques),
                    spatial_cliques=len(search.point_records),permanent_assertions=len(search.clauses),
                    temporary_rows=False)
    finally:
        search.close()


def restarted_solver_control(g,tiles,source,out):
    args=defaults(sides=(5,3,7),out=str(out),grid_step=1,no_grid=False,
                  edge_tiles_per_round=8,vertex_fans_per_round=0,max_columns=0,time_limit=0,
                  root_file=str(PACKAGE/'corners/ROOTS_143.json'),root_id='O1-X2-Y2',
                  model_checkpoint=str(source))
    search=WholeEdgeSearch(args)
    selected=set(tiles)
    try:
        search.load_root()
        search.boundary()
        search.flush()
        assert len(search.edge_obligations)==429 and len(search.exact)==335
        assert search.restart_metadata['prior_root_assumptions_imported'] is False
        assert search.root_metadata['id']=='O1-X2-Y2'
        _,_,bound=search.query_bounds()
        search.enqueue('(push 1)')
        search.enqueue(f'(assert {bound})')
        for i,tile in enumerate(search.tiles):
            search.enqueue('(assert '+(f'x{i}' if tile in selected else f'(not x{i})')+')')
        search.flush()
        status=search.smt.run('(check-sat)')
        assert status=='sat',(status,search.smt.run('(get-info :reason-unknown)'))
        search.enqueue('(pop 1)')
        search.flush()
        return dict(positive='sat',whole_edge_obligations=len(search.edge_obligations),
                    complete_rows=len(search.exact),columns=len(search.tiles),
                    prior_root_literals_not_imported=True,current_root_explicit=True)
    finally:
        search.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--with-solver',action='store_true',help='Also run local and integrated libz3 controls.')
    mode.add_argument('--geometry-only',action='store_true',help='Standard-library controls only (the default).')
    parser.add_argument('--out')
    parser.add_argument('--workdir')
    args=parser.parse_args()
    source=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    raw=source.read_bytes()
    data=json.loads(raw)
    assert data['sides']==[5,3,7] and data['N']==143
    tiles=tuple((tuple(t[0]),*t[1:]) for t in data['tiles'])
    assert len(tiles)==len(set(tiles))==143
    g=core.Geometry(5,3,7)
    oracle,example,geometry=geometric_checks(g,tiles)
    result=dict(status='PASS',control_sha256=hashlib.sha256(raw).hexdigest(),geometry=geometry,
                full_target_excluded=False)
    if args.with_solver:
        result['local_encoding']=local_solver_control(g,tiles,oracle,example)
        if args.workdir:
            work=Path(args.workdir)
            result['integrated_encoding']=integrated_solver_control(g,tiles,work)
            result['restart_encoding']=restarted_solver_control(g,tiles,work/'necessary_model.json',work/'restart')
        else:
            with tempfile.TemporaryDirectory(prefix='wholeedge143-') as temporary:
                work=Path(temporary)
                result['integrated_encoding']=integrated_solver_control(g,tiles,work)
                result['restart_encoding']=restarted_solver_control(g,tiles,work/'necessary_model.json',work/'restart')
    if args.out:
        Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O: verification assertions are required.')
    main()
