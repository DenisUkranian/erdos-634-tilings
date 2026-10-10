#!/usr/bin/env python3
"""Restore/check exact archived 8 October N=154 search traces.

Checks bytes only; these finite searches do not certify an impossibility.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/legacy-snapshots/2026-10-08/n154-checkpoints"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

def validate_members(bundle, rows):
    p = subprocess.Popen(["zstd", "-dc", str(bundle)], stdout=subprocess.PIPE)
    actual = {}
    with tarfile.open(fileobj=p.stdout, mode="r|") as tar:
        for member in tar:
            if not member.isfile():
                continue
            value = hashlib.sha256()
            count = 0
            f = tar.extractfile(member)
            while True:
                buf = f.read(1024*1024)
                if not buf:
                    break
                value.update(buf)
                count += len(buf)
            actual[member.name] = (count, value.hexdigest())
    status = p.wait()
    if status:
        raise RuntimeError(f"zstd decompression failed: {status}")
    expect = {x["name"]: (x["size"], x["sha256"]) for x in rows}
    assert actual == expect, f"Checkpoint members failed: missing={set(expect)-set(actual)} extra={set(actual)-set(expect)}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", type=Path, help="Save restored .tar.zst archive to this path")
    args = ap.parse_args()
    m = json.loads((BASE / "CHECKPOINT_MANIFEST.json").read_text())
    assert len(m["parts"]) == 9 and len(m["members"]) == 12
    with tempfile.TemporaryDirectory() as d:
        target = Path(d) / m["archive_filename"]
        size = 0
        digest_all = hashlib.sha256()
        with target.open("wb") as out:
            for part in m["parts"]:
                raw = (BASE / part["name"]).read_bytes()
                assert len(raw) == part["size"], part["name"]
                assert digest(raw) == part["sha256"], part["name"]
                assert git_blob(raw) == part["git_blob_sha1"], part["name"]
                digest_all.update(raw)
                size += len(raw)
                out.write(raw)
        assert size == m["archive_bytes"]
        assert digest_all.hexdigest() == m["archive_sha256"]
        if shutil.which("zstd"):
            validate_members(target, m["members"])
            members="PASS"
        else:
            members="SKIP_NO_ZSTD"
        if args.write:
            args.write.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target, args.write)
    print(f"N154_CHECKPOINT_ARCHIVE=PASS parts={len(m['parts'])} bytes={size} members={members}")
    print("Integrity of search traces, not a proof of N=154 impossibility.")

if __name__ == "__main__":
    main()
