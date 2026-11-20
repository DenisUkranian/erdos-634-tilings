"""Exact list of tile types on at least two axes of Q, up to translation."""
from itertools import product


def verify_directions():
    axes = {(0, 0), (0, 1), (1, 0), (1, 2)}
    axial, extra = [], {}
    for h, j, hand in product(range(-1, 3), range(6), (-1, 1)):
        edges = {(h, j % 3), (h, (j + hand) % 3), (h + hand, j % 3)}
        fresh = edges - axes
        if not fresh:
            axial.append((h, j, hand))
        elif len(fresh) == 1:
            key = next(iter(fresh))
            extra.setdefault(key, []).append((h, j, hand))
    assert len(axial) == 4
    assert set(extra) == {(-1, 1), (0, 2), (1, 1), (2, 2)}
    for (h, j, s), (hh, jj, ss) in extra.values():
        assert h == hh and s == ss and jj - j == 3
    all_axes = axes | set(extra)
    exceptional = set()
    for h, j, hand in product(range(-1, 3), range(6), (-1, 1)):
        labelled = [(h, j % 3), (h, (j+hand) % 3), (h+hand, j % 3)]
        edges = set(labelled)
        if edges <= all_axes and len(edges & axes) <= 1:
            exceptional.add((h,j,hand))
            assert labelled[2] in {(0,2),(1,1)}
    assert exceptional == {(0,1,1),(0,4,1),(1,2,-1),(1,5,-1)}
    for h,j,hand in axial + [t for pair in extra.values() for t in pair]:
        axes_by_label = [(h,j%3), (h,(j+hand)%3), (h+hand,j%3)]
        for i,axis in enumerate(axes_by_label):
            if axis in {(0,2),(1,1)}:
                assert i == 0
    return axial, extra


if __name__ == '__main__':
    print(verify_directions())
