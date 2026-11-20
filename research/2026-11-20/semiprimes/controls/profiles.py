"""Construct a variable-depth grid for the exceptional triple-scale layouts."""
from math import gcd

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def scale(n,p): return (n*p[0],n*p[1])
def neg(p): return scale(-1,p)


def make(a,b,c,h,L0,steps):
    """steps = (horizontal advance, vertical advance, new scaffold depth)."""
    assert a>b>0 and gcd(a,b)==1 and a*a+a*b+b*b==c*c
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
    depth=L0
    p=add(H,scale(-depth*b,ex))
    previous_r=depth*b
    uu,vv=depth*b,0
    for idx in range(len(steps)+1):
        final=idx==len(steps)
        r,s,new_depth=(0,depth*a,depth) if final else steps[idx]
        assert 0<previous_r<=depth*b and 0<s<=depth*a
        assert p[0]>=0 and p[1]>=0 and uu>=vv+s
        trap(p,ex,w,depth*b,previous_r)
        trap(p,ey,z,depth*a,s)
        ray=add(H,scale(-vv,add(u,v)))
        tri(ray,neg(u),neg(add(u,v)),s)
        rect=add(ray,scale(-s,u))
        para(rect,neg(u),neg(v),uu-vv-s,s,"sum")
        vv+=s
        if final:break
        t,rem=divmod(a*(r-(new_depth-depth)*b)-b*s,c)
        assert rem==0 and t>=0
        dx=r*c-t*a
        dy=s*c+t*b
        assert dx%b==0 and dy%a==0 and dy>0
        assert p[0]%(b*c)==0
        para((0,p[1]),xs,ys,p[0]//(b*c),dy//a,"sum")
        tip=add(p,scale(s,ey))
        tri(tip,(a*c,b*c),(0,b*c),t)
        p=add(p,(-dx*c,dy*c));previous_r=r
        uu+=r;depth=new_depth
    assert uu==vv==h*c and p==(0,V[1]-depth*a*c*c)
    return dict(tile=[a,b,c],target=[(0,0),H,V],coordinate_denominator=c,
                board_scale=h,count=h*h*(a+2*b)*(2*a+b),steps=steps,blocks=blocks)


def exceptional_three(u):
    assert u>=13 and u%3==1
    a,b,c=(u*u-1)//3,(2*u+1)//3,(u*u+u+1)//3
    k=(u-10)//3
    steps=[]
    n_tot=2*u+6
    for i in range(n_tot):
        m=4 if i<k else 1
        drop=i==k-1
        depth=3 if i<k-1 else 1
        r=(1+(u+1)*m)//3-(2*b if drop else 0)
        s=(u-m)//3
        steps.append((r,s,depth))
    return make(a,b,c,3,3,steps)


