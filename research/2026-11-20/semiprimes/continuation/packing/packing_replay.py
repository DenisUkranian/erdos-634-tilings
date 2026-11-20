"""Expand the two-step scaffolds into exact axial-coordinate unit triangles."""
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'patches'))
from notchshape import make


def add(p, q):
    return p[0] + q[0], p[1] + q[1]


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def mul(k, p):
    return k*p[0], k*p[1]


def div(k, p):
    assert p[0] % k == 0 and p[1] % k == 0
    return p[0]//k, p[1]//k


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def area(polygon):
    return sum(det(p,q) for p,q in edges(polygon))


def pos(polygon):
    return list(polygon if area(polygon) > 0 else polygon[::-1])


def gradtri(points, scale):
    origin, u, v = points
    e = div(scale, sub(u, origin))
    f = div(scale, sub(v, origin))
    for i in range(scale):
        for j in range(scale-i):
            p = add(origin, add(mul(i,e), mul(j,f)))
            q, r = add(p,e), add(p,f)
            yield pos([p,q,r])
            if i+j < scale-1:
                yield pos([q,r,add(q,f)])


def blocks(block):
    points = block['points']
    if block['kind'] == 'triangle':
        yield from gradtri(points, block['scale'])
        return
    p, q, _, s = points
    rows, cols = block['rows'], block['cols']
    e = div(rows, sub(q,p))
    f = div(cols, sub(s,p))
    for i in range(rows):
        for j in range(cols):
            u = add(p, add(mul(i,e), mul(j,f)))
            v, w = add(u,e), add(u,f)
            far = add(v,f)
            if block['diagonal'] == 'sum':
                yield pos([u,v,far])
                yield pos([far,w,u])
            else:
                yield pos([u,v,w])
                yield pos([far,v,w])


def edges(P):
    return zip(P,P[1:]+P[:1])


def norm(p):
    return p[0]**2+p[0]*p[1]+p[1]**2


def separated(A,B):
    return any(all(det(sub(q,p),sub(x,p))<=0 for x in B) for p,q in edges(A))


def disjoint(A,B):
    return separated(A,B) or separated(B,A)


def verify_boundary(polygons):
    lines=defaultdict(Counter)
    for weight,P in polygons:
        assert area(P)>0
        for p,q in edges(P):
            x,y=sub(q,p)
            g=gcd(x,y)
            x,y=x//g,y//g
            if (x,y)<(0,0):
                x,y=-x,-y
            events=lines[x,y,x*p[1]-y*p[0]]
            events[tuple(p)]+=weight
            events[tuple(q)]-=weight
    assert all(not any(v.values()) for v in lines.values())


def inventory(a,b,c):
    s=(c-a)//2
    r=(c-b)//2
    data=make(a,b,c,1,1,[(r,s,1)]*2)
    target=pos(data['target'])
    plus=[]
    minus=[]
    defects=[]
    for B in data['blocks']:
        if B['kind']!='notch':
            plus.extend(blocks(B))
            continue
        X,Y,W,D=B['points']
        t,k=B['scale'],B['notch']
        Z=add(Y,(t*a*c,0))
        plus.extend(gradtri([X,Y,Z],t))
        minus.extend(gradtri([Z,W,D],k))
        defects.append(pos([Z,W,D]))
    return target,plus,minus,defects


def run(a,b,c):
    target,plus,minus,defects=inventory(a,b,c)
    size=sorted((c*s)**2 for s in (a,b,c))
    for P in plus+minus:
        assert sorted(norm(sub(p,q)) for p,q in edges(P))==size
    verify_boundary([(1,P) for P in plus]+[(-1,P) for P in minus]+[(-1,target)])
    bad=[{i for i,P in enumerate(plus) if not disjoint(P,Q)} for Q in defects]
    assert not bad[0].intersection(bad[1])
    removed=bad[0]|bad[1]
    placed=[P for i,P in enumerate(plus) if i not in removed]
    for P in placed:
        assert all(det(sub(q,p),sub(x,p))>=0 for p,q in edges(target) for x in P)
    # A sweep of axial bounding boxes checks all pairs whose interiors might meet.
    boxes=sorted((min(p[0] for p in P),max(p[0] for p in P),
                  min(p[1] for p in P),max(p[1] for p in P),i)
                 for i,P in enumerate(placed))
    live=[]
    for xl,xr,yl,yr,i in boxes:
        live=[item for item in live if item[0]>xl]
        for right,lo,hi,j in live:
            if lo<yr and yl<hi:
                assert disjoint(placed[i],placed[j])
        live.append((xr,yl,yr,i))
    n=(a+2*b)*(2*a+b)
    assert len(plus)-len(minus)==n
    assert (len(plus),len(minus),len(placed),[len(S) for S in bad])=={
        3431:(3559,128,3290,[110,159]),5063:(5071,8,5019,[26,26])}[n]
    if n==5063:
        polygon=[(34400,12986),(35905,12986),(35905,12427),(36465,12635),
                 (38337,11270),(37882,12950),(39754,11585),(39299,13265),
                 (36179,15540),(36634,13860),(34762,15225),(35217,13545),
                 (34400,13545)]
        second=[add(p,(-11180,13545)) for p in polygon]
        assert area(polygon)==22*a*b*c**2
        verify_boundary([(1,P) for P in placed]+[(1,polygon),(1,second),(-1,target)])
    print(n,len(plus),len(minus),len(placed),[len(S) for S in bad])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    run(33,7,37)
    run(35,13,43)
