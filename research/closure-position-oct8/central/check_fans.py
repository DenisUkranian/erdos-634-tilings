#!/usr/bin/env python3
"""Independent angle-word counts verify completeness of exact ray templates."""
import json
from collections import Counter
import fan_probe as fp
# angle names at left/right ends of each of the six base tile types.
ENDS=(('g','b'),('b','g'),('g','a'),('a','g'),('b','a'),('a','b'))

def expected(a,b):
    pair=Counter((ENDS[a][1],ENDS[b][0]))
    if pair['g']==2:return {1:0,4:0}
    if pair['g']==1:return {1:2,4:0}
    if pair['a']==1 and pair['b']==1:return {1:2,4:96}
    return {1:0,4:64}

def run():
    checks=[]
    for a in range(6):
      for b in range(6):
        fs=fp.fans(a,b);counts=Counter(map(len,fs));want=expected(a,b)
        assert all(counts[k]==v for k,v in want.items())
        assert sum(counts.values())==sum(want.values())
        assert len(fs)==len(set(fs))
        assert all(-3<=h<=3 for fan in fs for h,i in fan)
        checks.append({'base_pair':[a,b],'one_extra_tile_fans':counts[1],'four_extra_tile_fans':counts[4]})
    return {'status':'PASS','all_36_base_pairs_match_independent_angle_word_counts':True,'actual_fan_height_range':[-3,3],'checks':checks,'N154_solved':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
