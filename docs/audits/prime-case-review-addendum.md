# Fresh adversarial review of the published prime-case candidate

29 September 2026. Reviewed source: [prime-case-candidate.tex](../../paper/prime-case-candidate.tex), version 0.1.0. This separate ChatGPT review pass is internal mathematical scrutiny, not external refereeing or formal verification. The result of earlier audits was not used as a premise.

## Conclusion

I found no concrete counterconfiguration or invalid inference in the current W column-completion argument or the beta forced-corner reduction. In this pass I isolated the weakest common step—the conversion of an actual seam into two whole-edge chains—and reconstructed it directly from the definition of a finite tiling. I then checked the orientation alternatives and the induction order using that lemma, allowing off-grid vertices, T-junctions, reflections, and opposing chains that change tiles before reaching a grid point.

The phrase “all-prime candidate” remains appropriate. This review does not certify the original published shape-classification or rationality proofs in their entirety, and does not establish the composite-count classification.

The new counterexamples to Beeson's Lemma 55 do **not** invalidate the paper's prime deduction. Its theta-isosceles row cites Theorem 22, whose proof uses Lemma 54 and not Lemma 55. An even simpler replacement for that row is the independent squarefree boundary obstruction already available in this investigation; its proof is reproduced in Section 5 below.

## 1. A local seam lemma without a lattice assumption

Let a convex polygon be the union of finitely many closed triangles with pairwise disjoint interiors. Suppose a segment I is covered by actual collinear tile edges and its relative interior lies in the polygon's interior.

**Barrier claim.** No tile can contain a point of the relative interior of I in its own interior. At such a point an existing edge belongs to another tile; on one side of that edge the latter tile occupies an open region arbitrarily close to the point. A tile containing the point in its interior would overlap that region. The same argument applies at a junction of consecutive supplied edges, using one of the adjacent nontrivial edge intervals.

Consider a point of I that is not any tile vertex. On each side of I the tiling must have a tile adjacent to that point. By the barrier claim, that tile has a boundary edge on the line of I. Finiteness now partitions I, on each side, into collinear tile-edge traces. At an interior endpoint of one trace, the next trace cannot bend away and leave a positive subinterval uncovered, nor can a tile cross the line: the original supplied segment remains an actual barrier there.

These traces might initially be portions of larger tile edges at the two ends of I. There are three distinct ways the manuscript excludes that endpoint problem:

1. **Maximal component.** If I is a maximal connected union of actual edges on its line, an end cannot lie in the interior of a participating edge, because that edge would extend the union.
2. **Supporting boundary.** If an end lies on a supporting side of the convex target, an opposing edge cannot overrun that end outside the target.
3. **An actual start or transverse crossing.** An explicitly supplied tile edge starting at an end starts its side chain there. Alternatively, if extending I enters another tile's interior, no collinear edge can overrun that end.

Only after applying these endpoint facts may one equate a segment length with a nonnegative integer sum of whole tile side lengths. Every use of the short-chain arithmetic in the reviewed proof has such endpoints. No assumption that all vertices of the unknown tiling lie in the generated grid is necessary.

This also addresses the “swallowed next edge” objection. An opposing tile cannot swallow the next known edge because swallowing an interior point of an actual edge produces positive-area overlap. An unknown continuation must never be supplied by this principle alone, but the proof only propagates opposing chains along edges it has already forced.

## 2. Direct fan audit for the W continuation

Use rays `+p`, `+q`, and `q−p`, with arguments `0`, β and `θ=α+β` respectively. Their order is strict regardless of whether a<b or a>b. A top-row inner junction has the old rectangle below it and the preceding normal D tile in the sector from θ to π. Its unfilled fan is therefore precisely the sector from 0 to θ.

Irrationality makes the inventory of that fan exactly one α and one β. There are only two orders:

| Order from +p toward the theta ray | Actual geometric consequence | Applicable existing result |
|---|---|---|
| α then β | The last tile has β at the junction and an a- or c-edge on the theta ray, on its lower/right side. | The diagonal-chain lemma at this junction's column index. |
| β then α | Their common ray is +q. The β tile is on its right, the α tile on its left. | The earlier column's no-right-a property fixes the β tile; its complete normal c-only left side fixes the α tile. |

In the second row, the right tile's q-side cannot have length a and hence is c. The left tile's q-side cannot have length b because its edge belongs to the already identified normal c-chain on that same side of the same column. Both placements are uniquely the stated D and U tiles. Their coordinates are consequences of this placement, not assumed coordinates of an arbitrary unknown tile.

At the outer column endpoint, the supplied real upward q-ray leaves an α fan on its left, between directions β and θ. Choosing b on q would place c on the theta ray, which is exactly the forbidden diagonal configuration. The other choice is the standard U. Thus the same argument completes the last cell of the row.

The diagonal lemma itself does not assume an edge-to-edge match. After k known b-edges, short-b purity says that the current b-chain endpoint cannot simultaneously be an endpoint of the opposite chain, since that opposite chain began with an a- or c-edge. Therefore it is in the relative interior of some opposing edge. That opposing edge may belong to a different tile from the initial one. Its crossing supplies the cap endpoint, and the cap supplies the next actual b-edge. At the terminal external side, the supporting-line condition makes both chains whole; this is where the arithmetic contradiction occurs.

## 3. Dependency order in W

There is a precise way to read the nested induction that avoids circular completion:

