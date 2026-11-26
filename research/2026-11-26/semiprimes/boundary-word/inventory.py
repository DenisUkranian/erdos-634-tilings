"""Independent slant spectrum calculation by direction inventories and path area."""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def determinant(u, v):
    return u[0]*v[1] - u[1]*v[0]


def inventory_bound(base, inventory, c):
    leading = c * sum(abs(determinant(base, v)) for v in inventory)
    mixed = sum(abs(determinant(u, v)) for u, v in combinations(inventory, 2))
    assert (leading + mixed) % c == 0
    return 2 * ((leading + mixed) // c)


def reachable(base, inventory, c, bound, targets):
    counts = Counter({base: c})
    for v in inventory:
        counts[v] += 1
        counts[(-v[0], -v[1])] += 1
    steps = tuple(counts)
    # A prefix whose area is d below the best area at the same count
    # vector loses at least d in every extension to the final inventory.
    limit = bound - min(targets)
    mask = (1 << (limit + 1)) - 1

    @lru_cache(maxsize=None)
    def signatures(state):
        if not any(state):
            return 0, 1
        position = tuple(sum(n * step[j] for n, step in zip(state, steps))
                         for j in (0, 1))
        peak = None
        flags = 0
        for j, n in enumerate(state):
            if n == 0:
                continue
            prev = state[:j] + (n-1,) + state[j+1:]
            previous_peak, previous_flags = signatures(prev)
            increment, rem = divmod(determinant(position, steps[j]), c)
            assert rem == 0
            value = previous_peak + increment
            if peak is None or value > peak:
                flags = 0 if peak is None else (flags << (value - peak)) & mask
                peak = value
            if peak - value <= limit:
                flags |= (previous_flags << (peak - value)) & mask
        return peak, flags

    peak, flags = signatures(tuple(counts.values()))
    signatures.cache_clear()
    assert peak <= bound
    return {t for t in targets if 0 <= peak - t <= limit and (flags >> (peak - t)) & 1}


def report(a, b, c):
    base = a, b
    axes = [(c, 0), (0, c), (-c, c), base, (-b, a+b), (-a-b, a)]
    found = {0}
    result = {}
    for r in range(7):
        if r*r >= c:
            break
        inventories = sorted(((inventory_bound(base, inv, c), inv) for inv in
                              combinations_with_replacement(axes, r)), reverse=True)
        upper = inventories[0][0] // (2*a*b)
        pending = {2*a*b*k for k in range(upper+1) if k not in found}
        examined = 0
        for bound, inv in inventories:
            if not pending or bound < min(pending):
                break
            accepted = reachable(base, inv, c, bound, {t for t in pending if t <= bound})
            found.update(t // (2*a*b) for t in accepted)
            pending -= accepted
            examined += 1
        result[c+2*r] = {"multipliers_of_2c": sorted(found), "area_upper": upper,
                         "inventories": len(inventories), "evaluated_inventories": examined}
    return result


if __name__ == "__main__":
    ap = ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    result = {(a+2*b)*(2*a+b): report(a, b, c) for a, b, c in
              [(5, 3, 7), (33, 7, 37), (35, 13, 43)]}
    out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert out == Path(__file__).with_name("INVENTORIES.json").read_text()
        print("Independent area inventories reproduced.")
    else:
        print(out, end="")
