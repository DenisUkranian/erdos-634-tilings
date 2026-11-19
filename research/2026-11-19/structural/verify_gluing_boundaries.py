"""Independent integer replay of the two-size shifted-line gluing, including holes.

No tiling solver or source data. Convex m-grid cores are counted by exact area.
Each complementary elementary n-triangle is enumerated by positive winding number.
Its actual boundary is compared to the recomputed boundary deficit.
"""
from collections import Counter, defaultdict
from math import gcd
import argparse
import json


def cycle(poly):
    return zip(poly,poly[1:]+poly[:1])


def area2(poly):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in cycle(poly))


def line(a,b):
    if a[0]==b[0]:return 'x',a[0]
    if a[1]==b[1]:return 'y',a[1]
    assert a[0]+a[1]==b[0]+b[1]
    return 'z',a[0]+a[1]


def on(ln,t):
    d,i=ln
    if d=='x':return i,t
    if d=='y':return t,i
    return t,i-t


def cuts(poly,weight,ends):
    for a,b in cycle(poly):
        ln=line(a,b);axis=int(ln[0]=='x')
        ends[ln][a[axis]]+=weight
        ends[ln][b[axis]]-=weight


def inc_edge(edges,a,b):
    key=(a,b) if a<b else (b,a)
    edges[key]+=1 if a<b else -1
    if not edges[key]:del edges[key]


def cells(m):
    faces=[]
    for i in range(m):
        for j in range(m-i):
            faces.append(((i,j),(i+1,j),(i,j+1)))
            if i+j+1<m:faces.append(((i+1,j+1),(i,j+1),(i+1,j)))
    return faces


def core(face, H, m, n, K):
    # Only the outermost row of coarse vertices carries a nonzero potential.
    # Compute the final levels directly, without sharing the other verifier's code.
    levels = {}
    for a,b in cycle(face):
        direction, index = line(a,b)
        i,j = min(a,b)
        if direction == 'z':
            residue = K if index == m else 0
        elif i+j == m-1:
            residue = K*(i+1) if direction == 'y' else -K*i
        else:
            residue = 0
        old = index*H
        levels[direction] = next(old+n*t for t in range(m) if (old+n*t-residue) % m == 0)
    x,y,z = map(levels.get, 'xyz')
    s = abs(z-x-y)
    v = ((x,y),(z-y,y),(x,z-x))
    R = 5*m*n
    assert s>2*R and s%m==0
    poly=[]
    for i,a in enumerate(v):
        for b in (v[i-1],v[(i+1)%3]):
            poly.append(tuple(c+R*(d-c)//s for c,d in zip(a,b)))
    assert all((a[0]-x)%m==0 and (a[1]-y)%m==0 for a in poly)
    assert area2(poly)==s*s-3*R*R>0
    return tuple(poly)


def patch(pieces):
    """Recover the exact local 0/1 area chain from its boundary in n units."""
    xs=[a[0] for a,b in pieces]+[b[0] for a,b in pieces]
    ys=[a[1] for a,b in pieces]+[b[1] for a,b in pieces]
    actual=Counter();count=0
    for j in range(min(ys),max(ys)):
        for layer in (1,2):
            Y=3*j+layer
            active=[]
            for (x1,y1),(x2,y2) in pieces:
                if min(3*y1,3*y2)<Y<max(3*y1,3*y2):
                    active.append((x1,y1,x2,y2))
            for i in range(min(xs),max(xs)):
                X=3*i+layer
                w=0
                for x1,y1,x2,y2 in active:
                    sgn=(x2-x1)*(Y-3*y1)-(y2-y1)*(X-3*x1)
                    if y2>y1 and sgn>0:w+=1
                    if y2<y1 and sgn<0:w-=1
                assert w in (0,1)
                if not w:continue
                count+=1
                if layer==1:t=((i,j),(i+1,j),(i,j+1))
                else:t=((i+1,j+1),(i,j+1),(i+1,j))
                for a,b in cycle(t):inc_edge(actual,a,b)
    target=Counter()
    for a,b in pieces:
        dx,dy=b[0]-a[0],b[1]-a[1];s=gcd(dx,dy)
        for k in range(s):
            inc_edge(target,(a[0]+k*dx//s,a[1]+k*dy//s),
                     (a[0]+(k+1)*dx//s,a[1]+(k+1)*dy//s))
    assert actual==target
    return count


def audit(m,n,K):
    assert m >= 2 and n >= 2 and gcd(m,n)==1 and K >= 20*m*m*n
    H = K//m
    while (K-m*H) % n:
        H -= 1
    f = cells(m)
    ends = defaultdict(Counter)
    cuts(((0,0),(K,0),(0,K)),1,ends)
    cores=0
    for tri in f:
        c=core(tri,H,m,n,K)
        assert area2(c)%(m*m)==0
        cores+=area2(c)//(m*m)
        cuts(c,-1,ends)
    local=defaultdict(list)
    for ln,changes in ends.items():
        weight=0;last=None
        for t,delta in sorted(changes.items()):
            if weight:
                assert abs(weight)==1
                a,b=on(ln,last),on(ln,t)
                if weight<0:a,b=b,a
                ia,ja=[(c+H//2)//H for c in a]
                ox,oy=ia*H,ja*H
                points=[]
                for x,y in (a,b):
                    x-=ox;y-=oy
                    assert max(abs(x),abs(y),abs(x+y))<=9*m*n
                    assert x%n==y%n==0
                    points.append((x//n,y//n))
                local[ia,ja].append(tuple(points))
            weight+=delta;last=t
        assert weight==0
    extra=sum(patch(segments) for segments in local.values())
    assert cores*m*m+extra*n*n==K*K
    return {'m':m,'n':n,'K':K,'m_tiles':cores,'n_tiles':extra,'vertex_patches':len(local),
            'exact_edge_cancellation':True}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', nargs='*', type=int, help='Optional m n K for a single board.')
    args = parser.parse_args()
    if args.case and len(args.case) != 3:
        parser.error('Supply m n K, or omit all three to run the reference examples.')
    if args.case:
        cases = [args.case]
    else:
        cases = [(2,3,240+j) for j in range(6)]
        cases += [(3,2,361), (3,4,727), (4,3,971), (5,2,1003),
                  (5,7,3534), (6,5,3619), (7,3,2953)]
    print(json.dumps([audit(m,n,k) for m,n,k in cases], indent=2))
