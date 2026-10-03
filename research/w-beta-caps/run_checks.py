"""Finite exact regressions accompanying, not replacing, PROOF.md."""
from copy import deepcopy
import argparse
import hashlib
import json
from math import gcd
from pathlib import Path

from check_symbolic import run as symbolic
from generate import cap,shell,generate,plan,strip_solution
from verify import check,check_expanded

ROOT=Path(__file__).resolve().parent


def run(output=None):
    summary=dict(symbolic=symbolic(),cap_checks=0,shell_checks=0,
                 complete_tiling_checks=0,macro_pairs=0,
                 arithmetic_scale_checks=0,strip_threshold_checks=0)
    def verified(data):
        result=check(data)
        summary['macro_pairs']+=result['checked_macro_pairs']
        return result
    for v in range(2,13):
        for u in range(1,v):
            if gcd(u,v)>1:continue
            verified(cap(u,v));summary['cap_checks']+=1
            for family in ['W','beta']:
                verified(shell(u,v,v-u,family));summary['shell_checks']+=1
            for T in range(1,v+2):
                try:strip_solution(u,v,T);possible=True
                except ValueError:possible=False
                assert possible==(T>=v-u),(u,v,T)
                summary['strip_threshold_checks']+=1
            for m in range(1,u*v+2*v+1):
                direct=any(m-v-i*u>=0 and (m-v-i*u)%v==0 for i in range(m//u+1))
                try:p=plan(u,v,m);possible=True
                except ValueError:possible=False
                assert possible==direct,(u,v,m)
                assert m<u*v-u+1 or possible
                if possible:
                    assert p['seed_scale']>=v and p['seed_scale']%v==0
                    assert p['seed_scale']+u*p['steps']==m and 0<=p['steps']<v
                summary['arithmetic_scale_checks']+=1
            if v<=8:
                for family in ['W','beta']:
                    for m in sorted(set([v,u*v-u+1,u*v-u+2])):
                        verified(generate(u,v,m,family))
                        summary['complete_tiling_checks']+=1
    cases=[('cap_u1_v2',cap(1,2)),('cap_u1_v3',cap(1,3)),
           ('cap_u2_v3',cap(2,3)),('W_u1_v2_m3',generate(1,2,3)),
           ('beta_u1_v2_m3',generate(1,2,3,'beta'))]
    expanded=[]
    for name,data in cases:
        expanded.append(dict(name=name,**check_expanded(data)))
    summary['expanded_unit_checks']=expanded
    examples=cases+[
        ('W_u2_v3_m5',generate(2,3,5)),
        ('beta_u2_v3_m5',generate(2,3,5,'beta')),
        ('W_u2_v5_m9',generate(2,5,9)),
        ('beta_u5_v7_m31',generate(5,7,31,'beta')),
        ('W_u6_v7_m37',generate(6,7,37)),
    ]
    examples_dir=ROOT/'examples'
    if output is None:examples_dir.mkdir(exist_ok=True)
    summary['examples']=[]
    for name,data in examples:
        result=verified(data)
        path=examples_dir/(name+'.json')
        if output is None:path.write_text(json.dumps(data,indent=2)+'\n')
        summary['examples'].append(dict(file=str(path.relative_to(ROOT)),**result))
    mutations=[]
    base=generate(2,3,5)
    changed=deepcopy(base);changed['tile_count']+=1;mutations.append(('tile_count',changed))
    changed=deepcopy(base);changed['blocks'][0]['n']+=1;mutations.append(('triangle_scale',changed))
    changed=deepcopy(base);changed['blocks'][3]['diagonal']='sum';mutations.append(('diagonal',changed))
    changed=deepcopy(base);changed['blocks'].pop();mutations.append(('missing_region',changed))
    changed=deepcopy(base);changed['blocks'].append(deepcopy(changed['blocks'][0]));mutations.append(('duplicate_region',changed))
    changed=deepcopy(base);changed['target'][1][0][0]+=1;mutations.append(('target_vertex',changed))
    changed=shell(2,3,3);changed['inner'][1][0][0]+=1;mutations.append(('inner_target',changed))
    changed=deepcopy(base);changed['blocks'][0]['vertices'][0][0][0]+=1;mutations.append(('macro_vertex',changed))
    summary['rejected_corruptions']=[]
    for name,data in mutations:
        try:check(data)
        except ValueError as error:summary['rejected_corruptions'].append(dict(name=name,reason=str(error)))
        else:raise AssertionError('Corruption accepted: '+name)
    summary['invalid_inputs_rejected']=0
    for args in [(0,2,2),(2,2,3),(2,4,4),(1,2,1),(2,3,4),(2,3,0)]:
        try:generate(*args)
        except ValueError:summary['invalid_inputs_rejected']+=1
        else:raise AssertionError('Invalid/unproved scale accepted: '+repr(args))
    summary.update(status='PASS',scope={
        'geometry':'All primitive u<v<=12 caps and minimal collars; complete targets for v<=8 at seed/tail/tail+1',
        'arithmetic':'Direct nonnegative semigroup enumeration for 1<=m<=uv+2v, all primitive u<v<=12',
        'unit_expansion':'Five small certificates, every unit triangle and pair checked',
        'universal_proof':'PROOF.md; finite regressions are not universal extrapolation',
        'necessity':'No claim for omitted scales or arbitrary tilings'})
    report_path=Path(output) if output is not None else ROOT/'verification.json'
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(summary,indent=2)+'\n')
    if output is None:
        files=sorted([p for p in ROOT.iterdir() if p.is_file() and p.suffix in ('.py','.md')]
                     +list(examples_dir.glob('*.json'))+[ROOT/'verification.json'])
        (ROOT/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+
            str(p.relative_to(ROOT))+'\n' for p in files))
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,
                        help='Write a fresh report here without rewriting package examples or manifest')
    args=parser.parse_args()
    report=run(args.output)
    print(json.dumps({k:v for k,v in report.items() if k not in ('symbolic','examples')},indent=2))
