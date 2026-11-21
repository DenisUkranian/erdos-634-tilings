#!/usr/bin/env python3
"""Complete actual opposite-bank placements along a selected whole side."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE/'owned'))
from owned_oracle import OwnedCornerOracle


@dataclass(frozen=True)
class EdgeData:
    start: tuple
    end: tuple
    ray: tuple
    length: int
    boundary: bool


@dataclass(frozen=True)
class BankCatalogue:
    tiles: tuple
    spans: tuple
    intervals: tuple


class WholeEdgeOracle:
    def __init__(self,geometry):
        self.g=geometry
        self.shapes=OwnedCornerOracle(geometry)

    def boundary_edge(self,p,q):
        def faces(v):
            x,y,e=v
            return x==0,y==0,self.g.B*x+self.g.A*y==self.g.A*self.g.B*self.g.power(e)
        return any(a and b for a,b in zip(faces(p),faces(q)))

    @lru_cache(maxsize=200000)
    def edge(self,tile,index):
        assert index in (0,1,2)
        vertices=self.g.vertices(tile)
        p,q=vertices[index],vertices[(index+1)%3]
        vector=self.g.sub(q,p)
        matches=[((h,j),length)
                 for h in (tile[1]-1,tile[1],tile[1]+1)
                 for j in range(6) for length in (self.g.a,self.g.b,self.g.c)
                 if vector==self.g.scale(length,self.g.unit(h,j))]
        assert len(matches)==1
        ray,length=matches[0]
        return EdgeData(p,q,ray,length,self.boundary_edge(p,q))

    @lru_cache(maxsize=100000)
    def catalogue(self,p,ray,length):
        """All right-bank tiles meeting an open part of [p,p+length*u].

        The six reference shapes start their selected side at p along u.
        A side of length ell starts at p+t*u, where every integer
        1-ell <= t <= length-1 is considered. No height cutoff is used.
        """
        assert length in (self.g.a,self.g.b,self.g.c)
        u=self.g.unit(*ray)
        spans={}
        for reference,ell in self.shapes.reference_shapes(p,ray):
            q,h,j,s=reference
            for offset in range(1-ell,length):
                tile=self.g.add(q,self.g.scale(offset,u)),h,j,s
                if not self.g.admissible(tile):
                    continue
                span=max(0,offset),min(length,offset+ell)
                assert span[0]<span[1]
                if tile in spans:
                    assert spans[tile]==span
                spans[tile]=span
        tiles=tuple(sorted(spans))
        ranges=tuple(spans[t] for t in tiles)
        intervals=tuple(tuple(i for i,(lo,hi) in enumerate(ranges) if lo<=k<hi)
                        for k in range(length))
        assert len(tiles)<=6*length+2*(self.g.a+self.g.b+self.g.c)-6
        return BankCatalogue(tiles,ranges,intervals)

    def satisfied(self,tile,index,selected):
        if tile not in selected:
            return True
        edge=self.edge(tile,index)
        if edge.boundary:
            return True
        catalogue=self.catalogue(edge.start,edge.ray,edge.length)
        return all(sum(catalogue.tiles[i] in selected for i in group)==1
                   for group in catalogue.intervals)

