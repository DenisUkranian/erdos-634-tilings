#!/usr/bin/env python3
"""Owned-through search with exact interior-point exclusion cliques.

The sampling grid controls only which necessary cuts are added. It never
restricts tile positions, orientations, heights, or possible completions.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys

OWNED = Path(__file__).resolve().parents[1] / 'owned'
sys.path.insert(0, str(OWNED))
from owned_search import OwnedSearch, defaults, GracefulResourceStop
from exact_geometry import polygon_record
from legacy import core


def grid_points(g, tile, step):
    """Enumerate all strictly interior axial grid points, with exact signs."""
    vertices, den = polygon_record(g, tile)
    xs, ys = zip(*vertices)
    for ix in range(min(xs)//(den*step), max(xs)//(den*step)+1):
        x = ix*step
        for iy in range(min(ys)//(den*step), max(ys)//(den*step)+1):
            y = iy*step
            if all((vertices[(k+1)%3][0]-u)*(y*den-v)
                   - (vertices[(k+1)%3][1]-v)*(x*den-u) > 0
                   for k,(u,v) in enumerate(vertices)):
                yield x,y


class SpatialSearch(OwnedSearch):
    def __init__(self, args):
        self.grid_step = args.grid_step or max(1,args.sides[1]//2)
        self.point_columns = defaultdict(list)
        self.point_dirty = set()
        self.point_records = set()
        super().__init__(args)

    def options(self):
        super().options()
        if getattr(self.args,'prefer_tiles',False):
            self.enqueue('(set-option :smt.phase_selection 1)')

    def insert(self, tile):
        old = len(self.tiles)
        index = super().insert(tile)
        if len(self.tiles) != old:
            for point in grid_points(self.g,self.tiles[index],self.grid_step):
                self.point_columns[point].append(index)
                self.point_dirty.add(point)
        return index

    def install_point_cliques(self):
        for point in sorted(self.point_dirty):
            indices = tuple(self.point_columns[point])
            if len(indices)>1:
                self.point_records.add((point,indices))
                self.assert_(core.atmost(1,[f'x{i}' for i in indices]))
        self.point_dirty.clear()

    def flush(self):
        self.install_point_cliques()
        return super().flush()

    def checkpoint(self, iteration, status):
        self.install_point_cliques()
        return super().checkpoint(iteration,status)

    def necessary_snapshot(self):
        snapshot = super().necessary_snapshot()
        snapshot['interior_point_cliques'] = [
            dict(point=point,indices=indices) for point,indices in sorted(self.point_records)]
        snapshot['sampling_grid_step'] = self.grid_step
        snapshot['sampling_grid_restricts_placements'] = False
        return snapshot


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('sides',type=int,nargs=3)
    p.add_argument('--out',required=True)
    p.add_argument('--root-file')
    p.add_argument('--root-id')
    p.add_argument('--rows')
    p.add_argument('--corner-checkpoint')
    p.add_argument('--seed-json')
    p.add_argument('--grid-step',type=int,default=0)
    p.add_argument('--prefer-tiles',action='store_true',
                   help='Heuristic only: initially prefer true Boolean phases.')
    p.add_argument('--timeout-ms',type=int,default=45000)
    p.add_argument('--time-limit',type=float,default=600)
    p.add_argument('--rounds',type=int,default=100)
    p.add_argument('--expand',type=int,default=300)
    p.add_argument('--owner-fans-per-round',type=int,default=12)
    p.add_argument('--owner-rows-per-round',type=int,default=300)
    p.add_argument('--max-columns',type=int,default=180000)
    p.add_argument('--max-rss-mb',type=float,default=2200)
    p.add_argument('--rebuild-every',type=int,default=10)
    p.add_argument('--proof',action='store_true')
    args=defaults(**vars(p.parse_args()))
    assert bool(args.root_file)==bool(args.root_id)
    assert args.grid_step>=0
    search=SpatialSearch(args)
    try:
        search.run()
    except GracefulResourceStop as exc:
        print('INCONCLUSIVE:',exc,flush=True)
    finally:
        search.close()


if __name__=='__main__':
    main()
