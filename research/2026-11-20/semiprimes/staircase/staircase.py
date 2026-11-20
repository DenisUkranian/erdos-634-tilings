"""Exact primitive F2 tilings from a list of staircase steps.

All coordinates are in the basis (1, exp(pi*i/3)), multiplied by c.
Run this file to emit compact grid witnesses for the listed prime pairs.
"""
from math import gcd
from pathlib import Path
import json


def add(p,q): return (p[0]+q[0],p[1]+q[1])
def scale(n,p): return (n*p[0],n*p[1])
def neg(p): return scale(-1,p)


def make(a,b,c,steps):
    assert a>b>0 and gcd(a,b)==1 and a*a+a*b+b*b==c*c
    assert (sum(r for r,s in steps),sum(s for r,s in steps))==(c-b,c-a)
    for r,s in steps:
        assert 0<r<=b and 0<s<=a and a*r>=b*s and (a*r-b*s)%c==0
    H=(b*(2*a+b)*c,0)
    V=(0,a*(a+2*b)*c)
    u=(b*(a+b),-a*b)
    v=(a*b,-a*(a+b))
    w=(a*a,a*b)
    z=(a*b,b*b)
    ex=(c*c,0)
    ey=(0,c*c)
    xs=(b*c,0)
    ys=(0,a*c)
    blocks=[]
    def tri(p,e,f,k):
        if k>0:
            blocks.append(dict(kind="triangle",points=[p,add(p,scale(k,e)),add(p,scale(k,f))],scale=k))
    def para(p,e,f,rows,cols,diag):
        if rows>0 and cols>0:
            q=add(p,scale(rows,e));r=add(p,scale(cols,f))
            blocks.append(dict(kind="parallelogram",points=[p,q,add(q,scale(cols,f)),r],rows=rows,cols=cols,diagonal=diag))
    def trap(p,e,f,n,k):
        # The band x<=k of the simplex x+y<=n in these cell axes.
        t=add(p,scale(n-k,f))
        para(p,e,f,k,n-k,"difference")
        tri(t,e,f,k)
    p=add(H,scale(-b,ex))
    previous_r=b
    uu,vv=b,0
    for idx,s in enumerate([s for r,s in steps]+[a]):
        trap(p,ex,w,b,previous_r)
        trap(p,ey,z,a,s)
        # Outer side, in coordinates H-Uu-Vv, bounds diagonal U=V.
        ray=add(H,scale(-vv,add(u,v)))
        tri(ray,neg(u),neg(add(u,v)),s)
        rect=add(ray,scale(-s,u))
        para(rect,neg(u),neg(v),uu-vv-s,s,"sum")
        vv+=s
        if idx==len(steps): break
        r,s=steps[idx];t=(a*r-b*s)//c
        dx=r*c-t*a
        dy=s*c+t*b
        assert dx%b==0 and dy%a==0 and dx>0 and dy>0
        assert p[0]%(b*c)==0
        para((0,p[1]),xs,ys,p[0]//(b*c),dy//a,"sum")
        tip=add(p,scale(s,ey))
        tri(tip,(a*c,b*c),(0,b*c),t)
        p=add(p,(-dx*c,dy*c));previous_r=r
        uu+=r
    assert uu==vv==c and p==(0,V[1]-a*c*c)
    return dict(tile=[a,b,c],target=[(0,0),H,V],coordinate_denominator=c,
                count=(a+2*b)*(2*a+b),steps=steps,blocks=blocks)


examples=[
    (5,3,7,[(2,1),(2,1)]),
    (187,93,247,[(20,11)]*5+[(54,5)]),
    (247,105,313,[(22,13)]*5+[(98,1)]),
    (475,141,559,[(28,19)]*3+[(78,13),(128,7),(128,7)]),
    (649,455,961,[(273,5),(24,11),(209,296)]),
    (3325,2291,4891,[(1176,1),(241,21),(54,25),(54,25),(54,25),(469,670),(552,799)]),
    (7289,5031,10729,[(1742,1),(1465,7),(80,37),(80,37),(695,992),(818,1183),(818,1183)]),
]

if __name__=='__main__':
    for a,b,c,steps in examples:
        data=make(a,b,c,steps)
        path=Path(__file__).parent/('certificate_%d.json'%data['count'])
        path.write_text(json.dumps(data,separators=(',',':'))+'\n')
        print(data['count'],len(data['blocks']),path.name)
