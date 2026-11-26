"""Exact disjoint signed-bank census for a charged leaf beyond the exterior path."""
from itertools import product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent / "boundary-word"))
from nested import cut_rows
from remote import norm_hex, signed_axes


def direction_options(a,b,c,k,cap):
    A,B = b*(2*a+b),a*(a+2*b)
    X,Y = A,-B
    if k == 2:
        X,r = divmod((a+b)*A-b*B,c)
        Y,s = divmod(-b*A-a*B,c)
        assert r == s == 0
    result = []
    for x in range(-cap,cap+1):
        for y in range(max(-cap,-cap-x),min(cap,cap-x)+1):
            u,r = divmod(X-a*x+b*y,c)
            v,s = divmod(Y-b*x-(a+b)*y,c)
            if r == s == 0 and norm_hex(x,y)+norm_hex(u,v)<=cap:
                result.append((u,v,x,y))
    return result


def spine(a,b,c,limit):
    rows = []
    for k in (1,2):
        cap = limit-c
        vectors = direction_options(a,b,c,k,cap)
        options = []
        for p,q,e,o,_ in cut_rows(c,a-b,k,limit):
            lengths = []
            for u,v,x,y in vectors:
                first,second = signed_axes(u,v,-p),signed_axes(x,y,q)
                if first is not None and second is not None:
                    lengths.append(sum(map(abs,first+second)))
            if lengths and min(lengths)<=cap:
                options.append((p,q,e,o,min(lengths)))
        rows.append(options)
    for first,second in product(*rows):
        p,q,e,o,m = first
        t,v,f,j,n = second
        if m+n<=limit:
            yield m+n,(b-a-e-q,-c-o,e-f,o-j-p-v,f-t,j),(p,q,t,v)


def census(a,b,c,limit=320):
    d=a-b
    best={}
    spine_rows=list(spine(a,b,c,limit))
    for parity,region in product(range(2),range(3)):
        result=limit+1
        for base,D,_ in spine_rows:
            for mag in range(1,(min(limit,result)-base)//(c+d)+1):
                for g in (mag,-mag):
                    residual=list(D)
                    residual[2*region+parity] -= c*g
                    residual[2*region+1-parity] -= d*g
                    result=min(result,base+(c+d)*mag+sum(map(abs,residual)))
        best[parity,region]=result
    return best


if __name__=="__main__":
    for a,b,c in [(33,7,37),(35,13,43)]:
        print(c,census(a,b,c))


def odd_source(a,b,c):
    d=a-b
    cap=6*c
    scores={k:cap+1 for k in ('axial','slant','middle_branch','native')}
    equality=[]
    for cost,D,banks in spine(a,b,c,cap):
        axial,slant=D[1],D[5]
        if (axial,slant)==(-c,0):
            loc='axial'
        elif (axial,slant)==(0,-c):
            loc='slant'
        elif (axial,slant)==(0,0):
            loc='native'
        else:
            continue
        middle=-D[2]//c
        best=cost+(c+d)*abs(middle)
        scores[loc]=min(scores[loc],best)
        if loc=='axial':
            equality.append((best,banks,D))
        if loc=='native':
            # Beyond this range the physical even bank alone exceeds cap.
            for j in range(-cap//c-2,cap//c+3):
                bound=cost+abs(c*j-d)+abs(d*j-c)+(c+d)*abs(middle-j)
                scores['middle_branch']=min(scores['middle_branch'],bound)
    return scores,[row for row in equality if row[0]==scores['axial']]
