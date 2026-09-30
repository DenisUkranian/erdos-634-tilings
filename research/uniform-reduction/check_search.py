#!/usr/bin/env python3
"""Positive, T-junction, mutation and limit controls for the fresh search.

Completeness is proved in PROOF.md, not inferred from these examples.
"""
from fractions import Fraction as F
from dataclasses import asdict
from pathlib import Path
from random import Random
from copy import deepcopy
from hashlib import sha256
import json,time
from candidates import Instance, enumerate_candidates
from exact_search import Search,triangle,atomic_boundary,convex_sectors,placements,encode_tri
from verify_positive import check

def require(x,msg):
    if not x:raise ValueError(msg)

def main():
    here=Path(__file__).resolve().parent;start=time.monotonic()
    controls=json.loads((here/'search_controls.json').read_text())
    fresh=[]
    for x in controls:
        if x['status']!='TILING_FOUND':continue
        i=x['instance']
        obj=Instance(i['branch'],tuple(i['tile']),tuple(i['target']),i['n'],tuple(i['parameters']),i['multiplier'])
        r=Search(obj,max_nodes=10000,seconds=5).run()
        require(r['status']=='TILING_FOUND',('Positive search failed',obj))
        fresh.append(r)
    positives=[check(x) for x in fresh]
    negatives=[]
    for n in (7,11,14,15,21):
        cs=enumerate_candidates(n)
        require(len(cs)==1,('Control needs unique candidate',n))
        r=Search(cs[0],max_nodes=20000,seconds=8).run()
        require(r['status']=='EXHAUSTED',('Unfinished control',n))
        negatives.append({'n':n,'branch':cs[0].branch,'nodes':r['nodes'],'status':r['status']})
    (here/'fresh_search_samples.json').write_text(json.dumps(fresh,indent=2)+'\n')
    require(len(positives)==18,'Expected 18 subdivision controls')
    sample=json.loads((here/'positive75.json').read_text())
    result75=check(sample)
    require(result75['t_junction_vertices']>0,'Not a T-junction control')
    parse=lambda tr:triangle(tuple(tuple(F(x) for x in p) for p in tr))
    tiles=[parse(t) for t in sample['tile_coordinates']]
    outer=parse(sample['target_coordinates']);D=sample['field_D']
    instance=Instance('theta-positive',(2,3,4),(30,30,15),75,(1,2),5)
    template=Search(instance).template
    rng=Random(6342026)
    indices=[set(range(k)) for k in (0,1,2,7,13,25,50,74)]
    indices.extend(set(rng.sample(range(75),k)) for k in (2,7,20,40,65) for _ in range(2))
    corner_checks=0;maximum_candidates=0;branch_vertices=0
    for ids in indices:
        placed=tuple(t for i,t in enumerate(tiles) if i in ids)
        remaining=set(t for i,t in enumerate(tiles) if i not in ids)
        B=atomic_boundary(outer,placed)
        degree={}
        for a,b in B:
            degree[a]=degree.get(a,0)+1;degree[b]=degree.get(b,0)+1
        branch_vertices+=sum(d>2 for d in degree.values())
        sectors=convex_sectors(B,D)
        require(sectors,'No convex sector in a known completion')
        for sec in sectors:
            ps=set(placements(template,sec,outer,placed,D))
            require(ps&remaining,('Lost true completing tile',ids,sec))
            corner_checks+=1;maximum_candidates=max(maximum_candidates,len(ps))
    mutations=[]
    for name in ('missing_tile','duplicate_tile','altered_coordinate','wrong_target','wrong_count'):
        m=deepcopy(sample)
        if name=='missing_tile':m['tile_coordinates'].pop()
        if name=='duplicate_tile':m['tile_coordinates'][1]=m['tile_coordinates'][0]
        if name=='altered_coordinate':m['tile_coordinates'][0][0][0]='1/17'
        if name=='wrong_target':m['instance']['target'][0]+=1
        if name=='wrong_count':m['instance']['n']+=1
        try:check(m)
        except ValueError:mutations.append(name)
        else:raise ValueError(('Bad certificate accepted',name))
    I=Instance('budget-control',(2,3,4),(4,6,8),4,(),2)
    for budget in (0,1):require(Search(I,max_nodes=budget).run()['status']=='INCOMPLETE',('node limit',budget))
    require(Search(I,seconds=0).run()['status']=='INCOMPLETE','time limit')
    require(Search(I).run()['status']=='TILING_FOUND','unlimited control')
    report={'status':'PASS','positive_subdivisions':positives,'positive75':result75,'negative_execution_controls':negatives,
            'known_completion_subsets':len(indices),'corner_completeness_checks':corner_checks,
            'maximum_placements_at_checked_corner':maximum_candidates,'branch_vertices_encountered':branch_vertices,
            'positive75_sha256':sha256((here/'positive75.json').read_bytes()).hexdigest(),
            'mutations_rejected':mutations,'budget_stops':'INCOMPLETE, not EXHAUSTED',
            'negative_controls_note':'Search-run EXHAUSTED records are not independently replayed proof-tree certificates.',
            'seconds':round(time.monotonic()-start,4)}
    (here/'search_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
