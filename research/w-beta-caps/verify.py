"""Independent exact grid-certificate checker; imports no generator code.

For each convex macroregion this checks its unit tile, dimension and area.
Rational convex clipping verifies that the macroregions partition the target.
For shells the inner triangle is checked as an extra uncovered region.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import gcd
from pathlib import Path


def require(condition,message):
    if not condition: raise ValueError(message)
def plus(p,q): return p[0]+q[0],p[1]+q[1]
def minus(p,q): return p[0]-q[0],p[1]-q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def turn(a,b,c): return cross(minus(b,a),minus(c,a))
def area2(poly):
    return sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
def norm2(p,D): return p[0]*p[0]+D*p[1]*p[1]
def divide(p,n): return p[0]/n,p[1]/n
def decode(p):
    require(type(p) is list and len(p)==2,'Malformed coordinate')
    result=[]
    for pair in p:
        require(type(pair) is list and len(pair)==2 and
                all(type(x) is int for x in pair) and pair[1]>0,'Malformed rational')
        result.append(Fraction(*pair))
    return tuple(result)
def polygon(points):
    require(len(points)>=3 and area2(points)!=0,'Degenerate polygon')
    p=points if area2(points)>0 else list(reversed(points))
    require(all(turn(p[i],p[(i+1)%len(p)],p[(i+2)%len(p)])>0
                for i in range(len(p))),'Nonconvex polygon')
    return p
def intersection(subject,clipper):
    output=list(subject)
    for j,a in enumerate(clipper):
        b=clipper[(j+1)%len(clipper)]
        old=output;output=[]
        if not old: break
        prev=old[-1];dp=turn(a,b,prev)
        for cur in old:
            dc=turn(a,b,cur)
            if (dp>=0)!=(dc>=0):
                t=dp/(dp-dc)
                output.append((prev[0]+t*(cur[0]-prev[0]),
                               prev[1]+t*(cur[1]-prev[1])))
            if dc>=0:output.append(cur)
            prev,dp=cur,dc
    return output
def contained(inner,outer):
    return all(turn(outer[i],outer[(i+1)%len(outer)],p)>=0
               for i in range(len(outer)) for p in inner)
def lengths(poly,D):
    return sorted(norm2(minus(poly[i],poly[(i+1)%len(poly)]),D)
                  for i in range(len(poly)))
def disjoint(p,q):
    cut=intersection(p,q)
    return not cut or area2(cut)==0


def check(data):
    require(data.get('format')=='erdos634-w-beta-caps-v1','Wrong certificate format')
    u,v=data['u'],data['v']
    require(type(u) is int and type(v) is int and 0<u<v and gcd(u,v)==1,
            'Invalid primitive parameters')
    a,b,c=u*v,v*v-u*u,v*v;Q,P=b+c,b+2*c;D=4*v*v-u*u
    require(data['metric_D']==D and data['tile_sides']==[a,b,c],'Wrong tile or metric')
    tile_sq=sorted([a*a,b*b,c*c]);unit_area2=Fraction(u*b,2)
    kind=data['kind'];require(kind in ('cap','shell','tiling'),'Unknown certificate kind')
    raw_target=[decode(p) for p in data['target']];target=polygon(raw_target)
    inners=[]
    if kind=='cap':
        top=u*(v-u)*b;bottom=top+u*u*Q
        require(len(target)==4 and lengths(target,D)==sorted([top*top,bottom*bottom,
                (u*v*b)**2,(u*v*c)**2]),'Wrong cap dimensions')
        require(cross(minus(raw_target[1],raw_target[0]),
                      minus(raw_target[2],raw_target[3]))==0,'Cap bases are not parallel')
        count=u**4+2*u*v*b
    else:
        family=data['family'];require(family in ('W','beta'),'Invalid family')
        base=(v**3,u*Q,v*b) if family=='W' else (v**3,v**3,u*P)
        coefficient=Q if family=='W' else P
        m=data['m'] if kind=='tiling' else data['T']+u
        require(type(m) is int and m>0 and len(target)==3,'Invalid target scale')
        require(lengths(target,D)==sorted((m*x)**2 for x in base),'Wrong target sides')
        count=coefficient*m*m
        if kind=='shell':
            T=data['T'];require(type(T) is int and T>0,'Invalid inner scale')
            inner=polygon([decode(p) for p in data['inner']])
            require(len(inner)==3 and lengths(inner,D)==sorted((T*x)**2 for x in base),
                    'Wrong inner sides')
            require(contained(inner,target),'Inner target is outside outer target')
            require(area2(inner)==coefficient*T*T*unit_area2,'Wrong inner area')
            inners.append(inner);count-=coefficient*T*T
    require(type(data['tile_count']) is int and data['tile_count']==count,'Wrong tile count')
    regions=[];total=0
    for block in data['blocks']:
        raw=[decode(p) for p in block['vertices']];poly=polygon(raw)
        require(contained(poly,target),'Macroregion outside target')
        if block['type']=='triangle_grid':
            n=block['n']
            require(type(n) is int and n>0 and len(raw)==3,'Invalid triangle grid')
            require([s/(n*n) for s in lengths(raw,D)]==tile_sq,'Noncongruent triangle cells')
            number=n*n
        elif block['type']=='parallelogram_grid':
            r,s=block['rows'],block['columns']
            require(type(r) is int and type(s) is int and r>0 and s>0 and len(raw)==4,
                    'Invalid parallelogram grid')
            require(plus(raw[0],raw[2])==plus(raw[1],raw[3]),'Not a parallelogram')
            e=divide(minus(raw[1],raw[0]),r);f=divide(minus(raw[3],raw[0]),s)
            diag=block['diagonal'];require(diag in ('sum','difference'),'Unknown diagonal')
            third=plus(e,f) if diag=='sum' else minus(e,f)
            require(sorted(norm2(p,D) for p in (e,f,third))==tile_sq,
                    'Noncongruent parallelogram cells')
            number=2*r*s
        else: raise ValueError('Unknown grid type')
        require(area2(poly)==number*unit_area2,'Wrong grid area')
        total+=number;regions.append(poly)
    pairs=0
    for p,q in combinations(regions+inners,2):
        require(disjoint(p,q),'Positive-area overlap')
        pairs+=1
    require(total==count,'Incorrect tile total')
    require(sum(area2(p) for p in regions+inners)==area2(target),'Incomplete coverage')
    return dict(status='PASS',kind=kind,tile_count=count,macroregions=len(regions),
                checked_macro_pairs=pairs,
                scope='Exact unit-cell, containment, pairwise-disjointness and area checks')


def expand(data):
    """Independent unit-triangle expansion, for finite small regressions only."""
    triangles=[]
    def scale(t,p):return t*p[0],t*p[1]
    def grid(p,e,f,i,j):return plus(p,plus(scale(i,e),scale(j,f)))
    for block in data['blocks']:
        p=[decode(z) for z in block['vertices']]
        if block['type']=='triangle_grid':
            n=block['n'];e=divide(minus(p[1],p[0]),n);f=divide(minus(p[2],p[0]),n)
            for i in range(n):
                for j in range(n-i):
                    z=grid(p[0],e,f,i,j)
                    triangles.append([z,plus(z,e),plus(z,f)])
                    if i+j<n-1:
                        triangles.append([plus(z,e),plus(z,f),plus(plus(z,e),f)])
        else:
            rows,cols=block['rows'],block['columns']
            e=divide(minus(p[1],p[0]),rows);f=divide(minus(p[3],p[0]),cols)
            for i in range(rows):
                for j in range(cols):
                    z=grid(p[0],e,f,i,j);ze,zf=plus(z,e),plus(z,f);zef=plus(ze,f)
                    triangles.extend([[z,ze,zef],[z,zf,zef]] if block['diagonal']=='sum'
                                     else [[z,ze,zf],[ze,zf,zef]])
    return triangles


def check_expanded(data,pairwise=True):
    macro=check(data);tiles=[polygon(t) for t in expand(data)]
    u,v=data['u'],data['v'];D=4*v*v-u*u
    expected=sorted([(u*v)**2,(v*v-u*u)**2,v**4])
    target=polygon([decode(z) for z in data['target']])
    require(len(tiles)==data['tile_count'],'Expanded tile count mismatch')
    require(all(lengths(t,D)==expected and contained(t,target) for t in tiles),
            'Invalid expanded unit triangle')
    if pairwise:
        require(all(disjoint(p,q) for p,q in combinations(tiles,2)),
                'Expanded unit triangles overlap')
    return dict(status='PASS',unit_triangles=len(tiles),all_pairs=pairwise,
                unit_pairs=len(tiles)*(len(tiles)-1)//2 if pairwise else 0)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--expand',action='store_true')
    args=parser.parse_args();data=json.loads(args.certificate.read_text())
    print(json.dumps(check_expanded(data) if args.expand else check(data),indent=2))
