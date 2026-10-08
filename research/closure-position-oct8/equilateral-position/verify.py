#!/usr/bin/env python3
"""Independent exact coordinate verification, no import from the search."""
import itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'group2-trapezoids'))
from exact_geometry import norm,sub,area2,contains,intersection_area2,convex

def main():
    path=Path(sys.argv[1]);obj=json.loads(path.read_text());den=obj['denominator'];start=time.monotonic()
    assert obj['format']=='exact_trapezoid_unit_v1';assert obj['tile']==[3,5,7]
    P=[tuple(F(v,den) for v in p) for p in obj['target']]
    T=[[tuple(F(v,den) for v in p) for p in t] for t in obj['triangles']]
    assert convex(P)
    for t in T:
        assert convex(t) and area2(t)==15
        assert sorted(norm(sub(t[(i+1)%3],t[i])) for i in range(3))==[9,25,49]
        assert all(contains(P,p) for p in t)
    for a,b in itertools.combinations(T,2):assert intersection_area2(a,b)==0
    assert sum(map(area2,T))==area2(P)
    out={'verified':True,'tiles':len(T),'pairwise_intersections':len(T)*(len(T)-1)//2,'exact_rational_arithmetic':True,'seconds':time.monotonic()-start}
    path.with_name(path.stem+'_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
