"""Native cuts with two middle owners and at most two extra opposite-bank steps."""
from collections import Counter
from itertools import product
import json
from native_owners import UNITS, add, board, compatible, inside, offsets, overlap, scale, shape, triangle
from middle_pairs import valid
from terminal import det
from two_native import census, need, prepend


def one_extra_pair(a,b,c,s,j):
    vertices = board(a,b,c)
    moves,apex = offsets(a,b,c,s,j)
    mods = (a,b)
    labels = []
    for m in mods:
        heading = (j+(s if m==a else 0))%6
        # Use the positive S generator at axis 2.
        def power(t):
            return 1 if t in (0,1,5) else -1
        r = power(heading)*(b if m==a else a)*pow(c,-1,m)%m
        labels.append([(t%3,power(t)) for t in range(6)]+[(heading%3,r),(heading%3,-r)])
    triangles = []
    path = []
    seen = {(0,0)}
    found = []
    def visit(p,area,remaining,state,words):
        for m,word,lbl in zip(mods,words,labels):
            for axis,positive,negative in ((0,0,3),(1,1,4),(2,5,2)):
                exps = tuple(e for i,e in word if i==axis)
                if not exps:
                    continue
                defects = tuple(lbl[t][1] for t in range(6+state,8) if lbl[t][0]==axis)
                corrections = defects + (-1,)*remaining[negative]
                if need(exps,m,corrections)>remaining[positive]:
                    return
        if state==2 and not any(remaining):
            assert not any(words) and p==scale(c,(a+b,-b))
            if area<0 and -area%(a*b*c)==0 and (-area//(a*b*c))%2:
                found.append((''.join(map(str,path)),-area//(a*b)))
            return
        for t in range(8):
            if (t<6 and not remaining[t]) or (t>=6 and state!=t-6):
                continue
            q = add(p,moves[t])
            if q in seen or not inside(scale(c,q),vertices):
                continue
            tri = triangle(scale(c,p),scale(c,q),apex[t])
            if not inside(tri[-1],vertices) or any(overlap(tri,prev) for prev in triangles):
                continue
            path.append(t)
            triangles.append(tri)
            seen.add(q)
            if t<6:
                remaining[t] -= 1
            reduced = [prepend(w,l[t][0],-l[t][1],m) for w,m,l in zip(words,mods,labels)]
            visit(q,area+det(p,q),remaining,state+(t>=6),reduced)
            if t<6:
                remaining[t] += 1
            seen.remove(q)
            triangles.pop()
            path.pop()
    for k in range(3):
        remaining = [a,0,0,0,0,b]
        remaining[k] += 1
        remaining[k+3] += 1
        visit((0,0),0,remaining,0,[((2,b%a),),((0,a%b),)])
    return found


def result(a,b,c):
    sides = {}
    for hand in (1,-1):
        paths = []
        for j in range(6):
            minimum = [(w.translate(str.maketrans('ES+-','0567')),n) for w,n in census(a,b,c,hand,j)]
            for extra,words in enumerate((minimum,one_extra_pair(a,b,c,hand,j))):
                for w,n in words:
                    owners = shape(a,b,c,hand,j,w)
                    if owners:
                        paths.append((extra,(n,j,w),owners))
        sides[hand] = paths
    counts = Counter()
    two_block = Counter()
    for (x,C,P),(y,T,Q) in product(sides[1],sides[-1]):
        n = C[0]-T[0]
        if n<2*c or not compatible(P,Q):
            continue
        if n==2*c:
            assert valid(a,b,c,C,T)<3
            two_block[x,y] += 1
        else:
            counts[x,y,n//c] += 1
    return dict(remaining=[[x,y,n,v] for (x,y,n),v in sorted(counts.items())],
                rejected_two_block=[[x,y,v] for (x,y),v in sorted(two_block.items())])


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    print(json.dumps({c:result(a,b,c) for a,b,c in ((33,7,37),(35,13,43))},indent=2))
