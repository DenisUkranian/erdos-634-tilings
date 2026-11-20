#!/usr/bin/env python3
"""Arithmetic controls for necessary charged-leaf/parent population bounds.

No positive tiling or geometric completion is asserted by this script.
"""
import argparse
import json
from pathlib import Path


def ceildiv(a,b):
    return -((-a)//b)


def ordinary_parent_blocks(c,d,rp,rn,z):
    lp,ln=ceildiv(d*rp,c),ceildiv(d*rn,c)
    return z+2*max(ln,lp-z,ceildiv(2-z,2))


def even_reserve(c,d,rp,rn,positive_children,negative_children):
    delta=(d+rp-rn)//c
    assert c*delta==d+rp-rn
    x=max(0,-delta,ceildiv(d*positive_children-rp,c),
          ceildiv(d*negative_children-rn,c)-delta)
    y=x+delta
    ep,en=rp+c*x,rn+c*y
    assert ep-en==-d
    assert ep>=d*positive_children and en>=d*negative_children
    return ep,en


def check_target(N,a,b,c,rp,rn,expected):
    d=a-b
    A,B=b*(2*a+b),a*(a+2*b)
    assert c*c==a*a+a*b+b*b
    assert N==(a+2*b)*(2*a+b)
    assert A*B==a*b*N
    # The angle at the origin is 60 degrees. For the other two
    # angles, the law of cosines gives cosines > -1/2 exactly when
    # the following integer expressions are positive.
    assert A*A+c**4+A*c*c-B*B>0
    assert B*B+c**4+B*c*c-A*A>0
    baseline=even_reserve(c,d,rp,rn,0,0)
    positive=even_reserve(c,d,rp,rn,1,0)
    negative=even_reserve(c,d,rp,rn,0,1)
    assert sum(positive)==sum(baseline)+2*c
    assert negative==baseline
    rows=[]
    for sign,even,odd_out in ((1,positive,4*c),(-1,negative,2*c)):
        leaf_plus=(3*c+sign*c)//2
        leaf_minus=(3*c-sign*c)//2
        outside_charge=-c-sign*c
        outside_plus=c
        outside_minus=outside_plus-outside_charge
        assert outside_plus+outside_minus==odd_out
        assert leaf_plus-leaf_minus==sign*c
        assert leaf_plus+outside_plus-leaf_minus-outside_minus==-c
        total=3*c+odd_out+sum(even)
        assert total==expected[sign]
        rows.append({'leaf_sign':sign,'leaf_minimum':3*c,
                     'leaf_sign_inventory':[leaf_plus,leaf_minus],
                     'outside_odd_minimum':odd_out,
                     'outside_odd_sign_inventory':[outside_plus,outside_minus],
                     'even_sign_minimum':list(even),'even_minimum':sum(even),
                     'total_minimum':total})
    controls=0
    for positive_children in range(6):
        for negative_children in range(6):
            if positive_children+negative_children==0:
                continue
            for charge_blocks in range(-6,7):
                got=ordinary_parent_blocks(c,d,positive_children,
                                           negative_children,charge_blocks)
                feasible=[x+y for x in range(30) for y in range(30)
                          if c*x>=d*positive_children
                          and c*y>=d*negative_children
                          and x-y==charge_blocks and x+y>=2]
                assert feasible and got==min(feasible)
                controls+=1
    assert controls==455
    return {'N':N,'tile':[a,b,c],'d':d,'core_residues':[rp,rn],
            'baseline_even_sign_inventory':list(baseline),
            'baseline_even_population':sum(baseline),
            'unit_core_attached_leaves':rows,
            'ordinary_parent_formula_controls':controls}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    report={
        'scope':'Necessary arithmetic costs of actual terminal leaves and their parents; neither target is decided.',
        'targets':[
            check_target(3431,33,7,37,19,8,{1:397,-1:249}),
            check_target(5063,35,13,43,5,27,{1:419,-1:247}),
        ],
        'ordinary_parent_control_range':{
            'positive_children':[0,5],'negative_children':[0,5],
            'at_least_one_child':True,'parent_charge_blocks':[-6,6],
            'enumerated_positive_and_negative_blocks':[0,29],
            'method':'Direct integer enumeration against the closed formula; not a geometric search.',
        },
        'checks':'PASS',
    }
    data=json.dumps(report,indent=2)+'\n'
    if args.out:
        args.out.write_text(data)
    print(data,end='')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
