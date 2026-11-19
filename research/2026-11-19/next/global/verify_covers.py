"""Verify angular interval certificates directly on their supplied endpoints."""

import json
from fractions import Fraction
from pathlib import Path

root = Path(__file__).resolve().parent
records = json.loads((root / "small_scale_results.json").read_text())
intervals = 0
for record in records:
    d, m, h = record["D"], record["M"], record["h"]
    assert record["multiplier"] == m*m*h
    low, high = Fraction(1, m), 1-Fraction(1, m-1)
    covered = Fraction(0)
    for interval in record["intervals"]:
        a, b = interval["a"], interval["b"]
        left, right = Fraction(interval["left"]), Fraction(interval["right"])
        assert 0 <= left <= covered < right <= 1
        assert a > 0 and a*a - d*b*b == h > 0
        values = [(a*r+d*b)/(a+b*r) for r in (left, right)]
        assert values[0] <= values[1] and values[0]*values[1] > 0
        assert all(low <= abs(y) <= high for y in values)
        covered = right
        intervals += 1
    assert covered == 1
print(f"Verified {intervals} rational intervals in {len(records)} complete covers.")
