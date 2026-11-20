"""Check both phase multiplicities on the two tiled scale-two control boards (prime c)."""
from collections import Counter
from fractions import Fraction as F
from itertools import pairwise
from pathlib import Path
import sys,json


def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def scale(k,p):return (k*p[0],k*p[1])
def prod(p,q): return (p[0]*q[0]-p[1]*q[1],p[0]*q[1]+p[1]*q[0]+p[1]*q[1])
def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2
def divide(p,k):
    assert p[0]%k==0 and p[1]%k==0
    return (p[0]//k,p[1]//k)


def expand(block):
    points=block['points']; o,q=points[:2]
    if block['kind']=='triangle':
        k=block['scale']; u=divide(sub(q,o),k);v=divide(sub(points[2],o),k)
        for i in range(k):
            for j in range(k-i):
                t=add(o,add(scale(i,u),scale(j,v)))
                yield t,add(t,u),add(t,v)
                if i+j+1<k:yield add(t,u),add(add(t,u),v),add(t,v)
    else:
        r,s=block['rows'],block['cols']
        u=divide(sub(q,o),r);v=divide(sub(points[-1],o),s)
        for i in range(r):
            for j in range(s):
                t=add(o,add(scale(i,u),scale(j,v)));x=add(t,u);y=add(t,v);w=add(x,v)
                if block['diagonal']=='difference':
                    yield t,x,y
                    yield w,x,y
                else:
                    yield t,x,w
                    yield t,y,w


def check(path):
    d=json.loads(path.read_text());a,b,c=d['tile']
    assert d['coordinate_denominator']==c and all(c%i for i in range(2,int(c**.5)+1))
    roots=[(-a*pow(b,-1,c))%c,((a+b)*pow(b,-1,c))%c]
    dirs={};z=(F(a,c),F(b,c));zb=(F(a+b,c),F(-b,c))
    for h in range(-6,7):
        t=(1,0)
        for _ in range(abs(h)):t=prod(t,z if h>=0 else zb)
        for _ in range(6):
            dirs[scale(a*c,t)]=h
            t=prod(t,(0,1))
    counts=[Counter(),Counter()]
    for block in d['blocks']:
        for t in expand(block):
            side=next(sub(q,p) for p,q in pairwise((*t,t[0])) if norm(sub(q,p))==(a*c)**2)
            h=dirs[side];x,y=t[0]
            for ix,root in enumerate(roots):
                power=(h if ix==0 else -h)+1
                val=root;mod=c
                for _ in range(1,power):
                    lift=-((val*val-val+1)//mod)*pow(2*val-1,-1,c)
                    val+=mod*(lift%c);mod*=c
                remainder=(x+y*val)%mod if power>0 else 0
                counts[ix][h,remainder]+=1
    for ix,co in enumerate(counts):
        assert sum(co.values())==d['count']
        for (h,r),n in co.items():
            if h==0 and r==0:assert n%c==d['count']%c
            else:assert n%c==0 and n>=2*c
        print(path.name,'forward' if ix==0 else 'reverse',sorted(co.items()))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    base=Path(__file__).resolve().parent.parent.parent/'controls'
    files=[Path(x) for x in sys.argv[1:]] or [base/'double_3431.json',base/'double_5063.json']
    for name in files:check(name)
