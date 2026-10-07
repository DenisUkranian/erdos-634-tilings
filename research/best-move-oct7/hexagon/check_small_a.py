#!/usr/bin/env python3
"""Independent exact macro and supplied-unit certificate verifier.

No construction code or geometric helper is imported.
"""
import argparse
import json
from fractions import Fraction as F
from math import gcd, isqrt
from pathlib import Path

def sub(p,q): return p[0]-q[0],p[1]-q[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def area2(p): return sum(det(x,y) for x,y in zip(p,p[1:]+p[:1]))
def norm(p): return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def ccw(p): return p if area2(p)>0 else p[::-1]
def inside(poly,p):
    return all(det(sub(q,r),sub(p,r))>=0 for r,q in zip(poly,poly[1:]+poly[:1]))
def separate(p,q):
    return any(all(det(sub(y,x),sub(v,x))<=0 for v in other)
               for poly,other in ((p,q),(q,p))
               for x,y in zip(poly,poly[1:]+poly[:1]))
def sides(poly): return sorted(norm(sub(p,q)) for p,q in zip(poly,poly[1:]+poly[:1]))

def macro(a,b,c):
    assert 0<a<b and c*c==a*a+a*b+b*b
    A,B=a*b,b*b
    X,Y,K=(-a*a,0),(2*A,-2*A-B),(2*A,A+2*B)
    P,E,L,R=(A,-A),(2*A,-2*A),(A,A+B),(2*A,A+B)
    target=ccw([X,Y,K])
    regions=[ccw(p) for p in [[X,Y,P],[Y,P,E],[L,R,K],[X,P,L],[E,P,L,R]]]
    for poly in regions:
        assert area2(poly)>0
        assert all(inside(target,p) for p in poly)
    for i,p in enumerate(regions):
        assert all(separate(p,q) for q in regions[i+1:])
    assert sum(area2(p) for p in regions)==area2(target)
    for poly,k in zip(regions[:3],(c,b,b)):
        assert sides(poly)==sorted((k*s)**2 for s in (a,b,c))
    assert sides(regions[3])==sorted(s*s for s in (a*c,b*(2*a+b),c*(a+b)))
    x=2*A+B
    assert sides(regions[4])==sorted(s*s for s in (x,x+A,A,A))
    assert area2(regions[4])==A*(2*x+A)
    d=a+b-c
    seed=a*a+b*b-a*d
    assert x-seed==a*(3*b-c)>0
    assert area2(target)==A*3*(a+b)*(a+2*b)
    assert sides(target)==sorted(s*s for s in (c*c,c*(a+2*b),3*b*(a+b)))
    return {'tile':[a,b,c], 'count':3*(a+b)*(a+2*b),
            'macroregions':5,'macro_pairs_checked':10,
            'trapezoid_seed':seed,'trapezoid_added_width':x-seed}

def units(path):
    data=json.loads(Path(path).read_text())
    a,b,c=data['tile'];m=data['multiplier']
    assert isinstance(m,int) and m>0
    macro(a,b,c)
    read=lambda p:[(F(x),F(y)) for x,y in p]
    target=ccw(read(data['target']))
    A,B=a*b,b*b
    assert set(target)=={(-m*a*a,F(0)),(2*m*A,m*(-2*A-B)),(2*m*A,m*(A+2*B))}
    triangles=[ccw(read(t)) for t in data['triangles']]
    assert data['count']==len(triangles)==3*(a+b)*(a+2*b)*m*m
    wanted=sorted(s*s for s in (a,b,c))
    boxes=[]
    for tri in triangles:
        assert len(tri)==3 and area2(tri)==A and sides(tri)==wanted
        assert all(inside(target,p) for p in tri)
        boxes.append((min(p[0] for p in tri),max(p[0] for p in tri),
                      min(p[1] for p in tri),max(p[1] for p in tri)))
    assert sum(area2(t) for t in triangles)==area2(target)
    order=sorted(range(len(triangles)),key=lambda i:boxes[i][0])
    checked=0
    for ii,i in enumerate(order):
        bx=boxes[i]
        for j in order[ii+1:]:
            by=boxes[j]
            if by[0]>=bx[1]: break
            if by[3]<=bx[2] or bx[3]<=by[2]: continue
            checked+=1
            assert separate(triangles[i],triangles[j]),f'Overlapping pair {i},{j}'
    return {'file':Path(path).name,'tile':[a,b,c],'multiplier':m,'count':len(triangles),
            'all_pairs':len(triangles)*(len(triangles)-1)//2,
            'exact_candidate_pairs_checked':checked,'verified':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificates',nargs='*')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    certificates=args.certificates or [Path(__file__).with_name(name)
                                      for name in ('f3-312.json','f3-2331.json')]
    rows=[]
    for b in range(2,501):
        for a in range(1,b):
            c=isqrt(a*a+a*b+b*b)
            if gcd(a,b)==1 and c*c==a*a+a*b+b*b:
                rows.append(macro(a,b,c))
    extra=macro(136,209,301)
    result={'status':'PASS','primitive_b_max':500,'macro_cases':len(rows),
            'large_example':extra,'unit_checks':[units(p) for p in certificates],
            'full_Erdos634_solved':False}
    encoded=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(encoded)
    print(encoded)
