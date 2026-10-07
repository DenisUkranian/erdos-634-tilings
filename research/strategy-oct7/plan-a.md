# Plan A audit: global orientation normalization

7 October 2026. This is a research-plan audit and a short necessary-condition
proof. It is not a complete classification of triangle tile counts.

## What a surviving normalization theorem would have to say

Fix a primitive plus-norm tile, `c²=a²+ab+b²`, and one classified triangular
target at its prescribed integer scale. Put `rho=exp(i*pi/3)` and
`z=(a+b*rho)/c`. A tile with short height h has its two short edges at h
and its long edge at h+1 or h-1.

The useful conjecture concerns **existence of a different tiling of the
entire target**, preserving its boundary, its unit tile, and its scale.
For example, one could try to prove a short-height window of two or three
consecutive heights determined by the target. This is not a statement that
every existing tiling has that window.

The following established barriers must be retained:

* The actual triangular embedding in
  [the extreme-island example](../../docs/extreme-pure-island-in-triangle.md)
  has a unique highest pure component which cannot be replaced by the
  opposite pure state. The same whole triangle nevertheless has a lower-
  height alternative. It refutes the proposed local move, not global
  normalization.
* A collar of bounded tile count or bounded physical width does not repair
  that opposite-pure move uniformly under scaling; see the
  [collar budget](../../docs/chirality-collar-budget.md). This does not rule
  out global or mixed moves.
* Minimality of a nonnegative integer energy establishes that an energy
  minimizer exists. It does **not** establish a move which decreases its
  energy. Every proposed descent proof must specify and prove its geometric
  replacement before using minimality.
* The [median-cut population theorem](../i120-global-oct7/HEIGHT_LEVELS.md)
  gives divisibility by c. Its cut lattice has index c, not c². Increasing
  that index without an additional theorem is invalid.

## A precise exclusion: I120 cannot have just one short height

**Proposition.** Every I120 tiling by a primitive plus-norm tile uses at
least two distinct short heights, at every positive integer scale m.
Reflections and T-junctions are allowed.

The canonical exterior edge heights are -1, 0, 1. If every tile had one
short height h, all available edge heights would lie in
`{h-1,h,h+1}`. Thus h would have to be zero.

Assign a directed edge of height h and rotation j the value
`length*(-1)^j*X^h`. The two tile chiralities have counterclockwise values

    a-b-cX,       -(a-b)+cX^-1.

After summing actual tiles and cancelling all internal atomic segments,
an all-short-height-zero tiling would therefore give integers U,V with

    (a-b-cX) U + (a-b-cX^-1) V
       = mb(a+2b) + mbcX + mbcX^-1.

The coefficients at X and X^-1 require `U=V=-mb`. The constant term on
the left then equals `-2mb(a-b)`, whereas its required value exceeds this
by `3mab>0`. This is a contradiction.

When a>b, there is also a geometric proof using the already established
[adjacent-c theorem](../i120-continuation/BOUNDARY_ADJACENCY.md): the target
base has a c-edge at height zero, whose tile has short height 1 or -1.
This contradicts the forced one-height value h=0 above.

This proposition does not refute a two-height normal form. The formal
unplaced inventory for 154, `(n_0,n_1)=(141,13)`, already survives the
two-height restriction. It is not an actual tiling.

## What a bounded-height theorem would actually deliver

Suppose all short heights lie in `[L,U]`, and put `K=U-L+2`. Rotate by
`z^(1-L)` and translate one target vertex to zero. All original edge
heights now lie in `[0,K]`. By the previously proved integer-atom theorem,
each atomic edge vector is an integer multiple of `rho^j z^d`, with
`0<=d<=K`. Since

    z^d = (a+b*rho)^d / c^d,

every vertex lies in `c^(-K) Z[rho]`. Connectivity of the subdivided edge
graph gives this assertion by integration from the chosen vertex. This
uses integer atomic lengths, not merely integer whole tile lengths.

Consequently, if the target has diameter R, it has
`O((R*c^K+1)^2)` possible lattice vertices. For a fixed tile and a fixed
height window, this is a finite placement problem with a denominator bound
independent of the number of tiles. Exact containment and pairwise
non-overlap, together with the prescribed total area, would certify a
chosen placement set.

**This conclusion is still a finite search, not the requested structural
classification.** A second theorem would have to characterize positive
completion of these placements by arithmetic conditions on the parameters.
The existing finite-N disk realization theorem already handles the
verification question without a uniform height bound.

Nor does bounded height produce a bounded-width automaton. Ordinary
triangular subdivisions have one short height and arbitrarily large grid
minors, and the geometric bound applies to all alternative tilings of
large targets; see the
[width audit](../../docs/audits/seam-automata-global-width-2026-10-07.md).

## Practical milestone and stopping rule

An optimal attempt at this route first asks for one explicit *whole-target*
replacement theorem for a named branch, preserving the unit scale and
reducing a rigorously defined height energy. It must allow the known
nonconvex obstruction and must specify the boundary of its replacement.
Without such a move, invoking an energy minimizer cannot advance the proof.

Even a successful move would need a separate positive-completion theorem,
or a stronger normal form consisting directly of a parameterized family
of constructible macroregions. A grammar made only of the current gamma
regions is insufficient, by the
[gamma boundary obstruction](../f3-position-invariants/GAMMA_BOUNDARY_OBSTRUCTION.md).
A finite parameterized grammar remains possible; it must not be confused
with a fixed finite collection of seed tilings.

Thus this route retains high potential scope, but currently contains two
substantial independent gaps. Neither has been closed in this audit.
