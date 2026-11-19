"""Replay the finite November checks from a clean repository checkout."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent

def run_python(script):
    return subprocess.check_output([sys.executable, str(ROOT / script)], text=True)

def check_json(script, expected):
    actual = json.loads(run_python(script))
    reference = json.loads((ROOT / expected).read_text())
    if actual != reference:
        raise ValueError(f"Unexpected result from {script}")
    return actual

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild-236", action="store_true")
    rebuild = parser.parse_args().rebuild_236
    if not __debug__:
        raise RuntimeError("Use Python without -O to enable all certificate checks.")
    manifest = json.loads((ROOT / "SHA256.json").read_text())
    for path, expected in manifest.items():
        if sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"File digest mismatch for {path}")
    counts = check_json("next/global/census279.py", "next/global/census279.json")
    assert counts["interval_through_279"] == {"YES": 139, "NO": 140}
    check_json("next/global/replay_census_positive.py", "next/global/replayed_census_positive.json")
    check_json("check_paliy_examples.py", "paliy_examples.json")
    print(f"Verified {len(manifest)} files. Census through 279: 139 positive, 140 negative.")
    print("Exact positive coordinate witnesses verified for 240, 264, 322 and 897.")
    check_json("structural/verify.py", "structural/verification.json")
    check_json("structural/verify_gluing_boundaries.py", "structural/gluing_boundaries.json")
    for script in ("positive280/verify.py", "positive280/verify_slices.py",
                   "structural/census_extension.py", "structural/verify_two_scale.py"):
        print(run_python(script).strip(), flush=True)
    for script in ("next/alpha136mesh/recheck_direct.py", "next/theta6/reproduce.py",
                   "next/audit/transfer280/packing.py", "next/alpha280mesh/corner_patterns.py"):
        print(run_python(script).strip(), flush=True)
    if rebuild:
        source = ROOT / "next/beta/mesh_replay.cpp"
        with TemporaryDirectory() as tmp:
            program = Path(tmp) / "mesh236"
            subprocess.run(["g++", "-O3", "-std=c++20", "-DWIDE_INIT", str(source),
                            "-lgmpxx", "-lgmp", "-o", str(program)], check=True)
            trace = subprocess.check_output([str(program), "52", "25", "55", "2", "36", "0"],
                                            stderr=subprocess.STDOUT, text=True)
        expected = (ROOT / "next/beta/unbounded-no-clearance.log").read_text()
        if trace.splitlines() != expected.splitlines():
            raise ValueError("The 236 trace does not reproduce.")
        print("The 236 certificate reproduced. The apex loses its final admissible fan on pass 29.")

if __name__ == "__main__":
    main()
