"""Construct exact F2 dissections into grid blocks and positive convex notches."""
from math import gcd

def add(p,q): return (p[0]+q[0],p[1]+q[1])
def scale(n,p): return (n*p[0],n*p[1])
def neg(p): return scale(-1,p)


def make(a,b,c,h,L0,steps,extend=0,cap=0,allow_left_padding=False):
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
        assert 0<previous_r and 0<s<=depth*a
        assert (p[0]>=0 or allow_left_padding) and p[1]>=0 and uu>=vv+s
        oversize = not final and r > new_depth*b
        strip = cap if oversize else 0
        extender = extend if oversize else 0
        if strip:
            assert extender == s and previous_r >= depth*b and 0 < strip <= depth*b
            assert strip <= uu-vv-s
            tri(add(p,scale(strip,ex)),ex,w,depth*b-strip)
        else:
            trap(p,ex,w,depth*b,min(previous_r,depth*b))
        assert 0 <= extender <= s
        trap(p,ey,z,depth*a,s-extender)
        ray=add(H,scale(-vv,add(u,v)))
        tri(ray,neg(u),neg(add(u,v)),s)
        rect=add(ray,scale(-s,u))
        para(rect,neg(u),neg(v),uu-vv-s-strip,s,"sum")
        vv+=s
        if final:break
        t,rem=divmod(a*(r-(new_depth-depth)*b)-b*s,c)
        assert rem==0
        dx=r*c-t*a
        dy=s*c+t*b
        assert dx%b==0 and dy%a==0 and dy>0
        assert p[0]%(b*c)==0
        para((0,p[1]),xs,ys,p[0]//(b*c),dy//a,"sum")
        tip=add(p,scale(s,ey))
        if r <= new_depth*b:
            sign=1 if t>=0 else -1
            tri(tip,scale(sign,(a*c,b*c)),(0,sign*b*c),abs(t))
        else:
            gap = r-new_depth*b
            end = add(tip,scale(t,(a*c,b*c)))
            A=add(tip,scale(-extender,ey))
            D=add(end,scale(-gap,w))
            poly=[A,add(tip,scale(t,(0,b*c))),add(end,scale(-gap,ex)),D]
            if strip:
                poly[-1] = add(D,scale(strip,u))
                poly.append(add(poly[-1],scale(s,v)))
                poly.append(add(p,scale(strip,ex)))
            elif extender: poly.append(add(D,scale(extender,v)))
            blocks.append(dict(kind="notch",scale=t,notch=gap,extend=extender,
                               width=depth*a-s,cap=strip,depth=depth,points=poly))

        p=add(p,(-dx*c,dy*c));previous_r=r
        uu+=r;depth=new_depth
    assert uu==vv==h*c and p==(0,V[1]-depth*a*c*c)
    return dict(tile=[a,b,c],target=[(0,0),H,V],coordinate_denominator=c,
                board_scale=h,count=h*h*(a+2*b)*(2*a+b),steps=steps,blocks=blocks)


