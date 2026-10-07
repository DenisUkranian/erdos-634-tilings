#!/usr/bin/env python3
"""Compose existing positive F4/trapezoid tilings in the new F3 partition."""
import argparse
import importlib.util
import json
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RESEARCH / 'group2-trapezoids'))
from exact_geometry import add, sub, scale, ccw, decode, encode, triangle_grid

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

f4 = module('f4_constructor', RESEARCH / 'group2-f4/construct.py')
trap = module('trapezoid_constructor', RESEARCH / 'group2-trapezoids/generate.py')
expand = module('trapezoid_expander', RESEARCH / 'group2-trapezoids/verify.py')

def cmul(p, q):
    return (p[0]*q[0]-p[1]*q[1], p[0]*q[1]+p[1]*q[0]+p[1]*q[1])

def construct(a, b, c, m=1):
    if not (all(type(v) is int for v in (a,b,c,m)) and
            0 < a < b and c*c == a*a+a*b+b*b and m > 0):
        raise ValueError('Require 0<a<b, norm triple, m>0')
    common = gcd(a,b)
    if common > 1:
        data = construct(a//common,b//common,c//common,m*common)
        data['tile'], data['multiplier'] = [a,b,c], m
        data['target'] = encode([scale(common,p) for p in decode(data['target'])])
        data['triangles'] = [encode([scale(common,p) for p in decode(t)])
                             for t in data['triangles']]
        data['trapezoid_short_base'] *= common
        data['trapezoid_leg'] *= common
        return data
    A, B, d = a*b, b*b, a+b-c
    X, Y, K = (-a*a, 0), (2*A, -2*A-B), (2*A, A+2*B)
    P, E, L, R = (A, -A), (2*A, -2*A), (A, A+B), (2*A, A+B)
    tiles = []
    for poly, n in (([X,Y,P], c), ([Y,P,E], b), ([L,R,K], b)):
        tiles += triangle_grid([scale(m, p) for p in poly], m*n)
    z = (F(a,c), F(b,c))
    f4data = f4.construct(a, b, c, m)
    for raw in f4data['triangles']:
        tiles.append(ccw([sub(scale(m,L),cmul(z,p)) for p in decode(raw)]))

    # The seed is generated in short-side order (b,a). Its origin is (ad,0).
    seed = trap.certificate(b,a,c,m=m)
    w = a*(3*b-c)
    seed_shift = (m*(w-a*d), 0)
    standard_tiles = []
    for block in seed['blocks']:
        _, _, unit = expand.check_block(block, seed['tile'], expand=True)
        standard_tiles += [[add(p,seed_shift) for p in tri] for tri in unit]
    # Left strip [0,mw] x [0,mab], using ordinary a,b cells.
    for i in range(m*(3*b-c)):
        for j in range(m*a):
            p = (i*a,j*b)
            u, v = (a,0),(0,b)
            pu, pv = add(p,u), add(p,v)
            puv = add(pu,v)
            standard_tiles += [[p,pu,puv],[p,puv,pv]]
    for tri in standard_tiles:
        tiles.append(ccw([add(scale(m,E),cmul((0,1),p)) for p in tri]))
    count = 3*(a+b)*(a+2*b)*m*m
    assert len(tiles) == count
    return {'format':'ERDOS634_F3_SMALL_A_V1', 'tile':[a,b,c],
            'multiplier':m, 'count':count,
            'target':encode(ccw([scale(m,p) for p in [X,Y,K]])),
            'triangles':[encode(tri) for tri in tiles],
            'construction':'positive F4 plus ideal trapezoid',
            'trapezoid_short_base':m*(2*A+B),
            'trapezoid_leg':m*A}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('a',type=int)
    parser.add_argument('b',type=int)
    parser.add_argument('c',type=int)
    parser.add_argument('output',type=Path)
    parser.add_argument('--multiplier',type=int,default=1)
    args = parser.parse_args()
    data = construct(args.a,args.b,args.c,args.multiplier)
    args.output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps({'count':data['count'],'output':str(args.output)}))
