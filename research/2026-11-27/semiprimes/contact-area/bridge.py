"""Exact endpoint inventories, both projections, literal high-area words and board fits."""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from subprocess import check_output, run
from tempfile import TemporaryDirectory
import json
from four_gates import solve
from saturation import letters,UNITS

MOVES, ORDER13 = letters(35,13,43,13)
MOVES[3] = (43,0)
ORDER13[3] = (0,43)


def inventories():
    # Net counts on the three axes (0,1,2) of each bank. The large bank
    # has 64 owners and absolute character 64, the small bank has nine.
    patterns = []
    for i in range(65):
        for j in range(65-i):
            k = 64-i-j
            x,y = [sum(n*v[d] for n,v in zip((i,j,k),MOVES[::2])) for d in (0,1)]
            if x%43 or y%43:
                continue
            # Signed counts u,v,w in directions U0,U1,U2 give
            # displacement (u-w,v+w), character u-v+w=-1.
            X,Y = -x//43,-y//43
            if (-1-X+Y)%3:
                continue
            w = (-1-X+Y)//3
            u,v = X+w,Y-w
            if abs(u)+abs(v)+abs(w) <= 9:
                patterns.append(((i,j,k),(u,v,w)))
    return patterns


def interleave(common,n,rare,k):
    for slots in combinations(range(n+k),k):
        word = [common]*(n+k)
        for i in slots:
            word[i] = rare
        yield tuple(word)


def key(word):
    stack = []
    x=y=score=0
    for j in word:
        a,b = MOVES[j]
        score += x*b-y*a
        x,y = x+a,y+b
        f,k = ORDER13[j]
        if stack and stack[-1][0]==f:
            k += stack.pop()[1]
        if k%13:
            stack.append((f,k%13))
    return tuple(stack),score


def append(words,gaps):
    for word in words:
        for gap in gaps:
            yield word+gap


def insert_balanced(words):
    for word in words:
        for gap in interleave(4,6,3,1):
            for i in range(1,len(word)):
                yield word[:i]+gap+word[i:]


def match(prefixes,suffixes):
    groups = defaultdict(list)
    for word in suffixes:
        stack,score = key(word)
        inverse = tuple((f,(-k)%13) for f,k in reversed(stack))
        groups[inverse].append((word,score))
    accepted = 0
    best = None
    high = []
    for prefix in prefixes:
        stack,score = key(prefix)
        for suffix,extra in groups.get(stack,()):
            accepted += 1
            area = score+extra
            best = area if best is None else max(best,area)
            if area >= 455*2537:
                high.append(prefix+suffix)
    return dict(accepted=accepted,maximum=best),high


def multiply(p,q):
    x,y=p
    a,b=q
    return x*a-y*b,x*b+y*a+y*b


def roof_excess(word):
    x=y=0
    points = []
    for j in word:
        points.append((x,y))
        dx,dy = MOVES[j]
        x,y = x+dx,y+dy
    assert x==y==0
    least = None
    for basis in [(43,0),(48,-13),(35,13)]:
        for turn in UNITS:
            rotor = multiply(turn,basis)
            for reflect in (False,True):
                pts = [multiply(rotor,(x+y,-y) if reflect else (x,y)) for x,y in points]
                x0,y0 = min(x for x,y in pts),min(y for x,y in pts)
                worst = max(min(48*(x-x0)+13*(y-y0)-13*43*2135,
                                35*(x-x0)+48*(y-y0)-35*43*1079) for x,y in pts)
                least = worst if least is None else min(least,worst)
    return least


def check():
    profiles = {}
    for a,b,c,L in [(33,7,37,203),(35,13,43,229)]:
        rows = solve(a,b,c,L,True,collect=True)
        assert len(rows)==1
        profiles[c] = rows[0]
    patterns = inventories()
    assert ((17,23,24),(4,2,-3)) in patterns
    assert len(patterns)==3 and all(sum(map(abs,h))==9 for _,h in patterns)
    with TemporaryDirectory() as temp:
        binary = str(Path(temp)/'bridge')
        run(['c++','-O3','-std=c++17',str(Path(__file__).with_name('bridge.cpp')),'-o',binary],check=True)
        scores = {u:int(check_output([binary,str(u)])) for u in range(-24,25)}
    assert [u for u,s in scores.items() if s>=455*2537]==[-24,-18]
    A,B = list(interleave(0,17,5,3)),list(interleave(2,23,1,2))
    by_type, high = {},[]
    for label, first, second in [
        ('-24', append(A,[(3,)*4]),append(B,[(4,)*24])),
        ('-18 four out',append(A,list(interleave(4,6,3,4))),append(B,[(4,)*18])),
        ('-18 one back',append(A,[(3,)*3]),append(B,list(interleave(4,24,3,1)))),
        ('-18 one within A',append(insert_balanced(A),[(3,)*3]),append(B,[(4,)*18])),
        ('-18 one within B',append(A,[(3,)*3]),append(insert_balanced(B),[(4,)*18]))]:
        by_type[label], words = match(first,second)
        high.extend(words)
    assert len(high)==4
    details = []
    for word in high:
        stack,area = key(word)
        assert not stack and area%455==0
        excess = roof_excess(word)
        assert excess>0
        details.append(dict(word=''.join(map(str,word)),tiles=area//455,minimum_excess=excess))
    return dict(endpoint_profiles=profiles,signed_inventories=patterns,level_scores=scores,
                exact_matches=by_type,large_contours=details)


if __name__=='__main__':
    print(json.dumps(check(),indent=2))
