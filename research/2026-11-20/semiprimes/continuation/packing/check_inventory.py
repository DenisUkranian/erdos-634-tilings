"""Replay exact lower and upper packing bounds for two fixed placement lists."""
import json
from itertools import chain
from pathlib import Path

from packing_replay import area, det, disjoint, edges, inventory, norm, sub


def contained(triangle, board):
    return all(det(sub(v, u), sub(w, u)) >= 0
               for u, v in edges(board) for w in triangle)


def overlap_pairs(placements, indices):
    """Compare all pairs whose open axial bounding boxes overlap."""
    boxes = []
    for index in indices:
        xs, ys = zip(*placements[index])
        boxes.append((min(xs), max(xs), min(ys), max(ys), index))
    active = []
    for left, right, low, high, index in sorted(boxes):
        active = [other for other in active if other[0] > left]
        for _, bottom, top, other in active:
            if bottom < high and low < top:
                if not disjoint(placements[index], placements[other]):
                    yield other, index
        active.append((right, low, high, index))


def replay(a, b, c, certificate):
    board, placements, _, _ = inventory(a, b, c)
    n = (a + 2*b)*(2*a + b)
    lengths = sorted((c*side)**2 for side in (a, b, c))
    for triangle in placements:
        assert area(triangle) == a*b*c*c
        assert sorted(norm(sub(v, u)) for u, v in edges(triangle)) == lengths
    assert area(board) == n*a*b*c*c
    inside = {i for i, tri in enumerate(placements) if contained(tri, board)}
    selected = set(range(len(placements))) - set(certificate['deleted'])
    assert selected <= inside
    assert next(overlap_pairs(placements, selected), None) is None

    # Disjoint pairs of IDs with geometrically intersecting interiors.
    matching = certificate['matching']
    ids = list(chain.from_iterable(matching))
    assert len(ids) == len(set(ids)) == 2*len(matching)
    assert set(ids) <= inside
    for i, j in matching:
        assert not disjoint(placements[i], placements[j])
    assert len(selected) == len(inside) - len(matching)
    print(f'{n}: {len(placements)} candidates, {len(inside)} inside, '
          f'{len(matching)} matched overlaps, '
          f'{len(selected)} packed, {n-len(selected)} units of free area.')
    return board, placements, selected


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    certificate = json.loads(Path(__file__).with_name('inventory_certificate.json').read_text())
    for a, b, c in [(33, 7, 37), (35, 13, 43)]:
        count = (a + 2*b)*(2*a + b)
        replay(a, b, c, certificate[str(count)])
