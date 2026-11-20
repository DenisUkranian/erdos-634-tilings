#!/usr/bin/env python3
"""Whole-board integer endpoint-current search, with complete-row expansion.

No seed tile is frozen, and no height, denominator, phase or radius bound is
used. An UNSAT answer with an empty temporary-row core is a global necessary
condition obstruction. Other UNSAT answers only request further row expansion.
See README.md for the quantifier argument and the limitations of solver proofs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from ctypes import CDLL, c_char_p, c_void_p
from functools import lru_cache
import json
import gzip
from pathlib import Path
import pickle
import random
import re
import resource
import sys
import time


class SMT:
    def __init__(self):
        self.lib = CDLL('libz3.so.4')
        z = self.lib
        z.Z3_mk_config.restype = c_void_p
        z.Z3_mk_context.argtypes = [c_void_p]
        z.Z3_mk_context.restype = c_void_p
        z.Z3_eval_smtlib2_string.argtypes = [c_void_p, c_char_p]
        z.Z3_eval_smtlib2_string.restype = c_char_p
        z.Z3_del_context.argtypes = [c_void_p]
        self.ctx = z.Z3_mk_context(z.Z3_mk_config())

    def run(self, source):
        return self.lib.Z3_eval_smtlib2_string(self.ctx, source.encode()).decode().strip()

    def close(self):
        if self.ctx:
            self.lib.Z3_del_context(self.ctx)
            self.ctx = None


def atmost(bound, terms):
    if len(terms) <= bound:
        return 'true'
    if bound < 0:
        return 'false'
    if bound == 0:
        return '(not (or ' + ' '.join(terms) + '))'
    return f'((_ at-most {bound}) ' + ' '.join(terms) + ')'


def equal(bound, terms):
    if not terms:
        return 'true' if bound == 0 else 'false'
    if bound < 0 or bound > len(terms):
        return 'false'
    if bound == 0:
        return atmost(0, terms)
    if bound == len(terms):
        return '(and ' + ' '.join(terms) + ')'
    return f'((_ pbeq {bound}' + ' 1' * len(terms) + ') ' + ' '.join(terms) + ')'


def load_state(path):
    """Portable JSON is preferred; pickle is only for trusted local checkpoints."""
    path = Path(path)
    if path.name.endswith('.json.gz'):
        return json.loads(gzip.decompress(path.read_bytes()))
    if path.suffix == '.json':
        return json.loads(path.read_text())
    with path.open('rb') as f:
        return pickle.load(f)


class Geometry:
    U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))

    def __init__(self, a, b, c):
        assert a > b > 0 and c * c == a * a + a * b + b * b
        self.a, self.b, self.c = a, b, c
        self.N = (a + 2 * b) * (2 * a + b)
        self.A, self.B = b * (2 * a + b), a * (a + 2 * b)
        self.coin = bytearray(max(self.A, self.B, c * c) + 1)
        self.coin[0] = 1
        for i in range(1, len(self.coin)):
            self.coin[i] = any(i >= n and self.coin[i - n] for n in (a, b, c))
        self.needs = Counter()
        for p, q, h, j in self.walls():
            self.needs[p, h, j] -= 1
            self.needs[q, h, j] += 1

    @lru_cache(None)
    def power(self, exponent):
        return self.c ** exponent

    def point(self, x, y, e):
        while e and x % self.c == 0 and y % self.c == 0:
            x //= self.c
            y //= self.c
            e -= 1
        return int(x), int(y), e

    def add(self, p, q):
        x, y, e = p
        u, v, f = q
        d = max(e, f)
        return self.point(x * self.power(d - e) + u * self.power(d - f),
                          y * self.power(d - e) + v * self.power(d - f), d)

    def scale(self, k, p):
        return self.point(k * p[0], k * p[1], p[2])

    def sub(self, p, q):
        return self.add(p, self.scale(-1, q))

    def mult(self, p, q):
        x, y, e = p
        u, v, f = q
        return self.point(x * u - y * v, x * v + y * u + y * v, e + f)

    @lru_cache(None)
    def unit(self, h, j):
        if j % 6:
            return self.mult(self.unit(h, 0), (*self.U[j % 6], 0))
        if h == 0:
            return 1, 0, 0
        v = (self.a, self.b, 1) if h > 0 else (self.a + self.b, -self.b, 1)
        return self.mult(v, self.unit(h - (1 if h > 0 else -1), 0))

    @lru_cache(50000)
    def legal(self, p):
        x, y, e = p
        d = self.power(e)
        A, B = self.A, self.B
        if x < 0 or y < 0 or B * x + A * y > A * B * d:
            return False
        if y == 0 and (x % d or not (self.coin[x // d] and self.coin[A - x // d])):
            return False
        if x == 0 and (y % d or not (self.coin[y // d] and self.coin[B - y // d])):
            return False
        if B * x + A * y == A * B * d:
            q, r = divmod(x * self.c * self.c, A * d)
            if r or not (self.coin[q] and self.coin[self.c * self.c - q]):
                return False
        return True

    @lru_cache(None)
    def template(self, h, j, s):
        u = self.scale(-self.a, self.unit(h, j))
        w = self.scale(self.b, self.unit(h, (j + s) % 6))
        o = (0, 0, 0)
        return ((u, h, j % 3, -s), (o, h, j % 3, s),
                (o, h, (j + s) % 3, -s), (w, h, (j + s) % 3, s),
                (w, h + s, j % 3, -s), (u, h + s, j % 3, s))

    @lru_cache(None)
    def inverse(self, h, j):
        result = []
        for H in (h - 1, h, h + 1):
            for J in range(6):
                for s in (1, -1):
                    for p, hh, jj, coefficient in self.template(H, J, s):
                        if (hh, jj) == (h, j):
                            result.append((self.scale(-1, p), H, J, s, coefficient))
        assert len(result) == 24 and len({v[:4] for v in result}) == 24
        return result

    def vertices(self, tile):
        q, h, j, s = tile
        t = self.template(h, j, s)
        result = (self.add(q, t[0][0]), q, self.add(q, t[3][0]))
        return result if s == 1 else result[::-1]

    def rows(self, tile):
        q, h, j, s = tile
        return [((self.add(q, off), H, J), w) for off, H, J, w in self.template(h, j, s)]

    @lru_cache(50000)
    def admissible(self, tile):
        return all(self.legal(p) for p in self.vertices(tile))

    def incident(self, row):
        p, h, j = row
        for off, H, J, s, w in self.inverse(h, j):
            tile = self.add(p, off), H, J, s
            if self.admissible(tile):
                yield tile, w

    def walls(self):
        O, X, Y = (0, 0, 0), (self.A, 0, 0), (0, self.B, 0)
        return ((O, X, 0, 0), (X, Y, 2, 1), (Y, O, 0, 1))

    def wall_points(self, w):
        L = (self.A, self.c * self.c, self.B)[w]
        for k in range(L + 1):
            if not (self.coin[k] and self.coin[L - k]):
                continue
            if w == 0:
                p = (k, 0, 0)
            elif w == 1:
                p = self.point(self.A * (L - k), self.B * k, 2)
            else:
                p = (0, self.B - k, 0)
            yield k, p

    def wedge(self, tile, row):
        """The two half-ray / half-plane signs at a shared side endpoint."""
        p, h, j = row
        items = self.rows(tile)
        other = None
        for k in (0, 2, 4):
            (r0, _), (r1, _) = items[k:k + 2]
            if r0[1:] == (h, j) and p in (r0[0], r1[0]):
                other = r1[0] if p == r0[0] else r0[0]
                break
        assert other is not None
        third = next(v for v in self.vertices(tile) if v not in (p, other))
        axis = self.unit(h, j)
        side, interior = self.sub(other, p), self.sub(third, p)
        along = side[0] * axis[0] if axis[0] else side[1] * axis[1]
        across = axis[0] * interior[1] - axis[1] * interior[0]
        assert along and across
        return along > 0, across > 0

    def seed(self, path=None):
        if path:
            data = json.loads(Path(path).read_text())
            for key, weight in data:
                if weight > 0:
                    q, h, j, s = key
                    yield tuple(q), h, j, s
            return
        seed_generator = None
        for parent in Path(__file__).resolve().parents:
            for relative in ('continuation/packing/packing_replay.py',
                             'repo/research/2026-11-20/semiprimes/continuation/packing/packing_replay.py'):
                candidate = parent / relative
                if candidate.is_file():
                    seed_generator = candidate
                    break
            if seed_generator is not None:
                break
        if seed_generator is None:
            raise FileNotFoundError('Supply --seed-json, or keep the repository continuation/packing seed generator.')
        sys.path.insert(0, str(seed_generator.parent))
        import packing_replay
        _, positive, _, _ = packing_replay.inventory(self.a, self.b, self.c)
        # This finite lookup only decodes an existing finite seed. It does not
        # restrict subsequent placement generation in any way.
        lookup = {self.scale(self.a, self.unit(h, j)): (h, j)
                  for h in range(-4, 5) for j in range(6)}
        for triangle in positive:
            T = tuple(self.point(*p, 1) for p in triangle)
            found = None
            for i in range(3):
                for k in (1, 2):
                    q, p, r = T[i], T[(i + k) % 3], T[(i - k) % 3]
                    au = self.sub(q, p)
                    if au not in lookup:
                        continue
                    h, j = lookup[au]
                    for s in (1, -1):
                        if self.sub(r, q) == self.scale(self.b, self.unit(h, (j + s) % 6)):
                            found = q, h, j, s
            assert found is not None, T
            yield found


class Search:
    def __init__(self, args):
        self.args = args
        self.g = Geometry(*args.sides)
        self.out = Path(args.out)
        self.out.mkdir(parents=True, exist_ok=True)
        self.smt = SMT()
        self.stack = []
        self.tiles, self.index = [], {}
        self.exact = set()
        # Each placement is inserted once, hence no incidence list has repeats.
        # Lists avoid two heavyweight Python sets for every endpoint row.
        self.inc = defaultdict(lambda: [[], []])
        self.guards, self.guard_rows = {}, {}
        self.guard_clauses, self.clause_guard = {}, {}
        self.serial = 0
        self.clauses = set()
        self.rng = random.Random(args.random_seed)
        self.core_hits = Counter()
        self.anchors = []
        self.coverage_points = []
        if args.point_checkpoint:
            point_data = load_state(args.point_checkpoint)
            assert tuple(point_data['sides']) == tuple(args.sides)
            self.coverage_points = point_data['coverage_points']
            assert all(len(p) == 3 and all(isinstance(v, int) for v in p) and p[2] > 0
                       for p in self.coverage_points)
        self.coverage_groups = [set() for _ in self.coverage_points]
        self.journal = (self.out / 'model.smt2').open('w')
        self.options()

    def options(self):
        self.enqueue('(set-option :produce-unsat-cores true)')
        if self.args.proof:
            self.enqueue('(set-option :produce-proofs true)')
        self.enqueue(f'(set-option :timeout {self.args.timeout_ms})')
        self.enqueue('(set-option :smt.random_seed 1776)')
        if self.args.minimize_core:
            self.enqueue('(set-option :smt.core.minimize true)')
            self.enqueue('(set-option :sat.core.minimize true)')

    def rebuild(self, iteration):
        """Keep every permanent assertion, but discard stale temporary guards."""
        self.checkpoint(iteration, 'rebuilding-equivalent-context')
        self.smt.close()
        self.smt = SMT()
        self.journal.close()
        self.journal = (self.out / 'model.smt2').open('w')
        self.stack.clear()
        self.options()
        for i in range(len(self.tiles)):
            self.enqueue(f'(declare-const x{i} Bool)')
        for clause in sorted(self.clauses):
            self.enqueue('(assert ' + clause + ')')
        self.guard_clauses = {guard: self.guard_clauses[guard] for guard in self.guard_rows}
        self.clause_guard = {clause: guard for guard, clause in self.guard_clauses.items()}
        for guard, clause in self.guard_clauses.items():
            self.enqueue(f'(declare-const {guard} Bool)')
            self.enqueue(f'(assert (=> {guard} {clause}))')
        print('rebuild', iteration, 'active guards', len(self.guard_rows),
              'permanent assertions', len(self.clauses), flush=True)

    def enqueue(self, command):
        self.stack.append(command)

    def assert_(self, clause):
        if clause == 'true' or clause in self.clauses:
            return
        self.clauses.add(clause)
        self.enqueue('(assert ' + clause + ')')

    def flush(self):
        if not self.stack:
            return
        text = '\n'.join(self.stack) + '\n'
        result = self.smt.run(text)
        assert not result, result[:2000]
        self.journal.write(text)
        self.journal.flush()
        self.stack.clear()

    def insert(self, tile):
        if tile in self.index:
            return self.index[tile]
        i = len(self.tiles)
        self.tiles.append(tile)
        self.index[tile] = i
        self.enqueue(f'(declare-const x{i} Bool)')
        return i

    def equation(self, row, positive, negative):
        positive, negative = tuple(sorted(positive)), tuple(sorted(negative))
        target = self.g.needs[row]
        if not target and negative < positive:
            positive, negative = negative, positive
        return equal(len(negative) + target,
                     [f'x{i}' for i in positive] +
                     [f'(not x{i})' for i in negative])

    def unbind(self, row):
        prior = self.guards.pop(row, None)
        if prior is not None:
            self.guard_rows[prior].remove(row)
            if not self.guard_rows[prior]:
                del self.guard_rows[prior]

    def install(self, row):
        if row in self.exact:
            return
        self.exact.add(row)
        self.unbind(row)
        sides = [set(), set()]
        wedges = defaultdict(set)
        for tile, coefficient in self.g.incident(row):
            i = self.insert(tile)
            sides[(1 - coefficient) // 2].add(i)
            wedges[self.g.wedge(tile, row)].add(i)
        self.assert_(self.equation(row, *sides))
        for group in wedges.values():
            self.assert_(atmost(1, [f'x{i}' for i in sorted(group)]))

    def update_guards(self, start):
        dirty = set()
        dirty_points = set()
        for i in range(start, len(self.tiles)):
            for row, sign in self.g.rows(self.tiles[i]):
                self.inc[row][(1 - sign) // 2].append(i)
                if row not in self.exact:
                    dirty.add(row)
            if self.coverage_points:
                vertices = self.g.vertices(self.tiles[i])
                exponent = max(p[2] for p in vertices)
                denominator = self.g.power(exponent)
                vertices = tuple((x * self.g.power(exponent-e), y * self.g.power(exponent-e))
                                 for x, y, e in vertices)
                minx, maxx = min(p[0] for p in vertices), max(p[0] for p in vertices)
                miny, maxy = min(p[1] for p in vertices), max(p[1] for p in vertices)
                edges = [(vertices[k], vertices[(k+1) % 3]) for k in range(3)]
                for cut, (x, y, q) in enumerate(self.coverage_points):
                    X, Y = x * denominator, y * denominator
                    if not (minx*q < X < maxx*q and miny*q < Y < maxy*q):
                        continue
                    if all((r[0]-p[0])*(Y-p[1]*q) - (r[1]-p[1])*(X-p[0]*q) > 0
                           for p, r in edges):
                        self.coverage_groups[cut].add(i)
                        dirty_points.add(cut)
        for row in sorted(dirty):
            self.unbind(row)
            clause = self.equation(row, *self.inc[row])
            if clause == 'true':
                continue
            guard = self.clause_guard.get(clause)
            if guard is None:
                guard = f'g{self.serial}'
                self.serial += 1
                self.guard_clauses[guard] = clause
                self.clause_guard[clause] = guard
                self.enqueue(f'(declare-const {guard} Bool)')
                self.enqueue(f'(assert (=> {guard} {clause}))')
            self.guards[row] = guard
            self.guard_rows.setdefault(guard, []).append(row)
        for cut in sorted(dirty_points):
            self.assert_(atmost(1, [f'x{i}' for i in sorted(self.coverage_groups[cut])]))

    def boundary(self):
        for w, (_, _, h, j) in enumerate(self.g.walls()):
            offsets = dict(self.g.wall_points(w))
            positions = {p: k for k, p in offsets.items()}
            length = (self.g.A, self.g.c * self.g.c, self.g.B)[w]
            banks = [set() for _ in range(length)]
            for lo, p in offsets.items():
                for tile, _ in self.g.incident((p, h, j)):
                    points = self.g.vertices(tile)
                    endpoints = [positions[v] for v in points if v in positions]
                    if len(endpoints) != 2 or min(endpoints) != lo:
                        continue
                    hi = max(endpoints)
                    i = self.insert(tile)
                    for k in range(lo, hi):
                        banks[k].add(i)
            for bank in banks:
                self.assert_(equal(1, [f'x{i}' for i in sorted(bank)]))
            print('boundary', w, 'length', length, 'columns', len(self.tiles), flush=True)

    def checkpoint(self, iteration, status):
        data = dict(format='global-integer-endpoint-v1', sides=self.args.sides,
                    N=self.g.N, boundary_arithmetic=True, iteration=iteration,
                    status=status, complete_rows=sorted(self.exact),
                    tiles=self.tiles, guards=list(self.guards.items()),
                    coverage_points=self.coverage_points,
                    assertions=len(self.clauses), random_seed=self.args.random_seed)
        path = self.out / 'checkpoint.pickle'
        temp = path.with_suffix('.tmp')
        with temp.open('wb') as f:
            pickle.dump(data, f)
        temp.replace(path)
        report = {k: v for k, v in data.items() if k not in ('complete_rows', 'tiles', 'guards', 'coverage_points')}
        report.update(columns=len(self.tiles), rows=len(self.exact), partial_rows=len(self.guards))
        report['coverage_points'] = len(self.coverage_points)
        report['active_guard_count'] = len(self.guard_rows)
        report['max_rss_mb'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
        (self.out / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def chosen(self):
        result = []
        for start in range(0, len(self.tiles), 10000):
            values = self.smt.run('(get-value (' + ' '.join(
                f'x{i}' for i in range(start, min(start + 10000, len(self.tiles)))) + '))')
            assert '(error' not in values, values[:500]
            result.extend(int(i) for i in re.findall(r'\(x(\d+) true\)', values))
        return result

    def save_solution(self):
        chosen = self.chosen()
        balance = Counter(self.g.needs)
        for i in chosen:
            for row, value in self.g.rows(self.tiles[i]):
                balance[row] -= value
        assert not any(balance.values()), 'A partial-row model is not a solution.'
        assert len(chosen) == self.g.N
        assert all(self.g.admissible(self.tiles[i]) for i in chosen)
        data = dict(format='positive-endpoint-tiling-v1', sides=self.args.sides,
                    N=self.g.N, tiles=[self.tiles[i] for i in chosen])
        (self.out / 'solution.json').write_text(json.dumps(data, separators=(',', ':')) + '\n')

    def choose_core_rows(self, core):
        keys = [row for guard in core for row in self.guard_rows[guard]]
        self.rng.shuffle(keys)
        for key in keys:
            self.core_hits[key] += 1
        if self.args.core_policy == 'defect' and self.anchors:
            def priority(row):
                (x, y, exponent), _, _ = row
                x, y = x / self.g.power(exponent), y / self.g.power(exponent)
                distance = min((x-u)**2 + (x-u)*(y-v) + (y-v)**2
                               for u, v in self.anchors)
                # This only chooses which necessary rows to complete next.
                # Recurrence eventually outweighs a finite geometric distance.
                return distance / (self.g.c ** 2) - 2 * self.core_hits[row]
            keys.sort(key=priority)
        return keys[:self.args.expand]

    def run(self):
        start_time = time.time()
        seed = 0
        for tile in self.g.seed(self.args.seed_json):
            if self.g.admissible(tile):
                self.insert(tile)
                seed += 1
        seed_balance = Counter(self.g.needs)
        for tile in self.tiles:
            for row, value in self.g.rows(tile):
                seed_balance[row] -= value
        anchor_points = {row[0] for row, value in seed_balance.items() if value}
        self.anchors = [(x / self.g.power(e), y / self.g.power(e)) for x, y, e in sorted(anchor_points)]
        print('seed imbalance points', len(self.anchors), 'core policy', self.args.core_policy, flush=True)
        self.boundary()
        for row in self.g.needs:
            self.install(row)
        if self.args.rows:
            data = load_state(self.args.rows)
            assert tuple(data['sides']) == tuple(self.args.sides)
            rows = data.get('complete_rows', list(data.get('rows', {})))
            for p, h, j in rows:
                self.install((tuple(p), h, j))
        self.update_guards(0)
        print('whole board', self.g.N, 'seed', seed, 'columns', len(self.tiles),
              'complete rows', len(self.exact), 'partial rows', len(self.guards),
              'coverage points', len(self.coverage_points),
              'setup seconds', round(time.time() - start_time, 2), flush=True)
        for iteration in range(self.args.rounds):
            if iteration and self.args.rebuild_every and iteration % self.args.rebuild_every == 0:
                self.rebuild(iteration)
            self.enqueue('(push 1)')
            self.enqueue('(assert ' + atmost(self.g.N, [f'x{i}' for i in range(len(self.tiles))]) + ')')
            self.flush()
            stamp = time.time()
            assumptions = ' '.join(self.guard_rows)
            status = self.smt.run('(check-sat-assuming (' + assumptions + '))')
            print('round', iteration, 'columns', len(self.tiles), 'complete rows',
                  len(self.exact), 'partial rows', len(self.guards), 'status', status,
                  'guards', len(self.guard_rows), 'seconds', round(time.time() - stamp, 3),
                  'max RSS MB', round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1), flush=True)
            if iteration % 5 == 0 or status != 'unsat':
                self.checkpoint(iteration, status)
            if status == 'sat':
                self.save_solution()
                print('POSITIVE ENDPOINT SOLUTION; independent metric audit required', flush=True)
                return
            if status != 'unsat':
                print('INCONCLUSIVE:', self.smt.run('(get-info :reason-unknown)'), flush=True)
                return
            if len(self.tiles) >= self.args.max_columns:
                self.checkpoint(iteration, 'column-resource-limit')
                print('INCONCLUSIVE: requested column resource limit reached', flush=True)
                return
            cause = self.smt.run('(get-unsat-core)')
            assert cause.startswith('(') and cause.endswith(')') and '(error' not in cause, cause
            assert re.fullmatch(r'\(\s*(?:g\d+\s*)*\)', cause), cause
            core = re.findall(r'g\d+', cause)
            assert all(g in self.guard_rows for g in core), cause
            print('temporary core guards', len(core), 'physical rows',
                  sum(len(self.guard_rows[guard]) for guard in core), flush=True)
            if not core:
                confirmed = self.smt.run('(check-sat)')
                if confirmed != 'unsat':
                    self.checkpoint(iteration, 'empty-core-not-confirmed')
                    print('INCONCLUSIVE: empty-core result did not reproduce without assumptions:', confirmed, flush=True)
                    return
                self.checkpoint(iteration, 'global-unsat-needs-proof-audit')
                (self.out / 'global_unsat.smt2').write_text(
                    (self.out / 'model.smt2').read_text() + '\n(check-sat)\n')
                if self.args.proof:
                    (self.out / 'z3_proof.txt').write_text(self.smt.run('(get-proof)') + '\n')
                print('GLOBAL NECESSARY MODEL UNSAT; independent encoding/proof audit required', flush=True)
                return
            keys = self.choose_core_rows(core)
            self.enqueue('(pop 1)')
            old_columns = len(self.tiles)
            for row in keys:
                self.install(row)
            self.update_guards(old_columns)
        self.flush()
        self.checkpoint(self.args.rounds, 'round-limit')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sides', type=int, nargs=3)
    parser.add_argument('--out', required=True)
    parser.add_argument('--seed-json')
    parser.add_argument('--rows', help='Regenerate complete rows from JSON/JSON.gz, or a trusted local pickle checkpoint.')
    parser.add_argument('--timeout-ms', type=int, default=45000)
    parser.add_argument('--rounds', type=int, default=1000)
    parser.add_argument('--expand', type=int, default=100)
    parser.add_argument('--random-seed', type=int, default=1776)
    parser.add_argument('--proof', action='store_true')
    parser.add_argument('--minimize-core', action='store_true')
    parser.add_argument('--max-columns', type=int, default=300000)
    parser.add_argument('--core-policy', choices=('random', 'defect'), default='random')
    parser.add_argument('--point-checkpoint', help='Load exact interior at-most-one coverage points from a trusted local LP checkpoint.')
    parser.add_argument('--rebuild-every', type=int, default=10,
                        help='Rebuild an equivalent solver context periodically to drop stale guards; zero disables.')
    Search(parser.parse_args()).run()


if __name__ == '__main__':
    main()
