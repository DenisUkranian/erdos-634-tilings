"""Independent Fraction replay with 48 angular intervals and convex clipping."""
from fractions import Fraction as F
from itertools import pairwise


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def sides(poly):
    return pairwise(poly + poly[:1])


def clip(poly, a, b):
    answer = []
    for p, q in sides(poly):
        l, r = dot(a, p) - b, dot(a, q) - b
        if l >= 0:
            answer.append(p)
        if (l > 0 > r) or (r > 0 > l):
            answer.append(tuple((r * v - l * w) / (r - l) for v, w in zip(p, q)))
    return answer


def run():
    # After the unit relaxation, the translation (= first tile vertex)
    # belongs to this generous box. This follows also from applying the
    # five unshifted hull normals to the box and checking their vertices.
    hull = [(0, 0), (-19, 0), (-19, -13), (16, -26), (F(1248,43), F(-910,43))]
    nbs = []
    for (x,y),(u,v) in sides(hull):
        n=(y-v,u-x)
        nbs.append((n,dot(n,(x,y))-abs(n[0])-abs(n[1])))
    # Certify a bounding box from all intersections; somewhat separate
    # from the translation clipping below.
    for i,(a,ca) in enumerate(nbs):
        for b,cb in nbs[i+1:]:
            det=a[0]*b[1]-a[1]*b[0]
            if not det:continue
            p=(F(ca*b[1]-cb*a[1],det),F(a[0]*cb-b[0]*ca,det))
            if all(dot(k,p)>=d for k,d in nbs):
                assert max(abs(p[0]),abs(p[1]))<100
    tested=systems=0
    for k in range(48):
        t=F(2*k+1,96)
        z=1+t+t*t
        rx,ry=(1-t*t)/z,(2*t+t*t)/z
        for _ in range(6):
            for vx,vy in ((35,13),(48,-13)):
                tile=[(F(0),F(0)),(35*rx,35*ry),(vx*rx-vy*ry, vx*ry+vy*(rx+ry))]
                trans=[(-100,-100),(100,-100),(100,100),(-100,100)]
                for a,b in nbs:
                    trans=clip(trans,a,b-min(dot(a,p) for p in tile))
                weights={F(0),F(1)}
                for w,v in sides(tile):
                    x,y=w[0]-v[0],w[1]-v[1]
                    if x!=y and 0<y/(y-x)<1:weights.add(y/(y-x))
                for s in weights:
                    m=(s,1-s)
                    b=dot(m,(15,-14))-min(dot(m,p) for p in tile)
                    assert not clip(trans,m,b)
                    systems+=1
                tested+=1
            rx,ry=-ry,rx+ry
    print('Independent Fraction clipping:',tested,'snapshots,',systems,'infeasible systems')


if __name__=='__main__':
    run()
