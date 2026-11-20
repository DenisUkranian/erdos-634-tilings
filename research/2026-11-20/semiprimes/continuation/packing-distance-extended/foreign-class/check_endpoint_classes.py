"""Check the foreign-height endpoint obstruction for the 5063 reference packing."""
from collections import Counter, defaultdict, deque
import gzip
import json
from math import gcd
from pathlib import Path


def multiply(p,q):
    x,y=p
    u,v=q
    return x*u-y*v, x*v+y*u+y*v


def difference(p,q): return p[0]-q[0],p[1]-q[1]


def det(p,q): return p[0]*q[1]-p[1]*q[0]


def norm(p): return p[0]**2+p[0]*p[1]+p[1]**2


def direction(p):
    d=gcd(*p)
    return p[0]//d,p[1]//d


def edges(points): return zip(points,points[1:]+points[:1])


def direction_table():
    table={}
    for h in range(-3,4):
        v=(1,0)
        for _ in range(abs(h)):
            v=multiply(v,(35,13) if h>0 else (48,-13))
        for j in range(6):
            table[direction(v)]=(h,j%3)
            v=(-v[1],v[0]+v[1])
    return table


def native(h,p):
    # p is stored after multiplication by 43.
    x,y=p
    if h==0: return not (x%43 or y%43)
    assert h==1
    v=multiply((x-1079*43,y),(48,-13))
    return not (v[0]%1849 or v[1]%1849)


def make_rows(data):
    axes=direction_table()
    def events(t):
        for p,q in edges(t):
            h,j=axes[direction(difference(q,p))]
            yield (p,h,j),1
            yield (q,h,j),-1
    board=list(map(tuple,data['board']))
    assert board==[(0,0),(1079*43,0),(0,2135*43)]
    tiles=[list(map(tuple,t)) for t in data['tiles']]
    assert len(tiles)==5059 and len({tuple(sorted(t)) for t in tiles})==len(tiles)
    rows=defaultdict(list)
    for i,t in enumerate(tiles):
        assert det(difference(t[1],t[0]),difference(t[2],t[0]))==35*13*43**2
        assert sorted(norm(difference(p,q)) for p,q in edges(t))==[(l*43)**2 for l in (13,35,43)]
        assert all(x>=0 and y>=0 and 2135*x+1079*y<=1079*2135*43 for x,y in t)
        p,q=next((p,q)for p,q in edges(t)if norm(difference(p,q))==(35*43)**2)
        h,_=axes[direction(difference(q,p))]
        assert h in (0,1) and all(native(h,p)for p in t)
        for key,sign in events(t): rows[key].append((i,sign))
    boundary=Counter()
    for key,s in events(board):
        boundary[key]+=s
        rows[key]
    return [(point,h,j,rows[point,h,j],boundary[point,h,j]) for point,h,j in sorted(rows)]


def contradiction(rows,h):
    active=[]
    occurrence=defaultdict(list)
    for p,k,j,terms,rhs in rows:
        # Discard every row that any candidate additional tile could touch.
        # When h=0 or 1, all foreign translates are permitted simultaneously.
        could_touch=(h is not None and abs(h-k)<=1 and (h not in (0,1) or not native(h,p)))
        if could_touch: continue
        row=len(active)
        active.append((terms,rhs))
        for i,_ in terms: occurrence[i].append(row)
    queue=deque(range(len(active)))
    pending=set(queue)
    assigned={}
    while queue:
        row=queue.popleft()
        pending.remove(row)
        terms,rhs=active[row]
        pos,neg=[],[]
        for i,sign in terms:
            if i in assigned: rhs-=sign*assigned[i]
            elif sign>0: pos.append(i)
            else: neg.append(i)
        if rhs>len(pos) or rhs< -len(neg):
            return len(active),len(assigned)
        if rhs!=len(pos) and rhs!= -len(neg): continue
        high=(rhs==len(pos))
        for group,value in ((pos,high),(neg,not high)):
            for i in group:
                assigned[i]=int(value)
                for j in occurrence[i]:
                    if j!=row and j not in pending:
                        pending.add(j)
                        queue.append(j)
    raise AssertionError('No contradiction found in branch '+str(h))


if __name__=='__main__':
    if not __debug__: raise SystemExit('Run with assertions enabled.')
    with gzip.open(Path(__file__).with_name('reference_5063.json.gz'),'rt') as src:
        data=json.load(src)
    rows=make_rows(data)
    assert len(rows)==8499
    assert {k for p,k,j,t,r in rows}=={-1,0,1,2}
    for h in (-2,-1,0,1,2,3,None):
        nr,nv=contradiction(rows,h)
        print('Additional short height',h,'checked rows',nr,'Boolean assignments before contradiction',nv)
    print('Every branch is impossible.')
