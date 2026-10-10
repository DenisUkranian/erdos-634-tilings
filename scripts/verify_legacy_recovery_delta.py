#!/usr/bin/env python3
"""Check all 236 historical Sep-30 recovery records (byte integrity, not proof)."""
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "5a4b2aa9c5e3839767b23879716bffd8bc3d65cb"
ARCH = ROOT / "research/legacy-snapshots/2026-09-30/Erdos634_legacy_recovery_delta_2026-09-30.zip"
SHA256 = "ff2b52424e0bc8a1bf43838a5eb9ad4c75054b1cc98ed2a0522041e0eaac18ae"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main():
    if sha(ARCH.read_bytes()) != SHA256:
        raise AssertionError("Archive SHA-256 mismatch")
    n=0
    with zipfile.ZipFile(ARCH) as z:
        assert z.testzip() is None
        manifest=json.loads(z.read("MANIFEST.json"))
        assert len(manifest["records"]) == 236
        assert manifest["included_files"] == 94
        for r in manifest["records"]:
            if r["stored_path"]:
                data=z.read(r["stored_path"])
            else:
                p=ROOT / r["legacy_git_path"]
                if p.is_file() and sha(p.read_bytes()) == r["sha256"]:
                    data=p.read_bytes()
                else:
                    data=subprocess.check_output(["git", "-C", str(ROOT), "show", BASE+":"+r["legacy_git_path"]])
            assert len(data) == r["size"], r["source_archive_path"]
            assert sha(data) == r["sha256"], r["source_archive_path"]
            assert git_sha(data) == r["git_blob_sha1"], r["source_archive_path"]
            n += 1
    print("LEGACY_RECOVERY=PASS", "files="+str(n), "delta=94", "existing=142")
    print("Scope: source bytes only. Earlier mathematical proofs require independent validation.")

if __name__ == "__main__":
    main()
