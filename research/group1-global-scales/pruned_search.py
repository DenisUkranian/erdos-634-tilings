#!/usr/bin/env python3
"""Exact corner search with necessary integer-seam and angle-fan filters.

This is a research search, not a general scale classification. A resource stop
is INCOMPLETE. The search retains every placement of the base exact search.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from functools import cmp_to_key
from fractions import Fraction as F
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'uniform-reduction'))
import exact_search as E
from candidates import Instance


def angle_fans(sides, D):
    """Exact unit rotations of all positive tile-angle sums below pi.

    A partial sum below pi plus one tile angle is strictly below 2*pi.
    Its sine is positive exactly when the new sum is still below pi.
    Breadth-first extension therefore never wraps, and visits every possible
    convex fan. It terminates because each addition is at least the smallest
    positive tile angle. All rotations and sign tests are rational and exact.
    """
    angles = []
    for i in range(3):
        a, b, c = sides[i], sides[(i+1) % 3], sides[(i+2) % 3]
        x = F(b*b+c*c-a*a, 2*b*c)
        angles.append((x, F(1, 2*b*c)))
    found = set()
    queue = deque([(F(1),F(0))])
    while queue:
        current = queue.popleft()
        for tile_angle in angles:
            new = E.cmul(current,tile_angle,D)
            if new[1] > 0 and new not in found:
                found.add(new)
                queue.append(new)
    return found


class PrunedSearch(E.Search):
    def __init__(self, instance, max_nodes=None, seconds=None, use_angles=False):
        super().__init__(instance, max_nodes, seconds)
        self.rejected = Counter()
        self.fans = angle_fans(instance.tile, self.D) if use_angles else None

    def subtract_triangle(self, boundary, candidate):
        """Cancel the new triangle against the current residual boundary.

        Interior edges already cancelled cannot reappear after deleting more
        material. Endpoint atomization is exactly the base search's operation,
        performed incrementally instead of rebuilding from every placed tile.
        """
        all_edges = list(boundary)+[(b,a) for a,b in E.edges(candidate)]
        vertices = set(p for edge in all_edges for p in edge)
        net = Counter()
        for a,b in all_edges:
            self.check_deadline()
            pts = sorted((p for p in vertices if E.on_segment(a,b,p)), reverse=a>b)
            for x,y in zip(pts,pts[1:]):
                if x<y: net[(x,y)] += 1
                elif x>y: net[(y,x)] -= 1
        result = []
        for (a,b), value in net.items():
            if abs(value)>1:
                raise ArithmeticError('Invalid incremental boundary multiplicity')
            if value == 1: result.append((a,b))
            if value == -1: result.append((b,a))
        return result

    def component_areas_valid(self, boundary):
        """An isolated residual component must contain an integer tile count.

        Successor rays trace boundary loops with residual material on the
        left. If negative loops occur, this optional test conservatively skips
        the state rather than guessing which outer loop owns a hole.
        """
        incident = defaultdict(list)
        for index,(a,b) in enumerate(boundary):
            incident[a].append((E.sub(b,a),('out',index)))
            incident[b].append((E.sub(a,b),('in',index)))
        successor = {}
        for vertex,rays in incident.items():
            rays.sort(key=cmp_to_key(E.polar_cmp))
            for i,(_,tag) in enumerate(rays):
                if tag[0] != 'out': continue
                next_tag = rays[(i+1)%len(rays)][1]
                if next_tag[0] != 'in':
                    raise ArithmeticError('Nonalternating residual rays')
                successor[next_tag[1]] = tag[1]
        unseen = set(range(len(boundary)))
        areas = []
        while unseen:
            index = start = min(unseen)
            doubled_area = F(0)
            while True:
                if index not in unseen:
                    if index != start:
                        raise ArithmeticError('Boundary loop joins a previous loop')
                    break
                unseen.remove(index)
                a,b = boundary[index]
                doubled_area += E.cross(a,b)
                index = successor[index]
            areas.append(doubled_area)
        if any(area <= 0 for area in areas):
            return True
        tile_area = E.orient(*self.template)
        if any((area/tile_area).denominator != 1 for area in areas):
            self.rejected['nonintegral_residual_component_area'] += 1
            return False
        return True

    def residual_valid(self, boundary):
        for a, b in boundary:
            v = E.sub(b, a)
            squared = E.dot(v, v, self.D)
            length = E.rational_sqrt(squared)
            if length.denominator != 1:
                self.rejected['nonintegral_known_seam_segment'] += 1
                return False
        if self.fans is not None:
            # Every convex residual sector must be a sum of tile angles.
            # A flat tile cannot meet such a sector through its side.
            for _, vertex, out, inc in E.convex_sectors(boundary, self.D):
                lengths = E.rational_sqrt(E.dot(out,out,self.D)) * E.rational_sqrt(E.dot(inc,inc,self.D))
                rot = (E.dot(out, inc, self.D)/lengths, E.cross(out,inc)/lengths)
                if rot not in self.fans:
                    self.rejected['infeasible_convex_angle_fan'] += 1
                    return False
        return self.component_areas_valid(boundary)

    def dfs(self, placed, boundary=None):
        if self.max_nodes is not None and self.nodes >= self.max_nodes:
            return None
        self.check_deadline()
        self.nodes += 1
        self.deepest = max(self.deepest, len(placed))
        if len(placed) == self.I.n:
            self.found = placed
            return True
        key = tuple(sorted(placed))
        if key in self.dead:
            return False
        if boundary is None:
            boundary = E.atomic_boundary(self.target, placed, self.check_deadline)
        if not self.residual_valid(boundary):
            self.dead.add(key)
            return False
        sectors = E.convex_sectors(boundary, self.D)
        if not sectors:
            raise ArithmeticError('Positive residual area without a convex sector')
        best = None
        for sector in sectors:
            choices = E.placements(self.template, sector, self.target, placed,
                                   self.D, self.check_deadline)
            if best is None or len(choices) < len(best):
                best = choices
            if len(choices) <= 1:
                break
        complete = True
        for candidate in best:
            result = self.dfs(placed+(candidate,),self.subtract_triangle(boundary,candidate))
            if result is True:
                return True
            if result is None:
                complete = False
                break
        if complete:
            self.dead.add(key)
            return False
        return None

    def run(self):
        report = super().run()
        report['pruning_rejections'] = dict(self.rejected)
        report['integer_seam_filter'] = True
        report['angle_fan_filter'] = self.fans is not None
        report['full_Erdos634_solved'] = False
        return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('u', type=int)
    parser.add_argument('v', type=int)
    parser.add_argument('scale', type=int)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--max-nodes', type=int)
    parser.add_argument('--angles', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    u, v, m = args.u, args.v, args.scale
    a,b,c = u*v,v*v-u*u,v*v
    Q = b+c
    instance = Instance('G1-W', (a,b,c), (m*v**3,m*u*Q,m*v*b),
                        Q*m*m, (u,v), m)
    report = PrunedSearch(instance,args.max_nodes,args.seconds,args.angles).run()
    result = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(result)
    print(result,end='')
