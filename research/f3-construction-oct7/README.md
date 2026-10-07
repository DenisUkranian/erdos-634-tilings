# Two restricted construction checks for primitive F3

No tiling or unrestricted obstruction for 4830 was obtained.

## Prescribed macro scales

The exact area identities

```
4830 = 5*31^2 + 5^2
     = 43^2 + 3*31^2 + 2*7^2
```

suggest two specific six-macrotriangle constructions. The script
`fixed_macro_probe.py` adapts the existing exact advancing-corner search
to each prescribed multiset of integer scales. Both restricted searches
exhausted: respectively 19 and 50 nodes. Their exact coordinates and
restrictions are retained in `fixed-macro-report.json`. No positive
certificate was found. This does not exclude other macro scale multisets,
larger dissections, or a unit-tile tiling of 4830.
These are search-engine exhaustion reports, without a separate proof
certificate or independent replay; they are not promoted to certified
nonexistence theorems even for the two restricted macro families.

Replay from the repository root:

```bash
python research/f3-construction-oct7/fixed_macro_probe.py
```

## Why a proposed interface divisibility does not follow

The reduced gamma quadrilateral for `(a,b,c)=(24,11,31)` has vertices

```
(0,0), (194,0), (506,143), (242,528)
```

in Eisenstein coordinates. Its area is that of 986 tiles. Its side of
length 194 needs a c-edge in any filling, since 194 is not in
`<24,11>`, although the known 15-tile boundary collar is locally feasible.

Consider a hypothetical filling using short-edge heights 0 and -1 only,
where `z=(24+11*rho)/31` and height means the exponent of z in an edge
direction. An interface between the two heights can have **either** of
the following forms:

* a c-edge of a height-0 tile, of edge height -1, meeting short edges
  of height--1 tiles;
* a c-edge of a height--1 tile, of edge height 0, meeting short edges
  of height-0 tiles.

The first form has vectors in `31*z^-1*Z[rho]`; the second has vectors
in `31*Z[rho]`. Multiplication by z sends these respectively to
`31*Z[rho]` and `(24+11*rho)*Z[rho]`. The second contribution does not
vanish modulo 31. It therefore invalidates the proposed inference that
the number of c-edges on the 194-side must be divisible by 31. The same
issue occurs with heights 0 and +1. No two-height exclusion is proved.

The invalid inference was noticed before being used in any theorem or
classification. This note records the precise missing interface term so
that the same route is not restarted under a stronger-looking notation.
