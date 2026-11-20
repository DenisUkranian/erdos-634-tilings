# An unconditional finite height and coordinate envelope

21 November 2026. This is a consequence of the existing occupied-parent
and signed phase-population theorems. It applies to complete tilings of
both target boards. It supplies a rigorous, but extremely large, finite
envelope for an exhaustive model; it is not a feasibility decision.

Work in the standard frame with exterior direction heights 0 and 2,
and let `L,H` be the least and greatest occupied short heights. Let
`Rmax=45` for 3431 and `Rmax=58` for 5063, the proved upper bounds
on the number of occupied ordinary nodes in either prime tree.

## Height bound

The height-zero core has nonzero prescribed population residue, so
`L<=0<=H`. Each outer side contains a tile long edge, by the existing
obtuse-angle endpoint argument. An outer height-two side therefore
requires an occupied short height 1 or 3; hence `H>=1`. An outer
height-zero side requires short height -1 or 1.

At negative heights the decreasing-height tree is exterior-free.
Repeated application of the occupied-parent theorem fills every height
from `L` through -1. At heights above 2 the increasing-height tree is
exterior-free, so the same theorem fills every height from 2 through
`H` whenever `H>=2`. These are ordinary nodes. Distinct physical
heights give distinct exact nodes within either single tree; no sum of
the two trees' populations is used.

The boundary supplier at height 1 or 3 lies outside the negative
levels. Thus `-L+1<=Rmax`, or `L>=1-Rmax`.

If `H>=2`, the `H-1` occupied levels 2 through `H` are supplemented
by the boundary supplier at -1 or 1. Thus `H<=Rmax`; for `H=1` this
holds trivially. Consequently every complete tiling satisfies

| Target | All possible short heights |
|---:|---|
| 3431 | `-44 <= h <= 45` |
| 5063 | `-57 <= h <= 58` |

There is a sharper bound on the occupied span. If height 1 occurs,
every level from `L` through `H` occurs and there are `H-L` ordinary
levels, so `H-L<=Rmax`. If height 1 is absent, both -1 and 3 occur
by the boundary suppliers; the only potentially absent intervening
level is 1, giving `H-L-1<=Rmax`.

## Coordinate bound

Normalize the two split-prime valuations by
`v_pi(z)=1`, `v_barpi(z)=-1`, and `v_pi(c)=v_barpi(c)=1`.

Every occupied short node has an ancestor at physical height `L` in
the increasing tree. If that ancestor were exterior-free, the no-gap
theorem would force it occupied, and the occupied-parent theorem would
force an occupied node at height `L-1`, contradicting minimality.
Its ancestor is therefore the unique exterior-containing height-`L`
node. Since `L<=0`, that node contains zero and all its vertices have
`v_pi(x)>=L`.

The conjugate argument at physical height `H` gives
`v_barpi(x)>=-H` for every tile vertex: otherwise an exterior-free
height-`H` ancestor would force an occupied parent at `H+1`.
Here `H>=1`, so the exterior-containing ancestor includes zero.
The existing vertex-lattice theorem supplies integrality at every
other prime. Therefore all tile vertices belong to the fixed
fractional ideal

`I(L,H) = {x in R[1/c] : v_pi(x)>=L, v_barpi(x)>=-H}`.

Its index relative to `R` is `c^(H-L)` in the enlargement direction.
In particular, because `L>=1-Rmax` and `H<=Rmax`, every vertex lies
in `c^(-Rmax) R`. In a bounded triangle each such lattice has only
finitely many points. Combining this with the height interval and the
12 orientations per height gives a truly finite containing placement
catalogue, with no guessed denominator cutoff.

Even the sharper ideal size can involve `c^(Rmax+1)` lattice
cosets. This envelope is consequently far too large to turn the
current research into a practical exhaustive search by itself.
It does not justify using a small cutoff such as `|h|<=4` or
denominator `c^5` for a nonexistence claim.
