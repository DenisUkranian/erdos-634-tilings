#!/usr/bin/env python3
"""Small exact integer certificate for STRUCTURE.md."""

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
    (edge(j, 3 if typ == 0 else 5),
     edge((j + 5) % 6, 5 if typ == 0 else 3))
    for typ in range(2) for j in range(6)
]


def signature(counts, offset=0):
    out = [0, 0, 0]
    for k, count in enumerate(counts):
        for d, length in EDGES[offset + k]:
            out[d] += count * length
    return tuple(v % 7 for v in out)


def enumerate_by_character():
    out = set()
    for sign in (-1, 1):
        allowed = [i for i in range(12)
                   if (1 if i < 6 else -1) * (-1)**(i % 6) == sign]
        assert len(allowed) == 6
        for six in compositions(7, 6):
            inv = [0] * 12
            for i, n in zip(allowed, six):
                inv[i] = n
            if signature(inv) == (0, 0, 0):
                out.add(tuple(inv))
    return out


def enumerate_by_residue_join():
    """All 12-orientation inventories, without assuming a common character."""
    bank = defaultdict(list)
    for n in range(8):
        for b in compositions(n, 6):
            bank[(n, signature(b, 6))].append(b)
    out = set()
    for n in range(8):
        for a in compositions(n, 6):
            opposite = tuple(-v % 7 for v in signature(a))
            for b in bank[(7 - n, opposite)]:
                out.add(a + b)
    return out


PAIRS = tuple(sorted((m, n) for m in range(8) for n in range(8-m)
                     if m+n and (3*m-5*n) % 7 == 0))


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
            totals[d][int(abs(length) == 5)] += n
    assert all(sum(t) <= 7 for t in totals)
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
                        "direction_totals_3_5": selected,
                        "max_supporting_lines": line_counts,
                        "max_gamma_vertices": bound})
    return out


def check():
    feasible = enumerate_by_character()
    assert feasible == enumerate_by_residue_join()
    assert len(feasible) == 36
    assert PAIRS == ((0, 7), (1, 2), (2, 4), (4, 1), (7, 0))
    assert {p: max_lines(p) for p in PAIRS} == {
        (0, 7): 1, (1, 2): 1, (2, 4): 2, (4, 1): 1, (7, 0): 1}
    orbits = defaultdict(list)
    certificate = []
    for inv in sorted(feasible):
        bad = violations(inv)
        assert bad, inv
        orbits[canonical(inv)].append(inv)
        certificate.append({"inventory_A0_to_A5_B0_to_B5": inv,
                            "contradiction": bad[0]})
    assert len(orbits) == 3
    assert all(len(v) == 12 for v in orbits.values())
    # Independent finite arithmetic in the 49-tail proof.
    assert (19*19) % 45 == 1
    assert (-2-7*19) % 45 == 0
    possible_M = [M for M in range(-49, 50)
                  if M % 45 == 0 and M % 2 == 1]
    assert possible_M == [-45, 45]
    assert all(abs(M) + abs(2*M//9) == 55 for M in possible_M)
    # Every side30 needs at least three short boundary edges.
    boundary_words = [(A,B,C) for A in range(11) for B in range(7)
                      for C in range(5) if 3*A+5*B+7*C == 30]
    assert min(A+B for A,B,C in boundary_words) == 3
    central = [n for n in range(5, 61) if n % 7 == 60 % 7]
    assert central[0] == 11
    assert 11 + 4*14 > 60
    return {"status": "PASS", "full_Erdos634_solved": False,
            "E60_solved": False,
            "all_modularly_feasible_seven_inventories": 36,
            "independent_enumerations_agree": True,
            "rotation_reflection_orbits": 3,
            "all_36_have_gamma_vertex_contradiction": True,
            "nonzero_height_population_floor": 14,
            "central_height_population_floor_for_E30": 11,
            "max_occupied_heights_for_E30": 4,
            "tail49_modulus": 45, "tail49_evaluation": 19,
            "tail49_candidate_currents": possible_M,
            "representatives": [
                {"inventory_A0_to_A5_B0_to_B5": inv,
                 "orbit_size": len(orbits[inv]),
                 "contradictions": violations(inv)} for inv in sorted(orbits)],
            "certificate_for_all_inventories": certificate}


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run without -O so the exact assertions execute.")
    print(json.dumps(check(), indent=2))
