"""Reconstruct Euler words and compare shoelace areas to actual whole tiles."""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "research/2026-11-21/semiprimes/global-closure-next/contact-budget"))
import verify_contact_budget as geom


def translated_area(segments):
    outgoing = defaultdict(list)
    flow = Counter()
    direct = 0
    for start, end in segments:
        outgoing[start].append(end)
        flow[start] += 1
        flow[end] -= 1
        direct += geom.det(start, end)
    assert not any(flow.values())
    total = count = 0
    for start, edges in outgoing.copy().items():
        while edges:
            # Finite zero-divergence multigraph. Every maximal trail closes.
            point = start
            x = y = 0
            while outgoing[point]:
                end = outgoing[point].pop()
                dx, dy = geom.sub(end, point)
                total += x*dy - y*dx
                x, y = x+dx, y+dy
                point = end
                count += 1
            assert point == start and (x, y) == (0, 0)
    assert count == len(segments) and total == direct
    return total


def nested_control(g, tiles, paired, tree, budget):
    high = []
    banks = []
    for k in (1, 2):
        level = k if tree == 1 else 1-k
        anchor = g.walls()[1][0] if tree == 1 else g.walls()[0][0]
        node = budget.node(anchor, level)
        def high_side(point, h):
            desc = tree*h >= level and budget.node(point, level) == node
            return desc if tree == 1 else not desc
        side = {i for i, t in enumerate(tiles) if high_side(t[0], t[1])}
        p = set()
        q = set()
        for i,t in enumerate(tiles):
            if i in paired:
                continue
            long_high = high_side(g.vertices(t)[0], t[1]+t[3])
            if i in side and not long_high:
                p.add(i)
            if i not in side and long_high:
                q.add(i)
        high.append(side)
        banks.append((p,q))
    first, second = high
    assert second <= first
    p,q = banks[0]
    t,v = banks[1]
    used = p | q | t | v
    assert len(used) == sum(map(len,(p,q,t,v)))
    def signed(ids, parity=None):
        return sum(geom.eps(tiles[i]) for i in ids
                   if parity is None or tiles[i][1] % 2 == parity)
    e,o = (signed(first,h) for h in (0,1))
    f,j = (signed(second,h) for h in (0,1))
    predicted = (-(g.a-g.b)-e-signed(q), -g.c-o, e-f, o-j-signed(p)-signed(v),
                 f-signed(t), j)
    regions = [set(range(g.N))-first, first-second, second]
    actual = tuple(signed(region-used-paired, h) for region in regions for h in (0,1))
    assert actual == predicted
    unmatched = g.N-len(paired)
    assert 23 <= len(used)+sum(map(abs,actual)) <= unmatched
    return unmatched


def check(which):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, which)
    polygons, centres, origin, _, _ = geom.check_full_tiling(g, tiles)
    paired, _ = geom.long_pairs(g, tiles, polygons, centres, origin)
    cuts = 0
    slants = []
    for tree in (1, -1):
        budget = geom.PhaseBudget(g, tree)
        unmatched = nested_control(g, tiles, paired, tree, budget)
        crossings = defaultdict(list)
        for i, tile in enumerate(tiles):
            q, h, _, hand = tile
            short = budget.node(q, tree*h)
            long = budget.node(g.vertices(tile)[-1], tree*(h+hand))
            child = max(short, long, key=lambda v: v[0])
            crossings[child].append((i, 1 if short == child else -1))
        total = 0
        for child, members in crossings.items():
            k = child[0]
            def belongs(q, h):
                return tree*h >= k and budget.node(q, k) == child

            inside = [t for t in tiles if belongs(t[0], t[1])]
            outer = [(u, v, h) for u, v, h, _ in g.walls() if belongs(u, h)]
            assert len(outer) in (0, 1, 2, 3)
            complement = len(outer) >= 2
            if complement:
                outer = [(u, v, h) for u, v, h, _ in g.walls() if not belongs(u, h)]
            assert not outer or len(outer) == 1 and outer[0][2] == 2
            segments = [(geom.point(g, u), geom.point(g, v)) for u, v, _ in outer]
            P = Q = m = 0
            for i, tau in members:
                if i in paired:
                    continue
                poly = polygons[i]
                segment = poly[-1], poly[0]
                segments.append(segment if (tau == 1) != complement else segment[::-1])
                if tau == 1:
                    P += geom.eps(tiles[i])
                else:
                    Q += geom.eps(tiles[i])
                m += 1
            n = g.N-len(inside) if complement else len(inside)
            assert translated_area(segments) == n*g.a*g.b
            total += m
            cuts += 1
            if tree == 1 and k == 2 and outer:
                odd = sum(geom.eps(t) for t in inside if t[1] % 2)
                even = sum(geom.eps(t) for t in inside if not t[1] % 2)
                if odd == even == 0:
                    assert (P, Q) == (0, g.c)
                    multipliers = {7: [0], 9: [0, 1, 2], 11: list(range(8))}
                    if m in multipliers:
                        assert Fraction(n, 2*g.c) in multipliers[m]
                    slants.append((n, m, P, Q))
        assert total == len(tiles)-len(paired)
    assert slants
    print(which, "cuts", cuts, "unmatched", unmatched, "balanced slant (n,m,P,Q)", slants)


if __name__ == "__main__":
    for name in ("known", "macro"):
        check(name)
