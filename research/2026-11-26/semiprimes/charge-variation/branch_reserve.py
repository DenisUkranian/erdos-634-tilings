"""Two exact optimizations of the disjoint branch reserve, and coordinate controls."""
from collections import Counter
from functools import lru_cache
import json
from verify import branch, cell, geom, reconstruct, step
from hull import ceil_div


def options(c, d, num, den, limit, budget, by_current):
    for k in range(1, limit+1):
        for x in range(int(k == 1 or (c == 43 and k == 2)), budget//c + 1):
            cap = num*c*k//den + c*x
            units = cap//d
            if by_current:
                rows = []
                # j=0 dominates negative net outward current in this relaxation.
                for j in range((budget-c*x+d*k)//c + 1):
                    if j and not units:
                        continue
                    degree = max(1, ceil_div(c*k-d*j, cap))
                    if c == 43 and k == 1 and x == 1:
                        degree = max(degree, 2)
                    rows.append((degree,j))
            else:
                rows = [(l,max(0,ceil_div(c*k-l*cap,d))) for l in range(1,2*c+1)]
            for degree, j in rows:
                if degree > 2*c or (c == 43 and k == x == degree == 1):
                    continue
                if j and not units:
                    continue
                gates = ceil_div(j,units) if units else 0
                if degree+gates > 2*c:
                    continue
                cost = c*(x+gates)+max(0,c*j-d*k)
                if cost <= budget:
                    yield k, cost, 2-degree


def solve(c,d,num,den,N,V,by_current):
    plus, minus = (V+1)//2, (V-1)//2
    budget = (N-(c+d)*V)//2
    rows = {}
    for k,cost,s in options(c,d,num,den,plus,budget,by_current):
        rows[k,cost] = max(rows.get((k,cost),-2*c),s)
    # Drop options dominated for this charge in both budget and degree.
    choices = []
    for k in range(1,plus+1):
        best = -2*c
        for cost in range(budget+1):
            score = rows.get((k,cost),-2*c)
            if score > best:
                choices.append((k,cost,score))
                best = score
    @lru_cache(None)
    def surplus(total,available):
        if not total:
            return 0
        return max((s+surplus(total-k,available-cost) for k,cost,s in choices
                    if k<=total and cost<=available), default=-1000000)
    return max(surplus(plus,i)+surplus(minus,budget-i) for i in range(budget+1))


def control(which):
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,which)
    polys,*_ = geom.check_full_tiling(g,tiles)
    lifts,T = reconstruct(g,tiles,polys)
    C = T[:1]
    short, long, sign = [], [], []
    for i,t in enumerate(tiles):
        short.append(lifts[i])
        long.append(step(lifts[i],cell(g,t[1]+t[3],g.vertices(t)[-1])))
        sign.append(-geom.eps(t))
    charges, received = Counter(), Counter()
    for v,w,s in zip(short,long,sign):
        charges[v] += s
        received[w] += s
    c,d = g.c,g.a-g.b
    mark = {C,T} | {v for v,s in charges.items() if v[-1][0]%2 and s}
    for v in set(short+long)|{C,T}:
        if v[-1][0]%2:
            assert c*received[v] == d*charges[v]
        else:
            assert (charges[v]-d*(v==C))%c == 0
            e = (charges[v]-d*(v==C))//c
            assert received[v] == d*e+2*c*(v==C)-c*(v==T)
    seen = set()
    for v in mark-{C,T}:
        hull = {branch(v,m) for m in mark-{v}}
        for w in {b for a,b in zip(short,long) if a==v}-hull:
            side = {i for i,u in enumerate(short) if u!=v and branch(v,u)==w}
            assert not seen & side
            seen |= side
            Q = sum(s for u,z,s in zip(short,long,sign) if (u,z)==(v,w))
            P = sum(s for u,z,s in zip(short,long,sign) if (u,z)==(w,v))
            assert Q%d == 0 and P*d==c*Q
            if all(not tiles[i][1]%2 for i in side):
                assert all(short[i]==w for i in side)
    return {"ordinary_off_hull_tiles_checked":len(seen),"tiles":len(tiles)}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Assertions must be enabled.")
    report = {}
    for c,d,num,den,N,values in [(37,26,43,222,3431,{51:-6,49:-4,47:-2,45:1}),
                                 (43,22,8,43,5063,{71:-4,69:-3,67:-2,65:-1,63:0})]:
        for V,s in values.items():
            for method in (False,True):
                assert solve(c,d,num,den,N,V,method)==s,(c,V,method)
        report[str(N)] = values
    report["controls_143"] = {w:control(w) for w in ("known","macro")}
    print(json.dumps(report,indent=2))
