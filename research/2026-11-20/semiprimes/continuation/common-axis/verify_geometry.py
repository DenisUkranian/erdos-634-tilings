"""Exact corner search for a common edge direction away from one exterior side."""
from collections import defaultdict
from functools import cache
from itertools import product
from math import gcd, isqrt


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def add(p, q):
    return p[0]+q[0], p[1]+q[1]


def neg(p):
    return -p[0], -p[1]


def mul(p, q):
    x, y = p
    u, v = q
    return x*u-y*v, x*v+y*u+y*v


def scale(n, p):
    return n*p[0], n*p[1]


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


@cache
def direction(p):
    d=gcd(*p)
    return p[0]//d, p[1]//d


def segments(P):
    return tuple(zip(P, P[1:] + P[:1]))


def update(rim, tri):
    for q,p in segments(tri):
        d=sub(q,p)
        events=defaultdict(int); events[p]+=1;events[q]-=1
        new=[]
        for x,y in rim:
            if det(d,sub(x,p)) or det(d,sub(y,p)):
                new.append((x,y))
            else:
                events[x]+=1;events[y]-=1
        n=0;last=None
        for x,k in sorted(events.items()):
            if not k:continue
            if n==1:new.append((last,x))
            if n==-1:new.append((x,last))
            n+=k
            assert abs(n)<=1
            last=x
        assert n==0
        rim=new
    return rim


def decide(a,b,c,es,j,h,corner=None,radius=50):
    board_heights=(0,2,0)
    outer_levels=board_heights if es is None else (board_heights[es],)
    low,high=min(h,*outer_levels)-1,max(h,*outer_levels)+1
    den=c**max(1,-low,high)
    def axis(r,k):
        v=(1,0)
        for _ in range(abs(k)): v=mul(v,(a,b) if k>=0 else (a+b,-b))
        for _ in range(r%6): v=mul(v,(0,1))
        return scale(den//(c**abs(k)),v)
    common=axis(j,h)
    boundary=((0,0),(den*b*(2*a+b),0),(0,den*a*(a+2*b)))
    walls=segments(boundary)
    exception_walls=walls if es is None else (walls[es],)
    def sector(t):
        return any(not det(common,sub(v,u)) for u,v in segments(t))
    def exempt(t,placed):
        return any(not det(sub(e,o),sub(v,u)) and (not placed or not det(sub(e,o),sub(u,o))) for u,v in segments(t) for o,e in exception_walls)
    templates=defaultdict(list);D=defaultdict(set)
    @cache
    def length(d):
        u,v=d
        sq=u*u+u*v+v*v;r=isqrt(sq)
        return r//den if r*r==sq and r%den==0 else -1
    for k,r,sign in product(range(low,high+1),range(6),(-1,1)):
        p, q=scale(a,axis(r,k)),scale(b,axis(r+2*sign,k))
        if det(p,q)<0:p,q=q,p
        v=((0,0),p,q)
        if not sector(v) and not exempt(v,False):continue
        for i in range(3):
            u=v[i];p=sub(v[(i+1)%3],u);q=sub(v[(i+2)%3],u)
            ray=direction(p);D[ray].add(length(p));templates[ray].append((p,q,sector(v)))
    maxlen=max(length(sub(v,u)) for u,v in walls)
    @cache
    def coins(ray):
        lengths=D[ray] if corner is None else (a,b,c)
        ok=[True]+[False]*maxlen
        for t in range(1,maxlen+1):ok[t]=any(t>=s and ok[t-s] for s in lengths)
        return ok
    def coin(ray,d):
        n=length(d)
        return 0<=n<=maxlen and coins(ray)[n]
    def separated(P,Q):
        return any(all(det(sub(v,u),sub(x,u))<=0 for x in Q) for u,v in segments(P))
    def inside(x,p,q):
        return min(p,q)<x<max(p,q) and not det(sub(x,p),sub(q,p))
    def near(p):
        x,y=sub(p,boundary[corner])
        return x*x+x*y+y*y<=radius*radius*den*den
    count=0
    def rec(rim,placed):
        nonlocal count
        count+=1
        if not rim:return True
        out=defaultdict(list);inc=defaultdict(list)
        for p,q in rim:
            out[p].append(sub(q,p));inc[q].append(sub(q,p))
        pivots={p for p in out if len(out[p])==len(inc[p])==1 and det(inc[p][0],out[p][0])>0 and not any(inside(p,x,y) for x,y in rim)}
        assert pivots,'singular frontier left undecided'
        banks=[]
        for p,q in rim:
            d=sub(q,p);ray=direction(d);border=any(not det(sub(y,x),d) and not det(sub(y,x),sub(p,x)) for x,y in walls)
            left=border or p in pivots;right=border or q in pivots
            if left or right:banks.append((p,q,ray,left,right))
            if left and right and not coin(ray,d):return False
        def good(t):
            for p,q in walls:
                if any(det(sub(q,p),sub(r,p))<0 for r in t):return False
            for p,q,ray,left,right in banks:
                for r in t:
                    if inside(r,p,q) and ((left and not coin(ray,sub(r,p))) or (right and not coin(ray,sub(q,r)))):return False
            return all(separated(t,v) or separated(v,t) for v in placed)
        best=None
        for p in sorted(pivots):
            if corner is not None and not near(p):continue
            begin=direction(out[p][0]);end=direction(neg(inc[p][0]));options=[]
            def fans(now,fan):
                if best is not None and len(options)>=len(best):return
                if now==end:options.append(fan);return
                for e,f,common_ok in templates[now]:
                    nxt=direction(f)
                    if det(begin,nxt)<=0 or det(nxt,end)<0 or (det(nxt,end)==0 and nxt!=end):continue
                    t=(p,add(p,e),add(p,f))
                    if (common_ok or exempt(t,True)) and good(t):fans(nxt,fan+(t,))
            fans(begin,())
            if not options:return False
            if best is None or len(options)<len(best):best=options
        if best is None:return True
        for fan in best:
            r=rim
            for tri in fan:r=update(r,tri)
            if rec(r,placed+fan):return True
        return False
    result=rec(walls,())
    return result,count


if __name__=='__main__':
    allowed={(0,0),(1,0),(2,0),(0,1),(0,-1),(1,-1),(2,1)}
    outer=((0,0),(1,2),(1,0))
    choices=[{((j+dj)%3,h+dh) for dj,dh in allowed} for j,h in outer]
    for a,b,c in ((33,7,37),(35,13,43)):
        for es in range(3):
            for j,h in sorted(choices[(es+1)%3]&choices[(es+2)%3]-choices[es]):
                result,nodes=decide(a,b,c,es,j,h)
                print((a,b,c),es,j,h,result,nodes,flush=True)
                assert not result

        for h,j in product(range(-2,5),range(3)):
            if (j,h)==(1,1):continue
            result,nodes=decide(a,b,c,None,j,h)
            print((a,b,c),"all sides",j,h,result,nodes,flush=True)
            assert not result

        for corner in (0,1):
            result,nodes=decide(a,b,c,0,1,1,corner=corner)
            print((a,b,c),"local corner",corner,"radius",50,result,nodes,flush=True)
            assert not result
