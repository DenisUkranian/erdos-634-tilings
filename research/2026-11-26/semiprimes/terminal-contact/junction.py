"""Exact whole-owner tests for the two three-direction distinguished inventories."""
from collections import defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "boundary-word"))
from remote import inventories
from terminal import add, det


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def orient(p, q, r):
    return det(sub(q, p), sub(r, p))


def ccw(p, q, r):
    return (p, q, r) if orient(p, q, r) > 0 else (p, r, q)


def contains(p, tri):
    return all(orient(tri[k-1], tri[k], p) >= 0 for k in range(3))


def overlap(first, second):
    for triangle, other in ((first, second), (second, first)):
        for k in range(3):
            if all(orient(triangle[k-1], triangle[k], p) <= 0 for p in other):
                return False
    return True


class Model:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
        self.A = b*(2*a+b)
        self.B = a*(a+2*b)
        self.board = ccw((-b*self.B, -a*self.B), (b*c*c, -(a+b)*c*c), (0, 0))
        self.moves = (((a+b, -b), (-b, -a), (c, 0)), ((0, -c), (a, b), (b, -a-b)))
        self.apex = (((a*c, 0), (0, -a*c), (a*(a+b), -a*b)),
                     ((a*b, -a*(a+b)), (a*c, 0), (0, -a*c)))
        self.caps = ((c-a, c+b, c-a+b), (c, b, c-a))
        self.semigroup = {a*x+b*y for x in range(self.B//a+1) for y in range(self.B//b+1)}

    @lru_cache(None)
    def st(self, cut, counts):
        return tuple(sum(n*v[j] for n, v in zip(counts, self.moves[cut])) for j in (0, 1))

    @lru_cache(None)
    def tri(self, cut, counts, token):
        x, y = self.st(cut, counts)
        p = (self.c*x, self.c*y)
        dx, dy = self.moves[cut][token]
        q = add(p, (self.c*dx, self.c*dy))
        return ccw(p, q, add(p, self.apex[cut][token]))

    @lru_cache(None)
    def local(self, cut, counts, last, token):
        poly = self.tri(cut, counts, token)
        if not all(contains(p, self.board) for p in poly):
            return False
        if last < 0:
            return True
        prev = list(counts)
        prev[last] -= 1
        return not overlap(poly, self.tri(cut, tuple(prev), last))

    def next(self, counts, token):
        following = list(counts)
        following[token] += 1
        return tuple(following)

    def upper(self):
        a, b, c = self.a, self.b, self.c
        for residue in range(b):
            @lru_cache(None)
            def tails(counts, last):
                if counts == self.caps[1]:
                    return ("",)
                i, j, k = counts
                x, y = c*j-b*i, -a*i-c*k
                result = []
                for t in range(3):
                    if counts[t] == self.caps[1][t] or (t != 1 and -x not in self.semigroup):
                        continue
                    if (t == 1 and y%b != residue) or (t == 2 and x%a):
                        continue
                    if self.local(1, counts, last, t):
                        result.extend(str(t)+w for w in tails(self.next(counts, t), t))
                return tuple(result)

            for word in tails((0, 0, 0), -1):
                width = area = 0
                for token in word:
                    if token == "0":
                        area += width*a
                        width += b
                    elif token == "1":
                        width -= c
                    else:
                        area += width*c
                n, rem = divmod(2*area, a*b)
                if not rem and n%(2*c) == 0:
                    yield word, n+c
            tails.cache_clear()

    def first_graph(self):
        graph = {}
        for counts in product(*(range(n+1) for n in self.caps[0])):
            _, j, k = counts
            y = self.B-self.c*j+self.b*k
            for last in range(-1, 3):
                if (last >= 0 and not counts[last]) or (last < 0 and any(counts)):
                    continue
                following = []
                for token in range(3):
                    if counts[token] == self.caps[0][token] or (token != 1 and y not in self.semigroup):
                        continue
                    if self.local(0, counts, last, token):
                        following.append(token)
                graph[counts, last] = following
        return graph


def cases(a,b,c):
    d=a-b
    lower=list(inventories(a,b,c,1,d-2*c,c-d,3*c-2*d))
    upper=list(inventories(a,b,c,2,-c,c-d,2*c-d))
    assert any((L,R)==((c-a,0,c+b),(c-d,0,0)) for _,L,R in lower)
    assert any((L,R)==((0,0,c),(b,0,c-a)) for _,L,R in upper)
    if c == 43:
        assert {tuple(row[1:]) for row in lower} == {
            ((8+6*i,i,56-7*i),(21-7*i,i,6*i)) for i in range(4)}
        assert {tuple(row[1:]) for row in upper} == {
            ((0,0,43),(13,0,8)), ((6,1,36),(6,1,14))}
        assert all((43*u-13*v)%35 or v == 6*u for u in range(4) for v in range(19))
        assert all((43*u+35*v)%13 or u == v for u in range(4) for v in range(4))
    # Exhaust possible SIGNED-CHARACTER circulation sizes under saturation.
    # Any nonempty such circulation consumes all c-d high-alphabet letters.
    for k,rows in enumerate((lower,upper),1):
        for _,L,R in rows:
            for u,v in product(range(sum(L)+1),range(sum(R)+1)):
                if not u+v or (u+v)%(c-d) or (u-v)%(c+d):
                    continue
                assert u==v==c-d
                remaining=sum(L)-u
                assert remaining<c or (remaining==c and k==1)
    return len(lower),len(upper)


def verify(a,b,c):
    counts=cases(a,b,c)
    model=Model(a,b,c)
    upper=list(model.upper())
    graph=model.first_graph()
    # Each graph state represents all prefixes with these counts and last owner.
    # Different permitted second-cut words stay separate.
    def buckets(P):
        size=c*c
        x,y=zip(*P)
        return product(range(min(x)//size,max(x)//size+1),
                       range(min(y)//size,max(y)//size+1))
    @lru_cache(None)
    def collides(s,t,poly):
        return overlap(model.tri(0,s,t),poly)
    for word,n in upper:
        s=(0,0,0)
        obstacle=defaultdict(set)
        for letter in word:
            j=int(letter)
            poly=model.tri(1,s,j)
            for bucket in buckets(poly):
                obstacle[bucket].add(poly)
            s=model.next(s,j)
        @lru_cache(None)
        def allowed(s,j):
            near=set().union(*(obstacle[bucket] for bucket in buckets(model.tri(0,s,j))))
            return not any(collides(s,j,poly) for poly in near)
        @lru_cache(None)
        def reaches_x(s,last):
            if s==model.caps[0]:
                return True
            return any(allowed(s,j) and reaches_x(model.next(s,j),j)
                       for j in graph[s,last])
        assert not reaches_x((0,0,0),-1)
        allowed.cache_clear()
        reaches_x.cache_clear()
    assert len(upper)==(42 if c==37 else 109)
    print(c,counts,"axis inventory counts;",len(upper),"second-cut words, zero compatible first-cut paths")
    collides.cache_clear()


if __name__=="__main__":
    verify(33,7,37)
    verify(35,13,43)
