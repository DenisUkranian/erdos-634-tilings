# Global exclusion of N=105

**Current result, 30 September 2026.** A computer-assisted proof that no triangle is tiled by exactly 105 congruent triangles is supplied in [the complete manuscript](../research/n105/PROOF_N105.md) and [PDF](../research/n105/PROOF_N105.pdf).

The exhaustive reduction has four survivors; [all four certificates](../research/n105/data/) have complete independently rebuilt root coverage. The proof permits reflections and T-junctions. The separate candidate all-primes proof is not a premise.

The original complete fourth certificate stores **22,552 states**. An independent replay may terminate early when a separately implemented necessary test already detects a contradiction. Thus a smaller replay count in an earlier report is not missing root coverage. Root coverage and certificate SHA-256, rather than a transient number of explored states, identify the checked result.

## Dependencies and scope

Read Sections 1–5 of the manuscript for the exact uses of Laczkovich, Snover–Waiveris–Williams, Beeson, and Beeson–Zhang. The corrected source versions and limited statements are explicit. Finite replay does not formalize these outside theorems or the human boundary lemmas.

[BASELINE_LEMMAS.md](../research/n105/BASELINE_LEMMAS.md) is a preserved earlier stage used for its written geometric lemmas. Its partial fourth-target count is superseded by the complete main manuscript, not silently reused as proof of completion.

The publication audit corrected one wording omission in the classical-case paragraph: the rational-angle equilateral count families include **twice a square**. This even family cannot produce 105; adding it makes the stated case list complete and does not change any certificate or arithmetic decision. The source and PDF are synchronized.

The result concerns **one global integer**, not all integers in Erdős problem 634. No external referee acceptance, proof-assistant verification of the complete argument, or priority adjudication is claimed.

## Reproduce

```bash
cd research/n105
python verify_all.py --jobs 2
```

The repository-wide coordinator runs this in a temporary copy and checks the frozen certificate hashes first. See [REPRODUCIBILITY.md](../REPRODUCIBILITY.md).
