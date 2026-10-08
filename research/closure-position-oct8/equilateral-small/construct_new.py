#!/usr/bin/env python3
"""Expand the new 180-tile trapezoid into equilateral triangle tilings.

This generator uses ordinary triangle grids and 3-by-5 parallelogram
cells for every auxiliary region. Output contains every unit triangle.
It does not import the search engine or a verification result.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
SEED=HERE.parent/'equilateral-position'/'cpsat'/'T30_30_0-1_certificate.json'
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def scale(a,s):return a[0]*s,a[1]*s
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def ccw(t):
    t=tuple(t)
    return t if det(sub(t[1],t[0]),sub(t[2],t[0]))>0 else (t[0],t[2],t[1])
def rot(p,k):
    x,y=p
    for _ in range(k%3):x,y=-x-y,x
    return x,y
def grid(tri,n):
    A,B,C=map(lambda p:tuple(map(F,p)),tri)
    U,V=scale(sub(B,A),F(1,n)),scale(sub(C,A),F(1,n))
    for i in range(n):
        for j in range(n-i):
            O=add(A,add(scale(U,i),scale(V,j)))
            yield ccw((O,add(O,U),add(O,V)))
            if i+j<n-1:yield ccw((add(O,U),add(add(O,U),V),add(O,V)))
def semigroup(w):
    for p in range(w//3+1):
        if (w-3*p)%5==0:return p,(w-3*p)//5
    raise ValueError(f'No nonnegative 3,5 representation for {w}')
def one_band(x):
    """T(x,15), for x-34 in <3,5>."""
    if x<34:raise ValueError('Auxiliary short base below basic seed')
    A=(0,0);B=(49,0);C=(34,15);D=(0,15);E=(25,15)
    result=list(grid((A,E,D),5))+list(grid((A,B,E),7))+list(grid((E,B,C),3))
    p,q=semigroup(x-34);offset=0
    for width,height in [(3,5)]*p+[(5,3)]*q:
        U=(F(width),F(0));V=(F(-height),F(height))
        for j in range(15//height):
            O=(F(49+offset-j*height),F(j*height))
            result.extend((ccw((O,add(O,U),add(O,V))),ccw((add(O,U),add(add(O,U),V),add(O,V)))))
        offset+=width
    assert len(result)==2*x+15
    return result
def usual_trapezoid(x,L):
    assert L>0 and L%15==0
    n=L//15;result=[]
    for j in range(n):
        result.extend(tuple(add(p,(0,15*j)) for p in tri) for tri in one_band(x+15*(n-j-1)))
    assert len(result)==L*(2*x+L)//15
    return result
def read_seed():
    obj=json.loads(SEED.read_text());d=obj['denominator']
    assert obj['tile']==[3,5,7]
    assert obj['target']==[[0,0],[60*d,0],[30*d,30*d],[0,30*d]]
    result=[tuple(tuple(F(v,d) for v in p) for p in tri) for tri in obj['triangles']]
    assert len(result)==180
    return result
def T(x,L,seed):
    if x==30 and L==30:return seed
    if x==30 and L>30 and L%15==0:
        return usual_trapezoid(60,L-30)+[tuple(add(p,(0,L-30)) for p in tri) for tri in seed]
    return usual_trapezoid(x,L)
def encode(data):
    out=[]
    for poly in data:
        p=[]
        for vertex in poly:
            scaled=[F(v)*7 for v in vertex]
            assert all(v.denominator==1 for v in scaled)
            p.append([int(v) for v in scaled])
        out.append(p)
    return out
def assemble(r,s,t,seed):
    S=15*(r+s+t)
    settings=[(15*r,15*t,(15*s,0),0),(15*t,15*s,(0,15*(s+t)),2),(15*s,15*r,(15*(s+r),15*t),1)]
    triangles=[];blocks=[]
    for x,L,origin,k in settings:
        local=T(x,L,seed);start=len(triangles)
        triangles.extend(ccw(add(rot(p,k),origin) for p in tri) for tri in local)
        blocks.append({'short_base':x,'leg':L,'rotation_120_turns':k,'translation':list(origin),'first_tile_index':start,'count':len(local)})
    assert len(triangles)==S*S//15
    return {'format':'exact_polygon_unit_v1','coordinate_convention':'(u,v)/denominator denotes (u+v/2, sqrt(3)*v/2)/denominator','denominator':7,'tile':[3,5,7],'target':encode([[(0,0),(S,0),(0,S)]])[0],'triangles':encode(triangles),'tile_count':len(triangles),'target_side':S,'construction_blocks':blocks,'seed_sha256':hashlib.sha256(SEED.read_bytes()).hexdigest(),'claim':'Explicit tiling of this fixed equilateral triangle; not a full solution of Erdos634'}
def main():
    seed=read_seed()
    for params in ((2,2,2),(2,2,3),(2,3,3)):
        obj=assemble(*params,seed);out=HERE/f"equilateral_{obj['tile_count']}.json";out.write_text(json.dumps(obj,indent=2)+'\n');print(out.name,obj['tile_count'],len(obj['triangles']))
    obj={'format':'exact_polygon_unit_v1','denominator':7,'tile':[3,5,7],'target':encode([[(0,0),(75,0),(30,45),(0,45)]])[0],'triangles':encode(T(30,45,seed)),'tile_count':315}
    (HERE/'T30_45_315.json').write_text(json.dumps(obj,indent=2)+'\n')
if __name__=='__main__':main()
