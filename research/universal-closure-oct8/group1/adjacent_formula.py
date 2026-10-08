#!/usr/bin/env python3
"""Solver-free uniform construction: u>=2, v=u+1, W scale u+2.

All triangles are generated from ordinary grids. The final exchange moves
one entire corner tile from the last upper strip grid into the left cap.
"""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import argparse
import json


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def area2(p):
    return sum(det(a, b) for a, b in zip(p, p[1:]+p[:1]))


def ccw(p):
    return list(p) if area2(p) > 0 else list(reversed(p))


def triangle_grid(vertices, n, skip=None):
    origin, left, right = vertices
    e = tuple(F(left[k]-origin[k], n) for k in range(2))
    f = tuple(F(right[k]-origin[k], n) for k in range(2))

    def p(i, j):
        return tuple(origin[k]+i*e[k]+j*f[k] for k in range(2))

    tiles = []
    removed = 0
    for i in range(n):
        for j in range(n-i):
            ts = [[p(i,j), p(i+1,j), p(i,j+1)]]
            if i+j < n-1:
                ts.append([p(i+1,j), p(i+1,j+1), p(i,j+1)])
            for t in ts:
                if skip is not None and set(t) == set(skip):
                    removed += 1
                else:
                    tiles.append(ccw(t))
    assert removed == (skip is not None)
    assert len(tiles) == n*n-removed
    return tiles


def rectangle_grid(x0, y0, x1, y1, w, h):
    assert (x1-x0) % w == 0 and (y1-y0) % h == 0
    assert x1 >= x0 and y1 >= y0
    out = []
    for x in range(x0, x1, w):
        for y in range(y0, y1, h):
            out.extend([[(x,y),(x+w,y),(x,y+h)],
                        [(x+w,y),(x+w,y+h),(x,y+h)]])
    return out


def residual_tiles(u):
    assert isinstance(u, int) and u >= 2
    v, m = u+1, u+2
    shift = (-u*u*m, u*v*m)
    k = u*u-u-1
    notch = [(shift[0]+k, shift[1]-u*u),
             (shift[0]+k, shift[1]-u*v),
             (shift[0]+u*u, shift[1]-u*v)]
    out = []
    # The staircase of uv squares and B-type triangular fringes.
    for j in range(u+1):
        x, y = -v-j*u*v, u+j*u*u
        out.extend(rectangle_grid(x,y,x+u*v,y+u*v,u,v))
        top = [(x,y+u*v),(x,y+u*v+u*u),(x+u*v,y+u*v)]
        out.extend(triangle_grid(top,u,skip=notch if j == u else None))
        if j > 0:
            bottom = [(x,y),(x+u*v,y),(x+u*v,y-u*u)]
            out.extend(triangle_grid(bottom,u))
    # Right lower end: a B unit followed by a B rectangle.
    right = v*(u-1)
    out.extend(triangle_grid([(-v,u),(0,0),(0,u)],1))
    out.extend(rectangle_grid(0,0,right,u,v,u))
    # Right upper end: A triangle, B rectangle, B unit.
    out.extend(triangle_grid([(right+v,0),(u*(2*u+1),0),(right+v,u*v)],u))
    out.extend(rectangle_grid(right,0,right+v,u*v,v,u))
    out.extend(triangle_grid([(right,u*v),(right+v,u*v),(right,u*v+u)],1))
    # Left cap, in coordinates translated by the original vertex V.
    left = []
    left.extend(triangle_grid([(-u*m,v*m),(-u*m,v),(-u,v)],v))
    left.extend(rectangle_grid(-u*m,1,-u,v,v,u))
    left.extend(triangle_grid([(-u,0),(-u,v),(0,0)],1))
    left.extend(rectangle_grid(-u*m,-u*m,-u,1,u,v))
    left.extend(triangle_grid([(-u*m,-u*m),(-u,-u*m),(-u,-2*u*v)],u))
    # Final exchange: this union includes the removed B unit notch.
    left.extend(rectangle_grid(-u,-u*v,0,0,u,v))
    left.extend(triangle_grid([(0,0),(0,-u*v),(v*v,-u*v)],v))
    left.extend(rectangle_grid(-u,-2*u*v,k,-u*v,v,u))
    left.extend(triangle_grid([(-u,-2*u*v),(k,-2*u*v),(k,-3*u*u-u)],u-1))
    out.extend([[(x+shift[0],y+shift[1]) for x,y in t] for t in left])
    assert len(out) == 4*u**3+14*u*u+16*u+5
    return out


