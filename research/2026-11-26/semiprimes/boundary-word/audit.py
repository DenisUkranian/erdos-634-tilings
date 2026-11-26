"""Audit rejected areas by ordering neutral steps, never using the inventory DP."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

from capacity import capacity
from spectrum import det, gap_sums, units

HERE = Path(__file__).resolve().parent


def words(counts, remaining, prefix):
    if not remaining:
        yield tuple(prefix)
        return
    for step in counts:
        if counts[step]:
            counts[step] -= 1
            prefix.append(step)
            yield from words(counts, remaining-1, prefix)
            prefix.pop()
            counts[step] += 1


def excludes(a, b, c, r, missing):
    base = a, b
    axes = tuple(units((c, 0)))[:3] + tuple(units(base))[:3]
    tried = 0
    for inv in combinations_with_replacement(axes, r):
        cap = c*sum(abs(det(v, base)) for v in inv)
        cap += sum(abs(det(v, w)) for v, w in combinations(inv, 2))
        targets = [a*b*k for k in missing if a*b*c*k <= cap]
        if not targets:
            continue
        counts = Counter(inv)
        counts.update((-x, -y) for x, y in inv)
        for word in words(counts, 2*r, []):
            path = [(0, 0)]
            for dx, dy in word:
                x, y = path[-1]
                path.append((x+dx, y+dy))
            assert path[-1] == (0, 0)
            area = sum(det(u, v) for u, v in zip(path, path[1:]))
            assert area % (2*c) == 0
            h = tuple(sorted({det(v, base)//c for v in path}))
            bits, lower = gap_sums(h, c)
            for target in targets:
                i = target - area//(2*c) - lower
                assert i < 0 or not ((bits >> i) & 1)
            tried += 1
    return tried


if __name__ == "__main__":
    large = json.loads((HERE/"INVENTORIES.json").read_text())
    small = json.loads((HERE/"SPECTRA.json").read_text())
    for a,b,c in [(5,3,7), (33,7,37), (35,13,43)]:
        n = str((a+2*b)*(2*a+b))
        total = 0
        for key, row in large[n].items():
            r = (int(key)-c)//2
            upper = capacity(a,b,c,r)
            assert upper == row["area_upper"]
            values = set(row["multipliers_of_2c"])
            if key in small[n]:
                assert values == set(small[n][key]["multipliers_of_2c"])
            missing = set(range(upper+1))-values
            if missing:
                total += excludes(a,b,c,r,missing)
        print(n, "ordered skeletons audited for exclusions", total)
