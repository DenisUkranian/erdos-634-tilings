#!/usr/bin/env python3
"""Whole, globally owned through tiles for unrestricted vertex half-fans.

No short-height, phase, denominator, odd-population, or coordinate cutoff is
used. The inherited Geometry.admissible tests containment and necessary
arithmetic on the actual outer boundary only.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from legacy import CornerOracle, and_, or_


@dataclass(frozen=True)
class OwnedAlternative:
    graphs: tuple
    owner_ray: tuple | None = None


class OwnedCornerOracle(CornerOracle):
    @lru_cache(maxsize=100000)
    def reference_shapes(self, p, ray):
        """Six right-bank shapes with an endpoint at p and side along ray.

        These reference placements need not themselves be contained: moving
        their side endpoint backwards can produce a contained through tile.
        """
        h, j = ray
        u = self.g.unit(h, j)
        result = []
        for off, H, J, s, _ in self.g.inverse(h, j % 3):
            tile = self.g.add(p, off), H, J, s
            vertices = self.g.vertices(tile)
            assert p in vertices
            for length in (self.g.a, self.g.b, self.g.c):
                endpoint = self.g.add(p, self.g.scale(length, u))
                if endpoint not in vertices:
                    continue
                third, = [v for v in vertices if v not in (p, endpoint)]
                v = self.g.sub(third, p)
                if u[0]*v[1] - u[1]*v[0] < 0:
                    result.append((tile, length))
        assert len(result) == 6
        assert sorted(length for _, length in result) == sorted(
            (self.g.a, self.g.a, self.g.b, self.g.b, self.g.c, self.g.c))
        return tuple(result)

    @lru_cache(maxsize=100000)
    def through_candidates(self, p, ray):
        """Every admissible actual through tile on the half-fan's right bank.

        A side of the complementary half-fan ends at p on the same maximal
        straight run. The integer-offset lemma therefore forces the shift
        t to belong to {1,...,length-1}. This is a full local catalogue.
        """
        u = self.g.unit(*ray)
        result = set()
        for reference, length in self.reference_shapes(p, ray):
            q, h, j, s = reference
            for offset in range(1, length):
                tile = self.g.sub(q, self.g.scale(offset, u)), h, j, s
                if self.g.admissible(tile):
                    result.add(tile)
        assert len(result) <= 2*(self.g.a+self.g.b+self.g.c-3)
        return tuple(sorted(result))

    @lru_cache(maxsize=100000)
    def owned_alternatives(self, tile, p):
        """Full/boundary fans, or half-fans with a complete owner catalogue."""
        start, (aa, bb) = self.sector(tile, p)
        end = self.advance(start, aa, bb)
        boundary = self.board_sector(p)
        result = []
        if boundary is not None:
            wall_start, (A, B) = boundary
            for x in range(A-aa+1):
                for y in range(B-bb+1):
                    if self.advance(wall_start, x, y) != start:
                        continue
                    left = self.graph(p, wall_start, (x, y))
                    right = self.graph(p, end, (A-aa-x, B-bb-y))
                    if left and right:
                        result.append(OwnedAlternative((left, right)))
            return tuple(result)
        full = self.graph(p, end, (6-aa, 6-bb))
        if full:
            result.append(OwnedAlternative((full,)))
        for x in range(4-aa):
            for y in range(4-bb):
                half_start = self.advance(start, -x, -y)
                if not self.through_candidates(p, half_start):
                    continue
                left = self.graph(p, half_start, (x, y))
                right = self.graph(p, end, (3-aa-x, 3-bb-y))
                if left and right:
                    result.append(OwnedAlternative((left, right), half_start))
        return tuple(result)

    def owned_candidates(self, tile, p):
        result = set()
        for option in self.owned_alternatives(tile, p):
            for graph in option.graphs:
                result.update(t for _, arcs in graph for t, _ in arcs)
            if option.owner_ray is not None:
                result.update(self.through_candidates(p, option.owner_ray))
        return result

    def owned_satisfied(self, tile, p, selected):
        """Evaluate the complete implication on an actual finite selection."""
        if tile not in selected:
            return True
        for option in self.owned_alternatives(tile, p):
            if not all(self.graph_satisfied(graph, selected) for graph in option.graphs):
                continue
            if option.owner_ray is None or any(
                    q in selected for q in self.through_candidates(p, option.owner_ray)):
                return True
        return False

    def owned_constraint(self, tile, p, insert):
        """A Boolean implication using one global index for each whole tile."""
        root = f'x{insert(tile)}'
        alternatives = []
        for option in self.owned_alternatives(tile, p):
            terms = [self.graph_smt(graph, insert) for graph in option.graphs]
            if option.owner_ray is not None:
                terms.append(or_(f'x{insert(q)}'
                                 for q in self.through_candidates(p, option.owner_ray)))
            alternatives.append(and_(terms))
        return f'(=> {root} {or_(alternatives)})'

