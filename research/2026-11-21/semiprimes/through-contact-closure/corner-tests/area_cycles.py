"""Exact supported polygon cuts for unrestricted selected physical tiles.

A simple cycle in the tile skeleton must enclose a whole number of tiles.
Its two additive boundary characters must also fit that number of tiles.
Integer-area mixed-height cycles are not automatically forbidden.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import cmp_to_key
from math import gcd, lcm
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(PACKAGE / 'owned'), str(PACKAGE / 'whole-edges')]
from exact_geometry import polygon_record, records_overlap
from whole_edge_oracle import WholeEdgeOracle


def _sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def _cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def _point(g, p):
    return F(p[0], g.power(p[2])), F(p[1], g.power(p[2]))


def _bins(p, q, step):
    for x in range(min(p[0], q[0])//step, max(p[0], q[0])//step+1):
        for y in range(min(p[1], q[1])//step, max(p[1], q[1])//step+1):
            yield x, y


def greedy_nonoverlap(g, tiles, chosen):
    """A deterministic exact subset; discarding tiles only weakens cuts."""
    step = max(1, 2*g.c)
    bins = defaultdict(list)
    records = {}
    boxes = {}
    retained = []
    for index in sorted(set(chosen)):
        record = polygon_record(g, tiles[index])
        points, den = record
        low = F(min(p[0] for p in points), den), F(min(p[1] for p in points), den)
        high = F(max(p[0] for p in points), den), F(max(p[1] for p in points), den)
        keys = tuple(_bins(low, high, step))
        possible = {j for key in keys for j in bins[key]}
        overlap = False
        for other in sorted(possible):
            lo, hi = boxes[other]
            if high[0] <= lo[0] or hi[0] <= low[0] or high[1] <= lo[1] or hi[1] <= low[1]:
                continue
            if records_overlap(record, records[other]):
                overlap = True
                break
        if overlap:
            continue
        assert g.admissible(tiles[index]), ('Uncontained selected tile', index)
        retained.append(index)
        records[index] = record
        boxes[index] = low, high
        for key in keys:
            bins[key].append(index)
    return retained


def _line(p, q):
    den = lcm(*(v.denominator for v in p+q))
    x, y, u, v = (int(value*den) for value in p+q)
    values = ((y-v)*den, (u-x)*den, x*v-u*y)
    divisor = gcd(gcd(abs(values[0]), abs(values[1])), abs(values[2]))
    assert divisor
    values = tuple(value//divisor for value in values)
    if next(value for value in values if value) < 0:
        values = tuple(-value for value in values)
    return values


def _angle_compare(left, right):
    a = 0 if left[1] > 0 or (left[1] == 0 and left[0] > 0) else 1
    b = 0 if right[1] > 0 or (right[1] == 0 and right[0] > 0) else 1
    if a != b:
        return -1 if a < b else 1
    cross = _cross(left, right)
    return -1 if cross > 0 else 1 if cross < 0 else 0


def _on_segment(point, first, last):
    return (_cross(_sub(last, first), _sub(point, first)) == 0
            and min(first[0], last[0]) <= point[0] <= max(first[0], last[0])
            and min(first[1], last[1]) <= point[1] <= max(first[1], last[1]))


def _intersect(a, b, c, d):
    x, y = _cross(_sub(b,a), _sub(c,a)), _cross(_sub(b,a), _sub(d,a))
    u, v = _cross(_sub(d,c), _sub(a,c)), _cross(_sub(d,c), _sub(b,c))
    if x*y < 0 and u*v < 0:
        return True
    return ((x == 0 and _on_segment(c,a,b)) or (y == 0 and _on_segment(d,a,b))
            or (u == 0 and _on_segment(a,c,d)) or (v == 0 and _on_segment(b,c,d)))


def simple_polygon(vertices):
    """Explicitly rule out all nonadjacent intersections and backtracks."""
    n = len(vertices)
    if n < 3 or len(set(vertices)) != n:
        return False
    for i, a in enumerate(vertices):
        b, c = vertices[(i+1)%n], vertices[(i+2)%n]
        first, second = _sub(b,a), _sub(c,b)
        if _cross(first, second) == 0 and sum(x*y for x,y in zip(first,second)) <= 0:
            return False
        for j in range(i+1,n):
            if j == i+1 or (i == 0 and j == n-1):
                continue
            if _intersect(a,b,vertices[j],vertices[(j+1)%n]):
                return False
    return True


def _skeleton(g, tiles, chosen):
    retained = greedy_nonoverlap(g, tiles, chosen)
    native = {}
    groups = defaultdict(list)
    point_bins = defaultdict(set)
    step = max(1, 2*g.c)
    oracle = WholeEdgeOracle(g)
    metadata = {}
    for index in retained:
        vertices = g.vertices(tiles[index])
        rational = tuple(_point(g,p) for p in vertices)
        for original, point in zip(vertices,rational):
            native[point] = g.point(*original)
            point_bins[point[0]//step,point[1]//step].add(point)
        for edge in range(3):
            first,last = rational[edge],rational[(edge+1)%3]
            low,high = sorted((first,last))
            groups[_line(low,high)].append((low,high,index,edge))
            description = oracle.edge(tiles[index],edge)
            metadata[index,edge] = first,last,description.ray,description.length
    atoms = {}
    for line, sides in groups.items():
        starts, ends = defaultdict(set), defaultdict(set)
        breaks = set()
        for first,last,index,edge in sides:
            starts[first].add((index,edge))
            ends[last].add((index,edge))
            breaks.update((first,last))
            # Include endpoints of OTHER supporting lines as well. This
            # handles a point contact and a genuine T-junction equally.
            for key in _bins(first,last,step):
                for point in point_bins[key]:
                    if first <= point <= last and line[0]*point[0]+line[1]*point[1]+line[2] == 0:
                        breaks.add(point)
        ordered = sorted(breaks)
        active = set()
        for first,last in zip(ordered,ordered[1:]):
            active.difference_update(ends[first])
            active.update(starts[first])
            if active:
                assert (first,last) not in atoms
                atoms[first,last] = tuple(sorted(active))
    adjacency = defaultdict(set)
    for first,last in atoms:
        adjacency[first].add(last)
        adjacency[last].add(first)
    ordered_neighbors = {}
    for point, neighbors in adjacency.items():
        ordered_neighbors[point] = sorted(neighbors, key=cmp_to_key(
            lambda a,b: _angle_compare(_sub(a,point),_sub(b,point))))
    successor = {}
    for point, neighbors in ordered_neighbors.items():
        for index,other in enumerate(neighbors):
            successor[other,point] = point,neighbors[index-1]
    return retained,native,atoms,metadata,successor


def _budget(g, area, W0, W1):
    E0, E1 = W0/(g.a-g.b-g.c), W1/(g.a-g.b+g.c)
    even, odd = (E0+E1)/2, (E0-E1)/2
    failures = []
    if area.denominator != 1:
        failures.append('nonintegral_area')
    if even.denominator != 1:
        failures.append('nonintegral_even_charge')
    if odd.denominator != 1:
        failures.append('nonintegral_odd_charge')
    if area.denominator == even.denominator == odd.denominator == 1:
        if area < abs(even)+abs(odd):
            failures.append('insufficient_area_for_signed_population')
        if (area-even-odd) % 2:
            failures.append('incompatible_population_parity')
    return dict(W0=str(W0),W1=str(W1),even_charge=str(even),odd_charge=str(odd),
                violations=failures)


def selected_skeleton_faces(g, tiles, chosen):
    """Yield exact simple positive face cycles of a nonoverlap subset.

    Repeated-vertex face walks are skipped, so this is intentionally not a
    complete detector of every possible skeleton cycle. No resulting cut
    depends on that detection completeness.
    """
    retained,native,atoms,metadata,successor = _skeleton(g,tiles,chosen)
    unvisited = set(successor)
    for initial in sorted(successor):
        if initial not in unvisited:
            continue
        edge, vertices = initial, []
        while True:
            assert edge in unvisited
            unvisited.remove(edge)
            vertices.append(edge[0])
            edge = successor[edge]
            if edge == initial:
                break
        if len(vertices) < 3 or len(set(vertices)) != len(vertices):
            continue
        area2 = sum(_cross(p,q) for p,q in zip(vertices,vertices[1:]+vertices[:1]))
        if area2 <= 0:
            continue
        area = area2/(g.a*g.b)
        W0 = W1 = F(0)
        witnesses, indices = [], set()
        for first,last in zip(vertices,vertices[1:]+vertices[:1]):
            owners = atoms[tuple(sorted((first,last)))]
            owner,side = min(owners)
            start,end,(h,j),length = metadata[owner,side]
            axis = 0 if start[0] != end[0] else 1
            signed_length = length*(last[axis]-first[axis])/(end[axis]-start[axis])
            W0 += signed_length*(-1 if j%2 else 1)
            W1 += signed_length*(-1 if (h+j)%2 else 1)
            indices.add(owner)
            witnesses.append(dict(
                start=list(native[first]),end=list(native[last]),
                representative=owner,side=side,
                selected_owners=sorted({i for i,_ in owners}),
                length=str(abs(signed_length)),
                direction=[h,j if signed_length > 0 else (j+3)%6]))
        budget = _budget(g,area,W0,W1)
        # The nonoverlap subset makes the atom graph planar. Before a
        # no-good is returned, also check its polygon directly pairwise.
        if budget['violations']:
            assert simple_polygon(vertices)
        yield dict(indices=sorted(indices),vertices=[list(native[p]) for p in vertices+[vertices[0]]],
                   edges=witnesses,twice_axial_area=str(area2),tile_area_ratio=str(area),
                   budget=budget,greedy_selected_count=len(retained))


def selected_area_cycles(g, tiles, chosen, max_cycles=1, use_characters=True):
    """Return valid selected-owner no-goods from exact polygon budgets.

    Each witness forbids the simultaneous selected tiles in its indices.
    A positive limit only caps how many sound cuts are returned; zero means
    no limit. With use_characters=False only nonintegral areas are cut.
    """
    assert max_cycles >= 0
    answer = []
    for witness in selected_skeleton_faces(g,tiles,chosen):
        failures = witness['budget']['violations']
        if not failures or (not use_characters and 'nonintegral_area' not in failures):
            continue
        answer.append(witness)
        if max_cycles and len(answer) >= max_cycles:
            break
    return answer
