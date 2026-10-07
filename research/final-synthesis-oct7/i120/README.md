# I120 final synthesis: the missing converse and a dominated F3 transfer

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

**154 remains unresolved. This note supplies no new classification.**
Its purpose is to state the exact geometric obligation after combining
Harries's constructions with the project's new F3 sector, and to record
a stronger search without mistaking an incomplete run for a proof.

## 1. The missing converse is a geometric extraction theorem

For the primitive tile `(a,b,c)`, where `c^2=a^2+ab+b^2`, put
`U=a+2b`, `W=a+b`. At multiplier one the I120 target has sides
`(bc,bc,bU)` and count `bU`.

It has a geometric dissection into an ordinary b-fold similar tile,
containing `b^2` unit tiles, and an F1 target with sides `(ab,bc,bW)`
and count `bW`. Therefore an F1 tiling constructs an I120 tiling.
This statement has **no converse from dissection alone**: the artificial
cut may cross tiles of an arbitrary I120 tiling.

For `(8,7,13)`, this is the attachment `105+49=154`.
The established exclusion of 105 does not exclude 154 unless one proves
that every 154 tiling can be transformed to contain the particular 49-tile
corner patch, or proves a different general necessity theorem.

Harries's manuscript, section "Provisional below-200 research programme",
identifies the same difficulty: reflected placements across a proposed
layer can undershoot one artificial wall at a T-junction and cross the
next artificial chord. The ordered short-edge word does not determine
the missing side assignment. Its conditional table still lists 154.
The source was freshly read on 7 October 2026:

- [Harries, *New constructions, obstructions, and multiplier structure for
  Erdős Problem 634*, manuscript dated 28 August 2026](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex).
- [Beeson, *Tilings of an Isosceles Triangle*, v7](https://arxiv.org/html/1206.1974v7), section 12 and Table 5.

No obsolete restriction from the 2012 *Triangle Tiling V* is imported.

## 2. Exact F3-to-I120 transfer

The new F3 construction suggests another route, but the simplest transfer
has a precise limitation.

**Dissection lemma.** An I120 triangle at real multiplier `m>0` can be
dissected into an F3 target at multiplier `bm/U` and another I120 target
at multiplier `cm/U`.

**Proof.** Let `ABC` have apex A and base BC, so
`AB=AC=bcm`, `BC=bUm`, and the base angles are alpha. Its apex angle is
`alpha+3 beta`, where `alpha+beta=pi/3`. Draw AD to BC with
`angle CAD=alpha`. Then triangle ACD has angles
`(alpha,alpha,pi-2 alpha)` and is similar to ABC. The side AC is its base,
so its scale relative to ABC is `c/U`. In particular

    AD=CD=bc^2 m/U.

Triangle ABD has angles `(3 beta,alpha,2 alpha)`, and its three sides are

    AB=bcm,
    AD=bc^2 m/U,
    BD=bUm-bc^2 m/U=3b^2 W m/U.

These are `bm/U` times `(cU,c^2,3bW)`, the ordered F3 target. Both pieces
have positive area since `U>c` and `U^2-c^2=3bW`. This proves the lemma.

The corresponding tile-count identity is

    bU m^2 = 3UW (bm/U)^2 + bU (cm/U)^2.

Thus at integer scales, for every positive integer s,

    I120(c s) and F3(b s)  =>  I120(U s).

By the new all-multiplier F3 construction, the F3 premise is automatic
when `0<a<2b`.

**Why this does not improve the known I120 tail.** The project's [improved equilateral tail](../../group2-trapezoids/PROOF.md),
combined with the earlier Harries/Zhang attachment, already gives every
I120 multiplier

    m >= T := 3 ceil(c/min(a,b)).

If `min(a,b)>=4`, then `c>=7` and `3 ceil(c/4)<=c`, so `T<=c<U`.
If `min(a,b)=3`, the difference-of-squares identity

    (2c-(2a+3))(2c+(2a+3))=27

(with the labels exchanged if necessary) forces `(a,b,c)=(5,3,7)`
up to order. Here `T=9`, whereas U is 11 or 13. Values 1 and 2 for the
smaller side admit no positive integer norm triple.
Consequently **every output U s of this transfer is already inside
the established tail**, for every primitive norm triple. This construction
is a valid synthesis of the two results, but it does not decide any new
I120 multiplier and cannot close 154.

The written proof is accompanied by `check_transfer.py`, which checks
both positive subtriangle areas, all side-length identities, the count
identity, and domination by the existing tail on all 174 ordered primitive
norm triples with `1<=a,b<=500`, using exact rational arithmetic.
The finite regression report is `transfer-check.json`.

## 3. What the stronger all-corner probe does

`combined_search.py` adapts the existing exact n105 fan engine to
`(91,91,154)` and starts from the empty triangle, covering all target-corner
fans. It combines:

1. exact nonoverlap, boundary semigroup and corner-fan constraints;
2. integer seam atoms and integer vertex-to-edge offsets;
3. the proved modulo-13 orientation-population bounds;
4. the proved connectivity correction for missing intermediate heights;
5. apex-first branching and simple-coordinate fan ordering.

No new mathematical pruning assumption is introduced. The two population
conditions are proved in
[the I120 boundary note](../../i120-boundary-oct7/README.md), and the seam
conditions are proved in
[the exact-seam note](../../../docs/exact-seam-certificates.md).

The retained 900-second run visited **7,747 states**, reached **124 placed
tiles**, and finished **INCOMPLETE**. It checked 123,253 vertex-on-edge
incidences and found 47 distinct integer-seam conflicts. The connected
height-population condition rejected 6,850 candidate partial placements
(including fan probes, so this is not a count of distinct search states).
Before the search, all 489,555 pairs of the actual 990-tile fixture passed
the seam condition, including 300 vertex-on-edge incidences.
These are search statistics, not a certificate for 154 or a measure of
how close a complete classification is.

The script is a search probe, not a separate refutation checker.
Its default run retains `combined-search-report.json`; a timeout is
`INCOMPLETE`. Even an exhausted search would still require a complete
export and independent replay before being used here as a negative theorem.

```sh
BRANCH_POLICY=top FAN_ORDER=simple python research/final-synthesis-oct7/i120/combined_search.py --seconds 900
```
