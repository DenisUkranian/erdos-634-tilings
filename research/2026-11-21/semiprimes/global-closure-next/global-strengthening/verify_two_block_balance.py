#!/usr/bin/env python3
"""Exact finite arithmetic for the one-height two-block balance theorem.

This is not a tiling search. The actual-line and gate hypotheses are
proved in TWO_BLOCK_BALANCE_5063.md and its cited project notes.
"""
import json
from pathlib import Path


def main():
    if not __debug__:
        raise RuntimeError('Run without -O.')
    all_pairs = []
    for M in range(87):
        for L in range(87):
            if not M+L or (35*M-13*L) % 43:
                continue
            t = (8*M+13*L)//43
            assert (2*M-t) % 13 == 0
            u = (2*M-t)//13
            assert t >= 1 and 2*L == 6*t-8*u
            assert (u-t) % 2 == 0 and u <= t-2
            assert (M+7*L) % 43 == 0 and (M+7*L)//43 >= 1
            all_pairs.append((M,L))
    tsum, usum = 42,10
    assert tsum == 21*86//43 and usum == (2*86-tsum)//13
    rmax = (tsum-usum)//2
    assert rmax == 16 == (86+7*86)//43
    families = []
    for r0 in range(17):
        for r1 in range(r0,17):
            for r2 in range(r1,17):
                if r0+r1+r2 <= 16 and r0*r1+r1*r2+r2*r0 >= 84:
                    families.append((r0,r1,r2))
    assert families == [(4,6,6),(5,5,6)]
    small_pairs = [(M,L) for M,L in all_pairs if M <= 8 and L <= 8]
    assert small_pairs == [(1,6),(8,5)]
    decompositions = [(x,y) for x in range(17) for y in range(17)
                      if x+y == 16 and x+8*y == 86 and 6*x+5*y == 86]
    assert decompositions == [(6,10)]
    minority_demand = (8-6)*10
    assert minority_demand == 20 and minority_demand > 2
    native = {}
    for tree, offset in [('increasing',86),('decreasing',-43)]:
        for sigma in [1,-1]:
            currents = [q for q in range(-16,17)
                        if 0 <= sigma*q <= 16 and (q-offset) % 22 == 0]
            native[f'{tree}, sign {sigma:+}'] = currents
    assert native == {'increasing, sign +1':[], 'increasing, sign -1':[-2],
                      'decreasing, sign +1':[1], 'decreasing, sign -1':[]}
    remote = [q for q in range(-16,17) if q % 22 == 0]
    assert remote == [0]
    report = {
        'scope':'Necessary arithmetic for two-block balance at height one on 5063; no tiling exclusion.',
        'single_sign_class_population':86,
        'line_bound':rmax,
        'family_sizes_if_at_most_two_minority_hand_tiles':families,
        'complete_line_pairs_with_M_L_at_most_8':small_pairs,
        'counts_of_the_two_line_types':decompositions[0],
        'forced_minority_hand_tiles':minority_demand,
        'hypothesized_maximum_minority_hand_tiles':2,
        'native_current_possibilities':native,
        'remote_current_possibilities':remote,
        'finite_arithmetic':'PASS',
        'full_5063_exclusion':False,
    }
    encoded=json.dumps(report,indent=2)+'\n'
    Path(__file__).with_name('TWO_BLOCK_BALANCE_REPLAY.json').write_text(encoded)
    print(encoded,end='')


if __name__ == '__main__':
    main()
