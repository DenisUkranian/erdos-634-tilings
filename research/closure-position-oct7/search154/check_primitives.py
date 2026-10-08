#!/usr/bin/env python3
"""Independent rational checks of fan generation and geometric predicates.

This checks primitives and a positive four-tile patch, not search exhaustion.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import json
import random
import subprocess

from check_fixed_search import D, canonical, direction, norm, product, reference_candidates, sub


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def conjugate(a):
    return a[0]+a[1],-a[1]


def argkey(a):
    return 0 if a[1]>0 or a[1]==0 and a[0]>0 else 1


def before(a,b):
    return argkey(a)<argkey(b) or argkey(a)==argkey(b) and cross(a,b)>0


ANGLE_QUOTAS={}
a=(1,0)
m=0
while True:
    b=a
    n=0
    while True:
        if b!=(1,0):
            ANGLE_QUOTAS[b]=(m,n)
        nxt=direction(product(b,(8,7)))
        if not before(b,nxt):break
        b=nxt
        n+=1
    nxt=direction(product(a,(7,8)))
    if not before(a,nxt):break
    a=nxt
    m+=1


def on_segment(p,q,r):
    return cross(sub(q,p),sub(r,p))==0 and all(min(p[k],q[k])<=r[k]<=max(p[k],q[k]) for k in (0,1))


def integral(v):
    from math import isqrt
    n=norm(v)
    return n.denominator==1 and isqrt(n.numerator)**2==n.numerator


def incompatible(a,b):
    separated=False
    for t,u in ((a,b),(b,a)):
        for p,q in zip(t,t[1:]+t[:1]):
            if all(cross(sub(q,p),sub(v,p))<=0 for v in u):
                separated=True
    if not separated:return True
    for t,u in ((a,b),(b,a)):
        for v in t:
            for p,q in zip(u,u[1:]+u[:1]):
                if v!=p and v!=q and on_segment(p,q,v) and not integral(sub(v,p)):
                    return True
    return False


def reference_fans(v,start,end):
    key=direction(product(end,conjugate(start)))
    if key not in ANGLE_QUOTAS:return set()
    answer=set()
    def visit(ray,m,n,placed):
        if m==n==0:
            assert ray==end
            answer.add(tuple(sorted(placed)))
            return
        for _,_,t in reference_candidates(v,ray):
            j=t.index(v)
            p,q=t[(j+1)%3],t[(j+2)%3]
            opposite=norm(sub(q,p))
            a,b=(1,0) if opposite==64 else ((0,1) if opposite==49 else (2,2))
            if a>m or b>n or any(incompatible(t,s) for s in placed):continue
            visit(direction(sub(q,v)),m-a,n-b,placed+(t,))
    visit(start,*ANGLE_QUOTAS[key],())
    return answer


def scalar(x):
    value=Q(x)*D
    assert value.denominator==1
    return str(value.numerator)


def coordinates(t):
    return ' '.join(scalar(x) for p in t for x in p)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('geometry',type=Path)
    ap.add_argument('executable',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    with args.geometry.open() as f:
        scale,np,nt=map(int,f.readline().split())
        assert scale==D
        points=[tuple(Q(x,D) for x in map(int,f.readline().split())) for _ in range(np)]
        triangles=[tuple(points[i] for i in map(int,f.readline().split()[:3])) for _ in range(nt)]
    rng=random.Random(63415408)
    fan_queries=[]
    outer=((Q(0),Q(0)),(Q(154),Q(0)),(Q(49),Q(56)))
    for t in [outer]+rng.sample(triangles,min(100,len(triangles))):
        for j in range(3):
            v=t[j]
            fan_queries.append((v,direction(sub(t[(j+1)%3],v)),direction(sub(t[(j+2)%3],v))))
    requests=[]
    for v,s,e in fan_queries:
        requests.append('F '+' '.join((scalar(v[0]),scalar(v[1]),str(s[0]),str(s[1]),str(e[0]),str(e[1]))))
    pair_queries=[tuple(rng.sample(triangles,2)) for _ in range(1500)]
    # A genuine side-two triangular grid: four unit (8,7,13) tiles.
    a,b,c=(Q(50),Q(10)),(Q(66),Q(10)),(Q(36),Q(24))
    midpoint=lambda p,q:((p[0]+q[0])/2,(p[1]+q[1])/2)
    ab,ac,bc=midpoint(a,b),midpoint(a,c),midpoint(b,c)
    patch=[(a,ab,ac),(ab,b,bc),(ac,bc,c),(ab,bc,ac)]
    pair_queries.extend(combinations(patch,2))
    # Overlap and nonintegral contact controls.
    for t in rng.sample(triangles,100):
        pair_queries.append((t,t))
        pair_queries.append((t,tuple((p[0]+Q(1,13),p[1]) for p in t)))
    # Two triangles on opposite banks of the same line. Integral offset is
    # an admissible partial contact; offset 1/13 violates atomic integrality.
    upper=((Q(50),Q(20)),(Q(58),Q(20)),(Q(43),Q(27)))
    for offset in (Q(1),Q(1,13)):
        lower=((Q(50)+offset,Q(20)),(Q(65)+offset,Q(13)),(Q(58)+offset,Q(20)))
        assert incompatible(upper,lower)==(offset.denominator!=1)
        pair_queries.append((upper,lower))
    for a,b in pair_queries:
        requests.append('I '+coordinates(a)+' '+coordinates(b))
    macro=((Q(50),Q(10)),(Q(66),Q(10)),(Q(36),Q(24)))
    requests.append('B 4 '+coordinates(macro))
    requests[-1]+=' '+' '.join(coordinates(t) for t in patch)
    proc=subprocess.run([str(args.executable)],input='\n'.join(requests)+'\n',text=True,capture_output=True,check=True)
    lines=proc.stdout.splitlines()
    assert len(lines)==len(requests)
    total_fans=0
    for query,line in zip(fan_queries,lines):
        nums=list(map(int,line.split()))
        nf=nums[0]
        cursor=1
        actual=set()
        for _ in range(nf):
            size=nums[cursor];cursor+=1
            fan=[]
            for _ in range(size):
                t=tuple((Q(nums[cursor+2*j],D),Q(nums[cursor+2*j+1],D)) for j in range(3))
                cursor+=6
                fan.append(canonical(t))
            actual.add(tuple(sorted(fan)))
        assert cursor==len(nums)
        assert actual==reference_fans(*query),query
        total_fans+=nf
    outcomes=[]
    for (a,b),line in zip(pair_queries,lines[len(fan_queries):]):
        expected=incompatible(a,b)
        assert bool(int(line))==expected
        outcomes.append(expected)
    assert all(not incompatible(a,b) for a,b in combinations(patch,2))
    assert lines[-1]=='0','Positive four-tile patch did not cancel exactly.'
    report={'status':'PASS','fan_queries':len(fan_queries),'fans_compared':total_fans,
            'incompatibility_queries':len(pair_queries),'incompatible_pairs':sum(outcomes),
            'positive_control':'Four-tile triangular grid; six compatible pairs and exactly zero residual boundary',
            'fan_reference':'Rational six-side permutations and independent alpha/beta angle quotas',
            'N154_decided':False,'search_exhaustion_verified':False,'full_Erdos634_solved':False}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
