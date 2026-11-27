# A simultaneous convex enclosure for a physical cut

For any subset of the positioned lift tree, take the oriented exterior walls assigned to it and all the directed whole unmatched long sides on its cut. Orient the far bank counterclockwise around its tiles and reverse the near bank when selecting the far subtree. More generally use the indicator difference on each tree edge as in [the all-cuts identity](ALL_CUTS.md). Sort this balanced vector inventory by counterclockwise heading and concatenate it. Call the resulting convex polygon W. The construction uses actual vectors in one common physical frame.

**Theorem.** If the selected short lifts carry a positive population of n tiles in the board T, there is a convex polygon K inside T of at least n tile areas which also fits inside one translate of W. This includes disconnected unions, holes, reflections and non-edge-to-edge tilings.

Work in axial coordinates and put
$$H(P,Q)=\sum_{e\in\partial Q}\max_{p\in P}\det(p,e)$$
with the edges of Q directed counterclockwise. A segment uses its two opposite steps. This is the planar mixed-area functional normalized so that H(P,P) is doubled axial area. It is symmetric, translation invariant, additive under Minkowski sums in either argument, and monotone under convex containment. For example, the right derivative of doubled area of Q+sP at zero is twice the sum of the first-order edge strips, namely 2H(P,Q). Merging the two angularly sorted edge lists shows that the doubled area of Q+sP is quadratic in s (the individual vertices are affine in s). Exchanging P and Q shows symmetry of the linear coefficient. The mixed-area inequality H(P,Q)² ≥ H(P,P)H(Q,Q) follows by comparing the linear coefficients in planar Brunn–Minkowski. Segments follow by continuity.

For any test polygon Q translate it to contain zero. The nonnegative sublinear cost of a directed edge e is max det(q,e) over q in Q. Subdivision preserves it and cancellation of opposite overlaps cannot increase it. Consequently the exposed boundary of the actual tile union U costs at most H(Q,W). Fill holes, decompose into outer simple polygonal contours (separate point contacts if necessary), and take their convex hulls. Consecutive extreme vertices occur in boundary order. Replacing each intervening arc by its chord cannot increase cost. Nested filled contours can be discarded. Merge intersecting hulls: translated about a shared point their support functions are nonnegative, so the maximum of the two support functions is bounded by their sum. By symmetry this merge cannot increase the sum of H(hull,Q). Their combined covered area cannot decrease. For disjoint components use the [translation argument inside a triangle](ALL_CUTS.md) to move two until first contact and merge. All choices can be made without reference to Q. The final K lies in T, has at least the original area and satisfies H(K,Q) ≤ H(W,Q) **simultaneously** for every convex Q.

Here is a second way to read the last inequalities. For an edge e of W, the requirement K ⊂ W+t is one linear inequality in t with normal proportional to the outward normal to e. If their system were infeasible, the linear alternative gives nonnegative weights on these normals with zero weighted sum and strictly positive weighted sum of the support excesses of K over W. Rotate the weighted normals counterclockwise by a right angle and concatenate in angular order. They bound a convex test polygon Q, possibly a segment, for which that sum is H(K,Q)−H(W,Q)>0. This contradicts the simultaneous bounds. W must have positive area, since a segment perpendicular to a missing width would otherwise give K zero width by the same mixed inequalities.

## Checking a bound without finding either translate

Put Q₀=T, B₀=H(T,T). Choose further polygons Qᵢ with Bᵢ=H(W,Qᵢ)>0. For nonnegative weights wᵢ take the Minkowski sum P of the scaled polygons (wᵢ/Bᵢ)Qᵢ. The theorem gives H(K,P) ≤ Σwᵢ. The mixed-area inequality and the doubled axial area ab of a tile now require
$$n ab\, H(P,P)\le (\textstyle\sum w_i)^2.$$
This combines board, signed directions and population in one inequality.

At 3431 a gate with |E−O|=37 costs at least 67 owners if its subtree has **more than 2775 tiles**. The caps at 63 and 65 owners separately are **2627** and **2775**. The input lists are the ten [saturated](SATURATION.md) and 54 [one-defect](ONE_DEFECT.md) inventories, modulo even rotations. For each compute W and use W, segments along the inventory headings, and closing triangles from triples of headings as tests. Include both reflected board orientations. It suffices to exclude a candidate odd multiple of c, since every feasible population in this class is an odd multiple of c.

The [verifier](mixed_enclosure.py) covers orientation continuously in six sectors with rational unit rotations (1+rρ)/(1+r conjugate(ρ)), 0 ≤ r ≤ 1. Their arguments increase continuously from zero to π/3. A numerical optimization only proposes nonnegative integer weights. On each closed subinterval freeze one supporting board vertex per test edge at the midpoint. Its endpoint values give valid rational lower bounds for the weighted cross term. The frozen sum has the form A cos θ+B sin θ. Between endpoints less than π apart it interpolates with nonnegative sine coefficients whose sum is at least one. When both endpoint values are nonnegative, their minimum therefore bounds the entire interval from below. The remaining terms are rotation invariant. Acceptance requires a strict rational inequality. A failed certificate gives no exclusion. The replay either verifies a weaker threshold or carries forward the prior proven cap.

Run with NumPy and enabled assertions:

```sh
OPENBLAS_NUM_THREADS=1 python3 mixed_enclosure.py | diff - MIXED.json
python3 mixed_control.py | diff - MIXED_CONTROL.json
```

The [independent control](mixed_control.py) reconstructs every subset of occupied lifts and wall markers on each complete 143 board. It checks the chain area, then constructs Minkowski sums by a hull of all pairwise vertex sums. The geometric area, rather than the certificate's support formula, gives the left side of the bound on 30 tests on each board. Neither target is closed.
