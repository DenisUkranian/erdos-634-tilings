#!/usr/bin/env python3
"""Generate positive universal-shaving certificates; no search is performed."""

import argparse
import json
from fractions import Fraction as F
from math import gcd
from pathlib import Path

from exact_geometry import add,ccw,encode,scale


def semigroup(n,a,b):
    x=(n*pow(a,-1,b))%b
    y=(n-a*x)//b
    if n<0 or y<0:
        raise ValueError(f"{n} is not a nonnegative combination of {a},{b}")
    return x,y


def certificate(a,b,c,t=None,m=1,kind="trapezoid"):
    if min(a,b,c,m)<=0 or gcd(a,gcd(b,c))!=1 or c*c!=a*a+a*b+b*b:
        raise ValueError("Require a primitive positive120-degree norm triple and m>0")
    t=a+b-c if t is None else t
    if not 0<t<b:
        raise ValueError("Require0<t<b")
    r=b*(c-b)-c*t
    x,y=semigroup(m*r,a,b)
    z=(F(b,c),F(a,c))
    F0=(F(0),F(0)); A=(F(c*c),F(0)); B=(F(b*b),F(a*b))
    C=(F(b*t),F(a*t)); E=(F(b*c),F(0)); D=(F(b*(c+t)),F(a*t))
    Q=add(C,scale(b*b,z)); R=add(E,scale(b*(c-b),z))
    O=(F(b*t),F(0)); H=(F(b*t),F(a*b)); J=(F(a*a+b*b),F(a*b))
    blocks=[]

    def poly(points):
        return encode(ccw([scale(m,p) for p in points]))

    def tri(points,n):
        blocks.append({"type":"triangle","polygon":poly(points),"scale":m*n,
                       "count":m*m*n*n})

    blocks.append({"type":"grid_minus_corner","polygon":poly([O,E,D,C]),
                   "origin":encode([F0])[0],"u":encode([(F(b),F(0))])[0],
                   "v":encode([(F(b),F(a))])[0],"columns":m*c,"rows":m*t,
                   "corner_scale":m*t,"count":m*m*(2*c*t-t*t)})
    tri([C,D,Q],b)
    tri([E,A,R],c-b)
    blocks.append({"type":"short_grid","polygon":poly([Q,B,R,D]),
                   "origin":encode([scale(m,Q)])[0],"unit_u":encode([z])[0],
                   "unit_v":encode([(z[0]+z[1],-z[0])])[0],
                   "width_coefficients":[x,y],"height_lcm_multiple":m,
                   "count":2*m*m*r})
    if kind=="trapezoid":
        tri([C,B,H],b-t)
        tri([B,A,J],a)
        target=poly([O,A,J,H])
        target_data={"short_base":m*(a*a+b*b-b*t),"leg":m*a*b}
    elif kind=="corner":
        target=poly([O,A,B,C])
        target_data={"outer":poly([F0,A,B]),"removed":poly([F0,O,C]),
                     "outer_scale":m*c,"removed_scale":m*t}
    else:
        raise ValueError("Unknown target kind")
    return {"format":"group2-shave-v1","coordinate_convention":
            "(u,v) -> (u+v/2,sqrt(3)*v/2)","tile":[a,b,c],"shave":t,
            "multiplier":m,"remainder":r,"kind":kind,"target":target,
            "target_data":target_data,"count":sum(p["count"] for p in blocks),
            "blocks":blocks}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("a",type=int);p.add_argument("b",type=int);p.add_argument("c",type=int)
    p.add_argument("output",type=Path);p.add_argument("--shave",type=int)
    p.add_argument("--multiplier",type=int,default=1)
    p.add_argument("--kind",choices=["trapezoid","corner"],default="trapezoid")
    args=p.parse_args()
    cert=certificate(args.a,args.b,args.c,args.shave,args.multiplier,args.kind)
    args.output.write_text(json.dumps(cert,indent=2)+"\n")
    print(json.dumps({"output":str(args.output),"count":cert["count"]}))


if __name__=="__main__":
    main()
