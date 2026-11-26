"""Exact branch arithmetic and independent gate measurements on complete F2 controls."""
from collections import Counter, defaultdict
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "joint-cell-tree"))
from controls import cell, geom, reconstruct, step
from hull import ceil_div, check as check_hull


def branch(v, w):
    """First neighbor on the unique path from v to another lift w."""
    assert v != w
    return w[:len(v) + 1] if w[:len(v)] == v else v[:-1]


def measure_control(which):
    g = geom.Geometry(5, 3, 7)
    tiles, _ = geom.read_tiles(g, which)
    polys, *_ = geom.check_full_tiling(g, tiles)
    lifts, slant = reconstruct(g, tiles, polys)
    axial = slant[:1]
    # Apply the path isometry to signs and parity labels. Tree paths keep their IDs.
    vlist = {w[:i] for w in lifts.values() for i in range(1, len(w) + 1)}
    populations = Counter(lifts[i] for i in range(len(tiles)))
    d, c = g.a - g.b, g.c
    odd_charges = Counter()
    for i, tile in enumerate(tiles):
        if tile[1] % 2:
            odd_charges[lifts[i]] -= geom.eps(tile)
    marked = {v for v, value in odd_charges.items() if value} | {axial, slant}
    half_excess = surplus = 0
    checked = Counter()
    for v in vlist - {axial}:
        odd = v[-1][0] % 2
        side_charges = defaultdict(lambda: [0, 0])
        signed_owners, unsigned_owners = Counter(), Counter()
        far_owners = Counter()
        for i, tile in enumerate(tiles):
            short = lifts[i]
            sign = -geom.eps(tile)
            if short == v:
                long = step(v, cell(g, tile[1] + tile[3], g.vertices(tile)[-1]))
                signed_owners[long] += sign
                unsigned_owners[long] += 1
            else:
                w = branch(v, short)
                side_charges[w][tile[1] % 2] += sign
                long = step(short, cell(g, tile[1] + tile[3], g.vertices(tile)[-1]))
                if long == v:
                    assert w == short
                    far_owners[w] += sign
        core_gate = branch(v, axial)
        slant_gate = branch(v, slant) if v != slant else None
        neighbors = set(side_charges) | set(unsigned_owners) | {core_gate}
        if slant_gate is not None:
            neighbors.add(slant_gate)
        S = U = total_s = total_t = 0
        for w in neighbors:
            even, odd_charge = side_charges[w]
            ic, it = int(w == core_gate), int(w == slant_gate)
            assert (even - d * ic) % c == odd_charge % c == 0
            if odd:
                s, t = odd_charge // c - 2 * ic + it, (even - d * ic) // c
            else:
                s, t = (even - d * ic) // c, odd_charge // c - ic
            assert signed_owners[w] == d * t - c * s
            if odd:
                assert far_owners[w] == even - d*(odd_charge//c)
                if not (ic or it or odd_charge):
                    assert d*far_owners[w] == c*signed_owners[w]
            if populations[v]:
                assert 2 * max((unsigned_owners[w] + signed_owners[w]) // 2,
                               (unsigned_owners[w] - signed_owners[w]) // 2) <= populations[v]
            S += abs(s)
            U += abs(t)
            total_s += s
            total_t += t
            checked["odd_gate_equations" if odd else "even_gate_equations"] += 1
        assert total_s * c == -sum(signed_owners.values()) and total_t == 0
        if odd:
            assert sum(far_owners.values()) * c == d * sum(signed_owners.values())
        if odd_charges[v]:
            hull_gates = {branch(v, mark) for mark in marked if mark != v}
            degree = len(hull_gates)
            surplus += 2 - degree
            charge = abs(odd_charges[v])
            minority = (populations[v] - charge)//2
            sigma = 1 if odd_charges[v] > 0 else -1
            outside = sum(sigma*value for gate, value in signed_owners.items()
                          if gate not in hull_gates)
            assert outside % d == 0
            assert outside >= charge - degree*(charge//2 + minority)
            assert sum(sigma*value for gate, value in far_owners.items()
                       if gate not in hull_gates) == c*(outside//d)
            J = ceil_div(charge-degree*(charge//2+minority),d)
            half_excess += minority + max(0,c*J-d*(charge//c))
        n_odd = sum(tile[1] % 2 for tile in tiles)
        n_even = len(tiles) - n_odd
        if odd:
            assert n_odd >= populations[v] + c * (S - 3) and n_even >= c * U - d
        else:
            assert n_even >= populations[v] + c * S - d and n_odd >= c * (U - 1)
        checked["ordinary_lifts"] += 1
    variation = sum(map(abs,odd_charges.values()))//c
    assert surplus >= 0 and (c+d)*variation + 2*half_excess <= len(tiles)
    checked["charged_hull_degree_surplus"] = surplus
    checked["hull_tile_lower_bound"] = (c+d)*variation + 2*half_excess
    return dict(sorted(checked.items()))


def minimum_variation(c, d, k, cap, weight, ceiling):
    """Unbounded multisets of gates, with positive integer cost as the DP index."""
    assert cap < min(c, d)
    options = []
    # If the complete variation costs at most ceiling, each charged
    # coordinate costs at most ceiling. Derive the other from the gate law.
    for q in range(cap + 1):
        for x in range(-ceiling, ceiling + 1):
            if weight == "t":
                t = x
                if (d * t - q) % c:
                    continue
                s = (d * t - q) // c
            else:
                s = x
                if (q + c * s) % d:
                    continue
                t = (q + c * s) // d
            cost = {"s": abs(s), "t": abs(t), "both": abs(s) + abs(t)}[weight]
            if cost == 0:
                assert q == s == t == 0
            elif cost <= ceiling:
                options.append((q, s, cost))
    levels = [set() for _ in range(ceiling + 1)]
    levels[0].add((0, 0))
    for used, states in enumerate(levels):
        if (k * c, -k) in states:
            return used
        for q, s, cost in options:
            if used + cost <= ceiling:
                levels[used + cost].update(
                    (p + q, r + s) for p, r in states if p + q <= k * c
                )
    raise ValueError("No terminal state within cost ceiling")


def main():
    records = {}
    for c, d, k, num, den, expected in [
        (37, 26, 2, 43, 222, [10, 12, 22]),
        (37, 26, 3, 43, 222, [9, 12, 21]),
        (43, 22, 2, 8, 43, [46, 88, 134]),
    ]:
        cap = num * k * c // den
        result = [minimum_variation(c, d, k, cap, w, bound)
                  for w, bound in zip(("s", "t", "both"), expected)]
        assert result == expected
        assert (k*c + cap-1)//cap == 6
        records[f"c{c}_k{k}"] = dict(cap=cap, min_S=result[0], min_U=result[1],
                                     min_S_plus_U=result[2])
    for q in range(17):
        # For l<=0 and l>=1 the slopes are constant on all integer tails.
        for ell in (0, 1):
            assert abs(q-22*ell) >= q-10*ell
    assert 86+43*(132-3)-22 == 5611 > 5063
    assert 86+43*(134-3)-22 == 5697 > 5063
    assert (3431-3431%37)//37 == 92 and 4*26 > 92
    return {"base_main": "d7a7af8d2b3bfad140b3ce84c4e35070564e73ff",
            "original_counts": {"3431": "OPEN", "5063": "OPEN"},
            "gate_relaxation": records,
            "maximum_degree_surplus_by_odd_variation": check_hull(),
            "controls_143": {which: measure_control(which) for which in ("known", "macro")},
            "max_combined_monochromatic_two_or_three_block_lifts_3431": 3,
            "ordinary_86_tile_cell_signs_5063": [43, 43]}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so every certificate assertion is checked.")
    print(json.dumps(main(), indent=2))
