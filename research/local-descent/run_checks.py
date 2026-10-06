#!/usr/bin/env python3
"""Reproduce local-descent certificates and independent regression controls.

Default execution is read-only. --report writes the exact JSON output.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import json
from math import gcd, isqrt
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import local_obstructions as L


def independent_squarefree(n: int) -> bool:
    return all(n % (p*p) for p in range(2, isqrt(n)+1))


def independent_covers(k: int) -> set[int]:
    n = 3*k
    divisors = set()
    for a in range(1, isqrt(n)+1):
        if n % a == 0:
            divisors.update((a, n//a))
    return {s*d for d in divisors if d % 2 == 0 and independent_squarefree(d)
            for s in (-1, 1)}


def audit_certificate(k: int, D: int, cert: dict) -> None:
    """Independent replay: direct residue sets, not the producer's symbols."""
    assert cert['excluded'] is True
    p = cert['prime']
    assert L.is_prime(p)
    method = cert['method']
    if method == 'primitive_projective_modulus':
        q = cert['modulus']
        assert q == p**cert['exponent']
        assert cert['checked_pairs'] == cert['charts_size'] == q+q//p
        squares = {z*z % q for z in range(q)}
        assert cert['square_residue_count'] == len(squares)
        # Independent full primitive-pair enumeration, not normalized charts.
        square2 = [u*u % q for u in range(q)]
        square4 = [u*u % q for u in square2]
        coefficient = -3*k*k//D
        for u in range(q):
            for v in range(q):
                if u % p == 0 and v % p == 0:
                    continue
                rhs = (D*square4[u]+6*k*square2[u]*square2[v]+coefficient*square4[v]) % q
                assert rhs not in squares
        return
    assert p > 3 and k % p == 0 and k % (p*p) != 0
    squares = {u*u % p for u in range(p)}
    if method == 'odd_prime_unit_classes':
        assert D % p and cert['modulus'] == p**3 and cert['exponent'] == 3
        assert cert['D_mod_p'] == D % p
        assert cert['minus3D_mod_p'] == -3*D % p
        assert cert['legendre_D'] == cert['legendre_minus3D'] == -1
        # Unit-u chart fails modulo p. In the other primitive chart, dividing
        # by p² gives the second nonsquare; this is a mod-p³ obstruction.
        assert D % p not in squares
        divided = (-3*(k//p)**2*pow(D, -1, p)) % p
        assert divided not in squares
        return
    assert method == 'odd_prime_divisor_quadratic'
    assert D % p == 0 and D % (p*p) != 0
    assert cert['modulus'] == p*p and cert['exponent'] == 2
    delta, kappa = D//p, k//p
    assert cert['delta_mod_p'] == delta % p
    assert cert['kappa_mod_p'] == kappa % p
    # Directly enumerate the divided bracket on P^1(F_p). This independently
    # checks the discriminant/Legendre test used to create the certificate.
    coefficient = -3*kappa*kappa*pow(delta, -1, p)
    for u, v in [(1, v) for v in range(p)]+[(0, 1)]:
        assert (delta*u**4+6*kappa*u*u*v*v+coefficient*v**4) % p != 0
    if cert['legendre_3'] == -1:
        assert 3 % p not in squares
    else:
        r = cert['sqrt3_mod_p']
        assert r*r % p == 3 % p
        assert cert['quadratic_roots'] == [(-3+2*r) % p, (-3-2*r) % p]
        denom = delta*kappa % p
        values = [t*pow(denom, -1, p) % p for t in cert['quadratic_roots']]
        assert cert['delta_kappa_mod_p'] == denom
        assert cert['required_square_residues'] == values
        assert cert['legendre_values'] == [-1, -1]
        assert all(value not in squares for value in values)


def audit_report(report: dict) -> int:
    k = report['k']
    rows = report['covers']
    assert len(rows) == report['cover_count']
    assert len({r['D'] for r in rows}) == len(rows)
    assert {r['D'] for r in rows} == independent_covers(k)
    killed = 0
    for row in rows:
        if row['status'] == 'KILLED':
            audit_certificate(k, row['D'], row['certificate'])
            killed += 1
        else:
            assert row['status'] == 'SURVIVES'
            assert all(t['excluded'] is False for t in row['necessary_tests'])
    survivors = sorted(r['D'] for r in rows if r['status'] == 'SURVIVES')
    assert report['survivors'] == survivors
    assert report['status'] == ('INCOMPLETE' if survivors else 'NO_ODD_F3')
    return killed


def double_point(k: int, x: int | Fraction, y: int | Fraction) -> tuple[Fraction, Fraction]:
    x, y = Fraction(x), Fraction(y)
    assert y*y == x**3+6*k*x*x-3*k*k*x and y != 0
    slope = (3*x*x+12*k*x-3*k*k)/(2*y)
    xx = slope*slope-6*k-2*x
    return xx, slope*(x-xx)-y


def verify() -> dict:
    reports: dict[int, dict] = {}
    def report(k: int) -> dict:
        if k not in reports:
            reports[k] = L.odd_f3_sieve(k)
        return reports[k]

    # Complete primitive cover controls, including ramification at 3 and
    # a negative squareclass. Every given solution must survive all stages.
    cover_points = [(2, 6, 1, 1, 4), (114, 6, 3, 1, 12),
                    (330, 22, 5, 1, 220), (330, -66, 3, 1, 132)]
    for k, D, u, v, Z in cover_points:
        assert gcd(u, v) == 1
        assert Z*Z == D*u**4+6*k*u*u*v*v-(3*k*k//D)*v**4
        assert report(k)['status'] == 'INCOMPLETE'
        assert D in report(k)['survivors']

    # In the p∤D rule one needs p³, not p², to see the second chart.
    assert not L.primitive_modular_test(14, -2, 7, 2)['excluded']
    assert L.primitive_modular_test(14, -2, 7, 3)['excluded']
    assert L.odd_prime_test(14, -2, 7)['excluded']

    # Seven genuine primitive positive F3 coefficients with odd multipliers.
    # The small bound generates controls only; no negative result uses it.
    positive_coefficients = []
    for a in range(1, 61):
        for b in range(1, 61):
            c = isqrt(a*a+a*b+b*b)
            if gcd(a, b) != 1 or c*c != a*a+a*b+b*b:
                continue
            coefficient = 3*(a+2*b)*(a+b)
            d = L.squarefree_kernel(coefficient)
            s = isqrt(coefficient//d)
            assert coefficient == d*s*s
            if d % 2 or s % 2 == 0:
                continue
            k = L.squarefree_kernel(3*d)
            assert report(k)['status'] == 'INCOMPLETE'
            positive_coefficients.append({'a': a, 'b': b, 'c': c, 'd': d,
                                          's': s, 'k': k, 'coefficient': coefficient})
    assert len(positive_coefficients) == 7

    expected_predicates = {13: False, 37: True, 61: False, 109: True,
                           157: True, 181: True, 229: True}
    predicates = []
    for p, expected in expected_predicates.items():
        result = L.prime_family_predicate(p)
        assert result['predicate'] == expected
        # Independent original root/Legendre formulation of the predicate.
        squares = {a*a % p for a in range(p)}
        roots = [r for r in range(p) if r*r % p == 3]
        assert len(roots) == 2
        original = [(((-3+2*r) % p in squares) != (5 % p in squares)) for r in roots]
        assert original == [expected, expected]
        predicates.append(result)

    R4 = 7*31*79*103
    family_inputs = [(6*7*31, 1), (6*7*79, 3), (6*R4, 5),
                     (30*37, 1), (30*109, 7), (30*157, 3),
                     (30*181, 1), (30*229, 1)]
    family_decisions = []
    for d, m in family_inputs:
        decision = L.classify_count(d, m)
        assert decision['status'] == 'NO'
        obstruction = decision.pop('F3_obstruction')
        assert obstruction == report(obstruction['k'])
        decision['F3_obstruction_reference_k'] = obstruction['k']
        family_decisions.append(decision)

    # Valid inputs outside either exact hypothesis must not become NO.
    scope_inputs = [(1302, 2), (1302, 8660), (1110, 2), (4710, 4),
                    (30*13, 1), (30*61, 1), (6, 1), (42, 1),
                    (38, 1), (22, 1), (1110*17, 1)]
    scope_controls = []
    for d, m in scope_inputs:
        decision = L.classify_count(d, m)
        assert decision['status'] == 'NOT_COVERED'
        scope_controls.append(decision)
    assert report(130)['status'] == report(610)['status'] == 'INCOMPLETE'

    # Positive-rank d4710 control: exact point and Nagell-Lutz certificate.
    k, x, y = 1570, -471, 73947
    assert y*y == x**3+6*k*x*x-3*k*k*x
    xx, yy = double_point(k, x, y)
    assert xx == Fraction(10609, 4)
    short_x = xx+2*k
    assert short_x == Fraction(23169, 4)
    assert short_x.denominator != 1
    assert yy*yy == short_x**3-15*k*k*short_x+22*k**3
    rank_control = {'d': 4710, 'k': k, 'point': [x, y],
                    'double_x': str(xx), 'short_model_double_x': str(short_x),
                    'short_model_coefficients': [-15*k*k, 22*k**3],
                    'nontorsion_reason': 'Nagell-Lutz: a multiple has nonintegral x on the integral short Weierstrass model.'}

    # An actual arithmetic coefficient in d1302, with EVEN multiplier.
    a, b, c, d, s = 159711, 13889, 167089, 1302, 8660
    assert gcd(a, b) == 1 and c*c == a*a+a*b+b*b
    assert 3*(a+2*b)*(a+b) == d*s*s and s % 2 == 0
    assert report(434)['status'] == 'NO_ODD_F3'
    assert L.classify_count(d, s)['status'] == 'NOT_COVERED'
    assert 51960**2 == (-1200)**3+6*434*(-1200)**2-3*434**2*(-1200)
    even_control = {'d': d, 'k': 434, 'a': a, 'b': b, 'c': c, 's': s,
                    'coefficient': d*s*s, 'curve_point': [-1200, 51960],
                    'scope': 'Primitive F3 coefficient witness; small-scale geometric realization is not asserted.'}

    invalid = [lambda: L.odd_f3_sieve(0), lambda: L.odd_f3_sieve(-2),
               lambda: L.odd_f3_sieve(3), lambda: L.odd_f3_sieve(18),
               lambda: L.odd_f3_sieve(True), lambda: L.odd_f3_sieve(Fraction(2)),
               lambda: L.classify_count(12, 1), lambda: L.classify_count(0, 1),
               lambda: L.classify_count(1110, 0), lambda: L.classify_count(1110, True),
               lambda: L.prime_family_predicate(25), lambda: L.prime_family_predicate(7),
               lambda: L.primitive_modular_test(14, 4, 2, 7),
               lambda: L.primitive_modular_test(14, 10, 2, 7),
               lambda: L.primitive_modular_test(14, -2, 4, 2),
               lambda: L.odd_prime_test(14, -2, 3)]
    for call in invalid:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input was accepted')

    # Independently replay EVERY retained killing certificate and complete
    # signed-cover universe, including all generated positive controls.
    killed = sum(audit_report(r) for r in reports.values())
    mutation = deepcopy(report(434))
    mutation['covers'].pop()
    try:
        audit_report(mutation)
    except AssertionError:
        pass
    else:
        raise AssertionError('incomplete cover certificate was accepted')
    mutation = deepcopy(report(434))
    row = next(r for r in mutation['covers'] if r['certificate']['method'] == 'primitive_projective_modulus')
    row['certificate']['checked_pairs'] += 1
    try:
        audit_report(mutation)
    except AssertionError:
        pass
    else:
        raise AssertionError('corrupted modular certificate was accepted')

    return {'status': 'PASS', 'full_Erdos634_solved': False,
            'general_rank_algorithm': False, 'Mordell_Weil_bases_computed': False,
            'summary': {'sieve_kernels': len(reports), 'killing_certificates_replayed': killed,
                        'primitive_cover_points': len(cover_points),
                        'genuine_positive_odd_F3_coefficients': len(positive_coefficients),
                        'family_count_exclusions': len(family_decisions),
                        'scope_controls': len(scope_controls), 'invalid_inputs_rejected': len(invalid),
                        'corrupted_certificates_rejected': 2},
            'cover_point_controls': [dict(zip(('k', 'D', 'u', 'v', 'Z'), row)) for row in cover_points],
            'positive_odd_F3_coefficients': positive_coefficients,
            'prime_predicate_controls': predicates, 'family_decisions': family_decisions,
            'scope_controls': scope_controls, 'positive_rank_control_4710': rank_control,
            'even_coefficient_control_1302': even_control,
            'sieve_certificates': {str(k): reports[k] for k in sorted(reports)},
            'boundary': 'Local survivors are INCOMPLETE. NO count decisions use both proved family hypotheses and exhaustive classification inputs. Even multipliers are NOT_COVERED.'}


def main() -> None:
    if not __debug__:
        raise SystemExit('Run without Python -O: assertions are part of verification.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = verify()
    data = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.report:
        args.report.write_text(data, encoding='utf-8')
    print(data, end='')


if __name__ == '__main__':
    main()
