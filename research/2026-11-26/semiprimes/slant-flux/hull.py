"""Necessary populations and signed gate currents for a small excess budget."""
from itertools import product


def allocations(budget, lower):
    if not lower:
        yield ()
        return
    for first in range(lower[0], budget - sum(lower[1:]) + 1):
        for tail in allocations(budget - first, lower[1:]):
            yield (first,) + tail


def branches(parents):
    adjacent = [[] for _ in range(3 + len(parents))]
    for u, v in [(0, 1), (1, 2), *[(p, i + 3) for i, p in enumerate(parents)]]:
        adjacent[u].append(v)
        adjacent[v].append(u)

    def walk(v, previous):
        yield v
        for w in adjacent[v]:
            if w != previous:
                yield from walk(w, v)

    return [[tuple(walk(w, v)) for w in neighbors] for v, neighbors in enumerate(adjacent)]


def gate_filters(c, size, charge, currents, middle):
    a, b = (43, 222) if c == 37 else (8, 43)
    numerator, denominator = (3810, 1002) if c == 37 else (4304, 1001)
    pos, neg = (size + charge)*c//2, (size - charge)*c//2
    positive = sum(max(x, 0) for x in currents)
    negative = sum(max(-x, 0) for x in currents)
    if positive > pos or negative > neg:
        return False
    if any(x*b > a*pos + (b-a)*neg or -x*b > a*neg + (b-a)*pos for x in currents):
        return False
    nonzero = sorted(x for x in currents if x)
    if len(nonzero) == 1 and abs(charge)*numerator > size*denominator:
        return False
    if c == 37 and size == 4 and nonzero == [26, 48]:
        return False
    if middle:
        axial, slant, *other = currents
        other = sorted(x for x in other if x)
        if not other and (axial, slant) in ((2*c, -c), (c, -c)):
            if size < (9 if axial == 2*c else 6):
                return False
        if size == 4 and axial == 2*c:
            if (slant == -2*c and not other) or (slant == -c and other == [-c]):
                return False
    return True


def profiles(c, d, budget):
    assert c in (37, 43) and 6 <= budget <= 8
    out = set()
    for k in range(budget - 1):
        for parents in product(*(range(3+i) for i in range(k))):
            children = [parents.count(3+i) for i in range(k)]
            lower = [3 if v == 0 else int(v == 1) for v in children]
            if sum(lower) > budget:
                continue
            sides = branches(parents)
            for excess in allocations(budget, [0, 0] + lower):
                if max(excess) < 3:
                    continue
                sizes = (0,) + tuple(2+x for x in excess)
                for ordinary in product(*(range(2-n, n, 2) for n in sizes[1:])):
                    if any(g == 0 and k < 2 for g, k in zip(ordinary[2:], children)):
                        continue
                    for tail in product((0, 1), repeat=k):
                        parity = (0, 1, 0) + tail
                        if sum(g for g, p in zip(ordinary, parity[1:]) if p) != 1:
                            continue
                        core = -sum(g for g, p in zip(ordinary, parity[1:]) if not p)
                        charge = (core,) + ordinary
                        star = []
                        for i in range(1, len(charge)):
                            q = []
                            for side in sides[i]:
                                e = sum(charge[j] for j in side if not parity[j])
                                o = sum(charge[j] for j in side if parity[j])
                                C, T = int(0 in side), int(2 in side)
                                q.append(d*e-c*o+2*c*C-c*T if parity[i] else d*o-c*e-d*C)
                            assert sum(q) == c*charge[i]
                            if not gate_filters(c, sizes[i], charge[i], q, i == 1):
                                break
                            star.append((sizes[i], tuple(q) if i == 1 else tuple(sorted(x for x in q if x))))
                        else:
                            remote = []
                            for side in sides[0][1:]:
                                even = sum(charge[j] for j in side if not parity[j])
                                odd = sum(charge[j] for j in side if parity[j])
                                remote.append(d*odd-c*even)
                            native = d+c*core-sum(remote)
                            core_gates = native, tuple(sorted(x for x in remote if x))
                            out.add((core, core_gates, tuple(star)))
    return sorted(out)
