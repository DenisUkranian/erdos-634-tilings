"""Exact strict-interior overlap at arbitrary powers of the tile denominator."""
from collections import defaultdict


def polygon_record(geometry, tile):
    vertices = geometry.vertices(tile)
    exponent = max(p[2] for p in vertices)
    denominator = geometry.power(exponent)
    points = tuple((x*geometry.power(exponent-e), y*geometry.power(exponent-e))
                   for x, y, e in vertices)
    return points, denominator


def records_overlap(first, second):
    """True exactly when the interiors of two CCW convex triangles overlap."""
    for (points, denominator), (other, other_denominator) in ((first, second), (second, first)):
        for k in range(3):
            x, y = points[k]
            u, v = points[(k+1) % 3]
            if max((u-x)*(q*denominator-y*other_denominator)
                   - (v-y)*(p*denominator-x*other_denominator)
                   for p, q in other) <= 0:
                return False
    return True


def overlap_pairs(geometry, tiles, chosen):
    """Spatial hashing only accelerates a complete exact pair enumeration."""
    bins = defaultdict(list)
    records = {}
    boxes = {}
    result = set()
    step = max(1, 2*geometry.c)
    for i in sorted(chosen):
        points, denominator = polygon_record(geometry, tiles[i])
        records[i] = points, denominator
        x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
        y0, y1 = min(p[1] for p in points), max(p[1] for p in points)
        boxes[i] = x0, x1, y0, y1, denominator
        keys = [(x, y)
                for x in range(x0//(step*denominator), x1//(step*denominator)+1)
                for y in range(y0//(step*denominator), y1//(step*denominator)+1)]
        candidates = set(j for key in keys for j in bins[key])
        for j in candidates:
            u0, u1, v0, v1, other_denominator = boxes[j]
            if (x1*other_denominator <= u0*denominator or
                u1*denominator <= x0*other_denominator or
                y1*other_denominator <= v0*denominator or
                v1*denominator <= y0*other_denominator):
                continue
            if records_overlap(records[i], records[j]):
                result.add((j, i))
        for key in keys:
            bins[key].append(i)
    return sorted(result)
