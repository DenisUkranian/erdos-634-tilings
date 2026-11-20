"""Directed long-edge path for tilings supported on the two middle heights."""
from collections import deque
from math import gcd
import sys
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def mul(p,q):return(p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def tb(n,p):return n*p[0],n*p[1]
def cr(p,q):return p[0]*q[1]-p[1]*q[0]
def positive(p):return p if cr(sub(p[1],p[0]),sub(p[2],p[0]))>0 else p[::-1]
def disjoint(P,Q):return any(all(cr(sub(t,s),sub(x,s))<=0 for x in Y) for X,Y in ((P,Q),(Q,P)) for s,t in zip(X,X[1:]+X[:1]))
def graph(a,b,c):
    c2=c*c;B=tb(c,(a+b,-b));base=(a+b,-b)
    def inside(p):
        x,y=p
        return (a+b)*y+b*x>=0 and b*x-a*y>=0 and (a+b)*x+b*y<=c2*a*(a+2*b)
    base_tiles=[tuple(tb(c,add(tb(i,base),s)) for s in ((0,0),base,(a,0))) for i in range(c)]
    base_tiles=[positive(t) for t in base_tiles]
    r=(1,0); motions=[]
    for j in range(6):
        for step,apex,label in [((c,0),(a*a,a*b),1),((a,b),(a*c,0),2)]:
            v=mul(r,step); t=positive([(0,0),tb(c,v),mul(r,apex)])
            motions.append((v,t,(j,label)))
        r=mul(r,(0,1))
    visited={(0,0):None};queue=deque([(0,0)]); edges=0
    while queue:
        P=queue.popleft()
        for v,tri,label in motions:
            Q=add(P,v)
            if Q in visited:continue
            T=[add(tb(c,P),x) for x in tri]
            if not all(inside(x) for x in T):continue
            # Only test base teeth with overlapping x ranges.
            xs=[x for x,y in T];sw=c*(a+b)
            lo=max(0,min(xs)//sw);hi=min(c,max(xs)//sw+1)
            if any(not disjoint(T,base_tiles[i]) for i in range(lo,hi)):continue
            visited[Q]=P,label;queue.append(Q)
    path=[];cur=B
    if B in visited:
        while visited[cur]:
            prev,label=visited[cur];path.append(label);cur=prev
    return len(visited),path[::-1]
if __name__=='__main__':
    for a,b,c in [(5,3,7),(33,7,37),(35,13,43)]:
        n,p=graph(a,b,c)
        print(a,b,c,n,len(p),p,flush=True)
