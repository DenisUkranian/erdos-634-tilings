# A finite global pricing theorem for congruent-triangle tilings

20 November 2026. This is a complete verification principle, not a
certificate of nonexistence for 3431 or 5063. No successful obstructing
dual for either board is supplied in this note.

## Endpoint currents

For a polygon `P` traversed counterclockwise, define its endpoint-current
vector `A(P)`. A row is a pair `(x,ell)`, where `x` is a point of the
plane and `ell` is an unoriented line direction. An oriented side from
`x` to `x+v` contributes `+1` at `(x,axis(v))` and `-1` at
`(x+v,axis(v))`. A triangle has six such contributions.

Subdividing a side leaves this vector unchanged: the new internal
endpoint receives opposite contributions. Oppositely traversed copies
of the same side cancel, including when the two banks are subdivided
differently. Therefore any tiling of a board `B` by triangles `T_i`
satisfies

```
sum_i A(T_i) = A(B).
```

The same identity holds with nonnegative real coefficients for an exact
fractional covering. Conversely, a finite real combination satisfying
the identity has the required signed covering multiplicity almost
everywhere. On any fixed supporting line, the weighted interval
indicator has zero endpoint jumps and compact support, so it is zero.
Thus all interior edge jumps in the polygon arrangement cancel. The
covering multiplicity is constant on the plane after subtracting the
board indicator, and equals zero outside a sufficiently large disk.

For nonnegative integer coefficients the identity is especially strong:
the multiplicity is one on the board and zero outside, so the positive
triangles have disjoint interiors and coefficient one. Fractional
solutions may have overlapping triangles with noninteger weights.

## Finite support finds every violating placement

Let `y` assign rational weights to a finite set `S` of endpoint-current
rows and zero to every other row. Write

```
score(T) = sum_(x,ell) A(T)_(x,ell) y_(x,ell).
```

If `score(T)` is nonzero, at least one side endpoint of `T`, with that
side's direction, occurs in `S`. Fix one such row `(x,ell)`. Every
triangle congruent to a given scalene tile and matching that row is
determined by the following four finite choices:

1. The length of the incident side on `ell`: `a`, `b`, or `c`.
2. Which of the two rays on `ell` leads from `x` to its other endpoint.
3. Which of the two remaining lengths is incident to `x`.
4. On which side of `ell` the third vertex lies.

There are at most `3*2*2*2=24` placements. Their coordinates follow
directly from the cosine law. Test their vertices against the three
closed half-planes of `B`; this is equivalent to containment because
both triangles are convex. Repeating the construction for all `s=|S|`
rows gives at most `24s` placements before deduplication. Every other
contained congruent placement has score exactly zero.

This is a global separation oracle. It imposes no restriction on
orientation heights, translation phases, or coordinate denominators.
It does not need to enumerate all possible placements in the board.
An arbitrary tile meeting a supported row is already fixed by one of
the 24 choices, even if its other rows have never occurred in the LP.
A tile with a supported point in the interior of one of its edges
has no endpoint contribution there; such an incidence need not be
enumerated unless another actual endpoint row is supported.

## Exact obstruction theorem and robust positive-score bound

Suppose the finite enumeration verifies

```
score(T) <= 0
```

for every contained candidate, and suppose

```
score(B) > 0.
```

Then the board has no tiling by congruent copies of the tile. It has no
finite exact nonnegative fractional covering either. A hypothetical
cover would give

```
0 < score(B) = sum_i w_i score(T_i) <= 0,
```

where `w_i>=0`, a contradiction. The absent candidates contribute
zero by the finite-support lemma. Reflections, arbitrary orientations,
and all partial edge contacts are included.

There is a more robust version. Let `N=area(B)/area(T)` and let `M` be
the maximum of zero and all scores in the finite candidate enumeration.
Every other placement scores zero, so this is a valid global upper
bound on a tile score. Consequently

```
score(B) > N*M
```

