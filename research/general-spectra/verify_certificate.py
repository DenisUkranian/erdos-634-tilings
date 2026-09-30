#!/usr/bin/env python3
"""Independent exact verifier. Does not import the construction program.

Checks the macro partition by rational convex clipping. A triangle block
is subdivided by the ordinary n^2 grid; a strip block is partitioned into
parallelogram cells. Those standard partitions prove coverage/disjointness
inside a block. With --expand, also checks every resulting tile's three
squared lengths and containment, and can export the exact flat coordinates.
This is not a proof-assistant formalization.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path


def need(ok,why):
    if not ok: raise ValueError(why)
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def mul(k,p):return (k*p[0],k*p[1])
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def orient(p,q,r):return cross(sub(q,p),sub(r,p))
def norm(p):return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]
def dot2(u,v):return 2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]+2*u[1]*v[1]
def area2(poly):return sum(cross(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly))
def inside(p,poly):return all(orient(poly[i],poly[(i+1)%len(poly)],p)>=0 for i in range(len(poly)))

def clip(poly,clipper):
    out=list(poly)
    for i,p in enumerate(clipper):
        q=clipper[(i+1)%len(clipper)]
        old=out;out=[]
        if not old:break
        prev=old[-1];pv=orient(p,q,prev)
        for cur in old:
            cv=orient(p,q,cur)
            if (cv>=0)!=(pv>=0):
                t=pv/(pv-cv)
                out.append(add(prev,mul(t,sub(cur,prev))))
            if cv>=0:out.append(cur)
            prev,pv=cur,cv
    return out

def points(values):
    need(isinstance(values,list),'vertices must be a list')
    return [tuple(F(v) for v in p) for p in values]

def triangle_grid(poly,n):
    P,Q,R=poly
    U=mul(F(1,n),sub(Q,P));V=mul(F(1,n),sub(R,P))
    for i in range(n):
        for j in range(n-i):
            O=add(P,add(mul(i,U),mul(j,V)))
            A=add(O,U);B=add(O,V)
            yield [O,A,B]
            if i+j<n-1:
                yield [A,add(A,V),B]

def strip_grid(poly,counts,a,b,angle):
    P,Q,R,S=poly
    length=counts[0]*a+counts[1]*b
    U=mul(F(1,length),sub(Q,P));V=mul(F(1,a*b),sub(S,P))
    pos=0
    for width,amount,height in [(a,counts[0],b),(b,counts[1],a)]:
        for _ in range(amount):
            for j in range((a*b)//height):
                O=add(P,add(mul(pos,U),mul(j*height,V)))
                A=add(O,mul(width,U));B=add(O,mul(height,V));C=add(A,mul(height,V))
                if angle==120:
                    yield [O,A,B];yield [A,C,B]
                else:
                    yield [O,A,C];yield [O,C,B]
            pos+=width
    need(pos==length,'strip coverage mismatch')

def verify(data,expand=False,expanded_path=None):
    start=time.monotonic()
    need(data['format']=='ERDOS634_HIERARCHICAL_TRIANGLE_PARTITION_V1','wrong format')
    a,b,c=data['tile'];angle=data['angle_opposite_c'];S=data['target_side']
    need(all(type(x) is int and x>0 for x in [a,b,c,S]),'bad integer data')
    need(a>b>1 and gcd(a,b)==1 and angle in [60,120],'bad primitive tile')
    need(c*c==a*a+b*b+(1 if angle==120 else -1)*a*b,'bad tile norm')
    target=points(data['target_vertices'])
    need(target==[(F(0),F(0)),(F(S),F(0)),(F(0),F(S))],'unexpected target')
    total=0;polygons=[];counts=[]
    for index,reg in enumerate(data['regions']):
        poly=points(reg['vertices'])
        need(len(poly) in [3,4] and all(len(p)==2 for p in poly),'invalid polygon')
        need(all(orient(poly[i-1],poly[i],poly[(i+1)%len(poly)])>0 for i in range(len(poly))),
             f'nonconvex or degenerate polygon {index}')
        need(all(inside(p,target) for p in poly),'macroregion outside target')
        if reg['kind']=='similar_triangle':
            n=reg['scale'];need(type(n) is int and n>0 and len(poly)==3,'bad scale')
            lengths=sorted(norm(sub(poly[i],poly[(i+1)%3])) for i in range(3))
            need(lengths==sorted([F(n*n*a*a),F(n*n*b*b),F(n*n*c*c)]),'noncongruent triangle block')
            cnt=n*n
        elif reg['kind']=='strip_parallelogram':
            need(len(poly)==4,'strip must have four vertices')
            ca,cb=reg['counts']
            need(all(type(x) is int and x>=0 for x in [ca,cb]),'invalid strip counts')
            R=ca*a+cb*b;need(R>0,'empty strip')
            U=sub(poly[1],poly[0]);V=sub(poly[3],poly[0])
            need(add(poly[0],poly[2])==add(poly[1],poly[3]),'not a parallelogram')
            need(norm(U)==R*R and norm(V)==(a*b)**2,'wrong strip lengths')
            need(dot2(U,V)==-R*a*b,'wrong strip angle')
            cnt=2*R
        else:raise ValueError('unknown region kind')
        need(area2(poly)==cnt*a*b,'block area/count mismatch')
        polygons.append(poly);counts.append(cnt);total+=cnt
    pairs=0
    for i,j in combinations(range(len(polygons)),2):
        intersection=clip(polygons[i],polygons[j]);pairs+=1
        need(len(intersection)<3 or area2(intersection)==0,f'positive-area overlap {i},{j}')
    need(sum(map(area2,polygons))==area2(target),'uncovered target area')
    need(total==data['expected_tile_count']==S*S//(a*b) and S*S%(a*b)==0,'wrong tile count')
    result=dict(result='ACCEPT_EXACT_HIERARCHICAL_CONSTRUCTION',tile=[a,b,c],
                angle_opposite_c=angle,target_side=S,tile_count=total,
                macroregions=len(polygons),macro_pairs_checked=pairs,
                positive_area_macro_overlaps=0,
                exact_arithmetic=True,
                internal_partition_basis='Standard n^2 triangle subdivision and rectangular strip-cell partition.',
                external_peer_review=False,full_Erdos634_solved=False)
    if expand:
        expected=sorted([a*a,b*b,c*c]);seen=0;digest=hashlib.sha256()
        stream=gzip.open(expanded_path,'wt',encoding='utf-8') if expanded_path else None
        try:
            for reg,poly,cnt in zip(data['regions'],polygons,counts):
                it=triangle_grid(poly,reg['scale']) if reg['kind']=='similar_triangle' else strip_grid(poly,reg['counts'],a,b,angle)
                local=0
                for tri in it:
                    need(sorted(norm(sub(tri[i],tri[(i+1)%3])) for i in range(3))==expected,'expanded tile not congruent')
                    need(area2(tri)==a*b,'expanded tile area')
                    need(all(inside(p,target) and inside(p,poly) for p in tri),'expanded tile outside block/target')
                    text=json.dumps([[str(x),str(y)] for x,y in tri],separators=(',',':'))+'\n'
                    digest.update(text.encode('utf-8'))
                    if stream:stream.write(text)
                    local+=1;seen+=1
                need(local==cnt,'expanded block count mismatch')
        finally:
            if stream:stream.close()
        need(seen==total,'expanded total mismatch')
        result.update(expanded_tiles_checked=seen,expanded_coordinate_sha256=digest.hexdigest(),
                      expanded_pairwise_overlap_test='Not run at O(N^2); disjointness follows from the checked macro partition and the explicit standard subdivisions.')
    result['seconds']=round(time.monotonic()-start,6)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--expand',action='store_true')
    ap.add_argument('--expanded-path',type=Path)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    data=json.loads(args.certificate.read_text())
    result=verify(data,args.expand,args.expanded_path)
    result['certificate_sha256']=hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    text=json.dumps(result,indent=2)+'\n'
    if args.report:args.report.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
