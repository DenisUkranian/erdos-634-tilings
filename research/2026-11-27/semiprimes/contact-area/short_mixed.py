"""Rebuild the 22-owner classification and its marked section tests at 3431."""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

HERE = Path(__file__).resolve().parent
SECTIONS = HERE.parent/'remote-sections'
sys.path.insert(0,str(SECTIONS))
from replay import compile_cpp, run
from contours import repair
from controls_marked import controls
from three_lifts import batch, coordinates, trials
from saturation import UNITS, maximum, triples


def multiply(p,q):
    x,y=p
    a,b=q
    return x*a-y*b,x*b+y*a+y*b


def geometry():
    inventories = []
    for i in range(12):
        for j in range(12-i):
            k = 11-i-j
            rx,ry = multiply((40,-7),(i-j,j-k))
            if rx%37 or ry%37:
                continue
            X,Y = -rx//37,-ry//37
            middle,r = divmod(11-X+Y,3)
            if not r and min(middle+X,middle,middle-Y)>=0:
                inventories.append(((i,j,k),(middle+X,middle,middle-Y)))
    assert len(inventories)==3
    assert ((0,7,4),(7,0,4)) in inventories
    irreducible = []
    for n,k in [(7,4),(4,7)]:
        zero = [(i,j) for i,j in product(range(n+1),range(k+1)) if (7*i-37*j)%33==0]
        assert zero==[(0,0),(n,k)]
        irreducible.append(zero)
    areas = []
    word = None
    for i,j in product(range(5),repeat=2):
        # 0..5 are low; 6..11 are high in the same angular order.
        w = [10]*i+[2]*7+[10]*(4-i)+[4]*j+[6]*7+[4]*(4-j)
        x=y=s=0
        for l in w:
            u,v=multiply((40,-7) if l<6 else (37,0),UNITS[l%6])
            s+=x*v-y*u
            x,y=x+u,y+v
        assert x==y==0 and s==231*74*(j-i)
        if s==296*231:
            assert word is None
            word=w
        areas.append(s//231)
    assert word is not None
    direct = repair(word,33,7,37,blocks=8)
    # Reflection across the bank bisector followed by reversed traversal
    # swaps the long-edge alphabets in the repaired short chart.
    swap = [(6 if j<6 else 0)+(3-j)%6 for j in reversed(word)]
    reflected = repair(swap,33,7,37,blocks=8)
    def normalize(poly):
        u,v=min(poly)
        return [(x-u,y-v) for x,y in poly]
    def necklace(poly):
        v=normalize(poly)
        return min(v[k:]+v[:k] for k in range(len(v)))
    images = []
    for conj in (False,True):
        for j,rotor in enumerate(UNITS):
            image=[multiply(rotor,(x+y,-y) if conj else (x,y)) for x,y in direct]
            if conj:
                image.reverse()
            if necklace(image)==necklace(reflected):
                images.append((conj,j))
    assert images
    # Fix a CCW representative in an axial chart for the section replay.
    polygon=[multiply(UNITS[5],(x+y,-y)) for x,y in reversed(direct)]
    i=polygon.index(min(polygon))
    polygon=polygon[i:]+polygon[:i]
    return dict(inventories=inventories,area_range=[min(areas),max(areas)],
                word=word,bank_swap_isometries=images,polygon=polygon)


def ordinary_5063():
    rows=[]
    high={multiply((43,0),(i-j,j-k)):(i,j,k) for i,j,k in triples(21)}
    for i,j,k in triples(21):
        x,y=multiply((48,-13),(i-j,j-k))
        if (-x,-y) not in high:
            continue
        u,v,w=high[-x,-y]
        inventory=(i,w,j,u,k,v)
        score=maximum(35,13,43,inventory,35,reverse_high=True)
        rows.append(dict(inventory=inventory,order35_upper=score))
    assert len(rows)==7
    assert max(row['order35_upper'] for row in rows)==349160
    return rows


def verification(workers):
    data=geometry()
    data['ordinary_5063']=ordinary_5063()
    p=data['polygon']
    assert len(p)==21
    header=f'{len(p)} 100 {coordinates(p)}'
    with TemporaryDirectory() as temp:
        marked=Path(temp)/'marked'
        two=Path(temp)/'two'
        compile_cpp(SECTIONS/'marked.cpp',marked)
        compile_cpp(SECTIONS/'slices.cpp',two)
        data['control143']=controls(marked)
        inp=f'{len(p)} 1 {coordinates(p)}'
        two_rows=[tuple(map(int,l.split())) for l in run([two,33,7,37],inp).splitlines()]
        assert [(h,t) for h,t,_,_ in two_rows]==list(product((-1,1),range(37)))
        assert all(f in (1,2) for h,t,f,probe in two_rows)
        data['two_lift_outcomes']=sorted(Counter(row[2] for row in two_rows).items())
        first=batch(marked,'open',header,[(1,g,-1) for g in range(74)])
        rest=[(1,g,k) for _,g,_,status in first if not status for k in range(74)]
        second=trials(marked,'exact',header,rest,workers)
        data['open_outcomes']=sorted(Counter(row[3] for row in first).items())
        data['three_lift_outcomes']=sorted(Counter(row[3] for row in second).items())
        data['surviving_chains']=[row[1:3] for row in second if not row[3]]
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--workers',type=int,default=1)
    print(json.dumps(verification(parser.parse_args().workers),indent=2))
