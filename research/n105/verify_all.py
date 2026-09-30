#!/usr/bin/env python3
"""Replay all packaged certificates and tests; do not treat code as a formal
verification of the cited classification and written geometric lemmas."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
if not __debug__:raise RuntimeError('Run without -O or PYTHONOPTIMIZE.')
HERE=Path(__file__).resolve().parent
TASKS=[('f1_8_7_13','replay_exact.py','f1_8_7_13.json',120),
       ('eq_5_19_21','replay_eq_5_19_21.py','eq_5_19_21.json',15),
       ('eq_7_13_15','replay_eq7.py','eq_7_13_15.json',1788),
       ('f1_5_16_19','replay_16.py','f1_5_16_19.json',120)]

def execute(task):
    name,program,cert,expected=task
    dest=HERE/'verification'/f'{name}.log'
    with dest.open('w') as output:
        p=subprocess.run([sys.executable,str(HERE/program),str(HERE/'data'/cert)],cwd=HERE,stdout=output,stderr=subprocess.STDOUT)
    if p.returncode:raise RuntimeError(f'{name}: checker failed, inspect {dest.name}')
    report=json.loads((HERE/'data'/(Path(cert).stem+'_replay.json')).read_text())
    count=len(report.get('certified_root_ids',report.get('accepted_roots',[])))
    # Baseline equilateral checkers use the same explicit list field.
    if count!=expected:raise ValueError(f'{name}: expected {expected}, got {count}; inspect report fields')
    if report.get('incomplete_root_ids'):raise ValueError(f'{name}: incomplete root')
    digest=hashlib.sha256((HERE/'data'/cert).read_bytes()).hexdigest()
    return {'case':name,'certified_roots':count,'expected_roots':expected,'proof_states_replayed':report['replayed_nodes'],
            'complete_fixed_target_exclusion':True,'certificate_sha256':digest,'report':report}

def main():
    p=argparse.ArgumentParser();p.add_argument('--jobs',type=int,default=2);args=p.parse_args()
    if not 1<=args.jobs<=4:p.error('--jobs must be between 1 and 4')
    (HERE/'verification').mkdir(exist_ok=True);start=time.monotonic()
    for script in ['check_arithmetic.py','selftest.py','tests/test_capped_chains.py','tests/test_new_checker_mutations.py']:
        with (HERE/'verification'/(Path(script).stem+'.log')).open('w') as f:
            result=subprocess.run([sys.executable,str(HERE/script)],cwd=HERE,stdout=f,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError(f'{script} failed')
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:rows=list(pool.map(execute,TASKS))
    arithmetic=json.loads((HERE/'verification/arithmetic.json').read_text())
    if arithmetic['remaining_fixed_target_count']!=4:raise ValueError('unexpected reduction')
    summary={'result':'ALL_PACKAGED_CHECKS_PASSED','date':'2026-09-30','cases':rows,
             'global_N105_exclusion':True,
             'global_claim_dependencies':'PROOF_N105.md, published shape classification/rationality, BASELINE_LEMMAS.md and all four finite certificates.',
             'human_and_published_theorems_formally_verified':False,
             'full_Erdos634_solved':False,'external_peer_review':False,
             'seconds':round(time.monotonic()-start,6)}
    (HERE/'VERIFIED_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))
    for r in rows:print(r['case'],r['certified_roots'],r['proof_states_replayed'])
if __name__=='__main__':main()
