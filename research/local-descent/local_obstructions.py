#!/usr/bin/env python3
"""Certified necessary local-cover obstructions for odd F3 multipliers.

The generic API accepts even positive squarefree k and tests every signed
even squarefree D supported on 3k in
    Z^2 = D*u^4 + 6*k*u^2*v^2 - (3*k*k/D)*v^4.
NO_ODD_F3 requires a recorded obstruction for every cover. Surviving covers
mean INCOMPLETE, never existence. Factorization/primality use exact trial
division; no practical running-time guarantee for arbitrarily large inputs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def positive_integer(n: int, name: str = 'input') -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError(f'{name} must be a positive integer')
    return n


def factorint(n: int) -> dict[int, int]:
    """Deterministic exact trial division of a positive integer."""
    n = positive_integer(n)
    result: dict[int, int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0)+1
            n //= p
        p = 3 if p == 2 else p+2
    if n > 1:
        result[n] = result.get(n, 0)+1
    return result


def squarefree_kernel(n: int) -> int:
    result = 1
    for p, exponent in factorint(n).items():
        if exponent % 2:
            result *= p
    return result


def require_squarefree(n: int, name: str = 'input') -> dict[int, int]:
    fs = factorint(positive_integer(n, name))
    if any(e != 1 for e in fs.values()):
        raise ValueError(f'{name} must be squarefree')
    return fs


def require_even_kernel(k: int) -> list[int]:
    fs = require_squarefree(k, 'k')
    if k % 2:
        raise ValueError('k must be even')
    return list(fs)


def is_prime(p: int) -> bool:
    return (not isinstance(p, bool) and isinstance(p, int) and p >= 2
            and factorint(p) == {p: 1})


def legendre(a: int, p: int) -> int:
    """Euler criterion; internal callers have certified odd prime p."""
    value = pow(a % p, (p-1)//2, p)
    return -1 if value == p-1 else value


def sqrt_mod_prime(a: int, p: int) -> int | None:
    """Tonelli-Shanks at a certified odd prime; no probabilistic steps."""
    a %= p
    if a == 0:
        return 0
    if legendre(a, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p+1)//4, p)
    odd, order = p-1, 0
    while odd % 2 == 0:
        odd //= 2
        order += 1
    nonresidue = 2
    while legendre(nonresidue, p) != -1:
        nonresidue += 1
    c = pow(nonresidue, odd, p)
    x = pow(a, (odd+1)//2, p)
    t = pow(a, odd, p)
    while t != 1:
        exponent, tt = 0, t
        while tt != 1 and exponent < order:
            tt = tt*tt % p
            exponent += 1
        if exponent >= order:
            raise ArithmeticError('Tonelli-Shanks invariant failed')
        b = pow(c, 1 << (order-exponent-1), p)
        x = x*b % p
        t = t*b*b % p
        c = b*b % p
        order = exponent
    if x*x % p != a:
        raise ArithmeticError('modular square-root invariant failed')
    return min(x, p-x)


def signed_even_covers(k: int) -> list[int]:
    primes = require_even_kernel(k)
    primes = sorted(set(primes) | {3})
    divisors = [1]
    for p in primes:
        divisors += [p*d for d in divisors]
    return sorted(sign*d for d in divisors if d % 2 == 0 for sign in (-1, 1))


def _check_cover_input(k: int, D: int) -> None:
    require_even_kernel(k)
    if isinstance(D, bool) or not isinstance(D, int) or D == 0:
        raise ValueError('D must be a nonzero signed integer')
    require_squarefree(abs(D), 'abs(D)')
    if D % 2 or (3*k) % abs(D):
        raise ValueError('D must be a signed even squarefree divisor of 3k')


def primitive_modular_test(k: int, D: int, p: int, exponent: int) -> dict:
    """Complete primitive projective cover test modulo p**exponent.

    A primitive pair has u a unit (normalize u=1) or v a unit and p|u
    (normalize v=1). Multiplying a homogeneous quartic by a unit fourth
    power preserves whether it is a square. Thus these two disjoint charts
    cover every primitive pair; no denominator or parity case is omitted.
    """
    _check_cover_input(k, D)
    if not is_prime(p):
        raise ValueError('p must be prime')
    positive_integer(exponent, 'exponent')
    modulus = p**exponent
    squares = {x*x % modulus for x in range(modulus)}
    coefficient = -(3*k*k//D)
    # D divides 3k^2, including for negative D; no rounded division is used.
    if coefficient*D != -3*k*k:
        raise ArithmeticError('cover coefficient is not integral')
    checked = 0
    for u, v in [(1, v) for v in range(modulus)]+[(u, 1) for u in range(0, modulus, p)]:
        checked += 1
        value = (D*u**4+6*k*u*u*v*v+coefficient*v**4) % modulus
        if value in squares:
            return {'method': 'primitive_projective_modulus', 'prime': p,
                    'exponent': exponent, 'modulus': modulus,
                    'excluded': False, 'residue_witness': [u, v, value],
                    'charts_size': modulus+modulus//p}
    return {'method': 'primitive_projective_modulus', 'prime': p,
            'exponent': exponent, 'modulus': modulus, 'excluded': True,
            'charts_size': modulus+modulus//p, 'checked_pairs': checked,
            'square_residue_count': len(squares)}


def odd_prime_test(k: int, D: int, p: int) -> dict:
    """Compressed complete local obstructions at p|k, p>3.

    Exclusion in the p∤D case certifies no primitive solution modulo p^3;
    exclusion in the p|D case certifies no primitive solution modulo p^2.
    Surviving these necessary tests is never asserted locally sufficient.
    """
    _check_cover_input(k, D)
    if p <= 3 or not is_prime(p) or k % p:
        raise ValueError('p must be a prime greater than 3 dividing k')
    if D % p:
        first, second = legendre(D, p), legendre(-3*D, p)
        return {'method': 'odd_prime_unit_classes', 'prime': p,
                'modulus': p**3, 'exponent': 3,
                'D_mod_p': D % p, 'minus3D_mod_p': (-3*D) % p,
                'legendre_D': first, 'legendre_minus3D': second,
                'excluded': first == second == -1}
    delta, kappa = D//p, k//p
    symbol = legendre(3, p)
    base = {'method': 'odd_prime_divisor_quadratic', 'prime': p,
            'modulus': p*p, 'exponent': 2,
            'delta_mod_p': delta % p, 'kappa_mod_p': kappa % p,
            'legendre_3': symbol}
    if symbol == -1:
        return {**base, 'excluded': True, 'reason': '3 is a quadratic nonresidue'}
    root = sqrt_mod_prime(3, p)
    if root is None:
        raise ArithmeticError('discriminant square-root invariant failed')
    roots = [(-3+2*root) % p, (-3-2*root) % p]
    denominator = delta*kappa % p
    values = [(r*pow(denominator, -1, p)) % p for r in roots]
    symbols = [legendre(value, p) for value in values]
    return {**base, 'sqrt3_mod_p': root, 'quadratic_roots': roots,
            'delta_kappa_mod_p': denominator,
            'required_square_residues': values, 'legendre_values': symbols,
            'excluded': all(value == -1 for value in symbols)}


def odd_f3_sieve(k: int) -> dict:
    """Return NO_ODD_F3 only after every necessary cover is certified killed."""
    primes = require_even_kernel(k)
    covers = signed_even_covers(k)
    records, survivors = [], []
    for D in covers:
        attempts = []
        for p, exponent in ((2, 7), (3, 4)):
            test = primitive_modular_test(k, D, p, exponent)
            attempts.append(test)
            if test['excluded']:
                break
        if not attempts[-1]['excluded']:
            for p in primes:
                if p <= 3:
                    continue
                test = odd_prime_test(k, D, p)
                attempts.append(test)
                if test['excluded']:
                    break
        killed = attempts[-1]['excluded']
        if killed:
            records.append({'D': D, 'status': 'KILLED', 'certificate': attempts[-1]})
        else:
            survivors.append(D)
            records.append({'D': D, 'status': 'SURVIVES', 'necessary_tests': attempts})
    return {'status': 'NO_ODD_F3' if not survivors else 'INCOMPLETE', 'k': k,
            'k_prime_factors': primes, 'cover_support': sorted(set(primes) | {3}),
            'cover_equation': 'Z^2=D*u^4+6*k*u^2*v^2-(3*k^2/D)*v^4',
            'cover_count': len(covers), 'covers': records, 'survivors': survivors,
            'scope': 'Odd F3 coefficient multipliers only; other tiling branches are not decided.',
            'survivor_meaning': 'Necessary local tests survived; no rational point or tiling is asserted.'}


def prime_family_predicate(p: int) -> dict:
    """Exact no-square-root predicate for primes p=13 mod24."""
    if not is_prime(p) or p % 24 != 13:
        raise ValueError('p must be prime and congruent to 13 modulo 24')
    left = pow(3, (p-1)//4, p)
    right = pow(5, (p-1)//2, p)
    return {'p': p, 'quartic_power_3': left, 'quadratic_power_5': right,
            'predicate': left == right,
            'formula': '3^((p-1)/4) == 5^((p-1)/2) modulo p'}


def classify_count(d: int, m: int) -> dict:
    """Certified NO for odd m in two proved families; otherwise NOT_COVERED.

    The family-wide removal of classical, alpha, QP, and other branches
    uses the cited uniform reduction and the elementary family arguments.
    A generic F3 obstruction alone is not a global non-tiling certificate.
    """
    fs = require_squarefree(d, 'd')
    m = positive_integer(m, 'm')
    base = {'d': d, 'm': m, 'N': d*m*m, 'd_prime_factors': list(fs)}
    if m % 2 == 0:
        return {**base, 'status': 'NOT_COVERED',
                'reason': 'The two family theorems concern odd multipliers only.'}
    family = None
    if d % 6 == 0:
        R = d//6
        r_primes = list(factorint(R))
        if R > 1 and len(r_primes) % 2 == 0 and all(p % 24 == 7 for p in r_primes):
            family = {'name': '6R_even_prime_support', 'R': R,
                      'R_prime_factors': r_primes, 'number_of_primes': len(r_primes),
                      'prime_residue_modulus': 24, 'prime_residue': 7,
                      'alpha_reason': 'The forced placement of 3 contradicts Q modulo 3.',
                      'QP_reason': 'All primes of R must lie in Q; P=3*y^2 contradicts their 3-nonresidue condition.'}
    if family is None and d % 30 == 0:
        p = d//30
        if is_prime(p) and p % 24 == 13:
            predicate = prime_family_predicate(p)
            if predicate['predicate']:
                family = {'name': '30p_quartic_predicate', **predicate,
                          'alpha_reason': 'No odd kernel prime is 7 modulo 8, so the alpha kernel allocation is impossible.',
                          'QP_reason': 'Prime 5 is inert for both 2 and 3.'}
            else:
                return {**base, 'status': 'NOT_COVERED', 'predicate': predicate,
                        'reason': 'The exact prime-family predicate fails; failure is not a positive tiling test.'}
    if family is None:
        return {**base, 'status': 'NOT_COVERED',
                'reason': 'The squarefree kernel is outside the two proved count-exclusion families.'}
    k = squarefree_kernel(3*d)
    obstruction = odd_f3_sieve(k)
    if obstruction['status'] != 'NO_ODD_F3':
        raise ArithmeticError('recognized family lacks its required complete local-cover certificate')
    if d <= 6 or d % 16 != 6:
        raise ArithmeticError('family escaped the required exhaustive residue-sector reduction')
    return {**base, 'status': 'NO', 'family': family,
            'F3_obstruction': obstruction,
            'classification_input': 'For squarefree d>6, d=6 mod16 and odd m, only alpha, QP, and F3 can contribute.',
            'scope': 'Nonexistence of any congruent-triangle tiling at N, using the cited exhaustive classification inputs.'}


def main() -> None:
    if not __debug__:
        raise SystemExit('Run without Python -O; verification packages retain normal assertion semantics.')
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    f3 = sub.add_parser('f3', help='necessary odd-F3 local-cover sieve')
    f3.add_argument('k', type=int)
    count = sub.add_parser('count', help='two-family count-exclusion decision')
    count.add_argument('d', type=int)
    count.add_argument('m', type=int)
    predicate = sub.add_parser('predicate', help='exact prime-family residue predicate')
    predicate.add_argument('p', type=int)
    for child in (f3, count, predicate):
        child.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = (odd_f3_sieve(args.k) if args.command == 'f3' else
                  classify_count(args.d, args.m) if args.command == 'count' else
                  prime_family_predicate(args.p))
    except ValueError as exc:
        parser.error(str(exc))
    data = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.report:
        args.report.write_text(data, encoding='utf-8')
    print(data, end='')


if __name__ == '__main__':
    main()
