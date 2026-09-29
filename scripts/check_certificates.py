#!/usr/bin/env python3
"""Regenerate all three certificates and replay their exact geometry."""
import json
from pathlib import Path

from generate_tiling import construct, verify


def main():
    root = Path(__file__).resolve().parents[1]
    results = []
    for u, v, count in ((1, 2, 77), (2, 3, 322), (3, 4, 897)):
        path = root / "data" / f"tiling-{count}.json"
        saved = json.loads(path.read_text(encoding="utf-8"))
        rebuilt = json.loads(json.dumps(construct(u, v)))
        # Historical timing/check reports are not part of the geometric object.
        geometry = {key: value for key, value in saved.items() if key != "verification"}
        if geometry != rebuilt:
            raise ValueError(f"The frozen {count}-tile geometry differs from regeneration")
        result = verify(saved)
        result["deterministic_geometry_regeneration"] = "PASS"
        results.append(result)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
