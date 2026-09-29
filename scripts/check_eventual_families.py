"""Exact checks of macrodissections and gluing in the eventual theorem.

All decisions use rational arithmetic in coordinates (x,y*sqrt(D)).
We check every pair of macroregions, not every pair of individual tiles.
The grid fillings are justified by integral repetition counts and SSS.
"""
from fractions import Fraction as F
from math import gcd
import json

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")


def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(p,r): return (p[0]*r,p[1]*r)
def cross(o,p,q):
    return (p[0]-o[0])*(q[1]-o[1])-(p[1]-o[1])*(q[0]-o[0])
def area2(poly):
    return sum(cross(poly[0],poly[i],poly[i+1]) for i in range(1,len(poly)-1))
def ccw(poly):
    return tuple(poly) if area2(poly)>=0 else tuple(reversed(poly))
def sq(p,q,D):
    x,y=sub(p,q)
    return x*x+D*y*y
def sides2(poly,D):
    return sorted(sq(poly[i],poly[(i+1)%len(poly)],D) for i in range(len(poly)))
def ceil(x): return -((-x.numerator)//x.denominator)


def verify_partition(target,regions):
    target=ccw(target)
    pieces=[ccw(p) for p in regions if area2(p)]
    for p in pieces:
        assert all(cross(p[i],p[(i+1)%len(p)],x)>=0
                   for i in range(len(p)) for x in p)
        assert all(cross(target[i],target[(i+1)%len(target)],x)>=0
                   for i in range(len(target)) for x in p)
    assert sum(area2(p) for p in pieces)==area2(target)
    pairs=0
    for i,p in enumerate(pieces):
        for q in pieces[:i]:
            assert any(all(cross(r[j],r[(j+1)%len(r)],x)<=0 for x in s)
                       for r,s in ((p,q),(q,p)) for j in range(len(r)))
            pairs+=1
    return pairs


def represent(n,a,b):
    for y in range(a):
        if n>=b*y and (n-b*y)%a==0:
            return ((n-b*y)//a,y)
    raise AssertionError((n,a,b))


def theta_macro(u,v,T=None):
    assert 0<u<v and gcd(u,v)==1
    a,b,c=u*v,v*v-u*u,v*v
    D=4*v*v-u*u
    delta=b*(a*a+b*b)-a*a*c
    assert delta>0
    f=(a-1)*(b-1)
    bound=ceil(F((a*a*c+f)*(a*a+b*b),u*delta))
    T=bound if T is None else T
    assert T>=bound
    j=ceil(F(u*T,a*a+b*b))
    assert F(u*T,a*a+b*b)<=j<=F(u*b*T-f,a*a*c)
    mu=F(b*T,v)
    p=a*a*j; q=a*b*j; r=mu-F(p*c,a)
    red=a*u*u*j
    yellow=v*T-a*c*j
    pink=u*T-a*a*j
    h=a*((a*a+b*b)*j-u*T)
    assert q==F(p*b,a) and red==F(p*a,c)
    assert yellow==F((mu-q)*c,b) and pink==F((mu-q)*a,b)
    assert h==q*b-pink*a
    assert min(p,q,red,yellow,pink)>0 and r>=0 and h>=0
    A=(F(0),F(0)); C=(mu*a,F(0)); B=(mu*a/2,mu*v/2)
    PP=(F(p*c),F(0))
    G=(F(p*b*(b+c),2*c),F(p*b*u,2*c))
    K=(F(q*a,2),F(q*v,2))
    L=((mu+yellow)*a/2,(mu-yellow)*v/2)
    off=(F(-red*b*a,2*c),F(red*b*v,2*c))
    QQ=add(PP,off); R=add(C,off)
    V=add(K,mul(sub(G,K),F(pink*a,q*b)))
    regions=[(A,PP,G),(A,G,K),(B,K,L),(PP,G,QQ),(K,L,V),
             (PP,C,R,QQ),(G,R,L,V)]
    scales=[p,q,yellow,red,pink]
    for region,scale in zip(regions,scales):
        assert sides2(region,D)==sorted(scale*scale*z*z for z in (a,b,c))
    base_length=u*b*T-a*a*c*j
    base_height=a*b*u*u*j
    assert sides2(regions[5],D)==sorted([base_length**2]*2+[base_height**2]*2)
    x,y=represent(base_length,a,b)
    assert base_height%a==base_height%b==0
    cap_length=b*(u*T-a*a*j)
    cap_height=h
    assert sides2(regions[6],D)==sorted([cap_length**2]*2+[cap_height**2]*2)
    assert cap_length%b==0 and cap_height%a==0
    counts=[k*k for k in scales]+[2*base_length*base_height//(a*b),
                                 2*cap_length*cap_height//(a*b)]
    assert sum(counts)==b*T*T
    pairs=verify_partition((A,B,C),regions)
    return {'u':u,'v':v,'tile':[a,b,c],'T':T,'bound':bound,'J':j,
            'Delta':delta,'N':b*T*T,'macro_counts':counts,
            'base_strip_decomposition':[x,y],'macro_pair_checks':pairs,
            'all_macro_sss_containment_area_nonoverlap':'PASS'}


def transfers(u,v,T=1):
    a,b,c=u*v,v*v-u*u,v*v
    Q=b+c; P=b+2*c; D=4*v*v-u*u
    A=(F(0),F(0)); C=(F(u*b*T),F(0)); B=(F(u*b*T,2),F(b*T,2))
    E=(F(-u*c*T),F(0)); W=(F(u*Q*T),F(0))
    theta=(A,B,C)
    first=(B,C,W);second=(E,A,B)
    want=sorted((v*T*z)**2 for z in (a,b,c))
    assert sides2(first,D)==want and sides2(second,D)==want
    assert sides2((A,B,W),D)==sorted(z*z for z in (b*v*T,v**3*T,u*Q*T))
    assert sides2((E,B,W),D)==sorted(z*z for z in (v**3*T,v**3*T,u*P*T))
    verify_partition((A,B,W),(theta,first))
    verify_partition((E,B,W),(theta,first,second))
    # The alpha transfer uses theta at scale vT.
    A2=A; C2=(F(a*b*T),F(0));B2=(F(a*b*T,2),F(b*v*T,2))
    E2=mul(B2,F(-b,c))
    assert sides2((A2,C2,E2),D)==sorted((b*T*z)**2 for z in (a,b,c))
    assert sides2((B2,C2,E2),D)==sorted(z*z for z in (b*c*T,b*c*T,b*Q*T))
    verify_partition((B2,C2,E2),((A2,B2,C2),(A2,C2,E2)))
    return {'u':u,'v':v,'scale':T,'theta_to_W_to_beta':'PASS','theta_to_alpha':'PASS'}


if __name__=='__main__':
    named=[theta_macro(1,2),theta_macro(1,3),theta_macro(3,5)]
    sweep=[]
    for v in range(2,26):
        for u in range(1,v):
            if gcd(u,v)>1: continue
            a,b,c=u*v,v*v-u*u,v*v
            if b*(a*a+b*b)>a*a*c:
                sweep.append(theta_macro(u,v))
    joins=[transfers(u,v,2) for v in range(2,26) for u in range(1,v) if gcd(u,v)==1]
    out={'named_macro_checks':named,'general_macro_sweep':len(sweep),
         'transfer_parameter_pairs':len(joins),'status':'PASS',
         'scope':'Exact macroregions and integral grid counts; not individual-tile replay.'}
    print(json.dumps(out,indent=2))
