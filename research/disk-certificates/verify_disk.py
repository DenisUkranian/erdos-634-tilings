#!/usr/bin/env python3
"""Verify a coordinate-free certificate for a disk tiled by integer triangles.

Input contains only whole triangle side lengths, their vertex subdivisions,
and the three marked boundary corners. Atomic lengths and an exact planar
development are recovered here. No construction or external package is used.

Soundness of the final geometric check uses the degree-one disk lemma: a
continuous map of an oriented disk, affine with positive determinant on each
nondegenerate triangle, whose boundary maps homeomorphically to a positively
oriented triangle, is a homeomorphism. In particular, its tiles do not overlap.
This verifies a supplied scheme; it neither searches nor classifies tile counts.
"""

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


SCHEMA = "integer-triangle-disk-v1"


class CertificateError(ValueError):
    """An input failed an explicit certificate condition."""


def require(condition, message):
    if not condition:
        raise CertificateError(message)


def integer(value, where, *, positive=False):
    require(type(value) is int, f"{where}: expected an integer, not {type(value).__name__}")
    require(value > 0 if positive else value >= 0,
            f"{where}: expected a {'positive' if positive else 'nonnegative'} integer")
    return value


def exact_keys(value, keys, where):
    require(isinstance(value, dict), f"{where}: expected an object")
    require(set(value) == set(keys), f"{where}: expected exactly keys {sorted(keys)}")


def triple(value, where, *, positive=False):
    require(isinstance(value, list) and len(value) == 3,
            f"{where}: expected a list of three integers")
    return tuple(integer(x, f"{where}[{i}]", positive=positive)
                 for i, x in enumerate(value))


def triangle_sides(value, where):
    sides = triple(value, where, positive=True)
    require(2 * max(sides) < sum(sides), f"{where}: triangle inequality fails")
    return sides


def edge_key(u, v):
    return (u, v) if u < v else (v, u)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def scale(t, p):
    return (t * p[0], t * p[1])


def determinant(p, q):
    return p[0] * q[1] - p[1] * q[0]


def dot(p, q, h):
    return p[0] * q[0] + h * p[1] * q[1]


