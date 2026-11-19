"""Compute the exact largest sum of 180 individual scores in the full pool."""
from gzip import open as gzip_open
from heapq import nlargest
from math import gcd
from pathlib import Path


def axis(p, q):
    x, y = q[0] - p[0], q[1] - p[1]
    g = gcd(x, y)
    if (x, y) < (0, 0):
        g = -g
    return x // g, y // g


def stamped_vertices(triangle):
    outgoing = [axis(p, triangle[(k + 1) % 3]) for k, p in enumerate(triangle)]
    return [(x, y, outgoing[k], outgoing[k - 1]) for k, (x, y) in enumerate(triangle)]


def score(stamps, weights, dx=0, dy=0):
    return sum(
        weights.get((x + dx, y + dy, *outgoing), 0)
        - weights.get((x + dx, y + dy, *incoming), 0)
        for x, y, outgoing, incoming in stamps
    )


def main():
    folder = Path(__file__).resolve().parents[1] / "theta6lp"
    with gzip_open(folder / "d729-weights.tsv.gz", "rt") as source:
        weights = {}
        for line in source:
            x, y, r, s, w = map(int, line.split())
            assert (x, y, r, s) not in weights
            weights[x, y, r, s] = w
    with (folder / "candidates.dat.shapes").open() as source:
        d, n, count = map(int, source.readline().split())
        templates = []
        for line in source:
            a, b, c, e = map(int, line.split())
            templates.append(stamped_vertices([(0, 0), (a, b), (c, e)]))
    assert (d, n, count) == (729, 180, len(templates))
    with gzip_open(folder / "candidates.dat.gz", "rt") as source:
        assert tuple(map(int, source.readline().split())) == (729, 180, 146434)
        scores = []
        for line in source:
            k, x, y = map(int, line.split())
            scores.append(score(templates[k], weights, x, y))
    assert len(scores) == 146434
    board = score(stamped_vertices([(0, 0), (60*d, 0), (30*d, 60*d)]), weights)
    largest = nlargest(n, scores)
    assert board > sum(largest)
    print(f"board {board}, top {n} sum {sum(largest)}, gap {board - sum(largest)}")
    print(f"maximum {largest[0]}, cutoff {largest[-1]}")


if __name__ == "__main__":
    main()
