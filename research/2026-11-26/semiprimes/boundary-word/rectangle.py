"""Enumerate necessary boundary words in the saturated three-direction inventory."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache

from control import geom
from remote import inventories


def det(u,v):
    return u[0]*v[1]-u[1]*v[0]


def sub(p,q):
    return p[0]-q[0],p[1]-q[1]


def overlap(a,b):
    for left,right in ((a,b),(b,a)):
        for p,q in zip(left,left[1:]+left[:1]):
            if all(det(sub(q,p),sub(v,p))<=0 for v in right):
                return False
    return True


def classify(a,b,c):
    g = geom.Geometry(a,b,c)
    bound = c,b,c-a
    target = ((0,0,c), (b,0,c-a))
    permitted = list(inventories(a,b,c,2,-c,c-a+b,2*c-a+b))
    assert target in [(l,r) for _,l,r in permitted]
    patterns = [(2,4,-1),(1,0,1),(1,4,1)]
    move = [(-b,-a),(c,0),(0,-c)]
    wall = (0,g.B,0)
    allowed = {a*i+b*j for i in range(b*c//a+1) for j in range(c+1)}
    histogram = Counter()

    @lru_cache(maxsize=None)
    def owner(state, index):
        x = c*state[1]-b*state[0]
        y = -a*state[0]-c*state[2]
        start = g.add(wall,g.mult(g.unit(2,0),(x,y,0)))
        h,j,s = patterns[index]
        template = g.vertices(((0,0,0),h,j,s))
        origin = template[-1] if s==-1 else template[0]
        tile = g.sub(start,origin),h,j,s
        vertices = g.vertices(tile)
        end = vertices[0] if s==-1 else vertices[-1]
        dx,dy = move[index]
        assert g.sub(end,start) == g.mult(g.unit(2,0),(dx,dy,0))
        poly = tuple(geom.point(g,p) for p in vertices)
        if all(x>=0 and y>=0 and g.B*x+g.A*y<=g.A*g.B for x,y in poly):
            return poly
        return None

    for residue in range(b):
        @lru_cache(maxsize=None)
        def tails(state, last):
            if state == bound:
                return ("",)
            x = c*state[1]-b*state[0]
            y = -a*state[0]-c*state[2]
            previous = list(state)
            if last >= 0:
                previous[last] -= 1
            result = []
            for j in range(3):
                if state[j]==bound[j] or (j!=1 and -x not in allowed):
                    continue
                if (j==1 and y%b!=residue) or (j==2 and x%a):
                    continue
                poly = owner(state,j)
                if poly is None or (last>=0 and overlap(poly,owner(tuple(previous),last))):
                    continue
                following = list(state)
                following[j] += 1
                result.extend(str(j)+w for w in tails(tuple(following),j))
            return tuple(result)

        for word in tails((0,0,0),-1):
            width = 0
            rows = []
            area = x = y = 0
            for token in word:
                j = int(token)
                dx,dy = move[j]
                area += x*dy-y*dx
                x,y = x+dx,y+dy
                if j==0:
                    rows.extend([width]*a)
                    width += b
                elif j==1:
                    width -= c
                else:
                    rows.extend([width]*c)
            assert (x,y)==(0,-c*c) and width==0 and len(rows)==c*c
            # Independent doubling of area, using the remaining rectangles.
            assert area == c*a*b+2*sum(rows)
            population = Fraction(area,a*b)
            if population.denominator == 1 and (population.numerator-c)%(2*c)==0:
                histogram[population.numerator] += 1
        tails.cache_clear()
    print(g.N, "saturated inventories",len(permitted),"three-direction words",
          sum(histogram.values()),"population histogram",sorted(histogram.items()))
    return sorted(histogram)


if __name__ == "__main__":
    assert classify(33,7,37)==list(range(925,1444,74))
    assert classify(35,13,43)==list(range(1247,2022,86))
