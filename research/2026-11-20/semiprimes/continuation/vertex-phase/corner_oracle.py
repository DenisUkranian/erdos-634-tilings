#!/usr/bin/env python3
"""Exact, unrestricted vertex-fan implications for congruent 120-degree tiles.

Pass the Geometry instance used by global_core_sat.py.  Nothing in this module
imposes a height range or a translation phase: all neighbors of a selected
corner are enumerated from its angle budget.  The finite circuit includes
full vertex stars and half-stars alongside an unrepresented through-edge.

The central API is CornerOracle.constraint(tile, vertex, insert).  ``insert``
maps a complete tile key to its Boolean index, adding it to the parent model
if needed.  The returned SMT-LIB Boolean term is permanently necessary for
every tiling.  Call the parent's update_guards for all newly inserted columns.
"""
from __future__ import annotations

from functools import lru_cache
from functools import cmp_to_key
from math import gcd
from fractions import Fraction

ANGLE = {"alpha": (1, 0), "beta": (0, 1), "gamma": (2, 2)}


def and_(terms):
    terms = list(dict.fromkeys(t for t in terms if t != "true"))
    if "false" in terms:
        return "false"
    if not terms:
        return "true"
    if len(terms) == 1:
        return terms[0]
    return "(and " + " ".join(terms) + ")"


def or_(terms):
    terms = list(dict.fromkeys(t for t in terms if t != "false"))
    if "true" in terms:
        return "true"
    if not terms:
        return "false"
    if len(terms) == 1:
        return terms[0]
    return "(or " + " ".join(terms) + ")"


def angular_groups(geometry, tiles, p):
    """Maximal elementary angular-cell groups at one common tile vertex.

    Each returned group consists of placements with overlapping open sectors
    at p; at most one may be selected.  All arithmetic is exact.  The groups
    constrain a finite subset and never require its completeness.
    """
    def primitive(v):
        x, y, _ = v
        d = gcd(abs(x), abs(y))
        assert d
        return x // d, y // d

    def compare(u, v):
        hu = u[1] > 0 or (u[1] == 0 and u[0] > 0)
        hv = v[1] > 0 or (v[1] == 0 and v[0] > 0)
        if hu != hv:
            return -1 if hu else 1
        cross = u[0] * v[1] - u[1] * v[0]
        return -1 if cross > 0 else (1 if cross < 0 else 0)

    sectors, rays = [], set()
    for tile in tiles:
        vertices = geometry.vertices(tile)
        k = vertices.index(p)
        lo = primitive(geometry.sub(vertices[(k + 1) % 3], p))
        hi = primitive(geometry.sub(vertices[(k + 2) % 3], p))
        sectors.append((tile, lo, hi))
        rays.update((lo, hi))
    ordered = sorted(rays, key=cmp_to_key(compare))
    indices = {ray: k for k, ray in enumerate(ordered)}
    groups = [set() for _ in ordered]
    for tile, lo, hi in sectors:
        k, end = indices[lo], indices[hi]
        while k != end:
            groups[k].add(tile)
            k = (k + 1) % len(ordered)
    unique = {frozenset(group) for group in groups if len(group) >= 2}
    # Nonmaximal angular groups follow from a containing group.
    return tuple(group for group in unique if not any(group < other for other in unique))


