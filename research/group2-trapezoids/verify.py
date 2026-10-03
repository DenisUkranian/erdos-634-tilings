#!/usr/bin/env python3
"""Independently check a generated macrocertificate and its subdivision recipes.

The construction generator is not imported. Optional unit expansion uses
the certificate recipes and then checks all unit triangle intersections.
"""

import argparse
import itertools
import json
from fractions import Fraction as F
from math import gcd
from pathlib import Path

from exact_geometry import (add,area2,ccw,contains,convex,cross,decode,
                            intersection_area2,norm,scale,sub,triangle_grid)


def require(condition,message):
    if not condition:
        raise ValueError(message)


def point(raw):
    return F(raw[0]),F(raw[1])


def equal_vertices(p,q):
    return set(p)==set(q) and len(p)==len(q)


def check_triangle(poly,n,tile):
    require(len(poly)==3 and isinstance(n,int) and n>0,"Invalid triangle scale")
    lengths=sorted(norm(sub(q,p)) for p,q in zip(poly,poly[1:]+poly[:1]))
    require(lengths==sorted((n*s)**2 for s in tile),"Incorrect triangular block")


def check_block(block,tile,expand=False):
    a,b,c=tile
    poly=decode(block["polygon"])
    require(convex(poly),"Block must be a strictly convex counterclockwise polygon")
    out=[]
    if block["type"]=="triangle":
        n=block["scale"]
        check_triangle(poly,n,tile)
        count=n*n
        if expand:
            out=triangle_grid(poly,n)
    elif block["type"]=="grid_minus_corner":
        origin=point(block["origin"]);u=point(block["u"]);v=point(block["v"])
        columns,rows,k=block["columns"],block["rows"],block["corner_scale"]
        require(all(isinstance(n,int) for n in [columns,rows,k]),"Noninteger grid sizes")
        require(0<k==rows<=columns,"Unsupported clipped-grid shape")
        require(norm(u)==b*b and norm(v)==c*c and norm(sub(u,v))==a*a,
                "Grid cell is not two original tiles")
        expected=[add(origin,scale(k,u)),add(origin,scale(columns,u)),
                  add(origin,add(scale(columns,u),scale(rows,v))),add(origin,scale(rows,v))]
        require(equal_vertices(poly,expected),"Clipped-grid boundary mismatch")
        count=2*columns*rows-k*k
        if expand:
            for i in range(columns):
                for j in range(rows):
                    w=add(origin,add(scale(i,u),scale(j,v)))
                    if i+j>=k:
                        out.append(ccw([w,add(w,u),add(w,v)]))
                    if i+j>=k-1:
                        out.append(ccw([add(w,u),add(add(w,u),v),add(w,v)]))
    elif block["type"]=="short_grid":
        origin=point(block["origin"]);u=point(block["unit_u"]);v=point(block["unit_v"])
        x,y=block["width_coefficients"];h=block["height_lcm_multiple"]
        require(all(isinstance(n,int) for n in [x,y,h]) and min(x,y)>=0 and h>0,
                "Invalid short-grid strip counts")
        width=x*a+y*b;height=h*a*b
        require(width>0 and norm(u)==norm(v)==1,"Invalid short-grid basis")
        require(norm(add(scale(a,u),scale(b,v)))==c*c,
                "Short-grid cell is not two original tiles")
        expected=[origin,add(origin,scale(width,u)),
                  add(origin,add(scale(width,u),scale(height,v))),add(origin,scale(height,v))]
        require(equal_vertices(poly,expected),"Short-grid boundary mismatch")
        count=2*h*width
        if expand:
            offset=0
            for strip_width,cell_height in [(a,b)]*x+[(b,a)]*y:
                for row in range(height//cell_height):
                    w=add(origin,add(scale(offset,u),scale(row*cell_height,v)))
                    U,V=scale(strip_width,u),scale(cell_height,v)
                    wU,wV,wUV=add(w,U),add(w,V),add(add(w,U),V)
                    out.extend([ccw([w,wU,wUV]),ccw([w,wUV,wV])])
                offset+=strip_width
    else:
        raise ValueError("Unknown block type")
    require(count==block["count"],"Block count mismatch")
    require(area2(poly)==count*a*b,"Block area/count mismatch")
    if expand:
        require(len(out)==count,"Expansion count mismatch")
    return poly,count,out


def check_target(rec,tile,target):
    data=rec["target_data"]
    if rec["kind"]=="trapezoid":
        x,L=data["short_base"],data["leg"]
        require(x>0 and L>0 and len(target)==4,"Invalid ideal trapezoid")
        lengths=[norm(sub(target[(i+1)%4],target[i])) for i in range(4)]
        for i in range(4):
            order=lengths[i:]+lengths[:i]
            if order==[(x+L)**2,L*L,x*x,L*L]:
                p=[target[(i+j)%4] for j in range(4)]
                require(cross(sub(p[1],p[0]),sub(p[3],p[2]))==0,"Bases are not parallel")
                require(area2(target)==L*(2*x+L),"Incorrect ideal-trapezoid area")
                return
        raise ValueError("Wrong ideal-trapezoid side order")
    require(rec["kind"]=="corner","Unknown target kind")
    outer,removed=decode(data["outer"]),decode(data["removed"])
    require(convex(outer) and convex(removed),"Invalid outer/removed triangle")
    check_triangle(outer,data["outer_scale"],tile)
    check_triangle(removed,data["removed_scale"],tile)
    require(all(contains(outer,p) for p in target+removed),"Corner target leaves outer triangle")
    require(intersection_area2(target,removed)==0,"Target overlaps removed triangle")
    require(area2(target)+area2(removed)==area2(outer),"Corner partition area mismatch")
    shared=set(outer)&set(removed)
    require(len(shared)==1,"Expected one shared corner")
    apex=next(iter(shared))
    ratios=[]
    for p in outer:
        if p==apex:
            continue
        v=sub(p,apex)
        candidates=[q for q in removed if q!=apex and cross(v,sub(q,apex))==0]
        require(len(candidates)==1,"Removed corner is not on both outer sides")
        axis=0 if v[0] else 1
        ratio=(candidates[0][axis]-apex[axis])/v[axis]
        require(0<ratio<1,"Invalid corner truncation")
        ratios.append(ratio)
    require(ratios[0]!=ratios[1],"Corner must be reflected, not homothetic")


def verify(rec,expand=False):
    require(rec["format"]=="group2-shave-v1","Unknown certificate format")
    tile=rec["tile"];a,b,c=tile
    require(all(isinstance(s,int) and s>0 for s in tile),"Invalid integer tile")
    require(c*c==a*a+a*b+b*b and gcd(a,gcd(b,c))==1,"Not a primitive120-degree tile")
    target=decode(rec["target"])
    require(convex(target),"Target must be convex and counterclockwise")
    check_target(rec,tile,target)
    polys=[];tiles=[];count=0
    for block in rec["blocks"]:
        poly,n,unit=check_block(block,tile,expand)
        require(all(contains(target,p) for p in poly),"Block leaves target")
        polys.append(poly);count+=n;tiles+=unit
    pairs=0
    for p,q in itertools.combinations(polys,2):
        require(intersection_area2(p,q)==0,"Macroregion interiors overlap")
        pairs+=1
    require(count==rec["count"],"Certificate count mismatch")
    require(sum(area2(p) for p in polys)==area2(target),"Macro coverage area mismatch")
    result={"tile":tile,"kind":rec["kind"],"count":count,
            "macroregions":len(polys),"macro_pairs_checked":pairs,
            "recipes_checked":True,"unit_expansion_checked":expand}
    if expand:
        require(len(tiles)==count,"Wrong expanded count")
        for tri in tiles:
            check_triangle(tri,1,tile)
            require(area2(tri)==a*b,"Unit area mismatch")
            require(all(contains(target,p) for p in tri),"Unit tile leaves target")
        for p,q in itertools.combinations(tiles,2):
            require(intersection_area2(p,q)==0,"Expanded tile interiors overlap")
        require(sum(area2(p) for p in tiles)==area2(target),"Expanded coverage area mismatch")
        result["unit_pairs_checked"]=len(tiles)*(len(tiles)-1)//2
    result["verified"]=True
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("certificate",type=Path);p.add_argument("--expand",action="store_true")
    args=p.parse_args()
    result=verify(json.loads(args.certificate.read_text()),args.expand)
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
