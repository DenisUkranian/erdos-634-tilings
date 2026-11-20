"""An exact certificate for extending a unit F2 board by one tiled parallelogram."""
from itertools import combinations
from math import gcd, isqrt


def edges(polygon):
    return zip(polygon, polygon[1:] + polygon[:1])


def cross(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])


def area(polygon):
    return sum(x*v-y*u for (x,y),(u,v) in edges(polygon))


def rectangle(x, y, width, height):
    return ((x,y), (x+width,y), (x+width,y+height), (x,y+height))


def tiling(a,b,c):
    if not (a >= b > 0 and c*c == a*a + a*b + b*b):
        raise ValueError("Require integer 120-degree tile sides, a >= b > 0.")
    s, k = a*b, a*a+b*b
    p, q = a+2*b, 2*a+b
    A, B, w = a*p, b*q, a*(a+b)
    o, east, north = (0,0), (A,0), (0,B)
    u, v, mid = (2*s,0), (0,2*s), (s,s)
    board = (o,east,north)
    padding = rectangle(-w,0,w,B)
    outer = ((-w,0),east,north,(-w,B))
    regions = [('grid',a,(u,east,mid)), ('grid',b,(mid,north,v)),
               ('grid',c,(east,north,mid))]
    for j in (0,1):
        y = j*s
        x = (1-j)*s-k
        left, right = (x,y),(x+k+s,y)
        top_left, top_right = (x,y+s),(x+k,y+s)
        split = (x+a*a,y+s)
        regions.extend([('grid',a,(left,split,top_left)),
                        ('grid',c,(left,right,split)),
                        ('grid',b,(split,right,top_right))])
        if x > -w:
            regions.append(('cell',(b,a),rectangle(-w,y,w+x,s)))
    regions.append(('cell',(a,b),rectangle(-w,2*s,w,B-2*s)))
    return board, padding, outer, regions


def partition(outer, pieces):
    if not all(cross(p,q,r)>=0 for p,q in edges(outer) for piece in pieces for r in piece):
        raise ValueError("A vertex lies outside the target.")
    if not (all(area(piece)>0 for piece in pieces)
            and sum(area(piece) for piece in pieces)==area(outer)):
        raise ValueError("Area mismatch.")
    for first,second in combinations(pieces,2):
        if not any(all(cross(p,q,r)<=0 for r in rest)
                   for poly,rest in ((first,second),(second,first)) for p,q in edges(poly)):
            raise ValueError("Two cells have intersecting interiors.")


def verify(a,b,c):
    board, pad, outer, regions = tiling(a,b,c)
    partition(outer,[board,pad])
    partition(outer,[poly for _,_,poly in regions])
    count = 0
    for kind,param,poly in regions+[('cell',(a,b),pad)]:
        if kind == 'grid':
            sides = []
            for (x,y),(u,v) in edges(poly):
                dx,dy = u-x,v-y
                sides.append(dx*dx+dx*dy+dy*dy)
            assert sorted(sides)==sorted((param*i)**2 for i in (a,b,c))
            count += param*param
        else:
            x,y = poly[0]
            w,h = poly[2][0]-x,poly[2][1]-y
            dx,dy = param
            assert poly == rectangle(x,y,w,h) and w % dx == h % dy == 0
            assert sorted((dx,dy)) == sorted((a,b)) and dx*dx+dx*dy+dy*dy==c*c
            tiles = 2*(w//dx)*(h//dy)
            if poly == pad:
                padding_tiles=tiles
            else:
                count += tiles
    n=(a+2*b)*(2*a+b)
    assert padding_tiles==2*(a+b)*(2*a+b) and count==n+padding_tiles
    return n,padding_tiles,count


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    for tile in [(33,7,37),(35,13,43)]:
        print(tile, verify(*tile))
    cases = 0
    for u in range(2,90):
        for v in range(1,u):
            if gcd(u,v)!=1:
                continue
            g=gcd(3,u-v)
            a,b=sorted(((u*u-v*v)//g, v*(2*u+v)//g),reverse=True)
            c=(u*u+u*v+v*v)//g
            verify(a,b,c)
            cases += 1
    print("Exact partitions verified for",cases,"additional parameter pairs.")
