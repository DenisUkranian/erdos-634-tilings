#!/usr/bin/env python3
"""Exact necessary p-adic phase-tree budgets for a partial placement list.

This is a projection constraint, never a sufficiency test.  The mathematical
input is PHASE_BRANCHES.md in the Erdős 634 project: each ordinary nonempty
node contains >=2c tiles, and at most one exterior-free empty node has an
occupied descendant.  The two prime budgets are applied separately.
"""
from functools import lru_cache
from math import gcd


class PhaseBudget:
    def __init__(self, geometry, sign):
        assert sign in (-1, 1)
        self.g, self.sign = geometry, sign
        self.c = geometry.c
        assert geometry.a % 2 == geometry.b % 2 == 1, 'The population theorem used here is scoped to odd primitive F2 tiles.'
        assert gcd(geometry.a, geometry.b) == 1
        # This version intentionally supports only a prime hypotenuse.  No
        # assertion about composite prime ideals is hidden in the code.
        assert self.c >= 3 and all(self.c % d for d in range(2, int(self.c**0.5)+1))
        roots = [r for r in range(self.c) if (r*r-r+1) % self.c == 0]
        assert len(roots) == 2
        positive = next(r for r in roots if (geometry.a+geometry.b*r) % self.c == 0)
        self.roots = {1: positive if sign == 1 else next(r for r in roots if r != positive)}
        self.j = geometry.N % self.c
        assert self.j
        self.limit = (geometry.N - self.j)//(2*self.c) + 1
        self.outer = [(p, sign*h) for p, _, h, _ in geometry.walls()]

    def root(self, exponent):
        assert exponent >= 1
        while len(self.roots) < exponent:
            n = len(self.roots)
            r, modulus = self.roots[n], self.c**n
            assert (r*r-r+1) % modulus == 0
            digit = (-(r*r-r+1)//modulus * pow(2*r-1, -1, self.c)) % self.c
            self.roots[n+1] = r + modulus*digit
            assert (self.roots[n+1]**2-self.roots[n+1]+1) % (modulus*self.c) == 0
        return self.roots[exponent]

    @lru_cache(maxsize=200000)
    def node(self, point, level):
        x, y, e = point
        precision = e + level
        if precision <= 0:
            return level, 0, 0
        value = (x + y*self.root(precision)) % (self.c**precision)
        while e and value % self.c == 0:
            value //= self.c
            e -= 1
        return level, value, e

    def exterior_free(self, node):
        level = node[0]
        return all(level > h or self.node(p, level) != node for p, h in self.outer)

    @lru_cache(maxsize=200000)
    def required(self, tile):
        p, h, _, _ = tile
        height = self.sign*h
        # At every lower level than this, the ball contains all integral
        # exterior vertices and at least one exterior edge node.
        start = min(1-p[2], 1+min(hh for _, hh in self.outer))
        result = []
        for level in range(start, height+1):
            node = self.node(p, level)
            if self.exterior_free(node):
                result.append(node)
        return tuple(result)

    def check_selected(self, tiles):
        required = {node for tile in tiles for node in self.required(tile)}
        return len(required), self.limit


def self_check(geometry, tile_list):
    """Check exact node arithmetic and the necessary bound on a known tiling."""
    records = []
    for sign in (1, -1):
        budget = PhaseBudget(geometry, sign)
        for tile in tile_list:
            p, h, _, _ = tile
            at = budget.node(p, sign*h)
            assert all(budget.node(v, sign*h) == at for v in geometry.vertices(tile))
            # Nodes are constant under every short-height lattice generator.
            for j in range(6):
                translated = geometry.add(p, geometry.unit(h, j))
                assert budget.node(translated, sign*h) == at
            for node in budget.required(tile):
                assert budget.exterior_free(node)
        count, limit = budget.check_selected(tile_list)
        assert count <= limit, (sign, count, limit)
        records.append({'sign':sign, 'required_nodes':count, 'limit':limit})
    return records
