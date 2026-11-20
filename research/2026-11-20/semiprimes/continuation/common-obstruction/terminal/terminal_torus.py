#!/usr/bin/env python3
"""Integer endpoint projection of a terminal Euclidean translate.

A feasible point is an algebraic residue pattern, not a geometric tiling.
An infeasibility claim is used only for the explicitly chosen finite model.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

UNITS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def model(a, b, c, blocks):
    assert a*a+a*b+b*b == c*c

    def add(p, q):
        return ((p[0]+q[0]) % c, (p[1]+q[1]) % c)

    def scale(k, p):
        return (k*p[0] % c, k*p[1] % c)

    def row(axis, q):
        return (axis % 3)*c*c+q[0]*c+q[1]

    def tile(j, s, q):
        u = add(q, scale(-a, UNITS[j]))
        w = add(q, scale(b, UNITS[(j+s) % 6]))
        return [(row(j,q),s),(row(j,u),-s),
                (row(j+s,w),s),(row(j+s,q),-s)]

    cols, labels, costs, signs = [], [], [], []
    points = [(x,y) for x in range(c) for y in range(c)]
    for j in range(6):
        for q in points:
            cols.append(tile(j,-1,q))
            labels.append(('inward',j,q))
            costs.append(1)
            signs.append(-(-1)**j)
    for j in range(3):
        for q in points:
            mate = add(add(q,scale(-a,UNITS[j])),scale(b,UNITS[(j+1)%6]))
            cols.append(tile(j,1,q)+tile(j+3,1,mate))
            labels.append(('outward_pair',j,q))
            costs.append(2)
            signs.append(0)
    entries = [(i,j,v) for j,col in enumerate(cols) for i,v in col]
    entries += [(3*c*c,j,s) for j,s in enumerate(signs) if s]
    entries += [(3*c*c+1,j,cost) for j,cost in enumerate(costs)]
    ii,jj,vv = zip(*entries)
    matrix = coo_matrix((vv,(ii,jj)),shape=(3*c*c+2,len(cols))).tocsc()
    rhs = np.zeros(3*c*c+2)
    rhs[-2:] = [c, blocks*c]
    lower = np.zeros(len(cols))
    # Translation and 120-degree rotation put some positive inward tile here.
    lower[labels.index(('inward',1,(0,0)))] = 1
    return matrix,rhs,lower,labels,costs,signs


def main():
    p = argparse.ArgumentParser()
    p.add_argument('sides',type=int,nargs=3)
    p.add_argument('--blocks',type=int,default=3)
    p.add_argument('--seconds',type=float,default=20)
    p.add_argument('--out',type=Path)
    args = p.parse_args()
    a,b,c = args.sides
    matrix,rhs,lower,labels,costs,signs = model(a,b,c,args.blocks)
    started = time.monotonic()
    result = milp(np.zeros(len(labels)),integrality=np.ones(len(labels)),
                  bounds=Bounds(lower,np.full(len(labels),args.blocks*c)),
                  constraints=LinearConstraint(matrix,rhs,rhs),
                  options={'time_limit':args.seconds,'mip_rel_gap':0.0})
    report = {'tile':[a,b,c],'blocks':args.blocks,'rows':matrix.shape[0],
              'columns':matrix.shape[1],'status':int(result.status),
              'message':result.message,'seconds':round(time.monotonic()-started,3),
              'scope':'Integer residue projection only; no geometric tiling is asserted.'}
    if result.x is not None:
        x = np.rint(result.x).astype(np.int64)
        exact = np.array_equal(matrix @ x,rhs) and np.all(x >= lower)
        report['exact_integer_witness'] = bool(exact)
        if exact:
            report['population'] = int(np.dot(costs,x))
            report['signed_population'] = int(np.dot(signs,x))
            report['support'] = int(np.count_nonzero(x))
            report['witness'] = [(lab,int(n)) for lab,n in zip(labels,x) if n]
    print(json.dumps({k:v for k,v in report.items() if k != 'witness'}),flush=True)
    if args.out:
        args.out.write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
