"""Check the mixed-area cut inequality independently by taking convex hulls of sums."""
from itertools import product
import json
from check import geom, cell, reconstruct, step
from mixed_enclosure import det, edges, mixed_edges, sorted_polygon


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 2:
        return pts

    def side(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and det(geom.sub(out[-1], out[-2]), geom.sub(p, out[-1])) <= 0:
                out.pop()
            out.append(p)
        return out

    return side(pts)[:-1] + side(pts[::-1])[:-1]


def twice_area(poly):
    return sum(det(a, b) for a, b in zip(poly, poly[1:] + poly[:1]))


def sum_hull(p, q):
    return hull((a+c, b+d) for a, b in p for c, d in q)


def run(which):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, which)
    polygons, centers, origin, _, _ = geom.check_full_tiling(g, tiles)
    paired, _ = geom.long_pairs(g, tiles, polygons, centers, origin)
    lifts, _ = reconstruct(g, tiles, polygons)
    walls = [(lifts[g.N+i], geom.point(g, p), geom.point(g, q))
             for i, (p, q, _, _) in enumerate(g.walls())]
    board = [p for _, p, _ in walls]
    gates = []
    for i, t in enumerate(tiles):
        if i in paired:
            continue
        short = lifts[i]
        long = step(short, cell(g, t[1]+t[3], g.vertices(t)[-1]))
        gates.append((short, long, polygons[i][-1], polygons[i][0]))
    support = sorted(set(lifts[i] for i in range(g.N+3)) | {t for s, t, p, q in gates})
    subsets = tests = 0
    for bits in product((False, True), repeat=len(support)):
        selected = {v for v, b in zip(support, bits) if b}
        n = sum(lifts[i] in selected for i in range(g.N))
        chain = [(p, q) for v, p, q in walls if v in selected]
        for s, t, p, q in gates:
            if (s in selected) != (t in selected):
                chain.append((p, q) if s in selected else (q, p))
        assert sum(det(p, q) for p, q in chain) == n*g.a*g.b
        subsets += 1
        if not n:
            continue
        w = sorted_polygon([geom.sub(q, p) for p, q in chain])
        assert twice_area(w) >= n*g.a*g.b
        for shape in [w, board, [(0,0), (7,-13)], [(0,0),(23,11),(-7,9)],
                      [(0,0),(2,-15),(37,-4),(6,8)]]:
            q = hull(shape)
            t_area = twice_area(board)
            q_area = twice_area(q)
            w_mixed2 = twice_area(sum_hull(w, q)) - twice_area(w) - q_area
            assert w_mixed2 == 2*mixed_edges(w, edges(q))
            total_area = twice_area(sum_hull(board, q))
            assert 4*n*g.a*g.b*total_area <= (2*t_area + w_mixed2)**2
            tests += 1
    return dict(subsets=subsets, mixed_tests=tests)


if __name__ == '__main__':
    print(json.dumps({w:run(w) for w in ('known','macro')}, indent=2))