also excludes every exact nonnegative covering. The total coefficient
of any such covering is `N` by area, so its score is at most `N*M`.
This version allows small positive column scores introduced by rounding
a numerical dual to rational coefficients. The verifier computes `N`
from exact polygon area and computes `M` and the exact uniform margin
`score(B)-N*M`. No numerical tolerance is used in the final decision.
The stronger finite-budget bound below
is the verifier's actual acceptance rule; this uniform bound is also
reported for comparison.

## Stronger finite-budget bound

Every individual physical placement in a finite exact nonnegative
cover has coefficient at most one. Choose a point strictly inside
that triangle and away from all tile edges. The total covering
multiplicity there is one and every coefficient is nonnegative, so
that triangle's coefficient cannot exceed one. Combine duplicated
placements before applying this argument.

Let `s_1>=s_2>=...>0` be the positive scores of the distinct contained
placements in the finite candidate enumeration. Pad this sequence
with zeros, put `k=floor(N)` and `f=N-k`, and define

```
U_N = s_1 + ... + s_k + f*s_(k+1).
```

An exact nonnegative cover has total coefficient `N`, with each
placement coefficient at most one. Its score is consequently at most
`U_N`, obtained by spending that coefficient budget on the largest
positive scores first. All nonincident placements have score zero.
Thus `score(B)>U_N` is a global obstruction. For the two original
boards, sum the largest 3431 or 5063 positive scores, padding with
zeros if necessary. This is never weaker than `N*M`, and can be much
stronger when only a small number of placements have positive score.

The checker deduplicates candidates by their exact three-point sets
before computing this bound. Its reported `global_obstruction_margin`
is `score(B)-U_N`. The separate
`uniform_score_obstruction_margin` is `score(B)-N*M`.

## Optional geometric penalties at finitely many points

Choose finitely many exact points `P_r` and rational weights `lambda_r>=0`.
Replace each tile score by

```
s(T) = score(T) - sum_r lambda_r * 1(P_r strictly inside T).
```

In any genuine tiling the number of tiles containing a fixed point
strictly in their interiors is at most one. For a finite exact
nonnegative fractional cover, the sum of their coefficients is also
at most one: a sufficiently small common neighborhood of the point
lies in all those triangle interiors, so a larger coefficient sum
would give covering multiplicity greater than one on an open set.
It follows that the sum of the adjusted tile scores is at least

```
L = score(B) - sum_r lambda_r.
```

Every tile whose endpoint score is zero or negative has adjusted
score at most zero, because all penalties are nonnegative. Thus
every positive adjusted score still belongs to the same finite
endpoint-incident candidate list. No search over placements incident
only to a penalty point is needed. Compute `U_N` from the positive
adjusted scores instead of the unadjusted scores. The exact test

```
L > U_N
```

is a global obstruction. The default with no penalty points is the
previous theorem. A point on an edge or at a vertex contributes no
penalty; the checker uses three strict rational determinant signs.

Add the optional top-level field

```json
"point_penalties": [
  {"point": ["400/37", "100/37"], "weight": "3/2"}
]
```

or compact entries `[x,y,weight]`. Duplicate points are combined and
zero weights are removed; negative weights are rejected. With this
extension, `target` remains the endpoint boundary score,
`adjusted_target_lower_bound` is `L`,
`top_budget_score_bound` is the bound using adjusted scores, and
`global_obstruction_margin` is `L-U_N`.

## A signed LP and its global verification

For a finite placement pool with endpoint matrix `A` and board vector
`b`, one useful phase-I LP is

```
minimize sum_i x_i^-;
A(x^+ - x^-) = b;
x^+,x^- >= 0.
```

Its dual constraints on the included columns are
`-1 <= A_i^T y <= 0`, with objective `b^T y`. A positive finite-pool
objective is not a proof: omitted positive columns can violate the
upper inequality. For a fixed endpoint row set, generate every contained
placement meeting the nonzero dual rows, add the violated columns on
those rows, and re-solve. A new column's previously unrepresented rows
need not be installed immediately. When a positive primal is available,
test its complete current and install missing nonzero rows separately.
The lower inequality matters when reporting a
globally valid optimum of this signed LP; for the nonexistence theorem
itself only `A_T^T y<=0` on all positive placements and `b^T y>0` are
needed. A finite global certificate is sufficient, but there is no
claim that this column-generation procedure must terminate.

