#!/usr/bin/env python3
"""Refine only complete physical rows using actual partial integer selections.

There are no temporary-row assumptions. Exact selected-overlap conflicts and
complete incident rows are valid necessary cuts in the declared regime.
Solver infeasibility is a candidate requiring independent proof validation.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
import time

import scoped_physical_search as scoped


def overlap(a, b):
    """Strict overlap of convex CCW triangles by exact separating axes."""
    for first, second in ((a,b),(b,a)):
        for i in range(3):
            x,y = first[i]
            u,v = first[(i+1)%3]
            if max((u-x)*(q-y)-(v-y)*(p-x) for p,q in second) <= 0:
                return False
    return True


def integer_vertices(g, tile):
    result=[]
    for x,y,e in g.vertices(tile):
        assert e<=2
        result.append((x*g.c**(2-e),y*g.c**(2-e)))
    return tuple(result)


def overlaps(g, tiles, chosen):
    bins=defaultdict(list)
    points={}
    boxes={}
    step=2*g.c**3
    result=set()
    for i in chosen:
        vertices=integer_vertices(g,tiles[i]);points[i]=vertices
        x0=min(p[0] for p in vertices);x1=max(p[0] for p in vertices)
        y0=min(p[1] for p in vertices);y1=max(p[1] for p in vertices)
        boxes[i]=(x0,x1,y0,y1)
        candidates=set()
        keys=list((x,y) for x in range(x0//step,x1//step+1)
                         for y in range(y0//step,y1//step+1))
        for key in keys:
            candidates.update(bins[key])
        for j in candidates:
            u0,u1,v0,v1=boxes[j]
            if x0>=u1 or u0>=x1 or y0>=v1 or v0>=y1:
                continue
            if overlap(vertices,points[j]):
                result.add((j,i))
        for key in keys:
            bins[key].append(i)
    return sorted(result)


def run(args):
    start=time.monotonic()
    scoped.ScopedGeometry.mode=args.mode
    scoped.base.Geometry=scoped.ScopedGeometry
    s=scoped.ScopedSearch(args)
    if args.use_seed:
        for tile in s.g.seed(None):
            if s.g.admissible(tile):
                s.insert(tile)
    s.boundary()
    for row in s.g.needs:
        s.install(row)
    if args.rows:
        for p,h,j in scoped.base.load_state(args.rows)['complete_rows']:
            s.install((tuple(p),h,j))
    rng=random.Random(args.random_seed)
    history=[]
    result='round-limit'
    last_selected=[]
    for iteration in range(args.rounds):
        s.enqueue('(push 1)')
        s.enqueue('(assert '+scoped.base.atmost(s.g.N,[f'x{i}' for i in range(len(s.tiles))])+')')
        s.flush()
        stamp=time.monotonic()
        status=s.smt.run('(check-sat)')
        record=dict(iteration=iteration,status=status,columns=len(s.tiles),complete_rows=len(s.exact),
                    solve_seconds=round(time.monotonic()-stamp,6))
        if status != 'sat':
            result='conditional-unsat-needs-proof-audit' if status=='unsat' else 'solver-inconclusive'
            if status=='unsat':
                (s.out/'candidate_unsat.smt2').write_text((s.out/'model.smt2').read_text()+'\n(check-sat)\n')
                if args.proof:
                    (s.out/'candidate_proof.txt').write_text(s.smt.run('(get-proof)')+'\n')
            else:
                record['reason']=s.smt.run('(get-info :reason-unknown)')
            history.append(record);print(json.dumps(record),flush=True)
            break
        chosen=s.chosen();last_selected=chosen
        balance=Counter(s.g.needs)
        for i in chosen:
            for row,value in s.g.rows(s.tiles[i]):
                balance[row]-=value
        residual=[row for row,value in balance.items() if value]
        assert not set(residual)&s.exact
        conflicts=overlaps(s.g,s.tiles,chosen)
        record.update(selected=len(chosen),residual_rows=len(residual),overlap_pairs=len(conflicts))
        history.append(record);print(json.dumps(record),flush=True)
        if not residual:
            assert not conflicts
            s.save_solution();result='positive-needs-independent-geometric-verification'
            break
        s.enqueue('(pop 1)')
        for i,j in conflicts:
            s.assert_(f'(not (and x{i} x{j}))')
        rng.shuffle(residual)
        residual.sort(key=lambda row: -abs(balance[row]))
        for row in residual[:args.expand]:
            s.install(row)
        if len(s.tiles)>=args.max_columns:
            result='column-resource-limit'
            break
        if time.monotonic()-start>=args.wall_seconds:
            result='wall-resource-limit'
            break
    report=dict(mode=args.mode,N=s.g.N,odd_population=args.odd_population,
                joint_cell_reserve=args.cell_reserve,temporary_rows_used=False,
                status=result,full_target_excluded=False,
                columns=len(s.tiles),complete_rows=len(s.exact),
                seconds=round(time.monotonic()-start,6),history=history)
    (s.out/'status.json').write_text(json.dumps(report,indent=2)+'\n')
    (s.out/'complete_rows.json').write_text(json.dumps(dict(sides=args.sides,complete_rows=sorted(s.exact)),separators=(',',':'))+'\n')
    print('FINAL',result,flush=True)
    s.smt.close();s.journal.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=('3431-111','5063-215','143-control'),required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--rows')
    p.add_argument('--cell-reserve',action='store_true')
    p.add_argument('--use-seed',action='store_true')
    p.add_argument('--proof',action='store_true')
    p.add_argument('--rounds',type=int,default=100)
    p.add_argument('--expand',type=int,default=200)
    p.add_argument('--max-columns',type=int,default=250000)
    p.add_argument('--timeout-ms',type=int,default=30000)
    p.add_argument('--wall-seconds',type=int,default=600)
    p.add_argument('--random-seed',type=int,default=1776)
    args=p.parse_args()
    args.sides,args.odd_population={
        '3431-111':((33,7,37),111),'5063-215':((35,13,43),215),
        '143-control':((5,3,7),105)}[args.mode]
    args.point_checkpoint=None;args.seed_json=None;args.minimize_core=False
    run(args)


if __name__=='__main__':
    main()
