# Adversarial review of the prime-count candidate

29 September 2026. This is a further internal review of a proposed proof, not external refereeing, a formal proof certificate, or a priority determination.

## Outcome and limits

I found no concrete mathematical gap or counterexample in the two scale-one arguments as currently written. I specifically reconstructed the whole-edge endpoint argument, both column inductions, their use of earlier maximal components, the reverse-apex terminal step, and the elementary arithmetic in the global prime deduction. The checks below explain that conclusion; they do not turn the manuscript into a peer-reviewed result.

The appropriate public description remains **a candidate proof of the prime-count classification, with explicit proofs and internal audits**. The proposed statement is

$$
p\text{ prime admits some triangle tiled by }p\text{ congruent triangles}
\quad\Longleftrightarrow\quad
p=2,\ p=3,\ \text{or }p\equiv1\pmod4.
$$

The complete classification for arbitrary composite counts is not obtained. The separate construction of 322 tiles has a different evidentiary basis: explicit coordinates that can be replayed mechanically. A replay of that construction does not verify either nonexistence proof.

## Material examined

- `Erdos634_beta_scale_one_proof_2026-09-29.md`, including its full W appendix.
- `output/pdf/Erdos634_scale_one_note_for_Beeson_2026-09-29.tex`.
- `docs/prime-case-dependencies.md`.
- `docs/audits/geometric-review.md` and the earlier branch audit underlying `docs/isosceles-120-invariant.md`, read as previous internal analyses rather than authorities establishing correctness.
- The local text of Beeson, `1206.2229v4`, specifically its rationality statement, primitive parametrization, corrected W equation, and Theorems 16, 19, 22 and 26.

An attempted fresh web retrieval of the other cited arXiv documents failed with the retrieval service's `DisabledError`. Consequently this review does not claim to have freshly audited the original proofs of Laczkovich's complete classification, the reptiling theorem, or all the external rationality results. Those remain explicitly identified literature inputs in the prime-count argument.

## 1. The endpoint principle really permits T-junctions

The essential object is a component of actual collinear whole tile edges in one fixed hypothetical finite tiling. It is not an arbitrarily drawn line continued through tiles.

At a point in the interior of an existing edge, the tile on that side supplies a straight angle. On the other side, the boundary trace must therefore remain on the same line. If an opposing edge ends there, another opposing edge must continue. At a junction between two supplied collinear edges, an opposing tile cannot straddle the line: it would overlap the open interior adjacent to one of the supplied edges. These observations give opposing edge coverage of every supplied segment.

For a maximal collinear component, an endpoint cannot occur in the relative interior of any participating edge, because that edge would extend the component. Thus both side chains consist of whole edges from endpoint to endpoint. For the horizontal subsegments used in the proof, maximality is replaced by two explicit endpoint facts: a supporting line prevents overrun at the outer end, and an actual starting tile edge or a transverse tile interior fixes the inner end. These are sufficient; edge-to-edge tiling is never needed.

A tile vertex on a supporting side of the target is also a genuine boundary junction. It cannot lie in the relative interior of another boundary tile edge: both tiles would then have positive-area interior on the same side of that edge near the point. This justifies the integral boundary distance used to reject the reflected first-column tile in W.

## 2. Arithmetic checked independently

For `a=uv`, `b=v²−u²`, `c=v²`, with `gcd(u,v)=1` and `0<u<v`:

1. A whole-edge decomposition of `ib` with `i<v` is `i` copies of `b`. Indeed the number of b-edges is congruent to i modulo v and is at most i.
2. A whole-edge decomposition of `ia` with `i<v` is `i` copies of `a`. Writing the b-count as `vℓ`, the length identity becomes `i=A+Tv−ℓu` with `Tu=ℓv+C`. If either ℓ or C is positive, then `T≥ℓ+1`, giving `i≥v`.
3. A whole-edge decomposition of `nc` with `n<v` has no b-edge. With `d=v−u`, the identities are `A=vh−dℓ` and `n=C+uh+dℓ`. If `ℓ>0`, nonnegativity forces `h≥1` and hence `n≥v`. If also `n<u`, then `h=0`, so the decomposition is c-only.

