#!/usr/bin/env python3
"""Independent positive and adversarial tests for the abstract disk verifier.

N=1 and N=4 are hand-written incidence certificates. The cone examples are
topological disks with balanced lengths: a six-sector 3-4-5 fan has angle
3*pi at its center, while an eight-sector fan develops around it twice
(4*pi) with trivial holonomy. Neither is a genuine triangular tiling.
No coordinates are added to any input of verify_disk.py.
"""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from verify_disk import CertificateError, verify_certificate
from export_322 import DEFAULT_SOURCE, export

HERE = Path(__file__).resolve().parent


def face(corners, lengths):
    return {"side_lengths": list(lengths),
            "side_vertices": [[corners[i], corners[(i + 1) % 3]]
                              for i in range(3)]}


def certificate(faces, corners, sides, tile_sides=(3, 4, 5)):
    return {"schema": "integer-triangle-disk-v1",
            "tile_sides": list(tile_sides), "faces": faces,
            "target_corners": list(corners),
            "target_side_lengths": list(sides)}


def single_triangle():
    return certificate([face((0, 1, 2), (4, 5, 3))], (0, 1, 2), (4, 5, 3))


def four_triangles():
    # 0,1,2 are the outer corners; 3,4,5 are their successive midpoints.
    return certificate([face((0, 3, 5), (4, 5, 3)),
                        face((3, 1, 4), (4, 5, 3)),
                        face((5, 4, 2), (4, 5, 3)),
                        face((3, 4, 5), (3, 4, 5))],
                       (0, 1, 2), (8, 10, 6))


def triangular_grid(k, remove_interior=False):
    # Pure combinatorial grid indexing. All tile lengths are one.
    ids = {(i, j): v for v, (i, j) in enumerate(
        (i, j) for i in range(k + 1) for j in range(k + 1 - i))}
    faces = []
    for i in range(k):
        for j in range(k - i):
            if not (remove_interior and (i, j) == (1, 1)):
                faces.append(face((ids[i, j], ids[i + 1, j], ids[i, j + 1]),
                                  (1, 1, 1)))
            if i + j < k - 1:
                faces.append(face((ids[i + 1, j], ids[i + 1, j + 1], ids[i, j + 1]),
                                  (1, 1, 1)))
    return certificate(faces, (ids[0, 0], ids[k, 0], ids[0, k]),
                       (k, k, k), (1, 1, 1))


def cone_disk(k):
    if k % 2 or k < 4:
        raise ValueError("The alternating-radius cone needs an even number of sectors")
    faces = [face((0, i, i % k + 1), (3, 5, 4) if i % 2 else (4, 5, 3))
             for i in range(1, k + 1)]
    if k == 8:
        # These marked vertices really develop to a positively oriented
        # triangle with side lengths 5,5,6. Even that is insufficient:
        # the final boundary arc winds around instead of being straight.
        return certificate(faces, (1, 2, 3), (5, 5, 6))
    gap = (k + 1) // 3
    return certificate(faces, (1, 1 + gap, 1 + 2 * gap),
                       (5 * gap, 5 * gap, (k - 2 * gap) * 5))


def reverse_face(f):
    f["side_vertices"] = [list(reversed(side)) for side in reversed(f["side_vertices"])]
    f["side_lengths"] = list(reversed(f["side_lengths"]))


def renumber(obj, offset):
    obj = deepcopy(obj)
    for f in obj["faces"]:
        f["side_vertices"] = [[v + offset for v in side] for side in f["side_vertices"]]
    obj["target_corners"] = [v + offset for v in obj["target_corners"]]
    return obj


def negative_fixtures(disk322):
    tests = []
    obj = single_triangle()
    obj["coordinates"] = [[0, 0], [4, 0], [0, 3]]
    tests.append(("coordinate_payload_forbidden", obj))

    obj = single_triangle()
    obj["target_side_lengths"][0] += 1
    tests.append(("wrong_target_length", obj))

    obj = four_triangles()
    obj["target_corners"] = [0, 2, 1]
    obj["target_side_lengths"] = [6, 10, 8]
    tests.append(("reversed_boundary_orientation", obj))

    obj = four_triangles()
    obj["target_corners"] = [0, 3, 2]
    tests.append(("flat_boundary_vertex_claimed_as_corner", obj))

    obj = four_triangles()
    reverse_face(obj["faces"][-1])
    tests.append(("one_face_reversed", obj))

    obj = four_triangles()
    obj["faces"][-1]["side_lengths"] = [4, 3, 5]
    tests.append(("inconsistent_side_balance", obj))

    obj = four_triangles()
    obj["faces"].append(deepcopy(obj["faces"][-1]))
    tests.append(("triple_edge_incidence", obj))

    obj = four_triangles()
    obj["faces"].extend(renumber(single_triangle(), 10)["faces"])
    tests.append(("disconnected_component", obj))

    obj = single_triangle()
    obj["faces"].append(face((0, 3, 4), (4, 5, 3)))
    tests.append(("two_disks_pinched_at_one_vertex", obj))

    tests.append(("annulus_with_two_boundary_cycles", triangular_grid(4, True)))
    tests.append(("cone_3pi_inconsistent_holonomy", cone_disk(6)))
    tests.append(("cone_4pi_trivial_holonomy_but_double_winding", cone_disk(8)))

    obj = deepcopy(disk322)
    for f in obj["faces"]:
        side = next((s for s in f["side_vertices"] if len(s) > 2), None)
        if side is not None:
            del side[1]
            break
    tests.append(("missing_T_junction_incidence", obj))
    return tests


class DiskTests(unittest.TestCase):
    outcomes = []

    @classmethod
    def setUpClass(cls):
        cls.disk322 = json.loads((HERE / "disk-322.json").read_text())

    def test_export_is_reproducible(self):
        self.assertEqual(export(json.loads(DEFAULT_SOURCE.read_text())), self.disk322)
        self.assertEqual(set(self.disk322),
                         {"schema", "tile_sides", "faces", "target_corners", "target_side_lengths"})
        self.assertTrue(any(len(s) > 2 for f in self.disk322["faces"] for s in f["side_vertices"]))

    def test_valid_disks(self):
        for name, obj in [("single_345_triangle", single_triangle()),
                          ("four_345_triangles", four_triangles()),
                          ("sixteen_equilateral_triangles", triangular_grid(4)),
                          ("N322_with_24_T_junctions", self.disk322)]:
            with self.subTest(name=name):
                report = verify_certificate(obj)
                self.assertEqual(report["status"], "PASS")
                self.outcomes.append({"name": name, "expected": "accept", "actual": "accept"})

    def test_adversarial_disks(self):
        for name, obj in negative_fixtures(self.disk322):
            with self.subTest(name=name):
                with self.assertRaises(CertificateError) as caught:
                    verify_certificate(obj)
                self.outcomes.append({"name": name, "expected": "reject", "actual": "reject",
                                      "reason": str(caught.exception)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DiskTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL",
              "scope": "positive and adversarial abstract disk verifier checks",
              "full_Erdos634_solved": False,
              "cases": DiskTests.outcomes,
              "disk322_sha256": hashlib.sha256((HERE / "disk-322.json").read_bytes()).hexdigest()}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
