"""Check the CSV using exact vertical slices, independently of separating axes."""

import csv
from fractions import Fraction
from pathlib import Path


DENOMINATOR = 81
BOARD = ((0, 0), (140*81, 0), (70*81, 40*81))


def length_squares(triangle):
    return sorted((x-u)**2 + 2*(y-v)**2
                  for (x, y), (u, v) in zip(triangle, triangle[1:] + triangle[:1]))


def active_edges(triangle, x):
    """Represent each nonvertical edge meeting x by its affine height function."""
    lines = []
    for (u, v), (w, z) in zip(triangle, triangle[1:] + triangle[:1]):
        if min(u, w) < x < max(u, w):
            slope = Fraction(z-v, w-u)
            lines.append((slope, v - slope*u))
    if len(lines) not in (0, 2):
        raise ValueError("Unexpected number of edges crossing an open slab")
    return sorted(lines, key=lambda line: line[0]*x + line[1])


def verify(path):
    triangles = []
    with path.open(newline="", encoding="ascii") as source:
        rows = csv.DictReader(source)
        for row in rows:
            triangles.append(tuple((int(row[f"x{i}"]), int(row[f"y{i}"])) for i in (1, 2, 3)))
    if len(triangles) != 280:
        raise ValueError("Wrong tile count")
    if length_squares(BOARD) != [s*s*DENOMINATOR**2 for s in (90, 90, 140)]:
        raise ValueError("Wrong outer side lengths")
    for triangle in triangles:
        if length_squares(triangle) != [s*s*DENOMINATOR**2 for s in (5, 6, 9)]:
            raise ValueError("Wrong tile side lengths")
    cuts = sorted({x for triangle in [BOARD, *triangles] for x, _ in triangle})
    for left, right in zip(cuts, cuts[1:]):
        x = Fraction(left + right, 2)
        board = active_edges(BOARD, x)
        intervals = [active_edges(t, x) for t in triangles]
        intervals = [i for i in intervals if i]
        if not board:
            if intervals:
                raise ValueError("Tiles outside the board")
            continue
        if not intervals:
            raise ValueError("An open slab is empty")
        intervals.sort(key=lambda pair: pair[0][0]*x + pair[0][1])
        boundary = board[0]
        for lower, upper in intervals:
            # Equality of both affine coefficients checks the entire slab.
            if lower != boundary:
                raise ValueError(f"Unmatched slice boundary in slab ({left},{right})")
            boundary = upper
        if boundary != board[1]:
            raise ValueError("Slice chain does not reach the top of the board")
    return f"Exact coverage in all {len(cuts)-1} open slabs, with all 280 side triples checked."


if __name__ == "__main__":
    print(verify(Path(__file__).with_name("tiling_280.csv")))