The last distinction is respected in the two proofs: the W argument uses c-only purity only below u; the reverse-apex argument uses the larger no-b range below v. Replacing the latter by c-only purity would be false, since `uc=va`.

I also checked the W side counts `(0,u,u)`, the equal-side exclusion of b-edges in the isosceles target, and the irrational-angle inventories used for the α, β, α+β and 3α sectors.

## 3. W induction: dependency order and the suspected circularity

The first column is established without later columns. Its strip width is the altitude to c, whereas the altitudes to a and b are larger. Every tile edge on the strip side is therefore c. Its reflected third-vertex position has boundary distance

$$
iv^2+\frac{u^2(3v^2-u^2)}{v^2},
$$

which is nonintegral because `gcd(u,v)=1`. Thus the actual strip tiles have the normal orientation. Their intervening one-tile-area regions are bounded by actual edges and the external side and must be the standard D tiles. The boundary angle at the upper end requires another c-edge, forcing column height `n<u`. This yields its c-only opposing chain.

For column m, the induction assumes only the completed properties of columns with smaller indices. The diagonal obstruction at index j uses horizontal caps whose indices strictly decrease from `j−1` to zero. At every cap, the newly forced c-edge is attached to a smaller column already connected to the base by an actual rectangle. Its established completion property supplies the next required rectangle. There is no appeal to the property currently being proved for column j.

In the top-row sweep, the residual sector is exactly α+β. In order α,β, the β tile places an a- or c-edge on the forbidden diagonal. In order β,α, the common ray is the actual q-direction: the earlier column's no-right-a property fixes the right tile, and its known c-only left side fixes the left tile. At the outer endpoint, choosing b on q produces the same forbidden diagonal; choosing c gives the next normal U. Thus every actual continuation adds an entire standard row.

The component is finite, so this continuation process reaches its genuine endpoint. Only then is the short-c arithmetic applied to obtain its opposite-side property. That order is important and is the order used in the manuscript.

Finally, the front induction can be organized explicitly as:

1. Have the actual front `K_m` and the completed properties of columns `<m`.
2. Use `K_m` and its forced opposite b-row to initialize `R(m,1)`.
3. Complete column m by the preceding induction, using only columns `<m`.
4. Exclude every switched β notch and obtain `K_(m+1)`.

This is a valid nested induction. The front endpoints remain strictly inside the outer sides for all `m≤u`, so the b-chord is internal throughout the needed range. The final `K_(u+1)` contradicts the exact boundary c-count u.

## 4. Reverse-apex induction: whole components, not assumed extension

The apex inventory is exactly three α sectors, even in the parameter regime where `3α>γ`. The equal sides have no b-edges, so both outer apex edges are c. Consequently the two internal seams are one b/b seam and one b/c seam. Reflection selects the latter next to the first outer tile.

For every `m<v`, the actual diagonal chain of m b-edges has an opposite chain starting with a c-edge. Short-b purity prevents a common endpoint at `V_m`. Thus `V_m` lies inside an actual opposing edge, and the positive q-ray enters that tile. This fixes the upper endpoint of the downward component `M_m`.

The reverse horizontal cap is a complete segment of length `ma` with `m<v`. Its opposite chain is therefore a-only. At its inner endpoint, the old D tile and the transverse straight sector leave α+β; since γ is larger, the first opposite a-tile has β there. All subsequent a-tiles have the normal orientation because a reversal would place two γ sectors in one half-plane.

For a downward continuation at `Z(m,t)`, the left residual sector is exactly β. If the β tile takes a on the downward q-ray, its horizontal side is c; the full horizontal lower chain would then decompose `ma` using c, contradicting short-a purity. Hence the downward edge is c, forcing the standard row.