1. Assume the actual standard front `K_m` and the completed properties of columns with indices strictly less than m.
2. Its whole opposite b-row is forced by the short-b lemma, giving `R(m,1)`.
3. To prove the property of column m, extend only when that fixed actual maximal component really has a next edge.
4. Complete the next row by the two fan alternatives above. The diagonal lemma at j uses horizontal caps of indices j−1,j−2,...,0, so every column-completion property it invokes has an index less than j and hence less than or equal to m−1.
5. At the true top endpoint, the complete normal left chain and the boundary count imply height less than u. Only now does short-c purity prove the opposing c-only property of column m.
6. Having proved that property, exclude the switched β notch and force `K_(m+1)`.

The smaller-column connection used in step 4 is not arbitrary graph connectivity. The preceding rectangle contains the actual collinear c-edges on the same q-line from the base up to the required height. The newly supplied c-edge attaches to that chain. This is sufficient to identify it with the previously considered maximal component.

The first column has a separate argument, so the induction does not assume its own base case. The altitude bound forces c on its entire strip side; boundary-distance integrality then eliminates the reflected orientation. At its top external boundary junction, the α+γ already present leave β, which requires one additional c-edge. That gives the strict height bound needed for its first no-right-a property.

## 4. Reverse-apex audit with arbitrary opposing traces

The target apex has precisely three α tiles. Its outer incident edges are c because the equal target sides have no b-edges. The two internal seams are therefore one b/b seam and one b/c seam; reflection can place the latter next to the selected outer tile. No comparison between the full apex angle 3α and γ is required.

For `m<v`, the actual diagonal b-chain from the apex to `V_m` has an opposite chain starting with c. Whole-edge purity prevents a common endpoint at `V_m`, so that point lies inside an opposing edge. Extending the q-ray upward enters that tile, making `V_m` the true upper endpoint of the q-component being studied.

The horizontal cap uses an already supplied segment of exactly m a-edges, with an external supporting line at one end and that transverse interior at the other. Its opposite chain is a-only by length purity. Its normal orientation is fixed first at the crossing endpoint, where the remaining sector is α+β<γ, then successively along the row, where a reversal would put two γ angles in the same half-plane. These are local half-plane contradictions, unlike the invalid use of `2γ>π` at a completely unconstrained interior point.

For downward continuation at `Z(m,t)`, the old left tiles leave exactly a β sector between the negative horizontal ray and the downward q-ray. If this β tile takes a on q, then its horizontal edge is c, producing a whole horizontal chain of length ma containing c. The segment starts at an actual tile endpoint and ends on an external supporting side, so the short-a contradiction is legitimate. Thus the q-edge is c, and a whole normal row follows.

When that row supplies a new c-edge in an earlier column i<m, the existing truncated region supplies a collinear c-chain upward to `V_i`. This identifies the new edge with the already completed maximal component `M_i`. If it extended past a previously identified endpoint, it would contradict the assumed tiling and the earlier maximality conclusion. It would not invalidate the earlier conclusion or create an unrelated component.

For the current component, every real continuation adds one full c-edge. Boundedness terminates the process at an integer grid height r≥0. Its length is `(v−m−r)c`, with multiplier less than v. Short-c arithmetic in this range excludes b but does not exclude a; the proof uses exactly that weaker conclusion. It never assumes c-only purity up to height v, which would be false because `uc=va`.

At m=v−1 the initialized component reaches height zero. Completion gives `T(v−1,0)`, and the final α tile gives `D(v−1,0)`, hence all of `K_v`. No short-b lemma is used at the prohibited index v. Removing `K_v` removes whole actual tiles and leaves the stated W triangle; it does not cut tiles along an assumed grid line.

## 5. Lemma 55 versus the prime deduction

The current Theorem 22 argument uses:

- rationality and primitive normalization;
- the area equation and the valid theta coloring equation;
- Lemma 54's boundary congruence;
- one mandatory c-edge on the base;
- arithmetic specific to prime N.

It does not use Lemma 55, integer µ, or the retracted beta coloring divisibility. Lemma 54 follows from integer boundary lengths, `gcd(b,v)=1`, and the coloring equation; its proof does not use Lemma 55 either. The new counterexamples to Lemma 55 therefore do not automatically propagate to Theorem 22.

The theta prime row can in any case be replaced by the following shorter proof that does not use a coloring number. Assume squarefree N. The theta area identity gives `X²=N b v²`, hence

$$
b=Nh^2,\qquad X=Nvh
$$

for a positive integer h. The single α tile at the target apex forces a b-edge on one equal side. That side's b-edge count is divisible by v, hence at least v, by reducing its whole-edge length equation modulo v. It also contains at least one c-edge by the obtuse-endpoint pigeonhole principle. Therefore

$$
X\ge vb+c=Nvh^2+v^2>Nvh=X,
$$

a contradiction. This excludes all squarefree N in that branch, including every prime, using only rationality, area, the apex inventory and one elementary boundary congruence.

The general two-c-edge Lemma 8 is likewise unnecessary for either new scale-one proof and unnecessary for this replacement. Thus its separately identified delicate intermediate step is not silently imported here.

## 6. Exact scope of this pass

No geometric inference required correction during this pass. The main expository improvement would be to promote the local seam lemma of Section 1 to a named lemma and explicitly label the two nested induction orders. This makes the delicate endpoint and dependency arguments inspectable without assuming that the reader has reconstructed them from the surrounding prose.

I did not find a tiling of a forbidden scale-one target, nor a local configuration satisfying the actual hypotheses and violating the asserted continuation. This is evidence from mathematical analysis, not a finite exhaustive proof over arbitrary tilings. The published source classification and rationality inputs remain substantive outside dependencies.

During the same audit session, a separate exact replay verified the new theta 75-tiling. That result closes a different fixed-tile existence question and provides another counterexample to Lemma 55; it neither verifies nor contradicts the W/beta scale-one nonexistence arguments. Its exact replay record is `verification/theta-odd.json`.
