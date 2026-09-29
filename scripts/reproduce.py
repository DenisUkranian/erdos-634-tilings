#!/usr/bin/env python3
"""Complete offline replay of the release's finite computational evidence.

This does not verify the infinite geometric proofs or the global prime claim.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")

ROOT = Path(__file__).resolve().parents[1]


def run(*arguments):
    result = subprocess.run(
        [sys.executable, *arguments], cwd=ROOT,
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def verify_manifest():
    manifest = json.loads((ROOT / "verification/manifest.json").read_text())
    for relative, entry in manifest["files"].items():
        path = ROOT / relative
        if path.resolve().parent != ROOT.resolve() and ROOT.resolve() not in path.resolve().parents:
            raise ValueError(f"Unsafe manifest path: {relative}")
        data = path.read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError(f"Manifest mismatch: {relative}")
    return len(manifest["files"])


def main():
    file_count = verify_manifest()
    print(f"MANIFEST=PASS ({file_count} files)", flush=True)
    certificates = json.loads(run("scripts/check_certificates.py"))
    print("CONSTRUCTION_REPLAY=PASS (77, 322, 897 tiles)", flush=True)
    independent = json.loads(run("scripts/verify_322.py", "data/tiling-322.json"))
    print("INDEPENDENT_322_REPLAY=PASS (51681 pairs; T-junction seams checked)", flush=True)
    theta = [json.loads(line) for line in run("scripts/generate_theta.py", "--check").splitlines() if line]
    print("THETA_CONSTRUCTION_REPLAY=PASS (48, 75, 108, 147, 243, 300 tiles)", flush=True)
    theta_odd = json.loads(run("scripts/verify_theta_odd.py"))
    print("INDEPENDENT_THETA_ODD_REPLAY=PASS (2775, 10731 and 29403 pairs; seams checked)", flush=True)
    collars = json.loads(run("scripts/verify_n105_collars.py"))
    if collars.get("verdict") != "PASS" or collars.get("complete_tiling") is not False:
        raise ValueError("Unexpected partial-collar result or scope")
    print("N105_PARTIAL_COLLARS=PASS (990 and 1596 pairs; not complete tilings)", flush=True)
    collar_refutations = json.loads(run("scripts/verify_n105_collar_refutations.py"))
    if (collar_refutations.get("verdict") != "PASS"
            or collar_refutations.get("scope") != "two_fixed_collars_only"
            or collar_refutations.get("global_N105_decided") is not False):
        raise ValueError("Unexpected fixed-collar refutation result or scope")
    print("N105_FIXED_COLLAR_REFUTATIONS=PASS (one blocked corner in each fixed collar; no global N105 decision)", flush=True)
    local_fans = json.loads(run("scripts/verify_n105_local_fans.py"))
    if (local_fans.get("verdict") != "PASS_INDIVIDUAL_FULL_FANS_ONLY"
            or local_fans.get("fans_asserted_jointly_compatible") is not False
            or local_fans.get("global_N105_decided") is not False):
        raise ValueError("Unexpected individual-fan check result or scope")
    print("N105_INDIVIDUAL_FULL_FANS=PASS (18 separately fillable corners; joint compatibility not established)", flush=True)
    invariants = json.loads(run("scripts/check_n105_invariants.py"))
    print("N105_INVARIANT_CHECKS=PASS (exact branch arithmetic and formal boundary identity)", flush=True)
    bridges = [json.loads(line) for line in run("scripts/check_bridges.py").splitlines() if line]
    print(f"BRIDGE_REPLAY=PASS ({len(bridges)} exact examples)", flush=True)
    scale_bridges = [json.loads(line) for line in run("scripts/check_scale_bridges.py").splitlines() if line]
    print(f"W_BETA_BRIDGE_REPLAY=PASS ({len(scale_bridges)} exact examples)", flush=True)
    eventual = json.loads(run("scripts/check_eventual_families.py"))
    if eventual.get("status") != "PASS":
        raise ValueError("Unexpected eventual-family check result")
    print(f"EVENTUAL_FAMILY_MACRO_CHECKS=PASS ({eventual['general_macro_sweep']} macro cases; {eventual['transfer_parameter_pairs']} transfer parameter pairs; not individual-tile replay)", flush=True)
    annuli = json.loads(run("scripts/check_universal_annuli.py"))
    if annuli.get("status") != "PASS":
        raise ValueError("Unexpected universal annulus check result")
    print(f"UNIVERSAL_ANNULUS_MACRO_CHECKS=PASS ({annuli['primitive_parameter_pairs']} parameter pairs; two shell constructions; not individual-tile replay)", flush=True)
    explicit_seeds = json.loads(run("scripts/check_explicit_theta_seed.py"))
    if explicit_seeds.get("status") != "PASS":
        raise ValueError("Unexpected explicit theta seed check result")
    print(f"EXPLICIT_THETA_SEEDS=PASS ({explicit_seeds['negative_delta_cases']} negative-Delta macro cases; {explicit_seeds['positive_delta_cases']} positive-Delta interval cases)", flush=True)
    n21_arithmetic = json.loads(run("scripts/check_n21_reduction.py"))
    if n21_arithmetic.get("status") != "PASS":
        raise ValueError("Unexpected N21 arithmetic result")
    alpha21 = json.loads(run("scripts/verify_alpha21.py"))
    if alpha21.get("result") != "PASS":
        raise ValueError("Unexpected alpha21 refutation result")
    print(f"N21_REDUCTION_AND_REFUTATION=PASS (finite arithmetic; {alpha21['certificate_nodes']} certificate nodes; {alpha21['expanded_nodes_without_memoization']} independently expanded states)", flush=True)
    run("-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py")
    print("VERIFIER_REJECTION_TESTS=PASS (9 rejected cases; positive control accepted)", flush=True)
    report = {
        "status": "PASS", "manifest_files": file_count,
        "construction_certificates": certificates,
        "independent_322_replay": independent,
        "theta_certificates": theta,
        "independent_theta_odd_replay": theta_odd,
        "n105_partial_collars": collars,
        "n105_fixed_collar_refutations": collar_refutations,
        "n105_individual_full_fans": local_fans,
        "n105_invariant_checks": invariants,
        "bridge_examples": bridges,
        "w_beta_bridge_examples": scale_bridges,
        "eventual_family_macro_checks": eventual,
        "universal_annulus_macro_checks": annuli,
        "explicit_theta_seed_checks": explicit_seeds,
        "n21_arithmetic_reduction": n21_arithmetic,
        "alpha21_exact_refutation": alpha21,
        "rejection_cases": 9, "positive_controls": 1,
        "scope": "Finite certificates and implementation checks only; not formal verification of the prime-case candidate or full Erdős 634.",
    }
    (ROOT / "verification/replay.json").write_text(json.dumps(report, indent=2) + "\n")
    print("ERDOS634_FINITE_REPLAY=PASS")


if __name__ == "__main__":
    main()
