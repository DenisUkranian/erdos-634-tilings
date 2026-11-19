"""Four decisions supplementary to the frozen project census ending at 279."""

import json
from pathlib import Path


def main():
    november = Path(__file__).resolve().parents[1]
    previous = json.loads((november / "next/global/census279.json").read_text())
    old = {row["n"]: row["status"] for row in previous["entries"]}
    assert {n for n in old if n <= 279} == set(range(1, 280))
    assert old[70] == "NO"
    status = [old[n] for n in range(1, 280)]
    # 280: see the two independent geometric verifiers, run by ../verify.py.
    assert 16**2 + 5**2 == 281
    # Paliy's earlier squarefree-cofactor theorem for 6*47.
    assert 6*47 == 282 and 4*47 > 3*6**2 + 6*6 - 1 and 47 % 4 == 3
    assert all(47 % j for j in range(2, 7))
    # Beeson–Rosu's prime theorem for 283.
    assert all(283 % j for j in range(2, 17)) and 283 % 4 == 3
    new = {280: "YES", 281: "YES", 282: "NO", 283: "NO"}
    status.extend(new.values())
    assert status.count("YES") == 141 and status.count("NO") == 142
    return {"through": 283, "yes": 141, "no": 142, "additional": new}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    print(json.dumps(main(), indent=2))
