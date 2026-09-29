#!/usr/bin/env python3
"""Independent replay of two FIXED-collar nonextendability certificates.

No search imports, polygon subtraction, stitching, numeric angles, or node cap.
At every proof node the actual local empty sector is reconstructed directly
from the incident placed triangles. Pair intersections use rational clipping.
This certifies only the two named fixed partial configurations, not N=105.
"""
from collections import deque
from fractions import Fraction as F
from functools import cmp_to_key
from hashlib import sha256
from math import gcd,isqrt
from pathlib import Path
import json,sys

if not __debug__:
    raise SystemExit('Verification requires assertions; disable neither assertions nor checks.')
REPO=Path(__file__).resolve().parents[1]
DATA=REPO/"data"

def vsub(a,b):return (a[0]-b[0],a[1]-b[1])
def determinant(a,b):return a[0]*b[1]-a[1]*b[0]
def turn(a,b,p):return determinant(vsub(b,a),vsub(p,a))
def area2(p):return sum(determinant(a,b) for a,b in zip(p,p[1:]+p[:1]))
def length(v):
    q=v[0]*v[0]+v[0]*v[1]+v[1]*v[1]
    n,d=isqrt(q.numerator),isqrt(q.denominator)
    assert n*n==q.numerator and d*d==q.denominator
    return F(n,d)
def ray(v):
    d=v[0].denominator*v[1].denominator
    x,y=int(v[0]*d),int(v[1]*d);g=gcd(abs(x),abs(y))
    assert g
    return (x//g,y//g)
def order(a,b):
    ha=(a[1]<0 or (a[1]==0 and a[0]<0))
    hb=(b[1]<0 or (b[1]==0 and b[0]<0))
    if ha!=hb:return 1 if ha else -1
    t=determinant(a,b)
    return -1 if t>0 else (1 if t<0 else 0)
def product(a,b):return (a[0]*b[0]-3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])

def clipping(subject,triangle):
    p=list(subject)
    for i in range(3):
        if not p:break
        a,b=triangle[i],triangle[(i+1)%3];q=[]
        for u,v in zip(p,p[1:]+p[:1]):
            su,sv=turn(a,b,u),turn(a,b,v)
            if su>=0:q.append(u)
            if su*sv<0:
                r=su/(su-sv)
                q.append((u[0]+r*(v[0]-u[0]),u[1]+r*(v[1]-u[1])))
        p=q
    return p

def exact_angle_sums(angles):
    """BFS of all nonnegative angle sums strictly below 2pi, including 0."""
    zero=(F(1),F(0));seen={zero};todo=deque([zero])
    while todo:
        x=todo.popleft()
        for a in angles:
            y=product(x,a)
            # Each tile angle lies in (0,pi). Decreasing circular order means
            # the sum crossed 2pi; equality with 0 also fails this inequality.
            if order(x,y)<0 and y not in seen:
                seen.add(y);todo.append(y)
    return seen

def empty_sector(P,u,w,placed):
    """Validate the precise maximal local residual sector CCW from u to w."""
    assert determinant(u,w)>0  # Selected sector is strictly convex.
    outer=((F(0),F(0)),(F(105),F(0)),(F(0),F(105)))
    outer_active=[];incident=[];directions={ray(u),ray(w),ray((-u[0],-u[1])),ray((-w[0],-w[1]))}
    for i in range(3):
        a,b=outer[i],outer[(i+1)%3];s=turn(a,b,P)
        assert s>=0
        if s==0:outer_active.append(vsub(b,a))
    for t in placed:
        signs=[turn(t[i],t[(i+1)%3],P) for i in range(3)]
        if any(s<0 for s in signs):continue
        assert any(s==0 for s in signs),'Chosen proof corner lies inside a placed tile.'
        incident.append([vsub(t[(i+1)%3],t[i]) for i,s in enumerate(signs) if s==0])
    for v in outer_active+[v for sides in incident for v in sides]:
        directions.add(ray(v));directions.add(ray((-v[0],-v[1])))
    ds=sorted(directions,key=cmp_to_key(order));n=len(ds)
    empty=[]
    for a,b in zip(ds,ds[1:]+ds[:1]):
        if determinant(a,b)==0:
            # Antipodal adjacent rays: rotate a through exactly 60 degrees.
            sample=(-a[1],a[0]+a[1])
        else:
            sample=(a[0]+b[0],a[1]+b[1])
        inside=all(determinant(v,sample)>0 for v in outer_active)
        covered=any(all(determinant(v,sample)>0 for v in sides) for sides in incident)
        empty.append(inside and not covered)
    first,last=ds.index(ray(u)),ds.index(ray(w));k=first
    assert not empty[(first-1)%n] and not empty[last]
    while k!=last:
        assert empty[k],'Certified local sector is obstructed.'
        k=(k+1)%n
    nu,nw=length(u),length(w)
    cosine=(2*u[0]*w[0]+u[0]*w[1]+u[1]*w[0]+2*u[1]*w[1])/(2*nu*nw)
    sine_coefficient=determinant(u,w)/(2*nu*nw)
    return (cosine,sine_coefficient)

