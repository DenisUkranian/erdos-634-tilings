"""Exact rational checks of the two universal annular macrodissections.

Checks macroregions, integer block scales, and the primitive strip cells.
Does not enumerate or check every pair of individual congruent tiles.
No third-party dependencies; deterministic JSON goes to stdout.
"""
from fractions import Fraction as F
from math import gcd
import json

if not __debug__:
    raise SystemExit("Verification requires assertions: do not use Python -O.")


def add(p, q): return (p[0] + q[0], p[1] + q[1])
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
def mul(p, t): return (p[0] * t, p[1] * t)
def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def area2(p):
    return sum(cross(p[0],p[i],p[i+1]) for i in range(1,len(p)-1))
def ccw(p): return tuple(p) if area2(p)>0 else tuple(reversed(p))
def norm2(p, d): return p[0]*p[0]+d*p[1]*p[1]
def sq(p, q, d): return norm2(sub(p,q),d)
def ceil(q): return -((-q.numerator)//q.denominator)


def separated(p,q):
    return any(all(cross(r[j],r[(j+1)%len(r)],z)<=0 for z in s)
               for r,s in ((p,q),(q,p)) for j in range(len(r)))


def partition(target, inner, outer, regions):
    target,inner,outer=map(ccw,(target,inner,outer))
    regions=[ccw(p) for p in regions]
    assert area2(target)+area2(inner)==area2(outer)
    for p in regions:
        assert area2(p)>0
        assert all(cross(target[i],target[(i+1)%len(target)],z)>=0
                   for z in p for i in range(len(target)))
        assert all(cross(p[i],p[(i+1)%len(p)],z)>=0
                   for z in p for i in range(len(p)))
        assert separated(p,inner)
    assert sum(area2(p) for p in regions)==area2(target)
    pairs=0
    for i,p in enumerate(regions):
        for q in regions[:i]:
            assert separated(p,q)
            pairs+=1
    return pairs


def triangle(p, scale, a,b,c,d):
    assert scale>0 and isinstance(scale,int)
    assert sorted(sq(p[i],p[(i+1)%3],d) for i in range(3)) == \
           sorted((scale*z)**2 for z in (a,b,c))


def strip_grid(long_vector, short_vector, length, a,b,c,d):
    assert length>0 and isinstance(length,int)
    assert norm2(long_vector,d)==length*length
    assert norm2(short_vector,d)==b*b*c*c
    # At the chosen corner the parallelogram angle is alpha.
    x=mul(long_vector,F(b,length))
    y=mul(short_vector,F(1,b))
    assert norm2(x,d)==b*b and norm2(y,d)==c*c
    assert norm2(sub(x,y),d)==a*a
    y_count=(length*pow(c,-1,b))%b
    x_count=(length-y_count*c)//b
    assert x_count>=0 and y_count>=0 and x_count*b+y_count*c==length
    return [x_count,y_count]


def apex_shell(u,v,T):
    a,b,c=u*v,v*v-u*u,v*v; d=4*v*v-u*u
    A=(F(0),F(0)); C=(F(u*b*(T+u)),F(0))
    B=(F(u*u*b,2),F(u*b,2)); E=add(B,(F(u*b*T),F(0)))
    D=add(B,(F(a*a),F(0))); R=(F(c*c),F(0))
    S=sub(E,(F(b*b),F(0)))
    tip=(F(u*b*(T+u),2),F(b*(T+u),2))
    tri=[(A,B,D),(A,D,R),(S,E,C)]
    for p,k in zip(tri,(a,c,b)): triangle(p,k,a,b,c,d)
    width=u*b*T-a*a-b*b
    strips=strip_grid(sub(S,D),sub(R,D),width,a,b,c,d)
    assert width>=(b-1)*(c-1)
    pairs=partition((A,C,E,B),(B,E,tip),(A,C,tip),tri+[(R,D,S,C)])
    count=a*a+c*c+b*b+2*width
    assert count==b*((T+u)**2-T*T)
    return dict(step=u,T=T,triangle_scales=[a,c,b],parallelogram_sides=[width,b*c],
                strip_counts=strips,tile_count=count,macro_pair_checks=pairs)


def base_shell(u,v,T):
    a,b,c=u*v,v*v-u*u,v*v; d=4*v*v-u*u
    O=(F(0),F(0))
    A=(F(u*b*(T+v),2),F(b*(T+v),2)); B=(F(u*b*(T+v)),F(0))
    C=(F(u*b*T),F(0)); D=(F(u*b*T,2),F(b*T,2))
    E=(F(u*b*T)-F(u*u*u*v,2),F(u*u*v,2))
    G=add(E,(F(u*b*v,2),F(b*v,2)))
    tri=[(B,C,E),(B,E,G)]
    for p,k in zip(tri,(a,c)): triangle(p,k,a,b,c,d)
    width=b*v*T-a*a
    strips=strip_grid(sub(G,A),sub(D,A),width,a,b,c,d)
    assert width>=(b-1)*(c-1)
    pairs=partition((A,B,C,D),(O,C,D),(O,B,A),tri+[(A,D,E,G)])
    count=a*a+c*c+2*width
    assert count==b*((T+v)**2-T*T)
    return dict(step=v,T=T,triangle_scales=[a,c],parallelogram_sides=[width,b*c],
                strip_counts=strips,tile_count=count,macro_pair_checks=pairs)


def check_pair(u,v):
    assert 0<u<v and gcd(u,v)==1
    a,b,c=u*v,v*v-u*u,v*v
    f=(b-1)*(c-1)
    hu=ceil(F(a*a+b*b+f,u*b))
    hv=ceil(F(a*a+f,b*v))
    apex=apex_shell(u,v,hu)
    base=base_shell(u,v,hv)
    t0=v*ceil(F(hu,v))
    conductor=t0+(u-1)*(v-1)
    return dict(u=u,v=v,tile=[a,b,c],Hu=hu,Hv=hv,
                W_beta_conductor=conductor,apex=apex,base=base)


if __name__=="__main__":
    results=[check_pair(u,v) for v in range(2,51)
             for u in range(1,v) if gcd(u,v)==1]
    out=dict(status="PASS",primitive_parameter_pairs=len(results),
             apex_shells=len(results),base_shells=len(results),
             macro_pair_checks=sum(r["apex"]["macro_pair_checks"]+
                                   r["base"]["macro_pair_checks"] for r in results),
             named=[r for r in results if (r["u"],r["v"]) in ((1,2),(2,3),(3,4))],
             scope="Exact macroregions, shell nesting, triangle SSS, integral strip cells and count identities; not individual-tile replay.")
    print(json.dumps(out,indent=2))
