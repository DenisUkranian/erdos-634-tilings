#!/usr/bin/env python3
"""Permanent necessary-model search with actual whole through-tile owners.

No temporary incomplete-row equations, height cutoffs, or fixed odd
populations are used. An UNSAT response is a candidate requiring an
independent encoding/proof check; a root-conditioned response is local to
that explicitly recorded root. Resource limits never exclude a tiling.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import time

from legacy import ROOT, core, make_search_class, and_, or_, angular_groups, GracefulResourceStop
from owned_oracle import OwnedCornerOracle
from exact_geometry import overlap_pairs


LegacyCornerSearch = make_search_class(core)


def defaults(**changes):
    """Shared public constructor defaults for control and integration code."""
    values = dict(sides=(5,3,7), out=None, rows=None, seed_json=None,
                  corner_checkpoint=None, root_file=None, root_id=None,
                  timeout_ms=30000, rounds=50, expand=100,
                  owner_fans_per_round=2, owner_rows_per_round=0,
                  max_columns=200000, time_limit=600, max_rss_mb=0,
                  stop_file=None, random_seed=1776, proof=False,
                  minimize_core=False, point_checkpoint=None,
                  rebuild_every=10, angular_cliques=True,
                  core_policy='few_missing', corner_rows=0,
                  global_probe_every=0, checkpoint_every_query=False)
    values.update(changes)
    return argparse.Namespace(**values)


class OwnedSearch(LegacyCornerSearch):
    def __init__(self, args):
        self.started = time.monotonic()
        self.history = []
        self.iteration = 0
        self.owner_ids = set()
        self.owner_catalogues = {}
        self.owner_cliques = set()
        self.angular_records = set()
        self.overlap_records = set()
        self.fan_path_records = {}
        self.owned_root_clauses = {}
        self.root_indices = []
        self.root_metadata = None
        self.boundary_complete = False
        self.query_active = False
        super().__init__(args)
        self.corner = OwnedCornerOracle(self.g)

    def canonical_tile(self, tile):
        q, h, j, s = tile
        assert s in (-1, 1)
        return self.g.point(*q), int(h), int(j) % 6, int(s)

    def insert(self, tile):
        tile = self.canonical_tile(tile)
        old = len(self.tiles)
        assert self.g.admissible(tile), ('Uncontained placement', tile)
        i = super().insert(tile)
        if len(self.tiles) != old:
            # Register all six actual endpoint contributions immediately.
            # Equality is imposed only when that row has its COMPLETE oracle.
            for row, sign in self.g.rows(tile):
                self.inc[row][(1-sign)//2].append(i)
        return i

    def corner_path(self, p, start, target):
        key = p, start, target
        if key in self.corner_path_cache:
            return self.corner_path_cache[key]
        A, B = target
        terms = []
        if A == B == 0:
            term = 'true'
        else:
            for tile, (aa, bb) in self.corner.outgoing(p, *start):
                if aa > A or bb > B:
                    continue
                child = self.corner_path(p, self.corner.advance(start, aa, bb), (A-aa, B-bb))
                if child != 'false':
                    self.corner_tiles[p].add(tile)
                    self.corner_dirty.add(p)
                    terms.append(and_((f'x{self.insert(tile)}', child)))
            term = or_(terms)
        expression = term
        if term not in ('true', 'false') and len(terms) > 1:
            symbol = f'cf{self.corner_symbols}'
            self.corner_symbols += 1
            self.enqueue(f'(declare-const {symbol} Bool)')
            self.assert_(f'(= {symbol} {term})')
            term = symbol
        self.corner_path_cache[key] = term
        self.fan_path_records[key] = dict(term=term, expression=expression)
        return term

    def owner_disjunction(self, p, ray):
        key = p, ray
        if key not in self.owner_catalogues:
            indices = tuple(self.insert(t) for t in self.corner.through_candidates(p, ray))
            self.owner_catalogues[key] = indices
            self.owner_ids.update(indices)
            if len(indices) > 1:
                # Every candidate contains p strictly inside the same side
                # on the same bank, so any two overlap near p.
                ordered = tuple(sorted(indices))
                self.owner_cliques.add((p, ray, ordered))
                self.assert_(core.atmost(1, [f'x{i}' for i in ordered]))
        return or_(f'x{i}' for i in self.owner_catalogues[key])

    def install_corner_tile(self, tile, p):
        tile, p = self.canonical_tile(tile), self.g.point(*p)
        key = tile, p
        if key in self.corner_roots:
            return
        assert p in self.g.vertices(tile)
        self.corner_roots.add(key)
        self.corner_tiles.setdefault(p, set()).add(tile)
        self.corner_dirty.add(p)
        start, (aa, bb) = self.corner.sector(tile, p)
        end = self.corner.advance(start, aa, bb)
        boundary = self.corner.board_sector(p)
        alternatives = []
        if boundary is not None:
            wall_start, (A, B) = boundary
            for x in range(A-aa+1):
                for y in range(B-bb+1):
                    if self.corner.advance(wall_start, x, y) == start:
                        alternatives.append(and_((
                            self.corner_path(p, wall_start, (x,y)),
                            self.corner_path(p, end, (A-aa-x,B-bb-y)))))
        else:
            alternatives.append(self.corner_path(p, end, (6-aa,6-bb)))
            for x in range(4-aa):
                for y in range(4-bb):
                    ray = self.corner.advance(start, -x, -y)
                    if not self.corner.through_candidates(p, ray):
                        continue
                    left = self.corner_path(p, ray, (x,y))
                    right = self.corner_path(p, end, (3-aa-x,3-bb-y))
                    if left == 'false' or right == 'false':
                        continue
                    alternatives.append(and_((left, right, self.owner_disjunction(p, ray))))
        clause = f'(=> x{self.insert(tile)} {or_(alternatives)})'
        self.owned_root_clauses[key] = clause
        self.assert_(clause)

    def update_guards(self, start=0):
        """Compatibility name; no temporary row guards are ever installed."""
        assert not self.guards and not self.guard_rows
        if self.args.angular_cliques:
            for p in sorted(self.corner_dirty):
                for group in angular_groups(self.g, self.corner_tiles[p], p):
                    ids = tuple(sorted(self.index[t] for t in group))
                    self.angular_records.add((p, ids))
                    self.assert_(core.atmost(1, [f'x{i}' for i in ids]))
        self.corner_dirty.clear()

    def boundary(self):
        super().boundary()
        self.boundary_complete = True

    def query_bounds(self):
        total = core.atmost(self.g.N, [f'x{i}' for i in range(len(self.tiles))])
        reserves = []
        for sigma in (-1, 1):
            for tau in (-1, 1):
                ids = []
                for i, (_, h, j, s) in enumerate(self.tiles):
                    epsilon = s*(-1 if j % 2 else 1)
                    if epsilon == (-sigma if h % 2 else -tau):
                        ids.append(i)
                bound = (self.g.N+sigma*self.g.c+tau*(self.g.a-self.g.b))//2
                term = core.atmost(bound, [f'x{i}' for i in ids])
                reserves.append(dict(sigma=sigma, tau=tau, bound=bound, indices=ids, term=term))
        return total, reserves, and_([total]+[r['term'] for r in reserves])

    def add_overlap_conflicts(self, chosen):
        conflicts = overlap_pairs(self.g, self.tiles, chosen)
        for i, j in conflicts:
            self.overlap_records.add((i,j))
            self.assert_(f'(not (and x{i} x{j}))')
        return conflicts

    def selected_owner_rows(self, chosen):
        return sorted({row for i in chosen if i in self.owner_ids
                       for row, _ in self.g.rows(self.tiles[i]) if row not in self.exact})

    def load_root(self):
        if not self.args.root_file:
            assert self.args.root_id is None
            return
        path = Path(self.args.root_file)
        raw = path.read_bytes()
        data = json.loads(raw)
        assert data.get('schema',data.get('format')) == 'three-corner-roots-v1'
        assert tuple(data['sides']) == tuple(self.args.sides)
        roots = [r for r in data['surviving_roots'] if r['id'] == self.args.root_id]
        assert len(roots) == 1, ('Unknown or duplicate root ID', self.args.root_id)
        self.root_metadata = dict(id=self.args.root_id, source=str(path),
                                  sha256=hashlib.sha256(raw).hexdigest())
        for tile in roots[0]['tiles']:
            i = self.insert(tile)
            self.root_indices.append(i)
            self.assert_(f'x{i}')
        self.root_indices = sorted(set(self.root_indices))

    def necessary_snapshot(self):
        total, reserves, query = self.query_bounds()
        return dict(format='owned-through-necessary-model-v1', sides=list(self.args.sides), N=self.g.N,
                    unrestricted_heights=True, fixed_odd_population=None,
                    temporary_row_equations=False, boundary_complete=self.boundary_complete,
                    tiles=self.tiles, complete_rows=sorted(self.exact),
                    root=self.root_metadata, root_indices=self.root_indices,
                    root_assumptions=[f'x{i}' for i in self.root_indices],
                    corner_roots=[dict(tile=self.index[t], point=p, clause=clause)
                                  for (t,p),clause in sorted(self.owned_root_clauses.items())],
                    fan_paths=[dict(point=p,start=start,target=target,**record)
                               for (p,start,target),record in sorted(self.fan_path_records.items())],
                    owner_catalogues=[dict(point=p,ray=ray,indices=ids)
                                      for (p,ray),ids in sorted(self.owner_catalogues.items())],
                    owner_cliques=[dict(point=p,ray=ray,indices=ids)
                                   for p,ray,ids in sorted(self.owner_cliques)],
                    angular_cliques=[dict(point=p,indices=ids) for p,ids in sorted(self.angular_records)],
                    overlap_pairs=sorted(self.overlap_records),
                    permanent_assertions=sorted(self.clauses), total_count_bound=total,
                    charge_reserves=reserves, query_count_bound=query,
                    mathematical_status='NECESSARY_MODEL_ONLY')

    def checkpoint(self, iteration, status):
        # Flush pending permanent constraints directly. Calling self.flush
        # here would recurse through a resource stop.
        core.Search.flush(self)
        snapshot = self.necessary_snapshot()
        (self.out/'necessary_model.json').write_text(json.dumps(snapshot,separators=(',',':'))+'\n')
        (self.out/'complete_rows.json').write_text(json.dumps(
            dict(sides=list(self.args.sides),complete_rows=sorted(self.exact)),separators=(',',':'))+'\n')
        (self.out/'corners.json').write_text(json.dumps(
            dict(format='unrestricted-corner-roots-v1',sides=list(self.args.sides),
                 roots=sorted(self.corner_roots)),separators=(',',':'))+'\n')
        report = dict(format='owned-through-search-status-v1', sides=list(self.args.sides), N=self.g.N,
                      iteration=iteration,status=status,root=self.root_metadata,
                      scope='explicit-root-branch' if self.root_metadata else 'unrestricted-whole-board',
                      full_target_excluded=False,temporary_row_equations=False,
                      columns=len(self.tiles),complete_rows=len(self.exact),
                      owned_corner_roots=len(self.corner_roots),owner_candidates=len(self.owner_ids),
                      overlap_conflicts=len(self.overlap_records),permanent_assertions=len(self.clauses),
                      seconds=round(time.monotonic()-self.started,3),
                      max_rss_mb=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,1),
                      history=self.history)
        (self.out/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def check_resources(self):
        reason = None
        if self.args.max_columns and len(self.tiles) >= self.args.max_columns:
            reason = 'column-resource-limit'
        elif self.args.time_limit and time.monotonic()-self.started >= self.args.time_limit:
            reason = 'wall-resource-limit'
        elif self.args.max_rss_mb and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 >= self.args.max_rss_mb:
            reason = 'memory-resource-limit'
        elif self.args.stop_file and Path(self.args.stop_file).exists():
            reason = 'user-stop-file'
        if reason:
            self.checkpoint(self.iteration, reason)
            raise GracefulResourceStop(reason)

    def flush(self):
        self.update_guards()
        core.Search.flush(self)
        self.check_resources()

    def refine_fans(self, chosen, residual):
        points = {row[0] for row in residual}
        pending = []
        for i in chosen:
            tile = self.tiles[i]
            for p in self.g.vertices(tile):
                if (tile,p) not in self.corner_roots:
                    pending.append((i not in self.owner_ids,
                                    self.corner.board_sector(p) is not None,
                                    p not in points,p,i))
        used_points = set()
        done = 0
        for _,_,_,p,i in sorted(pending):
            if p in used_points:
                continue
            self.install_corner_tile(self.tiles[i],p)
            used_points.add(p)
            done += 1
            if done >= self.args.owner_fans_per_round:
                break
        return done

    def run(self):
        if self.args.seed_json:
            data = json.loads(Path(self.args.seed_json).read_text())
            if isinstance(data,dict) and 'tiles' in data:
                seeds = data['tiles']
            else:
                seeds = (tile for tile,weight in data if weight > 0)
            for tile in seeds:
                tile = self.canonical_tile(tile)
                if self.g.admissible(tile):
                    self.insert(tile)
        self.load_root()
        self.boundary()
        for row in sorted(self.g.needs):
            self.install(row)
        if self.args.rows:
            data = core.load_state(self.args.rows)
            assert tuple(data['sides']) == tuple(self.args.sides)
            for p,h,j in data['complete_rows']:
                self.install((self.g.point(*p),h,j))
        self.flush()
        self.checkpoint(0,'initialized')
        for iteration in range(self.args.rounds):
            self.iteration = iteration
            if iteration and self.args.rebuild_every and iteration % self.args.rebuild_every == 0:
                self.rebuild(iteration)
                self.flush()
            _,_,bound = self.query_bounds()
            self.enqueue('(push 1)')
            self.enqueue(f'(assert {bound})')
            self.query_active = True
            self.flush()
            timeout = self.args.timeout_ms
            if self.args.time_limit:
                remaining = max(1,int(1000*(self.args.time_limit-(time.monotonic()-self.started))))
                timeout = min(timeout,remaining)
            assert self.smt.run(f'(set-option :timeout {timeout})') == ''
            stamp = time.monotonic()
            status = self.smt.run('(check-sat)')
            assert status in ('sat','unsat','unknown'), status
            record = dict(iteration=iteration,status=status,columns=len(self.tiles),
                          complete_rows=len(self.exact),solve_seconds=round(time.monotonic()-stamp,3))
            if status == 'unsat':
                self.history.append(record)
                # Retrieve the exact current proof before altering the solver.
                if self.args.proof:
                    (self.out/'candidate_z3_proof.txt').write_text(self.smt.run('(get-proof)')+'\n')
                label = ('root-branch-unsat-needs-proof-audit' if self.root_metadata else
                         'unrestricted-unsat-needs-proof-audit')
                self.checkpoint(iteration,label)
                (self.out/'candidate_unsat.smt2').write_text((self.out/'model.smt2').read_text()+'\n(check-sat)\n')
                print('CANDIDATE',label,flush=True)
                return label
            if status == 'unknown':
                record['reason'] = self.smt.run('(get-info :reason-unknown)')
                self.history.append(record)
                self.checkpoint(iteration,'solver-inconclusive')
                print(json.dumps(record,sort_keys=True),flush=True)
                return 'solver-inconclusive'
            chosen = self.chosen()
            balance = Counter(self.g.needs)
            for i in chosen:
                for row,value in self.g.rows(self.tiles[i]):
                    balance[row] -= value
            residual = [row for row,value in balance.items() if value]
            assert not set(residual)&self.exact
            conflicts = overlap_pairs(self.g,self.tiles,chosen)
            owner_rows = self.selected_owner_rows(chosen)
            record.update(selected=len(chosen),selected_owners=len(set(chosen)&self.owner_ids),
                          residual_rows=len(residual),overlap_pairs=len(conflicts),
                          pending_selected_owner_rows=len(owner_rows))
            self.history.append(record)
            print(json.dumps(record,sort_keys=True),flush=True)
            if not residual and not conflicts:
                self.save_solution()
                self.checkpoint(iteration,'positive-needs-independent-geometric-verification')
                return 'positive-needs-independent-geometric-verification'
            self.enqueue('(pop 1)')
            self.query_active = False
            for i,j in conflicts:
                self.overlap_records.add((i,j))
                self.assert_(f'(not (and x{i} x{j}))')
            if self.args.owner_rows_per_round:
                owner_rows = owner_rows[:self.args.owner_rows_per_round]
            for row in owner_rows:
                self.install(row)
            residual.sort(key=lambda row:(-abs(balance[row]),self.corner.board_sector(row[0]) is None,row))
            for row in residual[:self.args.expand]:
                self.install(row)
            if self.args.owner_fans_per_round:
                self.refine_fans(chosen,residual)
            self.flush()
            self.checkpoint(iteration,'refined-necessary-model')
        self.checkpoint(self.args.rounds,'round-limit')
        return 'round-limit'

    def close(self):
        self.smt.close()
        self.journal.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sides',type=int,nargs=3)
    parser.add_argument('--out',required=True)
    parser.add_argument('--root-file')
    parser.add_argument('--root-id')
    parser.add_argument('--rows')
    parser.add_argument('--corner-checkpoint')
    parser.add_argument('--seed-json',help='Optional unfrozen placements, including a positive-control JSON.')
    parser.add_argument('--timeout-ms',type=int,default=30000)
    parser.add_argument('--time-limit',type=float,default=600)
    parser.add_argument('--rounds',type=int,default=50)
    parser.add_argument('--expand',type=int,default=100)
    parser.add_argument('--owner-fans-per-round',type=int,default=2)
    parser.add_argument('--owner-rows-per-round',type=int,default=0,
                        help='0 completes all selected-owner rows; a positive cap only weakens refinement.')
    parser.add_argument('--max-columns',type=int,default=200000)
    parser.add_argument('--max-rss-mb',type=float,default=0)
    parser.add_argument('--stop-file')
    parser.add_argument('--rebuild-every',type=int,default=10)
    parser.add_argument('--random-seed',type=int,default=1776)
    parser.add_argument('--proof',action='store_true')
    parser.add_argument('--no-angular-cliques',action='store_true')
    parsed = parser.parse_args()
    assert bool(parsed.root_file) == bool(parsed.root_id), 'Use --root-file and --root-id together.'
    values = vars(parsed)
    values['angular_cliques'] = not values.pop('no_angular_cliques')
    args = defaults(**values)
    assert args.rounds >= 0 and args.expand >= 0 and args.owner_fans_per_round >= 0
    search = OwnedSearch(args)
    try:
        search.run()
    except GracefulResourceStop as exc:
        print('INCONCLUSIVE:',exc,flush=True)
    finally:
        search.close()


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact geometry assertions are required.')
    main()
