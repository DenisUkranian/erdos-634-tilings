"""Necessary integer interval-start and orientation counts for paired polygons."""
from collections import Counter
from itertools import groupby


def interval_matching(profile, a, b):
    """Split a nonnegative coverage into paths with forward steps a or b."""
    starts, ends = [], []
    for i, (prev, now) in enumerate(zip([0]+profile, profile+[0])):
        starts.extend([i]*max(0,now-prev))
        ends.extend([i]*max(0,prev-now))
    reach = {a*i+b*j for i in range(len(profile)//a+1)
             for j in range((len(profile)-a*i)//b+1)}
    mates = {}
    def augment(i,seen):
        for j, y in enumerate(ends):
            if j in seen or y-starts[i] not in reach:
                continue
            seen.add(j)
            if j not in mates or augment(mates[j],seen):
                mates[j] = i
                return True
        return False
    return all(augment(i,set()) for i in range(len(starts)))


def axis_options(J,a,b):
    if not J:
        return 0,0,{0}
    starts_a,starts_b = {},{}
    remaining=[]
    volume=width=0
    for t in range(min(J),max(J)+max(a,b)+1):
        width+=J[t]
        volume+=width
        starts_a[t]=(starts_a.get(t-b,0)+pow(a,-1,b)*J[t])%b
        starts_b[t]=(starts_b.get(t-a,0)+pow(b,-1,a)*J[t])%a
        extra=width-a*sum(starts_a.get(t-i,0) for i in range(b))
        extra-=b*sum(starts_b.get(t-i,0) for i in range(a))
        if extra<0 or extra%(a*b):
            return None
        remaining.append(extra//(a*b))
    if width or volume%(a*b):
        return None
    choices={sum(starts_a.values())}
    for positive,part in groupby(remaining,key=bool):
        run=list(part)
        if positive:
            if not interval_matching(run,a,b):
                return None
            size=sum(run)
            extras={b*i for i in range(size//b+1) if (size-b*i)%a==0}
            choices={x+y for x in choices for y in extras}
    return volume//(a*b),sum(starts_b.values()),choices


def passes(jumps,a,b):
    results=[axis_options(axis,a,b) for axis in jumps]
    if any(row is None for row in results):
        return False
    twice=sum(row[0] for row in results)
    if twice%2 or any(2*row[0]>twice for row in results):
        return False
    totals={0}
    for _,_,choices in results:
        totals={x+y for x in totals for y in choices}
    return twice//2 in totals


def path_jumps(a,b,c,word):
    jumps=[Counter() for _ in range(3)]
    p=(0,0)
    def move(i,n):
        nonlocal p
        x,y=p
        if i==0:
            jumps[i][y]+=n
            p=x+n,y
        elif i==1:
            jumps[i][-x]+=n
            p=x,y+n
        else:
            jumps[i][-x-y]+=n
            p=x-n,y+n
    steps=[[(0,a),(2,-b)],[(2,-a),(1,-b)],[(1,-a),(0,-b)],[(2,-c)],[(1,-c)]]
    for ch in word:
        for i,n in steps[int(ch)]:
            move(i,n)
    for _ in range(c):
        move(2,b)
        move(1,a)
    assert p==(0,0)
    return jumps


def control(which):
    from verify import geom
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,which)
    polys,centres,origin,*_=geom.check_full_tiling(g,tiles)
    _,pairs=geom.long_pairs(g,tiles,polys,centres,origin)
    from collections import defaultdict
    classes=defaultdict(lambda:[Counter() for _ in range(3)])
    for i,j in pairs:
        h=tiles[i][1]
        for idx in (0,1):
            p,q=polys[i][idx:idx+2]
            delta=geom.sub(q,p)
            axis=next(k for k in range(3) if geom.det(geom.point(g,g.unit(h,k)),delta)==0)
            u=geom.point(g,g.unit(h,axis))
            length=abs(delta[0]/u[0] if u[0] else delta[1]/u[1])
            levels=[geom.det(u,x) for x in polys[i]+polys[j]]
            lo,hi=min(levels),max(levels)
            # Normalize one Euclidean translate before pooling its pair counts.
            point=g.mult(g.unit(-h,0),tiles[i][0])
            x,y=geom.point(g,point)
            rx,ry=x%1,y%1
            offset=(ry,-rx,-rx-ry)[axis]
            assert (lo-offset).denominator==(hi-offset).denominator==1
            counts=classes[h,rx,ry][axis]
            counts[int(lo-offset)]+=int(length)
            counts[int(hi-offset)]-=int(length)
    assert all(passes(jumps,g.a,g.b) for jumps in classes.values())
    return len(pairs)
