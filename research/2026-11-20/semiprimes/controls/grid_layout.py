"""Construct a constant-depth grid certificate in scaled Eisenstein coordinates."""
from math import gcd

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def scale(n,p): return (n*p[0],n*p[1])
def neg(p): return scale(-1,p)


def make(a,b,c,steps,h,L):
    assert a>b>0 and gcd(a,b)==1 and a*a+a*b+b*b==c*c
    assert (sum(r for r,s in steps),sum(s for r,s in steps))==(h*c-L*b,h*c-L*a)
    for r,s in steps:
        assert 0<r<=L*b and 0<s<=L*a and a*r>=b*s and (a*r-b*s)%c==0
    H=(h*b*(2*a+b)*c,0)
    V=(0,h*a*(a+2*b)*c)
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
    p=add(H,scale(-L*b,ex))
    previous_r=L*b
    uu,vv=L*b,0
    for idx,s in enumerate([s for r,s in steps]+[L*a]):
        trap(p,ex,w,L*b,previous_r)
        trap(p,ey,z,L*a,s)
        # Outer side, in coordinates H-Uu-Vv, bounds diagonal U=V.
        ray=add(H,scale(-vv,add(u,v)))
        tri(ray,neg(u),neg(add(u,v)),s)
        assert uu>=vv+s
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
    assert uu==vv==h*c and p==(0,V[1]-L*a*c*c)
    return dict(tile=[a,b,c],target=[(0,0),H,V],coordinate_denominator=c,
                dilation=h,count=h*h*(a+2*b)*(2*a+b),steps=steps,blocks=blocks)


