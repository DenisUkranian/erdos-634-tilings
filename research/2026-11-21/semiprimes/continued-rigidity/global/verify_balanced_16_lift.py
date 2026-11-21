#!/usr/bin/env python3
"""Exact disjoint cylinder lift of the 16-tile (35,13,43) kernel.

This is a partial packing, not a tiling.  It checks a counterexample to a
proposed restriction on balanced cylinder kernels, not to the open problem.
Only Python integer arithmetic and the standard library are used.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

U = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
A, B, C = 35, 13, 43
ORIGINAL = (
    (0, 0, 1, -1), (0, 0, 1, 1), (0, 0, 3, -1),
    (26, 0, 2, 1), (35, 0, 2, 1), (18, 8, 5, 1),
    (31, 8, 5, 1), (5, 8, 5, 1), (27, 8, 5, 1),
    (14, 8, 5, 1), (1, 8, 5, 1), (22, 0, 2, 1),
    (39, 0, 2, 1), (9, 0, 2, 1), (5, 8, 5, -1),
    (5, 8, 3, 1),
)
GROUPS = ((0, 1, 2), (3, 5), (4, 8), (6, 12),
          (9, 11), (10, 13), (7, 14, 15))


def vertices(label):
    x, y, j, s = label
    return ((x, y), (x-A*U[j][0], y-A*U[j][1]),
            (x+B*U[(j+s) % 6][0], y+B*U[(j+s) % 6][1]))


def cylinder_row(axis, p):
    axis %= 3
    x, y = p
    if axis == 0:
        return axis, y, x % C
    if axis == 1:
        return axis, x, y % C
    return axis, x+y, y % C


def separating_axis(poly, other):
    """Return an exact separating support direction, including edge contact."""
    for which, triangle in enumerate((poly, other)):
        for k in range(3):
            p, q = triangle[k], triangle[(k+1) % 3]
            dx, dy = q[0]-p[0], q[1]-p[1]
            first = [dx*y-dy*x for x, y in poly]
            second = [dx*y-dy*x for x, y in other]
            if max(first) <= min(second) or max(second) <= min(first):
                return {'triangle': which, 'edge': k, 'direction': [dx, dy],
                        'first_range': [min(first), max(first)],
                        'second_range': [min(second), max(second)]}
    return None


def verify():
    labels = [list(q) for q in ORIGINAL]
    assert sorted(i for group in GROUPS for i in group) == list(range(16))
    for k, group in enumerate(GROUPS):
        for i in group:
            labels[i][0] += 4*C*k
    rows = Counter()
    polygons = []
    signed_a_axes = [0, 0, 0]
    signed_b_axes = [0, 0, 0]
    signs = Counter()
    for label in labels:
        x, y, j, s = label
        eps = s * (-1 if j % 2 else 1)
        signs[eps] += 1
        signed_a_axes[j % 3] += eps
        signed_b_axes[(j+s) % 3] += eps
        q, u, w = vertices(label)
        polygons.append((q, u, w))
        for axis, p, v in ((j, q, s), (j, u, -s),
                           (j+s, w, s), (j+s, q, -s)):
            rows[cylinder_row(axis, p)] += v
    assert signs == {1: 8, -1: 8}
    assert all(v == 0 for v in rows.values())
    separation_witnesses = []
    for i, j in combinations(range(16), 2):
        witness = separating_axis(polygons[i], polygons[j])
        assert witness is not None, (i, j)
        separation_witnesses.append({'pair': [i, j], **witness})
    assert signed_a_axes == signed_b_axes == [0, 0, 0]
    # A more compact lift also lies strictly inside the target board.
    # These are normalized height-one coordinates; physical coordinates are
    # z*(x+y*rho), z=(35+13*rho)/43.  The numerator coordinates below have
    # the common positive denominator 43.
    compact = [list(q) for q in ORIGINAL]
    for k, group in enumerate(GROUPS):
        for i in group:
            compact[i][0] += 3*C*k + 40
            compact[i][1] += 40
    compact_rows = Counter()
    compact_polygons = []
    physical_numerators = []
    margins = []
    board_a, board_b = B*(2*A+B), A*(A+2*B)
    for label in compact:
        x, y, j, s = label
        q, u, w = vertices(label)
        compact_polygons.append((q, u, w))
        physical = []
        for px, py in (q, u, w):
            xx, yy = A*px-B*py, B*px+(A+B)*py
            physical.append((xx, yy))
            # x>0, y>0, x/board_a+y/board_b<1, scaled by C.
            triple = (xx, yy, C*board_a*board_b-board_b*xx-board_a*yy)
            assert min(triple) > 0
            margins.append(triple)
        physical_numerators.append(physical)
        for axis, p, v in ((j, q, s), (j, u, -s),
                           (j+s, w, s), (j+s, q, -s)):
            compact_rows[cylinder_row(axis, p)] += v
    assert all(v == 0 for v in compact_rows.values())
    compact_separations = []
    for i, j in combinations(range(16), 2):
        witness = separating_axis(compact_polygons[i], compact_polygons[j])
        assert witness is not None, (i, j)
        compact_separations.append({'pair': [i, j], **witness})
    return {
        'tile': [A, B, C], 'population': 16, 'positive': 8, 'negative': 8,
        'original_periodic_support': ORIGINAL, 'groups': GROUPS,
        'group_translations': [[4*C*k, 0] for k in range(len(GROUPS))],
        'support': labels, 'vertices': polygons,
        'actual_transverse_cylinder_rows_checked': len(rows),
        'nonzero_cylinder_rows': 0,
        'triangle_pairs_checked': len(separation_witnesses),
        'overlapping_pairs': 0, 'separation_witnesses': separation_witnesses,
        'signed_a_axis_inventory': signed_a_axes,
        'signed_b_axis_inventory': signed_b_axes,
        'strict_board_containment_control': {
            'N': (A+2*B)*(2*A+B),
            'standard_board_vertices': [[0, 0], [board_a, 0], [0, board_b]],
            'height': 1,
            'group_spacing': 3*C,
            'common_normalized_translation': [40, 40],
            'normalized_support': compact,
            'physical_vertex_numerators': physical_numerators,
            'common_physical_denominator': C,
            'minimum_strict_containment_margins':
                [min(v[k] for v in margins) for k in range(3)],
            'margin_definitions': ['43*x', '43*y',
                                   '43*A_board*B_board-43*B_board*x-43*A_board*y'],
            'nonzero_cylinder_rows': 0,
            'overlapping_pairs': 0,
            'separation_witnesses': compact_separations,
        },
        'scope': 'A finite nonoverlapping packing with exact actual-transverse '
                 'cylinder equations. A compact height-one version lies '
                 'strictly inside the target board. It is not a full tiling: '
                 'whole long-edge currents, joint gates, and filling are '
                 'not imposed. It disproves the proposed statement that every '
                 'balanced nonoverlapping cylinder kernel of size below 2c '
                 'has population divisible by six.',
    }


if __name__ == '__main__':
    result = verify()
    out = Path(__file__).with_name('BALANCED_16_NONOVERLAP.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {'original_periodic_support', 'support',
                                   'vertices', 'separation_witnesses',
                                   'strict_board_containment_control'}}, indent=2))
