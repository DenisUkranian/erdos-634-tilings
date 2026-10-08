#!/usr/bin/env python3
"""Exact two-parameter all-scale seed audit, using polynomials in p,q.

Set t=q+2, u=p+q+3. Nonnegative coefficients prove all sign conditions
throughout 2<=t<=u-1. No sampled values are premises of the identities.
"""
from collections import Counter
from pathlib import Path
import json


class P:
    def __init__(self,x=0):
        d=dict(x.d) if isinstance(x,P) else dict(x) if isinstance(x,dict) else {(0,0):x}
        self.d=tuple(sorted((k,v) for k,v in d.items() if v))
    def __add__(self,x):
        d=dict(self.d)
        for k,v in P(x).d:d[k]=d.get(k,0)+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d})
    def __sub__(self,x):return self+-P(x)
    def __rsub__(self,x):return P(x)+-self
    def __mul__(self,x):
        d={}
        for (a,b),v in self.d:
            for (c,e),w in P(x).d:
                k=(a+c,b+e);d[k]=d.get(k,0)+v*w
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,x):return self.d==P(x).d
    def __hash__(self):return hash(self.d)
    def value(self,p=1,q=1):return sum(v*p**a*q**b for (a,b),v in self.d)
    def nonnegative(self):return all(v>=0 for _,v in self.d)


def pt(x,y):return (P(x),P(y))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def edges(poly):return zip(poly,poly[1:]+poly[:1])
def area(poly):return sum((cross(a,b) for a,b in edges(poly)),P())
def rect(x0,y0,x1,y1):return [pt(x0,y0),pt(x1,y0),pt(x1,y1),pt(x0,y1)]


def audit(regions,target,directions):
    sign_checks=0;normalized=[]
    for poly in regions:
        if area(poly).value()<0:poly=list(reversed(poly))
        assert area(poly).nonnegative() and area(poly)!=0
        for a,b in edges(poly):
            for p in poly:
                assert cross(sub(b,a),sub(p,a)).nonnegative(), 'Convexity sign failed'
                sign_checks+=1
        normalized.append(poly)
    if area(target).value()<0:target=list(reversed(target))
    events=Counter()
    for weight,poly in [(1,p) for p in normalized]+[(-1,target)]:
        for a,b in edges(poly):
            e=sub(b,a);kinds=[i for i,d in enumerate(directions) if cross(d,e)==0]
            assert len(kinds)==1
            k=kinds[0];line=cross(directions[k],a)
            events[(k,line,a)]+=weight;events[(k,line,b)]-=weight
    assert not any(events.values()), 'Positioned boundary mismatch'
    assert sum((area(poly) for poly in normalized),P())==area(target)
    return normalized,sign_checks


