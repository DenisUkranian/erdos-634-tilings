"""Small original rational-geometry helpers; no search-engine dependency.

Coordinates (u,v) represent (u+v/2, sqrt(3)v/2). All areas returned are
twice coordinate area; physical area is sqrt(3)/4 times this quantity.
"""

from fractions import Fraction as F


def add(p, q):
    return p[0]+q[0], p[1]+q[1]


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def scale(k, p):
    return k*p[0], k*p[1]


def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]


def area2(poly):
    return sum(cross(p,q) for p,q in zip(poly,poly[1:]+poly[:1]))


def ccw(poly):
    return poly if area2(poly)>0 else poly[::-1]


def clip(poly, a, b):
    out=[]
    edge=sub(b,a)
    for p,q in zip(poly,poly[1:]+poly[:1]):
        sp,sq=cross(edge,sub(p,a)),cross(edge,sub(q,a))
        if sp>=0:
            out.append(p)
        if (sp>0 and sq<0) or (sp<0 and sq>0):
            t=sp/(sp-sq)
            out.append(add(p,scale(t,sub(q,p))))
    return out


def intersection_area2(p,q):
    poly=p[:]
    for a,b in zip(q,q[1:]+q[:1]):
        poly=clip(poly,a,b)
        if len(poly)<3:
            return F(0)
    return abs(area2(poly))


def convex(poly):
    return len(poly)>=3 and area2(poly)>0 and all(
        cross(sub(poly[(i+1)%len(poly)],poly[i]),
              sub(poly[(i+2)%len(poly)],poly[(i+1)%len(poly)]))>0
        for i in range(len(poly)))


def contains(poly,p):
    return all(cross(sub(b,a),sub(p,a))>=0
               for a,b in zip(poly,poly[1:]+poly[:1]))


def encode(poly):
    return [[str(u),str(v)] for u,v in poly]


def decode(poly):
    return [(F(u),F(v)) for u,v in poly]


def triangle_grid(poly,n):
    p,q,r=poly
    u,v=scale(F(1,n),sub(q,p)),scale(F(1,n),sub(r,p))
    out=[]
    for i in range(n):
        for j in range(n-i):
            w=add(p,add(scale(i,u),scale(j,v)))
            out.append(ccw([w,add(w,u),add(w,v)]))
            if i+j<n-1:
                out.append(ccw([add(w,u),add(add(w,u),v),add(w,v)]))
    return out
