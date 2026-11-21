#!/usr/bin/env python3
"""Exact limits of joint charge/contact/moment bounds on known inventories.

The inputs are the previously published abstract axis inventories, not tilings.
No coordinate gluing, phase-compatible anchors, containment, nonoverlap, or
coverage is inferred from a successful check. Standard library only.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


def add(v, w):
    return tuple(x+y for x, y in zip(v, w))


def scale(t, v):
    return tuple(t*x for x in v)


def mul(v, w):
    x, y = v
    u, z = w
    return x*u-y*z, x*z+y*u+y*z


def dot(v, w):
    return v[0]*w[0]+v[1]*w[1]+F(v[0]*w[1]+v[1]*w[0], 2)


def det(v, w):
    return v[0]*w[1]-v[1]*w[0]


def outer(v):
    return [[v[i]*v[j] for j in range(2)] for i in range(2)]


def madd(A, B, t=1):
    return [[A[i][j]+t*B[i][j] for j in range(2)] for i in range(2)]


def mscale(t, A):
    return [[t*A[i][j] for j in range(2)] for i in range(2)]


def mv(A, v):
    return tuple(sum(A[i][j]*v[j] for j in range(2)) for i in range(2))


def inv(A):
    d = A[0][0]*A[1][1]-A[0][1]*A[1][0]
    assert d
    return [[A[1][1]/d, -A[0][1]/d],
            [-A[1][0]/d, A[0][0]/d]]


def trace_metric(A):
    return A[0][0]+A[1][1]+A[0][1]


def psd(A):
    return A[0][0] >= 0 and A[1][1] >= 0 and det(A[0], A[1]) >= 0


U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
ZERO = [[F(0), F(0)], [F(0), F(0)]]
QI = [[F(4, 3), F(-2, 3)], [F(-2, 3), F(4, 3)]]


def template(a, b, c, h, j, s):
    assert h in (0, 1)
    z = (F(a, c), F(b, c)) if h else (F(1), F(0))
    v, w = mul(z, U[j]), mul(z, U[(j+s) % 6])
    av, bw = scale(a, v), scale(b, w)
    lv = scale(-s, add(av, bw))
    assert dot(lv, lv) == c*c
    cov = mscale(F(1, 36), madd(madd(outer(av), outer(bw)), outer(lv)))
    delta = scale(F(1, 6), add(av, scale(-1, bw)))
    assert dot(delta, delta) == F(a*a+b*b-a*b, 36)
    return lv, cov, delta


def inventory(a, b, c, k, detail=False):
    d = a-b
    A, B = b*(2*a+b), a*(a+2*b)
    N = (a+2*b)*(2*a+b)
    assert c*c == a*a+a*b+b*b
    t, m = (k-3)*c//2, (N-k*c-d)//2
    assert k >= 3 and k % 2 and (N-k*c-d) % 2 == 0 and min(t, m) >= 0
    rows = [(0, 0, 1, m), (0, 3, 1, m), (0, 3, 1, d),
            (1, 0, -1, c+t), (1, 3, -1, t),
            (1, 4, -1, c), (1, 4, 1, c)]
    assert sum(r[3] for r in rows) == N
    G0 = sum(s*((-1)**j)*count for h, j, s, count in rows if h == 0)
    G1 = sum(s*((-1)**j)*count for h, j, s, count in rows if h == 1)
    assert (G0, G1) == (-d, -c)
    M1, M2 = 2*c+d, c
    M = M1+M2
    assert 2*(m+t)+M == N
    # Two connected bands. Each has two vertices joined by parallel edges.
    demand = (F(3*k*c-N-2*c+d), F(c-N))
    alpha, beta = (F(d-2*c), F(-c)), (F(-M1), F(c))
    graph_energy = lambda x, y: x[0]*y[0]/M1+x[1]*y[1]/M2
    ea, eb, cross = graph_energy(alpha, alpha), graph_energy(beta, beta), graph_energy(alpha, beta)
    correlation = c-d
    assert eb == M and cross == correlation
    assert M-ea == F(8*c*d, 2*c+d)
    assert ea <= M
    # Thus the full two-by-two difference of the charge-flow energy matrices
    # is diag(8cd/(2c+d), 0), and is positive semidefinite for every u,v.
    Fenergy = graph_energy(demand, demand)
    SB, ST, D = A*A+B*B+c**4, a*a+b*b+c*c, a*a+b*b-a*b
    K = F(c*c, 3*a*a*b*b)*(N*(SB-ST)-(N-M)*D)
    assert Fenergy <= K
    W = (F(A), F(-B))
    assert dot(W, W) == c**4
    centered = [[F(M1)-F(c*c, N), -F(c*c, N)],
                [-F(c*c, N), F(M2)-F(c*c, N)]]
    centered_inv = inv(centered)
    Fc = mv(centered_inv, demand)
    centered_energy = sum(x*y for x, y in zip(demand, Fc))
    assert centered_energy >= Fenergy and centered_energy <= K
    # Full directional covariance of the abstract orientation inventory.
    CB = mscale(F(1, 36), madd(madd(outer((A, 0)), outer((-A, B))), outer((0, -B))))
    CT = [r[:] for r in ZERO]
    for h, j, s, count in rows:
        CT = madd(CT, template(a, b, c, h, j, s)[1], count)
    paired_delta = madd(mscale(2*m, outer(template(a, b, c, 0, 0, 1)[2])),
                        mscale(2*t, outer(template(a, b, c, 1, 0, -1)[2])))
    SM = madd(madd(mscale(N, CB), CT, -1), paired_delta, -1)
    R = F(N*(SB-ST)-(N-M)*D, 36)
    assert trace_metric(SM) == R and psd(SM)
    # Rational minimum-norm reduced centroids satisfying the two area rows
    # and the zero global mean. All paired tiles receive the same midpoint.
    Gram = mscale(F(4*c*c, 3), centered)
    rhs = scale(F(a*b, 3), demand)
    lam = mv(inv(Gram), rhs)
    JW = (W[1], -W[0])
    row_mean = scale((lam[0]+lam[1])/N, JW)
    pair_x = mv(QI, scale(-1, row_mean))
    C0 = mscale(N-M, outer(pair_x))
    mean = scale(N-M, pair_x)
    row_value = [F(0), F(0)]
    # (height, rotation, hand, multiplicity, band index)
    unpaired = [(0, 3, 1, d, 0), (1, 0, -1, c, 0),
                (1, 4, -1, c, 0), (1, 4, 1, c, 1)]
    centers = []
    for h, j, s, count, band in unpaired:
        lv = template(a, b, c, h, j, s)[0]
        rr = scale(-s, (lv[1], -lv[0]))
        x = mv(QI, add(scale(lam[band], rr), scale(-1, row_mean)))
        C0 = madd(C0, outer(x), count)
        mean = add(mean, scale(count, x))
        row_value[band] += count*sum(rr[i]*x[i] for i in range(2))
        centers.append({'h': h, 'j': j, 's': s, 'count': count,
                        'band': band+1, 'reduced_centroid_from_board_center': x})
    assert mean == (0, 0) and tuple(row_value) == rhs
    assert trace_metric(C0) == F(a*a*b*b, 12*c*c)*centered_energy
    residual = madd(SM, C0, -1)
    assert psd(residual)
    # Four matched pairs suffice to add any PSD residual covariance through
    # symmetric displacements +/-u,+/-v of their shared reduced midpoints.
    # These shifts preserve every area row and the global mean. This proves
    # feasibility of all global covariance inequalities, not local placement.
    assert m+t >= 4
    for mass, aa, bb in ((M1, alpha[0], beta[0]), (M2, alpha[1], beta[1])):
        assert max(abs(aa), abs(bb)) <= mass
        assert (mass-aa) % 2 == (mass-bb) % 2 == 0
    out = {'N': N, 'tile': [a,b,c], 'odd_blocks': k,
           'odd_tiles': k*c, 'paired_tiles': N-M, 'unmatched_tiles': M,
           'band_edge_multiplicities': [M1, M2],
           'area_demands_at_increasing_vertices': demand,
           'alpha_energy': ea, 'beta_energy': eb,
           'charge_cross_energy': cross, 'actual_unit_flow_correlation': correlation,
           'area_energy': Fenergy, 'centered_area_energy': centered_energy,
           'area_energy_budget': K,
           'centered_energy_fraction_of_budget': centered_energy/K,
           'covariance_completion_positive_semidefinite': True,
           'all_charge_cut_bounds_and_parities': True,
           'active_band_components': [1,1]}
    if detail:
        out.update({'reduced_centroid_covariance': SM,
                    'minimum_norm_centroid_covariance': C0,
                    'remaining_covariance': residual,
                    'remaining_covariance_determinant': det(residual[0], residual[1]),
                    'unmatched_centroid_groups': centers,
                    'common_reduced_paired_centroid': pair_x})
    return out


def exact(value):
    if isinstance(value, F):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        return {str(k): exact(v) for k,v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(v) for v in value]
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, default=Path(__file__).with_name('ABSTRACT_JOINT_GRAPH_REPLAY.json'))
    args = ap.parse_args()
    if not __debug__:
        raise RuntimeError('Run without -O.')
    selected = [inventory(33,7,37,15,True), inventory(35,13,43,17,True), inventory(5,3,7,15,True)]
    ranges = []
    for a,b,c in [(33,7,37), (35,13,43)]:
        N, d = (a+2*b)*(2*a+b), a-b
        cases = [inventory(a,b,c,k) for k in range(3,(N-d)//c+1,2)]
        ranges.append({'N':N, 'odd_block_values': [r['odd_blocks'] for r in cases],
                       'checked_inventories':len(cases),
                       'all_joint_graph_charge_and_area_bounds_pass':True,
                       'all_directional_covariance_completions_pass':True,
                       'largest_centered_budget_fraction':max(r['centered_energy_fraction_of_budget'] for r in cases),
                       'scope':'Some inventories fail other already known constraints. This range tests only the specified joint-graph/moment projection.'})
    report = {'scope':'Exact abstract inventories and global-moment feasibility only; no geometric tiling, common-contact realization, or nonoverlap certificate.',
              'selected_existing_axis_inventories':selected, 'finite_odd_population_ranges':ranges,
              'hard_body_realization_claimed':False}
    args.out.write_text(json.dumps(exact(report), indent=2)+'\n')
    print(json.dumps(exact({k:v for k,v in report.items() if k != 'selected_existing_axis_inventories'}), indent=2))
    for r in selected:
        print(json.dumps(exact({k:r[k] for k in ('N','odd_tiles','unmatched_tiles','area_energy','centered_area_energy','area_energy_budget','centered_energy_fraction_of_budget')})))


if __name__ == '__main__':
    main()
