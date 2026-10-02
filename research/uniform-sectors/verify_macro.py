#!/usr/bin/env python3
"""Independent exact checker for compressed triangle/parallelogram grids.

This module does not import the generator or the arithmetic sector solver.
Its positive result certifies a finite formula for a complete dissection:
macro containment, all pairwise macro intersections, exact area, congruence of
unit cells, and positive integer subdivisions. It does not enumerate huge grids.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from itertools import combinations
from math import gcd


def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def det(a,b,c): return cross(sub(b,a),sub(c,a))
def area2(poly):
    return sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
def ccw(poly):
    z=area2(poly)
    if not z: raise ValueError("Degenerate polygon")
    return poly if z>0 else list(reversed(poly))
def length2(p,D): return p[0]*p[0]+D*p[1]*p[1]

def clip(poly, cutter):
    """Exact Sutherland-Hodgman intersection of convex CCW polygons."""
    out=poly[:]
    for i,a in enumerate(cutter):
        b=cutter[(i+1)%len(cutter)]
        old=out;out=[]
        if not old: break
        prev=old[-1];dp=det(a,b,prev)
        for cur in old:
            dc=det(a,b,cur)
            if (dp>=0)!=(dc>=0):
                lam=dp/(dp-dc)
                out.append((prev[0]+lam*(cur[0]-prev[0]),prev[1]+lam*(cur[1]-prev[1])))
            if dc>=0: out.append(cur)
            prev,dp=cur,dc
    return out


def require(x,msg):
    if not x: raise ValueError(msg)


def verify(data: dict) -> dict:
    require(data.get("format")=="erdos634-QP-macro-v1","Wrong format")
    u,v,t = (data[x] for x in ("u","v","scale"))
    require(all(isinstance(x,int) and not isinstance(x,bool) for x in (u,v,t)),"Integer parameters required")
    require(0<u<v and gcd(u,v)==1 and t>=1,"Invalid primitive parameters")
    a,b,c=u*v,v*v-u*u,v*v
    Q,P=b+c,b+2*c
    D=data["metric_D"]
    require(D==4*v*v-u*u and D>0,"Incorrect metric")
    require(data["tile_sides"]==[a,b,c],"Incorrect tile")
    require(data["tile_count"]==Q*P*t*t,"Incorrect count")
    pts={name:tuple(F(z[0],z[1]) for z in p) for name,p in data["points"].items()}
    require(all(len(p)==2 for p in pts.values()),"Malformed points")
    target=ccw([pts[n] for n in data["target"]])
    require(len(target)==3,"Target not triangular")
    target_sq=sorted(length2(sub(target[(i+1)%3],target[i]),D) for i in range(3))
    require(target_sq==sorted((t*x)**2 for x in (c*c,c*Q,b*P)),"Wrong target side lengths")
    tile_sq=sorted(x*x for x in (a,b,c))
    # Twice the coordinate area of a reference primitive tile. In metric D,
    # an (a,b,c) tile has coordinate area u*b/4.
    unit_area2=F(u*b,2)
    polygons=[];total_count=0;tri_count=para_count=0
    require(len(data["blocks"])==5,"Expected exactly five construction blocks")
    for block in data["blocks"]:
        raw=[pts[n] for n in block["vertices"]]
        poly=ccw(raw)
        require(all(det(poly[i],poly[(i+1)%len(poly)],poly[(i+2)%len(poly)])>0
                    for i in range(len(poly))),"Block not strictly convex")
        require(all(det(target[i],target[(i+1)%3],q)>=0 for i in range(3) for q in poly),
                "Block outside target")
        if block["type"]=="triangle_grid":
            n=block["subdivision"]
            require(isinstance(n,int) and not isinstance(n,bool) and n>0,"Invalid triangle grid size")
            require(len(raw)==3,"Wrong triangle vertices")
            sides=sorted(length2(sub(raw[(i+1)%3],raw[i]),D)/(n*n) for i in range(3))
            require(sides==tile_sq,"Noncongruent triangle-grid cell")
            cnt=n*n;tri_count+=1
        elif block["type"]=="parallelogram_grid":
            r,s=block["rows"],block["columns"]
            require(all(isinstance(x,int) and not isinstance(x,bool) and x>0 for x in (r,s)),"Invalid parallelogram grid")
            require(len(raw)==4 and add(raw[0],raw[2])==add(raw[1],raw[3]),"Not a parallelogram")
            require(block.get("diagonal")=="difference","Wrong cell diagonal")
            d=tuple(x/r for x in sub(raw[1],raw[0]));e=tuple(x/s for x in sub(raw[3],raw[0]))
            require(sorted((length2(d,D),length2(e,D),length2(sub(d,e),D)))==tile_sq,
                    "Noncongruent parallelogram-grid cell")
            cnt=2*r*s;para_count+=1
        else:
            raise ValueError("Unknown block type")
        require(area2(poly)==cnt*unit_area2,"Block area/count mismatch")
        total_count+=cnt;polygons.append(poly)
    require(tri_count==4 and para_count==1,"Wrong block inventory")
    checked=0
    for first,second in combinations(polygons,2):
        intersection=clip(first,second)
        require(not intersection or area2(intersection)==0,"Positive-area macro overlap")
        checked+=1
    require(total_count==data["tile_count"],"Total cell count mismatch")
    require(sum(area2(p) for p in polygons)==area2(target)==total_count*unit_area2,
            "Target coverage/area mismatch")
    return {"status":"PASS", "tile_count":total_count, "macro_blocks":len(polygons),
            "macro_pairs_checked":checked, "triangle_grids":tri_count,
            "parallelogram_grids":para_count, "expanded_individual_tiles":False,
            "scope":"Complete compressed-grid construction; exact containment, congruence, coverage, and macro disjointness"}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("certificate");p.add_argument("--output")
    x=p.parse_args()
    try:
        with open(x.certificate,encoding="utf-8") as h: data=json.load(h)
        result=verify(data)
    except (ValueError,KeyError,TypeError,ZeroDivisionError) as exc:
        p.exit(1,"FAIL: "+str(exc)+"\n")
    text=json.dumps(result,indent=2)+"\n"
    if x.output:
        with open(x.output,"w",encoding="utf-8") as h:h.write(text)
    print(text,end="")

if __name__=="__main__":main()
