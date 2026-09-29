#!/usr/bin/env python3
"""Check explicit theta seeds with exact rational macro geometry.

Standard library only. Prints deterministic JSON; never writes files.
The negative-Delta cases check geometry, while positive-Delta cases
check the integer interval used by the linked earlier construction.
"""
if not __debug__:
    raise SystemExit("Refusing optimized Python: these exact checks require assertions.")
from fractions import Fraction as F
from math import gcd
import json
import argparse

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(s,p): return (s*p[0],s*p[1])
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def area2(p): return abs(sum(cross(p[i],p[(i+1)%len(p)]) for i in range(len(p))))
def norm2(p,D): return p[0]**2+D*p[1]**2
def sides2(p,D): return sorted(norm2(sub(p[i],p[(i+1)%3]),D) for i in range(3))
def inside(p,poly):
    signed=sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
    sign=1 if signed>0 else -1
    return all(sign*cross(sub(poly[(i+1)%len(poly)],poly[i]),sub(p,poly[i]))>=0
               for i in range(len(poly)))

def ccw(poly):
    signed=sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))
    return list(poly) if signed>0 else list(reversed(poly))

def intersection(poly,clip):
    out=ccw(poly)
    clip=ccw(clip)
    for i in range(len(clip)):
        A,B=clip[i],clip[(i+1)%len(clip)]
        old=out; out=[]
        if not old: break
        for j in range(len(old)):
            P,Q=old[j-1],old[j]
            fP=cross(sub(B,A),sub(P,A)); fQ=cross(sub(B,A),sub(Q,A))
            if (fP>=0)!=(fQ>=0): out.append(add(P,mul(fP/(fP-fQ),sub(Q,P))))
            if fQ>=0: out.append(Q)
    return out

