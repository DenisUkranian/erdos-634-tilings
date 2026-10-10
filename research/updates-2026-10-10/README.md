# Erdős 634 — research supplements of 9–10 October 2026

**Research directed by Denis Paliy, assisted by ChatGPT.** This supplements, but does not supersede, the historical main repository. Erdős problem 634 remains unsolved as a complete classification.

## Verified archive and source files

- [Complete, SHA-256-verified source ZIP](packages/Erdos634_complete_updates_2026-10-10.zip): 10 historical source archives, 242 original files, original relative paths, executable scripts, JSON certificates, logs, diagrams and reports.
- [Expanded repository tree](expanded/): all 220 UTF-8 files of at most 100,000 bytes, browsable and diffable directly in GitHub. The remaining 22 large/binary members are present in the complete ZIP.
- [Phase 1 independent audit](audit-phase1/REPORT.md) (9 October): global 56 trees, negative controls, 29,600 search nodes and 14,556 contradiction leaves within the stated audited branches.
- [Phase 2 independent audit](audit-phase2/REPORT.md) (10 October): foundational boundary geometry, exact polygon intersection checks, corrected T-junction rules and additional checks of W/beta constructions.

## Main updates and remaining gaps

| Research | Result and exact limitations |
| --- | --- |
| General W and beta | [Constructive sufficient result](w-beta/UNRESTRICTED_CONSTRUCTION.md): for coprime 0<u<v, tile (uv,v²−u²,v²) realizes W and beta at every integral multiplier M≥v. Does not classify smaller multipliers or all possible tilings. |
| Square class 14 | [Proof package](class-14/COMPLETE_CLASS14_PROOF.md): 14m² realizable iff m≥3, relying on the described all-branch classification and the specific certified global N=56 refutation. This is not a general criterion for all N. |
| F3, N=14430 | [Independent attack](f3-14430/INDEPENDENT_ATTACK.md), [boundary/current restrictions](f3-14430/BOUNDARY_GAP_ANALYSIS.md), [height-61 exclusion](f3-14430/NO_61_HEIGHT.md): unique primitive candidate (56,9,61) with stronger necessary constraints; still UNDECIDED. |
| W92, beta92 | Additional exact root/partial boundary tests in the [parallel boundary package](expanded/Erdos634_parallel_W92_boundary_2026-10-09/). No exhaustive negative certificate. N=92 remains UNDECIDED. |
| Fixed square-class effective density | Written deduction and finite probes preserved in [original source](expanded/erdos634_effective_density_2026-10-09/). Assumes earlier classification and constructive tails. It does not decide every small multiplier. |
| Prime-count reverse-apex | [Base-case audit and outstanding objections](quarantine/BEESON_BASE_CASE_AUDIT.md). Unsupported general induction is QUARANTINED and is not invoked as a theorem. |

## Source verification

Run the following after checking out the repository:

```sh
python3 scripts/verify_oct10_archive.py
```

Expected output begins OCT10_ARCHIVE=PASS, checking all 242 source SHA-256 hashes and all 220 expanded copies. ZIP SHA-256: `fda301389453d0579d45c595e59552769baf363138084444d4df07ee26a8d048`.

Source integrity is not a mathematical proof. The ten source ZIPs retain their original dated limitations and statuses (PASS, INCOMPLETE, UNDECIDED). A negative claim requires its actual complete refutation, not a timed-out search.

The separate 441,709,276-byte `Erdos634_135_Verified_Certificate.zip` archive from 8 October was not duplicated here because of GitHub file-size constraints. See the already-published smaller [135 proof and replay material](../../universal-closure-oct8/global/GLOBAL_135_PROOF.md). No claim of a fresh independent run of that full heavyweight external file is made.

Baseline prior to integration: [3a0ad269f645850ed9fd01bbd76a08c9b456032e](https://github.com/DenisUkranian/erdos-634-tilings/commit/3a0ad269f645850ed9fd01bbd76a08c9b456032e) (8 October 2026). All original historical files are preserved. No external peer-review acceptance or proof-assistant verification of the full problem is claimed.
