"""Intersect the two supported word identities with exact area thresholds on ordinary mixed contours."""
from functools import lru_cache
from pathlib import Path
import sys
from saturation import letters

SOURCE=Path(__file__).resolve().parents[3]/'2026-11-26/semiprimes/charged-contour'
sys.path.insert(0,str(SOURCE))
from grammar import program
from geometry import det

@lru_cache(maxsize=65536)
def join(x,y,q):
    i,j=len(x),0
    while i and j<len(y) and x[i-1]//q==y[j]//q:
        a,b=x[i-1],y[j]
        e=(a+b)%q
        i-=1
        j+=1
        if e:
            return x[:i]+(a//q*q+e,)+y[j:]
    return x[:i]+y[j:]

def alphabet(a,b,c,exception):
    directions,first=letters(a,b,c,a)
    _,second=letters(a,b,c,b)
    directions=[(x*(-1)**j,y*(-1)**j) for j,(x,y) in enumerate(directions)]
    second=[(k,e*(-1)**j) for j,(k,e) in enumerate(second)]
    axes=[k for k,e in first]
    if exception is not None:
        x,y=directions[exception]
        directions.append((-x,-y))
        axes.append(axes[exception])
        k,e=second[exception]
        second.append((k,-e))
    return tuple(directions),tuple(axes),second


def maximum(inv,blocks,trace=False,params=(35,13,43),exception=None):
    a,b,c=params
    directions,axes,second=alphabet(a,b,c,exception)
    atoms=len(inv)
    rules,ds=program(inv,a,c,-1,directions,axes)
    # Each grammar state has a fixed physical displacement. Compute the best
    # possible area, then the minimum required area of each child on any pass.
    rules=[[] for _ in range(atoms+1)]+[[(i,j,det(ds[i],ds[j])) for i,j in terms] for terms in rules]
    upper=[0]*(atoms+1)
    for terms in rules[atoms+1:]:
        upper.append(max(upper[i]+upper[j]+w for i,j,w in terms))
    need=[None]*len(rules)
    need[-1]=blocks*a*b*c
    remaining=[0]*len(rules)
    for n in reversed(range(atoms+1,len(rules))):
        useful=[]
        if need[n] is not None:
            for i,j,w in rules[n]:
                if upper[i]+upper[j]+w<need[n]:
                    continue
                for child,sibling in ((i,j),(j,i)):
                    required=need[n]-w-upper[sibling]
                    if need[child] is None or need[child]>required:
                        need[child]=required
                    remaining[child]+=1
                useful.append((i,j,w))
        rules[n]=useful
    states=[{(b*k+e%b,):0} for j,(k,e) in enumerate(second)]+[{():0}]
    for n in range(atoms+1,len(rules)):
        out={}
        for i,j,w in rules[n]:
            for x,left in states[i].items():
                for y,right in states[j].items():
                    v=left+right+w
                    if v>=need[n]:
                        key=join(x,y,b)
                        if v>out.get(key,-10**9):
                            out[key]=v
            for child in (i,j):
                remaining[child]-=1
                if not trace and not remaining[child]:
                    states[child]=None
        states.append(out)
    if not trace:
        return states[-1].get(())
    @lru_cache(None)
    def spell(n,key):
        if n<=atoms:
            return {bytes([n]) if n<atoms else b''}
        target=states[n][key]
        words=set()
        for i,j,w in rules[n]:
            for x,left in states[i].items():
                # x*y=key uniquely determines the suffix in the free product.
                inverse=tuple(b*(g//b)+b-g%b for g in reversed(x))
                y=join(inverse,key,b)
                if states[j].get(y,-10**9)+left+w!=target:
                    continue
                words.update(u+v for u in spell(i,x) for v in spell(j,y))
        return words
    def necklace(word):
        return min(word[j:]+word[:j] for j in range(len(word)))
    return sorted({necklace(w) for w in spell(len(rules)-1,())})
