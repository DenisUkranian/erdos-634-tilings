"""Extreme-area mixed gate inventories and the physical 3431 residuals."""
from collections import Counter
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

from mixed_word_area import alphabet, maximum
from saturation import triples
SECTIONS=Path(__file__).resolve().parent.parent/'remote-sections'
sys.path.insert(0,str(SECTIONS))
from contours import repair
from replay import compile_cpp, run
from three_lifts import coordinates
from controls_marked import controls
from branch_blocks import scan

def inventories(params,exception):
    a,b,c=params
    bank=c-a+b
    moves,*_=alphabet(a,b,c,exception)
    low=bank+int(exception is not None and exception%2==0)
    high=bank+int(exception is not None and exception%2==1)
    for left in triples(low):
        for right in triples(high):
            inv=tuple(n for p in zip(left,right) for n in p)+((1,) if exception is not None else ())
            if all(sum(n*d[k] for n,d in zip(inv,moves))==0 for k in (0,1)):
                yield inv


def extremal_3431():
    params=(33,7,37)
    for exc in (0,1):
        for inv in inventories(params,exc):
            value=maximum(inv,10,params=params,exception=exc)
            if value is None:
                continue
            assert value==370*33*7
            words=maximum(inv,10,True,params,exc)
            assert len(words)==1
            word=[]
            for j in words[0]:
                i=exc if j==6 else j
                heading=(i+3*(i%2)+3*(j==6))%6
                word.append(6*(i%2)+heading)
            yield word


def normalized(poly):
    def turn(p):return -p[1],p[0]+p[1]
    choices=[]
    for q in (list(poly),[(x+y,-y) for x,y in reversed(poly)]):
        for _ in range(6):
            u,v=min(q)
            choices.append(min(tuple((x-u,y-v) for x,y in q[i:]+q[:i]) for i in range(len(q))))
            q=list(map(turn,q))
    return min(choices)


def polygons():
    out={}
    for word in extremal_3431():
        swap=[(6 if j<6 else 0)+(3-j)%6 for j in reversed(word)]
        for seq in (word,swap):
            p=normalized(repair(seq,33,7,37,10))
            low=sum(i<6 for i in seq)
            assert p not in out or out[p]==low
            out[p]=low
    return out

def literal_check(inv,w,params,exc,blocks):
    from saturation import letters
    from geometry import det
    a,b,c=params
    directions,axes,second=alphabet(a,b,c,exc)
    assert tuple(w.count(i) for i in range(len(inv)))==inv
    x=y=area=0
    for i in w:
        dx,dy=directions[i]
        area+=x*dy-y*dx
        x,y=x+dx,y+dy
    assert (x,y,area)==(0,0,a*b*c*blocks)
    for q in (a,b):
        _,labels=letters(a,b,c,q)
        stack=[]
        for symbol in w:
            j=exc if symbol==6 else symbol
            k,d=labels[j]
            e=d*(-1)**(j+(symbol==6))
            if stack and stack[-1][0]==k:
                e+=stack.pop()[1]
            if e%q:
                stack.append((k,e%q))
        assert not stack

def verify():
    result={}
    for params,size,exceptions in [((33,7,37),10,(0,1)),((35,13,43),16,(None,))]:
        rows=[]
        for exc in exceptions:
            for inv in inventories(params,exc):
                if exc is None and inv!=min(inv[k:]+inv[:k] for k in (0,2,4)):
                    continue
                value=maximum(inv,size,params=params,exception=exc)
                row=dict(exception=exc,inventory=inv,best_doubled_area=value)
                if value is not None:
                    a,b,c=params
                    assert value==size*c*a*b
                    words=maximum(inv,size,True,params,exc)
                    for w in words:
                        literal_check(inv,w,params,exc,size)
                    row.update(cyclic_words=len(words),first_word=list(words[0]))
                rows.append(row)
        result[str(params[2])]=rows
    assert scan(37,10)==dict(block_floor=10,relaxed_equality_shapes=[((),),((),())])
    with TemporaryDirectory() as temp:
        two=Path(temp)/'two'
        marked=Path(temp)/'marked'
        compile_cpp(SECTIONS/'slices.cpp',two)
        compile_cpp(SECTIONS/'marked.cpp',marked)
        result['control143']=controls(marked)
        result['two_lifts_3431']=[]
        for p,low in polygons().items():
            twodata=f'{len(p)} 1 {coordinates(p)}'
            rows=[list(map(int,l.split())) for l in run([two,33,7,37],twodata).splitlines()]
            assert [tuple(r[:2]) for r in rows]==list(product((-1,1),range(37)))
            assert all(r[2] in (1,2) for r in rows)
            result['two_lifts_3431'].append(dict(polygon=p,far_owners=low,
                    rejections=sorted(Counter(r[2] for r in rows).items())))
    # Check the two ordered group identities on the actual 143 unit skeletons.
    import importlib.util
    source=SECTIONS.parents[2]/'2026-11-26/semiprimes/charged-contour/review.py'
    spec=importlib.util.spec_from_file_location('contour_review',source)
    review=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)
    result['word_controls143']={w:review.full_control(w) for w in ('known','macro')}
    return result


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
