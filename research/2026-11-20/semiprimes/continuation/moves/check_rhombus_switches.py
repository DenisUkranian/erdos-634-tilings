"""Regenerate three F2 patch fillings in exact axial coordinates."""
from collections import Counter, defaultdict
from fractions import Fraction
from math import ceil, floor, gcd, isqrt


def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def mul(k,p): return k*p[0],k*p[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2


def triangle(p,q,r):
    return (p,q,r) if det(sub(q,p),sub(r,p))>0 else (p,r,q)


def grid(base,e,f,n,m,diagonal_sum):
    for i in range(n):
        for j in range(m):
            o=add(base,add(mul(i,e),mul(j,f)))
            x,y=add(o,e),add(o,f)
            v=add(x,f)
            if diagonal_sum:
                halves=(triangle(o,x,v),triangle(o,y,v))
            else:
                halves=(triangle(o,x,y),triangle(x,y,v))
            yield i,j,halves


def boundary(polygons):
    lines=defaultdict(Counter)
    for poly in polygons:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            dx,dy=sub(q,p)
            length=gcd(dx,dy)
            ux,uy=dx//length,dy//length
            if (ux,uy)<(0,0):
                ux,uy=-ux,-uy
            events=lines[ux,uy,ux*p[1]-uy*p[0]]
            events[p]+=1
            events[q]-=1
    return {k: {p:n for p,n in v.items() if n} for k,v in lines.items() if any(v.values())}


def check(a,b,c,k=2):
    # All unrotated numerators have denominator c.
    p,q=a+2*b,2*a+b
    e=mul(b,(b,a))
    f=(c*c,0)
    start=(0,0)
    first=grid(start,mul(c,(b,a)),(b*c,0),k*b,c,False)
    initial=[t for _,_,halves in first for t in halves]
    intermediate=[]
    final=[]
    m=(k*c-b)//a
    for i,j,halves in grid(start,e,f,k*c,b,False):
        intermediate.extend(halves)
        # Both triangles have the same diagonal at i+j+1; their interiors
        # occupy the two adjacent open unit intervals of the i+j coordinate.
        for h,t in enumerate(halves):
            if not b<=i+j+h<b+m*a:
                final.append(t)
    for j in range(m):
        origin=mul(b+j*a,e)
        switched=grid(origin,mul(a,(b,a)),mul(b,(a+b,-b)),b,a,True)
        final.extend(t for _,_,halves in switched for t in halves)
    corner1=mul(k*c,e)
    corner2=mul(b,f)
    outer=(start,corner2,add(corner1,corner2),corner1)
    assert det(corner2,corner1)>0
    shell=boundary([outer])
    for patch in (initial,intermediate,final):
        assert len(patch)==2*k*b*c
        assert boundary(patch)==shell
        for t in patch:
            assert det(sub(t[1],t[0]),sub(t[2],t[0]))==a*b*c*c
            assert sorted(norm(sub(s,r)) for r,s in zip(t,t[1:]+t[:1]))==sorted((v*c)**2 for v in (a,b,c))
    assert {tuple(sorted(t)) for t in final} != {tuple(sorted(t)) for t in initial}
    # Translation along the board side distinguishes the patch from the corner cap.
    fit=Fraction(a,q)+Fraction(k*b*c,a*p)
    delta=min(Fraction(1),Fraction(a*p,2)*(1-fit))
    assert delta>0
    for v in ((0,0),(-a*b,b*(a+b)),(0,k*b*c),(-a*b,b*(a+b)+k*b*c)):
        x,y=add((a*b,delta),v)
        assert x>=0 and y>0 and Fraction(x,b*q)+Fraction(y,a*p)<1
    print(f'{p*q}: {len(initial)} tiles at each stage, {m} second-stage rhombi, fit {fit}.')


def surrounding(a,b,c):
    p,q=a+2*b,2*a+b
    H,V=b*q,a*p
    # Numerators of the anchor and basis, on an integer grid of denominator c.
    X=(a*b*c,c)
    u=(0,c*c)
    v=(-a*b,b*(a+b))
    coords=[]
    for corner in ((0,0),(H*c,0),(0,V*c)):
        d=sub(corner,X)
        coords.append((Fraction(det(d,v),det(u,v)),Fraction(det(u,d),det(u,v))))
    def inside(i,j):
        x,y=add(X,add(mul(i,u),mul(j,v)))
        return x>=0 and y>=0 and V*x+H*y<=H*V*c
    total=0
    for i in range(floor(min(x for x,y in coords))-1,ceil(max(x for x,y in coords))+1):
        for j in range(floor(min(y for x,y in coords))-1,ceil(max(y for x,y in coords))+1):
            if inside(i+1,j) and inside(i,j+1):
                total+=int(inside(i,j))+int(inside(i+1,j+1))
    assert all(inside(i,j) for i in (0,2*b) for j in (0,c))
    print(f'{p*q}: rotated initial grid contains {total} whole tiles.')
    return total


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    for tile in ((33,7,37),(35,13,43)):
        check(*tile)
    assert surrounding(33,7,37)==3248
    assert surrounding(35,13,43)==4846
    count=0
    for a in range(2,650):
        for b in range(1,a):
            c=isqrt(a*a+a*b+b*b)
            if gcd(a,b)>1 or c*c!=a*a+a*b+b*b: continue
            p,q=a+2*b,2*a+b
            assert all(Fraction(2*a*b,s)+Fraction(2*s,p*q)>1 for s in (a*p,b*q,c*c))
            if a>=2*b: assert 4*a*c>p*q
            if 2*a>=5*b: assert Fraction(a,q)+Fraction(2*b*c,a*p)<1
            count+=1
    print(f'Area, width and fit bounds checked for {count} primitive triples.')
