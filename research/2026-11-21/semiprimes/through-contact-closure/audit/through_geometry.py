#!/usr/bin/env python3
"""Independent rational geometry for complete through-owner catalogues.

The six edge shapes are reconstructed by side lengths, dot products and
signed area, without importing the search's inverse-placement catalogue.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations

if not __debug__:
    raise SystemExit('Run without -O: exact geometry assertions are required.')


def add(p, q): return p[0] + q[0], p[1] + q[1]
def sub(p, q): return p[0] - q[0], p[1] - q[1]
def scale(k, p): return k * p[0], k * p[1]
def det(p, q): return p[0] * q[1] - p[1] * q[0]
def norm(p): return p[0] * p[0] + p[0] * p[1] + p[1] * p[1]
def multiply(p, q):
    x, y = p; u, v = q
    return x * u - y * v, x * v + y * u + y * v
def conjugate(p): return p[0] + p[1], -p[1]
def canonical(vertices): return tuple(sorted(vertices))


class ExactGeometry:
    def __init__(self, a, b, c):
        assert a > b > 0 and c*c == a*a+a*b+b*b
        self.a, self.b, self.c = a, b, c
        self.A, self.B = b*(2*a+b), a*(a+2*b)
        self.N = (a+2*b)*(2*a+b)
        self.board = ((F(0), F(0)), (F(self.A), F(0)), (F(0), F(self.B)))
        self.coin = [False] * (max(self.A, self.B, c*c)+1)
        self.coin[0] = True
        for k in range(1, len(self.coin)):
            self.coin[k] = any(k >= side and self.coin[k-side] for side in (a,b,c))

    def point(self, encoded):
        x, y, exponent = encoded
        return F(x, self.c**exponent), F(y, self.c**exponent)

    @lru_cache(None)
    def unit(self, h, j):
        z = (F(self.a,self.c), F(self.b,self.c))
        if h < 0:
            z = conjugate(z)
        result = (F(1), F(0))
        power = abs(h)
        while power:
            if power & 1:
                result = multiply(result, z)
            z = multiply(z, z)
            power //= 2
        for _ in range(j % 6):
            result = (-result[1], result[0]+result[1])
        assert norm(result) == 1
        return result

    @lru_cache(None)
    def polygon(self, tile):
        q, h, j, s = tile
        q = self.point(q)
        vertices = [sub(q, scale(self.a,self.unit(h,j))), q,
                    add(q, scale(self.b,self.unit(h,j+s)))]
        if det(sub(vertices[1],vertices[0]),sub(vertices[2],vertices[0])) < 0:
            vertices.reverse()
        assert det(sub(vertices[1],vertices[0]),sub(vertices[2],vertices[0])) == self.a*self.b
        return tuple(vertices)

    def admissible_polygon(self, vertices):
        for x, y in vertices:
            if x < 0 or y < 0 or self.B*x+self.A*y > self.A*self.B:
                return False
            offsets = []
            if y == 0:
                offsets.append((x,self.A-x))
            if x == 0:
                offsets.append((y,self.B-y))
            if self.B*x+self.A*y == self.A*self.B:
                t = y*self.c*self.c/self.B
                offsets.append((t,self.c*self.c-t))
            for pair in offsets:
                if any(t.denominator != 1 or not self.coin[int(t)] for t in pair):
                    return False
        return True

    def six_shapes(self, p, ray):
        """Six triangles on the right of p -> p+L*u, before shifts."""
        u = self.unit(*ray)
        perpendicular = (-u[0]-2*u[1],2*u[0]+u[1])  # i*sqrt(3)*u
        result = []
        for L in (self.a,self.b,self.c):
            other = [s for s in (self.a,self.b,self.c) if s != L]
            for r,s in (other,other[::-1]):
                along = F(r*r+L*L-s*s,2*L)
                normal = F(self.a*self.b,2*L)
                third = add(p,sub(scale(along,u),scale(normal,perpendicular)))
                end = add(p,scale(L,u))
                triangle = (p,end,third)
                assert sorted(norm(sub(x,y)) for x,y in combinations(triangle,2)) == sorted((self.a**2,self.b**2,self.c**2))
                assert det(u,sub(third,p)) < 0
                result.append((L,triangle))
        return result

    @lru_cache(maxsize=20000)
    def owners(self, p, ray):
        u = self.unit(*ray)
        result = set()
        for length,triangle in self.six_shapes(p,ray):
            for offset in range(1,length):
                shifted = tuple(sub(v,scale(offset,u)) for v in triangle)
                if self.admissible_polygon(shifted):
                    result.add(canonical(shifted))
        assert len(result) <= 2*(self.a+self.b+self.c-3)
        return frozenset(result)

    @lru_cache(maxsize=20000)
    def endpoint_candidates(self, p, ray):
        result = set()
        for direction in (ray,(ray[0],(ray[1]+3)%6)):
            for _,right in self.six_shapes(p,direction):
                # Reflect the third vertex in the oriented base line.
                u = self.unit(*direction)
                x = sub(right[2],p)
                reflected = multiply(multiply(u,u),conjugate(x))
                for polygon in (right,(right[0],right[1],add(p,reflected))):
                    if self.admissible_polygon(polygon):
                        result.add(canonical(polygon))
        assert len(result) <= 24
        return frozenset(result)

    @lru_cache(maxsize=20000)
    def edge_bank(self,p,ray,length):
        """Complete right-bank placements and clipped integer overlap spans."""
        assert length in (self.a,self.b,self.c)
        u = self.unit(*ray)
        result = {}
        for side,triangle in self.six_shapes(p,ray):
            for start in range(1-side,length):
                shifted = tuple(add(v,scale(start,u)) for v in triangle)
                if self.admissible_polygon(shifted):
                    key = canonical(shifted)
                    span = max(0,start),min(length,start+side)
                    assert key not in result or result[key] == span
                    result[key] = span
        assert len(result) <= 6*length+2*(self.a+self.b+self.c)-6
        return result


def overlap_open(a, b):
    """Exact separating-axis test; touching boundaries are permitted."""
    for polygon in (a,b):
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            direction = sub(q,p)
            left = [det(direction,v) for v in a]
            right = [det(direction,v) for v in b]
            if max(left) <= min(right) or max(right) <= min(left):
                return False
    return True


def interior(p, polygon):
    return all(det(sub(q,r),sub(p,r)) > 0 for r,q in zip(polygon,polygon[1:]+polygon[:1]))


def common_vertex_interior(p,polygons):
    """Exact linear-time common open sector test at a shared vertex.

    Any direction in the first triangle's open cone is proportional to
    lo+t*hi, t>0. Every other cone imposes two strict linear inequalities on
    t. Their rational interval intersection is checked without angle floats.
    """
    if not polygons:
        return False
    first = polygons[0]
    k = first.index(p)
    lo,hi = sub(first[(k+1)%3],p),sub(first[(k+2)%3],p)
    assert det(lo,hi) > 0
    lower,upper = F(0),None
    for polygon in polygons:
        k = polygon.index(p)
        a,b = sub(polygon[(k+1)%3],p),sub(polygon[(k+2)%3],p)
        for constant,slope in ((det(a,lo),det(a,hi)),(det(lo,b),det(hi,b))):
            if slope > 0:
                lower = max(lower,-constant/slope)
            elif slope < 0:
                bound = -constant/slope
                upper = bound if upper is None else min(upper,bound)
            elif constant <= 0:
                return False
    return upper is None or lower < upper
