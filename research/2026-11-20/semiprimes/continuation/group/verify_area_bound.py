"""Verify the two-notch diagram counts and that the gluing arcs are proper."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'packing'))
from packing_replay import inventory, make, verify_boundary


def strictly_between(a,b,c):
    x,y=b[0]-a[0],b[1]-a[1]
    u,v=c[0]-a[0],c[1]-a[1]
    return x*v==y*u and 0<x*u+y*v<u*u+v*v


for a,b,c,N,q in [(33,7,37,3431,128),(35,13,43,5063,8)]:
    board,positive,negative,_=inventory(a,b,c)
    assert (len(positive),len(negative))==(N+q,q)
    verify_boundary([(1,t) for t in positive]+[(-1,t) for t in negative]+[(-1,board)])
    steps=[((c-b)//2,(c-a)//2,1)]*2
    notches=[z for z in make(a,b,c,1,1,steps)['blocks'] if z['kind']=='notch']
    assert len(notches)==2
    for notch in notches:
        X,Y,W,D=notch['points'];Z=(Y[0]+notch['scale']*a*c,Y[1])
        assert strictly_between(Y,W,Z) and strictly_between(X,D,Z)
    print(N,'positive faces',len(positive),'negative faces',q,'total',N+2*q)
