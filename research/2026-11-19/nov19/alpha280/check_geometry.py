"""Exact metric checks and optional full survival test for Bonfioli's theta8 tiling."""
from fractions import Fraction as F
from itertools import combinations, product
import argparse

def delta(p, q):
    return (p[0] - q[0], p[1] - q[1])

def dist2(p, q):
    x, y = delta(p, q)
    return x*x + 2*y*y

def area2(a,b,c):
    x,y=delta(b,a); u,v=delta(c,a)
    return x*v-y*u

def diameter(s,t):
    def leg(x):
        return (F((14-x)*7,9), F((14-x)*4,9))
    a,b=leg(s); c,d=leg(t)
    points=[(s,0),(a,b),(70,40),(140-c,d),(140-t,0)]
    return max(dist2(p,q) for p,q in combinations(points,2))

def witness(source, pool):
    with open(source) as f:
        triangles=[[tuple(map(F,w[i:i+2])) for i in (0,2,4)] for line in f
                   if not line.startswith('#') and (w:=line.split())]
    target=[(0,0),(80,0),(40,80)]
    assert len(triangles)==320
    for t in triangles:
        assert sorted(dist2(u,v) for u,v in combinations(t,2))==[25,36,81]
        assert all(area2(target[i-1],target[i],p)>=0 for p in t for i in range(3))
        assert abs(area2(*t))==20
        if area2(*t)<0:
            t.reverse()
    for s,t in combinations(triangles,2):
        assert any(all(area2(a[k-1],a[k],v)<=0 for v in b) for a,b in ((s,t),(t,s)) for k in range(3))
    assert sum(area2(*t) for t in triangles)==area2(*target)
    with open(pool+'.shapes') as f:
        assert list(map(int,next(f).split()))==[9,320,20]
        shapeids={tuple(map(int,line.split())):i for i,line in enumerate(f)}
    expected=set()
    for t in triangles:
        for i in range(3):
            p,q,r=t[i:]+t[:i]
            if dist2(q,r)!=81:
                continue
            a=delta(q,p); b=delta(r,p)
            expected.add((shapeids[tuple(9*v for v in (*a,*b))],9*p[0],9*p[1]))
    assert len(expected)==320
    with open(pool) as f:
        assert list(map(int,next(f).split()))==[9,320,456106]
        for line in f:
            expected.discard(tuple(map(int,line.split())))
    assert not expected
    print("Verified all 320 exact unit cells and found each in the surviving pool.")

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--theta8-witness')
    parser.add_argument('--pool')
    args=parser.parse_args()
    assert sorted(dist2(p,q) for p,q in combinations([(0,0),(140,0),(70,40)],2))==[90**2,90**2,140**2]
    assert sorted(dist2(p,q) for p,q in combinations([(50,0),(140,0),(70,40)],2))==[60**2,90**2,90**2]
    assert sorted(dist2(p,q) for p,q in combinations([(50,0),(90,0),(70,40)],2))==[40**2,60**2,60**2]
    print("Pentagon diameter squared for the four orientations of the two corner tiles")
    for s,t in product((5,9),repeat=2):
        d=diameter(s,t)
        assert d < 138**2
        print(s,t,d)
    if args.theta8_witness and args.pool:
        witness(args.theta8_witness,args.pool)
