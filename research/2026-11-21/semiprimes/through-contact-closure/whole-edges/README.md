# Complete whole-edge contact constraints

21 November 2026. **3431 and 5063 remain OPEN.** This package requires an
actual opposite-bank tile along every unit interval of a selected interior
side. It extends the owned-through model and supplies exact positive,
deleted-neighbor, integration and restart controls. No target exclusion
is supplied by those controls.

## 1. The complete local catalogue

Let `T` be a selected whole triangle and let one of its counterclockwise
sides run from `p` to `q=p+L*u`, with `L in {a,b,c}` and `u` a unit
direction. The triangle lies on the left of that directed line. Any
opposite-bank tile lies on the right and has a side of some length
`ell in {a,b,c}` along the same line.

There are two reference triangles for each `ell`, according to the order
of its other two sides. The inherited unrestricted endpoint oracle gives
all six shapes with that side starting at `p` along `u`. Translate the
reference triangle by `t*u`. It contacts a positive-length part of the
selected side precisely when `t<L` and `t+ell>0`.

The [integer-offset lemma](../../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
applies to this actual maximal straight run: `p` is already a tile-side
endpoint. Therefore the offset of the other tile's side endpoint is an
integer. The complete list is consequently

\[
\boxed{t=1-\ell,\ldots,L-1.}                             \tag{1}
\]

Every reference shape and every offset in (1) is considered. Only full
containment and the existing necessary outer-boundary arithmetic discard
a placement. Both hands, partial side contacts and all adjacent short
heights are included. The enumeration imposes no global height,
denominator, phase or odd-population cutoff.

For a fixed selected side the number of candidates before containment is
at most

\[
\sum_{\ell\in\{a,b,c\}}2(L+\ell-1)
=6L+2(a+b+c)-6.
\]

The maximum is **370 for 3431** and **434 for 5063**. A candidate beginning
at integer offset `t` covers the selected unit interval `[k,k+1]` exactly
when `t<=k` and `k+1<=t+ell`. All actual side endpoints are at integer
offsets, so no hypothetical completion can split the open unit interval
between different opposite-bank tiles.

## 2. The Boolean constraints

Let `C_k` contain every contained candidate covering unit interval `k`.
For every interior side of every processed tile, impose

\[
x_T\Longrightarrow\bigvee_{Q\in C_k}x_Q,
\qquad \sum_{Q\in C_k}x_Q\le1.                           \tag{2}
\]

The second constraint is valid independently of `x_T`: any two candidates
in `C_k` occupy the same open bank interval and overlap on a positive-area
neighborhood of it. Together, (2) require exactly one neighbor when `T`
is selected. An empty catalogue correctly forbids selecting `T`.

There is deliberately **no** equality `sum x_Q=x_T`. When `T` is absent,
one of the opposite-bank candidates may legitimately remain present.
The deleted-antecedent control below explicitly preserves that case.

Every actual triangle has one canonical global Boolean `(q,h,j,s)`. A
candidate that covers several intervals or participates in several side
catalogues remains the same whole tile and is counted once. All six of
its actual endpoint contributions enter the shared model. Its selection
cannot use different placements to satisfy different intervals.

## 3. Outer sides and geometric completeness

A selected side needs no opposite-bank tile when both endpoints lie on
one supporting side of the board. Otherwise every point in its relative
interior lies strictly inside the board. To see this, each board
half-plane functional is nonnegative at both endpoints. If it vanishes
at an interior point of their segment, it vanishes at both endpoints.
Thus the only non-interior case is a segment lying wholly on one board
side. The code uses precisely this test.

The inherited model independently enumerates all possible exterior tile
sides and requires exact coverage of each exterior unit interval. It also
checks containment and, on a selected candidate, exact interior overlaps.

**Finite-selection sufficiency.** Suppose a finite selection consists of
contained whole tiles with pairwise disjoint interiors, has exact outer
boundary coverage, and satisfies the complete bank constraints (2) for
every side of every selected tile. Then it tiles the board.

Indeed, every interior unit side interval has a selected tile on each
bank. No such interval can belong to the boundary of a hole. If the
finite polygonal union left a positive-area part of the board uncovered,
its interface with the selected union would contain an open interval
of a selected side, contradicting (2). Equivalently, the internal oriented
side currents cancel and the remaining current is the board boundary.
The nonnegative winding multiplicity is one inside the board. Thus the
union is exactly the board, and the area fixes the count at `N`.

This is a completeness statement for a fully closed finite selected set.
The search may have imposed banks on only some selected tiles, so a SAT
response from an intermediate model remains a partial candidate. The
inherited positive-solution path checks every physical current and every
selected overlap before exporting a solution for independent verification.

## 4. Search integration and global scope

`WholeEdgeSearch` subclasses the permanent-only owned and spatial search.
It gives all six fixed corner-root tiles their three complete side banks
before the first query. During refinement it processes all three sides
of each chosen tile, with a configurable number of tiles per round.
Whole-edge refinement precedes optional additional vertex-fan refinement.
Selected edge neighbors' endpoint rows receive the same completion priority
as selected through owners.

The inherited global count and four charge-reserve bounds remain active.
The optional interior-point cliques may be disabled with `--no-grid` or
made coarse with `--grid-step`; neither sampling choice restricts
placements. Every explicit side bank, endpoint row and overlap exclusion
is permanent and necessary. There are no temporary finite-pool equalities.

The driver also uses the audited
[supported-long-cycle cuts](../corner-tests/LONG_CYCLE_CUTS.md) on selected
partial models. They apply only to the two target shapes, at every
direction height and translation. Repeated copies of one physical long
segment are deduplicated. A simple cycle supplies a permanent no-good on
its representative selected triangles. The cut is disabled for the 143
control and may be disabled explicitly with `--no-cycle-cuts`.

For any finite set of imposed banks, every actual full tiling projects to
a satisfying assignment: if its selected antecedent occurs, every real
opposite-bank tile belongs to the complete local list in (1). Missing
placements away from the imposed constraints create no restriction.
Therefore a separately checked UNSAT certificate would exclude the stated
scope, including every odd population. With a root ID, that scope is one
explicit corner branch; all surviving roots must be excluded for full
closure. A timeout, column cap or unverified solver response proves none
of these exclusions.

`necessary_model.json` exports every side's ordered endpoints, length,
ray, full neighbor list, per-unit candidate groups and coverage clauses.
It also exports their unconditional bank cliques and supported-cycle
witnesses. All variables share the canonical tile table used by the
existing permanent assertion and CNF proof interface.

## 5. Restart without losing the side banks

`--model-checkpoint PATH/necessary_model.json` regenerates complete
physical rows, owned corner roots, whole-edge banks and their cliques.
Stored overlap pairs are rechecked geometrically. Stored cycle sources
are regenerated through the target-specific detector. Arbitrary saved
assertion strings are never imported.

The old root assumptions are **not** imported. Supply `--root-file` and
`--root-id` again to continue that branch. Without them, the regenerated
geometric constraints remain necessary for the unrestricted board.
Interior sampling cliques are rebuilt using the newly requested grid.
This is a semantic regeneration of geometric sources, not restoration
of the solver's learned clauses or execution state.

## 6. Exact 143 controls

The verifier first checks the known 143-tile certificate's metric,
containment, area, physical currents and nonoverlap. It then reconstructs
the actual opposite banks independently by rational collinear segment
intersection, without using the candidate-template enumeration.

| Control | Result |
|---|---:|
| Actual outer sides correctly skipped | 25 |
| Actual interior sides recovered completely | 404 |
| Unit contacts with exactly one actual neighbor | 2,002 |
| Required neighbor deleted from a local bank | 442 rejections |
| Maximum actual neighbors along one side | 3 |

Optional solver controls check that the actual local bank is SAT, deleting
a required neighbor is UNSAT, and deleting its antecedent tile still
allows the neighbors. The complete actual 143 selection remains SAT with
all its side banks, all its physical endpoint rows, the exterior/root
constraints, spatial cliques, count and charge reserves. It remains SAT
after an equivalent solver rebuild and after regeneration from a model
checkpoint.

The integrated model contains 12,127 variables, 335 complete physical
rows, 429 side obligations, 1,984 bank cliques, 1,026 spatial cliques and
6,536 permanent assertions. Its actual selection is the single known
143 control with SHA256
`f9c864244612d930efeeea405f22a44881399d6f6974bdeda2fb6f70b2047aa9`.

For standard-library replay, with no solver installation required:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/whole-edges/verify_whole_edges.py --geometry-only
```

For fresh encoding, rebuild and restart checks using system `libz3`:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/whole-edges/verify_whole_edges.py --with-solver
```

The saved result is [WHOLE_EDGE_CONTROL_REPLAY.json](WHOLE_EDGE_CONTROL_REPLAY.json).
These controls validate the stated geometry and encoding; they do not
establish a target contradiction.

## 7. Example unrestricted branch run

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/whole-edges/whole_edge_search.py \
  35 13 43 --out /tmp/whole-5063-O0-X0-Y0 \
  --root-file research/2026-11-21/semiprimes/through-contact-closure/corners/ROOTS_5063.json \
  --root-id O0-X0-Y0 --no-grid --edge-tiles-per-round 20 \
  --vertex-fans-per-round 2 --time-limit 600 --proof
```

Omit both root flags for an unrestricted whole-board model. No fixed odd
population is used in either mode. All bounded exits checkpoint with an
explicit inconclusive status. Both original targets remain open until a
complete independently verified certificate or an actual tiling is found.
