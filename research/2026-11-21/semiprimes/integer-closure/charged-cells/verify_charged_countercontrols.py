#!/usr/bin/env python3
"""Exact countercontrols for overly broad charged-cell population bounds.

All endpoint and gate arithmetic uses integers. These are partial packings in
the plane, with no target-board containment or complete neighboring-bank
compatibility claimed.
"""
from collections import Counter
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def separated(A,B):
    # Invertible affine axial coordinates preserve convex separation.
    for polygon in (A,B):
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            nx,ny=p[1]-q[1],q[0]-p[0]
            x=[nx*t[0]+ny*t[1] for t in A]
            y=[nx*t[0]+ny*t[1] for t in B]
            if max(x)<=min(y) or max(y)<=min(x):return True
    return False


def check(a,b,c,support,all_pairs=True):
    assert a>b>0 and a*a+a*b+b*b==c*c
    cyl=Counter();tor=Counter();up=Counter();down=Counter();polys=[]
    plus=minus=0
    for x,y,j,s in support:
        u=x-a*U[j][0],y-a*U[j][1]
        w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
        polys.append([(x,y),u,w])
        eps=s*(-1)**j;plus+=eps==1;minus+=eps==-1
        if s>0:up[(a*u[1]-b*u[0])%c]+=eps
        else:down[(a*u[0]-b*u[1])%c]+=eps
        for ax,p,v in ((j,(x,y),s),(j,u,-s),(j+s,w,s),(j+s,(x,y),-s)):
            ax%=3
            transverse=(p[1],p[0],sum(p))[ax]
            longitudinal=p[0] if ax==0 else p[1]
            cyl[ax,transverse,longitudinal%c]+=v
            tor[ax,p[0]%c,p[1]%c]+=v
    assert not any(cyl.values()) and not any(tor.values())
    pairs=0
    if all_pairs:
        for i,A in enumerate(polys):
            for B in polys[:i]:
                assert separated(A,B),(i,pairs)
                pairs+=1
    return {'tile':[a,b,c],'population':len(support),'positive':plus,'negative':minus,
        'charge':plus-minus,'all_actual_cylinder_rows_zero':True,
        'all_periodic_rows_zero':True,'pairwise_separating_axis_checks':pairs,
        'up_currents':[up[r] for r in range(c)],
        'down_currents':[down[r] for r in range(c)]}


def unit_charge_small():
    orientations=[(0,1),(2,1),(4,1),(4,1),(5,1),(2,1),(2,1),
                  (4,-1),(4,1),(1,-1),(1,1),(2,1),(2,1)]
    # Every periodic endpoint row has one term of each sign. The following
    # anchor projections are equal on every forced actual supporting line.
    T,H,I,W,V,R,S=7,19,11,9,8,18,26
    q=[(0,0),(T,0),(0,T),(0,H),(I-W,W),(I,0),(H-V,V),
       (R,V),(R,H-R),(S,0),(S,H-S),(H,0),(T-W,W)]
    D=15
    assert D%7==1
    support=[(D*x,D*y,j,s) for (x,y),(j,s) in zip(q,orientations)]
    result=check(5,3,7,support)
    assert (result['population'],result['charge'])==(13,7)
    assert result['population']<3*abs(result['charge'])
    result.update({'support':[list(t) for t in support],
        'counterexample':'The unit-charge inequality n>=3c fails even for a finite nonoverlapping actual-cylinder packing at (5,3,7).',
        'scope':'Unbounded plane only; neither target-board containment nor gate compatibility is asserted.'})
    return result


def higher_charge(a,b,c):
    # One positive orientation in each a-by-a axial parallelogram. It occupies
    # x in [a(r-1),ar], y in [as,as+b]. Distinct parallelograms have disjoint
    # interiors; b<a. Thus this proves nonoverlap without O(c^4) pair checks.
    support=[(a*r,a*s,0,1) for r in range(c) for s in range(c)]
    result=check(a,b,c,support,all_pairs=False)
    assert result['positive']==c*c and result['negative']==0
    assert result['up_currents']==[c]*c and result['down_currents']==[0]*c
    result.update({'support_formula':'q=(a*r,a*s), 0<=r,s<c, (j,s)=(0,+1)',
        'nonoverlap_proof':'Each triangle lies in a distinct a-by-a axial parallelogram and has b<a; parallelogram interiors are pairwise disjoint.',
        'counterexample':'The unrestricted inequality n>=3|G| fails: n=G=c^2.',
        'scope':'Finite nonoverlapping actual-cylinder packing; no board containment or complete gate compatibility asserted.'})
    return result


def main():
    output={'status':'PASS','unit_charge_small':unit_charge_small(),
            'higher_charge_controls':[higher_charge(*t) for t in ((5,3,7),(33,7,37),(35,13,43))],
            'target_unit_charge_status':'Not settled by these countercontrols.'}
    (HERE/'CHARGED_COUNTERCONTROLS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('unit_charge_small','higher_charge_controls')},indent=2))
    print('unit-charge c=7: 13 tiles, charge7, 78 exact pair separation checks')
    print('higher-charge controls: c=7,37,43, n=G=c^2')


if __name__=='__main__':main()
