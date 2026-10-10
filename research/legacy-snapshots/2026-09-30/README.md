# Archival completeness check — 30 September 2026

**Project:** Erdős Problem 634, historical source snapshot. **Audit date:** 10 October 2026.
**Status:** byte-preservation only — not an endorsement of old mathematical claims.

A full recovery ZIP dated 30 September 2026 was retained in Denis Paliy's ChatGPT Library (SHA-256 `9c653b4329f2819f1fd71372a7b987171a680564f5d58e0877f8efb68e75640d`; 4,751,559 bytes). We audited its **236 source members**, of which **215** represent historical files under `repository/` and **21** are recovery reports/logs. Compared with main at commit [5a4b2aa](https://github.com/DenisUkranian/erdos-634-tilings/commit/5a4b2aa9c5e3839767b23879716bffd8bc3d65cb):

| Category | Files | How preserved |
| --- | ---: | --- |
| Same path and same Git blob | 142 | Already in main at the pinned audit commit |
| Paths absent at that commit | 38 | Exact old copies inside the supplemental ZIP |
| Paths present but later modified | 35 | Exact old versions inside the supplemental ZIP (do not replace the newer version) |
| Recovery metadata and logs outside `repository/` | 21 | Exact copies inside the supplemental ZIP |
| **Total** | **236** | **Reconstructible at original byte level** |

**[Lossless historical delta ZIP](Erdos634_legacy_recovery_delta_2026-09-30.zip)** contains 94 saved members, an `INDEX.md`, and a 236-entry `MANIFEST.json` with source pathname, byte length, SHA-256, Git blob SHA-1, and disposition. Its SHA-256 is `ff2b52424e0bc8a1bf43838a5eb9ad4c75054b1cc98ed2a0522041e0eaac18ae`; Git blob SHA-1 is `df9729220d0b3d8cc152fdc29a542fbdaab5323c`.

The ZIP preserves the old `research/spectra` package (including the 116640-tile construction data), old N=105 verification logs and older versions of documentation and scripts. These are *historical records*; the current README, STATUS, workflows and proofs remain authoritative for the repository's present status. The exact local integrity test is `python3 scripts/verify_legacy_recovery_delta.py`.

**Separately inventoried, not included in this delta:** 8 October raw N=154 search checkpoints (7.53 MB and 10.57 MB compressed), the August N=83 certificate archive (701,938 bytes, contains upstream third-party checker code with unclear redistribution license), and the 441,709,276-byte original N=135 certificate. Those are preserved in Library but require separate distribution decisions. This document does not claim they are uploaded here.
