#!/usr/bin/env python3
"""Independent pool accounting and small filter controls.

The full zero-survivor theorem must use the separate exhaustive replay.
This script audits saved pool integrity and compares the incremental
filter with independent Cartesian calculations on small controls.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from verify_profile_duals import brute_profiles, universe_counts


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def read_pool(path,c,d,cap):
    result={};maxP=2*c//d
    for text in path.read_text().splitlines():
        row=tuple(map(int,text.split()))
        assert len(row) in (maxP+3,maxP+5)
        native_up,native_down=row[:2]
        positive=[x for x in row[2:2+maxP] if x>=0]
        negative=row[2+maxP]
        assert row[2:2+maxP]==tuple(positive)+(-1,)*(maxP-len(positive))
        assert positive==sorted(positive)
        assert all(0<=x<2*(c-1) for x in positive)
        assert all(n*d<=cap for n in Counter(positive).values())
        assert negative==-1 or 0<=negative<2*(c-1) and negative not in positive
        P=len(positive);M=int(negative>=0)
        assert native_up+native_down+P-M==0
        qu=2*c+d*native_up;qd=-c+d*native_down
        assert -c<=qu<=cap and -c<=qd<=cap
        assert max(qu,0)+max(qd,0)+d*P<=2*c
        assert max(-qu,0)+max(-qd,0)+d*M<=c
        remote=[0]*(2*(c-1))
        for x in positive:remote[x]+=1
        if negative>=0:remote[negative]-=1
        key=(native_up,native_down,tuple(remote))
        assert key not in result
        if len(row)==maxP+5:assert row[-1]>0
        result[key]=row
    return result


def data(c,d,cap,cuts):
    lines=[f'{c} {d} {cap} {2*c//d} {c//d} {len(cuts)} 0']
    for D,up,down in cuts:lines.extend([str(D),' '.join(map(str,up)),' '.join(map(str,down))])
    return '\n'.join(lines)+'\n'


def small_controls(enumerator,filter_binary):
    c,d,cap=5,3,6
    first=(2,[3,-2,1,0,-3],[-1,3,-2,2,0])
    second=(1,[-2,0,3,1,-1],[2,-3,0,1,2])
    reports=[]
    with tempfile.TemporaryDirectory(prefix='erdos634-pool-audit-') as temp:
        base=Path(temp);previous=base/'initial.txt'
        run=subprocess.run([str(enumerator),str(previous)],input=data(c,d,cap,[]),capture_output=True,text=True,check=True)
        expected,visited,reserved=brute_profiles(c,d,cap,[])
        initial=read_pool(previous,c,d,cap)
        summary=json.loads(run.stdout.splitlines()[-1])
        assert set(initial)==expected and summary['cut_passed']==len(initial)
        assert summary['exhaustive'] and summary['visited']==visited and summary['reserve_passed']==reserved
        reports.append({'stage':'complete_initial_pool','profiles':len(initial),'status':'PASS'})
        for i,cut in enumerate((first,second)):
            following=base/f'next_{i}.txt'
            run=subprocess.run([str(filter_binary),str(previous),str(following)],input=data(c,d,cap,[cut]),capture_output=True,text=True,check=True)
            summary=json.loads(run.stdout.splitlines()[-1])
            current=read_pool(following,c,d,cap)
            expected,_,_=brute_profiles(c,d,cap,[first] if i==0 else [first,second])
            assert set(current)==expected
            assert summary['pool_input']==len(read_pool(previous,c,d,cap))
            assert summary['pool_survivors']==len(current)
            assert sum(summary['rejected'])+len(current)==summary['pool_input']
            reports.append({'stage':f'filter_{i}','profiles':len(current),'status':'PASS'})
            previous=following
        # Deliberately absurd stored lower bounds must affect candidate choice
        # only, never remove a profile without a newly checked cut.
        inflated=base/'inflated.txt';untouched=base/'untouched.txt'
        inflated.write_text(''.join(' '.join(map(str,row[:6]))+' 1000000000000 1\n' for row in current.values()))
        run=subprocess.run([str(filter_binary),str(inflated),str(untouched)],input=data(c,d,cap,[]),capture_output=True,text=True,check=True)
        assert set(read_pool(untouched,c,d,cap))==set(current)
        reports.append({'stage':'stored_bound_not_a_pruning_rule','profiles':len(current),'status':'PASS'})
    return reports


def trace(directory,initial_summary):
    meta=json.loads((directory/'metadata.json').read_text())
    history=json.loads((directory/'history.json').read_text())
    a,b,c=meta['tile'];d=a-b;cap=51 if c==43 else 44
    previous=Path(meta['initial_pool'])
    assert digest(previous)==meta['initial_pool_sha256']
    initial=read_pool(previous,c,d,cap)
    summary=json.loads(initial_summary.read_text().splitlines()[-1])
    universe=universe_counts((a,b,c))
    assert summary['exhaustive'] and summary['visited']==universe['visited']
    assert summary['reserve_passed']==universe['reserve_passed']
    assert summary['cut_passed']==len(initial)
    assert sum(summary['rejected'])+len(initial)==summary['reserve_passed']
    before=initial;stages=[]
    for i,record in enumerate(history):
        assert record['iteration']==i
        assert record['pool_input_sha256']==digest(previous)
        following=directory/f'pool_{i:03d}.txt'
        assert record['pool_output_sha256']==digest(following)
        after=read_pool(following,c,d,cap)
        assert set(after)<=set(before)
        stats=record['filter']
        assert stats['pool_input']==len(before) and stats['pool_survivors']==len(after)
        assert sum(stats['rejected'])+len(after)==len(before)
        expected=meta['initial_certificates'] if i==0 else [str(directory/f'certificate_{i-1:03d}.json')]
        assert record['new_certificates']==expected
        assert all(Path(path).exists() for path in expected)
        stages.append({'iteration':i,'input':len(before),'output':len(after),'input_sha256':digest(previous),'output_sha256':digest(following),'status':'PASS'})
        previous=following;before=after
    return {'initial_profiles':len(initial),'initial_pool_sha256':meta['initial_pool_sha256'],'last_profiles':len(before),'stages':stages,'scope':'Pool hashes, canonical membership, subset transitions and accounting only. Exact pruning arithmetic is covered by the separately checked cuts and final full enumeration.'}


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--initial-summary',type=Path,required=True)
    p.add_argument('--enumerator',type=Path,required=True)
    p.add_argument('--filter',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    ar=p.parse_args()
    result={'trace':trace(ar.directory,ar.initial_summary),'independent_small_controls':small_controls(ar.enumerator,ar.filter)}
    ar.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'initial_profiles':result['trace']['initial_profiles'],'last_profiles':result['trace']['last_profiles'],'transitions':len(result['trace']['stages']),'small_controls':result['independent_small_controls'],'status':'PASS'},indent=2))
