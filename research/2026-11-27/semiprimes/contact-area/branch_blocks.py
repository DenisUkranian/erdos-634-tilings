"""Enumerate all small rooted occupied branches under the local population bounds."""
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json


@lru_cache(None)
def trees(n):
    if n==1:
        return ((),)
    smaller=[(k,t) for k in range(1,n) for t in trees(k)]
    out=[]
    for degree in range(1,n):
        for children in combinations_with_replacement(smaller,degree):
            if sum(k for k,t in children)==n-1:
                out.append(tuple(t for k,t in children))
    return tuple(out)


def signatures(tree,c,limit):
    kids=[signatures(t,c,limit) for t in tree]
    totals={(0,0,0)}
    for child in kids:
        totals={(s+n,e+y,o+x) for s,e,o in totals for n,x,y in child if s+n<=limit-2}
    out=set()
    for n in range(2,limit+1):
        for g in range(-n,n+1,2):
            m=abs(g)
            if n==m and len(tree)+1<6:
                continue
            if not tree and ((22*n<91*m) if c==37 else (13*n<83*m)):
                continue
            if len(tree)<=1 and m and ((3*n<=10*m) if c==37 else (10*n<=39*m)):
                continue
            out.update((s+n,e+g,o) for s,e,o in totals if s+n<=limit)
    return out


def scan(c,limit):
    best=limit+1
    endpoint=[]
    for size in range(1,limit//2+1):
        for t in trees(size):
            small=min((n for n,e,o in signatures(t,c,limit) if e and o),default=limit+1)
            if small<best:
                best=small
                endpoint=[]
            if small==best<=limit:
                endpoint.append(t)
    return dict(block_floor=best,relaxed_equality_shapes=endpoint)


if __name__=='__main__':
    print(json.dumps({c:scan(c,k) for c,k in [(37,10),(43,12)]},indent=2))
