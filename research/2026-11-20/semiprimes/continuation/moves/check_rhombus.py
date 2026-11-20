"""Exact grid exchanges for F2 using integer axial coordinates with denominator c."""
from collections import Counter, defaultdict
from itertools import product
from math import gcd, isqrt


def add(p,q):
    return p[0]+q[0], p[1]+q[1]


def sub(p,q):
    return p[0]-q[0], p[1]-q[1]


def mul(k,p):
    return k*p[0], k*p[1]


def det(p,q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    x,y=p
    return x*x+x*y+y*y


def boundary(polygons):
    events=defaultdict(Counter)
    for polygon in polygons:
        for p,q in zip(polygon, polygon[1:]+polygon[:1]):
            dx,dy=sub(q,p)
            g=gcd(dx,dy)
            ux,uy=dx//g,dy//g
            if (ux,uy)<(0,0):
                ux,uy=-ux,-uy
            line=ux,uy,ux*p[1]-uy*p[0]
            events[line][p]+=1
            events[line][q]-=1
    return {(line,point):v for line,terms in events.items() for point,v in terms.items() if v}


def cells(U,V,n,m):
    for i,j in product(range(n),range(m)):
        p=add(mul(i,U),mul(j,V))
        q,r=add(p,U),add(p,V)
        yield [p,q,r]
        yield [add(q,V),r,q]


def anchor(tri):
    return tuple(sorted(tri))


def check(a,b,c):
    old=list(cells((b*c,0),(c*b,c*a),c,b))
    new=list(cells((c*c,0),(b*b,b*a),b,c))
    hull=[(0,0),(b*c*c,0),(b*c*c+b*b*c,a*b*c),(b*b*c,a*b*c)]
    edges=boundary([hull])
    assert edges==boundary(old)==boundary(new)
    assert len(old)==len(new)==2*b*c
    assert not ({anchor(t) for t in old}&{anchor(t) for t in new})
    p,q=a+2*b,2*a+b
    R=p*(2*a-c)//(q*b)
    allsites=set()
    for j in range(R):
        shift=(0,j*a*b*c)
        for t in old:
            points=[add(s,shift) for s in t]
            key=anchor(points)
            assert key not in allsites
            allsites.add(key)
            # Every original half-cell must be contained, including its furthest corner.
            assert all(x%(b*c)==0 and y%(a*c)==0 for x,y in points)
            grid=[(x//(b*c),y//(a*c)) for x,y in points]
            assert p*max(x for x,y in grid)+q*max(y for x,y in grid)<=p*q
    sq=sorted((c*k)**2 for k in (a,b,c))
    for tr in old+new:
        assert det(sub(tr[1],tr[0]),sub(tr[2],tr[0]))==a*b*c*c
        assert sorted(norm(sub(x,y)) for x,y in zip(tr,tr[1:]+tr[:1]))==sq
    print(f'{p*q}: {len(old)} tiles per switch, {R} independent sites.')


def test_threshold():
    total=0
    for a in range(2,401):
        for b in range(1,a):
            if gcd(a,b)>1:continue
            c=isqrt(a*a+a*b+b*b)
            if c*c!=a*a+a*b+b*b:continue
            p,q=a+2*b,2*a+b
            assert (p*(c+b)+q*b<=p*q)==(a**3-3*a*b*b-b**3>=0)
            if a>=2*b:assert p*(2*a-c)//(q*b)>=1
            total+=1
    print('Verified board threshold on',total,'primitive triples with a <= 400.')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    check(33,7,37)
    check(35,13,43)
    test_threshold()
