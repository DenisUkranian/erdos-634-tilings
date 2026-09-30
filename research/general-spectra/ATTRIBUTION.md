# Attribution addendum — 30 September 2026

A subsequent source comparison found that the 120-degree threshold refinement and the same fixed-tile example in this package were already written down by **Jan Philipp Harries**, *New constructions, obstructions, and multiplier structure for Erdős Problem 634*, version 0.5, dated 28 August 2026.

In its trapezoid section the manuscript proves

    R(a,b) = ceil(a/b) + ceil(b/a),     m >= 3R(a,b),

and explicitly gives the tile (32,45,67), multiplier m=9, and count 116640 below the printed conjectural cutoff 12. For A=max(a,b)>B>1, coprimality makes 3R=3(floor(A/B)+2), exactly the 120-degree bound derived here.

Source of record inspected: [progress634.tex](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex), lines 1080–1110 in the inspected file, blob SHA `85536aabe013ad393e33985cbfcadbae50722f08`. The [author's README](https://github.com/jphme/math-problems/blob/main/progress634/README.md) identifies version 0.5 and its date.

Accordingly, these mathematical conclusions and this example are **prior work, rederived and independently implemented here**, not first discoveries of this project. The package supplies its own inspectable macrocertificate, generator, expanded exact coordinates, and separate checking program. The integer 116640 was already globally admissible; the example concerns the specified tile and multiplier.

Harries also proves the equilateral divisibility ab|S for 120-degree tiles, explicitly extending the argument to 60-degree tiles in Remark "What the invariant closes" (inspected lines 990-1020). This conclusion is also prior work; the half-sum proof here is a different short derivation. The original PDF and TeX are retained as the preparation snapshot; this adjacent addendum records the subsequent attribution correction.

The direction-functional framework also predates this note: Laczkovich's signed specialization, later Laurent/signed-direction treatments by Harries and Bonfioli, and Zhang's constructive geometry are relevant. The existing note already credits Bonfioli for the isosceles/F1 necessary spectra and Zhang for the building blocks. No priority claim is made for any other statement in this package.

This addendum does not import unrelated claims from the earlier manuscripts. In particular, it does not validate the separate all-primes candidate, and it does not treat a finite generator window for each fixed ray as a finite global classification.
