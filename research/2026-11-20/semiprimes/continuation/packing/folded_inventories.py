"""Test a finite list of unit-triangle inventories on the 3431 board.

Run with Python 3.10+ using only the standard library.
"""
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor
from itertools import product
from math import gcd
from sys import argv

A,B,C = 33,7,37
H = (B*(2*A+B)*C, 0)
V = (0, A*(A+2*B)*C)
TARGET = ((0,0), H, V)


def plus(p,q):
    return (p[0]+q[0],p[1]+q[1])


def times(n,p):
    return (n*p[0],n*p[1])


def regular_triangle(origin, first, second, width):
    if width < 0:
        first, second, width = times(-1,first), times(-1,second), -width
    for i in range(width):
        for j in range(width-i):
            p = plus(origin,plus(times(i,first),times(j,second)))
            x,y = plus(p,first),plus(p,second)
            yield (p,x,y)
            if i+j+1 < width:
                yield (x,plus(x,second),y)


def rectangle(origin, first, second, width, height, sum_diagonal):
    if width < 0 and height < 0:
        first,second = times(-1,first),times(-1,second)
        width,height = -width,-height
    for i in range(width):
        for j in range(height):
            p = plus(origin,plus(times(i,first),times(j,second)))
            q,s = plus(p,first),plus(p,second)
            r = plus(q,second)
            if sum_diagonal:
                yield (p,q,r)
                yield (p,r,s)
            else:
                yield (p,q,s)
                yield (r,q,s)


def band(p,e,f,n,k):
    k = min(k,n)
    if k > 0:
        yield from rectangle(p,e,f,k,n-k,False)
        yield from regular_triangle(plus(p,times(n-k,f)),e,f,k)


def generate(steps, initial, final):
    a,b,c = A,B,C
    u,v = (b*(a+b),-a*b),(a*b,-a*(a+b))
    w,z = (a*a,a*b),(a*b,b*b)
    ex,ey = (c*c,0),(0,c*c)
    depth=initial
    previous=initial*b
    x,y=previous,0
    tip=plus(H,times(-previous,ex))
    for i,(r,s,next_depth) in enumerate([*steps,(0,final*a,final)]):
        yield from band(tip,ex,w,depth*b,previous)
        yield from band(tip,ey,z,depth*a,s)
        ray=plus(H,times(-y,plus(u,v)))
        yield from regular_triangle(ray,times(-1,u),times(-1,plus(u,v)),s)
        yield from rectangle(plus(ray,times(-s,u)),times(-1,u),times(-1,v),x-y-s,s,True)
        y+=s
        if i==len(steps):
            break
        t,rem=divmod(a*(r-b*(next_depth-depth))-b*s,c)
        assert rem==0
        dx,dy=r*c-t*a,s*c+t*b
        assert dx%b==0 and dy%a==0
        yield from rectangle((0,tip[1]),(b*c,0),(0,a*c),tip[0]//(b*c),dy//a,True)
        yield from regular_triangle(plus(tip,times(s,ey)),(a*c,b*c),(0,b*c),t)
        tip=plus(tip,(-dx*c,dy*c))
        previous,depth=r,next_depth
        x+=r
    assert x==y==c and tip==(0,V[1]-final*a*c*c)


def ccw(t):
    a,b,c=t
    d=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    assert d
    return t if d>0 else (a,c,b)


def inside(t):
    return all(x>=0 and y>=0 and x*V[1]+y*H[0]<=H[0]*V[1] for x,y in t)


def incidences(tri):
    for p,q in zip(tri,tri[1:]+tri[:1]):
        x,y=q[0]-p[0],q[1]-p[1]
        g=gcd(x,y)
        if x<0 or (x==0 and y<0):
            g=-g
        key=(x//g,y//g)
        yield (key,p),1
        yield (key,q),-1


def contradiction(tiles):
    rows=defaultdict(list)
    terms=[]
    rhs=defaultdict(int,dict(incidences(TARGET)))
    for i,tri in enumerate(tiles):
        row=list(incidences(tri))
        terms.append(row)
        for k,d in row:
            rows[k].append((i,d))
    state=[None]*len(tiles)
    hi={k:sum(d>0 for _,d in v) for k,v in rows.items()}
    lo={k:-sum(d<0 for _,d in v) for k,v in rows.items()}
    queue=deque(rows.keys() | rhs.keys())
    while queue:
        k=queue.popleft()
        bottom,top=lo.get(k,0),hi.get(k,0)
        demand=rhs[k]
        if not bottom<=demand<=top:
            return True
        if bottom==top or demand not in (bottom,top):
            continue
        at_top=demand==top
        for i,d in rows[k]:
            if state[i] is not None:
                continue
            keep=at_top==(d>0)
            state[i]=keep
            for key,sign in terms[i]:
                hi[key]-=int(sign>0)
                lo[key]+=int(sign<0)
                rhs[key]-=int(keep)*sign
                queue.append(key)
    return False


def cases():
    a,b,c=A,B,C
    inv=pow(a,-1,c)
    for m in range(1,5):
        for rises in product(range(1,5),repeat=m):
            if sum(rises)!=4:
                continue
            for middle in product(range(7),repeat=m-1):
                levels=(1,)+middle+(1,)
                runs=[(b*(levels[j+1]-levels[j])+b*inv*s)%c for j,s in enumerate(rises)]
                if sum(runs)==30:
                    yield (list(zip(runs,rises,levels[1:])),1,1)
    for initial,final,smin,smax,ds,depths,rmin,rmax,buckets in [
        (1,1,-7,11,1,range(6),-21,51,(-1,0,1)),
        *[(i,f,-2,c-f*a+2,1 if f else 3,range(4),-12,c-i*b+12,(-1,0))
          for i,f in ((2,1),(0,1),(3,1),(1,0),(2,0),(0,0))]]:
        for level in depths:
            for s in range(smin,smax+1,ds):
                base=(b*(level-initial)+b*inv*s)%c
                for offset in buckets:
                    r=base+c*offset
                    if rmin<=r<=rmax:
                        yield ([(r,s,level),(c-initial*b-r,c-final*a-s,final)],initial,final)
    for middle in ((1,1),(1,2),(2,1),(1,0),(0,1)):
        levels=(1,)+middle+(1,)
        for s,t in product(range(-4,9),repeat=2):
            rises=(s,t,4-s-t)
            if min(rises)<-4 or max(rises)>8 or min(rises)>=1:
                continue
            options=[range((b*(levels[j+1]-levels[j])+b*inv*s+12)%c-12,46,c)
                     for j,s in enumerate(rises)]
            for runs in product(*options):
                if sum(runs)==30 and all(r or s or levels[j]!=levels[j+1] for j,(r,s) in enumerate(zip(runs,rises))):
                    yield (list(zip(runs,rises,levels[1:])),1,1)


def test(record):
    raw=generate(*record)
    tiles=[ccw(t) for t in {tuple(sorted(t)) for t in raw if inside(t)}]
    return contradiction(tiles)


if __name__=="__main__":
    assert not contradiction([TARGET]) and contradiction([])
    rows=list(cases())
    assert len(rows)==1512
    workers=int(argv[1]) if len(argv)>1 else 1
    with ProcessPoolExecutor(max_workers=workers) as executor:
        outcomes=list(executor.map(test,rows,chunksize=8))
    print("Records:",len(rows),"rejected by endpoint equations:",sum(outcomes))
    print("Survivors:",[i for i,eliminated in enumerate(outcomes) if not eliminated])
