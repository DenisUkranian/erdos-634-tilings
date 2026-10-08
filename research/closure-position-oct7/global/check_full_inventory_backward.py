#!/usr/bin/env python3
"""Independent backward replay of the complete N=154 directional inventory.

Derive edge currents from exact Eisenstein coordinates, enumerate signed A
vectors (the producer enumerates B), and try admissible populations directly.
This decides a formal inventory relaxation, not positioned tilings.
Python standard library only. No time/state cutoff is used.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
ZERO = (0, 0, 0)
N = 154
C = 13


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def emul(a, b):
    # rho^2 = rho - 1.
    x, y = a
    u, v = b
    return x*u-y*v, x*v+y*u+y*v


def escale(t, a):
    return tuple(t*x for x in a)


def norm(a):
    return sum(abs(x) for x in a)


def target(h):
    return {0: (154, 0, 0), 1: (0, 0, 91), -1: (0, -91, 0)}.get(h, ZERO)


def derive_edges():
    rho_powers = [(1, 0)]
    for _ in range(5):
        rho_powers.append(emul(rho_powers[-1], (0, 1)))
    z_powers = {-1: (Q(15, 13), Q(-7, 13)),
                0: (1, 0), 1: (Q(8, 13), Q(7, 13))}
    references = [[(0, 0), (8, 0), (-7, 7)],
                  [(0, 0), (7, 0), (-8, 8)]]
    edges = []
    for tri in references:
        orientation_edges = []
        for rotation in range(6):
            vertices = [emul(v, rho_powers[rotation]) for v in tri]
            this = []
            for k in range(3):
                vector = minus(vertices[(k+1) % 3], vertices[k])
                matches = [(h, j, length)
                           for h, j, length in product((-1, 0, 1), range(6), (7, 8, 13))
                           if escale(length, emul(z_powers[h], rho_powers[j])) == vector]
                assert len(matches) == 1, (vector, matches)
                this.append(matches[0])
            orientation_edges.append(this)
        edges.append(orientation_edges)
    # Check the actual target, separately from the displayed target dictionary.
    p = [(0, 0), (154, 0), (49, 56)]
    direct = Counter()
    for k in range(3):
        vector = minus(p[(k+1) % 3], p[k])
        matches = [(h, j, length)
                   for h, j, length in product((-1, 0, 1), range(6), (91, 154))
                   if escale(length, emul(z_powers[h], rho_powers[j])) == vector]
        assert len(matches) == 1
        h, j, length = matches[0]
        direct[h, j % 3] += length if j < 3 else -length
    assert dict(direct) == {(0, 0): 154, (1, 2): 91, (-1, 1): -91}
    return edges


EDGES = derive_edges()


def make_columns(tile_type, edge_height):
    columns = []
    for j in range(3):
        v = [0, 0, 0]
        for h, axis, length in EDGES[tile_type][j]:
            if h == edge_height:
                v[axis % 3] += length if axis < 3 else -length
        columns.append(tuple(v))
    return tuple(columns)


SHORT_A = make_columns(0, 0)
SHORT_B = make_columns(1, 0)
LONG_A = make_columns(0, -1)
LONG_B = make_columns(1, 1)


def apply(columns, values):
    return tuple(sum(columns[k][j] * values[k] for k in range(3)) for j in range(3))


def solve_long(columns, output):
    # The independently derived long-edge matrix is 13 times a signed permutation.
    answer = [0, 0, 0]
    used = set()
    for col, v in enumerate(columns):
        nonzero = [(row, x) for row, x in enumerate(v) if x]
        assert len(nonzero) == 1 and abs(nonzero[0][1]) == C
        row, x = nonzero[0]
        assert row not in used
        used.add(row)
        if output[row] % x:
            return None
        answer[col] = output[row] // x
    return tuple(answer)


@lru_cache(maxsize=None)
def min_population(h, size):
    # Deliberately enumerate the congruence progression rather than round a formula.
    for n in range(11 if h == 0 else 13, N+1, 13):
        if n >= size and (n-size) % 2 == 0:
            return n
    return N+1


def vectors_l1(bound):
    for x in range(-bound, bound+1):
        rem = bound-abs(x)
        for y in range(-rem, rem+1):
            tail = rem-abs(y)
            for z in range(-tail, tail+1):
                yield (x, y, z)


def backward(L, U, groups):
    """Exhaust all signed inventories under the population budget, in reverse."""
    assert L <= 0 <= U
    top_b = solve_long(LONG_B, target(U+1))
    assert top_b is not None
    states = {(ZERO, top_b): 0}  # (A at h+1, B at h) -> used population above h
    layers = []
    for h in range(U, L-1, -1):
        remaining_base = sum(11 if k == 0 else 13 for k in range(L, h))
        new = {}
        for (a_next, b), used in states.items():
            from_known = plus(apply(SHORT_B, b), apply(LONG_A, a_next))
            required = tuple(x % C for x in minus(target(h), from_known))
            available = N-used-remaining_base
            b_norm = norm(b)
            for a, a_norm, short in groups.get(required, ()):
                n = min_population(h, a_norm+b_norm)
                if n > available:
                    continue
                rest = minus(minus(target(h), from_known), short)
                b_previous = solve_long(LONG_B, rest)
                assert b_previous is not None
                if h == L:
                    if b_previous != ZERO or apply(LONG_A, a) != target(L-1):
                        continue
                key = (a, b_previous)
                total = used+n
                if total < new.get(key, N+1):
                    new[key] = total
        states = new
        layers.append({'height': h, 'states': len(states)})
        if not states:
            return {'support': [L, U], 'status': 'EXACT_UNSAT', 'layers': layers}
    return {'support': [L, U], 'status': 'FORMAL_FEASIBLE',
            'minimum_population': min(states.values()), 'layers': layers}


def replay_witness(record):
    L, U = record['support']
    blocks = record['witness']
    assert [b['h'] for b in blocks] == list(range(L, U+1))
    currents = Counter()
    population = 0
    for block in blocks:
        h, n = block['h'], block['n']
        assert isinstance(n, int) and n > 0 and n % C == (11 if h == 0 else 0)
        counts = [[0]*6, [0]*6]
        for t, key in enumerate(('A', 'B')):
            assert len(block[key]) == 3
            for j, value in enumerate(block[key]):
                assert isinstance(value, int)
                counts[t][j if value >= 0 else j+3] = abs(value)
        excess = n-sum(map(sum, counts))
        assert excess >= 0 and excess % 2 == 0
        counts[0][0] += excess//2
        counts[0][3] += excess//2
        for t in range(2):
            for rotation, count in enumerate(counts[t]):
                for delta, axis, length in EDGES[t][rotation]:
                    currents[h+delta, axis % 3] += count*length*(1 if axis < 3 else -1)
        population += n
    nonzero = {key: value for key, value in currents.items() if value}
    assert population == N
    assert nonzero == {(0, 0): 154, (1, 2): 91, (-1, 1): -91}
    return {'support': [L, U], 'population': population, 'status': 'PASS'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE/'full_inventory_backward_verified.json')
    args = parser.parse_args()
    started = time.monotonic()
    records = []
    for K in (12, 11, 10, 9):
        # Reserving all other occupied heights leaves at most this many tiles
        # at any one height; the height-zero bound is two units smaller.
        bound = N-(11+13*(K-1))+13
        groups = defaultdict(list)
        for a in vectors_l1(bound):
            short = apply(SHORT_A, a)
            groups[tuple(v % C for v in short)].append((a, norm(a), short))
        for L in range(1-K, 1):
            result = backward(L, L+K-1, groups)
            assert result['status'] == 'EXACT_UNSAT', result
            records.append(result)
        print(json.dumps({'height_count': K, 'checked_supports': K, 'status': 'PASS'}), flush=True)
    source = HERE.parent/'dual'/'directional_supports_verified.json'
    raw = source.read_bytes()
    producer = json.loads(raw)
    positives = [r for r in producer['records'] if r['support'][1]-r['support'][0]+1 == 8]
    assert {tuple(r['support']) for r in positives} == {(L, L+7) for L in range(-7, 1)}
    controls = [replay_witness(r) for r in positives]
    report = {'status': 'PASS', 'method': 'Exact geometry-derived reverse-height dynamic program',
              'scope': 'Formal signed-direction inventories only; positions are not tested',
              'full_Erdos634_solved': False, 'case154_solved': False,
              'resource_cutoffs': False, 'excluded_supports': len(records),
              'positive_formal_controls': len(controls),
              'producer_report_sha256': hashlib.sha256(raw).hexdigest(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'seconds': round(time.monotonic()-started, 6),
              'derived_edge_table': EDGES, 'negative_records': records, 'positive_records': controls}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'excluded_supports', 'positive_formal_controls', 'seconds')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: exact assertions must execute.')
    main()