Avoid introducing unnecessary positive columns outside the board.
They are not admissible tiles of a hypothetical tiling. The checker
correctly tests only wholly contained triangles. Signed scaffolds with
outside triangles may be useful for initializing a different LP, but
their role and costs must be specified separately.

## Exact checker interface

Run:

```sh
python3 verify_endpoint_dual.py certificate.json
python3 verify_endpoint_dual.py --self-test
```

The first command exits successfully only when the exact global
obstruction margin `L-U_N` is positive, with `L=score(B)` if there
are no point penalties. It prints up to ten
positive-scoring placements, including their exact scores, to help
diagnose a failed certificate or a successful robust one. It exits
with code 2 when the obstruction margin is nonpositive.
It reports every rational exactly. It rejects
floating-point coordinates and weights.

An optional top-level field `"boundary_arithmetic": true` excludes
contained placements that cannot occur at the exterior in a tiling.
For every candidate vertex on an outer side it requires both distances
to that side's endpoints to belong to the additive semigroup
`<a,b,c>`. The checker builds this semigroup with an exact integer
dynamic program. All three outer lengths must be integers in this mode.
The default is false, so the unrestricted geometric-containment test
remains available for comparison.

The optional restriction is necessary. The exterior side of a tiling
is partitioned into full tile sides of lengths `a,b,c`. Every tile
vertex on that side is an endpoint of this partition: otherwise a
boundary tile whose side passes through the point occupies the whole
available small half-disk, leaving no room for the proposed incident
tile. The two portions of the exterior side therefore consist of
whole tile sides, which proves both semigroup conditions.
The same argument holds for a finite exact nonnegative fractional
cover. Boundary intervals give a positive directed flow, directed
monotonically from one exterior vertex to the other. Each positive
endpoint can be traced backwards to the start and forwards to the end
through finitely many whole tile edges; their lengths are in the
semigroup. If a proposed tile vertex is not such an endpoint, the
through-interval weights already sum to one on the entire small
half-disk. The extra tile would give covering multiplicity greater
than one. Thus the global fractional-cover obstruction also remains
valid when this option is enabled.

Example schema for the 3431 board, using an illustrative weight that
is **not** claimed to be an obstruction:

```json
{
  "format": "endpoint-current-dual-v1",
  "sides": [33, 7, 37],
  "board": [[0, 0], [511, 0], [0, 1551]],
  "rows": [
    {"point": [0, 0], "height": 0, "phase": 0, "weight": "1/2"}
  ]
}
```

Coordinates are axial coordinates in `1,rho`, where
`rho=exp(i*pi/3)`. A row's `height=h, phase=j` means the axis of
`rho^j z^h`, with `z=(a+b rho)/c`. Phase is taken modulo 6; opposite
directions are automatically identified. Compact rows
`[x,y,h,j,weight]` are also accepted.

Alternatively a dictionary row can give `"axis":[u,v]` instead of
height and phase. This can be any nonzero rational axial vector on
the direction whose squared norm `u^2+uv+v^2` has a rational square
root; the checker normalizes it exactly. In particular every primitive
integer direction generated from the F2 tile can be used directly,
without reconstructing its height.

Rationals are represented by integers, fraction strings such as
`"17/1369"`, or two-element lists `[numerator,denominator]`.
The script combines duplicate rows, drops zero weights, independently
checks the metric of each generated triangle, and uses exact rational
half-plane containment and column scores.

The finite endpoint enumeration is an extension of the earlier project
verifier `packing-distance/verify_unrestricted_dual.py`, which used the
same mechanism for placement-distance inequalities. The unrestricted
negative-tiling conclusion here requires the stated stronger sign
certificate; a distance lower bound alone does not provide it.
