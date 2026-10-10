# Erdős 634 — original N=154 search checkpoints (8 October 2026)

This is a **byte-preserving archive of two 600-second bounded positional searches**,
not a global proof that N=154 is impossible. Preserve their original status
and do not turn time limits, partial branches or unverified logs into theorems.

The full original data are large raw search traces. Original compressed ZIP
sizes: 7,530,385 and 10,566,232 bytes. The ZIP payloads were extracted
without changing any of their **12 member files** and packed into one zstd
tar archive (13,799,579 bytes). The tar was uploaded to GitHub as **nine
lossless binary Git blobs** in this directory.

* [SHA-256 manifest, parts and member hashes](CHECKPOINT_MANIFEST.json)
* [Verified reconstruction script](../../../../scripts/verify_checkpoint_archive.py)
* Original uncompressed trace data: two `*-geometry.txt` files,
  two `*-trace.txt` files plus source summaries and run metadata
* Reconstituted archive SHA-256:
  `38e2c7b43e53329ad4d71e735545b5fbc2514070d0580de3e32cbed0096ccaa4`

From the repository root:

```sh
python3 scripts/verify_checkpoint_archive.py
python3 scripts/verify_checkpoint_archive.py --write Erdos634_N154_search_checkpoints_2026-10-08.tar.zst
tar --use-compress-program=unzstd -tf Erdos634_N154_search_checkpoints_2026-10-08.tar.zst
```

The first command verifies every Git-tracked binary part by SHA-256 and
Git blob identity, the reconstructed archive by SHA-256 and, when zstd is
available, all 12 original uncompressed members by SHA-256.
This package is a preservation record, **not a new successful N=154 refutation**.
The later certified arguments are documented elsewhere in the repository.
