#!/usr/bin/env python3
"""Exact orientation/supporting-line obstruction for n_0=11 in N=154."""
import sys,json
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'closure-position-oct7/oct8-structural'))
from check_no_thirteen_height import compositions,EDGES,signature,max_lines

ALLOWED=[i for i in range(12) if (1 if i<6 else -1)*(-1)**(i%6)==1]

def check():
    cases=[]
    for six in compositions(11,6):
        inv=[0]*12
        for i,n in zip(ALLOWED,six): inv[i]=n
        if signature(inv)!=(11,0,0): continue
        totals=[[0,0] for _ in range(3)]
        for n,edges in zip(inv,EDGES):
            for d,l in edges: totals[d][int(abs(l)==7)]+=n
        if totals[0][0]<3:
            cases.append({'inventory':inv,'contradiction':'Fewer than three positively directed 8-edges available on the base.'})
            continue
        lm=[1+max_lines((totals[0][0]-3,totals[0][1]))]+[max_lines(tuple(t)) for t in totals[1:]]
        if min(lm)<0:
            cases.append({'inventory':inv,'totals':totals,'contradiction':'No affine-line partition.'})
            continue
        base_capacity=min(inv[0],lm[2])+min(inv[7],lm[1])
        if base_capacity<3:
            cases.append({'inventory':inv,'totals':totals,'maximum_lines':lm,'contradiction':'The base needs three 8-edges, but available gamma vertices allow only '+str(base_capacity)+'.'})
            continue
        bad=[]
        for i,(n,edges) in enumerate(zip(inv,EDGES)):
            if n>lm[edges[0][0]]*lm[edges[1][0]]:
                bad.append({'orientation':('A' if i<6 else 'B')+str(i%6),'tiles':n,'possible_gamma_vertices':lm[edges[0][0]]*lm[edges[1][0]]})
        assert bad,(inv,totals,lm)
        cases.append({'inventory':inv,'totals':totals,'maximum_lines':lm,'contradiction':bad[0]})
    assert len(cases)==28,len(cases)
    return {'status':'PASS','cases':cases,'conclusion':'n_0=11 is geometrically impossible; n_0>=24.','N154_solved':False}
if __name__=='__main__': print(json.dumps(check(),indent=2))
