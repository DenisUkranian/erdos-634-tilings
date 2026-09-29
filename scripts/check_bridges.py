from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json
if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")


def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def scale(a,s): return (a[0]*s,a[1]*s)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def normal(t): return t if cross(*t)>0 else (t[0],t[2],t[1])
def dist2(a,b,co):
    x,y=a[0]-b[0],a[1]-b[1]
    return x*x+y*y+2*co*x*y
def separated(t,u):
    for x,y in ((t,u),(u,t)):
        for i in range(3):
            if all(cross(x[i],x[(i+1)%3],p)<=0 for p in y): return True
    return False

def elementary(e,f,p,q):
    assert gcd(e,f)==1 and 0<e<f and q%e==0 and q<=2*p
    a,b,c=e*f,f*f-e*e,f*f
    N=3*f*f-e*e
    H,J=q*f,2*p*f
    s=p*e*b
    tiles=[]
    def cell(i,j,offset,D,U):
        x,y=offset+i*a,j*c
        if D: tiles.append(((F(x),F(y)),(F(x+a),F(y)),(F(x),F(y+c))))
        if U: tiles.append(((F(x+a),F(y)),(F(x+a),F(y+c)),(F(x),F(y+c))))
    for i in range(H):
        for j in range(H): cell(i,j,0,i+j<=H-1,i+j<=H-2)
    for i in range(J):
        for j in range(H): cell(i,j,s,i+j>=H,i+j>=H-1)
    # c-glued two-tile bricks in the diagonal strip
    U=(F(b),F(0))
    V=(F(-a*a,b),F(a*c,b))
    origin=(F(H*a),F(0))
    for i in range(p*e):
        for j in range(q*b//e):
            o=plus(origin,plus(scale(U,i),scale(V,j)))
            ou,ov=plus(o,U),plus(o,V)
            uv=plus(ou,V)
            tiles.extend(((o,ou,uv),(o,uv,ov)))
    return [normal(t) for t in tiles],p*e*N,q*f**3

def build(e,f,p,q):
    assert q%e==0 and p>=(e+1)//2
    base,W,h=elementary(e,f,p,e)
    tiles=[]
    for j in range(q//e):
        tiles.extend(tuple(plus(v,(F(0),F(j*h))) for v in t) for t in base)
    return tiles,W,q*f**3

def verify(e,f,p,q):
    a,b,c=e*f,f*f-e*e,f*f
    N=3*f*f-e*e
    co=F(a*a+c*c-b*b,2*a*c)
    tiles,W,H=build(e,f,p,q)
    assert len(tiles)==2*p*q*N
    area=F(0)
    for t in tiles:
        assert sorted(dist2(t[i],t[(i+1)%3],co) for i in range(3))==sorted([a*a,b*b,c*c])
        assert all(0<=x<=W and 0<=y<=H for x,y in t)
        area+=cross(*t)
    assert area==2*W*H
    boxes=[(min(x for x,y in t),max(x for x,y in t),min(y for x,y in t),max(y for x,y in t)) for t in tiles]
    tested=0
    for i,t in enumerate(tiles):
        for j in range(i):
            u=tiles[j]
            A,B=boxes[i],boxes[j]
            if A[1]<=B[0] or B[1]<=A[0] or A[3]<=B[2] or B[3]<=A[2]: continue
            tested+=1
            assert separated(t,u),(e,f,p,q,i,j)
    return dict(e=e,f=f,p=p,q=q,tiles=len(tiles),nontrivial_exact_separation_checks=tested,status='PASS')

if __name__=='__main__':
    cases=[(1,2,1,1),(1,3,1,1),(2,3,1,2),(2,5,1,2),(3,4,2,3),(2,3,1,6)]
    results=[]
    for args in cases:
        r=verify(*args)
        results.append(r)
        print(json.dumps(r),flush=True)
