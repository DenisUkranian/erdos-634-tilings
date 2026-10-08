# Complete angular-candidate gates for N=60,135,154

8 October 2026. These gates concern **all triangle shapes and congruent tile
shapes** in Erdős634. They are arithmetic reductions, not by themselves
geometric nonexistence proofs.

## The unique N=154 candidate

Every realization of154, if one exists, is necessarily, up to similarity,
reflection and relabeling, a tiling of

    target (91,91,154) by154 copies of tile (8,7,13).

In the repository's ordered notation this is branch I120, primitive parameters
(a,b,c)=(8,7,13), multiplier1. Direct verification gives

    13²=8²+8*7+7²,
    154=7*(8+2*7),
    (bc,bc,b(a+2b))=(91,91,154).

No W/beta scale-one candidate or prime-case exclusion is used in this
reduction. The two independently written enumerations both return exactly
this one row. Thus an exhaustive geometric exclusion of this instance is a
**global** exclusion of N=154, subject to the published classification and
rationality inputs below.

## Exhaustive inputs and finite parameter bounds

The geometric inputs are Laczkovich's exhaustive triangle-tiling angular
classification, as tabulated in Beeson–Zhang, *Rationality of certain triangle
tilings*, arXiv:2604.01314v1, Table1, and their Theorem1.2 for rationality
outside the classical cases. The resulting thirteen necessary integer-scale
families are proved and attributed in
[the uniform reduction](../../uniform-reduction/PROOF.md) and
[uniform sectors](../../uniform-sectors/PROOF.md). The present code imports
these **necessary** forms, without treating any arithmetic candidate as a
construction.

The classical cases have counts among squares, sums of two squares, and
2,3,6 times a square. For154 the squarefree part is154, while its7-adic
valuation is odd; therefore no classical case occurs. For60 and135 the
squarefree part is15 and the3-adic valuation is odd, with the same conclusion.

The existing divisor sieve is compared against a second implementation which
sweeps bounded primitive parameters directly, evaluates every count and target
formula, and compares the complete normalized candidate sets:

* Difference-of-squares coefficients b=v²-u² satisfy b≥2v-1, so
  v≤(N+1)/2 suffices whenever b dividesN.
* The other Group-1 coefficients exceed v², so their parameters are also
  covered by that conservative bound at the three tested counts.
* Every positive norm-family parameter a,b is at mostN, because the associated
  positive product coefficient must divideN.
* Multipliers are obtained by exact integer square tests; all rational scale
  refinements used by the formulas have already been proved in the cited
  necessary-spectrum notes.

The elementary scale-one exclusions for theta and double-angle targets are
those proved in the uniform-reduction note. The enumeration does not invoke
any disputed scale-one W or beta lemma.

## N=60 and N=135

Each initial arithmetic list has precisely four candidates:

| N | Branch | Tile | Target |
|---:|---|---|---|
|60|E120|(3,5,7)|(30,30,30)|
|60|theta|(4,15,16)|(120,120,30)|
|60|theta|(56,15,64)|(240,240,210)|
|60|double angle|(49,15,56)|(210,210,240)|
|135|E120|(3,5,7)|(45,45,45)|
|135|theta|(4,15,16)|(180,180,45)|
|135|theta|(56,15,64)|(360,360,315)|
|135|double angle|(49,15,56)|(315,315,360)|

The extra necessary bounds in
[the class15 reduction](../class15/REDUCTION.md) exclude all three non-equilateral
rows for each count. Specifically,15m≥56 and15m≥49 fail at m=2,3 for the last
two families. In the (4,15,16) family the base must contain two16-edges; base30
is too short, while45-32=13 is not a sum of4 and15.

Consequently the side30 and side45 equilateral instances are the respective
unique geometric cases still requiring inspection after these known bounds.
This arithmetic note does not transfer a negative result between the two.

## Reproduction

From the repository root:

```sh
python3 research/final-closure-oct8/arithmetic-gates/check.py
```

This standard-library computation creates `checked.json`. It compares full
candidate sets, not merely counts of candidates. The second implementation is
`../class15/reduce_class15.py:independent`; it does not call the divisor sieve.
The two implementations share the mathematical count formulas, whose
exhaustiveness comes from the documented classification theorem, not from
agreement of finite programs.
