#!/usr/bin/env python3
"""Check a unit certificate using only Python integers, no other project code.

Pairwise nonoverlap uses the separating-axis theorem. Boundary cancellation
uses independently grouped collinear intervals, not the search lattice atoms.
"""
import argparse,collections,itertools,json,math,time
from pathlib import Path

def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]
def area2(P):return sum(cross(p,q) for p,q in zip(P,P[1:]+P[:1]))
def interior_disjoint(A,B):
    for P in (A,B):
        for p,q in zip(P,P[1:]+P[:1]):
            v=sub(q,p);a=[cross(v,w) for w in A];b=[cross(v,w) for w in B]
            if max(a)<=min(b) or max(b)<=min(a):return True
    return False

def verify(path):
    start=time.monotonic();c=json.loads(path.read_text());d=c['denominator'];P=c['target'];T=c['triangles']
    assert type(d) is int and d>0 and c['tile']==[3,5,7]
    assert all(type(v) is int for p in P for v in p)
    assert all(type(v) is int for tri in T for p in tri for v in p)
    assert len(P)>=3 and area2(P)>0
    for i in range(len(P)):
        assert cross(sub(P[(i+1)%len(P)],P[i]),sub(P[(i+2)%len(P)],P[(i+1)%len(P)]))>0
    for t in T:
        assert len(t)==3 and area2(t)==15*d*d
        assert sorted(norm(sub(t[(i+1)%3],t[i])) for i in range(3))==[9*d*d,25*d*d,49*d*d]
        for p,q in zip(P,P[1:]+P[:1]):
            assert all(cross(sub(q,p),sub(w,p))>=0 for w in t)
    pairs=0
    for A,B in itertools.combinations(T,2):
        assert interior_disjoint(A,B);pairs+=1
    assert sum(map(area2,T))==area2(P)
    lines=collections.defaultdict(lambda:collections.defaultdict(int))
    for polygon,weight in [(t,1) for t in T]+[(P,-1)]:
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            v=sub(q,p);g=math.gcd(*v);u=(v[0]//g,v[1]//g);sg=1
            if u<(0,0):u=(-u[0],-u[1]);sg=-1
            offset=cross(u,p);a=u[0]*p[0]+u[1]*p[1];b=u[0]*q[0]+u[1]*q[1]
            lo,hi=sorted((a,b));assert lo<hi
            line=lines[u,offset];line[lo]+=sg*weight;line[hi]-=sg*weight
    checked_intervals=0
    for line in lines.values():
        balance=0;points=sorted(line)
        for i,p in enumerate(points):
            balance+=line[p]
            if i<len(points)-1:assert balance==0;checked_intervals+=1
        assert balance==0
    out={'status':'EXACT_PASS','method':'integer separating axes plus collinear interval boundary cancellation',
         'tile':[3,5,7],'count':len(T),'pair_checks':pairs,'lines_checked':len(lines),'boundary_intervals_checked':checked_intervals,
         'target_area2_scaled':area2(P),'coordinate_denominator':d,'seconds':time.monotonic()-start,
         'independent_from_search_and_other_geometry_checker':True}
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('certificate',type=Path);args=a.parse_args()
    result=verify(args.certificate);print(json.dumps(result,indent=2))
    args.certificate.with_name(args.certificate.stem+'_independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