At an inner grid point in that row, the new U-edge is collinear and connected, through existing U-edges, to the same previously studied maximal component `M_i` with `i<m`. Its no-opposite-b property therefore applies. The phrase “previously studied” does not mean the component was truncated: it was the entire maximal component in the fixed tiling. If the newly forced edge were to extend past its already identified endpoint, the hypothetical tiling would be inconsistent. It does not produce a new component to which the earlier proof fails to apply.

Every real continuation adds a whole c-edge. The bottom endpoint has an integer grid height `r≥0`, so the total length is `(v−m−r)c`, with positive multiplier less than v. Only now is the no-b conclusion established for this whole component. The following diagonal step uses that conclusion to force `D(m,v−m−1)`.

The last step has `m=v−1`: initialization already reaches height zero, the completion property gives `T(v−1,0)`, and the new D gives `K_v`. No short-b argument is used at index v. Since `K_v` consists of actual whole tiles, removing it leaves an actual tiling of the complementary W triangle. This completes the claimed reduction without a geometric cut through tiles.

## 5. Prime reduction and additional independent checks

Once rationality and the two target shapes are known, the integer scale reduction can be checked directly rather than relying only on the printed coloring equations. The normalized W side triple is

$$
(v^3,u(2v^2-u^2),v(v^2-u^2)),
$$

and the β-isosceles side triple is

$$
(v^3,v^3,u(3v^2-u^2)).
$$

Each triple has gcd 1: already `gcd(v³,u(2v²−u²))=1` and `gcd(v³,u(3v²−u²))=1`. All actual target sides are integer sums of primitive tile lengths. Bézout therefore makes the similarity scale an integer j. The area counts are `j²(2v²−u²)` and `j²(3v²−u²)`, and primality forces `j=1`. The two proposed geometric exclusions have exactly the required normalization.

The equilateral 60° factorization was independently checked: if `y²=(9p−M²)(p−M²)` and `0<M²<p`, then `(5p−M²−y)(5p−M²+y)=16p²`. The two positive factors cannot both be divisible by p. One contains p², so their sum exceeds p² but is less than 10p, excluding `p≥11`. The four discriminants for p=5 and p=7 are not squares.

For the non-equilateral isosceles 120° row, the character on directions `jπ/3+ℓα` given by `(-1)^j` is well-defined and changes sign on reversal. Positive-length adjacency propagates the direction group through a connected tiling; subdivision at T-junctions preserves signed length and cancels interior subsegments. A counterclockwise tile boundary has weight `±(c+a−b)` and the target has weight `k(a+2b−2c)`. When primality gives `b=k²`, their ratio is `(c−a−b)/k`. The divisibility and final contradiction in the global audit follow. This calculation does not assume edge-to-edge tiling.

For the four non-isosceles 120° rows, the primitive target triples and the displayed factorizations give composite counts. In the exceptional-looking quotient row, `N=λ²(a+b)/b`, coprimality gives `b|λ²`; and `a+b` cannot be prime because `c²=a²+ab+b²` modulo `a+b` would force `c=a+b−a=b`, contradicting `c>b`.

The elementary existence constructions for p=2, p=3 and `p=m²+n²` were also checked. In the last case, the altitude partitions the larger right triangle into m- and n-scaled copies of the tile, with standard subdivisions contributing m²+n² tiles.

## Publication recommendation

Publish the statements, complete geometric arguments, exact construction certificates, and this audit with their distinct status labels. Avoid “the full problem is solved,” “formally verified,” or “independently peer reviewed.” A mathematically precise claim suitable for a research repository is:

> This repository presents a candidate proof of the prime-count classification in Erdős problem 634. Its two new geometric obstructions have undergone internal adversarial review. The global deduction uses the versioned classification results listed in the accompanying audit. The general composite-count classification remains open in this work.

No change to a geometric inference was required by this review. The direct Bézout scale reduction above is a useful simplification for a public version; it reduces reliance on a source-specific coloring parametrization without replacing the required rationality and shape-classification inputs.
