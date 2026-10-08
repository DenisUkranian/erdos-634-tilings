# Second text audit of the global N=154 proof

8 October 2026. Reviewed
`../154-audit/GLOBAL_154_PROOF.md` against its current inputs and reports.

**PASS: no missing implication was found in the written global reduction
or in the combination of the three positioned refutations.** This is an
internal mathematical/textual audit, not external refereeing. It does
not substitute for the separately completed large certificate replays.

1. **Global candidate coverage.** The all-branch arithmetic gate was
   rerun through its `run()` entry point without overwriting its report.
   Both implementations again return precisely I120, tile(8,7,13),
   target(91,91,154), multiplier1. The argument does not invoke either
   disputed scale-one W/beta exclusion. The primary arXiv HTML for
   Beeson--Zhang2604.01314v1 was also opened: Table1 tabulates the stated
   noncommensurable-angle shapes, and Theorem1.2 states commensurable
   sides for nonsimilar, nonright tiles with noncommensurable angles.
   Its use in the proof is correctly scoped; Theorem1.1 is the narrower
   120-degree theorem, so the reference to1.2 is deliberate and correct.

2. **Height coverage.** The prior fresh audit in
   `154_STRUCTURAL_REVIEW.md` independently reran the nonzero-population13
   exclusion and all six six-height signed-current exclusions. Together
   with154<169 and the whole-edge cut theorem, this proves at most five
   consecutive heights containing zero. The final text correctly retains
   the six-height computation instead of incorrectly rejecting
   24+5*26=154 on population grounds.

3. **All bands, including smaller supports.** The five intervals of
   lengthfive containing zero are exactly those listed. Target reflection
   exchanges[-4,0]with[0,4] and[-3,1]with[-1,3], while[-2,2] is fixed.
   Any shorter interval containing zero is a subset of at least one
   such interval. The systems impose no positive population requirement
   for a listed height, so smaller supports are genuinely included.

4. **Complete lattice.** With eta=3+rho and eta_bar=4-rho, the identities
   eta*eta_bar=13, eta^2=8+7rho, and
   2eta+2eta_bar-eta*eta_bar=1 are correct. Factoring
   g=eta^L/eta_bar^U gives the claimed integer generators. For positive
   width w, raising a Bezout identity to power2w-1 proves that the two
   endpoint powers generate the unit ideal. In particular the asserted
   lattice equality, and the weaker inclusion sufficient for a negative
   enumeration, are valid. The extra sixth-root basis rotations preserve
   the integer Eisenstein lattice and apply to target and templates alike.

5. **Positioned equations and elimination.** For a directed edge A->B,
   the derivative of its signed one-dimensional current is+delta_A-delta_B,
   whether the direction is positive or negative in the chosen axis.
   Thus storing an unoriented direction with these endpoint signs is
   sound. The six endpoint contributions per triangle are necessary
   under arbitrary T-junctions. At a homogeneous zero row every incident
   same-sign coefficient forces its nonnegative variable tozero; a target
   row without the required sign is then contradictory. This argument
   needs neither binary integrality nor a normal-form assumption.

6. **Numerical statements checked against reports.** The three reports
   all sayPASS, with the bands and basis rotations stated in the text.
   Their placement sum is exactly14,303,325,332 and their mask-record sum
   is88,600,250. Their remaining counts346,573,610 agree with the respective
   enumerated-minus-removed totals. Direct independent Eisenstein
   multiplication gives the transformed apices(8281,9464),(-1365,16016),
   and(7049,10591), exactly as printed. The required signs and empty-support
   flags agree with the reports.

7. **Reproduction and scope.** `reproduce_bitmap.py` rejects incomplete
   producer runs, compiles and invokes the separate verifier, checks each
   exact band/rotation/count, and requires actual terminal contradiction
   flags. The final text correctly distinguishes this completed
   computer-assisted exclusion of154 from the full classification of
   Erdős634. A timeout during a future regeneration is not promoted toNO.

The audit's source observation is
https://arxiv.org/html/2604.01314v1 . It checks the stated theorem and
classification references; it does not reprove the external classification.
