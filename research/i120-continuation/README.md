# The I120 scale-one barrier, including N = 154

7 October 2026. Denis Paliy, research with ChatGPT assistance.

This continuation does **not** decide whether the triangle `(91,91,154)`
can be tiled by 154 copies of `(8,7,13)`. It identifies the scope of the
invariants and boundary restrictions proved here. The current literature also retains
this particular candidate: Beeson, *Tilings of an Isosceles Triangle*,
[arXiv:1206.1974v7](https://arxiv.org/pdf/1206.1974v7), Table 5 and its
following remarks. No obsolete boundary restriction from the author's
2012 *Triangle Tiling V* manuscript is used here.

## 1. Complete directed signatures do not exclude any integral I120 scale

Let `a,b,c` be a primitive integer 120-degree tile, so

    c² = a² + ab + b².

Write `ρ=exp(iπ/3)` and `exp(iθ)=(a+bρ)/c`. Thus `θ=β`, and
`α=π/3−θ`. Directed lengths are recorded in

    R = Z[T,X,X⁻¹] / (T³+1),

where `T` records rotation through π/3 and `X` records rotation through
θ. We deliberately do not impose the geometric relation `T²−T+1=0`:
the three separate unoriented direction classes must remain distinct
in the signature. The CCW tile and reflected tile have signatures

    P = a + bT − cX,
    Q = −a + bT² + cX⁻¹.

At integral scale `m`, the isosceles target has side lengths

    (bcm, bcm, b(a+2b)m)

and tile count `N=b(a+2b)m²`. Its CCW boundary signature is

    B_m = m[b(a+2b) + bcT²X − bcTX⁻¹].

**Exact identity.**

    B_m = −maP + (mcX−mbT)Q.                         (1)

To verify (1), expand its right side. The two `acX` terms and the two
`abT` terms cancel. Using `T³=−1` leaves constant term
`m(c²−a²+b²)=mb(a+2b)` and the two stated nonconstant terms.
The independent checker expands this identity coefficientwise over
`Z[a,b,c,T,X,X⁻¹]/(c²−a²−ab−b²,T³+1)`.

The negative coefficients in (1) are not negative tile populations:
`−P=T³P` and `−TQ=T⁴Q` represent rotations. Thus (1) gives a positive
**unplaced** orientation inventory of `m(a+b+c)` triangles. A triangle
and its half-turn have opposite signatures, so adding half-turn pairs
preserves the boundary signature.

For every primitive tile and every integer `m≥1`,

    N−m(a+b+c)

is nonnegative and even. For parity, `c` is odd and at least one of
`a,b` is odd; hence `b(a+2b)≡a+b+c (mod 2)`, and `m²≡m (mod 2)`.
There is no positive integer norm tile with `b=1`: the norm would lie
strictly between `a²` and `(a+1)²`. For `b≥2`, the strict triangle
inequality `c<a+b` gives

    b(a+2b)−(a+b+c) > a(b−2)+2b(b−1) > 0.

Consequently the inventory can be padded to exactly `N` positive
triangles, with correct total area and exactly the target's directed
signature. For `(8,7,13),m=1`, the inventory consists of 28 triangles
and 63 half-turn pairs, giving 154 triangles in total.

**Scope.** No positions are assigned. These triangles need not fit inside
the target or avoid one another. This proves that all additive,
translation-invariant, direction-dependent edge-length invariants
factoring through this directed signature pass the I120 candidates.
It does not prove that all other kinds of invariants pass.

## 2. The existing vertex-defect restrictions transfer to I120

The irrationality of `α/π` follows from
`2 cos α=(a+2b)/c`, which is rational and strictly between 1 and 2.
The corner fans of the target are exactly

    α,    α,    α+3β.

Indeed the apex equation for a fan `(r,s,t)` of `(α,β,γ)` is
`r−s=−2`, `s+2t=3`, whose only nonnegative solution is `(1,3,0)`.
Thus the total corner inventory is `(3,3,0)`, exactly as for F3.

Using the populations `x,y,z,w,p,q,r,s` defined in the existing
[vertex-defect proof](../../docs/f3-vertex-defects.md), the same counts give

    x = 1 + z + 2w + q + s,
    p ≥ 1 + z + 2w + s + 2x₃.

In particular an I120 tiling has a triple-γ interior vertex and a mixed
T-junction. Every exterior side contains a whole c-edge. For `(8,7,13)`
the forced a/b mismatch also gives a unit seam atom, by the existing
integer-atom theorem. These are corollaries of the previously proved
inventory and mismatch argument; they are not new existence results.

The complete possible counts `(A,B,C)` of whole `(8,7,13)` edges on a
91-side, after requiring a c-edge, are

    (0,0,7), (1,10,1), (2,7,2),
    (3,4,3), (4,1,4), (8,2,1).

There are 17 possible count triples on the 154-side. The checker records
them all. A count triple is not a boundary placement certificate.

The [boundary-adjacency extension](BOUNDARY_ADJACENCY.md) strengthens
this for every primitive I120 tile with a>b: **each target side contains
two consecutive c-edges**. For 154 the remaining length-91 count rows
are `(0,0,7), (2,7,2), (3,4,3), (4,1,4)`; the length-154 side has
14 remaining rows. The extension proves a necessary restriction and
does not decide the remaining placements or their fillings.

## 3. Why a single short-direction class cannot suffice

This is another corollary of the c-edge boundary restriction, included
to delimit a possible search model. Suppose all tile short sides have
one common direction class modulo π/3. If its class is `h`, the possible
edge classes are `h,h+θ,h−θ`. The exterior classes of I120 are
`0,θ,−θ`. Irrationality of `θ/π` forces `h=0`: choosing either other
exterior class for `h` misses the opposite exterior class.

The base then has the short class, and cannot contain a c-edge, contrary
to Section 2. Therefore any actual I120 tiling, at every scale, uses
more than one short-direction class. This rules out a restricted grid
model; it does not rule out the target.

## Replay

```sh
python research/i120-continuation/check_i120.py
```

The replay imports only the standard-library polynomial arithmetic from
the existing F3 signature checker. It verifies the universal identity,
the exact local corner inventories, the boundary count lists before and
after the adjacency restriction for 154, and padding on representative
norm tiles and scales. These checks
are not an exhaustive geometric search, and the retained outcome for
154 is `UNRESOLVED`.
