#!/usr/bin/env python3
"""Exact cylinder lift and fixed-cardinality packing hull at native n1=215.

Standard library only. Replays the rational torus certificate, checks a
finite convolution identity, and constructs a rational point in the
convex hull of contained integral nonoverlapping partial packings of
exactly 215 tiles. The required signs, gate currents, and cylinder
equations are imposed only on the mixture, not on any one component.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
A, B, C, N = 35, 13, 43, 215
CENTRE = (1000, 0)
SHIFT = (CENTRE[0], CENTRE[1]-(C-1))
U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
BOARD = ((0, 0), (C*C*(A+B), -C*C*B),
         (A*A*(A+2*B), A*B*(A+2*B)))


def check(ok, message):
    if not ok:
        raise ArithmeticError(message)


def det(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])


def ceildiv(x, y):
    return -((-x)//y)


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
    ux, uy = q[0]-A*U[j][0], q[1]-A*U[j][1]
    return ((A*uy-B*ux) if s > 0 else (A*ux-B*uy)) % C


def source_certificate():
    folder = HERE.parent.parent/'five-block-two-heights'
    path = folder/'N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz'
    verifier = folder/'verify_native_215_projection.py'
    compressed = path.read_bytes()
    check(compressed[4:8] == b'\0\0\0\0', 'Deterministic gzip timestamp')
    cert = json.loads(gzip.decompress(compressed))
    check(cert['tile'] == [A, B, C], 'Source tile')
    check(cert['target_population'] == N, 'Source population')
    check(cert['native_gate_currents'] == [42, 1], 'Source gate currents')
    spec = importlib.util.spec_from_file_location('exact_native_215_projection', verifier)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    K, histogram = module.inverse_bound(cert)
    point = module.point_checks(cert, K)
    check(point['exact_corrected_population'] == N, 'Verified population')
    check(point['exact_corrected_positive_population'] == 129, 'Verified positive population')
    check(point['exact_corrected_negative_population'] == 86, 'Verified negative population')
    return {'certificate': str(path.relative_to(ROOT)),
            'certificate_sha256': hashlib.sha256(compressed).hexdigest(),
            'checker_sha256': hashlib.sha256(verifier.read_bytes()).hexdigest(),
            'fourier_checker_sha256': hashlib.sha256(module.FOURIER_SOURCE.read_bytes()).hexdigest(),
            'fourier_blocks': C*C, 'block_histogram': histogram,
            'point_checks': point, 'replayed': True}


def finite_convolution():
    multiplicity = Counter()
    for X in range(C):
        for Y in range(C):
            for K in range(C):
                multiplicity[SHIFT[0]+X-K, SHIFT[1]+Y+K] += 1
    check(len(multiplicity) == 3*C*(C-1)+1, 'Convolution support')
    check(sum(multiplicity.values()) == C**3, 'Convolution total')
    byres = defaultdict(list)
    for q, m in sorted(multiplicity.items()):
        check(0 < m <= C, 'Convolution coefficient')
        dx, dy = q[0]-CENTRE[0], q[1]-CENTRE[1]
        check(max(abs(dx), abs(dy), abs(dx+dy)) <= C-1, 'Anchor hexagon')
        byres[q[0] % C, q[1] % C].append((q, m))
    check(len(byres) == C*C, 'All residues represented')
    for r, lifts in byres.items():
        check(sum(m for q, m in lifts) == C, 'Unit mass in each residue')
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
            expected = {v: m for v, m in line_mass[axis].items()
                        if v % C == transverse(axis, r) % C}
            check(actual == expected, 'Transverse conditional marginal')
            marginal_checks += 1
    minimum = None
    placed = columns = 0
    for x in range(C):
        for y in range(C):
            r = x, y
            for j in range(6):
                for s in (-1, 1):
                    lhs, rhs = Counter(), Counter()
                    for axis, p, sign in short_rows(r, j, s):
                        for v, m in line_mass[axis].items():
                            if v % C == transverse(axis, p) % C:
                                rhs[axis, v, (p[0] if axis == 0 else p[1]) % C] += sign*m
                    for q, m in byres[r]:
                        check(gate(q, j, s) == gate(r, j, s), 'Gate preservation')
                        for axis, p, sign in short_rows(q, j, s):
                            lhs[cylinder_row(axis, p)] += sign*m
                        u = q[0]-A*U[j][0], q[1]-A*U[j][1]
                        w = q[0]+B*U[(j+s) % 6][0], q[1]+B*U[(j+s) % 6][1]
                        polygon = [u, q, w] if s > 0 else [w, q, u]
                        check(det(*polygon) == A*B, 'Tile area')
                        for p in polygon:
                            for i in range(3):
                                value = det(BOARD[i], BOARD[(i+1) % 3], (C*p[0], C*p[1]))
                                check(value > 0, 'Strict containment')
                                minimum = value if minimum is None else min(minimum, value)
                        placed += 1
                    check(not any((lhs-rhs).values()) and not any((rhs-lhs).values()),
                          'A_cylinder L = E A_torus')
                    columns += 1
    check(columns == 12*C*C and placed == 12*len(multiplicity), 'Column counts')
    return multiplicity, {'anchor_count': len(multiplicity),
             'convolution_triples': C**3,
             'axis_residue_marginals_checked': marginal_checks,
             'operator_columns_checked': columns,
             'strictly_contained_placed_columns': placed,
             'minimum_halfplane_determinant': minimum,
             'lift_denominator': C,
             'operator_identity': 'A_cylinder L = E A_torus, checked exactly column by column'}


def translated_packing_hull(multiplicity):
    radius = A+C-1
    hull = [(CENTRE[0]+radius*x, CENTRE[1]+radius*y) for x, y in U]
    xmin, xmax = ceildiv(min(x for x, y in BOARD), C), max(x for x, y in BOARD)//C
    ymin, ymax = ceildiv(min(y for x, y in BOARD), C), max(y for x, y in BOARD)//C
    umin, umax = ceildiv(xmin-CENTRE[0], C), (xmax-CENTRE[0])//C
    vmin, vmax = ceildiv(ymin-CENTRE[1], C), (ymax-CENTRE[1])//C
    translations, minimum = [], None
    for u in range(umin, umax+1):
        for v in range(vmin, vmax+1):
            values = [det(BOARD[i], BOARD[(i+1) % 3],
                          (C*(q[0]+C*u), C*(q[1]+C*v)))
                      for q in hull for i in range(3)]
            if min(values) >= 0:
                check(min(values) > 0, 'All accepted translates are strict')
                translations.append((u, v))
                minimum = min(values) if minimum is None else min(minimum, *values)
    M = len(translations)
    check(M == 410 and M > N, 'Sufficient contained translates')
    averaged = Counter()
    for u, v in translations:
        for q, m in multiplicity.items():
            averaged[q[0]+C*u, q[1]+C*v] += m
    check(0 < min(averaged.values()) <= max(averaged.values()) <= C,
          'Averaged multiplicity bound from distinct same-residue preimages')
    byres = defaultdict(list)
    for q, m in averaged.items():
        byres[q[0] % C, q[1] % C].append((q, m))
    check(len(byres) == C*C, 'Averaged residue classes')
    D = C*M
    offset_cases = 0
    for r, anchors in byres.items():
        check(sum(m for q, m in anchors) == C*M, 'Averaged mass per residue')
        differences = [0]*(D+1)
        start = 0
        for q, m in sorted(anchors):
            width = N*m
            check(0 < width < D, 'One conditional interval cannot wrap twice')
            left, right = start % D, start % D+width
            if right <= D:
                differences[left] += 1
                differences[right] -= 1
            else:
                differences[left] += 1
                differences[D] -= 1
                differences[0] += 1
                differences[right-D] -= 1
            start += width
        check(start == N*D, 'Exact total conditional interval length')
        size = 0
        for t in range(D):
            size += differences[t]
            check(size == N, 'Every offset selects exactly N distinct anchors')
            offset_cases += 1
    check(offset_cases == C*C*D, 'Conditional offset count')
    # A tile has diameter c. Distinct anchors in cR are separated by at
    # least c, as the axial norm of a nonzero integer vector is >=1.
    for j in range(6):
        for s in (-1, 1):
            poly = [(0, 0), (-A*U[j][0], -A*U[j][1]),
                    (B*U[(j+s) % 6][0], B*U[(j+s) % 6][1])]
            norm = []
            for i in range(3):
                dx, dy = poly[i][0]-poly[(i+1) % 3][0], poly[i][1]-poly[(i+1) % 3][1]
                norm.append(dx*dx+dx*dy+dy*dy)
            check(sorted(norm) == sorted((A*A, B*B, C*C)), 'Tile diameter')
    return {'containing_hexagon_centre': list(CENTRE),
            'containing_hexagon_radius': radius,
            'translation_search_box': [umin, umax, vmin, vmax],
            'strictly_contained_translations': M,
            'translations_in_units_of_cR': [list(t) for t in translations],
            'minimum_translated_hull_determinant': minimum,
            'averaged_anchors': len(averaged),
            'averaged_placed_columns': 12*len(averaged),
            'maximum_averaged_multiplicity': max(averaged.values()),
            'lift_denominator': D,
            'global_pointwise_density_bound': str(Fraction(N, M)),
            'conditional_interval_width_bound': N*max(averaged.values()),
            'conditional_total_interval_length': N*D,
            'minimum_available_anchors_per_residue': min(len(v) for v in byres.values()),
            'residue_sampling_offsets_checked': offset_cases,
            'convex_component_count_with_repetitions': 12*C*C*D,
            'every_component_population': N,
            'component_weight': f'x_star[r,j,s]/{N*D}',
            'component_recipe': 'For each residue/orientation, order its supported anchors lexicographically and partition [0,N*D) into integer intervals of lengths N*mbar(q). Select intervals containing an integer congruent to t modulo D, for t=0,...,D-1.',
            'each_component': 'An integral nonoverlapping contained partial packing of exactly 215 native height-one tiles, all of one orientation and one sign.',
            'requirements_preserved_only_in_the_mixture': ['sign populations 129 and 86', 'native gate currents 42 and 1 with zero remote currents', 'cylinder endpoint equations'],
            'scope': 'Convex hull of exact-cardinality partial packings intersected with the required linear equations; no common integral configuration satisfying those equations is asserted.'}


def verify():
    check(A*A+A*B+B*B == C*C, 'Tile equation')
    source = source_certificate()
    multiplicity, convolution = finite_convolution()
    packing = translated_packing_hull(multiplicity)
    return {'checks': 'PASS', 'tile': [A, B, C],
            'full_5063_excluded': False, 'physical_tiling_constructed': False,
            'integer_configuration_with_required_profile_constructed': False,
            'source_exact_certificate': source,
            'convolution_shift': list(SHIFT),
            'finite_cylinder_lift': convolution,
            'averaged_fixed_cardinality_packing_hull': packing,
            'exact_population': N, 'exact_positive_population': 129,
            'exact_negative_population': 86,
            'exact_gate_currents': {'native_up': 42, 'native_down': 1, 'all_remote': 0},
            'positive_gate_capacity': 94,
            'conclusion': 'There is an exact rational native population-215 cylinder point in the convex hull of actual contained integral nonoverlapping partial packings of exactly 215 tiles. All ordinary packing inequalities are satisfied. Sign, gate and cylinder data hold only in the mixture. This is neither an integral solution with the required profile nor a full tiling.'}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O; the imported source verifier uses assertions.')
    report = verify()
    text = json.dumps(report, indent=2)+'\n'
    (HERE/'N5063_CYLINDER_PACKING_REPLAY.json').write_text(text)
    print(text, end='')
