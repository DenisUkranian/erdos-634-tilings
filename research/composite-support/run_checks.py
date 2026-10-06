#!/usr/bin/env python3
"""Independent finite arithmetic checks; not an S-unit or geometric solver."""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import allocate
import check_quartics
import classify22
import verify_rank22

if not __debug__:
    raise SystemExit('Run this verifier without Python optimization (-O).')

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_coefficients',
        HERE.parent/'square-class-tails'/'verify_22.py')
independent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(independent)


def key(w):
    return ((w['branch'],w['u'],w['v']) if 'u' in w else
            (w['branch'],w['a'],w['b'],w['c']))


def check():
    generated = independent.independent_generation(5000)
    for D in range(1,5001):
        actual = {key(w) for w in allocate.allocated_witnesses(D,allocate.tails.factor(D))}
        assert actual == generated.get(D,set()),D
    unknown = allocate.classify(110,3)
    assert unknown['status']=='UNKNOWN' and unknown['witnesses']
    for w in unknown['witnesses']:
        assert w['coefficient']*w['t']**2==unknown['N']
        assert w['s']*w['t']==3
    old = allocate.classify(22,248599631)
    assert old['status']=='YES'
    w = old['positive_witness']
    assert (w['branch'],w['u'],w['v'],w['t'])==('QP',10132,22779,1)
    assert w['allocation']==[2*(7*3089)**2,11*11497**2]
    assert allocate.classify(22,21)['status']=='NO'
    assert allocate.classify(22,27)['status']=='NO'
    bad = [(1,1),(22,0),(22,2),(44,3),(14,3),(22,-1)]
    for d,m in bad:
        try:
            allocate.classify(d,m)
        except ValueError:
            pass
        else:
            raise AssertionError(('bad input accepted',d,m))
    cli = subprocess.run([sys.executable,str(HERE/'allocate.py'),'110','3'],
                         text=True,capture_output=True,check=True)
    assert json.loads(cli.stdout)==unknown
    # All square divisors, including primes shared by d and m, are covered.
    comparisons=0
    for d in (22,30,38,46,66,78,110):
        if allocate.tails.tail(d)['status']!='NOT_COFINITE':
            continue
        for m in (1,3,5,9,11,15,21,33):
            actual=allocate.classify(d,m)
            expected=set()
            for s in allocate.tails.divisors(m):
                expected.update((s,*z) for z in independent.inverse(d*s*s))
            assert {(w['s'],*key(w)) for w in actual['witnesses']}==expected,(d,m)
            comparisons+=1
    quartic = check_quartics.verify()
    rank = verify_rank22.verify()
    assert rank['status']=='PASS' and rank['positive'] is True
    # Independent coefficient enumeration tests the exact class-22 interface.
    for m in range(1,102,2):
        result=classify22.classify(m)
        candidates=allocate.classify(22,m)
        qp=[w for w in candidates['witnesses'] if w['branch']=='QP']
        assert all(w['branch']=='QP' for w in candidates['witnesses'])
        assert (result['status']=='YES')==bool(qp)
    for m in (2,4,6,100):
        result=classify22.classify(m)
        assert result['status']=='YES' and result['witness']['t']==m//2
    for m in (248599631,3*248599631):
        result=classify22.classify(m)
        assert result['status']=='YES' and result['witness']['branch']=='QP'
        w=result['witness']
        assert w['Q']*w['P']*w['t']**2==22*m*m
    for m in (0,-1):
        try:
            classify22.classify(m)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid class-22 input accepted')
    # Fresh replay of the already published 88-tile positive certificate.
    modules=[]
    for name in ('construct','verify'):
        path=HERE.parent/'group2-f4'/f'{name}.py'
        sp=importlib.util.spec_from_file_location(f'old_f4_{name}',path)
        mod=importlib.util.module_from_spec(sp)
        sp.loader.exec_module(mod)
        modules.append(mod)
    old88=modules[1].verify(modules[0].construct(3,5,7,1))
    return dict(status='PASS',coefficient_crosscheck=[1,5000],
                comparison_method='independent complete forward conic and Group-1 enumeration',
                composite_divisor_crosschecks=comparisons,invalid_inputs_rejected=len(bad),
                scoped_status_examples={'NO':[22,21],'UNKNOWN':[110,3],
                                       'YES_old_witness':[22,248599631]},
                quartic_check=quartic,
                rank22_check=rank,
                exact_class22_odd_small_regressions=51,
                exact_class22_even_regressions=4,
                exact_class22_old_positive_and_odd_refinement_regressions=2,
                old_88_tiling_replayed=old88,
                fixed_support_S_unit_solver_executed=False,
                new_geometric_tiling_search_executed=False,full_Erdos634_solved=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    report=check()
    if args.report:
        args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
