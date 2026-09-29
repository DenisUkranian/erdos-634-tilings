# Adversarial independent audit of the 322-tile construction

**Verdict: PASS. No mathematical or certificate flaw found.**

Audit date: 29 September 2026. This is an internal independent audit, not a claim of external refereeing or publication priority. The certificate is a valid tiling of a triangle with side lengths **81, 115, 126** by **322 congruent triangles with side lengths 5, 6, 9**. The proposed gluing also works for every stated primitive parameter pair, and indeed does not require coprimality for sufficiency.

## Independent certificate replay

The replay in `scripts/verify_322.py` reads the JSON as data. It does **not** import the generator, call its verifier, or use its separating-axis test. It fixes the claimed instance independently: tile sides 5,6,9, target sides 81,115,126, and coordinate map `(X,Y) -> (X/18, Y*sqrt(32)/18)`.

The audited JSON SHA-256 is:

`4b18e031bfa3e3df62ebe71a4a9f90eb83d0843e39c856b42fd74bb40f53c3bc`

Exact integer checks establish:

- There are exactly 322 nondegenerate positively oriented triangles.
- Every tile's three squared physical edge lengths are exactly 25,36,81.
- The outer triangle's squared edge lengths are exactly 6561,13225,15876.
- Every tile vertex lies in all three closed target halfplanes. Convexity then puts every entire tile inside the target.
- Each tile has area `10*sqrt(2)` and the outer triangle has area `3220*sqrt(2)`.

For **all 51,681 unordered tile pairs**, a separate exact rational polygon-clipping algorithm computes their intersection. All intersections have area zero. This is a different geometric decision method from the supplied verifier and uses neither floating point nor a tolerance. It finds 1,715 pairs with nonempty zero-area contact, and zero pairs with positive-area intersection.

An additional independent edge-chain check splits each tile edge at every certificate vertex lying on it. Every resulting interior atomic segment occurs exactly twice in opposite directions. Every outer atomic segment occurs exactly once in the target's boundary direction. Results: 195 vertices, 474 interior atomic edges, 42 boundary atomic edges, and **24 distinct T-junction vertices**. Thus the audit explicitly permits and checks the non-edge-to-edge joins; it does not incorrectly assume matching whole edges.

Containment, pairwise interior disjointness, and equality of total area prove coverage. A finite union of closed triangles is closed; a missing target interior point would leave a relatively open positive-area hole. The atomic-boundary check additionally verifies all boundary seams directly.

The machine-readable results are in `verification/322-original-replay.json`.

## Audit of the supplied finite verifier

The supplied verifier is also sound for this use.

1. It first checks positive orientation, so every triangle occupies the left closed halfplane of each of its three directed edges.
2. Its nonoverlap predicate ranges over **all three edges of both triangles**, six candidate supporting lines in total. When all vertices of the other triangle are on the right closed halfplane of one such edge, the interiors are disjoint. The weak inequality correctly permits contact.
3. Its preliminary coordinate bounding-box rejection uses weak inequalities. Two boxes touching only on a line cannot have a positive-area intersection, so this shortcut is safe.
4. Coordinates are Python integers after denominator clearing; the computations have no fixed-width overflow or floating-point error.
5. The metric rescales the second coordinate by a positive constant. This affine transformation preserves incidence, orientation, containment, and disjointness. Ordinary coordinate halfplane tests are therefore valid; inserting the metric coefficient into these determinants would be unnecessary.

Even interpreted merely as sufficient separation witnesses, rather than invoking completeness of polygon SAT, the successful checks prove the claimed pairwise disjointness. The independent clipping replay removes any dependence on the author's separation implementation.

## All-parameter mathematical audit

Write

`a=uv`, `b=v^2-u^2`, `c=v^2`, `J=u^2`, `Q=b+c`, `P=b+2c`,

where `0<u<v`. Then `J=c-b` and `a^2=cJ`.

### Short proof from Beeson Theorem 11

Beeson arXiv:1206.2229v4, Theorem 11, states the following sufficient construction: if `M^2+N_W=2K^2`, `M^2<N_W`, and `K|N_W`, there is an `N_W`-tiling with tile sides `(M,N_W/K-K,K)` and outer sides `(MN_W/K,N_W-K^2,K^2)`, with angles `(2alpha,beta,alpha+beta)`.

Use `M=a`, `K=c`, `N_W=cQ`. All hypotheses hold:

`a^2+cQ=c(c-b)+c(b+c)=2c^2`,

`cQ-a^2=2bc>0`, and `c|cQ`.

