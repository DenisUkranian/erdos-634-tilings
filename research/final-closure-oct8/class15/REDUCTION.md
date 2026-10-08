# What remains in square class 15 after the new equilateral tail

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This note is an exact reduction, **not a complete classification**. No claim of
novelty is made for the small exclusion N=15: Harries's August 28 result ledger
already attributes that exclusion to Beeson's earlier work.

The new independently checked **240-tile equilateral construction**, with
side60 and tile(3,5,7), extends to every N=15m² with m≥4. To increase the side
from15m to15(m+1), translate the equilateral triangle upward by15 in
Eisenstein coordinates and fill the bottom strip with the known tileable
trapezoid T(15m,15). The old trapezoid construction applies since15m≥60.
Consequently the entire unresolved part of square class15 is now:

> **135 only.**

The remaining count can only use the (3,5,7) equilateral branch. Thus this is an actual
reduction of the full problem (all triangle shapes and tiles), not only the
fixed (3,5,7) problem. It does not assert that135 is
impossible. N=15 is excluded below; N=60 is now excluded by the complete
[structural and positional proof](../e60-position/PROOF.md), including independent
replay of both exhaustive four-height position models. For m=4,5 the arithmetic sieve still has
four candidates, but existence is settled by the equilateral construction.

## Exhaustive small candidate list

For N=15m² with 1≤m≤5, the necessary spectra leave these candidates. Side triples
are primitive tile sides and actual target sides, in a common unit.

| Branch | Tile | Target | Multipliers surviving the added geometric bounds |
|---|---|---|---|
| E120 | (3,5,7) | (15m,15m,15m) | 3,4,5 |
| Group-1 theta | (4,15,16) | (60m,60m,15m) | 4,5 |
| Group-1 theta | (56,15,64) | (120m,120m,105m) | 4,5 |
| Double angle | (49,15,56) | (105m,105m,120m) | 4,5 |

At m=1 only the E120 row occurs in the initial sieve; the other rows have
already been excluded by the elementary scale-one theorem. At m=2,3,4,5 the
initial sieve has exactly the four rows shown.

The exhaustive inputs are the published angular classification and rationality
results, and their necessary thirteen count spectra, with citations in
[the uniform reduction](../../uniform-reduction/PROOF.md). No candidate W/beta
scale-one exclusion is used. The script `reduce_class15.py` checks the existing
divisor sieve against an independently implemented bounded parameter sweep at
all five counts. The parameter bounds are exhaustive: for the difference of
squares rows, v≤(N+1)/2 since v²−u²≥2v−1; in the norm rows every positive
parameter is at most N because one of their positive product coefficients must
divide N. The other Group-1 coefficients exceed v².

Classical cases cannot occur: 3 has odd valuation in every 15m², precluding a
sum of two squares, and the squarefree part 15 is different from 1,2,3,6.

## Positive seed and extension

The seed is the full coordinate certificate
`../equilateral-search/cpsat_count/E60_0-1_certificate.json`. Its independent
checker verifies all240tiles, target containment, area, and all28680pairwise
intersections. The extension uses only disjoint horizontal stacking, and the
known T(x,15) family, so no universal geometric normal form is assumed.

## The additional geometric exclusions

The [long-seam inequalities](../../../docs/long-seams-density.md), Theorem 1,
state

    theta:        t(v²−u²) ≥ uv,
    double angle: t(v²−u²) ≥ u².

For (u,v)=(7,8), these become 15m≥56 and 15m≥49 respectively. Both fail at
m=2 and m=3. They eliminate the last two table rows at these multipliers.

For the theta tile (4,15,16), the [two-longest-edge lemma](../../../docs/theta-branch.md),
Section 2, forces at least two whole edges of length16 on the base, whose
length is15m. At m=2 this is too short. At m=3 an edge decomposition would require

    45 = 4A+15B+16C,  A,B≥0, C≥2.

Since C=2 is the only possibility, the remaining13 cannot equal4A+15B.
Thus this row is also impossible at m=2,3.

## Excluding N=15, with two exact checks

For E120=(3,5,7), the target at m=1 has side15. The same two-longest-edge proof
applies: gamma=120° is obtuse, neither short length divides the other, and each
target corner has precisely the alpha+beta inventory: irrationality follows
from 2cos(alpha)=13/7, and alpha+beta=pi/3. The source proof uses
exactly these properties, and allows arbitrary T-junctions. Thus each exterior
side contains two whole7-edges. The equation

    15 = 3A+5B+7C, A,B≥0,C≥2

has no solution: C=2 leaves1, and C≥3 is already too large.

For an additional check independent of that boundary lemma, a complete
convex-frontier search, with no prescribed coordinate lattice or direction
band, gives a102-node refutation. `replay_n15.py` replays every branch using
local tangent cones and rational polygon clipping, independently of the
searcher's residual-boundary and separating-axis routines. It verifies all102
nodes,45dead ends, and all26 possible angle sums below pi; maximum depth is7.

The branching principle is elementary: at a convex corner of the remaining
region, some still-unplaced tile has a vertex there and an edge along the first
boundary ray. There are exactly the six angle-and-adjacent-side choices tested
by the verifier. A negative branch is accepted only after all such placements
are rejected or recursively checked. No time limit is involved in replay.

## Source scope and incomplete searches

The statement about N<105 in Beeson, *Tiling an Equilateral Triangle*,
arXiv:1812.07014v3, occurs in the discussion of the 60-degree tile family.
It is **not used** as an exclusion for the present120-degree (3,5,7) tile.
Nor do we use Zhang's assertion about target side X<105: the newly verified
side90 construction already prevents treating that assertion as a valid bound.

The generic frontier probe at N=60 stopped after45seconds and1211nodes,
maximum depth37. A 60-second repetition with additional necessary whole-boundary
arithmetic pruning visited 760 nodes, maximum depth29, and was also incomplete.
Neither is a negative certificate. Two earlier
30-second probes of the (56,15,64) and (49,15,56) candidates at N=135 were also
incomplete; those probes are unnecessary because the long-seam inequalities
already exclude those two candidates. The probe summaries are preserved as
`probe_summaries.json`. The search trees of incomplete probes are not used by
any proof here.

## Reproduction

From the repository root:

```sh
python3 research/final-closure-oct8/class15/reduce_class15.py
python3 research/final-closure-oct8/class15/replay_n15.py
```

Both commands use only the Python standard library. The first verifies the
full arithmetic list and the displayed small boundary obstructions. The second
verifies the complete N=15 geometric refutation. Neither command claims to
settle135 or Erdős634 as a whole.
