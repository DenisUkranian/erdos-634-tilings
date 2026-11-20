#!/usr/bin/env python3
"""Core-guided endpoint search strengthened by unrestricted corner fans.

The base search module is provided by the repository's global-endpoints
integer package.  Pass --base-dir when running this file outside that package.
This is a search procedure.  Temporary-guard UNSAT and resource stops remain
inconclusive, exactly as in the base implementation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import resource
import sys
import time
from types import SimpleNamespace

from corner_oracle import CornerOracle, and_, or_, angular_groups


class GracefulResourceStop(Exception):
    pass


class GlobalObstructionFound(Exception):
    pass


def make_search_class(base):
    class CornerSearch(base.Search):
        def __init__(self, args):
            self.corner_symbols = 0
            self.corner_path_cache = {}
            self.corner_roots = set()
            self.corner_pending = set()
            self.corner_tiles = {}
            self.corner_dirty = set()
            self.corner_calls = 0
            self.corner_rounds = 0
            self.global_probes = []
            self.last_global_probe = None
            super().__init__(args)
            self.corner = CornerOracle(self.g)

        def options(self):
            super().options()
            for k in range(self.corner_symbols):
                self.enqueue(f'(declare-const cf{k} Bool)')

        def insert(self, tile):
            old = len(self.tiles)
            i = super().insert(tile)
            if len(self.tiles) != old and self.corner_tiles:
                for p in self.g.vertices(tile):
                    if p in self.corner_tiles:
                        self.corner_tiles[p].add(tile)
                        self.corner_dirty.add(p)
            return i

        def corner_path(self, p, start, target):
            key = p, start, target
            if key in self.corner_path_cache:
                return self.corner_path_cache[key]
            A, B = target
            if A == B == 0:
                return 'true'
            terms = []
            for tile, (aa, bb) in self.corner.outgoing(p, *start):
                if aa > A or bb > B:
                    continue
                child = self.corner_path(p, self.corner.advance(start, aa, bb),
                                         (A - aa, B - bb))
                if child != 'false':
                    self.corner_tiles[p].add(tile)
                    self.corner_dirty.add(p)
                    terms.append(and_((f'x{self.insert(tile)}', child)))
            term = or_(terms)
            if term not in ('true', 'false') and len(terms) > 1:
                symbol = f'cf{self.corner_symbols}'
                self.corner_symbols += 1
                self.enqueue(f'(declare-const {symbol} Bool)')
                self.assert_(f'(= {symbol} {term})')
                term = symbol
            self.corner_path_cache[key] = term
            return term

        def install_corner_tile(self, tile, p):
            key = tile, p
            if key in self.corner_roots:
                return
            self.corner_roots.add(key)
            self.corner_tiles.setdefault(p, set()).add(tile)
            self.corner_dirty.add(p)
            start, (aa, bb) = self.corner.sector(tile, p)
            end = self.corner.advance(start, aa, bb)
            boundary = self.corner.board_sector(p)
            alternatives = []
            if boundary is not None:
                wall_start, (A, B) = boundary
                for x in range(A - aa + 1):
                    for y in range(B - bb + 1):
                        if self.corner.advance(wall_start, x, y) == start:
                            alternatives.append(and_((
                                self.corner_path(p, wall_start, (x, y)),
                                self.corner_path(p, end, (A-aa-x, B-bb-y)))))
            else:
                alternatives.append(self.corner_path(p, end, (6-aa, 6-bb)))
                for x in range(4-aa):
                    for y in range(4-bb):
                        half_start = self.corner.advance(start, -x, -y)
                        if not self.corner.through_possible(p, half_start):
                            continue
                        alternatives.append(and_((
                            self.corner_path(p, half_start, (x, y)),
                            self.corner_path(p, end, (3-aa-x, 3-bb-y)))))
            self.assert_(f'(=> x{self.insert(tile)} {or_(alternatives)})')

        def install_corner(self, row):
            p, _, _ = row
            before = len(self.tiles)
            roots_before = len(self.corner_roots)
            for tile, _ in self.g.incident(row):
                self.install_corner_tile(tile, p)
            self.corner_calls += 1
            print('corner', self.corner_calls, 'new roots', len(self.corner_roots)-roots_before,
                  'new columns', len(self.tiles)-before, 'aux', self.corner_symbols, flush=True)

        def update_guards(self, start):
            if self.args.angular_cliques:
                for p in sorted(self.corner_dirty):
                    for group in angular_groups(self.g, self.corner_tiles[p], p):
                        self.assert_(base.atmost(1, [f'x{self.index[t]}' for t in sorted(group)]))
            self.corner_dirty.clear()
            super().update_guards(start)

        def boundary(self):
            super().boundary()
            for row in sorted(self.g.needs):
                self.install_corner(row)
            if self.args.corner_checkpoint:
                data = json.loads(Path(self.args.corner_checkpoint).read_text())
                assert data['sides'] == list(self.args.sides)
                for tile, p in data['roots']:
                    tile = tuple(tile[0]), *tile[1:]
                    self.install_corner_tile(tile, tuple(p))

        def choose_core_rows(self, core):
            self.corner_rounds += 1
            self.check_resources()
            if self.args.core_policy == 'few_missing':
                candidates = {row for guard in core for row in self.guard_rows[guard]}
                scored = []
                for row in candidates:
                    self.core_hits[row] += 1
                    missing = sum(tile not in self.index for tile,_ in self.g.incident(row))
                    boundary = self.corner.board_sector(row[0]) is not None
                    scored.append((missing, not boundary, -self.core_hits[row], row))
                scored.sort()
                closed = [item[-1] for item in scored if item[0] == 0]
                growing = [item[-1] for item in scored if item[0] != 0]
                keys = closed + growing[:self.args.expand]
                print('core completion', 'zero missing',len(closed),
                      'growing selected',min(self.args.expand,len(growing)),
                      'smallest missing',scored[0][0] if scored else None,flush=True)
            else:
                keys = super().choose_core_rows(core)
            preferred = sorted(keys, key=lambda row: (self.corner.board_sector(row[0]) is None,
                                                       -self.core_hits[row], row))
            self.corner_pending = set(preferred[:self.args.corner_rows])
            return keys

        def check_resources(self):
            limit = getattr(self.args, 'max_rss_mb', 0)
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            stop_file = getattr(self.args, 'stop_file', None)
            reason = None
            if limit and rss >= limit:
                reason = 'corner-memory-resource-limit'
            elif stop_file and Path(stop_file).exists():
                reason = 'corner-user-stop-file'
            if reason:
                self.checkpoint(self.corner_rounds, reason)
                self.journal.flush()
                raise GracefulResourceStop(f'{reason}: peak RSS {rss:.1f} MB')

        def flush(self):
            self.check_resources()
            query = '(push 1)' in self.stack
            if query and getattr(self.args,'checkpoint_every_query',False):
                self.checkpoint(self.corner_rounds,'before-next-query')
            result = super().flush()
            self.check_resources()
            every = getattr(self.args,'global_probe_every',0)
            if query and every and self.corner_rounds%every == 0 and self.last_global_probe != self.corner_rounds:
                self.last_global_probe = self.corner_rounds
                self.global_probe()
            return result

        def global_probe(self):
            # All incomplete endpoint equations are guarded implications.
            # Their guards are supplied only as assumptions in the base query.
            # Here no guard assumption is passed; the current tile/population
            # query scope remains active throughout.
            timeout = getattr(self.args,'global_probe_timeout_ms',10000)
            assert self.smt.run(f'(set-option :timeout {timeout})') == ''
            stamp = time.time()
            status = self.smt.run('(check-sat)')
            assert status in ('sat','unsat','unknown'), ('Unexpected SMT response',status)
            record = dict(round=self.corner_rounds,columns=len(self.tiles),
                          complete_rows=len(self.exact),status=status,
                          seconds=round(time.time()-stamp,3),
                          temporary_assumptions=False,
                          tile_and_population_caps_active=True)
            if status == 'unknown':
                record['reason'] = self.smt.run('(get-info :reason-unknown)')
            self.global_probes.append(record)
            (self.out/'global_probes.json').write_text(json.dumps(self.global_probes,indent=2)+'\n')
            print('UNGUARDED PROBE',json.dumps(record,sort_keys=True),flush=True)
            if status == 'unsat':
                # Do not pop, assert, or run another solver query before saving
                # the existing result/proof and its exact replayable context.
                if self.args.proof:
                    (self.out/'z3_proof.txt').write_text(self.smt.run('(get-proof)')+'\n')
                self.checkpoint(self.corner_rounds,'global-probe-unsat-needs-proof-audit')
                self.journal.flush()
                (self.out/'global_unsat.smt2').write_text((self.out/'model.smt2').read_text()+'\n(check-sat)\n')
                raise GlobalObstructionFound('Unconditional finite necessary model is UNSAT; proof and encoding audit required.')
            assert self.smt.run(f'(set-option :timeout {self.args.timeout_ms})') == ''

        def install(self, row):
            super().install(row)
            if row in self.corner_pending:
                self.corner_pending.remove(row)
                self.install_corner(row)

        def checkpoint(self, iteration, status):
            super().checkpoint(iteration, status)
            data = dict(format='unrestricted-corner-roots-v1', sides=list(self.args.sides),
                        roots=sorted(self.corner_roots), symbols=self.corner_symbols,
                        calls=self.corner_calls, mathematical_status='SEARCH_ONLY')
            (self.out/'corners.json').write_text(json.dumps(data, separators=(',', ':'))+'\n')

    return CornerSearch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sides', type=int, nargs=3)
    parser.add_argument('--base-dir', required=True)
    parser.add_argument('--phase-dir', help='Optionally inherit PhaseSearch from this directory.')
    parser.add_argument('--population-budgets', action='store_true', help='Use exact per-node populations, with --phase-dir.')
    parser.add_argument('--signed-populations', action='store_true', help='Use signed per-node populations and parity completion.')
    parser.add_argument('--joint-heights', action='store_true', help='Share physical-height signed capacities between the two trees.')
    parser.add_argument('--no-phase-empty', action='store_true', help='Requires a separately proved no-empty-ancestor theorem.')
    parser.add_argument('--out', required=True)
    parser.add_argument('--seed-json')
    parser.add_argument('--rows')
    parser.add_argument('--timeout-ms', type=int, default=45000)
    parser.add_argument('--rounds', type=int, default=1000)
    parser.add_argument('--expand', type=int, default=30)
    parser.add_argument('--random-seed', type=int, default=1776)
    parser.add_argument('--proof', action='store_true')
    parser.add_argument('--minimize-core', action='store_true')
    parser.add_argument('--max-columns', type=int, default=150000)
    parser.add_argument('--core-policy', choices=('random', 'defect', 'few_missing'), default='few_missing')
    parser.add_argument('--point-checkpoint')
    parser.add_argument('--rebuild-every', type=int, default=10)
    parser.add_argument('--corner-rows', type=int, default=1)
    parser.add_argument('--corner-checkpoint')
    parser.add_argument('--angular-cliques', action='store_true')
    parser.add_argument('--max-rss-mb', type=float, default=1400)
    parser.add_argument('--stop-file')
    parser.add_argument('--checkpoint-every-query', action='store_true')
    parser.add_argument('--global-probe-every', type=int, default=0)
    parser.add_argument('--global-probe-timeout-ms', type=int, default=10000)
    args = parser.parse_args()
    assert not args.no_phase_empty or args.population_budgets or args.signed_populations, '--no-phase-empty requires a population model.'
    sys.path.insert(0, args.base_dir)
    import global_core_sat
    base = global_core_sat
    if args.phase_dir:
        sys.path.insert(0, args.phase_dir)
        if args.signed_populations:
            from phase_budget import PhaseBudget
            from signed_population_search import make_signed_population_search_class
            PopulationSearch = make_signed_population_search_class(global_core_sat, PhaseBudget)
            if args.joint_heights:
                from joint_height_search import make_joint_height_search_class
                PopulationSearch = make_joint_height_search_class(PopulationSearch)
            base = SimpleNamespace(Search=PopulationSearch, atmost=global_core_sat.atmost)
        elif args.population_budgets:
            from phase_budget import PhaseBudget
            from population_search import make_population_search_class
            PopulationSearch = make_population_search_class(global_core_sat, PhaseBudget)
            base = SimpleNamespace(Search=PopulationSearch, atmost=global_core_sat.atmost)
        else:
            from phase_search import PhaseSearch
            base = SimpleNamespace(Search=PhaseSearch, atmost=global_core_sat.atmost)
    else:
        assert not args.population_budgets, '--population-budgets requires --phase-dir'
        assert not args.signed_populations, '--signed-populations requires --phase-dir'
    assert not args.joint_heights or args.signed_populations, '--joint-heights requires --signed-populations'
    search = make_search_class(base)(args)
    try:
        search.run()
    except GracefulResourceStop as exc:
        print('INCONCLUSIVE: saved checkpoint;', exc, flush=True)
    except GlobalObstructionFound as exc:
        print('GLOBAL CANDIDATE:',exc,flush=True)


if __name__ == '__main__':
    main()
