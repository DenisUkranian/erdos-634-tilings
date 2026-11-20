"""Count two-orientation whole-triangle tilings independently on small staircase boards."""
from functools import lru_cache
from math import comb,gcd

def formula(a,c,t):
    if t<a+c:
        return 1
    d=t-a-c
    assert d<a<c and gcd(a,c)==1
    return 1+comb(d+a+1,a+1)+comb(d+c+1,c+1)-comb(d+2,2)

def rectangular_cover(a,c,t,k=0):
    # After forcing all outer slant triangles, the available heights in
    # these integral x-columns form the ordinary a-by-c staircase.
    heights=tuple(c*(t-1-x//a) for x in range(a*(t-1)))
    @lru_cache(None)
    def count(front):
        low=min(front,default=0)
        if low==0 and not front:return 1
        candidates=[x for x,h in enumerate(front) if h<heights[x]]
        if not candidates:return 1
        y,x=min((front[x],x) for x in candidates)
        result=0
        for w,h in ((a,c),(c,a)):
            if x+w>len(front):continue
            if a*x+c*y<k*a*c and (w!=c or x%c or y%a):continue
            if any(front[v]!=y or heights[v]<y+h for v in range(x,x+w)):continue
            result+=count(front[:x]+(y+h,)*w+front[x+w:])
        return result
    result=count((0,)*len(heights))
    used=count.cache_info().misses
    count.cache_clear()
    return result,used

if __name__=='__main__':
    for a,c in [(1,2),(2,3),(3,4),(3,5),(4,5),(5,7)]:
        for t in range(max(1,a+c-1),2*a+c):
            expected=formula(a,c,t); result,used=rectangular_cover(a,c,t)
            assert result==expected,(a,c,t,result,expected)
            print(a,c,t,result,used,flush=True)

    for a,c in [(2,3),(3,5),(5,7)]:
        for d in range(a):
            for k in range(1,a+1):
                expected=comb(d+a-k,a-k)+comb(d+c-k,c-k)-1
                result,used=rectangular_cover(a,c,a+c+d,k)
                assert result==expected,(a,c,d,k,result,expected)
            print("prescribed corners",a,c,d,"all passed",flush=True)