def verify(a,b,c,count,expected_hash):
    collar_path=DATA/f'n105-collar-{a}-{b}-{c}.json'
    proof_path=DATA/f'n105-collar-refutation-{a}-{b}-{c}.json'
    raw=collar_path.read_bytes();obj=json.loads(raw);pr=json.loads(proof_path.read_text())
    assert sha256(raw).hexdigest()==expected_hash==pr['collar_sha256']
    assert pr['format']=='fixed-collar-corner-refutation-v1' and pr['root']==0
    assert pr['tile']==obj['tile']==[a,b,c] and pr['target_side']==obj['side']==105
    assert obj['count']==count and obj['vertices_are_oblique'] is True
    D=obj['scale'];assert type(D) is int and D>0
    initial=tuple(tuple((F(x,D),F(y,D)) for x,y in t) for t in obj['triangles'])
    assert len(initial)==count
    tests=0
    for i,t in enumerate(initial):
        assert len(t)==3 and area2(t)==a*b
        assert all(x>=0 and y>=0 and x+y<=105 for x,y in t)
        assert sorted(length(vsub(q,p)) for p,q in zip(t,t[1:]+t[:1]))==sorted([a,b,c])
        for other in initial[:i]:
            assert area2(clipping(t,other))==0;tests+=1
    cosines=(F(b*b+c*c-a*a,2*b*c),F(a*a+c*c-b*b,2*a*c),F(1,2))
    angles=tuple(zip(cosines,(F(a,2*c),F(b,2*c),F(1,2))))
    sums=exact_angle_sums(angles);adjacent=((b,c),(a,c),(a,b))
    nodes=pr['nodes'];visited=set();leaves=maxdepth=0
    def replay(index,placed,depth):
        nonlocal tests,leaves,maxdepth
        assert type(index) is int and 0<=index<len(nodes) and index not in visited
        visited.add(index);node=nodes[index];maxdepth=max(maxdepth,depth)
        assert len(placed)<105
        P=tuple(map(F,node['point']));u=tuple(map(F,node['outgoing_unit']));w=tuple(map(F,node['incoming_back']))
        assert length(u)==1
        theta=empty_sector(P,u,w,placed)
        assert theta in sums
        eligible=[]
        for k,z in enumerate(angles):
            rest=product(theta,(z[0],-z[1]))
            if order(z,theta)<=0 and rest in sums:eligible.append(k)
        assert eligible==node['eligible_corner_types']
        possible={}
        for k in eligible:
            cs,sn=angles[k]
            ux=u[0]+u[1]/2;uy=u[1]/2
            rx=cs*ux-3*sn*uy;ry=sn*ux+cs*uy
            v=(rx-ry,2*ry)
            for swap in (0,1):
                l,m=adjacent[k][swap],adjacent[k][1-swap]
                t=(P,(P[0]+l*u[0],P[1]+l*u[1]),(P[0]+m*v[0],P[1]+m*v[1]))
                assert area2(t)==a*b
                if any(x<0 or y<0 or x+y>105 for x,y in t):continue
                blocked=False
                for other in placed:
                    tests+=1
                    if area2(clipping(t,other))>0:blocked=True;break
                if not blocked:possible[str(2*k+swap)]=t
        assert set(possible)==set(node['children']),'Missing or extraneous complete-search branch.'
        if not possible:leaves+=1
        for branch,t in possible.items():replay(node['children'][branch],placed+(t,),depth+1)
    replay(0,initial,0)
    assert len(visited)==len(nodes)
    assert (len(nodes),leaves,maxdepth)==(1,1,0)
    return dict(verdict='PASS_FIXED_COLLAR_NONEXTENDABILITY',tile=[a,b,c],
                fixed_collar_tiles=count,collar_sha256=expected_hash,
                proof_file=proof_path.name,proof_sha256=sha256(proof_path.read_bytes()).hexdigest(),
                complete_proof_nodes=len(nodes),leaves=leaves,max_added_tiles=maxdepth,
                rational_clipping_pair_tests=tests,angle_sum_keys=len(sums),
                search_imported=False,polygon_subtraction_used=False,
                local_empty_sectors_verified_directly=True,node_cap=None,
                global_N105_decided=False)

if __name__=='__main__':
    if len(sys.argv)>2:
        raise SystemExit('Usage: verify_n105_collar_refutations.py [DATA_DIRECTORY]')
    if len(sys.argv)==2:
        DATA=Path(sys.argv[1])
    claims=[(5,21,19,45,'3c00405995fb0a4d92c8c987e1a7bd69a51fe292c2a54566ed50ebf4ec98b3f5'),
            (7,15,13,57,'a986ec475db0ecccfe4cc46d740d4c64158be510e6aba80a0869e974a08d6b24')]
    print(json.dumps(dict(verdict='PASS',scope='two_fixed_collars_only',
                          global_N105_decided=False,results=[verify(*x) for x in claims]),indent=2))
