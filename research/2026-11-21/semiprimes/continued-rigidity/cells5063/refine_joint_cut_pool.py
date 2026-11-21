#!/usr/bin/env python3
"""Numerical adaptive exploration; only exported, replayed duals are exact claims."""
import argparse
import importlib.util
import hashlib
import json
import os
from pathlib import Path
from probe_joint_gate_cuts import run
from discover_cell_cut import discover, discover_full

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
spec=importlib.util.spec_from_file_location('independent_dual_checker',ROOT/'research/2026-11-21/semiprimes/audit/verify_profile_duals.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rounds',type=int,default=8)
    p.add_argument('--kind',choices=('two','four'),default='two')
    p.add_argument('--x',type=int,default=21)
    p.add_argument('--native-row',type=int,default=0)
    p.add_argument('--native-col',type=int,default=0)
    p.add_argument('--free-charges',action='store_true')
    p.add_argument('--master-seconds',type=float,default=45)
    p.add_argument('--tag',default='adaptive')
    p.add_argument('--full-oracle-seconds',type=float,default=60)
    ar=p.parse_args();history=[]
    destination_dir=HERE/ar.tag
    destination_dir.mkdir(exist_ok=True)
    for round in range(ar.rounds):
        result=run(ar.kind,ar.x,ar.native_row,ar.native_col,ar.master_seconds,not ar.free_charges)
        (destination_dir/f'master_{round:03d}.json').write_text(json.dumps(result,indent=2)+'\n')
        item={'round':round,'master_trace':result['trace'],'new_duals':[]}
        history.append(item)
        w=result['finite_pool_witness']
        if w is None:
            item['stop']='No master witness; numerical status only.'
            break
        for h,(cell,q) in enumerate(zip(result['cells'],w['cell_currents'])):
            candidate=discover(q,20)
            if ('D' not in candidate or
                candidate['lower_numerator']<=sum(cell[2:])*candidate['D']):
                candidate=discover_full(q,ar.full_oracle_seconds)
                (destination_dir/f'full_cell_{round:03d}_{h}.json').write_text(json.dumps(candidate,indent=2)+'\n')
            item.setdefault('cell_minima',[]).append({k:v for k,v in candidate.items()
                if k not in ('endpoint_tables','up_weights','down_weights','cell_gate_currents','floating_support')})
            if 'D' not in candidate:continue
            if candidate['lower_numerator']<=sum(cell[2:])*candidate['D']:continue
            mathematical={key:candidate[key] for key in ('tile','D','endpoint_tables','up_weights','down_weights')}
            candidate.pop('floating_support',None)
            digest=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()[:16]
            destination=HERE/f'shared_profile_cut_{digest}.json'
            if not destination.exists():
                temporary=destination.with_name(destination.name+f'.tmp-{os.getpid()}')
                temporary.write_text(json.dumps(candidate,indent=2)+'\n')
                temporary.replace(destination)
            checked,_=audit.verify(destination)
            checked['recorded_profile_excluded_population']=sum(cell[2:])
            item['new_duals'].append(checked)
        (destination_dir/'DISCOVERY_LOG.json').write_text(json.dumps(history,indent=2)+'\n')
        print(json.dumps(item),flush=True)
        if not item['new_duals']:
            item['stop']='No new certified cut from marginal/full-endpoint probes; inspect individual optimizer statuses. No tiling witness asserted.'
            break
    (destination_dir/'DISCOVERY_LOG.json').write_text(json.dumps(history,indent=2)+'\n')


if __name__=='__main__':main()
