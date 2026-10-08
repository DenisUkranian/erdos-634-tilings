#!/usr/bin/env python3
"""Small exact integer certificate for NO_THIRTEEN_HEIGHT.md."""

from collections import defaultdict
from functools import lru_cache
import json


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for x in range(n + 1):
            for tail in compositions(n - x, k - 1):
                yield (x,) + tail


def edge(rotation, length):
    return (rotation % 3, length if rotation < 3 else -length)


EDGES = [
    (edge(j, 8 if typ == 0 else 7),
     edge((j + 5) % 6, 7 if typ == 0 else 8))
    for typ in range(2) for j in range(6)
]


def signature(counts, offset=0):
    out = [0, 0, 0]
    for k, count in enumerate(counts):
        for d, length in EDGES[offset + k]:
            out[d] += count * length
    return tuple(v % 13 for v in out)


def enumerate_by_character():
    out = set()
    for sign in (-1, 1):
        allowed = [i for i in range(12)
                   if (1 if i < 6 else -1) * (-1)**(i % 6) == sign]
        assert len(allowed) == 6
        for six in compositions(13, 6):
            inv = [0] * 12
            for i, n in zip(allowed, six):
                inv[i] = n
            if signature(inv) == (0, 0, 0):
                out.add(tuple(inv))
    return out


def enumerate_by_residue_join():
    """All 12-orientation inventories, without assuming a common character."""
    bank = defaultdict(list)
    for n in range(14):
        for b in compositions(n, 6):
            bank[(n, signature(b, 6))].append(b)
    out = set()
    for n in range(14):
        for a in compositions(n, 6):
            opposite = tuple(-v % 13 for v in signature(a))
            for b in bank[(13 - n, opposite)]:
                out.add(a + b)
    return out


PAIRS = tuple(sorted((m, n) for m in range(14) for n in range(14-m)
                     if m+n and (8*m-7*n) % 13 == 0))


@lru_cache(None)
def max_lines(total):
    if total == (0, 0):
        return 0
    best = -100
    for m, n in PAIRS:
        if m <= total[0] and n <= total[1]:
            suffix = max_lines((total[0]-m, total[1]-n))
            if suffix >= 0:
                best = max(best, suffix+1)
    return best


def rotate(inv, k):
    return tuple(inv[6*t+(j-k) % 6] for t in range(2) for j in range(6))


def reflect(inv):
    # Conjugate coordinates and reverse the CCW vertex order:
    # A_j maps to B_(4-j), and B_j maps to A_(4-j).
    return tuple(inv[6*(1-t)+(4-j) % 6] for t in range(2) for j in range(6))


def canonical(inv):
    return min([rotate(inv, k) for k in range(6)] +
               [rotate(reflect(inv), k) for k in range(6)])


def violations(inv):
    totals = [[0, 0] for _ in range(3)]
    for n, edges in zip(inv, EDGES):
        for d, length in edges:
            totals[d][int(abs(length) == 7)] += n
    assert all(sum(t) <= 13 for t in totals)
    assert all(tuple(t) in PAIRS or t == [0, 0] for t in totals)
    out = []
    for i, (n, edges) in enumerate(zip(inv, EDGES)):
        if not n:
            continue
        selected = [tuple(totals[d]) for d, _ in edges]
        line_counts = [max_lines(t) for t in selected]
        bound = line_counts[0] * line_counts[1]
        assert all(x >= 1 for x in line_counts)
        if n > bound:
            out.append({"orientation": ("A" if i < 6 else "B") + str(i % 6),
                        "multiplicity": n,
                        "direction_totals_8_7": selected,
                        "max_supporting_lines": line_counts,
                        "max_gamma_vertices": bound})
    return out


def check():
    feasible = enumerate_by_character()
    assert feasible == enumerate_by_residue_join()
    assert len(feasible) == 108
    assert PAIRS == tuple(sorted(((13, 0), (0, 13), (9, 1), (5, 2),
                                (1, 3), (6, 5), (2, 6), (3, 9))))
    expected_maxima = {(13, 0): 1, (0, 13): 1, (9, 1): 1, (5, 2): 1,
                       (1, 3): 1, (6, 5): 2, (2, 6): 2, (3, 9): 3}
    assert {p: max_lines(p) for p in PAIRS} == expected_maxima
    orbits = defaultdict(list)
    certificate = []
    for inv in sorted(feasible):
        bad = violations(inv)
        assert bad, inv
        orbits[canonical(inv)].append(inv)
        certificate.append({"inventory_A0_to_A5_B0_to_B5": inv,
                            "contradiction": bad[0]})
    assert len(orbits) == 9
    assert all(len(v) == 12 for v in orbits.values())
    return {"status": "PASS", "full_Erdos634_solved": False,
            "N154_solved": False,
            "all_modularly_feasible_inventories": 108,
            "independent_enumerations_agree": True,
            "rotation_reflection_orbits": 9,
            "all_108_have_gamma_vertex_contradiction": True,
            "conclusion": "Every occupied nonzero height has at least 26 tiles.",
            "representatives": [
                {"inventory_A0_to_A5_B0_to_B5": inv,
                 "orbit_size": len(orbits[inv]),
                 "contradictions": violations(inv)} for inv in sorted(orbits)],
            "certificate_for_all_inventories": certificate}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
