"""Exact single-order area relaxation for each inventory at a saturated unit cut."""
from functools import lru_cache
from itertools import product
import json

UNITS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
ZERO = (0,)*6

def letters(a,b,c,order):
    moves, syllables = [], []
    for j,(x,y) in enumerate(UNITS):
        u,v = UNITS[j-1]
        low = j%2==0
        moves.append((a*x+b*u,a*y+b*v) if low else (c*x,c*y))
        heading = (j-1)%6 if low and order==a else j
        size = (b if order==a else a) if low else c
        syllables.append((heading%3,size if heading<3 else -size))
    return moves,syllables

def triples(n):
    for i in range(n+1):
        for j in range(n+1-i):
            yield i,j,n-i-j

def inventories(a,b,c):
    m = c+a-b
    for low in range(m+1):
        high = {(c*(k-j),c*(i-k)):(i,j,k) for i,j,k in triples(m-low)}
        for i,j,k in triples(low):
            x,y=i-j,j-k
            h=high.get((-(a+b)*x-b*y,b*x-a*y))
            if h is None:
                continue
            inv=(i,h[0],j,h[1],k,h[2])
            if inv!=min(inv[s:]+inv[:s] for s in (0,2,4)):
                continue
            for order in (a,b):
                _,syllables=letters(a,b,c,order)
                residual=[0]*3
                for t,(f,e) in zip(inv,syllables):
                    residual[f]+=t*e
                if any(r%order for r in residual):
                    break
            else:
                yield inv

def maximum(a,b,c,inv,order,last=None,*,reverse_high=False):
    moves,syllables=letters(a,b,c,order)
    if reverse_high:
        # All high headings change sign for ordinary-character saturation.
        for j in (1,3,5):
            x,y=moves[j]
            f,e=syllables[j]
            moves[j],syllables[j]=(-x,-y),(f,-e)
    by_axis=[[i for i,(f,_) in enumerate(syllables) if f==k] for k in range(3)]
    pairs=[]
    for i,j in by_axis:
        pairs.append([(x,y) for x in range(inv[i]+1) for y in range(inv[j]+1)
                      if (x*syllables[i][1]+y*syllables[j][1])%order==0])
    candidates=[]
    for parts in product(*pairs):
        vec=[0]*6
        for (i,j),(u,v) in zip(by_axis,parts):
            vec[i],vec[j]=u,v
        if any(vec):
            candidates.append(tuple(vec))

    guard=sum(32 << (6*j) for j in range(6))
    def pack(t):
        return sum(v << (6*j) for j,v in enumerate(t))
    encoded=[(v,pack(v)) for v in candidates]
    @lru_cache(None)
    def shift(t):
        return tuple(sum(k*v[d] for k,v in zip(t,moves)) for d in (0,1))

    @lru_cache(None)
    def solve(t,k):
        if t==ZERO:
            return 0
        x,y=shift(t)
        if x==y==0 and t!=inv:
            return None
        best=None
        for i in by_axis[k]:
            if not t[i]:
                continue
            pre=t[:i]+(t[i]-1,)+t[i+1:]
            prev=factor(pre,k)
            if prev is not None:
                u,v=moves[i]
                val=prev+x*v-y*u
                best=val if best is None else max(best,val)
        if t in neutral:
            # At an identity simply choose the factor of its actual last letter.
            return best
        current=pack(t)
        for sub,bits in encoded:
            if (guard+current-bits)&guard != guard:
                continue
            end=id_score(sub)
            if end is None:
                continue
            pre=tuple(u-v for u,v in zip(t,sub))
            start=factor(pre,k)
            if start is not None:
                u,v=shift(sub)
                val=start+end+x*v-y*u
                best=val if best is None else max(best,val)
        return best

    @lru_cache(None)
    def id_score(t):
        vals=[v for k in range(3) if (v:=solve(t,k)) is not None]
        return max(vals,default=None)

    neutral=set(candidates)|{ZERO}
    @lru_cache(None)
    def factor(t,k):
        return id_score(t) if t in neutral else solve(t,k)
    return id_score(inv) if last is None else factor(inv,syllables[last][0])

def run():
    out={}
    for a,b,c in [(33,7,37),(35,13,43)]:
        rows=[]
        for inv in inventories(a,b,c):
            values=[maximum(a,b,c,inv,q) for q in (a,b)]
            cap=None
            if None not in values:
                units=min(values)//(a*b*c)
                cap=c*(units-(units+1)%2)
            rows.append(dict(inventory=inv, area_maxima=values, population_cap=cap))
        out[c]=rows
    return out

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
