"""Exact finite regression for NORM_GEOMETRIC_REMAINDER.md.

Counts subthreshold representations, not non-tilable integers.  The
asymptotic result is a written proof; this enumeration checks its inputs.
"""
import argparse
from collections import Counter
from math import gcd, isqrt
import json
from pathlib import Path


if not __debug__:
    raise SystemExit("Run without -O: this verifier requires assertions.")


def plus_tiles(bound):
    # ab >= k^3 delta/27 >= k^3/27.
    k = 3
    while k**3 <= 27*bound:
        for h in range(k//2+1, k):
            if gcd(h,k) != 1:
                continue
            ar,br,cr = k*k-h*h, k*(2*h-k), h*h-h*k+k*k
            g=gcd(ar,br)
            assert g in (1,3) and cr%g == 0
            a,b,c=ar//g,br//g,cr//g
            assert c*c == a*a+a*b+b*b and gcd(a,b)==1
            delta=min(k-h,2*h-k)
            assert max(a,b)*delta <= k*min(a,b)
            assert 27*a*b >= k**3*delta
            if a*b <= bound:
                yield a,b,c,k,delta
        k+=1


def count(bound):
    records=Counter()
    distinct=set()
    tiles=0
    def add(row,D,T,k,delta):
        for t in range(1,min(T-1,isqrt(bound//D))+1):
            assert delta*t < 9*k
            assert delta*t*t*k**3 <= 27*bound
            records[row]+=1
            distinct.add(D*t*t)
    for a,b,c,k,delta in plus_tiles(bound):
        tiles+=1
        M=3*(max(a,b)//min(a,b)+2)
        for row,D,T in (
            ('E120',a*b,M),
            ('F1',b*(a+b),M),
            ('I120',b*(a+2*b),M),
            ('F2',(a+2*b)*(2*a+b),(M+1)//2),
            ('F3',3*(a+2*b)*(a+b),(M+1)//2),
            ('F4',(2*a+b)*(a+b),M),
        ):
            add(row,D,T,k,delta)
        # Both minus-norm orders have the same D and threshold.
        aa,bb=a+b,b
        assert c*c == aa*aa-aa*bb+bb*bb
        T=3*(aa//bb+1)
        for _ in range(2):
            add('E60',aa*bb,T,k,delta)
    return {'X':bound,'primitive_plus_pairs':tiles,
            'subthreshold_representations':sum(records.values()),
            'distinct_subthreshold_counts':len(distinct),
            'representations_by_row':dict(sorted(records.items()))}


def direct_parameter_check(side_bound=200):
    # Independent direct norm-square search versus parametrization.
    direct={(a,b,isqrt(a*a+a*b+b*b))
            for a in range(1,side_bound+1)
            for b in range(1,side_bound+1)
            if gcd(a,b)==1 and isqrt(a*a+a*b+b*b)**2==a*a+a*b+b*b}
    param={(a,b,c) for a,b,c,_,_ in plus_tiles(side_bound**2)
           if a<=side_bound and b<=side_bound}
    assert direct==param
    return {'side_bound':side_bound,'ordered_triples':len(direct),'passed':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path,
                        help='also write the JSON report to this path')
    args = parser.parse_args()
    report = {
        'status': 'PASS',
        'full_solution': False,
        'full_Erdos634_solved': False,
        'scope': 'Subthreshold candidates, not nonexistence decisions',
        'parameter_regression': direct_parameter_check(),
        'counts': [count(10**j) for j in range(3,8)],
    }
    output = json.dumps(report, indent=2) + '\n'
    if args.report is not None:
        args.report.write_text(output, encoding='utf-8')
    print(output, end='')


if __name__=='__main__':
    main()
