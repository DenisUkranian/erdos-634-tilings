# Erdős 634: global exclusion of the count 105

Denis Paliy, 30 September 2026. Research with ChatGPT assistance.

## Exact scope

The proposed computer-assisted theorem is that **no triangle is a union of 105 congruent triangles with disjoint interiors**. Reflections and T-junctions are allowed.

This is a result about the single integer 105, **not** a solution of the unrestricted classification in Erdős problem 634. It has internal checks only, no external referee acceptance or proof-assistant formalization. No priority claim is made.

The theorem uses the explicitly cited published shape and rationality theorems, the written geometric lemmas, and all four supplied fixed-target certificates. Do not treat a checker success as a formal verification of those human/external inputs.

## Reading

* `PROOF_N105.pdf` / `PROOF_N105.md`: complete global reduction, squarefree arguments, the new convex-capped chain lemma, and the certificate interface.
* `BASELINE_LEMMAS.md`: preserved earlier geometric lemmas, including the correct boundary-support definition and the hand obstruction for (5,19,21). Its old partial status for (5,16,19) is superseded by this package.
* `RESULT_RU.md`: Russian report.
* `VERIFIED_RESULTS.json`: actual final replay results.

## Reproduce

Python 3.10 or later; standard library only. Use ordinary Python without `-O`, `-OO` or `PYTHONOPTIMIZE`.

```sh
python verify_all.py --jobs 2
```

The program independently regenerates initial boundary configurations, replays all four complete certificates, checks the arithmetic reduction, and runs regression tests. It writes logs and exact reports into `verification/` and `data/`. Search is not needed for replay.

Check only the new fixed target:

```sh
python replay_16.py data/f1_5_16_19.json
```

The fresh search source is `search/engine_16_5_19.py`. Its default generation budget is a resource limit, not a proof limit. A timeout is recorded as `INCOMPLETE`, never `REFUTED`. To rerun its complete generation, set `BRANCH_POLICY=anchors` and an appropriate `OUTFILE`; the retained 120 raw root IDs are in the certificate. The final supplied file was produced by fresh generation, not by importing the earlier partial checkpoints.

## Verification boundary

The final fixed target is (80,95,105) using (5,16,19). All 120 retained initial configurations have complete refutations. The new search and checker additionally use the convex-capped whole-edge chain lemma: both ends must be convex corners of the actual residual region. Reflex ends and branching vertices do not qualify. The longest possible segment in this target is at most 105.

The other three fixed-target certificates were carried forward and replayed again in this turn. The count reduction shows these four targets exhaust every possible 105-tiling under the stated classification. The separate all-primes candidate manuscript and withdrawn packing lemmas are not premises.

Two implementations in the same project are computationally separate, not external peer review. Exact replay does not make a claim of priority or of having solved the full problem.

No emails were sent and no GitHub files were changed in this continuation.
