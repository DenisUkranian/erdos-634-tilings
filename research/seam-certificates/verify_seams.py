#!/usr/bin/env python3
"""Replay exact atomic seams of data/tiling-322.json; not a tiling search.

No construction module is imported. The existing geometric certificate is
the input: full nonoverlap is checked separately by scripts/verify_322.py.
Default execution is read-only; --report writes the supplied JSON path.
"""

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from math import isqrt
from pathlib import Path

if not __debug__:
    raise SystemExit("Run without -O: this verifier requires assertions.")

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "data/tiling-322.json"


def cross(a, b, p):
    return ((b[0] - a[0]) * (p[1] - a[1])
            - (b[1] - a[1]) * (p[0] - a[0]))


def on_segment(a, b, p):
    return (cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def verify():
    raw = CERTIFICATE.read_bytes()
    obj = json.loads(raw)
    assert obj["N"] == 322 and obj["D"] == 32 and obj["denominator"] == 18
    assert sorted((obj["a"], obj["b"], obj["c"])) == [5, 6, 9]
    tiles = [[tuple(p) for p in t] for t in obj["tiles"]]
    target = [tuple(p) for p in obj["target"]]
    assert len(tiles) == obj["N"] and len(target) == 3
    vertices = set(p for t in tiles for p in t)
    assert set(target) <= vertices
    boundary_sides = list(zip(target, target[1:] + target[:1]))

    def length(a, b):
        sq = (a[0] - b[0]) ** 2 + obj["D"] * (a[1] - b[1]) ** 2
        z = isqrt(sq)
        assert z > 0 and z * z == sq and z % obj["denominator"] == 0
        return z // obj["denominator"]

    atom_sides = defaultdict(list)
    side_lengths = {}
    side_atoms = {}
    flat_incidence = Counter()
    for i, tile in enumerate(tiles):
        assert len(tile) == 3 and cross(*tile) != 0
        for j, (a, b) in enumerate(zip(tile, tile[1:] + tile[:1])):
            key = (i, j)
            side_lengths[key] = length(a, b)
            # All actual tile vertices are used, including vertices in the
            # relative interior of this side. Thus T-junctions are retained.
            pts = [p for p in vertices if on_segment(a, b, p)]
            pts.sort(key=lambda p: ((p[0] - a[0]) * (b[0] - a[0])
                                    + (p[1] - a[1]) * (b[1] - a[1])))
            assert pts[0] == a and pts[-1] == b
            flat_incidence.update(pts[1:-1])
            atoms = [tuple(sorted(e)) for e in zip(pts, pts[1:])]
            side_atoms[key] = atoms
            assert sum(length(*e) for e in atoms) == side_lengths[key]
            for atom in atoms:
                atom_sides[atom].append(key)
        assert sorted(side_lengths[i, j] for j in range(3)) == [5, 6, 9]

    adj = defaultdict(dict)
    for atom, sides in atom_sides.items():
        assert len(sides) in (1, 2)
        on_boundary = any(all(on_segment(a, b, p) for p in atom)
                          for a, b in boundary_sides)
        assert on_boundary == (len(sides) == 1)
        if len(sides) == 2:
            s, t = sides
            assert s[0] != t[0]
            # The two incident triangle interiors occupy opposite banks.
            third_s = tiles[s[0]][(s[1] + 2) % 3]
            third_t = tiles[t[0]][(t[1] + 2) % 3]
            assert cross(*atom, third_s) * cross(*atom, third_t) < 0
            assert t not in adj[s], "parallel contacts form a forbidden cycle"
            adj[s][t] = adj[t][s] = length(*atom)

    for atoms in side_atoms.values():
        counts = {len(atom_sides[e]) for e in atoms}
        assert len(counts) == 1, "partly boundary original side"
        if counts == {1}:
            assert len(atoms) == 1, "genuine vertex inside a boundary tile side"

    seen = set()
    components = []
    for seed in adj:
        if seed in seen:
            continue
        todo = [seed]
        seen.add(seed)
        comp = []
        while todo:
            v = todo.pop()
            comp.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
        edges = sum(len(adj[v]) for v in comp) // 2
        assert edges == len(comp) - 1, "side-contact cycle"
        # Recover lengths using only the tree and WHOLE side lengths.
        # Coordinates are used afterwards to compare the recovered values.
        rem = {v: side_lengths[v] for v in comp}
        work = {v: set(adj[v]) for v in comp}
        leaves = deque(v for v in comp if len(work[v]) == 1)
        recovered = {}
        while leaves:
            v = leaves.popleft()
            if len(work[v]) != 1:
                continue
            w = next(iter(work[v]))
            ell = rem[v]
            assert ell > 0
            recovered[frozenset((v, w))] = ell
            assert ell == adj[v][w]
            rem[w] -= ell
            work[w].remove(v)
            work[v].clear()
            rem[v] = 0
            if len(work[w]) == 1:
                leaves.append(w)
        assert all(r == 0 for r in rem.values())
        assert len(recovered) == edges
        components.append(len(comp))

    boundary_vertices = {p for p in vertices
                         if any(on_segment(a, b, p) for a, b in boundary_sides)}
    interior_vertices = vertices - boundary_vertices
    assert all(flat_incidence[p] == 0 for p in boundary_vertices)
    assert all(flat_incidence[p] <= 1 for p in interior_vertices)
    T = sum(flat_incidence[p] == 1 for p in interior_vertices)
    I = len(interior_vertices) - T
    B = len(boundary_vertices)
    N, V, E = len(tiles), len(vertices), len(atom_sides)
    darts = sum(map(len, side_atoms.values()))
    assert N == 2 * I + T + B - 2
    assert V - E + N == 1
    assert T <= N - 1 and V <= N + 2 and E <= 2 * N + 1
    assert darts == 3 * N + T <= 4 * N - 1
    return {
        "status": "PASS",
        "full_Erdos634_solved": False,
        "scope": "finite seam replay of the retained N=322 certificate",
        "certificate": CERTIFICATE.relative_to(ROOT).as_posix(),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "N": N,
        "original_tile_sides": len(side_lengths),
        "side_contact_tree_components": len(components),
        "side_contact_component_sizes": dict(sorted(Counter(components).items())),
        "interior_atoms": sum(len(ss) == 2 for ss in atom_sides.values()),
        "boundary_atoms": sum(len(ss) == 1 for ss in atom_sides.values()),
        "vertices": V,
        "interior_vertices_without_flat_tile": I,
        "interior_T_junctions": T,
        "boundary_vertices_including_three_corners": B,
        "atomic_edges": E,
        "face_edge_incidences": darts,
        "all_atom_lengths_integer": True,
        "length_histogram": dict(sorted(Counter(length(*e) for e in atom_sides).items())),
        "all_internal_atom_lengths_recovered_by_integer_leaf_elimination": True,
        "geometric_nonoverlap_not_reproved_by_this_script": True,
        "complete_abstract_disk_certificate_verifier": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", "--output", dest="report", type=Path,
                        help="write the JSON report here")
    args = parser.parse_args()
    output = json.dumps(verify(), indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
