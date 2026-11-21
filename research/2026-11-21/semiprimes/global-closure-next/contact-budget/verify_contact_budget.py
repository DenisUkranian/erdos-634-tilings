#!/usr/bin/env python3
"""Exact geometric controls for the global charge/contact/inertia theorem.

The checker verifies two complete positive tilings and every induced cut in
both prime trees. It does not find or exclude a 3431 or 5063 tiling.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CONT = ROOT / 'research/2026-11-20/semiprimes/continuation'
sys.path[:0] = [str(CONT / 'global-endpoints/integer'),
                str(CONT / 'vertex-phase')]
from global_core_sat import Geometry
from phase_budget import PhaseBudget


def point(g, p):
    return F(p[0], g.c ** p[2]), F(p[1], g.c ** p[2])


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def norm(p):
    return p[0] ** 2 + p[0] * p[1] + p[1] ** 2


def eps(t):
    return t[3] * (-1 if t[2] % 2 else 1)


def read_tiles(g, which):
    if which == 'known':
        path = CONT / 'global-endpoints/tiling_143.json'
        data = json.loads(path.read_text())
        tiles = [(tuple(t[0]), *t[1:]) for t in data['tiles']]
    else:
        path = CONT / 'charge-transport/geometry/macro143_certificate.json'
        data = json.loads(path.read_text())
        denominator = data['denominator']
        exponent = 0
        while g.c ** exponent < denominator:
            exponent += 1
        assert g.c ** exponent == denominator
        tiles = []
        for raw in data['triangles']:
            vertices = {g.point(x, y, exponent) for x, y in raw}
            found = []
            for q in vertices:
                for h in (0, 1):
                    for j in range(6):
                        for s in (-1, 1):
                            tile = q, h, j, s
                            if set(g.vertices(tile)) == vertices:
                                found.append(tile)
            assert len(found) == 1
            tiles.append(found[0])
    return tiles, {'path': str(path.relative_to(ROOT)),
                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def check_full_tiling(g, tiles):
    assert len(set(tiles)) == len(tiles) == g.N
    events = defaultdict(Counter)
    polys = []
    centroids = []
    for tile in tiles:
        poly = [point(g, p) for p in g.vertices(tile)]
        assert sorted(norm(sub(poly[(i + 1) % 3], poly[i]))
                      for i in range(3)) == sorted([g.a ** 2, g.b ** 2, g.c ** 2])
        assert all(x >= 0 and y >= 0 and g.B * x + g.A * y <= g.A * g.B
                   for x, y in poly)
        assert sum(det(p, q) for p, q in zip(poly, poly[1:] + poly[:1])) == g.a * g.b
        polys.append(poly)
        centroids.append(tuple(sum(p[i] for p in poly) / 3 for i in (0, 1)))
    board = [(F(0), F(0)), (F(g.A), F(0)), (F(0), F(g.B))]
    for poly, sign in [(p, 1) for p in polys] + [(board, -1)]:
        for p, q in zip(poly, poly[1:] + poly[:1]):
            dx, dy = sub(q, p)
            direction = (F(1), dy / dx) if dx else (F(0), F(1))
            line = direction, det(direction, p)
            events[line][p] += sign
            events[line][q] -= sign
    assert all(not any(row.values()) for row in events.values())
    centre = F(g.A, 3), F(g.B, 3)
    assert all(sum(p[i] for p in centroids) == g.N * centre[i] for i in (0, 1))
    sdiff = g.A ** 2 + g.B ** 2 + g.c ** 4 - g.a ** 2 - g.b ** 2 - g.c ** 2
    inertia = sum(norm(sub(p, centre)) for p in centroids)
    assert inertia == F(g.N * sdiff, 36)
    assert sum(eps(t) for t in tiles if t[1] % 2) == -g.c
    assert sum(eps(t) for t in tiles if not t[1] % 2) == -(g.a - g.b)
    return polys, centroids, centre, inertia, sdiff


def long_pairs(g, tiles, polys, centroids, centre):
    # A full long-side coincidence only counts as the cancelled pair when
    # the short height and hand agree and the apex is the actual half-turn.
    groups = defaultdict(list)
    for i, tile in enumerate(tiles):
        p, q = polys[i][-1], polys[i][0]
        groups[(tile[1], tile[3], tuple(sorted((p, q))))].append(i)
    matched = set()
    pairs = []
    D = g.a ** 2 + g.b ** 2 - g.a * g.b
    for key, ids in groups.items():
        assert len(ids) <= 2
        if len(ids) != 2:
            continue
        i, j = ids
        p, q = polys[i][-1], polys[i][0]
        ai, aj = point(g, tiles[i][0]), point(g, tiles[j][0])
        assert tuple(ai[k] + aj[k] for k in (0, 1)) == tuple(p[k] + q[k] for k in (0, 1))
        assert eps(tiles[i]) == -eps(tiles[j])
        assert sub(polys[i][0], polys[i][-1]) == tuple(-v for v in sub(polys[j][0], polys[j][-1]))
        midpoint = tuple((p[k] + q[k]) / 2 for k in (0, 1))
        assert norm(sub(centroids[i], midpoint)) == F(D, 36)
        assert norm(sub(centroids[j], midpoint)) == F(D, 36)
        assert norm(sub(centroids[i], centre)) + norm(sub(centroids[j], centre)) == 2 * norm(sub(midpoint, centre)) + F(D, 18)
        matched.update(ids)
        pairs.append(ids)
    return matched, pairs


def check_tree(g, tiles, polys, centroids, centre, inertia, sdiff, matched, tree):
    budget = PhaseBudget(g, tree)
    edges = defaultdict(list)
    for i, (q, h, j, s) in enumerate(tiles):
        short = budget.node(q, tree * h)
        long = budget.node(g.vertices(tiles[i])[-1], tree * (h + s))
        assert abs(short[0] - long[0]) == 1
        child = short if short[0] > long[0] else long
        tau = 1 if child == short else -1
        edges[child].append((i, tau))
    records = []
    lhs = F(0)
    total_l = total_m = 0
    free_load = 0
    for child, members in sorted(edges.items()):
        level = child[0]
        physical_height = tree * level
        inside = [i for i, t in enumerate(tiles)
                  if tree * t[1] >= level and budget.node(t[0], level) == child]
        outer = [k for k, (p, q, h, j) in enumerate(g.walls())
                 if tree * h >= level and budget.node(p, level) == child]
        assert (0 in outer) == (2 in outer)
        w = len(outer)
        bsum = sum((g.A, -g.c ** 2, g.B)[k] for k in outer)
        G = sum(eps(tiles[i]) for i in inside)
        Gstar = sum((-1 if tiles[i][1] % 2 else 1) * eps(tiles[i]) for i in inside)
        P = sum(eps(tiles[i]) for i, tau in members if tau == 1)
        Q = sum(eps(tiles[i]) for i, tau in members if tau == -1)
        assert g.c * (P - Q) == (g.c - g.a + g.b) * G + bsum
        assert g.c * (-1 if physical_height % 2 else 1) * (P + Q) == (g.c + g.a - g.b) * Gstar - bsum
        bank = [(i, tau) for i, tau in members if i not in matched]
        U = sum(tau == 1 for i, tau in bank)
        V = sum(tau == -1 for i, tau in bank)
        assert U >= abs(P) and V >= abs(Q)
        assert (U - P) % 2 == (V - Q) % 2 == 0
        M = U + V
        n = len(inside)
        C = 3 * n - g.N * w - U + V
        physical_flux = sum(tau * det(sub(centroids[i], centre), sub(polys[i][0], polys[i][-1])) for i, tau in bank)
        assert physical_flux == F(g.a * g.b * C, 3)
        p, q = abs(P), abs(Q)
        area_count = 3 * n - g.N * w
        load = p + q + abs(area_count - p + q)
        assert max(0, load - M) <= abs(C)
        if not outer:
            assert load == 3 * n + 2 * abs(Q)
            free_load += load
        if M:
            cost = F(C * C, M)
            bank_inertia = sum(norm(sub(centroids[i], centre)) for i, tau in bank)
            assert cost <= F(12 * g.c ** 2, g.a ** 2 * g.b ** 2) * bank_inertia
            lhs += cost
        else:
            assert C == load == 0
        total_m += M
        total_l += load
        records.append({'child': list(child), 'root_height': physical_height,
                        'subtree_tiles': n, 'odd_charge': sum(eps(tiles[i]) for i in inside if tiles[i][1] % 2),
                        'G': G, 'G_star': Gstar, 'exterior_side_count': w,
                        'P': P, 'Q': Q, 'U': U, 'V': V, 'M': M,
                        'area_residual': C, 'charge_area_load': load})
    assert total_m == g.N - len(matched)
    D = g.a ** 2 + g.b ** 2 - g.a * g.b
    Kbase = F(g.c ** 2 * g.N * sdiff, 3 * g.a ** 2 * g.b ** 2)
    Kmatched = F(g.c ** 2 * (g.N * sdiff - (g.N - total_m) * D), 3 * g.a ** 2 * g.b ** 2)
    Kactual = F(12 * g.c ** 2, g.a ** 2 * g.b ** 2) * sum(norm(sub(t, centre)) for i, t in enumerate(centroids) if i not in matched)
    assert lhs <= Kactual <= Kmatched <= Kbase
    assert F(max(0, total_l - total_m) ** 2) <= total_m * Kmatched
    return {'tree': tree, 'cuts': records, 'unmatched_tiles': total_m,
            'quadratic_cost': lhs, 'actual_bank_inertia_bound': Kactual,
            'pair_reserve_bound': Kmatched, 'board_inertia_bound': Kbase,
            'total_charge_area_load': total_l, 'exterior_free_load': free_load,
            'charge_transport': 'PASS', 'exact_area_flux': 'PASS',
            'global_inertia_and_pair_reserve': 'PASS', 'scalar_corollary': 'PASS'}


def json_exact(x):
    if isinstance(x, F):
        return x.numerator if x.denominator == 1 else str(x)
    if isinstance(x, list):
        return [json_exact(v) for v in x]
    if isinstance(x, tuple):
        return [json_exact(v) for v in x]
    if isinstance(x, dict):
        return {str(k): json_exact(v) for k, v in x.items()}
    return x


def solve_rational(matrix, rhs):
    """Small exact grounded Laplacian solve; controls need no optimizer."""
    n = len(rhs)
    rows = [[F(v) for v in r] + [F(b)] for r, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v / scale for v in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [u - scale * v for u, v in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def electrical_energy(graph_edges, demand):
    """Return exact minimum squared edge-flow norm for prescribed divergence."""
    adjacency = defaultdict(set)
    for u, v in graph_edges:
        assert u != v
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert set(demand) == set(adjacency)
    potentials = {}
    components = []
    remaining = set(adjacency)
    while remaining:
        start = min(remaining)
        component = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u] - component:
                component.add(v)
                stack.append(v)
        remaining -= component
        nodes = sorted(component)
        assert sum(demand[u] for u in nodes) == 0
        free = nodes[1:]
        index = {u: i for i, u in enumerate(free)}
        matrix = [[0] * len(free) for _ in free]
        for u, v in graph_edges:
            if u not in component:
                continue
            if u in index:
                matrix[index[u]][index[u]] += 1
            if v in index:
                matrix[index[v]][index[v]] += 1
            if u in index and v in index:
                matrix[index[u]][index[v]] -= 1
                matrix[index[v]][index[u]] -= 1
        values = solve_rational(matrix, [demand[u] for u in free])
        potentials[start] = F(0)
        potentials.update(zip(free, values))
        components.append(nodes)
    flow = [potentials[u] - potentials[v] for u, v in graph_edges]
    divergence = Counter()
    for (u, v), f in zip(graph_edges, flow):
        divergence[u] += f
        divergence[v] -= f
    assert all(divergence[u] == demand[u] for u in demand)
    energy = sum(f * f for f in flow)
    assert energy == sum(demand[u] * potentials[u] for u in demand)
    return energy, potentials, components


def check_joint_graph(g, tiles, polys, centroids, centre, matched, tree_reports):
    budgets = {tree: PhaseBudget(g, tree) for tree in (1, -1)}
    graph_edges = []
    physical_flows = []
    charge_flows = []
    alternating_charge_flows = []
    records = {}
    vertex_populations = {}
    demand = {}
    for report in tree_reports:
        tree = report['tree']
        for cut in report['cuts']:
            vertex = (tree, *cut['child'])
            records[vertex] = cut
            level = cut['child'][0]
            vertex_populations[vertex] = {
                i for i, t in enumerate(tiles)
                if tree * t[1] >= level
                and budgets[tree].node(t[0], level) == tuple(cut['child'])}
            if cut['M']:
                demand[vertex] = cut['area_residual']
    for i, (q, h, j, s) in enumerate(tiles):
        if i in matched:
            continue
        nodes = {}
        for tree, budget in budgets.items():
            short = budget.node(q, tree * h)
            long = budget.node(g.vertices(tiles[i])[-1], tree * (h + s))
            child = short if short[0] > long[0] else long
            tau = 1 if child == short else -1
            assert tau == -tree * s
            nodes[tree] = (tree, *child)
        graph_edges.append((nodes[1], nodes[-1]))
        charge_flows.append(-s * eps(tiles[i]))
        alternating_charge_flows.append(eps(tiles[i]))
        physical_flows.append(F(3, g.a * g.b) * (-s) *
                              det(sub(centroids[i], centre), sub(polys[i][0], polys[i][-1])))
    divergence = Counter()
    for (u, v), f in zip(graph_edges, physical_flows):
        divergence[u] += f
        divergence[v] -= f
    assert set(demand) == set(divergence)
    assert all(divergence[u] == demand[u] for u in demand)
    charge_divergence = Counter()
    alternating_divergence = Counter()
    for (u, v), f, fstar in zip(graph_edges, charge_flows, alternating_charge_flows):
        assert abs(f) == abs(fstar) == 1
        charge_divergence[u] += f
        charge_divergence[v] -= f
        alternating_divergence[u] += fstar
        alternating_divergence[v] -= fstar
    for vertex, cut in records.items():
        assert charge_divergence[vertex] == cut['P'] - cut['Q']
        assert alternating_divergence[vertex] == vertex[0] * (cut['P'] + cut['Q'])
    energy, potentials, components = electrical_energy(graph_edges, demand)
    physical_energy = sum(f * f for f in physical_flows)
    Kactual = tree_reports[0]['actual_bank_inertia_bound']
    Kmatched = tree_reports[0]['pair_reserve_bound']
    assert energy <= physical_energy <= Kactual <= Kmatched
    # A gradient is orthogonal to every circulation. This exactly verifies
    # the claimed minimum energy without relying on a solver status.
    optimum = [potentials[u] - potentials[v] for u, v in graph_edges]
    difference_energy = sum((f - p) ** 2 for f, p in zip(physical_flows, optimum))
    assert physical_energy == energy + difference_energy
    alpha = {v: charge_divergence[v] for v in demand}
    beta = {v: alternating_divergence[v] for v in demand}
    alpha_energy, alpha_potential, _ = electrical_energy(graph_edges, alpha)
    beta_energy, beta_potential, _ = electrical_energy(graph_edges, beta)
    alpha_optimum = [alpha_potential[u] - alpha_potential[v] for u, v in graph_edges]
    beta_optimum = [beta_potential[u] - beta_potential[v] for u, v in graph_edges]
    M = len(graph_edges)
    assert alpha_energy <= M and beta_energy <= M
    assert M == alpha_energy + sum((q - p) ** 2 for q, p in zip(charge_flows, alpha_optimum))
    assert M == beta_energy + sum((q - p) ** 2 for q, p in zip(alternating_charge_flows, beta_optimum))
    gram_cross = sum(p * q for p, q in zip(alpha_optimum, beta_optimum))
    hand_sum = sum(q * r for q, r in zip(charge_flows, alternating_charge_flows))
    assert (M - alpha_energy) * (M - beta_energy) >= (hand_sum - gram_cross) ** 2
    for report in tree_reports:
        assert report['quadratic_cost'] <= energy
    # A band k consists of increasing roots at k and decreasing roots at k-1.
    # Its child-subtree populations really partition the physical tiles.
    # Include zero-degree cuts here instead of hiding paired-only crossings.
    band_vertices = defaultdict(set)
    for vertex, cut in records.items():
        band = cut['root_height'] + (vertex[0] == -1)
        band_vertices[band].add(vertex)
    bands = []
    for band, all_vertices in sorted(band_vertices.items()):
        counts = Counter(i for vertex in all_vertices for i in vertex_populations[vertex])
        assert set(counts) == set(range(g.N)) and all(v == 1 for v in counts.values())
        assert sum(records[v]['subtree_tiles'] for v in all_vertices) == g.N
        assert sum(records[v]['exterior_side_count'] for v in all_vertices) == 3
        active = {v for v in all_vertices if records[v]['M']}
        band_components = [set(comp) for comp in components if set(comp) & active]
        assert all(comp <= active for comp in band_components)
        if active:
            assert len(band_components) == 1 and band_components[0] == active
            assert sum(records[v]['subtree_tiles'] for v in active) == g.N
            assert sum(records[v]['exterior_side_count'] for v in active) == 3
            assert all(records[v]['subtree_tiles'] == 0 for v in all_vertices - active)
        else:
            assert sorted(records[v]['subtree_tiles'] for v in all_vertices if records[v]['subtree_tiles']) == [g.N]
        bands.append({'upper_height': band, 'vertices': len(all_vertices),
                      'active_vertices': len(active), 'components': len(band_components),
                      'physical_population_partition': 'PASS'})
    # Test the graph-cut consequence at every subset of these small controls.
    vertices = sorted(demand)
    for mask in range(1 << len(vertices)):
        subset = {u for k, u in enumerate(vertices) if mask >> k & 1}
        qsum = sum(demand[u] for u in subset)
        crossing = sum((u in subset) != (v in subset) for u, v in graph_edges)
        assert qsum * qsum <= crossing * energy
        alpha = sum(charge_divergence[u] for u in subset)
        beta = sum(alternating_divergence[u] for u in subset)
        assert max(abs(alpha), abs(beta)) <= crossing
        assert (crossing - alpha) % 2 == (crossing - beta) % 2 == 0
        selected_bands = {records[u]['root_height'] + (u[0] == -1) for u in subset}
        if len(selected_bands) == 1:
            band = next(iter(selected_bands))
            union = set().union(*(vertex_populations[u] for u in subset))
            assert len(union) == sum(records[u]['subtree_tiles'] for u in subset)
            G = sum(eps(tiles[i]) for i in union)
            Gstar = sum((-1 if tiles[i][1] % 2 else 1) * eps(tiles[i]) for i in union)
            exterior = sum(g.c * (records[u]['P'] - records[u]['Q'])
                           - (g.c - g.a + g.b) * records[u]['G'] for u in subset)
            assert g.c * alpha == (g.c - g.a + g.b) * G + exterior
            assert g.c * beta == (-1 if band % 2 else 1) * ((g.c + g.a - g.b) * Gstar - exterior)
    return {'vertices': len(demand), 'physical_tile_edges': len(graph_edges),
            'connected_components': len(components),
            'component_demand_sums': [sum(demand[u] for u in comp) for comp in components],
            'minimum_flow_energy': energy, 'physical_flow_energy': physical_energy,
            'pair_reserve_bound': Kmatched,
            'divergence_from_real_tile_centroids': 'PASS',
            'orthogonal_flow_decomposition': 'PASS',
            'all_graph_cut_inequalities': 'PASS',
            'both_unit_charge_flows': 'PASS',
            'unit_charge_minimum_energies': [alpha_energy, beta_energy],
            'unit_charge_tile_budget': M,
            'joint_charge_gram_bound': 'PASS',
            'all_charge_cut_capacities_and_parities': 'PASS',
            'active_band_connectivity_and_population_partitions': bands}


def joint_algebra_control():
    # Abstract K_2,2, not a geometric tiling: keeping the joint incidences can
    # be strictly stronger than either separate degree budget.
    edges = [(0, 2), (0, 3), (1, 2), (1, 3)]
    demands = {0: 1, 1: -1, 2: 1, 3: -1}
    energy, _, _ = electrical_energy(edges, demands)
    separate = F(1 * 1, 2) + F((-1) ** 2, 2)
    assert energy == 2 and separate == 1
    return {'scope': 'Exact abstract graph algebra control, not a tiling.',
            'separate_tree_energy_bounds': [separate, separate],
            'joint_minimum_energy': energy}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=HERE / 'CONTACT_BUDGET_REPLAY.json')
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    results = {}
    for which in ('known', 'macro'):
        g = Geometry(5, 3, 7)
        tiles, source = read_tiles(g, which)
        polys, centroids, centre, inertia, sdiff = check_full_tiling(g, tiles)
        matched, pairs = long_pairs(g, tiles, polys, centroids, centre)
        tree_reports = [check_tree(g, tiles, polys, centroids, centre, inertia, sdiff, matched, tree)
                        for tree in (1, -1)]
        joint = check_joint_graph(g, tiles, polys, centroids, centre, matched, tree_reports)
        results[which] = {'source': source, 'complete_positive_tiling': 'PASS',
                          'tiles': g.N, 'centroid_inertia': inertia,
                          'matched_pairs': len(pairs),
                          'trees': tree_reports, 'joint_graph': joint}
    constants = []
    for a, b, c in ((33, 7, 37), (35, 13, 43)):
        N = (a + 2 * b) * (2 * a + b)
        A, B = b * (2 * a + b), a * (a + 2 * b)
        S = A * A + B * B + c ** 4 - a * a - b * b - c * c
        constants.append({'tile': [a, b, c], 'N': N, 'odd_charge': -c,
                          'S_board_minus_S_tile': S,
                          'pair_centroid_reserve_parameter': a * a + b * b - a * b,
                          'K_base': F(c * c * N * S, 3 * a * a * b * b),
                          'target_status': 'OPEN'})
    report = json_exact({'status': 'PASS', 'controls': results, 'target_constants': constants,
                         'joint_graph_algebra_control': joint_algebra_control(),
                         'full_3431_excluded': False, 'full_5063_excluded': False,
                         'scope': 'Exact geometric controls for a theorem valid at every odd population. No target feasibility decision.'})
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'controls': {k: {'tiles': v['tiles'], 'matched_pairs': v['matched_pairs'],
                                                     'quadratic_costs': [t['quadratic_cost'] for t in v['trees']]}
                                                    for k, v in report['controls'].items()},
                      'target_constants': report['target_constants'],
                      'full_3431_excluded': False, 'full_5063_excluded': False}, indent=2))


if __name__ == '__main__':
    main()
