"""Generate exact compressed W/beta tilings.
Reuses the credited triquadratic seed and apex-annulus motif; the arithmetic
square-class reduction and exact strip threshold are proved in PROOF.md.
"""
from __future__ import annotations
from fractions import Fraction as F
from arithmetic import bounds,plan

def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def mul(k,p): return k*p[0],k*p[1]
def enc(p): return [[F(z).numerator,F(z).denominator] for z in p]
def tri(points,n):return {'type':'triangle_grid','vertices':[enc(p) for p in points],'n':n}
def para(points,r,s,diag='difference'):
    return {'type':'parallelogram_grid','vertices':[enc(p) for p in points],
            'rows':r,'columns':s,'diagonal':diag}

def canonical(u,v):
    k=bounds(u,v);a,b,c,Q=k['a'],k['b'],k['c'],k['Q']
    A=(F(b*b),F(0));O=(F(0),F(0))
    C=(F(-u*u*b,2),F(u*b,2));D=(C[0],-C[1])
    E=(F(-u*u*Q,2),F(-u**3,2));B=add(D,E)
    points={'A':A,'O':O,'C':C,'D':D,'E':E,'B':B}
    conv=lambda p:mul(F(1,v),sub(p,A))
    f=(-F(b*v),F(0));z=conv(B);cvec=conv(C)
    metric=4*v*v-u*u
    axis=add(f,cvec)
    def reflect(p):
        dot=p[0]*axis[0]+metric*p[1]*axis[1]
        den=axis[0]*axis[0]+metric*axis[1]*axis[1]
        return sub(mul(2*dot/den,axis),p)
    return points,f,z,cvec,reflect(z)

def seed(u,v,r,family):
    k=bounds(u,v);a,b=k['a'],k['b']
    p,f,z,cv,z2=canonical(u,v)
    cvt=lambda name:mul(r,sub(p[name],p['A']))
    blocks=[tri([cvt(x) for x in row],size*r)
            for row,size in [('OAC',b),('OAD',b),('OCE',a)]]
    blocks.append(para([cvt(x) for x in 'ODBE'],b*r,u*u*r))
    if family=='beta':
        s=r*v
        blocks.append(tri([(F(0),F(0)),mul(s,cv),mul(s,z2)],v*s))
    return blocks

def tile_annulus(x,y,k,h):
    """x,y are two vectors of a primitive tile based at zero."""
    kx=mul(k,x);ky=mul(k,y);top=mul(k+h,y);corner=add(kx,mul(h,y))
    return [tri([kx,mul(k+h,x),corner],h),
            para([kx,ky,top,corner],k,h)]

def shell(u,v,T,family):
    k=bounds(u,v);a,b,c,Q,R=[k[x] for x in ('a','b','c','Q','R')]
    x=u*T-b-c*(R-1);y=b*R-c
    if x<0 or y<0:raise ValueError('The shell has no nonnegative mixed-strip filling')
    A=(F(0),F(0));C=(F(u*b*(T+u)),F(0))
    B=(F(u*u*b,2),F(u*b,2));E=add(B,(F(u*b*T),F(0)))
    D=add(B,(F(a*a),F(0)));Rpoint=(F(c*c),F(0));S=sub(E,(F(b*b),F(0)))
    apex=(F(u*b*(T+u),2),F(b*(T+u),2));metric=4*v*v-u*u
    def cvt(p):
        px,py=sub(p,apex)
        return (F(u*px+metric*py,2*v),F(px-u*py,2*v))
    blocks=[tri([cvt(p) for p in row],scale)
            for row,scale in [([A,B,D],a),([A,D,Rpoint],c),([S,E,C],b)]]
    V=sub(D,Rpoint)
    if x:
        W=(F(x*b),F(0));start=Rpoint
        blocks.append(para([cvt(p) for p in [start,add(start,V),add(add(start,V),W),add(start,W)]],b,x,'sum'))
    if y:
        W=(F(y*c),F(0));start=add(Rpoint,(F(x*b),F(0)))
        blocks.append(para([cvt(p) for p in [start,add(start,V),add(add(start,V),W),add(start,W)]],c,y,'sum'))
    _,f,z,cv,z2=canonical(u,v)
    blocks+=tile_annulus(mul(F(1,v),f),mul(F(1,v),z),v*T,v*u)
    if family=='beta':
        blocks+=tile_annulus(mul(F(1,v),cv),mul(F(1,v),z2),v*T,v*u)
    return blocks

def generate(u:int,v:int,m:int,family:str='W')->dict:
    if family not in ('W','beta'):raise ValueError('Unknown family')
    p=plan(u,v,m);k=bounds(u,v)
    blocks=seed(u,v,p['seed_factor'],family)
    stages=[{'kind':'seed','scale':p['seed_scale'],'block_end':len(blocks)}]
    T=p['seed_scale']
    for _ in range(p['steps']):
        blocks+=shell(u,v,T,family)
        T+=u
        stages.append({'kind':'shell','scale':T,'block_end':len(blocks)})
    _,f,z,cv,z2=canonical(u,v)
    target=[(F(0),F(0)),mul(m,z),mul(m,cv if family=='W' else z2)]
    coef=k['Q'] if family=='W' else k['P']
    return dict(format='erdos634-saturation-macro-v1',u=u,v=v,m=m,family=family,
                metric_D=4*v*v-u*u,tile_sides=[k[x] for x in ('a','b','c')],
                tile_count=coef*m*m,target=[enc(p) for p in target],blocks=blocks,
                stages=stages,arithmetic_plan=p,
                attribution='Triquadratic seed: Beeson; old apex annulus: 29 September project. '
                'This certificate integrates them with the exact mixed-strip threshold.',
                expanded_individual_tiles=False)
