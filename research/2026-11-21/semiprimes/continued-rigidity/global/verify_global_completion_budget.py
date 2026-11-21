#!/usr/bin/env python3
"""Integer arithmetic controls for the global physical cell-reserve budget.

These are arithmetic controls of the theorem, not a physical row catalogue
or an infeasibility certificate for either target.
"""
from itertools import product
import json
from pathlib import Path


def ceildiv(a, b):
    return -((-a) // b)


def coarse(c, positive, negative):
    return 2*c*ceildiv(max(positive, negative+c), c)-c


def strengthened(c, mu, positive, negative, largest_cell):
    assert 0 <= largest_cell <= positive
    assert (positive == 0) == (largest_cell == 0)
    need = max(positive+max(0, c+mu-largest_cell), negative+c)
    return 2*c*ceildiv(need, c)-c


def node_at_actual_charges(c, mu, full, retained):
    observed = [i for i, (p, n) in enumerate(retained) if p+n]
    assert observed
    charges = [(p-n)//c for p, n in full]
    hidden = sum(charges[i] for i in range(len(full)) if i not in observed)
    charged_mass = abs(hidden)+sum(abs(charges[i]) for i in observed)
    reserve = mu*(abs(hidden) == 1)
    for i in observed:
        p, n = retained[i]
        g = charges[i]
        reserve += max(0, p-c*max(g, 0), n-c*max(-g, 0),
                       mu*(abs(g) == 1))
    return max(2*c, c*charged_mass+2*c*ceildiv(reserve, c))


def arithmetic_controls():
    out = {'scope': 'Exact arithmetic controls, not target infeasibility.',
           'targets': []}
    for target, c, mu, odd_min, even_min, threshold in (
            (3431, 37, 2, 3*37, 64, 46),
            (5063, 43, 5, 5*43, 32, 59)):
        compared = strict = 0
        # Every such largest-cell count can occur in a partition of P:
        # use one cell of that size and singleton cells for the remainder.
        for p in range(3*c+1):
            for n in range(3*c+1):
                for largest in (range(1, p+1) if p else (0,)):
                    old = max(odd_min, coarse(c, p, n))
                    new = max(odd_min, strengthened(c, mu, p, n, largest))
                    assert new >= old
                    compared += 1
                    strict += new > old
        spread = []
        for k in range(1, threshold+1):
            raw = strengthened(c, mu, k*c, 0, c)
            assert raw == (2*k+1)*c
            spread.append({'cells': k, 'retained_positive': k*c,
                           'largest_retained_cell': c,
                           'old_rounded_odd_bound': max(odd_min, (2*k-1)*c),
                           'new_rounded_odd_bound': max(odd_min, raw)})
        assert even_min+(2*threshold+1)*c > target
        assert even_min+(2*(threshold-1)+1)*c <= target
        out['targets'].append({
            'N': target, 'c': c, 'mu': mu,
            'known_minimum_odd_population': odd_min,
            'minimum_even_population': even_min,
            'coarse_comparison_cases': compared,
            'strictly_stronger_cases': strict,
            'spread_examples': spread,
            'sufficient_spread_cell_threshold': threshold,
            'total_budget_at_threshold': even_min+(2*threshold+1)*c,
            'claimed_actual_row_family_with_this_property': False,
        })

    # A small exhaustive abstract population model tests retained-sign
    # accounting and aggregation of unobserved cells independently of any
    # triangle or endpoint implementation.  This does not prove the theorem;
    # its proof is the accompanying written argument.
    c, mu = 3, 1
    cells = [(p, n) for p in range(7) for n in range(7)
             if (p-n) % c == 0 and
             (abs(p-n) != c or min(p, n) >= mu)]
    node_checks = full_odd_checks = aggregate_checks = 0
    for count in (1, 2, 3):
        for full in product(cells, repeat=count):
            p_full = sum(p for p, n in full)
            n_full = sum(n for p, n in full)
            if abs(p_full-n_full) == c:
                assert min(p_full, n_full) >= mu
                aggregate_checks += 1
            if not p_full+n_full or p_full % c or n_full % c:
                continue
            alternatives = []
            for p, n in full:
                ps = sorted({0, min(1, p), p})
                ns = sorted({0, min(1, n), n})
                alternatives.append(tuple(product(ps, ns)))
            for retained in product(*alternatives):
                p = sum(x for x, y in retained)
                n = sum(y for x, y in retained)
                if p+n:
                    bound = node_at_actual_charges(c, mu, full, retained)
                    assert bound <= p_full+n_full
                    node_checks += 1
                if p_full-n_full == c:
                    largest = max(x for x, y in retained)
                    bound = strengthened(c, mu, p, n, largest)
                    assert bound <= p_full+n_full
                    full_odd_checks += 1
    out['small_abstract_controls'] = {
        'c': c, 'mu': mu, 'individual_cell_types': len(cells),
        'maximum_cells_per_node': 3,
        'unseen_aggregate_unit_charge_checks': aggregate_checks,
        'node_reserve_retention_checks': node_checks,
        'complete_odd_population_retention_checks': full_odd_checks,
        'scope': 'All cell populations in [0,6]^2 satisfying charge '
                 'divisibility and unit-charge minority, in lists of one, '
                 'two, or three cells. Retained signs independently use '
                 'zero, one when available, or the full count. Node tests '
                 'require both full sign populations divisible by c.',
    }
    return out


if __name__ == '__main__':
    result = arithmetic_controls()
    Path(__file__).with_name('GLOBAL_COMPLETION_BUDGET_REPLAY.json').write_text(
        json.dumps(result, indent=2)+'\n')
    summary = dict(result)
    summary['targets'] = [{k: v for k, v in row.items() if k != 'spread_examples'}
                          for row in result['targets']]
    print(json.dumps(summary, indent=2))
