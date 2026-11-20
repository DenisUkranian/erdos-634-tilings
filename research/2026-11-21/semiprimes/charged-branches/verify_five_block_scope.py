#!/usr/bin/env python3
"""Exact arithmetic controls of the conditional five-odd-block scope note.

The finite height control is not the proof of the unrestricted bound;
occupied-parent and boundary-supplier arguments are proved in the note.
"""
from itertools import combinations
from fractions import Fraction
import json
from pathlib import Path


def check():
    sign_allocations=[]
    for p2 in range(3):
        m2=2-p2
        for p3 in range(4):
            m3=3-p3
            if p2+p3==3 and m2+m3==2:
                sign_allocations.append([[p2,m2],[p3,m3]])
    assert sign_allocations==[[[0,2],[3,0]],[[1,1],[2,1]],[[2,0],[1,2]]]
    rows=[]
    # |t-1|+|2-t|<=5 already gives -1<=t<=4 analytically.
    for t in range(-1,5):
        gd,ge=t-1,2-t
        for kd in (0,2,3,4,5):
            ke=5-kd
            if ke not in (0,2,3,4,5):continue
            if abs(gd)>kd or abs(ge)>ke or (kd-gd)%2 or (ke-ge)%2:continue
            if kd==0:
                assert t==1
                for c,d in ((37,26),(43,22)):
                    assert (c-d)%d!=0
                continue
            rows.append({'t':t,'odd_blocks':[kd,ke],'lower_sign_blocks':[(kd+gd)//2,(kd-gd)//2],'upper_sign_blocks':[(ke+ge)//2,(ke-ge)//2]})
    assert len(rows)==7
    assert {r['t'] for r in rows}==set(range(-1,5))
    allowed=[]
    odd_range=list(range(-9,12,2))
    for count in (1,2):
        for subset in combinations(odd_range,count):
            s=set(subset)
            if not s&{-1,1} or not s&{1,3}:continue
            if any(not set(range(3,h,2))<=s for h in s if h>=5):continue
            if any(not set(range(h+2,0,2))<=s for h in s if h<=-3):continue
            allowed.append(list(subset))
    assert sorted(allowed)==[[-1,1],[-1,3],[1],[1,3]]
    capacities=[]
    for cc,dd,Cp,D in ((37,26,43,222),(43,22,8,43)):
        upper=Fraction(2*cc*Cp,D)
        assert upper<dd
        capacities.append({'c':cc,'d':dd,'monochromatic_2c_parent_gate_capacity':str(upper),'positive_terminal_parent_current_minimum':dd,'strict_contradiction':True})
    final_allowed=[s for s in sorted(allowed) if s!=[-1,3]]
    assert final_allowed==[[-1,1],[1],[1,3]]
    a,b,c,N,K=35,13,43,5063,17
    d=a-b;t=(K-3)*c//2;m=(N-K*c-d)//2
    assert t==301 and m==2155
    core=(m,m+d);middle=((K-1)*c//2,(K+1)*c//2)
    assert core==(2155,2177) and middle==(344,387)
    assert sum(core)+sum(middle)==N
    assert core[0]-core[1]==-d and middle[0]-middle[1]==-c
    assert sum(middle)==731>=5*c
    assert (core[0]%c,core[1]%c)==(5,27)
    assert middle[0]%c==middle[1]%c==0
    return {'status':'PASS','scope':__doc__,'five_block_sign_totals':[3,2],'two_odd_node_sign_allocations':sign_allocations,'median_rows':rows,'finite_height_control':{'odd_test_range':[-9,11],'initial_odd_height_sets':sorted(allowed),'after_forcing_height_one':final_allowed,'unrestricted_proof':'See FIVE_BLOCK_SCOPE.md, Sections 2 and 4.'},'height_one_forcing_gate_bounds':capacities,'existing_5063_axis_inventory':{'K':K,'odd_population':K*c,'core_signs':list(core),'middle_signs':list(middle),'total':N,'geometric_tiling':False},'target_status':'OPEN'}


if __name__=='__main__':
    out=check();text=json.dumps(out,indent=2)+'\n'
    Path(__file__).with_name('FIVE_BLOCK_SCOPE_REPLAY.json').write_text(text)
    print(text)
