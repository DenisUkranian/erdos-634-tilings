"""Generate the fixed layouts used in the scale-three to scale-six extraction test."""
from math import gcd
from .grid_layout import make
from .profiles import exceptional_three

def recipe(u,v,h):
    g=gcd(3,u-v)
    a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
    assert gcd(u,v)==1 and a>b>0 and h>=4
    if u<(h+1)*v:
        L=h
        steps=[(c-b,c-a)]*h
    else:
        L=3
        N=(h-L)*u+2*h*v
        M=h*u-(h+L)*v
        lo,high=divmod((M-N)//g,N)
        js=[1+g*lo]*(N-high)+[1+g*(lo+1)]*high
        assert max(js)<=4 and sum(js)==M and min(js)>=1
        steps=[((v+(u+v)*j)//g,(u-v*j)//g) for j in js]
    return a,b,c,L,steps

def instance(u,v,h):
    a,b,c,L,steps=recipe(u,v,h)
    return make(a,b,c,steps,h,L)

def triple(u,v):
    """Construct scale 3. An exceptional family changes scaffold depth once."""
    g=gcd(u-v,3)
    a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
    assert gcd(u,v)==1 and a>b
    if c<=4*b:
        return make(a,b,c,[(c-b,c-a)]*3,3,3)
    if v==1 and g==3 and u>=13:
        result=exceptional_three(u)
        result['dilation']=result['board_scale']
        return result
    if v==1 and g==3:
        assert u==10
        return make(a,b,c,[(15,2)]*6,3,3)
    N=u+6*v;M=3*u-5*v
    lo,high=divmod((M-N)//g,N)
    js=[1+g*lo]*(N-high)+[1+g*(lo+1)]*high
    assert sum(js)==M and min(js)>=1 and max(js)<=4
    steps=[((v+(u+v)*j)//g,(u-v*j)//g) for j in js]
    return make(a,b,c,steps,3,2)
