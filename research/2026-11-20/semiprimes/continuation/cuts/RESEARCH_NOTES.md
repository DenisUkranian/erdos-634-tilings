# Other tests on the two unit boards

## The 624-tile triangle

For the (35,13,43) tile the smaller target that can contain all 27 small certificate members has vertices $0,455,624\rho$. Testing only two consecutive short-edge heights gives the following results. The counts concern placements of single tiles.

| Heights | Candidates inside the target | After endpoint support | After collinear interval support and matching equal-length intervals on uniform lines |
|---|---:|---:|---:|
| $[-1,0]$ | 120,242,057 | 5,450,803 | 5,242,940 |
| $[0,1]$ | 119,919,047 | 3,826,933 | 3,606,477 |

The endpoint test translates the 24 possible oriented templates in each band, using $z=(6+\rho)/(7-\rho)$ and $\rho=e^{i\pi/3}$. It repeatedly removes a placement with an unsupported signed endpoint. The next test asks whether the union of oppositely oriented candidates covers the full length of each candidate edge. On lines where all surviving tile edges have equal length it also matches the whole equal-length intervals. No extra phase filter was applied. Neither band reached a contradiction. The surviving candidates overlap and their counts give no construction. Extra heights remain possible. These experimental counts are separate from the two certified whole-board lower bounds.

## A limitation on direction-only group obstructions

There is a short reason to set aside a class of proposed invariants on the unrestricted scale-one triangles. Assign a group element to a directed unit step as a function only of its direction, with the inverse assigned to the reverse step. Suppose tileability implies that the product along the outer boundary is the identity. For any fixed triangle with integral side lengths, let $X,Y,Z$ be the words for its three whole sides at scale one.

If the triangle tiles with the same unit tile at three consecutive positive integer scales $n,n+1,n+2$, then $XYZ=1$ in **any** such group, allowing noncommutative groups. Put $W=Z^{-1}$. The three identities give $X^mY^m=W^m$. Comparing two consecutive exponents gives $W=Y^{-m}XY^{m+1}$. Comparing this last identity at $m=n$ and $m=n+1$ shows $XY=YX$, whence $W=XY$. Thus a direction-only boundary word of this kind cannot refute scale one on either original F2 triangle. Zhang's Theorem 7 gives every sufficiently large integer scale for the same tile and target shape. A method that also uses positions or containment lies outside the argument. [Yan X Zhang, Section 4, Theorem 7](https://arxiv.org/pdf/2512.22696).