def verify(obj):
    """Return a PASS report, or raise CertificateError on an invalid scheme.

    Every face is positively oriented: side j follows corner j to j+1.
    target_side_lengths[j] joins target_corners[j] to target_corners[j+1].
    Both lists are cyclic. Coordinates and atomic lengths are not input fields.
    """
    exact_keys(obj, {"schema", "tile_sides", "faces", "target_corners",
                     "target_side_lengths"}, "certificate")
    require(obj["schema"] == SCHEMA, f"certificate: unsupported schema {obj['schema']!r}")
    tile_sides = triangle_sides(obj["tile_sides"], "tile_sides")
    target_sides = triangle_sides(obj["target_side_lengths"], "target_side_lengths")
    target_corners = triple(obj["target_corners"], "target_corners")
    require(len(set(target_corners)) == 3, "target_corners: corners must be distinct")
    faces_input = obj["faces"]
    require(isinstance(faces_input, list) and faces_input, "faces: expected a nonempty list")

    # Each atom is identified by its two global endpoints. A face is a simple
    # polygon combinatorially; its flat vertices will lie on its original sides.
    face_sides = []
    face_chains = []
    face_polygons = []
    sides = {}
    side_atoms = {}
    atom_incidence = defaultdict(list)
    genuine_vertices = set()
    flat_count = Counter()
    vertices = set()
    for f, face in enumerate(faces_input):
        exact_keys(face, {"side_lengths", "side_vertices"}, f"face {f}")
        lengths = triangle_sides(face["side_lengths"], f"face {f} side_lengths")
        require(sorted(lengths) == sorted(tile_sides), f"face {f}: tile is not congruent")
        chains = face["side_vertices"]
        require(isinstance(chains, list) and len(chains) == 3,
                f"face {f}: expected three side vertex chains")
        for j, chain in enumerate(chains):
            require(isinstance(chain, list) and len(chain) >= 2,
                    f"face {f} side {j}: expected at least two vertices")
            for k, v in enumerate(chain):
                integer(v, f"face {f} side {j} vertex {k}")
        for j, chain in enumerate(chains):
            require(chain[-1] == chains[(j + 1) % 3][0],
                    f"face {f}: side endpoints do not form a cyclic triangle")
        polygon = [v for chain in chains for v in chain[:-1]]
        require(len(set(polygon)) == len(polygon), f"face {f}: repeated polygon vertex")
        genuine_vertices.update(chain[0] for chain in chains)
        vertices.update(polygon)
        for j, chain in enumerate(chains):
            sid = (f, j)
            sides[sid] = lengths[j]
            atoms = []
            flat_count.update(chain[1:-1])
            for u, v in zip(chain, chain[1:]):
                atom = edge_key(u, v)
                atoms.append(atom)
                atom_incidence[atom].append((f, j, u, v))
            side_atoms[sid] = atoms
        face_sides.append(lengths)
        face_chains.append(chains)
        face_polygons.append(polygon)
    require(genuine_vertices == vertices,
            "every subdivision vertex must be an original triangle corner somewhere")

    # Orientation, dual connectivity, and the unique simple boundary cycle.
    boundary = []
    dual = defaultdict(list)
    for atom, inc in atom_incidence.items():
        require(len(inc) in (1, 2), f"atom {atom}: expected one or two incident faces")
        if len(inc) == 1:
            boundary.append((inc[0][2], inc[0][3]))
        else:
            left, right = inc
            require(left[0] != right[0], f"atom {atom}: two incidences from the same face")
            require((left[2], left[3]) == (right[3], right[2]),
                    f"atom {atom}: interior incidences must have opposite orientations")
            dual[left[0]].append((right[0], atom))
            dual[right[0]].append((left[0], atom))
    n = len(face_sides)
    reached = {0}
    todo = [0]
    while todo:
        f = todo.pop()
        for g, _ in dual[f]:
            if g not in reached:
                reached.add(g)
                todo.append(g)
    require(len(reached) == n, "face dual graph is disconnected")
    require(boundary, "the complex has no boundary")
    outgoing = {}
    incoming = {}
    for u, v in boundary:
        require(u not in outgoing and v not in incoming,
                "boundary is not a disjoint union of simple directed cycles")
        outgoing[u] = v
        incoming[v] = u
    require(set(outgoing) == set(incoming), "boundary chains do not close")
    require(set(target_corners) <= set(outgoing), "target corners must lie on the boundary")
    start = target_corners[0]
    boundary_cycle = []
    v = start
    while v not in boundary_cycle:
        boundary_cycle.append(v)
        v = outgoing[v]
    require(v == start and len(boundary_cycle) == len(boundary),
            "boundary must be exactly one simple cycle")
    boundary_vertices = set(boundary_cycle)

    # Link nodes are edge germs, not neighboring face IDs. Keeping parallel
    # link edges is essential for valid valence-two vertices.
    links = defaultdict(lambda: defaultdict(list))
    for polygon in face_polygons:
        for i, v in enumerate(polygon):
            before = edge_key(polygon[i - 1], v)
            after = edge_key(v, polygon[(i + 1) % len(polygon)])
            links[v][before].append(after)
            links[v][after].append(before)
    for v in vertices:
        link = links[v]
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            germ = todo.pop()
            for other in link[germ]:
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
        require(len(seen) == len(link), f"vertex {v}: disconnected link")
        degrees = [len(neighbors) for neighbors in link.values()]
        if v in boundary_vertices:
            require(degrees.count(1) == 2 and all(d in (1, 2) for d in degrees),
                    f"boundary vertex {v}: link is not a single interval")
            ends = {germ for germ, neighbors in link.items() if len(neighbors) == 1}
            require(all(len(atom_incidence[e]) == 1 for e in ends),
                    f"boundary vertex {v}: link endpoints are not boundary edge germs")
        else:
            require(all(d == 2 for d in degrees),
                    f"interior vertex {v}: link is not a single cycle")
    require(len(vertices) - len(atom_incidence) + n == 1,
            "Euler characteristic is not one")

    # Whole original sides are boundary segments or lie entirely on seams.
    # An internal atom joins its two original side nodes. Recovering its
    # length needs just the forest and the whole side lengths.
    atom_lengths = {}
    contact = defaultdict(dict)
    for sid, atoms in side_atoms.items():
        counts = {len(atom_incidence[e]) for e in atoms}
        require(len(counts) == 1, f"side {sid}: partly boundary original side")
        if counts == {1}:
            require(len(atoms) == 1, f"side {sid}: subdivided boundary original side")
            atom_lengths[atoms[0]] = sides[sid]
    for atom, inc in atom_incidence.items():
        if len(inc) == 2:
            s, t = inc[0][:2], inc[1][:2]
            require(t not in contact[s], f"atom {atom}: parallel side contacts form a cycle")
            contact[s][t] = atom
            contact[t][s] = atom
    unseen = set(contact)
    component_sizes = []
    while unseen:
        seed = min(unseen)
        comp = {seed}
        todo = [seed]
        unseen.remove(seed)
        while todo:
            s = todo.pop()
            for t in contact[s]:
                if t not in comp:
                    comp.add(t)
                    unseen.remove(t)
                    todo.append(t)
        edge_count = sum(len(contact[s]) for s in comp) // 2
        require(edge_count == len(comp) - 1, "original-side contact graph is not a forest")
        for s in comp:
            if len(contact[s]) >= 2:
                require(sum(len(contact[t]) >= 2 for t in contact[s]) <= 2,
                        f"side-contact component at {s}: nonleaf core is not a path")
        component_sizes.append(len(comp))
        remainder = {s: sides[s] for s in comp}
        active = {s: set(contact[s]) for s in comp}
        leaves = deque(sorted(s for s in comp if len(active[s]) == 1))
        recovered = 0
        while leaves:
            s = leaves.popleft()
            if len(active[s]) != 1:
                continue
            t = next(iter(active[s]))
            length = remainder[s]
            require(length > 0, f"side {s}: recovered atomic length is not positive")
            atom_lengths[contact[s][t]] = length
            recovered += 1
            remainder[t] -= length
            remainder[s] = 0
            active[t].remove(s)
            active[s].clear()
            if len(active[t]) == 1:
                leaves.append(t)
        require(recovered == edge_count and all(x == 0 for x in remainder.values()),
                "whole side lengths are inconsistent with leaf elimination")
    require(len(atom_lengths) == len(atom_incidence), "some atomic lengths were not recovered")
    for sid, atoms in side_atoms.items():
        require(sum(atom_lengths[e] for e in atoms) == sides[sid],
                f"side {sid}: reconstructed atomic lengths have an incorrect sum")

    # In this rational coordinate model a pair (x,y) denotes (x,sqrt(H)*y).
    # H=16*area(tile)^2 is integral. Every local point and every rotation
    # coefficient below is rational, including after arbitrarily many seams.
    a, b, c = tile_sides
    h = 2 * (a*a*b*b + b*b*c*c + c*c*a*a) - a**4 - b**4 - c**4
    require(h > 0, "tile has zero or negative squared area")
    local = []
    zero = Fraction(0)
    for f, lengths in enumerate(face_sides):
        s0, s1, s2 = lengths
        corners = [(zero, zero), (Fraction(s0), zero),
                   (Fraction(s0*s0 + s2*s2 - s1*s1, 2*s0), Fraction(1, 2*s0))]
        points = {}
        for j, chain in enumerate(face_chains[f]):
            p, q = corners[j], corners[(j + 1) % 3]
            offset = 0
            for k, v in enumerate(chain):
                point = add(p, scale(Fraction(offset, lengths[j]), sub(q, p)))
                require(v not in points or points[v] == point,
                        f"face {f}: inconsistent local corner")
                points[v] = point
                if k + 1 < len(chain):
                    offset += atom_lengths[edge_key(v, chain[k + 1])]
        local.append(points)

    developed = dict(local[0])
    placed = {0}
    queue = deque([0])
    while queue:
        f = queue.popleft()
        for g, atom in dual[f]:
            if g in placed:
                continue
            u, v = atom
            p, q = local[g][u], local[g][v]
            image_p, image_q = developed[u], developed[v]
            d, e = sub(q, p), sub(image_q, image_p)
            length_squared = dot(d, d, h)
            require(length_squared > 0 and dot(e, e, h) == length_squared,
                    f"face {g}: shared edge lengths differ during development")
            rotation_a = dot(e, d, h) / length_squared
            rotation_b = determinant(d, e) / length_squared
            require(rotation_a**2 + h * rotation_b**2 == 1,
                    f"face {g}: development is not an exact isometry")
            for w, point in local[g].items():
                x, y = sub(point, p)
                image = add(image_p, (rotation_a*x - h*rotation_b*y,
                                      rotation_b*x + rotation_a*y))
                require(w not in developed or developed[w] == image,
                        f"vertex {w}: inconsistent exact development (holonomy)")
                developed[w] = image
            placed.add(g)
            queue.append(g)
    require(len(placed) == n and set(developed) == vertices,
            "exact development did not reach the entire disk")

    # A developed boundary must follow each of the three target sides strictly
    # forward. Merely closing the development would allow multiple winding.
    i1, i2 = (boundary_cycle.index(v) for v in target_corners[1:])
    require(0 < i1 < i2, "marked target corners have the wrong boundary order")
    cuts = [0, i1, i2, len(boundary_cycle)]
    closed_boundary = boundary_cycle + [start]
    for j in range(3):
        chain = closed_boundary[cuts[j]:cuts[j + 1] + 1]
        p, q = developed[chain[0]], developed[chain[-1]]
        direction = sub(q, p)
        require(dot(direction, direction, h) == target_sides[j]**2,
                f"target side {j}: developed length is incorrect")
        length_sum = 0
        for u, v in zip(chain, chain[1:]):
            step = sub(developed[v], developed[u])
            require(determinant(direction, step) == 0 and dot(direction, step, h) > 0,
                    f"target side {j}: boundary is not straight and strictly forward")
            require(determinant(direction, sub(developed[u], p)) == 0,
                    f"target side {j}: boundary vertex is off the target side")
            length_sum += atom_lengths[edge_key(u, v)]
        require(length_sum == target_sides[j],
                f"target side {j}: boundary atom lengths have an incorrect sum")
    p, q, r = (developed[v] for v in target_corners)
    require(determinant(sub(q, p), sub(r, p)) > 0,
            "developed target triangle is not positively oriented")

    # The checks above supply all hypotheses of the degree-one disk lemma.
    # These additional identities are redundant, inexpensive consistency checks.
    require(len(set(developed.values())) == len(developed),
            "distinct abstract vertices have coincident developed positions")
    target_a, target_b, target_c = target_sides
    target_h = (2 * (target_a**2*target_b**2 + target_b**2*target_c**2
                     + target_c**2*target_a**2)
                - target_a**4 - target_b**4 - target_c**4)
    require(target_h == n*n*h, "target area is not the sum of the tile areas")
    require(all(flat_count[v] == 0 for v in boundary_vertices),
            "a boundary vertex is flat in a tile")
    require(all(flat_count[v] <= 1 for v in vertices - boundary_vertices),
            "an interior vertex is flat in more than one tile")

    return {
        "status": "PASS",
        "schema": SCHEMA,
        "scope": "verification of the supplied finite abstract disk certificate",
        "N": n,
        "tile_sides": list(tile_sides),
        "target_side_lengths": list(target_sides),
        "vertices": len(vertices),
        "atomic_edges": len(atom_incidence),
        "boundary_atoms": len(boundary),
        "interior_atoms": len(atom_incidence) - len(boundary),
        "interior_T_junctions": sum(flat_count[v] == 1 for v in vertices - boundary_vertices),
        "original_tile_sides": 3*n,
        "side_contact_tree_components": len(component_sizes),
        "side_contact_component_sizes": dict(sorted(Counter(component_sizes).items())),
        "length_histogram": dict(sorted(Counter(atom_lengths.values()).items())),
        "coordinate_field_radicand": h,
        "coordinate_free_input": True,
        "all_atom_lengths_integer": True,
        "all_internal_atom_lengths_recovered_by_integer_leaf_elimination": True,
        "side_contact_components_are_caterpillars": True,
        "abstract_complex_is_oriented_disk": True,
        "exact_development_consistent": True,
        "boundary_maps_homeomorphically_to_target_triangle": True,
        "geometric_nonoverlap_certified_by_degree_one": True,
        "full_Erdos634_solved": False,
    }


verify_certificate = verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="coordinate-free JSON certificate")
    parser.add_argument("--report", "--output", type=Path,
                        help="write the verification report as JSON")
    args = parser.parse_args()
    try:
        raw = args.input.read_bytes()
        obj = json.loads(raw)
        report = verify(obj)
        report["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    except (CertificateError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.write_text(output)
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
