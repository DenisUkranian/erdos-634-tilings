#!/usr/bin/env python3
"""Complete physical rows conditioned on a proved odd-population regime.

The catalogue filters below use proved height and phase restrictions.  A
temporary-row conflict or timeout is inconclusive, even in the stated scope.
An unconditional solver conflict still needs an independent proof audit.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from functools import lru_cache
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
OLD = ROOT / 'research/2026-11-20/semiprimes/continuation/global-endpoints/integer'
sys.path.insert(0, str(OLD))
import global_core_sat as base


def weighted_atmost(bound, terms, weights):
    assert len(terms) == len(weights) and all(w > 0 for w in weights)
    if bound < 0:
        return 'false'
    if sum(weights) <= bound:
        return 'true'
    if not terms:
        return 'true'
    return f'((_ pble {bound} ' + ' '.join(map(str, weights)) + ') ' + ' '.join(terms) + ')'


def variable_cap(terms, kind):
    """The six bits encode one integer x; encode count <= x,43-x,43+x."""
    bits = [f'cell_x{i}' for i in range(6)]
    weights = [1 << i for i in range(6)]
    if kind == '43-x':
        return weighted_atmost(43, terms+bits, [1]*len(terms)+weights)
    assert kind in ('x', '43+x')
    return weighted_atmost(63+(43 if kind == '43+x' else 0),
                          terms+[f'(not {b})' for b in bits],
                          [1]*len(terms)+weights)


class ScopedGeometry(base.Geometry):
    """Standard-board coordinates; the path reflection sends h to 2-h."""

    mode = ''

    def __init__(self, *sides):
        self.mode = type(self).mode
        super().__init__(*sides)

    def in_r_plus_zr(self, q):
        x, y, e = q
        if e == 0:
            return True
        return e == 1 and (self.a*y-self.b*x) % self.c == 0

    @lru_cache(50000)
    def admissible(self, tile):
        q, h, j, s = tile
        if h not in (0, 1, 2):
            return False
        if not super().admissible(tile):
            return False
        if self.mode == '3431-111':
            if h == 0:
                return self.in_r_plus_zr(q)
            v = self.mult(self.sub(q, (self.A, 0, 0)), self.unit(-1, 0))
            return v[2] == 0 if h == 1 else self.in_r_plus_zr(v)
        if self.mode == '5063-215':
            # Every vertex belongs to (z/c) R in either coordinate frame.
            return self.scale(self.c, self.mult(q, self.unit(-1, 0)))[2] == 0
        assert self.mode == '143-control'
        return True


class ScopedSearch(base.Search):
    def __init__(self, args):
        super().__init__(args)
        even = self.g.N - args.odd_population
        # Standard-frame signed charges are (-c,-d).
        self.budgets = {
            (1, 1): (args.odd_population-self.g.c)//2,
            (1, -1): (args.odd_population+self.g.c)//2,
            (0, 1): (even-(self.g.a-self.g.b))//2,
            (0, -1): (even+(self.g.a-self.g.b))//2,
        }
        assert sum(self.budgets.values()) == self.g.N
        assert all(v >= 0 for v in self.budgets.values())

    def options(self):
        super().options()
        if not self.args.cell_reserve:
            return
        assert self.args.mode == '5063-215'
        for tree in range(2):
            for kind in ('S', 'B', 'C'):
                self.enqueue(f'(declare-const phase_{tree}_{kind} Bool)')
            for r in range(1, 43):
                self.enqueue(f'(declare-const remote_{tree}_{r} Bool)')
            remote = [f'remote_{tree}_{r}' for r in range(1, 43)]
            self.enqueue('(assert '+base.atmost(1, remote)+')')
            self.enqueue('(assert '+base.equal(1, [f'phase_{tree}_{k}' for k in ('S','B','C')])+')')
            self.enqueue(f'(assert (= phase_{tree}_S (not (or '+ ' '.join(remote)+'))))')
        for i in range(6):
            self.enqueue(f'(declare-const cell_x{i} Bool)')
        self.enqueue('(assert (or '+ ' '.join(f'cell_x{i}' for i in range(6))+'))')
        self.enqueue('(assert '+weighted_atmost(42, [f'cell_x{i}' for i in range(6)], [1<<i for i in range(6)])+')')

    def labels(self, tile):
        q, h, j, s = tile
        assert h == 1
        u, v, e = self.g.scale(self.g.c, self.g.mult(
            self.g.sub(q, (self.g.A, 0, 0)), self.g.unit(-1, 0)))
        assert e == 0
        return ((self.g.a*v-self.g.b*u) % self.g.c,
                (self.g.a*u-self.g.b*v) % self.g.c)

    def insert(self, tile):
        old = len(self.tiles)
        i = super().insert(tile)
        if self.args.cell_reserve and i == old and tile[1] == 1:
            for tree, r in enumerate(self.labels(tile)):
                if r:
                    self.assert_(f'(=> x{i} remote_{tree}_{r})')
        return i

    def cell_caps(self):
        groups = defaultdict(list)
        for i, tile in enumerate(self.tiles):
            if tile[1] == 1:
                r, t = self.labels(tile)
                sign = tile[3] * (-1 if tile[2] % 2 else 1)
                groups[bool(r), bool(t), sign].append(f'x{i}')
        for first in ('S','B','C'):
            for second in ('S','B','C'):
                condition = f'(and phase_0_{first} phase_1_{second})'
                for row in (False, True):
                    for column in (False, True):
                        if (first == 'S' and row) or (second == 'S' and column):
                            continue  # Already forbidden by remote selectors.
                        rtype = first if not row else ('C' if first == 'B' else 'B')
                        ctype = second if not column else ('C' if second == 'B' else 'B')
                        for sign in (1, -1):
                            terms = groups[row, column, sign]
                            if first == second == 'S':
                                constraint = base.atmost(86 if sign == 1 else 129, terms)
                            elif 'S' in (first, second):
                                celltype = ctype if first == 'S' else rtype
                                bound = 86 if celltype == 'C' and sign == -1 else 43
                                constraint = base.atmost(bound, terms)
                            else:
                                kind = ('43-x' if rtype != ctype else
                                        '43+x' if rtype == 'C' and sign == -1 else 'x')
                                constraint = variable_cap(terms, kind)
                            if constraint != 'true':
                                self.enqueue(f'(assert (=> {condition} {constraint}))')

    def flush(self):
        if any(command == '(push 1)' for command in self.stack):
            groups = defaultdict(list)
            for i, (_, h, j, s) in enumerate(self.tiles):
                groups[h % 2, s * (-1 if j % 2 else 1)].append(f'x{i}')
            for key, budget in sorted(self.budgets.items()):
                self.enqueue('(assert ' + base.atmost(budget, groups[key]) + ')')
            if self.args.cell_reserve:
                self.cell_caps()
        super().flush()

    def checkpoint(self, iteration, status):
        if status == 'global-unsat-needs-proof-audit':
            status = 'conditional-unsat-needs-proof-audit'
        super().checkpoint(iteration, status)
        path = self.out / 'status.json'
        report = json.loads(path.read_text())
        report.update(mode=self.args.mode, odd_population=self.args.odd_population,
                      scope='Conditional on the stated exact odd population; no full target decision.',
                      sign_population_caps={str(k): v for k, v in self.budgets.items()},
                      full_target_excluded=False)
        report['joint_cell_reserve'] = self.args.cell_reserve
        path.write_text(json.dumps(report, indent=2)+'\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', choices=('3431-111', '5063-215', '143-control'), required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--rows')
    p.add_argument('--point-checkpoint')
    p.add_argument('--seed-json')
    p.add_argument('--timeout-ms', type=int, default=45000)
    p.add_argument('--rounds', type=int, default=100)
    p.add_argument('--expand', type=int, default=100)
    p.add_argument('--max-columns', type=int, default=300000)
    p.add_argument('--random-seed', type=int, default=1776)
    p.add_argument('--core-policy', choices=('random', 'defect'), default='defect')
    p.add_argument('--rebuild-every', type=int, default=10)
    p.add_argument('--minimize-core', action='store_true')
    p.add_argument('--proof', action='store_true')
    p.add_argument('--cell-reserve', action='store_true', help='Use the complete 5063/215 phase and sign classification as upper caps on partial selections.')
    args = p.parse_args()
    args.sides, args.odd_population = {
        '3431-111': ((33, 7, 37), 111),
        '5063-215': ((35, 13, 43), 215),
        '143-control': ((5, 3, 7), 105),
    }[args.mode]
    ScopedGeometry.mode = args.mode
    base.Geometry = ScopedGeometry
    print('CONDITIONAL PHYSICAL SEARCH', args.mode, flush=True)
    ScopedSearch(args).run()


if __name__ == '__main__':
    main()
