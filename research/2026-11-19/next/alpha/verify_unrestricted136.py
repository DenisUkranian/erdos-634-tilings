"""Check a finite endpoint and point-packing lower bound over arbitrary rotations/translations."""
import gzip
import json
from math import gcd
from pathlib import Path
import sys

def sub(u, v):
    return u[0]-v[0], u[1]-v[1]

def cross(u,v):
    return u[0]*v[1]-u[1]*v[0]

def area(a,b,c):
    return cross(sub(b,a),sub(c,a))

def axis(u,v):
    g=gcd(u,v)
    if (u,v)<(0,0):
        g=-g
    return u//g,v//g

def main(filename):
    with gzip.open(filename,'rt') as f:
        data=json.load(f)
    mass=data['mass_weight']
    assert mass>0 and data['endpoint_denominator']==2*3**24 and data['packing_denominator']==32
    rows,packing=data['endpoints'],data['packing']
    max_h=max(abs(h) for _,_,h,_ in rows)
    E=max(24,max_h+7); D=32*3**E
    scale=D//data['endpoint_denominator']
    Y={(x*scale,y*scale,h):v for x,y,h,v in rows}
    assert len(Y)==len(rows)
    points=[(x*(D//32),y*(D//32),v) for x,y,v in packing]
    assert all(w>=0 for _,_,w in points)
    units={0:(D,0)}
    for h in range(1,max_h+7):
        x,y=units[h-1];a,b=-x-35*y,x-y
        assert a%6==b%6==0
        units[h]=(a//6,b//6);units[-h]=(a//6,-b//6)
    axes={axis(x,y):h for h,(x,y) in units.items()}
    assert len(axes)==len(units)
    exterior=[(0,0),(136*D,0),(68*D,4*D)]
    sides=list(zip(exterior,exterior[1:]+exterior[:1],[136,72,72]))
    semigroup={0}
    for m in range(137):
        if m in semigroup: semigroup.update(m+s for s in [3,8,9])
    def inside(pt):
        x,y=pt
        for p,q,l in sides:
            z=area(p,q,pt)
            if z<0:return False
            if not z:
                n,rem=divmod((x-p[0])*l,q[0]-p[0])
                if rem or n not in semigroup or l-n not in semigroup: return False
        return True
    def gain(tri):
        val=0
        for (x,y),(u,v) in zip(tri,tri[1:]+tri[:1]):
            h=axes[axis(u-x,v-y)]
            val+=Y.get((x,y,h),0)-Y.get((u,v,h),0)
        return val
    angles=[(2,-1),(-3,1),(1,1)]
    lengths=[3,8,9]
    templates={}
    for h in {r[2] for r in Y}:
        patterns=set()
        ex,ey=units[h]
        for n,l in enumerate(lengths):
            for m,k in enumerate(lengths):
                if n==m:continue
                delta,flip=angles[3-m-n]
                for sg in [-1,1]:
                    q=(sg*l*ex,sg*l*ey)
                    for turn in [-1,1]:
                        u,v=units[h+turn*delta]
                        r=(sg*k*flip*u,sg*k*flip*v)
                        assert cross(q,r)
                        patterns.add((q,r) if cross(q,r)>0 else (r,q))
        # Independent inventory by the cosine law. In the unit-edge frame,
        # twice the axial area is 4, hence the third vertex has height +/-4/l.
        metric=set()
        for l in lengths:
            for m in lengths:
                if l==m:continue
                n=next(k for k in lengths if k!=l and k!=m)
                proj=l*l+m*m-n*n
                for sg in [-1,1]:
                    vx,vy=sg*ex,sg*ey
                    q=l*vx,l*vy
                    for hand in [-1,1]:
                        nx=proj*vx-280*hand*vy
                        ny=proj*vy+8*hand*vx
                        assert nx%(2*l)==ny%(2*l)==0
                        r=nx//(2*l),ny//(2*l)
                        metric.add((q,r) if cross(q,r)>0 else (r,q))
        assert metric==patterns
        templates[h]=patterns
    seen=set(); cap=0
    for x,y,h in Y:
        p=x,y
        for q,r in templates[h]:
            b=(x+q[0],y+q[1]);c=(x+r[0],y+r[1])
            if not inside(b) or not inside(c) or not inside(p):continue
            tri=(p,b,c);key=tuple(sorted(tri))
            if key in seen:continue
            seen.add(key)
            excess=gain(tri)-mass
            if excess<=0:continue
            for i,j,w in points:
                test=(i,j)
                if area(p,b,test)>0 and area(b,c,test)>0 and area(c,p,test)>0:
                    excess-=w
                    if excess<=0:break
            cap+=max(0,excess)
    demand=gain(tuple(exterior)); point_cap=sum(w for _,_,w in points)
    lb=demand-point_cap-cap
    print(f'weighted endpoints={len(Y)} placements={len(seen)} demand={demand} packing={point_cap} positive excess={cap} mass weight={mass}')
    print(f'exact lower bound {lb}/{mass}; at least {-(-lb//mass)} unit tiles')
    if 'claimed_numerator' in data:
        assert lb>=data['claimed_numerator']
    return lb,mass

if __name__=='__main__':
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('unrestricted136.json.gz'))
