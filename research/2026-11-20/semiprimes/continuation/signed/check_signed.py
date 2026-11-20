"""Check the triangle indicator recurrence coefficient by coefficient."""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

# This file is in semiprimes/continuation/signed inside the repository.
base = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(base))
from controls.dilation import instance, triple
from controls.verify_grids import check


def cells(n):
    result = Counter()
    for i in range(n):
        for j in range(n - i):
            result["up", i, j] = 1
            if i + j < n - 1:
                result["down", i, j] = 1
    return result

def add_shift(dest, src, dx, dy, sign):
    for (orientation, x, y), weight in src.items():
        dest[orientation, x + dx, y + dy] += sign * weight


def check_boards():
    macro_cells = Counter()
    records = [
        (4, 1, -1, -1), (3, -1, -1, -1), (3, -1, 0, -1),
        (3, -1, -1, 0), (2, 1, 0, -1), (2, 1, -1, 0), (2, 1, 0, 0),
    ]
    for h, sign, dx, dy in records:
        add_shift(macro_cells, cells(h), dx, dy, sign)
    if macro_cells != cells(1):
        raise ValueError("seven translated board indicators do not sum to the unit board")

    for n, u in [(3431, 10), (5063, 6)]:
        double_source = base / "controls" / f"double_{n}.json"
        grids = {2: json.loads(double_source.read_text()), 3: triple(u, 1),
                 4: instance(u, 1, 4)}
        counts = {}
        for h, grid in grids.items():
            counts[h] = check(grid)["count"]
            a, b, c = grid["tile"]
            expected = [[0, 0], [b * (2 * a + b), 0], [0, a * (a + 2 * b)]]
            target = [[Fraction(v, h * grid["coordinate_denominator"]) for v in point]
                      for point in grid["target"]]
            if target != expected or a*a+a*b+b*b != c*c or counts[h] != h*h*n:
                raise ValueError("inconsistent board normalization")
            if tuple(grid["tile"]) != tuple(grids[2]["tile"]):
                raise ValueError("the scale changed the tile")
        plus = sum(counts[h] for h, sign, dx, dy in records if sign == 1)
        minus = sum(counts[h] for h, sign, dx, dy in records if sign == -1)
        if (plus, minus) != (28*n, 27*n):
            raise ValueError("incorrect signed multiplicities")
        print(f"{n}: verified ordinary scales {list(counts.values())}, signed +{plus} -{minus}")


def main():
    if not __debug__:
        raise RuntimeError("enable Python assertions for the grid verifier")
    check_boards()
    for m in range(1, 101):
        result = Counter()
        for dx, dy in [(0, 0), (1, 0), (0, 1)]:
            add_shift(result, cells(m + 2), dx, dy, 1)
        for dx, dy in [(1, 0), (0, 1), (1, 1)]:
            add_shift(result, cells(m + 1), dx, dy, -1)
        add_shift(result, cells(m), 1, 1, 1)
        if result != cells(m + 3):
            raise ValueError(f"coefficient discrepancy at m={m}")
    print("PASS: both cell orientations agree at every position for m=1,...,100")

if __name__ == "__main__":
    main()
