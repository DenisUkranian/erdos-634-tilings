"""Independent exact verification of a positive triangular-grid certificate."""
from collections import defaultdict, Counter
from pathlib import Path
from math import gcd,isqrt
import json,sys

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def mul(k,p): return (k*p[0],k*p[1])
def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2

def read_certificate(path):
    lines=Path(path).read_text().splitlines();head=lines[0].split();assert head[0]=='YES'
    N,D,count=map(int,head[1:]); assert len(lines)==count+1
    result=[]
    for line in lines[1:]:
        values=line.split();kind=values[0];m,n,area,k=map(int,values[1:5]);coords=list(map(int,values[5:]));assert len(coords)==2*k
        result.append(dict(kind=kind,m=abs(m),n=n,area=area,points=list(zip(coords[::2],coords[1::2]))))
    return N,D,result

def check(path,a,b,c):
    N,D,blocks=read_certificate(path);assert N==(a+2*b)*(2*a+b);assert c*c==a*a+a*b+b*b
    triangles=[]; macro_area=0
    for block in blocks:
        ps=block['points'];m=block['m'];n=block['n'];assert m>0
        ar=sum(det(p,q)for p,q in zip(ps,ps[1:]+ps[:1]));assert ar>0
        assert ar==block['area']*a*b*D*D;macro_area+=block['area']
        if block['kind']=='T':
            assert len(ps)==3 and block['area']==m*m
            vec=[sub(p,ps[0])for p in ps[1:]]; assert all(z%m==0 for v in vec for z in v)
            u,v=[tuple(z//m for z in w)for w in vec]
            assert sorted(map(norm,[u,v,sub(v,u)]))==sorted((D*k)**2 for k in (a,b,c))
            for i in range(m):
                for j in range(m-i):
                    o=add(ps[0],add(mul(i,u),mul(j,v)))
                    triangles.append((o,add(o,u),add(o,v)))
                    if i+j<m-1:triangles.append((add(o,u),add(add(o,u),v),add(o,v)))
        else:
            assert block['kind']=='P' and len(ps)==4 and n>0 and block['area']==2*m*n
            U,V=sub(ps[1],ps[0]),sub(ps[3],ps[0]);assert all(x%m==0 for x in U)and all(x%n==0 for x in V)
            assert ps[2]==add(ps[0],add(U,V))
            u,v=tuple(x//m for x in U),tuple(x//n for x in V)
            good=lambda w:sorted(map(norm,[u,v,w]))==sorted((D*k)**2 for k in(a,b,c))
            dif=good(sub(v,u));summ=good(add(u,v));assert dif or summ
            for i in range(m):
                for j in range(n):
                    o=add(ps[0],add(mul(i,u),mul(j,v)));p=add(o,u);q=add(o,v);r=add(p,v)
                    triangles.extend(((o,p,q),(p,r,q)) if dif else ((o,p,r),(o,r,q)))
    assert macro_area==N and len(triangles)==N
    # Normalize each tile counterclockwise, check all three squared lengths.
    out=[]
    for t in triangles:
        if det(sub(t[1],t[0]),sub(t[2],t[0]))<0:t=(t[0],t[2],t[1])
        assert det(sub(t[1],t[0]),sub(t[2],t[0]))==D*D*a*b
        assert sorted(norm(sub(t[i],t[(i+1)%3]))for i in range(3))==sorted((D*k)**2 for k in(a,b,c))
        out.append(t)
    # Equality of oriented chains proves one-fold coverage, since every tile is CCW.
    board=((0,0),(D*b*(2*a+b),0),(0,D*a*(a+2*b)))
    events=defaultdict(Counter)
    for poly,sign in [(t,1) for t in out]+[(board,-1)]:
        for p,q in zip(poly,poly[1:]+poly[:1]):
            d=sub(q,p);g=gcd(*d);u=(d[0]//g,d[1]//g)
            if u<(0,0):u=mul(-1,u)
            key=(u,det(u,p));events[key][p]+=sign;events[key][q]-=sign
    assert all(not any(v.values())for v in events.values())
    print(f'PASS {Path(path).name}: {N} exact unit tiles in {len(blocks)} grid blocks; boundary chains cancel.')
    result=dict(tile=[a,b,c],count=N,denominator=D,triangles=out,blocks=blocks)
    return result

if __name__=='__main__':
    p=sys.argv[1];a,b,c=map(int,sys.argv[2:5]);data=check(p,a,b,c)
    if len(sys.argv)>5:Path(sys.argv[5]).write_text(json.dumps(data,separators=(',',':'))+'\n')
