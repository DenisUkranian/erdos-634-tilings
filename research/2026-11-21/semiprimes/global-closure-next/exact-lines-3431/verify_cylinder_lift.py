#!/usr/bin/env python3
"""Exact finite lift from the torus to all actual supporting-line cylinders.

No LP/MIP optimizer is used.  A three-direction convolution induces the
identity A_cylinder L = E A_torus, preserves every residue-column mass,
and places its entire support strictly inside the board.  The existing
exact rational torus population-111 certificate is independently replayed here.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
A, B, C = 33, 7, 37
U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
SHIFT = (800, -36)
BOARD = ((0, 0), (C*C*(A+B), -C*C*B), (A*A*(A+2*B), A*B*(A+2*B)))


def check(ok, message):
    if not ok:
        raise ArithmeticError(message)


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def transverse(axis, p):
    return (p[1], p[0], p[0]+p[1])[axis]


def cylinder_row(axis, p):
    axis %= 3
    return axis, transverse(axis, p), (p[0] if axis == 0 else p[1]) % C


def short_rows(q, j, s):
    u = q[0]-A*U[j][0], q[1]-A*U[j][1]
    k = (j+s) % 6
    w = q[0]+B*U[k][0], q[1]+B*U[k][1]
    return ((j % 3, q, s), (j % 3, u, -s),
            (k % 3, w, s), (k % 3, q, -s))


def gate(q, j, s):
    u = q[0]-A*U[j][0], q[1]-A*U[j][1]
    return ((A*u[1]-B*u[0]) if s > 0 else
            (A*u[0]-B*u[1])) % C


def idx(x, y, j, s):
    return ((x*C+y)*6+j)*2+(s == 1)


def averaged_packing(multiplicity):
    """Exact contained translates and an explicit convex packing decomposition."""
    centre = SHIFT[0], SHIFT[1]+C-1
    radius = C-1+A
    hull = [(centre[0]+radius*x, centre[1]+radius*y) for x, y in U]
    for q in multiplicity:
        dx, dy = q[0]-centre[0], q[1]-centre[1]
        check(max(abs(dx), abs(dy), abs(dx+dy)) <= C-1, 'Anchor hexagon')
    # Every tile vertex differs from its anchor by 0, -a*U_j, or b*U_k.
    # Thus the radius-(c-1+a) hexagon contains all twelve orientations.
    check(A > B, 'Hull radius uses max(a,b)')
    # Every possible translation must put its centre inside the board.
    xmin = -((-min(x for x, y in BOARD))//C)
    xmax = max(x for x, y in BOARD)//C
    ymin = -((-min(y for x, y in BOARD))//C)
    ymax = max(y for x, y in BOARD)//C
    umin = -((-(xmin-centre[0]))//C)
    umax = (xmax-centre[0])//C
    vmin = -((-(ymin-centre[1]))//C)
    vmax = (ymax-centre[1])//C
    translations = []
    minimum = None
    for u in range(umin, umax+1):
        for v in range(vmin, vmax+1):
            vals = [det(BOARD[i], BOARD[(i+1) % 3],
                        (C*(q[0]+C*u), C*(q[1]+C*v)))
                    for q in hull for i in range(3)]
            if min(vals) >= 0:
                check(min(vals) > 0, 'All accepted translates should be strict')
                translations.append((u, v))
                minimum = min(vals) if minimum is None else min(minimum, *vals)
    count = len(translations)
    check(count == 133 and count > 111, 'Expected sufficient contained translates')
    averaged = Counter()
    for u, v in translations:
        for q, m in multiplicity.items():
            averaged[q[0]+C*u, q[1]+C*v] += m
    # For a fixed resulting q, the preimages q-c*t are distinct points
    # in the same residue. Their original multiplicities sum to at most c.
    check(min(averaged.values()) >= 1 and max(averaged.values()) <= C,
          'Translation averaging coefficient bound')
    residues = defaultdict(Counter)
    anchors_byres = defaultdict(list)
    for q, m in averaged.items():
        residues[q[0] % C, q[1] % C][m] += 1
        anchors_byres[q[0] % C, q[1] % C].append((q, m))
    check(len(residues) == C*C, 'Averaged residue coverage')
    cardinalities = []
    for r, histogram in residues.items():
        check(sum(m*n for m, n in histogram.items()) == C*count,
              'Averaged residue mass')
        for k in range(1, C+1):
            cardinalities.append(sum(n for m, n in histogram.items() if m >= k))
    # A second, stronger decomposition has exactly 111 tiles in EVERY
    # component.  Conditional on a residue/orientation class, desired
    # marginals are 111*m(q)/(c*count), all below one and summing to 111.
    # Integer intervals of those lengths give a direct finite realization.
    D = C*count
    exact_cardinality_cases = 0
    min_support = min(len(v) for v in anchors_byres.values())
    for r, anchors in anchors_byres.items():
        differences = [0]*(D+1)
        start = 0
        for q, m in sorted(anchors):
            width = 111*m
            check(0 < width < D, 'Cardinality interval must be shorter than period')
            left = start % D
            right = left+width
            if right <= D:
                differences[left] += 1
                differences[right] -= 1
            else:
                differences[left] += 1
                differences[D] -= 1
                differences[0] += 1
                differences[right-D] -= 1
            start += width
        check(start == 111*D, 'Cardinality intervals total 111 periods')
        selected = 0
        for t in range(D):
            selected += differences[t]
            check(selected == 111, 'Every sampling offset must select 111 distinct anchors')
            exact_cardinality_cases += 1
    check(exact_cardinality_cases == C*C*D, 'Conditional exact-cardinality case count')
    # All triangles in a fixed (residue,orientation,hand) family differ
    # by a nonzero cR vector. Such vectors have squared norm >= c^2,
    # while every two interior points of a tile are closer than c.
    for j in range(6):
        for s in (-1, 1):
            p = ((0, 0), (-A*U[j][0], -A*U[j][1]),
                 (B*U[(j+s) % 6][0], B*U[(j+s) % 6][1]))
            norms = []
            for i in range(3):
                dx = p[i][0]-p[(i+1) % 3][0]
                dy = p[i][1]-p[(i+1) % 3][1]
                norms.append(dx*dx+dx*dy+dy*dy)
            check(sorted(norms) == sorted((A*A, B*B, C*C)), 'Tile diameter')
    return {
        'convex_hull_centre': list(centre), 'convex_hull_radius': radius,
        'translation_search_box': [umin, umax, vmin, vmax],
        'number_of_strictly_contained_translations': count,
        'translations_in_units_of_cR': [list(t) for t in translations],
        'minimum_translated_hull_determinant': minimum,
        'distinct_averaged_anchors': len(averaged),
        'supported_placed_columns': 12*len(averaged),
        'maximum_averaged_multiplicity': max(averaged.values()),
        'lift_coefficient_denominator': C*count,
        'coefficient_upper_bound': f'1/{count}',
        'global_pointwise_density_upper_bound': f'111/{count}',
        'all_fractional_point_packing_inequalities': 'SATISFIED STRICTLY',
        'all_fractional_conflict_clique_inequalities': 'SATISFIED STRICTLY',
        'convex_decomposition': {
            'nonempty_component_recipe': 'For each residue r, orientation j,s, and k=1,...,c, take every anchor q congruent to r with averaged multiplicity >=k.',
            'nonempty_component_count_with_repetitions': 12*C**3,
            'component_weight': f'x_star[r,j,s]/{C*count}',
            'empty_component_weight': f'{count-111}/{count}',
            'smallest_component_tile_count': min(cardinalities),
            'largest_component_tile_count': max(cardinalities),
            'each_component': 'An integral nonoverlapping partial packing, strictly contained in the board.',
            'scope': 'The cylinder, gate, and population equations hold in the mixture; they are not asserted for each integral component.'},
        'exact111_convex_decomposition': {
            'conditional_period': D,
            'conditional_interval_width': '111 times the averaged multiplicity of the anchor',
            'maximum_interval_width': 111*max(averaged.values()),
            'conditional_total_interval_length': 111*D,
            'minimum_anchors_per_residue': min_support,
            'residue_sampling_offsets_checked': exact_cardinality_cases,
            'component_count_with_repetitions': 12*C*C*D,
            'every_component_tile_count': 111,
            'component_weight': f'x_star[r,j,s]/{111*D}',
            'component_recipe': 'Order anchors of a residue lexicographically; partition [0,111D) into integer intervals of lengths 111*mbar(q). For sampling offset t=0,...,D-1, select every interval containing an integer congruent to t modulo D.',
            'each_component': 'A contained integral nonoverlapping partial packing of exactly 111 height-one tiles, all of one orientation and one sign.',
            'preserved_only_in_the_mixture': ['positive population 74 and negative population 37', 'specified signed gate currents', 'cylinder endpoint equations'],
            'conclusion': 'The averaged cylinder point lies in the convex hull of contained integral nonoverlapping partial packings of exactly 111 tiles. No single component has the required complete charge/current profile.'}
    }


def verify():
    # Multiplicity m(q) of q=t+X*U0+Y*U1+K*U2.
    multiplicity = Counter()
    for X in range(C):
        for Y in range(C):
            for K in range(C):
                multiplicity[SHIFT[0]+X-K, SHIFT[1]+Y+K] += 1
    check(len(multiplicity) == 3*C*(C-1)+1, 'Hexagon support size')
    check(sum(multiplicity.values()) == C**3, 'Convolution mass')
    byres = defaultdict(list)
    for q, m in sorted(multiplicity.items()):
        check(1 <= m <= C, 'Convolution coefficient')
        byres[q[0] % C, q[1] % C].append((q, m))
    check(len(byres) == C*C, 'Every residue must occur')
    for r, lifts in byres.items():
        check(sum(m for q, m in lifts) == C, 'Residue mass normalization')

    # L_i(tau) counts the two convolution parameters transverse to axis i.
    # The remaining uniform parameter provides exactly one representative
    # of every longitudinal residue, independently of the other two.
    line_mass = [Counter(), Counter(), Counter()]
    for V in range(C):
        for W in range(C):
            line_mass[0][SHIFT[1]+V+W] += 1
            line_mass[1][SHIFT[0]+V-W] += 1
            line_mass[2][SHIFT[0]+SHIFT[1]+V+W] += 1
    marginal_checks = 0
    for r, lifts in byres.items():
        for axis in range(3):
            actual = Counter()
            for q, m in lifts:
                actual[transverse(axis, q)] += m
            expected = {tau: count for tau, count in line_mass[axis].items()
                        if tau % C == transverse(axis, r) % C}
            check(actual == expected, 'Longitudinal residue independence')
            marginal_checks += 1

    def expand_torus_row(axis, p, sign, out):
        transverse_residue = transverse(axis, p) % C
        longitudinal_residue = (p[0] if axis == 0 else p[1]) % C
        for tau, mass in line_mass[axis].items():
            if tau % C == transverse_residue:
                out[axis, tau, longitudinal_residue] += sign*mass

    minimum_det = None
    columns = placements = 0
    # One generic strictly interior point for an explicit packing cut.
    point_den = 101*103
    probe = (800*point_den+103, 101)
    probe_weights = [0]*(12*C*C)
    for x in range(C):
        for y in range(C):
            for j in range(6):
                for s in (-1, 1):
                    lhs, rhs = Counter(), Counter()
                    r = x, y
                    for axis, p, sign in short_rows(r, j, s):
                        expand_torus_row(axis, p, sign, rhs)
                    for q, m in byres[r]:
                        check(gate(q, j, s) == gate(r, j, s), 'Gate preservation')
                        for axis, p, sign in short_rows(q, j, s):
                            lhs[cylinder_row(axis, p)] += m*sign
                        u = q[0]-A*U[j][0], q[1]-A*U[j][1]
                        k = (j+s) % 6
                        w = q[0]+B*U[k][0], q[1]+B*U[k][1]
                        poly = [u, q, w] if s > 0 else [w, q, u]
                        check(det(*poly) == A*B, 'Tile area/orientation')
                        for p in poly:
                            for i in range(3):
                                value = det(BOARD[i], BOARD[(i+1) % 3],
                                            (C*p[0], C*p[1]))
                                check(value > 0, 'Strict containment')
                                minimum_det = value if minimum_det is None else min(minimum_det, value)
                        scaled = [(point_den*p[0], point_den*p[1]) for p in poly]
                        determinants = [det(scaled[i], scaled[(i+1) % 3], probe)
                                        for i in range(3)]
                        check(all(value != 0 for value in determinants), 'Probe is on an edge')
                        if all(value > 0 for value in determinants):
                            probe_weights[idx(x, y, j, s)] += m
                        placements += 1
                    check(not any((lhs-rhs).values()) and not any((rhs-lhs).values()),
                          'Cylinder/toroidal operator identity')
                    columns += 1
    check(columns == 12*C*C and placements == 12*len(multiplicity), 'Column count')

    source_dir = HERE.parent.parent/'global-invariant'
    cert_path = source_dir/'N3431_RATIONAL_PROJECTION_CERTIFICATE.json'
    checker_path = source_dir/'verify_3431_rational_projection.py'
    spec = importlib.util.spec_from_file_location('exact_torus_projection', checker_path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    cert = json.loads(cert_path.read_text())
    check(cert['tile'] == [A, B, C] and cert['target_population'] == 3*C, 'Source target')
    check(cert['native_gate_currents'] == [22, 15], 'Source gate profile')
    K, hist = old.inverse_bound(cert)
    point_report = old.point_checks(cert, K)
    denominator = cert['point_denominator']
    vals = [cert['uniform_point_numerator']]*(12*C*C)
    for x, y, j, s, inc in cert['point_increments']:
        vals[idx(x, y, j, s)] += inc
    residual2 = point_report['residual_squared_numerator']
    maximum_approx = max(vals)
    check(denominator > maximum_approx, 'Source approximate coordinate below one')
    check((denominator-maximum_approx)**2 > K*residual2,
          'Exact corrected source coordinate below one')
    # Since 0 < m(q)/c <= 1, every nonzero lifted weight is also below one.

    # A concrete valid physical packing constraint violated by this witness.
    # Its exact value need not be expanded: Cauchy--Schwarz plus the same
    # certified correction bound proves it remains above one.
    coverage_num = sum(w*v for w, v in zip(probe_weights, vals))
    coverage_den = C*denominator
    error_squared_num = sum(w*w for w in probe_weights)*K*residual2
    packing_violation = (coverage_num > coverage_den and
                         (coverage_num-coverage_den)**2 > error_squared_num)
    check(packing_violation, 'Expected explicit packing violation was not certified')
    averaging_report = averaged_packing(multiplicity)

    return {
        'checks': 'PASS', 'target_existence_status': 'OPEN',
        'tile': [A, B, C], 'convolution_shift': list(SHIFT),
        'convolution_triples': C**3, 'distinct_anchors': len(multiplicity),
        'strictly_contained_placed_columns': placements,
        'torus_columns_checked': columns,
        'axis_residue_marginals_checked': marginal_checks,
        'lift_common_denominator': C,
        'residue_mass_numerator': C,
        'minimum_nonzero_lift_numerator': min(multiplicity.values()),
        'maximum_lift_numerator': max(multiplicity.values()),
        'minimum_board_halfplane_determinant': minimum_det,
        'operator_identity': 'A_cylinder L = E A_torus, checked column by column over integers',
        'source_certificate_sha256': hashlib.sha256(cert_path.read_bytes()).hexdigest(),
        'source_checker_sha256': hashlib.sha256(checker_path.read_bytes()).hexdigest(),
        'source_certificate_replayed': True,
        'source_fourier_block_histogram': hist,
        'source_point_checks': point_report,
        'exact_lifted_population': 111,
        'exact_lifted_positive_population': 74,
        'exact_lifted_negative_population': 37,
        'gate_currents': {'native_up': 22, 'native_down': 15, 'all_remote': 0},
        'all_placed_variable_bounds': '0 < y < 1 on the support; zero elsewhere',
        'coordinate_upper_bound_check': {
            'maximum_approximate_numerator': maximum_approx,
            'point_denominator': denominator,
            'squared_slack': (denominator-maximum_approx)**2,
            'correction_squared_bound': K*residual2},
        'explicit_packing_cut': {
            'point_in_normalized_coordinates': [str(F(v, point_den)) for v in probe],
            'condition': 'Sum of weights of tiles whose interiors contain this point is at most one in a packing.',
            'approximate_coverage_numerator': coverage_num,
            'coverage_denominator': coverage_den,
            'decimal_for_display_only': coverage_num/coverage_den,
            'squared_excess_numerator': (coverage_num-coverage_den)**2,
            'correction_error_squared_numerator': error_squared_num,
            'strict_violation_for_exact_witness': packing_violation,
            'scope': 'This eliminates this explicit fractional lift, not every feasible cylinder point or every tiling.'},
        'averaged_fractional_packing': averaging_report,
        'conclusion': 'The full contained native-height-one cylinder relaxation has an exact rational population-111 point, including positive gate caps and y<=1. Averaging 133 contained cR translates gives another such point in the convex hull of integral nonoverlapping partial packings of exactly 111 tiles and satisfies every valid linear inequality for those packings. The required sign populations, gate currents and cylinder equations hold only in the mixture. No single integral packing with that complete profile, no physical endpoint closure, and no tiling are certified.'
    }


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O; the imported exact source verifier uses asserts.')
    report = verify()
    text = json.dumps(report, indent=2)+'\n'
    (HERE/'CYLINDER_LIFT_REPLAY.json').write_text(text)
    print(text, end='')
