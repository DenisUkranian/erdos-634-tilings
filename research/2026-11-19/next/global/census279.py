"""Resolve the arithmetic candidates from 201 through 279; retain source flags."""

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / "nov19" / "global"
sys.path.insert(0, str(OLD))
from decision import classify


def extra(n, shapes):
    if n == 236:
        assert shapes == [("beta", 4, 5, 0, 2)]
        return "NO", "current certificate for the unique beta target; see ../beta/MESH_PROOF.md"
    if n == 240:
        assert ("equilateral120", 3, 5, 7, 4) in shapes
        return "YES", "Paliy's equilateral 240 seed, 8 October"
    if n == 264:
        assert ("F3", 5, 3, 7, 1) in shapes and 3*(5+3)*(5+2*3) == n
        return "YES", "Paliy's all-multiplier F3 cone, a/b=5/3"
    reasons = set()
    for kind, e, f, _, t in shapes:
        if kind == "theta" and t < 4:
            reasons.add("theta base word")
        elif kind == "double" and f + e > (2*t - 1)*(f - e):
            reasons.add("Bonfioli's Theorem F")
        elif kind == "W" and (t*e < f or (t == 2 and (e, f) != (1, 2))):
            reasons.add("Bonfioli's W side condition or W-gap theorem")
        else:
            raise ValueError(f"Unresolved shape at {n}: {(kind, e, f, t)}")
    return "NO", ", ".join(sorted(reasons))


def build():
    positive200 = set(json.loads((OLD / "spectrum200.json").read_text())["positive"])
    entries = []
    for n in range(1, 281):
        item = classify(n)
        if n <= 200:
            verdict = "YES" if n in positive200 else "NO"
            assert verdict == item["verdict"]
            source = "Bonfioli, Theorem 1.3 (1 through 200)"
        elif n != 280 and item["verdict"] == "UNRESOLVED":
            verdict, source = extra(n, item["shapes"])
        else:
            verdict, source = item["verdict"], item["reason"]
        entry = {"n": n, "status": verdict, "source": source}
        if n == 236:
            entry["prior_v6_census"] = "UNDECIDED"
            entry["source_type"] = "current project computer-assisted exclusion"
        if n == 280:
            assert verdict == "UNRESOLVED" and item["shapes"] == [("alpha", 2, 3, 0, 2)]
            entry["prior_v6_census"] = "UNDECIDED"
        if item.get("shape"):
            entry["shape"] = item["shape"]
        entries.append(entry)
    return {
        "interval_through_279": dict(Counter(x["status"] for x in entries[:-1])),
        "positive_201_to_279": [x["n"] for x in entries[200:-1] if x["status"] == "YES"],
        "pinned_census": {
            "repository": "ElVec1o/erdos634_primes_and_N200",
            "commit": "752005605ca4e607d2a08f57bdc2445dd5558dbb",
            "path": "data/census/undecided_6.0.txt",
            "git_blob": "cefab9bf38ff38d0e586fb545c43ecaaba7d56d3",
            "scope": "non-squarefree N only; 52,045 undecided up to 1,000,000",
            "first_12": [236, 280, 284, 332, 351, 423, 444, 524, 531, 552, 594, 644],
        },
        "entries": entries,
    }


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