def seed(u,v):
    a,b,c=u*v,v*v-u*u,v*v
    delta=b*(a*a+b*b)-a*a*c
    assert delta<0
    disc=4*v*v-u*u
    frob=(b-1)*(c-1)
    n=(frob-a*a*delta+b**3*c*c-1)//(b**3*c*c)
    rho=a*b*b*c*n
    T=u*c*n*(a*a+b*b)
    mu=F(b*T,v)
    A=(F(0),F(0)); C=(mu*a,F(0)); B=(mu*a/2,mu*v/2)
    downleft=(F(-u,2*v),F(-1,2*v))
    downright=(F(u,2*v),F(-1,2*v))
    alpha=(F(2*c-u*u,2*c),F(u,2*c))
    K=add(B,mul(b*rho,downleft))
    L=add(B,mul(c*rho,downright))
    H=mul(F(a**3*rho,b*c),alpha)
    I=mul(F(-rho*delta,a*b),alpha)
    J=add(C,mul(F(-rho*delta,b*c),(F(-u,2*v),F(1,2*v))))
    macro=[((B,K,L),rho),((K,H,L),a*rho//c),((A,K,H),a*a*rho//(b*c)),
           ((H,L,J),b*rho//c),((H,I,J),b*rho//a)]
    target=(A,C,B)
    for tri,k in macro:
        assert sides2(tri,disc)==sorted([a*a*k*k,b*b*k*k,c*c*k*k])
        assert all(inside(p,target) for p in tri)
    red=(A,C,J,I)
    assert I[1]==J[1] and J[0]>I[0]
    assert J[0]-I[0]==F(rho*b*c,a)
    assert area2(target)==sum(area2(tri) for tri,k in macro)+area2(red)
    regions=[tri for tri,k in macro]+[red]
    for i,P in enumerate(regions):
        for Q in regions[:i]:
            clipped=intersection(P,Q)
            assert not clipped or area2(clipped)==0
    added_count=sum(k*k for tri,k in macro)
    regions_area=F(0)
    min_width=b**3*c*c*n+a*a*delta
    assert min_width>=frob
    for j in range(n):
        lowleft=mul(F(j,n),I)
        lowright=add(C,mul(F(j,n),sub(J,C)))
        upleft=mul(F(j+1,n),I)
        upright=add(C,mul(F(j+1,n),sub(J,C)))
        strip=(lowleft,lowright,upright,upleft)
        r1=-a*delta; r2=-c*delta
        E=sub(upright,(F(a*r1),F(0)))
        G=sub(E,sub(upleft,lowleft))
        tri1=(lowright,upright,E); tri2=(lowright,E,G)
        para=(lowleft,upleft,E,G)
        assert sides2(tri1,disc)==sorted([a*a*r1*r1,b*b*r1*r1,c*c*r1*r1])
        assert sides2(tri2,disc)==sorted([a*a*r2*r2,b*b*r2*r2,c*c*r2*r2])
        width=E[0]-upleft[0]
        slant=b*c*(-delta)
        assert width==min_width+(n-j-1)*slant
        assert width.denominator==1 and width>=frob
        assert norm2(sub(upleft,lowleft),disc)==slant*slant
        assert all(inside(p,strip) for p in (E,G))
        assert area2(strip)==area2(tri1)+area2(tri2)+area2(para)
        regions_area+=area2(strip)
        added_count+=r1*r1+r2*r2+2*(-delta)*width
    assert regions_area==area2(red)
    assert added_count==b*T*T
    return {"u":u,"v":v,"a":a,"b":b,"c":c,"delta":delta,"strips":n,
            "seed_T":T,"tile_count":b*T*T,"red_min_width":min_width,
            "red_triangle_scales":[-a*delta,-c*delta],
            "five_scales":[k for tri,k in macro]}

def ceildiv(n,d):
    return (n+d-1)//d


def positive_seed(u,v):
    a,b,c=u*v,v*v-u*u,v*v
    delta=b*(a*a+b*b)-a*a*c
    assert delta>0
    frob_ab=(a-1)*(b-1)
    T=ceildiv((a*a*c+frob_ab)*(a*a+b*b),u*delta)
    J=ceildiv(u*T,a*a+b*b)
    width=u*b*T-a*a*c*J
    assert width>=frob_ab
    assert (a*a+b*b)*J>=u*T
    assert v*T-a*c*J>0
    assert u*T-a*a*J>0
    return {"u":u,"v":v,"seed_T":T,"interval_J":J,
            "mixed_width":width,"delta":delta}


def effective_bounds(u,v):
    a,b,c=u*v,v*v-u*u,v*v
    delta=b*(a*a+b*b)-a*a*c
    assert delta==b**3-c*u**4
    assert gcd(b,c)==1 and delta!=0
    frob_bc=(b-1)*(c-1)
    Hu=ceildiv(a*a+b*b+frob_bc,u*b)
    Hv=ceildiv(a*a+frob_bc,b*v)
    assert Hu>=Hv
    Cwb=v*ceildiv(Hu,v)+(u-1)*(v-1)
    if delta>0:
        s=positive_seed(u,v)["seed_T"]
        Ctheta=s
    else:
        n=ceildiv(frob_bc-a*a*delta,b**3*c*c)
        s=u*c*n*(a*a+b*b)
        Ctheta=s*ceildiv(Hu,s)+(u-1)*(v-1)
    return {"u":u,"v":v,"delta":delta,"theta_seed":s,
            "H_u":Hu,"H_v":Hv,"W_beta_threshold":Cwb,
            "theta_threshold":Ctheta,"alpha_threshold":ceildiv(Ctheta,v),
            "other_scalene_threshold":1}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-v",type=int,default=25,
                        help="check all coprime 0<u<v up to this v (default: 25)")
    args=parser.parse_args()
    if args.max_v<2:
        parser.error("--max-v must be at least 2")
    neg=[]; pos=[]; bounds=[]
    for v in range(2,args.max_v+1):
        for u in range(1,v):
            if gcd(u,v)!=1:
                continue
            a,b,c=u*v,v*v-u*u,v*v
            delta=b*(a*a+b*b)-a*a*c
            assert delta!=0
            if delta<0:
                neg.append(seed(u,v))
            else:
                pos.append(positive_seed(u,v))
            bounds.append(effective_bounds(u,v))
    named={(1,2),(1,3),(2,3),(3,4),(9,10),(24,25)}
    result={"status":"PASS","max_v":args.max_v,"arithmetic":"Fraction exact",
        "negative_delta_cases":len(neg),"positive_delta_cases":len(pos),
        "total_parameter_pairs":len(bounds),
        "scope":{
            "negative_delta":"Five triangle side lengths, containment, all main-region pairwise intersections, red-strip partitions, grid dimensions and total tile count.",
            "positive_delta":"Explicit seed bound and its integer interval; geometry is checked separately by check_eventual_families.py.",
            "bounds":"Both annulus thresholds and explicit sufficient bounds for all five target families.",
            "not_checked":"Individual tiles inside the quadratic and parallelogram macroblocks are not expanded."},
        "max_red_strips":max((p["strips"] for p in neg),default=0),
        "negative_delta_examples":[p for p in neg if (p["u"],p["v"]) in named],
        "effective_bound_examples":[p for p in bounds if (p["u"],p["v"]) in named]}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
