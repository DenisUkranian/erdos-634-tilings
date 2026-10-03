#!/usr/bin/env python3
"""Reproduce the free-k construction's exact arithmetic and unit checks."""
import copy
import json
from math import gcd, isqrt
from pathlib import Path

from construct_free_k import choose_k, construct, construct_f2, semigroup_witness
from verify_f2 import verify as verify_f2
from verify_reversed import verify
from audit_free_k import run_campaign as audit_macrogeometry

ROOT = Path(__file__).resolve().parent


def belongs(n, a, b):
    """Independent finite membership check, without a modular inverse."""
    return n >= 0 and any(n >= j*a and (n-j*a) % b == 0
                         for j in range(b//gcd(a, b)))


def arithmetic_campaign():
    triples = []
    optimized_checks = 0
    uniform_checks = 0
    for a in range(2, 401):
        for b in range(1, a):
            if gcd(a, b) != 1:
                continue
            c = isqrt(a*a+a*b+b*b)
            if c*c != a*a+a*b+b*b:
                continue
            triples.append((a, b, c))
            for m in range(1, 13):
                k0 = (m*(a-b)+c-1)//c
                limit = m*b*c//(a*a)
                candidates = [k for k in range(k0, limit+1)
                              if belongs(m*b*c-a*a*k, a, b)]
                optimized = a*k0 <= b*(m*c//a)
                assert bool(candidates) == optimized
                try:
                    selected = choose_k(a, b, c, m)
                except ValueError:
                    assert not candidates
                else:
                    assert selected == candidates[0] == k0
                if m == 1:
                    assert not candidates
                if m == 2:
                    assert bool(candidates) == (a <= 2*b)
                if m == 3:
                    assert bool(candidates) == (3*c >= 4*a)
                optimized_checks += 1
            if 3*c >= 4*a:
                for m in range(2, 32):
                    v = m % 2
                    u = (m-3*v)//2
                    k = u+2*v
                    A = u*(2*b-a)+v*(4*b-2*a)
                    B = u*2*(c-a)+v*(3*c-4*a)
                    assert min(u, v, A, B) >= 0
                    assert k*c > m*(a-b)
                    assert m*b*c-a*a*k == A*a+B*b > 0
                    semigroup_witness(a, b, c, m, k)
                    uniform_checks += 1
    # Nonprimitive triples retain the direct criterion, not the primitive iff.
    assert choose_k(16, 14, 26, 1) == 1
    assert belongs(14*26-16*16, 16, 14)
    # Deliberate equality cases; independent geometry is checked separately.
    for a, b, c, m, k in ((5, 3, 7, 7, 2), (5, 3, 7, 25, 21)):
        semigroup_witness(a, b, c, m, k)
    assert 2*7 == 7*(5-3)
    assert 25*3*7-5*5*21 == 0
    return {'primitive_triples': len(triples),
            'optimized_criterion_instances': optimized_checks,
            'uniform_seed_closure_instances': uniform_checks,
            'bound_a': 400, 'criterion_multipliers': [1, 12],
            'uniform_multipliers': [2, 31],
            'primitive_m1_rejected': True,
            'primitive_m2_m3_domains_checked': True,
            'nonprimitive_m1_accepted': True}


def main():
    results = []
    for m in (2, 3):
        path = ROOT/'certificates'/f'f4_free_k_5_3_7_m{m}.json'
        frozen = json.loads(path.read_text())
        assert construct(5, 3, 7, m) == frozen
        assert frozen['semigroup_witness']['free_k'] == 1
        results.append(verify(frozen))
    # The independent unit verifier must reject an altered placement.
    bad = copy.deepcopy(json.loads(
        (ROOT/'certificates/f4_free_k_5_3_7_m2.json').read_text()))
    bad['triangles'][0][0][0] = '-1234567'
    try:
        verify(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Altered unit geometry accepted')
    arithmetic = arithmetic_campaign()
    macro_audit = audit_macrogeometry()
    f2_result = verify_f2(construct_f2(5, 3, 7, 2))
    rejected_parameters = []
    for name, args in (
            ('rectangle_too_short', (5, 3, 7, 4, 1)),
            ('negative_width', (5, 3, 7, 1, 1)),
            ('positive_width_semigroup_gap', (8, 7, 13, 1, 1))):
        try:
            construct(*args)
        except ValueError:
            rejected_parameters.append(name)
        else:
            raise AssertionError('Invalid free-k parameters accepted: '+name)
    report = {
        'status': 'PASS',
        'construction_domain': 'a>b>0; c²=a²+ab+b²; integer k>=1; '
                               'kc>=m(a-b); mbc-a²k in <a,b>',
        'uniform_theorem': 'a>b and 3c>=4a imply every m>=2 in F4, F2, and F3',
        'primitive_exact_construction_criterion':
            'a ceil(m(a-b)/c) <= b floor(mc/a)',
        'unit_certificate_checks': results,
        'F2_unit_bridge_check': f2_result,
        'arithmetic_campaign': arithmetic,
        'independent_macro_audit': macro_audit,
        'invalid_parameter_rejections': rejected_parameters,
        'altered_unit_geometry_rejected': True,
        'full_Erdos634_solved': False,
        'external_peer_review': False,
    }
    (ROOT/'free_k_verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
