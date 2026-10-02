#!/usr/bin/env python3
"""Generate a compressed exact QP construction; no claim of novelty for the motif.
The five-block construction is from the project's 2026-09-29 two-piece note.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from math import gcd


def point(x, y):
    return [F(x), F(y)]


def encoded(p):
    return [[z.numerator, z.denominator] for z in p]


def generate(u: int, v: int, t: int = 1) -> dict:
    if not (isinstance(u, int) and isinstance(v, int) and isinstance(t, int)
            and 0 < u < v and gcd(u, v) == 1 and t >= 1):
        raise ValueError("Require coprime integers 0<u<v and integer t>=1")
    a, b, c = u*v, v*v-u*u, v*v
    Q, P = b+c, b+2*c
    O = point(0, 0)
    A = point(b*b, 0)
    C = point(F(-u*u*b, 2), F(u*b, 2))
    D = point(F(-u*u*b, 2), F(-u*b, 2))
    E = point(F(-u*u*Q, 2), F(-u**3, 2))
    B = [D[i]+E[i] for i in range(2)]
    H = [C[i]+F(Q, c)*(C[i]-A[i]) for i in range(2)]
    pts = {k: [t*x for x in p] for k, p in zip("OACDEBH", (O,A,C,D,E,B,H))}
    return {
        "format": "erdos634-QP-macro-v1", "u": u, "v": v, "scale": t,
        "coordinate_convention": "(x,y) means the Euclidean point (x,sqrt(metric_D)*y)",
        "metric_D": 4*v*v-u*u,
        "tile_sides": [a,b,c], "tile_count": Q*P*t*t,
        "points": {k: encoded(p) for k,p in pts.items()},
        "target": ["A","B","H"],
        "blocks": [
            {"type": "triangle_grid", "vertices": ["O","A","C"], "subdivision": b*t},
            {"type": "triangle_grid", "vertices": ["O","A","D"], "subdivision": b*t},
            {"type": "triangle_grid", "vertices": ["O","C","E"], "subdivision": a*t},
            {"type": "triangle_grid", "vertices": ["B","C","H"], "subdivision": Q*t},
            {"type": "parallelogram_grid", "vertices": ["O","D","B","E"],
             "rows": b*t, "columns": u*u*t, "diagonal": "difference"},
        ],
        "source": "DenisUkranian/erdos-634-tilings, docs/two-piece-construction.md, commit 50d7459bd1d3f41352630323f1c55a92e8d9b64e",
        "validation_scope": "Compressed grids, not an explicit list of every tile",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("u",type=int);p.add_argument("v",type=int)
    p.add_argument("--scale",type=int,default=1);p.add_argument("--output",required=True)
    x=p.parse_args()
    with open(x.output,"w",encoding="utf-8") as h:
        json.dump(generate(x.u,x.v,x.scale),h,indent=2,sort_keys=True);h.write("\n")

if __name__=="__main__": main()
