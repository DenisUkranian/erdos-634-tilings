"""Exact boundary-word spectra for a parity-balanced slant subtree."""
from argparse import ArgumentParser
from functools import lru_cache
import json
from pathlib import Path


def rotate(v):
    x, y = v
    return -y, x + y


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def units(v):
    for _ in range(6):
        yield v
        v = rotate(v)


def skeletons(letters, pairs):
    """Insert the mate of the first letter and recurse on the remaining word."""
    if not pairs:
        yield ()
        return
    for rest in skeletons(letters, pairs - 1):
        for i in range(len(rest) + 1):
            for x, y in letters:
                yield ((x, y),) + rest[:i] + ((-x, -y),) + rest[i:]


@lru_cache(maxsize=None)
def gap_sums(heights, c):
    """Bits for sums of c choices from heights, relative to c*min(heights)."""
    offsets = [h - heights[0] for h in heights]
    bits = 1
    for _ in range(c):
        new = 0
        for offset in offsets:
            new |= bits << offset
        bits = new
    return bits, c * heights[0]


def level(a, b, c, pairs):
    assert 4 * pairs * pairs < c
    base = a, b
    alphabet = tuple(units((c, 0))) + tuple(units(base))
    possibilities = set()
    words = 0
    for word in skeletons(alphabet, pairs):
        x = y = area = 0
        heights = {0}
        for u, v in word:
            area += det((x, y), (u, v))
            x, y = x + u, y + v
            value, rem = divmod(det((x, y), base), c)
            assert rem == 0
            heights.add(value)
        assert (x, y) == (0, 0)
        intercept, rem = divmod(area, 2 * c)
        assert rem == 0
        bits, shift = gap_sums(tuple(sorted(heights)), c)
        origin = intercept + shift
        for l in range(max(0, -(-origin // (a * b))),
                       (origin + bits.bit_length() - 1) // (a * b) + 1):
            if (bits >> (a * b * l - origin)) & 1:
                possibilities.add(l)
        words += 1
    return {"paired_orderings": words, "multipliers_of_2c": sorted(possibilities)}


def report():
    result = {}
    for a, b, c in [(5, 3, 7), (33, 7, 37), (35, 13, 43)]:
        n = (a + 2*b) * (2*a + b)
        rows = {}
        for r in range(4):
            if 4*r*r < c:
                rows[c+2*r] = level(a, b, c, r)
        result[n] = rows
    return result


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.dumps(report(), indent=2, sort_keys=True) + "\n"
    if args.check:
        assert data == Path(__file__).with_name("SPECTRA.json").read_text()
        print("Exact slant spectra reproduced.")
    else:
        print(data, end="")
