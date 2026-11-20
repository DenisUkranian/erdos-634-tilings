#!/usr/bin/env python3
"""Freeze hashes before a release; --package limits per-package updates.

The global manifest is always rebuilt. Rebuilding hashes is not a
mathematical check.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"verification/manifest.json", "verification/replay.json"}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package', action='append', help='Top-level research directory name; repeat as needed. Default: all packages.')
args = parser.parse_args()
selected = set(args.package or [])
for name in selected:
    if Path(name).name != name or not (ROOT/'research'/name).is_dir():
        parser.error(f'Unknown top-level research package: {name}')
# A deliberate publication freeze, never called automatically to hide a mismatch.
for package in sorted((ROOT / "research").glob("*")):
    if not package.is_dir() or (selected and package.name not in selected):
        continue
    lines = []
    for entry in sorted(package.rglob("*")):
        rel = entry.relative_to(package)
        if (not entry.is_file() or entry.name == "SHA256SUMS.txt"
                or any(part in {"__pycache__", "build", "audit-output"} for part in rel.parts)
                or entry.suffix in {".pyc", ".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk"}):
            continue
        lines.append(hashlib.sha256(entry.read_bytes()).hexdigest() + "  " + rel.as_posix())
    (package / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
files = {}
for path in sorted(ROOT.rglob("*")):
    relative = path.relative_to(ROOT)
    if not path.is_file() or any(part in {".git", "__pycache__", ".pytest_cache", "audit-output", "build", "dist", ".publication"} for part in relative.parts):
        continue
    if relative.as_posix() in EXCLUDED or path.suffix in {".pyc", ".aux", ".log", ".out"}:
        continue
    data = path.read_bytes()
    files[relative.as_posix()] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
manifest = {"format": 1, "algorithm": "SHA-256", "files": files}
(ROOT / "verification/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Manifest written for {len(files)} files")
