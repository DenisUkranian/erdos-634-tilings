"""Compare two exact population bounds on the four sectors of a remote cut."""
from functools import lru_cache
from hull import ceil_div


@lru_cache(None)
def minimum(c, A, D, signed, current, core, allowance):
    negative_residue = (19 if c == 37 else 5) if core else 0
    floor = (64 if c == 37 else 75) if core else 0
    lower = max(abs(signed), floor)
    if current:
        aligned = signed if current > 0 else -signed
        projected = ceil_div(2*D*abs(current) + (D-2*A)*aligned - 2*allowance, D)
        lower = max(lower, 2*abs(current)-aligned, projected)
    initial = signed + 2*negative_residue
    n = initial + 2*c*max(0, ceil_div(lower-initial, 2*c))

    # Independent integer scan over the two physical sign populations.
    for negative in range(negative_residue, (n-signed)//2+1, c):
        positive = negative + signed
        if positive < 0 or positive + negative < floor:
            continue
        same, other = (positive, negative) if current >= 0 else (negative, positive)
        if abs(current) <= same and D*abs(current) <= A*same+(D-A)*other+allowance:
            assert positive+negative == n
            return n
    raise AssertionError('Rounded sector lower bound was not attained in its relaxation.')


def sectors(c, d, A, D, N, W, V, allowance):
    result = {}
    for inside in ('even', 'odd'):
        surviving = []
        tested = 0
        for e in range(-W//2, W//2+1):
            for o in range(-(V-1)//2, (V+1)//2+1):
                p, q = c*e-d*o, d*e-c*o
                groups = [(c*e, p if inside=='even' else 0, False),
                          (c*o, -q if inside=='odd' else 0, False),
                          (d-c*e, -p if inside=='odd' else 0, True),
                          (c-c*o, q if inside=='even' else 0, False)]
                cost = sum(minimum(c,A,D,s,u,core,allowance if core else 0)
                           for s,u,core in groups)
                tested += 1
                if cost <= N:
                    surviving.append((e,o))
        result[inside] = dict(charge_pairs_before=tested, charge_pairs_remaining=len(surviving),
            maximum_absolute_e=max(abs(e) for e,o in surviving),
            maximum_absolute_o=max(abs(o) for e,o in surviving),
            maximum_absolute_difference=max(abs(e-o) for e,o in surviving))
    return result
