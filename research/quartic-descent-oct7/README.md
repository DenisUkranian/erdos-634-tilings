# Odd-product exclusion extending square class 78

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

Let R be the product of an odd number of distinct primes p satisfying

```
p = 13 (mod 24),    3^((p-1)/4) = 1 (mod p).
```

Then **6Rm² is impossible for every odd positive integer m**, allowing
all congruent triangle shapes, reflections and arbitrary T-junctions.
There are infinitely many qualifying primes, of density 1/16 among
primes; R may have arbitrarily many prime factors. Examples of squarefree
kernels are 78, 654, 1086, 1374, 1662 and 1538862.

The [universal proof](PROOF.md) reduces any putative tiling to F3,
then excludes every supported square class on an explicit rational cubic
by local residue conditions and quadratic reciprocity. It uses no rank
or basis computation. The [independent internal audit](AUDIT.md)
checks the proof and its Chebotarev infinitude argument.

Existing theta constructions give an effective eventual parity criterion
in each of these classes. All small even multipliers are settled here
only for the earlier complete class 78; the full tiling problem remains
open, including 154 and 4830.

From the repository root:

```bash
python research/quartic-descent-oct7/check_odd_product.py
python research/quartic-descent-oct7/check_independent.py
```

Retained fresh reports: [product checks](verification.json) and
[independent algebra/residue checks](independent-verification.json).
These finite checks support the written proof; they are not a replacement
for the universal argument or an external referee report.
