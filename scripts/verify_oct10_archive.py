#!/usr/bin/env python3
"""Verify source integrity of the 9-10 October 2026 Erdos 634 archive.

SHA-256 data validation does not certify the mathematical claims.
"""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
BASE = "research/updates-2026-10-10"
ARCHIVE = ROOT / BASE / "packages/Erdos634_complete_updates_2026-10-10.zip"
EXPECTED_SHA256 = "fda301389453d0579d45c595e59552769baf363138084444d4df07ee26a8d048"
EXPECTED_FILES = 242
EXPECTED_EXPANDED = 220

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    raw = ARCHIVE.read_bytes()
    assert digest(raw) == EXPECTED_SHA256, "Archive SHA256 does not match release"
    mirrored = 0
    with zipfile.ZipFile(ARCHIVE) as bundle:
        assert bundle.testzip() is None, "Corrupt archive member"
        manifest = json.loads(bundle.read("MANIFEST.json"))
        records = manifest["files"]
        assert len(records) == EXPECTED_FILES, "Unexpected number of source files"
        assert len(manifest["source_archives"]) == 10
        assert len({r["path"] for r in records}) == EXPECTED_FILES
        for r in records:
            raw_file = bundle.read(r["path"])
            assert len(raw_file) == r["size"], "Bad size: " + r["path"]
            assert digest(raw_file) == r["sha256"], "Bad hash: " + r["path"]
            is_text = False
            if r["size"] <= 100000:
                try:
                    raw_file.decode("utf-8")
                    is_text = True
                except UnicodeDecodeError:
                    pass
            if is_text:
                relative = r["path"].removeprefix("sources/")
                path = ROOT / BASE / "expanded" / relative
                assert path.is_file(), "Expanded path missing: " + str(path)
                assert digest(path.read_bytes()) == r["sha256"], "Expanded data changed: " + str(path)
                mirrored += 1
    assert mirrored == EXPECTED_EXPANDED, "Wrong number of expanded entries"
    print(f"OCT10_ARCHIVE=PASS original_files={EXPECTED_FILES} expanded_files={mirrored} SHA256={EXPECTED_SHA256}")
    print("SCOPE: source integrity only; not a proof of any global tiling claim")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print("OCT10_ARCHIVE=FAIL", str(error), file=sys.stderr)
        sys.exit(1)
