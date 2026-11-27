"""Signed unmatched owners in the five regions separated by four distinguished gates."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'2026-11-26/semiprimes/boundary-word'))
from nested import cut_rows
from remote import inventories


def solve(a, b, c, limit, unit, collect=False):
    d = a-b
    bound = limit//c
    # Each other native cut needs c, the pure descendant c+d, and the
    # mixed cut at least min(2(c-d),c+d) by its two characters.
    cap = limit-c-(c+d)-min(2*(c-d), c+d)
    native = []
    for depth in (1, 2):
        rows = []
        for p,q,E,O,lower in cut_rows(c,d,depth,limit):
            if lower > cap:
                continue
            cost = min((r[0] for r in inventories(a,b,c,depth,p,q,cap)), default=cap+1)
            if cost <= cap:
                rows.append((p,q,E,O,cost))
        native.append(rows)

    @lru_cache(None)
    def trunk(region, delta_even, delta_odd):
        best = limit+1
        for (p,q,E,O,m),(t,v,F,J,k) in product(*native):
            residual = [-d-E-q,-c-O,E-F,O-J-p-v,F-t,J]
            residual[2*region] += delta_even
            residual[2*region+1] += delta_odd
            best = min(best, m+k+sum(map(abs,residual)))
        return best

    best = limit+1
    witness = None
    profiles = []
    for e,o in product(range(-bound,bound+1), repeat=2):
        if not e or not o or c*(abs(e)+abs(o)) > limit:
            continue
        if unit and abs(e-o) != 1:
            continue
        for far in (0,1):
            same, other = (o,e) if far else (e,o)
            p, q = c*same-d*other, d*same-c*other
            mixed = abs(p)+abs(q)
            if abs(e-o)==1:
                mixed = max(mixed, 73 if c==43 else (67 if abs(e+o)>=5 else 63))
            external = [-c*e, -c*o]
            external[1-far] -= q
            for region in range(3):
                native_cost = trunk(region,*external)
                for h in (0,1):
                    for f in range(-bound,bound+1):
                        if not f:
                            continue
                        shell = [c*e,c*o]
                        shell[far] -= p
                        shell[h] -= c*f
                        shell[1-h] -= d*f
                        charge_cost = native_cost+mixed+(c+d)*abs(f)+sum(map(abs,shell))
                        if collect and charge_cost <= limit:
                            for first, second in product(*native):
                                p1,q1,E,O,m1 = first
                                p2,q2,F,J,m2 = second
                                residual = [-d-E-q1,-c-O,E-F,O-J-p1-q2,F-p2,J]
                                residual[2*region] += external[0]
                                residual[2*region+1] += external[1]
                                total = charge_cost-native_cost+m1+m2+sum(map(abs,residual))
                                if total <= limit:
                                    profiles.append(dict(mixed=[e,o], far=far, trunk=region,
                                                         deepest=[h,f], native=[first,second],
                                                         residual=residual, shell=shell))
                        if charge_cost < best:
                            best = charge_cost
                            witness = dict(mixed_units=[e,o], far_parity=far, trunk=region,
                                           deepest_parity=h, deepest_units=f)
    assert witness is not None and best<=limit
    if collect:
        return profiles
    return dict(lower=best, minimizing_relaxed_profile=witness)


if __name__ == '__main__':
    cases = {}
    for a,b,c,limit in [(33,7,37,235),(35,13,43,273)]:
        cases[(a+2*b)*(2*a+b)] = {
            mode:solve(a,b,c,limit,mode=='unit') for mode in ('mixed','unit')}
    print(json.dumps(cases,indent=2))
