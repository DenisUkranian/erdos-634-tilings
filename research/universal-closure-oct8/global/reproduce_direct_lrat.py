#!/usr/bin/env python3
"""Generate native LRAT and check it with the separate drat-trim lrat-check.

The complete native DIMACS parser is intentional: it reserves input clause
identifiers before proof logging, including simplified input clauses.
No UNSAT conclusion is accepted from the solver alone.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("prefix", type=Path)
    parser.add_argument("--cadical", required=True)
    parser.add_argument("--checker", required=True)
    parser.add_argument("--seconds", type=int, default=2400)
    args = parser.parse_args()
    proof = Path(str(args.prefix) + ".lrat")
    solver_log = Path(str(args.prefix) + ".solver.log")
    check_log = Path(str(args.prefix) + ".check.log")
    command = [args.cadical, "--lrat", "--no-binary", "--factor=0",
               "-t", str(args.seconds), str(args.cnf), str(proof)]
    start = time.monotonic()
    with solver_log.open("w") as out:
        result = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT)
    report = {"command": command, "solver_exit": result.returncode,
              "solver_seconds": time.monotonic() - start,
              "cnf_sha256": sha256(args.cnf),
              "proof_sha256": sha256(proof) if proof.exists() else None,
              "status": "NOT_VERIFIED"}
    if result.returncode == 20:
        check_start = time.monotonic()
        with check_log.open("w") as out:
            checked = subprocess.run([args.checker, str(args.cnf), str(proof)],
                                     stdout=out, stderr=subprocess.STDOUT)
        report["checker_exit"] = checked.returncode
        report["check_seconds"] = time.monotonic() - check_start
        if checked.returncode == 0 and "c VERIFIED\n" in check_log.read_text():
            report["status"] = "VERIFIED_UNSAT"
    Path(str(args.prefix) + ".json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "VERIFIED_UNSAT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