class CornerOracle:
    def __init__(self, geometry):
        self.g = geometry
        self.serial = 0

    @staticmethod
    def advance(ray, aa, bb):
        # alpha = pi/3-beta: rho^j z^h -> rho^(j+aa) z^(h-aa+bb).
        h, j = ray
        return h - aa + bb, (j + aa) % 6

    @lru_cache(maxsize=200000)
    def sector(self, tile, p):
        vertices = self.g.vertices(tile)
        k = vertices.index(p)
        first = self.g.sub(vertices[(k + 1) % 3], p)
        second = self.g.sub(vertices[(k + 2) % 3], p)
        q, h, j, s = tile
        lengths = (self.g.a, self.g.b, self.g.c)
        first_data = None
        second_length = None
        for hh in (h - 1, h, h + 1):
            for jj in range(6):
                u = self.g.unit(hh, jj)
                for length in lengths:
                    v = self.g.scale(length, u)
                    if first == v:
                        assert first_data is None
                        first_data = (hh, jj), length
                    if second == v:
                        assert second_length is None
                        second_length = length
        assert first_data is not None and second_length is not None
        ray, first_length = first_data
        pair = frozenset((first_length, second_length))
        if pair == frozenset((self.g.b, self.g.c)):
            kind = "alpha"
        elif pair == frozenset((self.g.a, self.g.c)):
            kind = "beta"
        else:
            assert pair == frozenset((self.g.a, self.g.b))
            kind = "gamma"
        aa, bb = ANGLE[kind]
        assert second == self.g.scale(second_length, self.g.unit(*self.advance(ray, aa, bb)))
        return ray, (aa, bb)

    @lru_cache(maxsize=200000)
    def outgoing(self, p, h, j):
        result = []
        for tile, _ in self.g.incident((p, h, j % 3)):
            ray, angle = self.sector(tile, p)
            if ray == (h, j):
                result.append((tile, angle))
        assert len(result) <= 6
        assert len({tile for tile, _ in result}) == len(result)
        return tuple(result)

    @lru_cache(maxsize=100000)
    def graph(self, p, start, target):
        """Return the viable DAG of all corner chains with the stated angle.

        Each edge represents a whole physical tile.  Angular order and strict
        positive increments make every path a set of distinct placements with
        pairwise disjoint sectors in a sufficiently small neighborhood of p.
        Removing dead states here is exact for the local graph alone.
        """
        A, B = target
        viable = {(A, B): ()}
        for total in range(A + B - 1, -1, -1):
            for aa in range(A + 1):
                bb = total - aa
                if not 0 <= bb <= B:
                    continue
                arcs = []
                h, j = self.advance(start, aa, bb)
                for tile, (da, db) in self.outgoing(p, h, j):
                    nxt = aa + da, bb + db
                    if nxt in viable:
                        arcs.append((tile, nxt))
                if arcs:
                    viable[aa, bb] = tuple(arcs)
        if (0, 0) not in viable:
            return ()
        # Only keep nodes reachable from the actual start as well.
        used, todo = set(), [(0, 0)]
        while todo:
            state = todo.pop()
            if state in used:
                continue
            used.add(state)
            todo.extend(nxt for _, nxt in viable[state])
        return tuple((state, viable[state]) for state in sorted(used, key=lambda k: (-sum(k), k)))

    def alternatives(self, tile, p):
        """A full fan, or every half-fan in which this tile occurs."""
        start, (aa, bb) = self.sector(tile, p)
        end = self.advance(start, aa, bb)
        result = []
        boundary = self.board_sector(p)
        if boundary is not None:
            wall_start, (A, B) = boundary
            for x in range(A - aa + 1):
                for y in range(B - bb + 1):
                    if self.advance(wall_start, x, y) != start:
                        continue
                    left = self.graph(p, wall_start, (x, y))
                    right = self.graph(p, end, (A - aa - x, B - bb - y))
                    if left and right:
                        result.append((left, right))
            return tuple(result)
        full = self.graph(p, end, (6 - aa, 6 - bb))
        if full:
            result.append((full,))
        for x in range(4 - aa):
            for y in range(4 - bb):
                left_start = self.advance(start, -x, -y)
                if not self.through_possible(p, left_start):
                    continue
                left = self.graph(p, left_start, (x, y))
                right = self.graph(p, end, (3 - aa - x, 3 - bb - y))
                if left and right:
                    result.append((left, right))
        return tuple(result)

    @lru_cache(maxsize=100000)
    def through_intervals(self, p, ray):
        """All feasible sliding intervals for the complementary through-tile.

        The corner half-fan runs CCW from ray to -ray, hence occupies the
        left half-plane.  A through-tile must lie on the right, have p in the
        relative interior of its side, and be fully contained in the board.
        Each of six shapes has the exact translation parameter 0<t<side.
        No restriction on its translation denominator or phase is imposed.
        """
        h, j = ray
        u = self.g.unit(h, j)
        ud = self.g.power(u[2])
        ux, uy = Fraction(u[0], ud), Fraction(u[1], ud)
        result, count = [], 0
        for off, H, J, s, _ in self.g.inverse(h, j % 3):
            tile = self.g.add(p, off), H, J, s
            vertices = self.g.vertices(tile)
            others = [v for v in vertices if v != p]
            assert len(others) == 2
            length = None
            third = None
            for k in range(2):
                v = self.g.sub(others[k], p)
                for L in (self.g.a, self.g.b, self.g.c):
                    if v == self.g.scale(L, u):
                        length, third = L, others[1-k]
            if length is None:
                continue
            v = self.g.sub(third, p)
            if u[0]*v[1] - u[1]*v[0] >= 0:
                continue
            count += 1
            low, high = Fraction(0), Fraction(length)
            feasible = True
            for v in vertices:
                d = self.g.power(v[2])
                x, y = Fraction(v[0], d), Fraction(v[1], d)
                # Each expression f0+t*f1 is required to be nonnegative.
                constraints = ((x, -ux), (y, -uy),
                               (self.g.A*self.g.B-self.g.B*x-self.g.A*y,
                                self.g.B*ux+self.g.A*uy))
                for f0, f1 in constraints:
                    if not f1:
                        if f0 < 0:
                            feasible = False
                            break
                    elif f1 > 0:
                        low = max(low, -f0/f1)
                    else:
                        high = min(high, -f0/f1)
                if not feasible or low > high:
                    feasible = False
                    break
            if feasible and high > 0 and low < length and low <= high:
                result.append((tile, low, high, length))
        assert count == 6
        return tuple(result)

    def through_possible(self, p, ray):
        return bool(self.through_intervals(p, ray))

    def board_sector(self, p):
        """Prescribed CCW interior sector at an exterior point, else None."""
        if p == (0, 0, 0):
            return (0, 0), (1, 1)
        if p == (self.g.A, 0, 0):
            return (2, 1), (2, 0)
        if p == (0, self.g.B, 0):
            return (0, 4), (0, 2)
        x, y, e = p
        if y == 0:
            return (0, 0), (3, 3)
        if x == 0:
            return (0, 4), (3, 3)
        if self.g.B * x + self.g.A * y == self.g.A * self.g.B * self.g.power(e):
            return (2, 1), (3, 3)
        return None

    def candidates(self, tile, p):
        return {candidate for option in self.alternatives(tile, p)
                for graph in option for _, arcs in graph for candidate, _ in arcs}

    def graph_satisfied(self, graph, selected):
        if not graph:
            return False
        value = {}
        for state, arcs in graph:
            value[state] = not arcs or any(tile in selected and value[nxt] for tile, nxt in arcs)
        return value[0, 0]

    def satisfied(self, tile, p, selected):
        return any(all(self.graph_satisfied(graph, selected) for graph in option)
                   for option in self.alternatives(tile, p))

    def graph_smt(self, graph, insert):
        if not graph:
            return "false"
        prefix = f"cf{self.serial}_"
        self.serial += 1
        name, groups = {}, {}
        for state, arcs in graph:
            if not arcs:
                name[state] = "true"
                continue
            terms = [and_((f"x{insert(tile)}", name[nxt])) for tile, nxt in arcs]
            value = or_(terms)
            if value in ("true", "false"):
                name[state] = value
                continue
            var = prefix + str(state[0]) + "_" + str(state[1])
            name[state] = var
            groups.setdefault(sum(state), []).append((var, value))
        body = name[0, 0]
        # Larger angle sums depend on still larger ones, so they must be outer.
        for total in sorted(groups):
            bindings = " ".join("(" + var + " " + value + ")" for var, value in groups[total])
            body = "(let (" + bindings + ") " + body + ")"
        return body

    def constraint(self, tile, p, insert):
        root = f"x{insert(tile)}"
        term = or_(and_(self.graph_smt(graph, insert) for graph in option)
                   for option in self.alternatives(tile, p))
        return f"(=> {root} {term})"

