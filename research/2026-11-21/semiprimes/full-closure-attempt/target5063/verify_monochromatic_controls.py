#!/usr/bin/env python3
"""Independent exact countercontrols; no target nonexistence is asserted."""
from collections import Counter
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def vertices(t,a,b):
    x,y,j,s=t
    return ((x,y),(x-a*U[j][0],y-a*U[j][1]),
            (x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]))

def disjoint(A,B):
    for P in (A,B):
        for u,v in zip(P,P[1:]+P[:1]):
            nx,ny=u[1]-v[1],v[0]-u[0]
            first=[nx*x+ny*y for x,y in A]
            second=[nx*x+ny*y for x,y in B]
            if max(first)<=min(second) or max(second)<=min(first):return True
    return False

def rows(support,a,b,c,cylinder):
    out=Counter()
    for x,y,j,s,m in support:
        q,u,w=vertices((x,y,j,s),a,b)
        for axis,p,value in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
            axis%=3
            if cylinder:
                key=(axis,(p[1],p[0],p[0]+p[1])[axis],(p[0] if axis==0 else p[1])%c)
            else:key=(axis,p[0]%c,p[1]%c)
            out[key]+=m*value
    return {k:v for k,v in out.items() if v}

def main():
    data=json.loads((HERE/'MONOCHROMATIC_COUNTERCONTROLS.json').read_text())
    replay={'status':'PASS','scope':data['scope'],'actual_controls':[]}
    for control in data['actual_monochromatic_cylinder_packings']:
        a,b,c=control['shape'];support=control['support'];assert a*a+a*b+b*b==c*c
        assert all(s*(-1)**j==1 for x,y,j,s in support)
        assert len({tuple(t)for t in support})==len(support)
        expanded=[[*t,1]for t in support]
        assert not rows(expanded,a,b,c,True)
        assert not rows(expanded,a,b,c,False)
        polys=[vertices(t,a,b)for t in support]
        assert all(disjoint(A,B)for i,A in enumerate(polys)for B in polys[:i])
        n=len(support);g=n//c;assert n==c*g and g==control['charge_units']
        in_semigroup=any(3*i+c*j==g for i in range(g+1)for j in range(g+1))
        replay['actual_controls'].append({'population':n,'charge':n,'charge_units':g,'all_actual_cylinder_rows_zero':True,'pair_checks':n*(n-1)//2,'n_less_than_c_squared':n<c*c,'charge_in_semigroup_3_c':in_semigroup})
    formal=data['signed_one_hand_kernel'];a,b,c=formal['shape'];support=formal['support']
    assert all(s==1 and j%2==0 for x,y,j,s,m in support)
    assert not rows(support,a,b,c,False)
    total=sum(t[-1]for t in support);negative=sum(t[-1]<0 for t in support)
    assert total==formal['target_population']==c and negative>0 and total%(c*c)
    replay['formal_one_hand']={'signed_population':total,'negative_coefficients':negative,'all_periodic_rows_zero':True,'population_not_divisible_by_c_squared':True}
    assert any(not x['charge_in_semigroup_3_c'] and x['n_less_than_c_squared']for x in replay['actual_controls'])
    (HERE/'MONOCHROMATIC_CONTROL_REPLAY.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(json.dumps(replay,indent=2))
if __name__=='__main__':main()
