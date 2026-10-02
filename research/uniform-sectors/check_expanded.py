#!/usr/bin/env python3
"""Expand a small grid certificate and independently check every tile and pair.

Separating-axis checks below do not use the macro checker's clipping routine.
Refuses oversized expansions instead of treating a timeout as verification.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from math import lcm


def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def det(a,b,c):return cross(sub(b,a),sub(c,a))
def scaled_add(o,d,e,i,j):return (o[0]+i*d[0]+j*e[0],o[1]+i*d[1]+j*e[1])
def require(x,msg):
    if not x:raise ValueError(msg)


def expand_and_check(data,max_tiles=5000):
    n=data['tile_count']
    require(isinstance(n,int) and 0<n<=max_tiles,'Expansion exceeds the explicit size limit')
    pts={k:tuple(F(*z) for z in p) for k,p in data['points'].items()}
    triangles=[]
    for block in data['blocks']:
        v=[pts[k] for k in block['vertices']]
        if block['type']=='triangle_grid':
            k=block['subdivision'];o=v[0]
            d=tuple(x/k for x in sub(v[1],o));e=tuple(x/k for x in sub(v[2],o))
            for i in range(k):
                for j in range(k-i):
                    z=scaled_add(o,d,e,i,j);x=scaled_add(o,d,e,i+1,j);y=scaled_add(o,d,e,i,j+1)
                    triangles.append((z,x,y))
                    if i+j<=k-2:
                        w=scaled_add(o,d,e,i+1,j+1)
                        triangles.append((x,w,y))
        elif block['type']=='parallelogram_grid':
            r,s=block['rows'],block['columns'];o=v[0]
            d=tuple(x/r for x in sub(v[1],o));e=tuple(x/s for x in sub(v[3],o))
            for i in range(r):
                for j in range(s):
                    z=scaled_add(o,d,e,i,j);x=scaled_add(o,d,e,i+1,j);y=scaled_add(o,d,e,i,j+1)
                    w=scaled_add(o,d,e,i+1,j+1)
                    triangles.extend(((z,x,y),(x,w,y)))
        else:raise ValueError('Unknown block')
    require(len(triangles)==n,'Expanded count mismatch')
    den=lcm(*(z.denominator for tr in triangles for p in tr for z in p),
            *(z.denominator for k in data['target'] for z in pts[k]))
    convert=lambda p:(int(p[0]*den),int(p[1]*den))
    target=tuple(convert(pts[k]) for k in data['target'])
    if det(*target)<0:target=tuple(reversed(target))
    raw=[tuple(convert(p) for p in tr) for tr in triangles]
    tris=[tr if det(*tr)>0 else tuple(reversed(tr)) for tr in raw]
    D=data['metric_D'];sq=sorted(x*x*den*den for x in data['tile_sides'])
    total=0;boxes=[]
    for tr in tris:
        ds=[sub(tr[(i+1)%3],tr[i]) for i in range(3)]
        require(sorted(dx*dx+D*dy*dy for dx,dy in ds)==sq,'Noncongruent individual tile')
        ar=det(*tr);require(ar>0,'Degenerate individual tile');total+=ar
        require(all(det(target[i],target[(i+1)%3],p)>=0 for i in range(3) for p in tr),'Tile outside target')
        boxes.append((min(p[0] for p in tr),max(p[0] for p in tr),min(p[1] for p in tr),max(p[1] for p in tr)))
    require(total==det(*target),'Expanded area does not cover target')
    aabb=sat=0
    for i,A in enumerate(tris):
        ax0,ax1,ay0,ay1=boxes[i]
        for j in range(i):
            bx0,bx1,by0,by1=boxes[j]
            if ax1<=bx0 or bx1<=ax0 or ay1<=by0 or by1<=ay0:
                aabb+=1;continue
            B=tris[j];sat+=1;separated=False
            for first,other in ((A,B),(B,A)):
                for k in range(3):
                    if all(det(first[k],first[(k+1)%3],p)<=0 for p in other):
                        separated=True;break
                if separated:break
            require(separated,f'Individual overlap at tiles {j},{i}')
    require(aabb+sat==n*(n-1)//2,'Pair accounting mismatch')
    return {'status':'PASS','individual_tiles_checked':n,'pairs_checked':aabb+sat,
            'aabb_separated_pairs':aabb,'exact_sat_pairs':sat,'integer_coordinate_scale':den,
            'all_tile_congruences':True,'all_tiles_contained':True,'exact_area_coverage':True,
            'positive_area_overlaps':0}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('certificate');p.add_argument('--max-tiles',type=int,default=5000);p.add_argument('--output')
    args=p.parse_args()
    try:
        with open(args.certificate,encoding='utf-8') as h:data=json.load(h)
        report=expand_and_check(data,args.max_tiles)
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:p.exit(1,'FAIL: '+str(exc)+'\n')
    text=json.dumps(report,indent=2)+'\n'
    if args.output:
        with open(args.output,'w',encoding='utf-8') as h:h.write(text)
    print(text,end='')
if __name__=='__main__':main()
