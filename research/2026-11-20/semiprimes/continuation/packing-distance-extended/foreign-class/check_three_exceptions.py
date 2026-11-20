"""Verify exact lower bounds on new placements outside a dominant foreign class."""
import gzip
import json
from collections import Counter
from itertools import permutations
from pathlib import Path
from check_endpoint_classes import difference, det, edges, make_rows, multiply, native, norm

HERE=Path(__file__).resolve().parent
A,B,C=35,13,43
D=C**6
UNIT_LENGTHS=(A,B,C)


def unit_vectors():
    units={}
    for h in range(-6,7):
        p=(D,0)
        for _ in range(abs(h)):
            p=multiply(p,(A,B) if h>0 else (A+B,-B))
            assert all(t%C==0 for t in p)
            p=(p[0]//C,p[1]//C)
        for j in range(6):
            units[h,j]=p
            p=(-p[1],sum(p))
    return units


UNITS=unit_vectors()
AXES={(l*x,l*y):(h,j%3) for (h,j),(x,y) in UNITS.items() for l in UNIT_LENGTHS}


def move(p,l,h,j):
    u,v=UNITS[h,j%6]
    return p[0]+l*u,p[1]+l*v


def inside(p):
    x,y=p
    return x>=0 and y>=0 and 2135*x+1079*y<=1079*2135*D


def anchored(point,h,j):
    # One incident side lies on the weighted undirected axis. The third side
    # determines the included angle. Its sine sign chooses the half-plane.
    for l,r in permutations(UNIT_LENGTHS,2):
        opposite=A+B+C-l-r
        m,n={A:(1,0),B:(0,1),C:(2,2)}[opposite]
        for d in (j,j+3):
            q=move(point,l,h,d)
            if not inside(q):continue
            for s in (-1,1):
                v=move(point,r,h+s*(n-m),d+s*m)
                assert norm(difference(q,v))==(D*opposite)**2
                if inside(v):
                    yield tuple(sorted((point,q,v)))


def case_bound(case,h,rows,reference,scale):
    weights={}
    for x,y,k,j,w in case['weights']:
        assert type(w) is int and w
        key=((x,y),k,j)
        assert key in rows and key not in weights
        assert abs(h-k)>1 or (h in (0,1) and native(h,(x,y)))
        weights[key]=w
    upper,lower=case['count_weights']
    assert upper<=0 and lower<=0
    score=85*upper-82*lower
    old=[upper-lower]*5059
    points={}
    for (p,k,j),w in weights.items():
        terms,board=rows[p,k,j]
        score+=w*(sum(s for _,s in terms)-board)
        for i,s in terms:old[i]+=s*w
        xy=(p[0]*(D//C),p[1]*(D//C))
        points[xy,k,j]=w
    score-=sum(max(0,x) for x in old)
    possible=set()
    for point,k,j in points:
        possible.update(anchored(point,k,j))
    possible.difference_update(reference)
    for t in possible:
        if det(difference(t[1],t[0]),difference(t[2],t[0]))<0:
            t=t[::-1]
        contribution=0
        for p,q in edges(t):
            k,j=AXES[difference(q,p)]
            contribution+=points.get((p,k,j),0)-points.get((q,k,j),0)
        # An additional x column has minus its signed interval endpoint events.
        score+=min(0,scale+contribution)
    assert score==case['lower_numerator'] and score>3*scale
    print(f'Height case {h:2}: {len(weights)} nonzero weights, {len(possible)} incident nonreference placements, bound {score}/{scale}.')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    with gzip.open(HERE/'reference_5063.json.gz','rt') as src:
        packing=json.load(src)
    rows={(p,k,j):(terms,rhs) for p,k,j,terms,rhs in make_rows(packing)}
    assert len(rows)==8499
    reference={tuple(sorted((x*(D//C),y*(D//C)) for x,y in t)) for t in packing['tiles']}
    data=json.loads((HERE/'three_exceptions_dual.json').read_text())
    assert data['scale']==10**6
    assert set(data['cases'])=={'-1','0','1','2'}
    for h in (-1,0,1,2):
        case_bound(data['cases'][str(h)],h,rows,reference,data['scale'])
