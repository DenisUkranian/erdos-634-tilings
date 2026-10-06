#!/usr/bin/env python3
"""Export the retained geometric N=322 witness to coordinate-free disk data.

Only this exporter reads coordinates.  The resulting certificate supplies
integer side lengths, ordered incidence lists and target-corner IDs; it
supplies neither coordinates nor atomic segment lengths to verify_disk.py.
The exporter does not replace independent validation of either certificate.
"""

import argparse
from collections import Counter
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "data/tiling-322.json"
DEFAULT_DESTINATION = Path(__file__).with_name("disk-322.json")


def cross(a, b, p):
    return ((b[0] - a[0]) * (p[1] - a[1])
            - (b[1] - a[1]) * (p[0] - a[0]))


def ccw(points):
    points = [tuple(p) for p in points]
    if len(points) != 3 or cross(*points) == 0:
        raise ValueError("Every source face and the target must be a triangle")
    return points if cross(*points) > 0 else [points[0], points[2], points[1]]


def on_segment(a, b, p):
    return (cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def export(obj):
    if (obj["N"], obj["D"], obj["denominator"]) != (322, 32, 18):
        raise ValueError("Expected the retained N=322 source coordinate model")
    tiles = [ccw(face) for face in obj["tiles"]]
    target = ccw(obj["target"])
    if len(tiles) != 322:
        raise ValueError("Wrong source tile count")
    vertices = sorted({p for face in tiles for p in face})
    ids = {p: i for i, p in enumerate(vertices)}
    if not set(target) <= set(vertices):
        raise ValueError("Target corners must be genuine tile vertices")

    def length(a, b):
        squared = (a[0] - b[0]) ** 2 + 32 * (a[1] - b[1]) ** 2
        numerator = isqrt(squared)
        if numerator <= 0 or numerator ** 2 != squared or numerator % 18:
            raise ValueError("Source edge does not have positive integer length")
        return numerator // 18

    def split_side(a, b):
        points = [p for p in vertices if on_segment(a, b, p)]
        points.sort(key=lambda p: ((p[0] - a[0]) * (b[0] - a[0])
                                   + (p[1] - a[1]) * (b[1] - a[1])))
        if points[0] != a or points[-1] != b:
            raise ValueError("Source side endpoint missing")
        # This exporter check is useful, but these atomic lengths are
        # intentionally omitted from the exported certificate.
        if sum(length(p, q) for p, q in zip(points, points[1:])) != length(a, b):
            raise ValueError("Source side subdivision does not preserve length")
        return [ids[p] for p in points]

    faces = []
    for tile in tiles:
        edges = list(zip(tile, tile[1:] + tile[:1]))
        lengths = [length(a, b) for a, b in edges]
        if sorted(lengths) != [5, 6, 9]:
            raise ValueError("Source contains a noncongruent face")
        faces.append({"side_lengths": lengths,
                      "side_vertices": [split_side(a, b) for a, b in edges]})
    return {
        "schema": "integer-triangle-disk-v1",
        "tile_sides": [5, 6, 9],
        "faces": faces,
        "target_corners": [ids[p] for p in target],
        "target_side_lengths": [length(a, b)
                                for a, b in zip(target, target[1:] + target[:1])],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args()
    source_raw = args.source.read_bytes()
    certificate = export(json.loads(source_raw))
    output = (json.dumps(certificate, indent=2) + "\n").encode()
    args.output.write_bytes(output)
    flat = Counter(v for f in certificate["faces"]
                   for side in f["side_vertices"] for v in side[1:-1])
    print(json.dumps({"status": "EXPORTED", "N": len(certificate["faces"]),
                      "genuine_T_junction_vertices": len(flat),
                      "source_sha256": hashlib.sha256(source_raw).hexdigest(),
                      "export_sha256": hashlib.sha256(output).hexdigest(),
                      "coordinates_in_export": False,
                      "atomic_lengths_in_export": False}, indent=2))


if __name__ == "__main__":
    main()
