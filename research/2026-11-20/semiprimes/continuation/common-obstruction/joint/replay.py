#!/usr/bin/env python3
"""Exact joint-cell and native-gate controls; never decides either target."""
from pathlib import Path
import argparse,hashlib,json,os,sys
from verify_joint_cells import check as joint_check
from verify_native_torus import check_dual,check_known_143
HERE=Path(__file__).resolve().parent

def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise SystemExit('Run Python with assertions enabled.')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--continuation-dir',type=Path,default=HERE.parent.parent)
    p.add_argument('--coupled-control',action='store_true')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    results={'joint_cells_143':joint_check(args.continuation_dir),
             'native_projection_143':check_known_143(args.continuation_dir)}
    for n in('3431','5063'):
        case=json.loads((HERE/('torus'+n)/'exact_dual.json').read_text())
        result=check_dual(case)
        assert result==case['verified_bound']
        results['native_dual_'+n]=result
    if args.coupled_control:
        from check_coupled_143 import check as coupled_check
        results['coupled_projection_143']=coupled_check(args.continuation_dir)
    sources=list(HERE.glob('*.py'))+[HERE/'torus3431/exact_dual.json',HERE/'torus5063/exact_dual.json']
    report={'format':'joint-phase-controls-v1','status':'PASS','checks':results,
            'source_sha256':{str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted(sources)},
            'target_status':{'3431':'OPEN','5063':'OPEN'},
            'scope':'Exact controls and necessary bounds. Native15c/17c require the stated two-height and native-mesh hypotheses; no nonexistence certificate.'}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
