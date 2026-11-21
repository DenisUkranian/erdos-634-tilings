# Independent mathematical audit of the contact-inertia theorem

21 November 2026. This review checks the proposed exact identities and
inequalities, including the strengthening in
[`JOINT_CONTACT_GRAPH.md`](JOINT_CONTACT_GRAPH.md). It is an internal
mathematical review, not external peer review or Lean verification.

## Findings

**The cut determinant identity is valid.** A CCW triangle centroid
splits its area into three equal parts, so each side satisfies
`det(u-o,v-o)=det(g-o,v-u)+2Delta/3`. Each selected exterior side
has determinant `2N Delta/3` about the board centroid. Thus
`F_e=3n_e-Nw_e-(U_e-V_e)` has exactly the stated signs and factor.
The population `n_e` must include matched tiles. Cancellation of
their long-edge chains does not remove their area from the subtree.

**The two crossing classes are disjoint within one tree.** Every tile
has one short node and one adjacent long-edge node, hence it is
assigned exactly one tree edge. A whole half-turn mate has the same
two nodes and opposite CCW long vector. Both members cancel in the
same crossing class. Unmatched tiles partition by the tree edges;
therefore their counts sum to `M`, or to at most `M` for selected cuts.

**The centroid and matching constants are correct.** The triangle
covariance is one thirty-sixth of the sum of the three edge outer
products. Its trace gives `N(S_B-S_T)/36`. The squared offset of a
centroid from its long-edge midpoint is
`(a^2+b^2-ab)/36`. A pair contributes two such offsets; with
`(N-M)/2` pairs, the removed reserve is exactly `(N-M)D/36`.
Replacing each pair by two copies of its midpoint preserves the
zero total centroid sum and every cut row.

**The two-tree Laplacian counts each tile once.** For hand `s`, the
increasing-tree bank sign is `-s` and the decreasing-tree sign is
`s`. The same long vector occurs in both rows. Thus every unmatched
tile supplies opposite vector coefficients at its two graph vertices.
Their squared Gram contribution is `c^2` times the two-vertex edge
Laplacian. Summing gives `c^2 L_H`. No assumption about disjoint
tile populations from the two trees is made.

**The scalar flow has the claimed divergence and energy.** In axial
coordinates its value is
`f_t=(3/(ab))*tau_+(t)*det_axial(g_t-o,v_t)`.
Equation (2) in the main note gives its divergence `F`. The Euclidean
determinant is `sqrt(3)/2` times the axial determinant; inserting this
factor gives
`sum f_t^2 <= c^2[N(S_B-S_T)-(N-M)D]/(3a^2b^2)`, precisely `K_M`.
The graph energy bound and every graph-cut bound then follow by
ordinary Cauchy--Schwarz or the minimum-energy flow identity.

**The active-band connectedness lemma is valid.** At band `k`, the
two sides of the population partition use the increasing-tree
ancestor of a tile at height `h>=k` and the decreasing-tree ancestor
of a tile at height `h<=k-1`. These disjoint alternatives count every
tile exactly once. Board-side direction heights give the analogous
partition of the three exterior sides, with multiplicity two at
the height-zero core. Summing cut chains over a graph component
cancels each unmatched long side between its two vertices; matched
pairs already cancel in each row. The resulting union has boundary
equal to a subset of the triangle's whole sides. Vector closure
forces that subset to be empty or full, and area then gives zero or
all `N` tiles. A component with a graph edge contains the tile at
one of its short-node endpoints, so cannot have zero population.
Consequently there is one active component. Isolated vertices obey
the same zero-or-full alternative; the full alternative is incompatible
with an active edge elsewhere because every tile has exactly one
owner in the partition. Thus isolated vertices in an active band are
empty and have no exterior sides. Paired-only crossings are included
in the populations but correctly omitted from the graph.

**Both charge flows and their parity constraints are valid.** The
two edge values `tau_+ epsilon` and `epsilon` are each `+1` or `-1`.
Their divergences are respectively `P-Q` on both parts, and `P+Q`
with opposite part signs. On one band the root parities are `k`
and `k-1`, so summing the transport equations gives exactly the
two integers in (10g). Every crossing edge contributes one sign to
each cut sum. Therefore both absolute values are at most the number
of cut edges and both have that number's parity. The populations
and charges can be summed in this statement because the band
partition, rather than two arbitrary tree levels, is being used.

**The global charge-energy bounds are valid.** Each of the two unit
flows has exactly `M` edges and every squared edge value is one, so
its energy is `M`. A flow with divergence `alpha` or `beta` is an
admissible competitor for the grounded Laplacian minimum; hence
`alpha^T L_H^dagger alpha<=M` and
`beta^T L_H^dagger beta<=M`. For their linear combination, the
edgewise product is exactly `q_t q'_t=tau_+(t)`, because
`epsilon(t)^2=1`. Therefore the energy of `u q+v q'` is
`M(u^2+v^2)+2uv sum_t tau_+(t)`, giving (10f.2) with no extra
hypothesis. Componentwise zero sums follow from the actual flows;
they must not be omitted when testing a proposed abstract demand.

**The rank-two correction is valid.** Centering the vector row
coefficients over all `N` tiles subtracts
`|sum lambda_e W_e|^2/N` from their squared norm. Its scalar product
with the reduced centroids is unchanged. The removed pair offsets
are orthogonal to the centered coefficients because each pair has
the same coefficient on its two tile positions. In particular one
must center over all `N` tiles, including paired ones, rather than
silently replacing `N` by `M`.

**The scalar charge-demand elimination is valid.** With fixed
`m=U+V`, the range permitted by `U>=p,V>=q` is
`U-V in [2p-m,m-2q]`. The distance of `A=3n-Nw` from this interval
is `(p+q+|A-p+q|-m)_+`. In an exterior-free subtree `n>=|P|`, so
its demand simplifies to `3n+2|Q|`. This demand is not itself a
lower bound on the number of contacts; it enters the quadratic
energy inequality. Treating it as a direct contact count would
be an error.

## Limits that must remain explicit

The graph requires the incidence of actual unmatched physical tiles,
not just the separate cut degrees or aggregate charge inventories.
If a finite optimization replaces it by possible graph variables,
the resulting feasible graph is only a necessary projection.

The board-scale inertia budget is substantial. No claim that this
theorem excludes every possible joint graph at 3431 or 5063 has been
verified here. It applies to all odd populations and arbitrary phase
branches, but that generality does not by itself close the two counts.

The trace form retains the exact paired reserve but loses directional
information. The tensor version is valid with the actual orientation
covariances and can be stronger; replacing those matrices by guessed
isotropic values would need a separate proof.
