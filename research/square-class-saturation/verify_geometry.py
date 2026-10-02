"""Independent exact verification of a complete compressed-grid dissection.
Does not import the arithmetic classifier or construction generator.
Checks metric, target sides, every primitive grid cell, exact area, containment,
and every pair of macroregions by rational convex clipping.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
from math import gcd


def req(ok,msg):
    if not ok:raise ValueError(msg)
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def det(a,b,c):return cross(sub(b,a),sub(c,a))
def area(poly):return sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
def ccw(p):
    req(area(p)!=0,'Degenerate polygon')
    return p if area(p)>0 else list(reversed(p))
def norm(p,D):return p[0]**2+D*p[1]**2
def decode(p):
    req(isinstance(p,list) and len(p)==2,'Malformed coordinate')
    result=[]
    for q in p:
        req(isinstance(q,list) and len(q)==2 and all(type(z) is int for z in q) and q[1]>0,'Malformed rational')
        result.append(F(*q))
    return tuple(result)
def clip(poly,cutter):
    out=poly[:]
    for i,a in enumerate(cutter):
        b=cutter[(i+1)%len(cutter)];old=out;out=[]
        if not old:break
        prev=old[-1];dp=det(a,b,prev)
        for cur in old:
            dc=det(a,b,cur)
            if (dp>=0)!=(dc>=0):
                t=dp/(dp-dc)
                out.append((prev[0]+t*(cur[0]-prev[0]),prev[1]+t*(cur[1]-prev[1])))
            if dc>=0:out.append(cur)
            prev,dp=cur,dc
    return out

def check(data:dict)->dict:
    req(data.get('format')=='erdos634-saturation-macro-v1','Wrong format')
    u,v,m=data['u'],data['v'],data['m']
    req(all(type(x) is int for x in (u,v,m)) and 0<u<v and gcd(u,v)==1 and m>=1,'Invalid parameters')
    a,b,c=u*v,v*v-u*u,v*v;Q,P=b+c,b+2*c
    family=data['family'];req(family in ('W','beta'),'Invalid family')
    D=4*v*v-u*u;req(data['metric_D']==D and data['tile_sides']==[a,b,c],'Wrong tile or metric')
    count=(Q if family=='W' else P)*m*m
    req(data['tile_count']==count,'Wrong requested tile count')
    target=ccw([decode(x) for x in data['target']]);req(len(target)==3,'Nontriangle target')
    sides=(v**3,u*Q,v*b) if family=='W' else (v**3,v**3,u*P)
    req(sorted(norm(sub(target[i],target[(i+1)%3]),D) for i in range(3))==sorted((m*x)**2 for x in sides),'Wrong target sides')
    one_area=F(u*b,2);tile_sq=sorted([a*a,b*b,c*c]);polygons=[];total=0
    for block in data['blocks']:
        raw=[decode(x) for x in block['vertices']];poly=ccw(raw)
        req(all(det(poly[i],poly[(i+1)%len(poly)],poly[(i+2)%len(poly)])>0 for i in range(len(poly))),'Nonconvex macroregion')
        req(all(det(target[i],target[(i+1)%3],p)>=0 for i in range(3) for p in poly),'Macroregion outside target')
        if block['type']=='triangle_grid':
            n=block['n'];req(type(n) is int and n>0 and len(poly)==3,'Invalid triangular grid')
            req(sorted(norm(sub(raw[i],raw[(i+1)%3]),D)/n**2 for i in range(3))==tile_sq,'Noncongruent triangular cells')
            number=n*n
        elif block['type']=='parallelogram_grid':
            r,s=block['rows'],block['columns'];req(type(r) is int and type(s) is int and r>0 and s>0 and len(poly)==4,'Invalid parallelogram grid')
            req(add(raw[0],raw[2])==add(raw[1],raw[3]),'Not a parallelogram')
            e=tuple(z/r for z in sub(raw[1],raw[0]));f=tuple(z/s for z in sub(raw[3],raw[0]))
            req(block['diagonal'] in ('sum','difference'),'Bad diagonal')
            g=add(e,f) if block['diagonal']=='sum' else sub(e,f)
            req(sorted(norm(z,D) for z in (e,f,g))==tile_sq,'Noncongruent parallelogram cells')
            number=2*r*s
        else:raise ValueError('Unrecognized grid type')
        req(area(poly)==number*one_area,'Wrong macroregion area/count')
        total+=number;polygons.append(poly)
    checked=0
    for p,q in combinations(polygons,2):
        intersection=clip(p,q)
        req(not intersection or area(intersection)==0,'Positive-area macroregion overlap')
        checked+=1
    req(total==count,'Wrong total count')
    req(sum(area(p) for p in polygons)==area(target)==count*one_area,'Coverage failure')
    return dict(status='PASS',tile_count=count,macroregions=len(polygons),macro_pairs=checked,
                expanded_individual_tiles=False,
                scope='Complete compressed-grid dissection; not an enumeration of every individual tile')