def outer_shape(u):
    v, m, b = u+1, u+2, 2*u+1
    O=(F(u*m*v**3,b),F(-u*u*m*v*v,b))
    X=(F(0),F(0)); A=(F(-u*v*m),F(u*u*m)); C=(F(-u*v*m),F(v*v*m))
    V=(F(-u*u*m),F(u*v*m)); U=(F(-u*u*m+v*v),F(u*v*v))
    Rr=(F(-u*u*v),F(u*v*v)); S=(F(u*v),F(u*v)); Q=(F(u*b),F(0))
    P=(Q[0]+F(u*v**3,b),Q[1]-F(u*u*v*v,b))
    R=(S[0]+F(u*v*v,b),S[1]-F(u*u*v,b))
    T=(U[0]+F((u-1)*v**3,b),U[1]-F((u-1)*u*v*v,b))
    macros=[([O,X,Q,P],u*m,u),([P,Q,S,R],v,1),
            ([R,Rr,U,T],2*u,u-1),([T,V,C],m,0)]
    return [O,A,C],macros


def annulus_grid(polygon, r, s):
    if s == 0:
        return triangle_grid(polygon,r)
    left,right,tr,tl=polygon
    apex=tuple((r*tl[k]-s*left[k])/(r-s) for k in range(2))
    e=tuple((left[k]-apex[k])/r for k in range(2))
    f=tuple((right[k]-apex[k])/r for k in range(2))
    def p(i,j):return tuple(apex[k]+i*e[k]+j*f[k] for k in range(2))
    ts=[]
    for i in range(r):
        for j in range(r-i):
            if i+j >= s:ts.append(ccw([p(i,j),p(i+1,j),p(i,j+1)]))
            if s-1 <= i+j < r-1:ts.append(ccw([p(i+1,j),p(i+1,j+1),p(i,j+1)]))
    assert len(ts)==r*r-s*s
    return ts


def generate(u,path):
    assert u >= 2
    v,m=u+1,u+2
    target,macros=outer_shape(u)
    ts=residual_tiles(u)
    for polygon,r,s in macros:ts.extend(annulus_grid(polygon,r,s))
    assert len(ts)==(2*v*v-u*u)*m*m
    E=(F(u*u-2*v*v,2*v*v),F(u,2*v*v))
    FF=(F(-u,2*v),F(1,2*v))
    O=target[0]
    def physical(p):
        x,y=p[0]-O[0],p[1]-O[1]
        return (v*(x*E[0]+y*FF[0]),v*(x*E[1]+y*FF[1]))
    ts=[ccw([physical(p) for p in t]) for t in ts]
    goal=ccw([physical(p) for p in target])
    den=lcm(*(x.denominator for t in ts+[goal] for p in t for x in p))
    D=4*v*v-u*u
    data={'metric':f'x^2+{D}y^2','metric_y_coefficient':D,'denominator':den,
          'tile':[u*v,2*u+1,v*v],'u':u,'v':v,'scale':m,
          'target':[[int(x*den),int(y*den)] for x,y in goal],
          'triangles':[[[int(x*den),int(y*den)] for x,y in t] for t in ts],
          'construction':'Uniform solver-free adjacent-parameter formula'}
    path.write_text(json.dumps(data,indent=2)+'\n')
    return len(ts)


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    ap=argparse.ArgumentParser();ap.add_argument('--u',type=int,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    print(json.dumps({'u':args.u,'tiles':generate(args.u,args.output),'output':str(args.output)}))
