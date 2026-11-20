#!/usr/bin/env python3
"""Standard-library replay of saved integer residue witnesses and statuses."""
from collections import Counter
import json
from pathlib import Path

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def check(path):
    data=json.loads(path.read_text())
    a,b,c=data['tile']
    assert a*a+a*b+b*b==c*c
    if not data.get('exact_integer_witness'):
        assert data['status']==1 and 'Time limit' in data['message']
        assert 'witness' not in data
        return {'tile':[a,b,c],'result':'inconclusive timeout; no witness or infeasibility proof'}
    rows=Counter(); n=G=0
    def add(p,q):return((p[0]+q[0])%c,(p[1]+q[1])%c)
    def scale(t,p):return(t*p[0]%c,t*p[1]%c)
    def tile(j,s,q,multiplicity):
        u=add(q,scale(-a,U[j]));w=add(q,scale(b,U[(j+s)%6]))
        for axis,p,coefficient in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
            rows[axis%3,p]+=coefficient*multiplicity
    for label,multiplicity in data['witness']:
        assert isinstance(multiplicity,int) and multiplicity>0
        kind,j,q=label; q=tuple(q)
        assert 0<=j<6 and all(0<=t<c for t in q)
        if kind=='inward':
            tile(j,-1,q,multiplicity)
            n+=multiplicity;G+=-(-1)**j*multiplicity
        else:
            assert kind=='outward_pair' and j<3
            mate=add(add(q,scale(-a,U[j])),scale(b,U[(j+1)%6]))
            tile(j,1,q,multiplicity);tile(j+3,1,mate,multiplicity)
            n+=2*multiplicity
    assert all(v==0 for v in rows.values())
    assert n==data['blocks']*c==data['population']
    assert G==c==data['signed_population']
    return {'tile':[a,b,c],'population':n,'G':G,
            'result':'exact integer residue witness; no geometric realization asserted'}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    folder=Path(__file__).resolve().parent
    print(json.dumps([check(folder/f'torus_{c}_3.json') for c in (7,37,43)],indent=2))
