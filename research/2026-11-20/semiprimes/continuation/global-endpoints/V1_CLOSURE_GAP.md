# Exact remaining gap for the v=1 family

20 November 2026. This analysis does not exclude the 3431 or 5063 boards,
and does not establish a complete semiprime classification.

## What a staircase-necessity theorem would need to prove

For v=1 the primitive parameters are

    a=(u²−1)/g, b=(2u+1)/g, c=(u²+u+1)/g, g=gcd(3,u−1).

In the odd mixed-prime branch u is even. The two possible prime factors
are p=(u²+4u+1)/g and q=(2u²+2u−1)/g. The first residual examples are
u=6 giving 5063 and u=10 giving 3431; neither exhausts the residual
family.

The existing staircase construction requires positive integer load
coordinates (n_i,m_i), with n_i=m_i modulo 3 when g=3, satisfying

    sum n_i=2, sum m_i=u−2,
    r_i=[n_i+(u+1)m_i]/g <= b=(2u+1)/g.

Because n_i>=1, this last inequality forces m_i=1. There can be at
most two loads because their positive n_i sum to two. Hence u−2<=2,
or u<=4. At u=4 two unit loads give the known 143 construction.

To extend this conclusion to unrestricted tilings one must prove the
following currently missing geometric implication:

> If the unit v=1 F2 board has any tiling, with arbitrary rotations,
> translations and T-junctions, then it admits such a positive load
> decomposition with the individual capacity bound r_i<=b.

An existence normal form would suffice: the original tiling would not
need to be a staircase, but its existence would have to imply the
existence of the load list. No existing result proves this implication.
It is stronger than a bound on the number of occupied heights. Even a
two-height tiling does not automatically supply the prescribed staircase
regions or their load capacities.

## Why the available global results stop before this implication

The no-remote-gap theorem makes occupied heights contiguous, after the
stated replacement at a missing middle height. It does not reduce that
interval to two heights. The pure-middle-path theorem is conditional on
an actual supported path using only that mesh. The unconditional upper
median path may mix its two alphabets and may be longer than a+b.
Canonicality of pure paths does not eliminate these mixed paths.

The shortest genuine upper path is canonical, but there is no theorem
forcing a hypothetical tiling to contain a shortest path. The existing
first-mixed-path calculations still retain locally compatible words above
the canonical minimum. These are partial bank configurations, not complete
tilings. Longer paths and other signed direction inventories remain separate
possibilities.

The v=1 stopped-run purity excludes particular equilateral, F1 and
pentagonal subregions. It requires a genuine supporting side and the
specified protected endpoint sectors. The actual F2 sides have lengths
b(2a+b), a(a+2b), c². One cannot insert the necessary internal ab side
without proving that the corresponding subregion occurs in every tiling.
That is precisely the missing geometric step, rather than an arithmetic
consequence of a+c=ub.

Per-height divisibility, line-population and phase-tree lower bounds
charge additional orientations and phases. Their costs do not currently
exhaust the board area N=2c²+3ab. A failure of a bounded-height or bounded-
phase catalogue cannot be promoted to a full-board exclusion without a
separate reduction theorem. The new complete-row integer projection
avoids this issue, but an actual unguarded UNSAT certificate is still
needed for each board it is to exclude.

## A uniform positive formal inventory explains one methodological limit

Here is an explicit aggregate-direction inventory for every primitive odd
norm tile a>b, not just v=1. It shows that total tile count, all oriented
edge-length totals by direction and height, and the basic population
consequences leave ample room beyond the staircase threshold.

Let T(h,j,s), s=+1 or −1, denote the orientation with obtuse vertex 0,
other vertices −a z^h rho^j and b z^h rho^(j+s). Orient its boundary
counterclockwise. Only the orientation is recorded: no positions or
nonoverlap are claimed. Use these five multiplicities:

| Orientation | Multiplicity |
|---|---:|
| T(0,3,+1) | 2a |
| T(0,4,+1) | a |
| T(0,2,+1) | b |
| T(1,4,+1) | c |
| T(1,0,−1) | 2c |

Adding their oriented lengths on each axis, separately at every height,
gives exactly the three board-side currents:

    height0, axis0: b(2a+b),
    height0, axis1: −a(a+2b),
    height2, axis1: c².

All other direction totals cancel. In particular height1 cancels
exactly. The initial tile count is 3a+b+3c. Opposite orientations
T(h,0,+1), T(h,3,+1) have opposite aggregate direction currents.
Add (c²−3c)/2 such pairs at height 1 and
(c²+3ab−3a−b)/2 pairs at height 0. Both are nonnegative integers.
The final count is exactly N, with populations

    n_0=c²+3ab, n_1=c².

Thus n_1 is an odd multiple of c well above the basic lower bounds, the
exceptional population has the correct residue modulo c, and the support
is contiguous. The two controls give (n_0,n_1)=(2062,1369) and
(3214,1849). This is only a positive *unplaced* inventory. It does not
meet the spatial endpoint equations, per-line requirements, or placement
constraints. Its purpose is to identify exactly why aggregate currents
cannot supply the desired universal staircase-necessity theorem.

The elementary identity is checked in `check_v1_inventory.py`, including
101 even parameters 4<=u<=204 and both controls. These computations verify
the displayed formulas; they do not convert the inventory into a tiling.

## Conclusion of this attempt

No new condition obtained here excludes all v=1 boards beyond u=4.
The precise unresolved issue is geometric realizability outside the
positive bounded-load normal form. The full-board integer projection is
a sound way to search for an unrestricted finite obstruction, but its
current inconclusive runs and all previous patch exclusions leave that
issue open.
