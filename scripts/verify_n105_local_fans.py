#!/usr/bin/env python3
"""Replay one exact partial collar and independent full fans at its corners.

This imports no search or geometry generator. Fraction convex clipping checks
positive witnesses; oriented edge atomization enumerates every residual corner.
Fans at different corners are deliberately NOT asserted jointly compatible.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys

if not __debug__:
    raise SystemExit('Run without -O: exact verification assertions are required.')


def cross(u, v):
    return u[0]*v[1]-u[1]*v[0]


def sub(u, v):
    return u[0]-v[0], u[1]-v[1]


def det(p, q, r):
    return cross(sub(q, p), sub(r, p))


def area2(poly):
    return sum(cross(p, q) for p, q in zip(poly, poly[1:]+poly[:1]))


def clip(polygon, triangle):
    p = list(polygon)
    for j in range(3):
        if not p:
            break
        a, b = triangle[j], triangle[(j+1) % 3]
        out = []
        for u, v in zip(p, p[1:]+p[:1]):
            su, sv = det(a, b, u), det(a, b, v)
            if su >= 0:
                out.append(u)
            if su*sv < 0:
                r = su/(su-sv)
                out.append((u[0]+r*(v[0]-u[0]), u[1]+r*(v[1]-u[1])))
        p = out
    return p


def same_ray(u, v):
    return cross(u, v) == 0 and u[0]*v[0]+u[1]*v[1] > 0


def tile_check(t):
    assert len(t) == 3 and area2(t) == 105
    assert all(x >= 0 and y >= 0 and x+y <= 105 for x, y in t)
    lengths = []
    for p, q in zip(t, t[1:]+t[:1]):
        x, y = sub(q, p)
        lengths.append(x*x+x*y+y*y)
    assert sorted(lengths) == [25, 361, 441]


def residual_loop(triangles):
    outer = ((Q(0), Q(0)), (Q(105), Q(0)), (Q(0), Q(105)))
    vertices = set(outer) | {p for t in triangles for p in t}
    edges = list(zip(outer, outer[1:]+outer[:1]))
    edges += [(q, p) for t in triangles for p, q in zip(t, t[1:]+t[:1])]
    atoms = Counter()
    for p, q in edges:
        cuts = [r for r in vertices if det(p, q, r) == 0 and
                (r[0]-p[0])*(r[0]-q[0])+(r[1]-p[1])*(r[1]-q[1]) <= 0]
        cuts.sort(key=lambda r: (r[0]-p[0])*(q[0]-p[0])+(r[1]-p[1])*(q[1]-p[1]))
        atoms.update(zip(cuts, cuts[1:]))
    for p, q in list(atoms):
        n = min(atoms[p, q], atoms[q, p])
        atoms[p, q] -= n
        atoms[q, p] -= n
    out = defaultdict(list)
    for (p, q), n in atoms.items():
        assert n in (0, 1)
        if n:
            out[p].append(q)
    assert all(len(qs) == 1 for qs in out.values())
    assert Counter(qs[0] for qs in out.values()) == Counter(out.keys())
    loops = []
    while out:
        start = next(iter(out))
        cur, poly = start, []
        while True:
            poly.append(cur)
            cur = out.pop(cur)[0]
            if cur == start:
                break
        loops.append(poly)
    assert len(loops) == 1
    return loops[0]


def verify(data_directory):
    cp = data_directory/'n105-local-fan-collar-5-21-19.json'
    fp = data_directory/'n105-local-fan-witnesses-5-21-19.json'
    raw, fraw = cp.read_bytes(), fp.read_bytes()
    obj, proof = json.loads(raw), json.loads(fraw)
    assert obj['format'] == 'partial-boundary-collar-v1'
    assert obj['tile'] == [5, 21, 19] and obj['side'] == 105
    assert obj['vertices_are_oblique'] is True and obj['complete_tiling'] is False
    assert proof['format'] == 'individual-convex-fans-v1'
    assert proof['collar'] == cp.name and proof['collar_sha256'] == sha256(raw).hexdigest()
    assert proof['fans_asserted_jointly_compatible'] is False
    D = obj['scale']
    assert type(D) is int and D > 0
    triangles = tuple(tuple((Q(x, D), Q(y, D)) for x, y in t) for t in obj['triangles'])
    assert len(triangles) == obj['count'] == 45
    assert len({tuple(sorted(t)) for t in triangles}) == 45
    pair_tests = 0
    for i, t in enumerate(triangles):
        tile_check(t)
        for other in triangles[:i]:
            assert area2(clip(t, other)) == 0
            pair_tests += 1
    poly = residual_loop(triangles)
    assert area2(poly)/105 == 60
    margin = min(min(x, y, 105-x-y) for x, y in poly)
    assert margin > 0
    corners = {}
    for i, P in enumerate(poly):
        u, w = sub(poly[(i+1) % len(poly)], P), sub(poly[i-1], P)
        if cross(u, w) > 0:
            assert P not in corners
            corners[P] = (u, w)
    assert len(corners) == 18
    witnesses = proof['sectors']
    assert len(witnesses) == len(corners)
    seen, fan_tests, fan_tiles = set(), 0, 0
    for row in witnesses:
        P = tuple(map(Q, row['point']))
        assert P in corners and P not in seen
        seen.add(P)
        u, w = corners[P]
        assert same_ray(u, tuple(map(Q, row['outgoing'])))
        assert same_ray(w, tuple(map(Q, row['incoming_back'])))
        fan = tuple(tuple(tuple(map(Q, p)) for p in t) for t in row['fan'])
        assert fan
        current = u
        for j, t in enumerate(fan):
            tile_check(t)
            assert t[0] == P
            v, nxt = sub(t[1], P), sub(t[2], P)
            assert same_ray(current, v)
            # Each triangle stays inside this strictly convex angular sector.
            assert all(cross(u, z) >= 0 and cross(z, w) >= 0 for z in (v, nxt))
            assert cross(v, nxt) > 0
            for other in triangles+fan[:j]:
                assert area2(clip(t, other)) == 0
                fan_tests += 1
            current = nxt
            fan_tiles += 1
        assert same_ray(current, w)
    assert seen == set(corners)
    return dict(verdict='PASS_INDIVIDUAL_FULL_FANS_ONLY', tile=[5, 21, 19],
                target_side=105, placed_tiles=45, residual_tile_area=60,
                residual_boundary_vertices=len(poly), convex_sectors_checked=18,
                local_fan_tiles_checked=fan_tiles, collar_pair_tests=pair_tests,
                fan_clipping_pair_tests=fan_tests,
                minimum_oblique_boundary_margin=str(margin),
                collar_sha256=sha256(raw).hexdigest(), fan_witness_sha256=sha256(fraw).hexdigest(),
                fans_asserted_jointly_compatible=False, complete_tiling=False,
                global_N105_decided=False, search_imported=False)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise SystemExit('Usage: verify_n105_local_fans.py [DATA_DIRECTORY]')
    data = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]/'data'
    print(json.dumps(verify(data), indent=2, sort_keys=True))
