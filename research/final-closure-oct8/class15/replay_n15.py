#!/usr/bin/env python3
"""Independent exact proof-tree replay for the equilateral15/(3,5,7) case.

Does not import the search. Uses local tangent-cone classification rather than
residual boundary subtraction, and exact polygon clipping rather than SAT.
Memo references are expanded and checked under every placement history.
"""
from fractions import Fraction as Q
from math import gcd, isqrt
from functools import cmp_to_key
from collections import Counter
from pathlib import Path
import json, hashlib, argparse

if not __debug__:
    raise SystemExit('This checker requires assertions; -O is unsupported.')

D = 3
OUT = ((Q(0), Q(0)), (Q(15), Q(0)), (Q(15,2), Q(15,2)))

def vsub(a,b): return (a[0]-b[0],a[1]-b[1])
def wedge(a,b): return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c): return wedge(vsub(b,a),vsub(c,a))
def scalar(a,b): return a[0]*b[0]+D*a[1]*b[1]
def polyedges(t): return zip(t,t[1:]+t[:1])
def area2(t): return sum(wedge(a,b) for a,b in polyedges(t)) if t else Q(0)
def norm(a):
    s=scalar(a,a); n=isqrt(s.numerator); d=isqrt(s.denominator)
    assert n*n==s.numerator and d*d==s.denominator
    return Q(n,d)
def point(x): return tuple(map(Q,x))
def unit(a):
    n=norm(a); assert n>0
    return (a[0]/n,a[1]/n)
