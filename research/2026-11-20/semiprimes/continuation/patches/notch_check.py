"""Exact verification of the oversize-band macrodissections."""
from fractions import Fraction
from itertools import combinations
from math import gcd
from pathlib import Path
import sys

# Reuse the independent verifier from the published semiprime package.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from notchshape import make
from controls.verify_grids import ar, positive, separated, side, sub, norm

def unit_board(a,b,c,copies,extend=0,cap=0):
    """Identical loads. Each positive notch has the same size and metric."""
    assert copies>0 and all(z%copies==0 for z in (c-b,c-a,a-b))
    r,s=(c-b)//copies,(c-a)//copies
    return make(a,b,c,1,1,[(r,s,1)]*copies,extend,cap)


def doubled_board(u):
    assert u>=10 and u%3==1
    a,b,c=(u*u-1)//3,(2*u+1)//3,(u*u+u+1)//3
    high=(u-7)//3
    moves=[]
    for i in range(u+4):
        m=4 if i<high else 1
        r=(1+(u+1)*m)//3-(b if i==high-1 else 0)
        moves.append((r,(u-m)//3,2 if i<high-1 else 1))
    return make(a,b,c,2,2,moves)


def verify(data):
    a,b,c=data['tile']; den=data['coordinate_denominator']
    unit=sorted((den*s)**2 for s in (a,b,c))
    T=positive(data['target']);regs=[];count=0;holes=[]
    h=data['board_scale']
    assert h>0 and den>0 and len(T)==3
    assert sorted(norm(sub(T[i],T[i-1])) for i in range(3))==sorted(
        (den*h*side_length)**2 for side_length in (c*c,a*(a+2*b),b*(2*a+b)))
    assert data['count']==h*h*(a+2*b)*(2*a+b)
    assert all(isinstance(x,int) for block in data['blocks'] for pt in block['points'] for x in pt)
    for blk in data['blocks']:
        raw=blk['points'];P=positive(raw)
        assert all(side(P[i-1],P[i],P[(i+1)%len(P)])>0 for i in range(len(P)))
        assert all(side(T[i-1],T[i],p)>=0 for p in P for i in range(3))
        if blk['kind']=='notch':
            t,k,j=blk['scale'],blk['notch'],blk['extend']
            expected=[(0,0),(0,t*b*den),(t*a*den-k*c*den,t*b*den),(t*a*den-k*a*a,t*b*den-k*a*b)]
            if j:
                expected=[expected[0]]+[(x,y+j*den*c) for x,y in expected[1:]]
                x,y=expected[-1]
                expected.append((x+j*a*b,y+j*(b*b-c*c)))
            cap=blk.get('cap',0)
            n=t*t-k*k+2*j*blk['width']+j*j
            if cap:
                assert j and cap <= blk['depth']*b
                step=(cap*b*(a+b),-cap*a*b)
                for pos in (-2,-1):
                    x,y=expected[pos]
                    expected[pos]=(x+step[0],y+step[1])
                expected.append((cap*den*c,0))
                n+=cap*(2*blk['depth']*b-cap+2*j)
            assert list(map(lambda p:sub(p,raw[0]),raw))==expected
            holes.append((t,k,n))
        elif blk['kind']=='triangle':
            k=blk['scale']
            assert type(k) is int and k>0 and len(raw)==3
            sizes=sorted(norm(sub(raw[i],raw[i-1])) for i in range(3))
            assert sizes==[k*k*z for z in unit]
            n=k*k
        else:
            assert blk['kind']=='parallelogram' and blk['diagonal'] in ('sum','difference')
            p,q,r,s=raw
            assert sub(q,p)==sub(r,s)
            rows,cols=blk['rows'],blk['cols']
            assert rows>0 and cols>0
            U=[Fraction(x,rows) for x in sub(q,p)]
            V=[Fraction(x,cols) for x in sub(s,p)]
            sign=1 if blk['diagonal']=='sum' else -1
            assert sorted(map(norm,(U,V,[x+sign*y for x,y in zip(U,V)])))==unit
            n=2*rows*cols
        assert ar(P)==n*a*b*den*den
        count+=n;regs.append(P)
    assert count==data['count'] and ar(T)==count*a*b*den*den
    assert all(separated(A,B) or separated(B,A) for A,B in combinations(regs,2))
    assert len(set(holes))==1
    return count,len(holes),holes[0]

if __name__=='__main__':
    for a,b,c in [(33,7,37),(35,13,43),(85,11,91),(143,25,157),(161,15,169),(323,37,343),(533,27,547)]:
        h=gcd(c-a,c-b)
        print('unit',a,b,c,[(j,verify(unit_board(a,b,c,j))) for j in sorted({1,2,h})])
        print('pentagon',a,b,c,verify(unit_board(a,b,c,2,1)))
    for u in (10,13,16,22,25,28,40,64,100):
        print('double',u,verify(doubled_board(u)))
