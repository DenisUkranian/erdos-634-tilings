"""Exact slant displacements in four small source profiles at 5063."""
from pathlib import Path
import gzip
import json
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'slant-flux'))
from duals import UNITS, scores
sys.path.insert(0, str(HERE.parent/'slant-flux'))
from replay import middle43
from hull import profiles


def bank_score(dual, axial=None):
    a, b, c = 35, 13, 43
    middle = axial is not None
    form = None if middle else -a*pow(b,-1,c) % c
    size = c*c if middle else c
    y, short, sign, j, h, down, up = scores(dual, a, b, c, form)
    label = np.where(h == -1, down, c+up) if middle else np.where(h == 1, up, c)
    assert len(y) == 3*size + (2*c if middle else c+1)
    native = np.array(UNITS)[j].T*(label == 0)
    lhs = short + sign*y[3*size+label]
    rhs = int(axial*y[3*size+c] - 21*y[3*size]) if middle else int(43*y[3*size])
    return native, lhs, rhs


def caps(tables, population, axial=None):
    limit = []
    for sign, dual in zip((1,-1), tables, strict=True):
        heading, value, rhs = bank_score(dual, axial)
        D = max(0, int(max(value + sign*10000*heading[0])))
        limit.append((population*D-rhs)//10000)
    return limit


def check():
    c = 43
    fit = middle43()
    passing = [stars for _, _, stars in profiles(c,22,8) if fit(*stars[0])]
    selected = [p for p in passing if p[0][1][1] == -21]
    assert len(passing) == 12 and len(selected) == 4
    for n, axial in ((4,21),(7,64)):
        local = [p for p in selected if p[0] == (n,(axial,-21))]
        assert sorted(p[1] for p in local) == [(2,(-43,43)), (5,(43,))]
        assert all(all(g == (5,(43,)) for g in p[2:]) for p in local)
    data = json.loads(gzip.decompress((HERE/'k8_duals.json.gz').read_bytes()))
    out = {}
    upper_t, lower_t = caps(data['T'], 215)
    fixed = data['T_fixed']
    heading, value, rhs = bank_score(fixed[:-2])
    multipliers = np.array(fixed[-2:])
    D = int(max(value + multipliers@heading))
    fixed_rhs = int(rhs + multipliers@np.array([32,-23]))
    assert fixed_rhs > 215*D > 0
    for axial, n in ((21,172),(64,301)):
        upper, lower = caps(data[f'B{axial}'],n,axial)
        vectors = []
        for x in range(-lower,upper+1):
            for y in range(-lower,upper+1):
                if not -lower <= -x-y <= upper or (x-y-21)%3:
                    continue
                X, Y = c-x, -y
                u, rx = divmod(48*X+13*Y,c)
                v, ry = divmod(-13*X+35*Y,c)
                if rx or ry or (u-v-43)%3:
                    continue
                if min(u,v,-u-v)<-lower_t or max(u,v,-u-v)>upper_t or (u,v)==(32,-23):
                    continue
                assert (c*x + 35*u-13*v, c*y+13*u+48*v) == (c*c,0)
                vectors.append(((x,y),(u,v)))
        assert len(vectors) == (4 if axial==21 else 2)
        out[axial] = dict(B_projection=[upper,lower], slant_vectors=vectors)
    out['T_projection'] = [upper_t,lower_t]
    out['excluded_T_vector_lower_bound'] = [fixed_rhs,D]
    return out


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps(check(),indent=2))
