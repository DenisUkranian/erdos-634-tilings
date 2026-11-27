"""Rule out all source profiles at a six-block excess on the 3431 board."""
from pathlib import Path
import gzip
import json
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'slant-flux'))
from duals import UNITS, load_tables, scores
sys.path.insert(0, str(HERE.parent / 'slant-flux'))
from replay import middle37
from hull import profiles


def bound(dual, middle, direction):
    a, b, c = 33, 7, 37
    form = None if middle else -a * pow(b, -1, c) % c
    size = c*c if middle else c
    y, short, sign, j, hand, down, up = scores(dual, a, b, c, form)
    label = np.where(hand == -1, down, c+up) if middle else np.where(hand == 1, up, c)
    assert len(y) == 3*size + (2*c if middle else c+1)
    reward = np.array([direction*u[0] for u in UNITS])[j] * (label == 0)
    value = short + sign*y[3*size+label] + 10000*reward
    D = max(0, int(max(value)))
    if middle:
        target = 11 * int(y[3*size+c] - y[3*size])
    else:
        target = 37 * int(y[3*size])
    return (74 if middle else 185)*D - target


def check():
    fit = middle37(load_tables()['middle37'])
    remaining = [p for g, core, p in profiles(37,26,6) if fit(*p[0])]
    first = ((2,(11,-11)), (2,(-37,37)), (5,(37,)), (5,(37,)))
    second = ((2,(11,-11)), (5,(37,)), (5,(37,)))
    assert sorted(remaining) == sorted([first, second])
    tables = json.loads(gzip.decompress((HERE/'k6_duals.json.gz').read_bytes()))
    bx = bound(tables['B_positive_x'], True, 1)
    nx = bound(tables['B_negative_x'], True, -1)
    tx = bound(tables['T_positive_x'], False, 1)
    assert bx//10000 == nx//10000 == 11 and tx//10000 == 32
    pairs = []
    for x in range(-11,12):
        for y in range(-11,12):
            if abs(x+y)>11 or (x-y-11)%3:
                continue
            X,Y = 37-x,-y
            u, rx = divmod(40*X+7*Y,37)
            v, ry = divmod(-7*X+33*Y,37)
            if not rx and not ry and (u-v-37)%3 == 0:
                assert (37*x+33*u-7*v,37*y+7*u+40*v) == (37**2,0)
                pairs.append(((x,y),(u,v)))
    assert len(pairs) == 3 and all(u>tx//10000 for _,(u,v) in pairs)
    return dict(profile_count=len(remaining), projection_numerators=[bx,nx,tx],
                common_denominator=10000, integer_displacement_pairs=pairs)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(check(),indent=2))
