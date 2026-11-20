#!/usr/bin/env python3
"""Known-tiling replay of joint-cell currents and the charge reserve inequality."""
from collections import Counter,defaultdict
from pathlib import Path
import argparse,json,sys

def check(base):
    base=Path(base);sys.path[:0]=[str(base/'global-endpoints/integer'),str(base/'vertex-phase')]
    from global_core_sat import Geometry
    from phase_budget import PhaseBudget
    g=Geometry(5,3,7);budgets=[PhaseBudget(g,s)for s in(1,-1)];cells=defaultdict(Counter)
    for q,h,j,s in json.loads((base/'global-endpoints/tiling_143.json').read_text())['tiles']:
        q=tuple(q);key=(h,budgets[0].node(q,h),budgets[1].node(q,-h))
        cells[key][s*(-1)**j]+=1
    checks=0
    for key,count in cells.items():
        core=key==(0,(0,0,0),(0,0,0));G=count[1]-count[-1]
        assert (G+(g.a-g.b if core else 0))%g.c==0
        if not core:
            assert sum(count.values())!=g.c
            if abs(G)==g.c:assert min(count[1],count[-1])>=1
        checks+=1
    rows=[]
    for tree in(0,1):
        groups=defaultdict(list)
        for key,count in cells.items():groups[key[tree+1]].append((key,count))
        for node,cs in groups.items():
            if node==(0,0,0):continue
            p=sum(x[1]for _,x in cs);q=sum(x[-1]for _,x in cs)
            assert p%g.c==q%g.c==0;p//=g.c;q//=g.c
            charges=[(x[1]-x[-1])//g.c for _,x in cs]
            P=sum(max(t,0)for t in charges);Q=sum(max(-t,0)for t in charges);m=sum(abs(t)==1 for t in charges)
            reserve=(m+g.c-1)//g.c
            assert p>=P+reserve and q>=Q+reserve
            if p+q<=3:assert sum(t!=0 for t in charges)<=1
            rows.append({'tree':tree,'node':node,'positive_blocks':p,'negative_blocks':q,'charges':charges})
    return {'status':'PASS','N':143,'cells_checked':checks,'ordinary_rows_checked':len(rows),'rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('base');args=p.parse_args();print(json.dumps(check(args.base)))
