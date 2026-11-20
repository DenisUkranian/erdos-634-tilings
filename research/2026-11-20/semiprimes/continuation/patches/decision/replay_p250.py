"""Replay the exact finite-palette enumeration for the 250-tile pentagon."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--jobs", type=int, default=4)
parser.add_argument("--shards", type=int, default=16)
parser.add_argument("--seed-y", action="store_true")
parser.add_argument("--ledger", type=Path)
args = parser.parse_args()
if args.jobs < 1 or args.shards < 1:
    parser.error("jobs and shards must be positive")
if args.ledger:
    if args.seed_y:
        parser.error("the supplied ledger is an unseeded ledger")
    data = json.loads(args.ledger.read_text())
    counts = data["shard_counts"]
    assert len(counts) <= 3 and all(isinstance(x, int) and x > 0 for x in counts)
    records = {tuple(row["partition"]): row["nodes"] for row in data["records"]}
    assert len(records) == len(data["records"])

    def cover(prefix):
        if prefix in records:
            return {prefix}
        assert len(prefix) < len(counts), f"missing partition {prefix}"
        return set().union(*(cover(prefix+(i,)) for i in range(counts[len(prefix)])))

    assert cover(()) == set(records), "incomplete or redundant partition manifest"
else:
    counts = [args.shards]
    records = {(i,): None for i in range(args.shards)}

def replay(binary, key):
    fields = [("PACK_SHARDS", "PACK_SHARD_ID"), ("PACK_SUBSHARDS", "PACK_SUBSHARD_ID"),
              ("PACK_THIRD_SHARDS", "PACK_THIRD_ID")]
    env = {k: v for k, v in os.environ.items() if not k.startswith("PACK_")}
    for depth, i in enumerate(key):
        count_key, index_key = fields[depth]
        env[count_key], env[index_key] = str(counts[depth]), str(i)
    run = subprocess.run([str(binary), "35", "13", "43", "22", "17", "-1", "2",
                          "8000000", "8", "1"], check=True, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    labels = [f"{name} {i} of {count}" for name, i, count in
              zip(("shard","subshard","third"), key, counts)]
    marker = f"NO({', '.join(reversed(labels))})" if counts[0] > 1 else "NO(in palette)"
    expected = re.fullmatch(re.escape(marker)+r" ([0-9]+)", run.stdout.strip())
    if not expected:
        raise RuntimeError(run.stdout)
    if records[key] is not None and int(expected[1]) != records[key]:
        raise RuntimeError(f"changed node count at {key}: {run.stdout}")
    return run.stdout.strip()

with tempfile.TemporaryDirectory() as directory:
    binary = Path(directory) / "sweep"
    flags = ["-DREFLEX_FILTER", "-DSPAN_FILTER", "-DSIGN_FILTER", "-DBANK_PROBES"]
    if args.seed_y:
        flags.append("-DSEED_P250")
    subprocess.run(["g++", "-std=c++20", "-O3", *flags, str(HERE / "pentfinite.cpp"),
                    "-o", str(binary)], check=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for result in pool.map(lambda key: replay(binary, key), sorted(records)):
            print(result, flush=True)
