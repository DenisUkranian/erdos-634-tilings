#!/usr/bin/env python3
"""Reconstruct the opposite lift and its boundary area, independently of the grid generator."""
from fractions import Fraction as F
import json
import os

if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
    raise SystemExit('Use ordinary Python without -O/-OO/PYTHONOPTIMIZE.')


def transpose(m):
    return [list(x) for x in zip(*m)]


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def mv(m, v):
    return [sum(x*y for x, y in zip(row, v)) for row in m]


def cross(p, q):
    return [p[1]*q[2]-p[2]*q[1], p[2]*q[0]-p[0]*q[2], p[0]*q[1]-p[1]*q[0]]


def inverse(m):
    a=[[F(x) for x in row]+[F(i == j) for j in range(3)] for i, row in enumerate(m)]
    for j in range(3):
        k=next(i for i in range(j, 3) if a[i][j])
        a[j], a[k]=a[k], a[j]
        d=a[j][j]
        a[j]=[x/d for x in a[j]]
        for i in range(3):
            if i != j:
                d=a[i][j]
                a[i]=[x-d*y for x, y in zip(a[i], a[j])]
    return [row[3:] for row in a]


def cofactor(m):
    columns=transpose(m)
    return transpose([cross(columns[1], columns[2]),
                      cross(columns[2], columns[0]),
                      cross(columns[0], columns[1])])


def area_vector_twice(poly):
    terms=[cross(p, q) for p, q in zip(poly, poly[1:]+poly[:1])]
    return [sum(v[k] for v in terms) for k in range(3)]


def verify(a, b):
    d=a*a+a*b+b*b
    u=[0,-b,a]; v=[-a,0,b]; w=[-b,a,0]
    up=[0,-a,b]; vp=[-b,0,a]; wp=[-a,b,0]
    t=mm(transpose([up,vp,wp]), inverse(transpose([u,v,w])))
    displayed=[[a*b,-a*(a+b),-b*(a+b)],
               [-b*(a+b),a*b,-a*(a+b)],
               [-a*(a+b),-b*(a+b),a*b]]
    assert t==[[F(x,d) for x in row] for row in displayed]
    assert mv(t,u)==up and mv(t,v)==vp and mv(t,w)==wp
    assert mm(transpose(t),t)==[[int(i==j) for j in range(3)] for i in range(3)]
    m=cofactor(t)
    assert m==[[-x for x in row] for row in t]
    o=[0,0,0]; p=[-a*b*b,0,b**3]; q=[0,-a*a*b,b**3]; c=[0,0,b**3-a**3]
    polygon=[o,p,q,c,[x-y for x,y in zip(c,p)],[x-y for x,y in zip(c,q)]]
    direct=[F(x,a*b) for x in area_vector_twice(polygon)]
    opposite=[F(x,a*b) for x in area_vector_twice([mv(t,p) for p in polygon])]
    assert direct==[2*a**4,2*b**4,2*a*a*b*b]
    assert opposite==mv(m,direct)
    assert opposite==[2*a*b*(b*b+a*b-a*a),
                      2*a*b*(a*a+a*b-b*b),
                      2*(a**4-a*a*b*b+b**4)]
    assert sum(direct)==2*d*(a*a-a*b+b*b)==sum(opposite)
    return {'a':a,'b':b,'direct':[int(x) for x in direct],
            'opposite':[int(x) for x in opposite]}


if __name__=='__main__':
    example=verify(3,5)
    assert example['opposite']==[930,-30,962]
    print(json.dumps({'status':'PASS','method':'exact long-lift matrix inversion and boundary cross products',
                      'example':example,'full_Erdos634_solved':False},indent=2))