The tile is precisely `(a,b,c)`. Label the resulting triangle `ABC` with

`AB=c^2`, `AC=bc`, `BC=aQ`,

and angles at `A,B,C` equal to `2alpha,beta,theta`, where `theta=alpha+beta`.

Take the integer-scale-`Q` copy of the tile, subdivided into `Q^2` original tiles. Glue its side of length `aQ` onto `BC`, placing its interior in the opposite halfplane. Match its beta endpoint to `B` and its gamma endpoint to `C`; call its other vertex `H`.

At `C`, `theta+gamma=pi`; at `B`, `beta+beta=2beta<pi`. Consequently `A,C,H` are collinear with `C` between `A,H`, and the union is the single convex triangle `ABH`. Its side lengths are

`AB=c^2`, `BH=cQ`, `AH=bc+bQ=bP`.

Its tile count is

`cQ+Q^2=Q(c+Q)=QP`.

The two large triangles occupy opposite halfplanes of the complete shared side. Therefore gluing introduces neither overlap nor gap. Boundary subdivisions on the seam may differ: T-junctions do not invalidate a tiling. Standard quadratic refinement of every tile yields `k^2 QP` tiles for each positive integer `k`.

For `u=2,v=3`, this is the 126-tile triangle with sides 81,45,84 plus the 196-tile triangle with sides 126,70,84, glued along 84. The outer sides are 81,115,126, and the count is 322.

### Direct check of the generator's geometry

The code need not rely on Theorem 11 as a black box. In complex physical coordinates put

`z=exp(i gamma)=-u/(2v)+i*sqrt(4v^2-u^2)/(2v)`.

Then `pi/2<gamma<2pi/3`, `|z|=1`, and `z+conj(z)=-a/c`. The generator's points are

`O=0`, `A=b^2`, `C=abz`, `D=ab*conj(z)`, `E=a^2 z^2`, `B=D+E`,

`H=C+(Q/c)(C-A)`.

The identities `z^2+(a/c)z+1=0` and `a^2=c(c-b)` give

`D=A+(b/c)(B-A)`,

`E=C+(c/Q)(B-C)`.

Both ratios lie strictly between zero and one. Thus `D` lies on `AB` and `E` lies on `CB`. Also `O` is strictly inside `ACB`: the edge determinants `det(A,C)`, `det(C,B)`, and `det(B,A)` are positive. For the only less immediate one,

`det(C,B)=-a^2 b^2 sin(2gamma)+a^3 b sin(gamma)>0`.

The ordered boundary `A,C,E,B,D` and the interior point `O` therefore partition the W triangle into the three code triangles `OAC`, `ODA`, `OCE`, and the parallelogram `O,E,B,D`.

The triangle side triples are respectively `b*(b,a,c)`, `b*(b,a,c)`, and `a*(b,a,c)`, so the `b`, `b`, and `a` quadratic subdivisions produce congruent original tiles.

The parallelogram steps are `d=D/b=a*conj(z)` and `e=E/J=c*z^2`. They have lengths `a,c`, while

`|d-e|^2=a^2+c^2-2ac cos(3gamma)=(c-a^2/c)^2=b^2`.

Consequently each `d,e` cell is exactly two original tiles, and the `b` by `J` cell grid gives `2bJ` tiles. Its side vectors sum to `D,E`, so it fills the entire parallelogram without a scale mismatch.

Finally `H` is beyond `C` on `AC`, the code triangle `BCH` has sides `aQ,bQ,cQ`, and it is on the opposite side of `BC` from `A`. The code's four quadratic grids and parallelogram grid thus implement the above gluing exactly. Their count is

`2b^2+a^2+2bJ+Q^2=cQ+Q^2=QP`.

The grid loop is the standard triangular lattice subdivision: `n(n+1)/2` upright cells and `n(n-1)/2` inverted cells, hence exactly `n^2`, covering the macro triangle.

## The historical discrepancy

The discrepancy is real: the same v4 text explicitly says after Theorem 14 that the `(6,5,9)` instance with `N=322` was not known, and Table 3 similarly lists 322 and 897 as unresolved minimal counts. That is a statement about the state of that source, not a mathematical prohibition. The exact replay and the elementary glue both pass despite it.

Theorem 11's prose calls the small parallelogram angle `gamma`; the actual `a,c` two-tile brick used in this construction has the appropriate acute included angle `beta`. The direct vector calculation above verifies the actual brick and avoids inheriting that local angle-label error.

This audit establishes the construction and its refinements. It does not by itself audit necessity of the complete `k^2QP` spectrum, other target-shape branches, global classification, or publication priority.
