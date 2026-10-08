#!/usr/bin/env python3
"""Independent rational polygon-clipping audit of boundary geometry primitives."""
from fractions import Fraction as F
from pathlib import Path
import json
import base_profiles as bp

def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def clip(poly,a,b):
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        dp,dq=det(a,b,p),det(a,b,q)
        if dp>=0:out.append(p)
        if (dp<0<dq) or (dq<0<dp):
            t=F(dp,dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return out

def twicearea(poly):
    return abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1]))) if poly else 0

def intersect(a,b):
    out=list(a)
    for p,q in zip(b,b[1:]+b[:1]):out=clip(out,p,q)
    return twicearea(out)

def run():
    ncontain=0
    for (x,k),ok in bp.OK.items():
        t=bp.triangle(k,x)
        assert ok==(intersect(t,list(bp.T))==twicearea(list(t)))
        ncontain+=1
    for (a,b),ok in bp.PAIR.items():
        assert ok==(intersect(bp.triangle(a,0),bp.triangle(b,bp.DATA[a][3]))==0)
    for (a,b,c),ok in bp.TRIPLE.items():
        assert ok==(intersect(bp.triangle(a,0),bp.triangle(c,bp.DATA[a][3]+bp.DATA[b][3]))==0)
    rec=bp.run()
    assert rec['count_profiles']==2561
    for q in rec['profiles']:
        assert sum(n*d[3] for n,d in zip(q,bp.DATA))==154
        assert q[3]+q[5]>=1 and q[2]+q[4]>=1
    return {'status':'PASS','independent_method':'Exact rational polygon clipping versus separating-axis and half-plane tests','containment_checks':ncontain,'adjacent_pair_checks':len(bp.PAIR),'one_intervening_tile_checks':len(bp.TRIPLE),'full_enumeration_profiles':rec['count_profiles'],'N154_solved':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
