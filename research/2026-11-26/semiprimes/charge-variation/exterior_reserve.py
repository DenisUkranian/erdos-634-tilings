"""Bound total odd charge variation using disjoint branch populations and native banks."""
from collections import Counter
from functools import lru_cache
import json

from branch_reserve import control
from hull import ceil_div
from verify import branch, cell, geom, reconstruct, step


def local(c,d,a,b,limit,budget):
    """Cheapest half-excess for each charge magnitude and degree surplus."""
    rows={}
    A,B=(3810,1002) if c==37 else (4304,1001)
    fee=2 if c==37 else 3
    for k in range(1,limit+1):
        for x in range(int(k==1 or (c==43 and k==2)),budget//c+1):
            p=a*c*k//b+c*x
            for degree in range(1,2*c+1):
                J=max(0,ceil_div(c*k-degree*p,d))
                if (J and p<d) or (c==43 and k==x==degree==1):
                    continue
                gates=ceil_div(J,p//d) if J else 0
                if degree==1 and (k+2*x)*B<A*k:
                    gates=max(gates,1)
                if degree+gates>2*c:
                    continue
                cost=c*x+fee*c*gates+max(0,c*J-d*k)
                key=k,2-degree
                if cost<=budget:
                    rows[key]=min(cost,rows.get(key,budget+1))
    # A higher surplus at no greater cost always suffices for a lower bound
    # on the required surplus, including after reserving the middle vertex.
    return {(k,s):v for (k,s),v in rows.items()
            if not any(t>s and w<=v for (j,t),w in rows.items() if j==k)}


def by_surplus(rows,limit,budget):
    """Minimum cost with exact total absolute charge and exact sum of surpluses."""
    result=[{0:0}]+[{} for _ in range(limit)]
    for total in range(1,limit+1):
        for (k,s),cost in rows.items():
            if k>total:
                continue
            for t,n in result[total-k].items():
                if n+cost<=budget:
                    result[total][s+t]=min(result[total].get(s+t,budget+1),n+cost)
    return result


def board(c,d,a,b,N,V):
    plus,minus=(V+1)//2,(V-1)//2
    budget=(N-(c+d)*V)//2
    rows=local(c,d,a,b,plus,budget)
    costs=by_surplus(rows,plus,budget)
    total=max(i+j for i,x in costs[plus].items() for j,y in costs[minus].items() if x+y<=budget)
    if total:
        return dict(half_budget=budget,maximum_surplus=total)

    @lru_cache(None)
    def others(P,M,need):
        return min((x+y for i,x in costs[P].items() for j,y in costs[M].items()
                    if i+j>=need),default=budget+1)

    feasible=0
    minimum=None
    for sign,limit in ((1,plus),(-1,minus)):
        for k in range(1,limit+1):
            P,M=plus-k*(sign==1),minus-k*(sign==-1)
            for degree in range(3,min(2*c,2+P+M)+1):
                other=others(P,M,degree-2)
                if other>budget:
                    continue
                for x in range(int(k==1 or (c==43 and k==2)),(budget-other)//c+1):
                    p=c*x+a*c*k//b
                    for e in range(-c,c+1):
                        axial=sign*(2*c+d*e)
                        if not -c*x<=axial<=p:
                            continue
                        first=d+c*e
                        core=max(64 if c==37 else 75,abs(first)+(8 if c==37 else 5))
                        for f in range(-c,c+1):
                            slant=sign*(-c+d*f)
                            if not -c*x<=slant<=p:
                                continue
                            if sum(max(-v,0) for v in (axial,slant))>c*x:
                                continue
                            if sum(max(v,0) for v in (axial,slant))>c*(k+x):
                                continue
                            J=max(0,ceil_div(c*k-axial-slant-(degree-2)*p,d))
                            if J and p<d:
                                continue
                            gates=ceil_div(J,p//d) if J else 0
                            second=c*f
                            delta=d*k-sign*(first+second)
                            even=core+2*abs(second)+max(abs(delta),2*c*J-delta)
                            even+=(4 if c==37 else 6)*c*gates
                            cost=other+c*x+ceil_div(even-d*k,2)
                            minimum=cost if minimum is None else min(minimum,cost)
                            feasible+=int(cost<=budget)
    return dict(half_budget=budget,maximum_surplus=total,
                minimum_after_budget_prefilters=minimum,affordable_middle_cases=feasible)


def coordinates(name):
    g=geom.Geometry(5,3,7)
    tiles,_=geom.read_tiles(g,name)
    polys,*_=geom.check_full_tiling(g,tiles)
    lifts,T=reconstruct(g,tiles,polys)
    C,B=T[:1],T[:-1]
    banks=Counter()
    for i,t in enumerate(tiles):
        w=step(lifts[i],cell(g,t[1]+t[3],g.vertices(t)[-1]))
        banks[lifts[i],w]-=geom.eps(t)
    result=[]
    for v in (C,T):
        side=[i for i in range(len(tiles)) if lifts[i]!=B and branch(B,lifts[i])==v]
        O=sum(-geom.eps(tiles[i]) for i in side if tiles[i][1]%2)
        E=sum(-geom.eps(tiles[i]) for i in side if not tiles[i][1]%2)
        d=g.a-g.b
        assert O==0 and (E-d*(v==C))%g.c==0
        e=(E-d*(v==C))//g.c
        assert banks[B,v]==d*e+(2*g.c if v==C else -g.c)
        assert banks[v,B]==E
        result.append([banks[B,v],banks[v,B]])
    return dict(native_banks=result,**control(name))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    results={}
    for c,d,a,b,N,values in ((37,26,43,222,3431,[45,43,41]),
                              (43,22,8,43,5063,[63,61])):
        data={v:board(c,d,a,b,N,v) for v in values}
        assert all(r['maximum_surplus']<0 or
                   (r['maximum_surplus']==0 and r['affordable_middle_cases']==0)
                   for r in data.values())
        endpoint=values[-1]-2
        data[endpoint]=board(c,d,a,b,N,endpoint)
        assert data[endpoint]["maximum_surplus"]==1
        results[N]=data
    results['143']={name:coordinates(name) for name in ('known','macro')}
    print(json.dumps(results,indent=2))
