#!/usr/bin/env python3
"""Finite independent implementation checks; universal claims need the proof."""
import argparse
import json
from pathlib import Path
import classify
import verify_22

if not __debug__:
    raise SystemExit('Use ordinary Python; optimization would disable checks.')


def as_tuple(w):
    if 'u' in w:
        return w['branch'],w['u'],w['v']
    return w['branch'],w['a'],w['b'],w['c']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    audit22=verify_22.check()
    assert json.loads(json.dumps(audit22))==json.loads(Path(__file__).with_name('verified22.json').read_text())
    forward=verify_22.independent_generation(5000)
    for D in range(1,5001):
        got={as_tuple(w) for w in classify.product_witnesses(D)}
        assert got==forward.get(D,set()),(D,got,forward.get(D,set()))
    # These old positive classes exercise norm reduction, the classical
    # exceptions, and the alpha tail. Bounds are sufficient, never minimal.
    examples={d:classify.tail(d) for d in [1,2,3,6,14,19,22,70,122]}
    for d in [1,2,3,6,14,19,70,122]:
        assert examples[d]['status']=='COFINITE_TAIL'
        assert examples[d]['sufficient_multiplier']>=1
    assert examples[14]['sufficient_multiplier']==5
    assert examples[22]['status']=='NOT_COFINITE'
    assert examples[70]['witness']['branch']=='alpha'
    primes=[q for q in range(3,45,2) if verify_22.prime(q)]
    for q in primes+[47]:
        assert classify.prime_power_ray(22,q)['status']=='EMPTY_RAY'
    for d in [1,2,3,6,14,19,70,122]:
        for q in [3,5,11]:
            result=classify.prime_power_ray(d,q)
            assert result['status']=='NONEMPTY_RAY'
            w=result['witness']; k=result['all_exponents_at_least']
            r=w['coefficient_exponent']
            assert k>=r and q**(k-r)>=classify.threshold(w)
    rejected=0
    for d,q in [(0,None),(4,None),(12,None),(22,2),(22,9),(22,1)]:
        try:
            classify.tail(d) if q is None else classify.prime_power_ray(d,q)
        except ValueError:
            rejected+=1
        else:
            raise AssertionError(('invalid input accepted',d,q))
    report=dict(status='PASS',product_coefficients_compared=5000,
                comparison='CLI divisor inversion versus separate forward conic/Group1 generation',
                kernel22_prime_power_coefficients_checked=len(audit22['cases']),
                kernel22_ray_implementation_primes=primes+[47],
                invalid_inputs_rejected=rejected,
                example_tail_status={str(d):v['status'] for d,v in examples.items()},
                scope='Exact finite arithmetic/code checks. Infinite conclusions use the written proof and its stated geometric inputs.',
                full_Erdos634_solved=False,external_peer_review=False)
    if args.report:
        args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
