#!/usr/bin/env python3
"""Exact compact six-tile patch: whole short current zero, boundary unfilled."""
from collections import Counter
import json
from pathlib import Path

from verify_charged_countercontrols import U,check

HERE=Path(__file__).resolve().parent


def verify(a,b,c):
    t=-a-b
    support=[(0,0,0,1),(0,0,2,-1),(0,0,2,1),
             (t,0,3,1),(t,0,5,-1),(t,0,5,1)]
    result=check(a,b,c,support)
    assert result['positive']==result['negative']==3
    full=Counter();vertices=[]
    for x,y,j,s in support:
        q=x,y;u=x-a*U[j][0],y-a*U[j][1]
        w=x+b*U[(j+s)%6][0],y+b*U[(j+s)%6][1]
        vertices.append([q,u,w])
        for ax,p,v in ((j,q,s),(j,u,-s),(j+s,w,s),(j+s,q,-s)):
            full[ax%3,*p]+=v
    assert not any(full.values())
    up=[0]*c;down=[0]*c
    down[(2*b*b)%c]+=1;down[(-b*b)%c]-=1
    assert result['up_currents']==up and result['down_currents']==down
    A=b*(2*a+b);B=a*(a+2*b)
    shift=150,100
    physical=[];margins=[]
    for poly in vertices:
        out=[]
        for x,y in poly:
            x+=shift[0];y+=shift[1]
            X=a*x-b*y;Y=b*x+(a+b)*y
            out.append([X,Y])
            margins.append((X,Y,c*A*B-B*X-A*Y))
        physical.append(out)
    contained=all(v>0 for row in margins for v in row)
    if c in (37,43):assert contained
    result.update({'normalized_support':[list(p) for p in support],
        'all_unreduced_short_endpoint_rows_zero':True,
        'mandatory_short_to_long_bank_segments':0,
        'gate_formula':'Q_up=0; Q_down=delta_(2b^2 mod c)-delta_(-b^2 mod c)',
        'height_one_containment':{'translation':list(shift),'rotation':'z=(a+b*rho)/c',
            'board_axial_vertices':[[0,0],[A,0],[0,B]],
            'physical_vertex_numerators':physical,'common_denominator':c,
            'minimum_integer_margins':[min(row[k] for row in margins) for k in range(3)],
            'strictly_contained':contained},
        'scope':'Rigid balanced six-tile patch, with its entire physical short current canceled internally. It passes short-to-long mandatory-bank feasibility vacuously. Its long boundary and complete phase-node gate compatibility are not filled or asserted.'})
    return result


def main():
    output={'status':'PASS','checks':[verify(*t) for t in ((5,3,7),(33,7,37),(35,13,43))],
        'conclusion':'Six balanced whole triangles can pass the full mandatory short-to-long bank test, including compact height-one placement inside both target boards.'}
    (HERE/'BALANCED_SIX_PATCH.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'PASS','shapes':[x['tile'] for x in output['checks']],
                      'full_short_current':'zero','mandatory_bank_segments':0,
                      'target_board_containment':'strict for c37 and c43'},indent=2))


if __name__=='__main__':main()
