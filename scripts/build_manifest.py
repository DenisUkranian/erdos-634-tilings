#!/usr/bin/env python3
"""Freeze hashes before a release. Rebuilding hashes is not a mathematical check."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"verification/manifest.json", "verification/replay.json"}
files = {}
for path in sorted(ROOT.rglob("*")):
    relative = path.relative_to(ROOT)
    if not path.is_file() or any(part in {".git", "__pycache__", ".pytest_cache"} for part in relative.parts):
        continue
    if relative.as_posix() in EXCLUDED or path.suffix in {".pyc", ".aux", ".log", ".out"}:
        continue
    data = path.read_bytes()
    files[relative.as_posix()] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
manifest = {"format": 1, "algorithm": "SHA-256", "files": files}
(ROOT / "verification/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Manifest written for {len(files)} files")
