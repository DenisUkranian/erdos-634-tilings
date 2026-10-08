# Independent mathematical audit of the all-adjacent-scale theorem

8 October 2026. **PASS**, as a sufficient tiling theorem. This audit reads
`../group1-helper/ADJACENT_ALL_SCALES.md` and
`../group1/check_all_adjacent_symbolic.py`, independently checks the
geometric implications and symbolic verification logic, and replays the
checker. It is internal review, not external peer review or formalization.

The proved consequence is: for every `u>=2`, `v=u+1`, both the W and
beta targets with tile `(uv,2u+1,v²)` are tiled at **every integer scale
`m>=v`**. No claim about the smaller scales is licensed.

## 1. Partition and tileability

For `u>=3,2<=t<=u−1`, set `m=v+t`. In the lower part, the j-th horizontal
layer has left slope `(-v²,uv)` and right slope `(-u²,uv)`. Its two
triangles are respectively ordinary B-grid scale v and A-grid scale u.
The intervening width is `uv+(2u+1)j=ju+(u+j)v`. This is a positive
integral collection of A and B columns with precisely the claimed
heights. Thus the layer is a dissection, not just an area identity.

The central region has parallel boundaries
`ux+vy=0` and `ux+vy=u(2u+1)(u+t)`. Each layer therefore has horizontal
width `(2u+1)(u+t)`, and the left/right B triangles of scale v leave
exactly `(t−1)u+(u+t−1)v` for the rectangle. Both coefficients are
nonnegative. The same complete strip cell applies upstairs with
width `(2u+1)m`, leaving `tu+(u+t)v`.

For the upper pentagon, `uv<um<2uv` puts its left kink strictly inside
the second negative layer. At the upper-left corner F of that layer's
left B triangle, deleting the B-grid corner of scale t is legitimate
because `t<v`. The two non-apex vertices of the removed corner are
`(-um,-uv)` and `(-um,-um)` by the displayed identities in the proof.
They are exactly the endpoints needed to create the target's vertical
edge and sloping continuation. Thus the removed part lies outside the
pentagon; it is not a signed piece inside it. All later layers are
complete strip cells and end at `tv²−(2u+1)m=u²t−v(2u+1)`.

The four outside macroregions pass the checker’s exact side and
homothety identities. The first three are ordinary tile triangles
with a smaller corner grid removed: their scale pairs are
`(um,ut)`, `(vt,t)`, and `(b−t,u−t)`, all integral, with a strictly
positive difference. Their respective leg lengths are exactly the
tile sides multiplied by that difference. The fourth is a full
m-fold tile triangle. Convexity and parallel-base homothety locate
the removed triangles at the correct common apex; they are actual
grid annuli.

**Endpoint convention:** at `t=2`, the last aggregated upper-strip
macroregion has zero area and is omitted. This is the empty sum of
the later complete layers. The other nonnegative polynomial checks
and current identities remain valid on this boundary of parameter
space. The statement should not require all 13 displayed aggregates
to have strictly positive area at every parameter.

## 2. The symbolic check proves a geometric partition

The substitution `u=p+q+3,t=q+2` is a bijection between the stated
integer domain and `p,q>=0`, with inverse `p=u−t−1,q=t−2`.
The polynomial class implements exact integer addition and
convolution. Nonnegative coefficients therefore establish all its
nonnegative sign assertions throughout the domain. No finite sample
is being used to infer a universal identity.

For each macroregion, a single orientation is chosen and its area
and every edge-side determinant are nonnegative polynomial
identities. Hence every nondegenerate specialized polygon is convex
and has the declared positive orientation. The checker places each
edge on its **positioned** supporting line, records signed endpoint
events, and proves their exact cancellation against the target.
On each line, vanishing endpoint jumps imply vanishing edge current
because the current is zero outside a bounded set. Any accidental
coincidence of lines or endpoints at a parameter value merely merges
already cancelling events.

Consequently the sum of the oriented boundaries of the positive
macroregions is exactly the target boundary. The multiplicity
function is locally constant off those edges and is zero outside
after subtracting the target indicator. Thus the multiplicity is
one inside and zero outside: both containment and disjoint interiors
follow. The count identity is a consistency check, not a substitute
for this boundary argument.

The metric has positive Gram determinant
`b²(4v²−u²)` and gives the A/B basic triangles side lengths `(uv,b,v²)`.
As an extra check on the outer normalization, in the unscaled model

```
O−A=(muQ/b)*(v,−u),   A−C=(0,−bm),
O−C=(mv/b)*(uQ,−v³).
```

The first unit vector has physical length b, the second axis has
unit physical length v, and the last vector has squared physical
norm `b²v⁴`: use `Q−P=−v²` and `v⁴−u²Q=b²` in the Gram form.
Therefore the target sides are exactly `m*(uQ,vb,v³)`, as required
for W. The checker’s b-scaled coordinates preserve these facts.

## 3. Closing the integer-scale quantifier

The old seed v and the previously proved seed v+1 cover t=0,1.
The present dissection supplies t=2,...,u−1. These are precisely
the u consecutive scales `[v,v+u−1]`, one in each residue modulo u.
The prior arbitrary-seed +u cap is applicable at each because its
cutoff is `v−u=1`; iteration supplies every larger scale. For u=2
the first two seeds already suffice and the new t-range is empty.
The standard W-to-beta attachment is a disjoint ordinary triangular
grid, so it preserves this full scale tail.

The replay returns PASS with 13 full-target aggregates, 180 full-target
convexity sign checks, 68 generic cell/band sign checks, positioned
boundary cancellation, positive metric, outer-annulus homotheties,
and the exact tile-count identity. File hashes and replay output are
recorded in `adjacent_audit_checked.json`.