def run():
    p=P({(1,0):1});q=P({(0,1):1});u=p+q+3;t=q+2
    v=u+1;b=2*u+1;m=v+t;a=u*v;c=v*v
    directions=[pt(1,0),pt(0,1),pt(u,-v),pt(v,-u),pt(-u*(2*v*v-u*u),v**3)]
    # Multiply the complete coordinate model by b to avoid fractions.
    O=pt(u*m*v**3,-u*u*m*v*v);X=pt(0,0)
    A=pt(-u*v*m*b,u*u*m*b);C=pt(-u*v*m*b,v*v*m*b)
    V=pt(-u*u*m*b,u*v*m*b);U=pt((-u*u*m+t*v*v)*b,u*v*v*b)
    R=pt((-u*u*v+b*(t-1))*b,u*v*v*b)
    S=pt((u*b-u*u*t)*b,u*v*t*b);Q=pt(u*b*b,0)
    PP=add(Q,pt(u*t*v**3,-u*u*t*v*v))
    R0=add(S,pt(t*u*v*v,-t*u*u*v))
    TT=add(U,pt((u-t)*v**3,-(u-t)*u*v*v))
    outside=[[O,X,Q,PP],[PP,Q,S,R0],[R0,R,U,TT],[TT,V,C]]
    def scaled(point):return (b*point[0],b*point[1])
    def shifted(poly):return [add(V,scaled(point)) for point in poly]
    lowleft=pt(-v*v*t,u*v*t);hightop=pt(-v**3,u*v*v)
    lower=[X,Q,S,scaled(lowleft)]
    center=[scaled(lowleft),S,R,scaled(hightop)]
    xx=v*v-b*m;yy=-u*v
    cap=[
        [pt(-u*m,v*m),pt(-u*m,0),pt(0,0)],
        rect(-u*m,-u*v,0,0),
        [pt(0,0),pt(0,-u*v),pt(v*v,-u*v)],
        [pt(xx+v*t,yy),pt(xx+v*v,yy),pt(xx+v*v,yy-u*v),pt(xx+v*t,yy-u*t)],
        rect(2*v*v-b*m,-2*u*v,v*v,-u*v),
        [pt(v*v,-u*v),pt(v*v,-2*u*v),pt(2*v*v,-2*u*v)],
        [pt(2*v*v-b*m,-2*u*v),pt(2*v*v,-2*u*v),pt(t*v*v,-t*u*v),pt(t*v*v-b*m,-t*u*v)],
    ]
    regions=outside+[lower,center]+[shifted(poly) for poly in cap]
    normalized,checks=audit(regions,[O,A,C],directions)
    assert area(normalized[0])!=0
    assert sum((area(poly) for poly in normalized),P())==u*v*b*b*(2*v*v-u*u)*m*m
    # Gram form: v times the squared physical norm of a coordinate vector.
    def metric(vec):
        x,y=vec
        return v**3*(x*x+y*y)+u*(3*v*v-u*u)*x*y
    for vec,length in [(pt(u,0),a),(pt(0,v),c),(pt(u,-v),b),
                       (pt(v,0),c),(pt(0,u),a),(pt(v,-u),b)]:
        assert metric(vec)==v*length*length
    gram=4*v**6-u*u*(3*v*v-u*u)**2
    assert gram==b*b*(4*v*v-u*u) and gram.nonnegative() and gram.value(0,0)>0
    for start,end,length in [(O,A,u*(2*v*v-u*u)*m),(A,C,v*b*m),(C,O,v**3*m)]:
        assert metric(sub(end,start))==v*b*b*length*length
    lengths=[[c*u*m,b*u*v,c*u*t,a*u*v],
             [a*v*t,b*u*t,a*t,c*u*t],
             [c*(b-t),b*v,c*(u-t),a*v],[a*m,b*m,c*m]]
    for poly,ww in zip(outside,lengths):
        for (start,end),length in zip(edges(poly),ww):
            assert metric(sub(end,start))==v*b*b*length*length
    for poly,rr,ss in zip(outside[:3],[u*m,v*t,b-t],[u*t,t,u-t]):
        bot=sub(poly[1],poly[0]);top=sub(poly[2],poly[3])
        assert (rr*top[0],rr*top[1])==(ss*bot[0],ss*bot[1])
        assert (rr-ss).nonnegative() and ss.nonnegative()
    # Generic horizontal periodic cell and expanding lower-cap band.
    # Here independently set u=p+3 and the unrestricted layer index j=q.
    uu=p+3;vv=uu+1;bb=2*uu+1;j=q;kk=q+1;W=bb*(uu+kk)
    dirs=[pt(1,0),pt(0,1),pt(uu,-vv),pt(vv,-uu)]
    cell_pieces=[
        [pt(0,0),pt(0,uu*vv),pt(-vv*vv,uu*vv)],
        rect(0,0,W-vv*vv,uu*vv),
        [pt(W-vv*vv,0),pt(W,0),pt(W-vv*vv,uu*vv)],
    ]
    cell=[pt(0,0),pt(W,0),pt(W-vv*vv,uu*vv),pt(-vv*vv,uu*vv)]
    _,cell_checks=audit(cell_pieces,cell,dirs)
    assert W-vv*vv==(kk-1)*uu+(uu+kk-1)*vv
    lower_width=bb*(uu+j)
    band_pieces=[
        [pt(0,0),pt(0,uu*vv),pt(-vv*vv,uu*vv)],
        rect(0,0,lower_width-uu*uu,uu*vv),
        [pt(lower_width-uu*uu,0),pt(lower_width,0),pt(lower_width-uu*uu,uu*vv)],
    ]
    band=[pt(0,0),pt(lower_width,0),pt(lower_width-uu*uu,uu*vv),pt(-vv*vv,uu*vv)]
    _,band_checks=audit(band_pieces,band,dirs)
    assert lower_width-uu*uu==j*uu+(uu+j)*vv
    # Outer annuli + residual area counts close the whole target.
    outside_count=u*u*(m*m-t*t)+(v*v-1)*t*t+(b-t)**2-(u-t)**2+m*m
    lower_count=b*t*(2*u+t);center_count=2*b*(u+t)*(v-t);upper_count=2*b*m*t
    assert lower_count+center_count+upper_count==b*(2*u*v+4*v*t+t*t)
    assert outside_count+lower_count+center_count+upper_count==(2*v*v-u*u)*m*m
    report={'status':'PASS','scope':'All integer u>=3 and 2<=t<=u-1, v=u+1, m=v+t',
            'parameter_substitution':'u=p+q+3, t=q+2, p,q>=0',
            'fixed_full_target_macroregions':len(regions),
            'zero_height_final_piece_omitted_when_t_equals_2':True,
            'full_target_convexity_sign_checks':checks,
            'generic_cell_and_band_sign_checks':cell_checks+band_checks,
            'full_positioned_boundary_identity':True,'metric_and_Gram_identities':True,
            'W_target_side_length_identities':True,
            'outside_annulus_homothety_identities':True,
            'generic_cell_and_band_partitions':True,'positive_strip_width_representations':True,
            'full_tile_count_identity':True}
    Path(__file__).with_name('all_adjacent_symbolic_verified.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    run()