def cmul(a,b): return (a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cpow(a,k):
    r=(Q(1),Q(0))
    for _ in range(k): r=cmul(r,a)
    return r

# Independent bounded angle inventory. alpha>pi/12 and beta>pi/6
# follow from the exact cosines13/14 and11/14; gamma=2pi/3.
# Thus i+2j+8k<12 is necessary for total<pi. Conversely these bounds
# and alpha<pi/6,beta<pi/3 imply total<2pi, so positive sine tests<pi.
rotations=((Q(13,14),Q(3,14)),(Q(11,14),Q(5,14)),(Q(-1,2),Q(1,2)))
FANS={(Q(1),Q(0))}
for i in range(12):
    for j in range(6):
        for k in range(2):
            if i+2*j+8*k>=12 or i+j+k==0: continue
            z=cmul(cmul(cpow(rotations[0],i),cpow(rotations[1],j)),cpow(rotations[2],k))
            if z[1]>0:FANS.add(z)
assert len(FANS)==26


def clip(subject, boundary):
    """Exact convex intersection, no separating-axis predicate."""
    result=list(subject)
    for a,b in polyedges(boundary):
        old=result; result=[]
        if not old: break
        for p,q in zip(old,old[1:]+old[:1]):
            fp,fq=orient(a,b,p),orient(a,b,q)
            if fp>=0: result.append(p)
            if (fp<0<fq) or (fq<0<fp):
                lam=fp/(fp-fq)
                result.append((p[0]+lam*(q[0]-p[0]),p[1]+lam*(q[1]-p[1])))
    return result


def raykey(x):
    den=x[0].denominator*x[1].denominator
    a,b=int(x[0]*den),int(x[1]*den); g=gcd(abs(a),abs(b)); assert g
    return (a//g,b//g)

def raycmp(a,b):
    # Counterclockwise order from the negative x axis; exact comparisons.
    lowera=(a[1]<0 or (a[1]==0 and a[0]<0))
    lowerb=(b[1]<0 or (b[1]==0 and b[0]<0))
    if lowera != lowerb: return -1 if lowera else 1
    z=wedge(a,b)
    return -1 if z>0 else (1 if z<0 else 0)

def interior_near(poly,p,w):
    # Whether p+epsilon*w is strictly inside for every sufficiently small
    # epsilon>0. Exact lexicographic sign, no epsilon chosen numerically.
    for a,b in polyedges(poly):
        f=orient(a,b,p)
        if f<0 or (f==0 and wedge(vsub(b,a),w)<=0): return False
    return True

def local_rays(poly,p):
    if any(orient(a,b,p)<0 for a,b in polyedges(poly)): return set()
    ans=set()
    for a,b in polyedges(poly):
        if orient(a,b,p)==0:
            for z in (a,b):
                if z!=p: ans.add(raykey(vsub(z,p)))
    return ans

def between(a,b):
    z=wedge(a,b)
    if z>0: return (a[0]+b[0],a[1]+b[1])
    if z<0: return (-a[0]-b[0],-a[1]-b[1])
    # Distinct normalized rays are antiparallel in this case.
    return (-a[1],a[0])

def certify_corner(encoded, placed):
    p,d,r,phi=map(point,encoded)
    assert wedge(d,r)>0
    du,ru=unit(d),unit(r)
    assert phi==(scalar(du,ru),wedge(du,ru))
    assert all(orient(a,b,p)>=0 for a,b in polyedges(OUT))
    assert not any(all(orient(a,b,p)>0 for a,b in polyedges(t)) for t in placed)
    rays=local_rays(OUT,p)
    for t in placed: rays |= local_rays(t,p)
    rays=sorted(rays,key=cmp_to_key(raycmp))
    dk,rk=raykey(d),raykey(r)
    assert dk in rays and rk in rays
    j=rays.index(dk); assert rays[(j+1)%len(rays)]==rk
    def allowed(w): return interior_near(OUT,p,w) and not any(interior_near(t,p,w) for t in placed)
    assert allowed(between(dk,rk))
    assert not allowed(between(rays[(j-1)%len(rays)],dk))
    assert not allowed(between(rk,rays[(j+2)%len(rays)]))
    return p,du,phi


def all_candidates(encoded,placed):
    p,d,phi=certify_corner(encoded,placed)
    ans={}
    if phi not in FANS: return ans
    for opposite in (3,5,7):
        adjacent=[s for s in (3,5,7) if s!=opposite]
        for s,t in (adjacent,adjacent[::-1]):
            cs=Q(s*s+t*t-opposite*opposite,2*s*t)
            sn=Q(15,2*s*t)
            assert cs*cs+D*sn*sn==1
            remaining=cmul(phi,(cs,-sn))
            if remaining not in FANS: continue
            e=cmul(d,(cs,sn))
            tri=(p,(p[0]+s*d[0],p[1]+s*d[1]),(p[0]+t*e[0],p[1]+t*e[1]))
            assert area2(tri)==Q(15,2)
            assert sorted(scalar(vsub(a,b),vsub(a,b)) for a,b in polyedges(tri))==[9,25,49]
            if any(orient(a,b,x)<0 for a,b in polyedges(OUT) for x in tri): continue
            if any(area2(clip(tri,old))>0 for old in placed): continue
            assert tri not in ans
            ans[tri]=(opposite,s,t)
    return ans


def run():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',nargs='?',type=Path,default=Path(__file__).resolve().with_name('e120_n15_refutation.json'))
    args=parser.parse_args()
    file=Path(args.certificate); raw=file.read_bytes(); cert=json.loads(raw)
    assert cert['status']=='UNSAT' and cert['tile_sides']==[3,5,7] and cert['D']==3
    assert tuple(map(point,cert['target']))==OUT
    tree=cert['tree']; assert len(tree)==cert['nodes']==102
    stats=Counter(); visited=set(); maxdepth=0
    def visit(index,placed):
        nonlocal maxdepth
        assert 0<=index<len(tree)
        node=tree[index]; depth=len(placed)
        assert node['depth']==depth and node['result']=='UNSAT' and depth<15
        stats['expanded_nodes']+=1; maxdepth=max(maxdepth,depth); visited.add(index)
        possible=all_candidates(node['corner'],placed)
        children=node['children']; assert len(children)==len(possible)
        seen=set()
        for child in children:
            tri=tuple(map(point,child['triangle']))
            assert tri in possible and tri not in seen; seen.add(tri)
            opposite,s,t=possible[tri]
            assert child['angle']=={3:'alpha',5:'beta',7:'gamma'}[opposite]
            assert (child['first_side'],child['second_side'])==(s,t)
            visit(child['node'],placed+[tri])
        if not children: stats['expanded_dead_ends']+=1
    visit(0,[])
    assert len(visited)==len(tree)
    result={'result':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'certificate_nodes':len(tree),'all_nodes_reachable':True,'expanded_nodes_without_memoization':stats['expanded_nodes'],'expanded_dead_ends':stats['expanded_dead_ends'],'maximum_depth':maxdepth,'angle_fans':len(FANS),'methods':{'corner':'exact local tangent cones; no residual-boundary subtraction','overlap':'exact rational convex polygon clipping','angle_inventory':'bounded integer-triple enumeration','memoization':'not trusted; every incoming placement history rechecked'},'scope':'No tiling of equilateral side15 by15 congruent (3,5,7) triangles, allowing reflections and arbitrary T-junctions. Global exclusion of N=15 additionally uses the exhaustive arithmetic reduction.'}
    print(json.dumps(result,indent=2))

if __name__=='__main__': run()
