"""Independent integer-coordinate grid verifier; imports no constructor."""
from itertools import combinations
from fractions import Fraction
from pathlib import Path
import json,sys


def sub(a,b): return a[0]-b[0],a[1]-b[1]
def cr(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return a[0]**2+a[0]*a[1]+a[1]**2
def ar(P): return sum(cr(p,q) for p,q in zip(P,P[1:]+P[:1]))
def side(p,q,z): return cr(sub(q,p),sub(z,p))
def positive(P): return P if ar(P)>0 else P[::-1]
def separated(A,B):
    return any(all(side(p,q,z)<=0 for z in B) for p,q in zip(A,A[1:]+A[:1]))


def check(data):
    a,b,c=data['tile'];den=data['coordinate_denominator'];target=positive(data['target'])
    assert den>0 and a*a+a*b+b*b==c*c
    assert len(target)==3 and ar(target)>0
    def sides(P): return sorted(norm(sub(p,q)) for p,q in zip(P,P[1:]+P[:1]))
    assert sides(target)==sorted((den*x)**2 for x in [c*c,a*(a+2*b),b*(2*a+b)])
    metrics=sorted((den*x)**2 for x in [a,b,c])
    regions=[];num=0;area=0
    for block in data['blocks']:
        pts=block['points'];P=positive(pts)
        assert ar(P)>0 and all(side(P[i-1],P[i],P[(i+1)%len(P)])>0 for i in range(len(P)))
        assert all(side(p,q,z)>=0 for p,q in zip(target,target[1:]+target[:1]) for z in P)
        if block['kind']=='triangle':
            n=block['scale'];assert type(n) is int and n>0 and len(pts)==3
            assert sides(pts)==[n*n*x for x in metrics];count=n*n
        else:
            assert block['kind']=='parallelogram' and len(pts)==4
            rows,cols=block['rows'],block['cols']
            assert type(rows) is int and type(cols) is int and min(rows,cols)>0
            p,q,r,z=pts;assert sub(q,p)==sub(r,z)
            a1=tuple(Fraction(x,rows) for x in sub(q,p))
            b1=tuple(Fraction(x,cols) for x in sub(z,p))
            d=block['diagonal'];assert d in ('sum','difference')
            sign=1 if d=='sum' else -1
            c1=tuple(x+sign*y for x,y in zip(a1,b1))
            assert sorted(map(norm,(a1,b1,c1)))==metrics;count=2*rows*cols
        assert ar(P)==count*den*den*a*b
        regions.append(P);num+=count;area+=ar(P)
    assert area==ar(target) and num==data['count']==(2*a+b)*(2*b+a)
    for i,j in combinations(range(len(regions)),2):
        assert separated(regions[i],regions[j]) or separated(regions[j],regions[i]),(i,j)
    return dict(count=num,regions=len(regions),pairs=len(regions)*(len(regions)-1)//2)

if __name__=='__main__':
    paths=map(Path,sys.argv[1:]) if sys.argv[1:] else sorted(Path(__file__).parent.glob('certificate_*.json'))
    for path in paths: print(path.name,check(json.loads(path.read_text())))
