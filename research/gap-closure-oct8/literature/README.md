# Targeted literature check: the high-ratio primitive F3 gap

8 October 2026. No inspected source supplies a geometric decision for
the sole primitive candidate at 14430 or a universal primitive-scale F3
construction at unbounded `a/b`. The useful positive deduction from
this audit is instead [the improved adjacent W/beta conductor](SEED_EXTENSION.md).
Its old addition input is explicitly attributed; the new seed comes
from the preceding project construction.

The subsequent [all-adjacent-scale construction](../group1-helper/ADJACENT_ALL_SCALES.md)
supersedes that numerical bound by `m>=v`. Its
[independent mathematical audit](ADJACENT_INDEPENDENT_AUDIT.md) passes.
The general +v extension remains valid for nonadjacent parameters too.

## Exact sources and hypotheses

* **Zhang**, [arXiv:2512.22696v4](https://arxiv.org/pdf/2512.22696v4), still
  the latest version (4 April 2026). Proposition6 gives F2 seeds at
  scales b and c; exchanging labels also gives a. Theorem7 combines
  seeds additively, giving a sufficient tail. Proposition11 transfers
  a *tiling of the F2 target by the same tile* to F3 at the same
  multiplier. It is not an existence theorem at multiplier one.
  Section6 explicitly presents the macro-tile normalization as a
  conjecture. Its ideal-trapezoid converse is also conjectural, not
  an available necessary-and-sufficient geometric lemma.

* **Harries**, [current progress634.tex](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex),
  fresh blob `85536aabe013ad393e33985cbfcadbae50722f08`, unchanged from
  [pinned commit67838578](https://github.com/jphme/math-problems/blob/67838578b5bd26aa66034fa46da96141be75de0e/progress634/progress634.tex).
  Corollary “Finite generator windows” fixes a primitive tile and
  ordered target; its window grows with the aspect ratio. Appendix
  “Addition data and constructive transfers” gives F2(m) from an
  equilateral core of side `2abm`. The complete one-patch transfer
  table has no incoming edge to F2; its incoming F3 edge is F2→F3.
  None changes the tile or supplies the missing F2(1) input.

* **Beeson**, [IsoscelesTilings.pdf](https://www.michaelbeeson.com/research/papers/IsoscelesTilings.pdf),
  Table5, printed page55: the search hit `(56,9,61)` is a necessary
  candidate for N74 with target `(183,183,222)`. The adjacent text
  explicitly declines to assert existence or nonexistence for table
  entries. It is not a construction for 14430. The current
  [1206.2229v4](https://arxiv.org/abs/1206.2229) remains dated25 September;
  its W and beta prime cases are expressly open in that version.
  [2607.19572v2](https://arxiv.org/abs/2607.19572) remains withdrawn for
  a faulty Lemma9. These are not usable universal small-scale exclusions.

* **Bonfioli**, current commit
  [`4bb61193bafa4471f7ba3a35324ae0f70bd2177c`](https://github.com/ElVec1o/erdos_634_proof/tree/4bb61193bafa4471f7ba3a35324ae0f70bd2177c),
  remains dated13 September. Main paper blob
  `b7a471881297a7cb0e44dc80ae3f65df60e8e076`; companion blob
  `89e515fcc931adac919c292ebdfb0a8337d6ce22`. The companion's
  `thm:addlaw` proves beta addition for two constructed scales when
  one is v-divisible. This supplies the old input used in our new
  conductor deduction. It also retracts an earlier unconditional
  one-seed step because the remaining corner needs its own tiling.
  Our +v step satisfies that requirement with Beeson's existing seed.
  The source's three-seed collar reduction is conditional on those
  geometric seeds; it does not construct them for general parameters.

The public Erdős634 page again returned HTTP403. Searches in both web
indexes found no additional relevant construction. This is a bounded
source audit, not a claim that no solution exists anywhere online.

## The precise 14430 transfer input

The complete candidate gate from the preceding audit leaves only

```
tile (56,9,61), F3 scale1, target (3721,4514,1755).
```

Zhang's F2→F3 transfer would solve it if we could tile the F2 target

```
(4144,1089,3721), count8954,
```

by the **same** tile. Harries' bisector partition reduces this sufficient
route further to an equilateral triangle of side1008, count2016, again
by `(56,9,61)`. The three other pieces have grid scales61,56,9;
the F3 attachment has grid scale74. The count identity is

```
2016 + 61² + 56² + 9² + 74² = 14430.
```

The global count2016 is already positive through the W construction
`2016=14*12²`. Its tile is `(6,5,9)` and its target is scalene, so it
cannot be inserted into the equilateral core. A count-only transfer
would silently lose congruence of the final tiles. No such substitution
is being made here.

The converse normalization is actually false. The `(3,5,7)` F3 target
`(49,91,120)` has the verified312-tile construction at scale one, but
the corresponding equilateral core has side30 and would require60
tiles. The [complete exclusion of60](../../final-closure-oct8/e60-position/PROOF.md)
rules it out. Thus arbitrary F3 tilings cannot always be transformed
into this particular equilateral-core decomposition.

The old seed scales9,56,61 and the sufficient F3 tail from12 cannot
produce scale1 by addition or integer subdivision. This rules out that
specific seed-combination shortcut; it does not exclude a new tiling
of the target, a different decomposition of F2(1), or the equilateral
core. This audit did not run a positional search for those targets.

## What the square-class transfer check did and did not close

The class15 result gives the fixed `(3,5,7)` equilateral at every scale
at least4. The old transfers give the isosceles coefficient33 tail from4;
the other isosceles coefficient65 and F1 coefficients24,40 are globally
classical. The F4 coefficients88,104 belong to classes22 and26; the
former already has a project classification and the latter is classical.
The F2 coefficient143 tail from2 was already covered by the balanced
corner theorem. Its scale1 all-branch gate still contains both F2 and
two beta candidates, so the equilateral result alone is not a
classification of class143. The transferred F3 coefficients264,312
already lie in the earlier all-scale positive F3 sector.

The adjacent W theorem at u2 gives the14-square-class tail from3.
Its full classification additionally needs the separate exclusions14
and56 (Bonfioli reports both; our previous W56 replay remained incomplete).
The beta tail gives23m² for all m>=3, which was already globally supplied
by prior constructions using more than one tile. Bonfioli reports23
excluded, but its general W-prime input has an explicit unresolved
dependency in `lean/PAPER_MAP.md`; its beta23 exhaustion alone does not
exclude our second W23 candidate. We therefore separately replay the
two exact instances instead of silently importing the global claim.
The detailed checkpoint is in `CLASS23_GATE.md`. Count92 remains in
that source's unresolved list. No new complete square class is claimed
from these transfers in this audit.

`candidate_checks.json` preserves the complete finite gates used for
these comparisons. `seed_extension_checked.json` records exact tests
of the positive deduction. Neither file treats arithmetic admission as
a geometric construction.
