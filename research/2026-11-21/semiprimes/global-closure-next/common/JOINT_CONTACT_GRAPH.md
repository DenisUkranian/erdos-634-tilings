# A joint contact graph for the two prime trees

21 November 2026. A global charge--contact--inertia theorem. The result is a necessary condition
for a genuine complete tiling. It does not assert nonexistence of the
3431 or 5063 tiling.

The stronger form below couples **both** prime trees at one physical
tile budget. It does not add two population bounds for the same tiles.
Its graph has one edge per actual unmatched tile.

The geometric inputs are the established exact phase-tree, integer-offset,
and cut-chain framework for the two target tiles `(33,7,37)` and
`(35,13,43)`. The positive control is `(5,3,7)`. Their denominators
`37,43,7` are split primes in the Eisenstein ring. The proof below
works for any tiling supplied with this two-tree framework and its
adjacent short/long-node assignment; it does not assert, without a
separate reduction, that every composite denominator has only two
such phase trees.

The geometric dependencies are the existing
[phase-node framework](../../../../2026-11-20/semiprimes/continuation/phase-height/PHASE_BRANCHES.md),
[signed population identities](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md),
and [exact signed, vector, area, and chain transport](../../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md).
The no-supported-pure-cycle theorem is not used as an extra premise
in the new graph and moment derivations below.

## 1. Definitions and exact cut identities

Use the standard board with vertices `0,A,B rho`, where

\[
 A=b(2a+b),\qquad B=a(a+2b),\qquad
 c^2=a^2+ab+b^2,\qquad
 N=(a+2b)(2a+b).
\]

The tile area is `Delta=ab sqrt(3)/4`. All centroids below are measured
relative to the centroid `o` of the board. The established two prime
trees assign every tile one exact short node and one adjacent exact
long-edge node. Children increase physical height in the first tree
and decrease physical height in the second.

Cancel every actual whole-long-edge half-turn pair, without removing
the tiles from the tiling or changing any subtree population. Let `M`
be the number of remaining, unmatched, tiles. The paired tiles number
`N-M`.

For a tree edge `e`, let `S_e` be its child subtree, and define:

* `n_e`: the full number of tiles whose short nodes are in `S_e`;
* `w_e`: the number of board sides whose edge nodes belong to `S_e`;
* `U_e,V_e`: the numbers of unmatched root-to-parent and
  parent-to-root crossing tiles;
* `P_e,Q_e`: the corresponding signed crossing counts;
* `W_e`: the sum of CCW long-edge vectors of the first crossing class
  minus the sum of those of the second.

In the usual notation, `w_e=2 delta_0+delta_2`. The crossing chains
give `W_e=-V_exterior,e`, where `V_exterior,e` is the vector sum of
the selected, CCW oriented board sides. A board side either belongs
to the subtree as a whole edge-node contribution or does not.

Put

\[
 F_e=3n_e-Nw_e-(U_e-V_e).                         \tag{1}
\]

For the actual CCW long vector `v_t` of a crossing tile and its
centroid `g_t`, let `tau_e(t)=+1` on the root bank and `-1` on the
parent bank. Then

\[
 \boxed{\frac{2\Delta}{3}F_e
   =\sum_{t\text{ unmatched at }e}
          \tau_e(t)\det(g_t-o,v_t).}             \tag{2}
\]

To prove this, every CCW side `u->v` of a triangle satisfies

\[
 \det(u-o,v-o)=\det(g_t-o,v-u)+2\Delta/3.
\]

The analogous determinant for every board side is `2N Delta/3`.
Insert these formulas in the established geometric cut-chain identity.
Half-turn mates have opposite directed long sides, so their endpoint
chains cancel exactly. Thus they can be canceled before this insertion;
the surviving constants are `(2Delta/3)(U_e-V_e)`. The term `n_e`
still counts all tiles, including the paired ones. This is essential.

The signed transport theorem gives the charge equations, including
the exterior character `b_e`,

\[
 c(P_e-Q_e)=(c-d)G(S_e)+b_e,\qquad
 c(-1)^{h_e}(P_e+Q_e)=(c+d)G_*(S_e)-b_e,
 \quad d=a-b.                                      \tag{3}
\]

Consequently (1)--(2) connect the actual odd and even subtree charges
to real long-side contacts and the spatial distribution of tile centroids.

Here a tile of short height `h`, direction index `j`, and hand `s`
has sign `epsilon=s(-1)^j`, and
`G(S)=sum_(t in S) epsilon(t)`,
`G_*(S)=sum_(t in S) (-1)^h(t) epsilon(t)`.
Its even and odd charges are `(G+G_*)/2` and `(G-G_*)/2`.
In this standard frame the full board has `G_odd=-c` and
`G_even=-d`. Thus the odd imbalance is fixed before a contact graph
is chosen. These signs would both reverse in the reflected path frame.

## 2. The exact centroid budget and the paired-tile reserve

For a triangle with edge vectors `d_1,d_2,d_3`, its uniform covariance
about its centroid is `sum_i d_i d_i^T/36`. Equality of the integrals
over the tiling and over the board therefore gives

\[
 \sum_t|g_t-o|^2=\frac{N}{36}(S_B-S_T),\qquad
 S_B=A^2+B^2+c^4,\quad S_T=a^2+b^2+c^2.           \tag{4}
\]

The centroids of a long-edge half-turn pair are `m+delta,m-delta`,
where `m` is the midpoint of the common side and

\[
 |\delta|^2=\frac{a^2+b^2-ab}{36}.
\]

Replace those two centroids by `m,m` and leave every unmatched
centroid unchanged. Write the resulting vectors from `o` as `x_t`.
They still have zero sum, and the exact remaining squared-norm budget is

\[
 \boxed{\sum_t x_t=0,\qquad
 \sum_t|x_t|^2=R_M
 =\frac{N(S_B-S_T)-(N-M)D}{36},\quad
 D=a^2+b^2-ab.}                                    \tag{5}
\]

Every cut row in (2) uses only unmatched tiles. Replacing paired
centroids does not change any row. The removed vectors `delta,-delta`
are orthogonal to every cut row and to the global mean. Thus the
reserve in (5) is also compatible with the centering refinement below.

## 3. One physical graph couples both prime trees

Make a bipartite multigraph `H` as follows. Its two vertex classes are
the cut edges of the two prime trees which carry at least one unmatched
tile. Each unmatched tile gives one graph edge between its assigned
cut in the first tree and its assigned cut in the second. Multiple
tiles may give parallel edges. There are exactly `M` graph edges.

For a tile of hand `s`, its bank signs are

\[
 \tau_+(t)=-s,\qquad \tau_-(t)=s.                  \tag{6}
\]

Indeed, a hand-plus tile goes from physical short height `h` to
long height `h+1`: it is on the parent bank in the increasing tree
and on the root bank in the decreasing tree. A hand-minus tile
reverses both roles. In particular the two coefficients of the same
tile in (2) are opposites.

Let `L_H` be the ordinary weighted multigraph Laplacian, with one
unit of conductance per unmatched tile. If `m_e=U_e+V_e` is the
degree at a graph vertex, its diagonal is `m_e`; an off-diagonal
entry is minus the number of shared physical tiles. The Gram matrix
of the vector-valued cut rows is **exactly** `c^2 L_H`, because
`|v_t|=c` and (6) holds.

Define the explicit budget

\[
 K_M=\frac{c^2}{3a^2b^2}
      \bigl[N(S_B-S_T)-(N-M)D\bigr].              \tag{7}
\]

**Joint contact-graph theorem.** For every real potential `lambda` on
the vertices of `H`,

\[
 \boxed{\left(\sum_e\lambda_eF_e\right)^2
 \le K_M\sum_{t\text{ unmatched}}
       (\lambda_{e_+(t)}-\lambda_{e_-(t)})^2.}    \tag{8}
\]

**Proof.** Multiply (2) by `lambda_e` and add over both trees. Each
unmatched tile appears with the one coefficient
`tau_+(t)(lambda_(e_+(t))-lambda_(e_-(t)))`. Apply Cauchy--Schwarz
to these coefficients times the rotated length-`c` vectors and to
the vectors `x_t` of (5), including zero row coefficients for paired
tiles. Division by `(2Delta/3)^2=a^2b^2/12` gives (8). No second
population or inertia budget is introduced. QED.

In particular every connected component `C` of `H` satisfies

\[
 \sum_{e\in C}F_e=0.                              \tag{9}
\]

This follows by choosing the potential to be one on `C` and zero
elsewhere. On the componentwise zero-sum subspace, (8) is equivalently

\[
 \boxed{F^T L_H^{\dagger}F\le K_M.}               \tag{10}
\]

The dagger denotes the Moore--Penrose inverse; it need not be used in
an exact implementation. Ground one vertex of each connected component,
solve its integer Laplacian system over the rationals, and evaluate
`F^T x`. Equation (9) guarantees that the resulting energy is independent
of the grounding and of the solution's additive constants.

There is also a direct flow interpretation. Orient every graph edge
from the increasing-tree cut to the decreasing-tree cut, and assign
the scalar flow

\[
 f_t=\frac{3}{2\Delta}\tau_+(t)\det(g_t-o,v_t).
                                                               \tag{10a}
\]

Its divergence is exactly `F`: equation (2) gives the increasing-tree
row, and (6) gives the decreasing-tree row. Moreover

\[
 \sum_t f_t^2\le\frac{9c^2}{4\Delta^2}
                  \sum_{t\text{ unmatched}}|g_t-o|^2\le K_M.
                                                               \tag{10b}
\]

The minimum squared energy of any real flow with this divergence is
`F^T L_H^dagger F`, so (10b) proves (10) independently of choosing
potentials. In exact axial coordinates `x+y rho`, formula (10a) is
`f_t=(3/(ab))*tau_+(t)*det_axial(g_t-o,v_t)`; the square-root factors
cancel.

For completeness, let `B_H` be the graph incidence matrix, so
`L_H=B_H B_H^T`. Solve `L_H x=F` on each grounded component.
The flow `f_0=B_H^T x` has the required divergence. Any other flow
is `f_0+w` with `B_H w=0`, so `f_0 dot w=0` and its squared norm
is `F^T x+|w|^2`. This proves the minimum-energy assertion directly.

For any set `W` of graph vertices, write `delta_H(W)` for its graph
cut, counted with multiplicity. Taking its indicator as a potential
in (8) gives the useful necessary cut bound

\[
 \boxed{\left|\sum_{e\in W}F_e\right|^2
           \le K_M\,|\delta_H(W)|.}              \tag{10c}
\]

Thus a nonzero total area demand behind a graph bottleneck forces
enough actual unmatched contacts across that bottleneck. Empty cuts
give the component balance (9). This is a cut of the joint contact
graph, not a second count of the tiles of a prime-tree subtree.

Selecting potentials supported on only one tree recovers the
single-tree inequality `sum_e F_e^2/m_e <= K_M`. The full graph may
give a strictly stronger inequality because its off-diagonal entries
retain which cuts share an actual tile. Abstract degree totals alone
do not specify these entries.

### Physical bands, disjoint populations, and connectedness

Every graph edge belongs to a unique integer band `k`: its two
endpoints are an increasing-tree cut whose child has physical height
`k` and a decreasing-tree cut whose child has physical height `k-1`.
For hand plus, the tile's short and long heights are `k-1,k`; for
hand minus they are `k,k-1`. There are no graph edges between different
bands.

At a fixed band include, temporarily, all cut vertices which contain
a tile in their child subtree, contain an exterior edge node, or are
incident to an unmatched tile of that band. This is a finite set.
Zero-degree vertices are handled below and may then be omitted.

**Band partition lemma.** These vertices partition the actual tile
population into disjoint sets: an `h>=k` tile belongs to its unique
increasing-tree ancestor subtree at height `k`, whereas an `h<=k-1`
tile belongs to its unique decreasing-tree ancestor subtree at height
`k-1`. Those alternatives exhaust the integer heights and are disjoint.
Likewise each board side belongs to exactly one vertex: use the first
tree if its direction height is at least `k`, and the second otherwise.
The two height-zero board sides are separate exterior contributions
even when they have the same phase node. Thus

\[
 \sum_{e\text{ in band }k} n_e=N,\qquad
 \sum_{e\text{ in band }k} w_e=3.                \tag{10d}
\]

This is one justified way to combine populations from the two trees:
the two selected levels are on opposite sides of the physical band.
It does not allow adding populations at arbitrary levels of both trees.

**Active-band connectedness lemma.** If a band has at least one
unmatched tile, its graph on nonzero-degree vertices is connected.
Every nonempty tile-population vertex and every exterior contribution
belongs to that one component.

**Proof.** For any graph component `C`, take the union `U_C` of
the disjoint actual tile populations in the band partition. Sum the
exact cut-chain identities of its vertices. Each unmatched crossing
tile occurs twice, with the same CCW long side and opposite bank
signs by (6), so its two terms cancel. A component has no unmatched
edge leaving it. All matched-pair crossing chains have already
canceled within their individual cut rows. Therefore

\[
 \partial U_C=\sum_{\text{board sides assigned to }C}
                     (\text{that oriented whole side}).        \tag{10e}
\]

The vector sum of a boundary is zero. In a nondegenerate triangle,
no nonempty proper subset of the three directed side vectors sums
to zero. Hence the right side of (10e) is either empty or the entire
board boundary. Taking signed area gives `n(C)=0` in the first
case and `n(C)=N` in the second. A graph component containing an
edge has positive population: the tile defining that edge belongs
to the subtree at its short-node endpoint. Such a component must
therefore have all `N` tiles and all three exterior sides. The disjoint
partition permits only one such component.

An isolated, zero-degree cut vertex satisfies the same argument on
its own. It has either `n=w=0` or `n=N,w=3`. In an active band the
second alternative is impossible: every unmatched edge has a tile
whose short-node endpoint owns that tile, so it would have to be
incident to that supposedly zero-degree vertex. Thus all isolated
vertices in an active band are empty and have no exterior contribution.
They may be deleted. If the band has no unmatched edge, exactly one
of its nonempty vertices contains the entire board and all its exterior
contributions; this inactive case supplies no contact graph. QED.

The lemma allows paired-only crossings. They produce no graph edge
and cancel as chains, but their tiles remain in the appropriate
partition population. It does not equate an omitted or unknown mate
in a search catalogue with an actual unmatched tile.

### The same graph carries the odd charge through unit-capacity flows

Orient graph edges from the increasing-tree vertex to the
decreasing-tree vertex. In addition to the area flow (10a), assign

\[
 q_t=\tau_+(t)\epsilon(t),\qquad q'_t=\epsilon(t).
                                                               \tag{10f}
\]

Both flows have magnitude exactly one on every unmatched graph edge.
The divergence of `q` at any vertex is `P_e-Q_e`. The divergence of
`q'` is `P_e+Q_e` on the increasing-tree part and `-(P_e+Q_e)` on
the decreasing-tree part. Whole half-turn pairs have opposite signs,
so canceling them preserves these signed divergences.

Define vectors on the entire joint graph by

\[
 \alpha_e=P_e-Q_e,\qquad
 \beta_e=\sigma_e(P_e+Q_e),\qquad
 \sigma_e=\begin{cases}+1,&e\text{ in the increasing tree},\\
                         -1,&e\text{ in the decreasing tree}.
          \end{cases}
\]

The two actual unit flows have respective divergences `alpha,beta`
and each has squared energy exactly `M`. The minimum-energy principle
proved after (10b) therefore gives the additional global bounds

\[
 \boxed{\alpha^T L_H^\dagger\alpha\le M\le N,\qquad
        \beta^T L_H^\dagger\beta\le M\le N.}       \tag{10f.1}
\]

Each divergence has zero sum on every connected component because
it comes from an actual flow. Its energy can thus be computed by the
same grounded rational Laplacian solver used for `F`. These bounds
connect the signed phase imbalance directly to the number of actual
contact tiles, without a board-scale inertia constant.

The two flows also retain a known correlation. Put
`T=sum_(t unmatched) tau_+(t)`, the number of hand-minus unmatched
tiles minus the number of hand-plus unmatched tiles. Since
`q_t q'_t=tau_+(t)`, for every pair of real numbers `u,v`,

\[
 \boxed{(u\alpha+v\beta)^T L_H^\dagger(u\alpha+v\beta)
          \le M(u^2+v^2)+2uvT.}                  \tag{10f.2}
\]

This follows by applying the same principle to the actual flow
`u q+v q'`; its squared energy is the displayed right side. It is a
joint necessary bound on the same physical graph, rather than a
sum of two separate population budgets.

For a subset `W` of vertices in one band `k`, the partition lemma
makes the sums `n_W,G_W,G_{*,W}` actual populations and charges of a
disjoint union of tiles. Let `b_W` be the ordinary character of its
assigned exterior sides, and let `m_boundary=|delta_H(W)|`. Summing
(3), and using opposite root-height parity on the two parts, gives

\[
 \alpha_W=\frac{(c-d)G_W+b_W}{c},\qquad
 \beta_W=(-1)^k\frac{(c+d)G_{*,W}-b_W}{c}.        \tag{10g}
\]

These are integers, the two net unit flows across the same physical
contact cut. In particular

\[
 \boxed{m_{\rm boundary}\ge
       \max(|\alpha_W|,|\beta_W|),\qquad
       m_{\rm boundary}\equiv\alpha_W\equiv\beta_W\pmod2.}
                                                               \tag{10h}
\]

Writing its even and odd charges as `E_W,O_W`, the two numerators
in (10g) are `(c-d)(E_W+O_W)+b_W` and
`(c+d)(E_W-O_W)-b_W`. This is the direct connection with the fixed
whole-board odd imbalance `-c`. The capacity in (10h), the area-flow
capacity in (10c), the Laplacian in (10), and the total budget `M<=N`
all refer to the **same unmatched physical tiles**.

These cut bounds need not be restricted to one prime-tree subtree.
They apply to every union of band-partition populations, including
unions of several charged and balanced branches from opposite trees.

## 4. A rank-two centering refinement

The zero-mean identity in (5) allows a further exact subtraction.
Let `W_e` be the vectors from Section 1. Then (8) strengthens to

\[
 \boxed{\left(\sum_e\lambda_eF_e\right)^2
 \le K_M\left[
       \lambda^T L_H\lambda-
       \frac{\left|\sum_e\lambda_eW_e\right|^2}{Nc^2}
       \right].}                                \tag{11}
\]

The bracket is nonnegative. Subtract the mean of the vector-valued
row coefficient from each of its `N` tile positions. Its squared
norm drops by `|sum lambda_e W_e|^2/N`, while its scalar product
with `x_t` stays unchanged. This proves (11). It also proves that
`L_H-(W_e dot W_f)/(Nc^2)` is positive semidefinite for every genuine
tiling. This is a Gram statement, not a guessed matrix constraint.

The same proof works for any selected collection of cuts, using the
corresponding principal submatrix and retaining all `N` tile positions
for centering. A paired-tile midpoint cannot be discarded from the
mean constraint merely because no cut row uses that tile.

## 5. Eliminating unknown bank-sign inventories in one tree

For one fixed tree let `p_e=|P_e|`, `q_e=|Q_e|`,
`A_e=3n_e-Nw_e`, and

\[
 L_e=p_e+q_e+|A_e-p_e+q_e|
     =\max(2p_e-A_e,A_e+2q_e).
\]

The actual bank counts obey `U_e>=p_e`, `V_e>=q_e`. For fixed
`m_e=U_e+V_e`, this puts `U_e-V_e` in the interval
`[2p_e-m_e,m_e-2q_e]`. Its distance from `A_e` is
`(L_e-m_e)_+`; hence the exact necessary scalar inequalities are

\[
 \sum_e\frac{(L_e-m_e)_+^2}{m_e}\le K_M,
 \qquad \sum_em_e\le M\le N.                     \tag{12}
\]

A zero denominator means its numerator must vanish. The value `M`
in `K_M` is the total number of unmatched tiles, even if only a
subset of this tree's cuts is summed.

For an exterior-free cut, `A_e=3n_e` and `n_e>=p_e`, so

\[
 L_e=3n_e+2|Q_e|.                                \tag{13}
\]

More explicitly let `R=c r` be the subtree charge at the parity of
the child height and `S=c s` the subtree charge at the other parity.
There is no exceptional core in an exterior-free subtree. From (3),

\[
 P_e=c r-d s,\qquad Q_e=d r-c s,\qquad
 n_e\ge c(|r|+|s|).
\]

Thus

\[
 \boxed{L_e=3n_e+2|d r-c s|.}                    \tag{14}
\]

For an even child height, `S` is its odd charge and (14) gives
`L_e>=5|G_odd(S_e)|`. For an odd child height, `R` is its odd charge
and it gives `L_e>=(3+2d/c)|G_odd(S_e)|`. These are lower bounds on
the spatial demand `L_e`, to be inserted in (12); they are not direct
lower bounds of that size on `m_e`. Confusing demand with bank count
would invalidate the argument.

## 6. Tensor version

Let `C_B` be the board's uniform covariance and `C_t` the uniform
covariance of tile `t` about its centroid. Before the paired reserve,

\[
 S=\sum_t(g_t-o)(g_t-o)^T=N C_B-\sum_t C_t.
\]

Subtract `2 delta delta^T` for each half-turn pair to obtain the
matrix `S_M=sum_t x_t x_t^T`. For any symmetric positive-definite
matrix `H_0`, the same proof gives

\[
 \left(\frac{2\Delta}{3}\sum_e\lambda_eF_e\right)^2
 \le \operatorname{tr}(H_0S_M)
 \left[\sum_t b_t^T H_0^{-1}b_t
       -\frac{(\sum_t b_t)^T H_0^{-1}(\sum_t b_t)}N\right],
\]

where `b_t=tau_+(t)(lambda_(e_+(t))-lambda_(e_-(t)))Jv_t` on an
unmatched tile and zero on a paired tile; `J` is a quarter-turn, with
either consistent sign convention. This retains actual bank directions
and the anisotropy of the board. Taking `H_0=I` gives (11).

## 7. Audit conclusion and limitation

The determinant constant, the factor in (7), the half-turn reserve,
and the centering correction all follow from exact identities. The
two-tree graph is a legitimate strengthening because an actual tile
is represented once and its two cut coefficients have opposite signs.

The theorem is global: it permits arbitrary heights, phase translates,
reflections, T-junctions, charged branches and balanced branches. It
does not require the minimum-odd normal form. Nevertheless its
right-hand side is large at the target board scale, and no exclusion
of all feasible joint graphs or all larger odd populations is proved
here. A graph or degree assignment satisfying these inequalities is
still only a necessary projection of a geometric tiling.

The project's [companion exact verifier](../contact-budget/verify_contact_budget.py)
checks the cut and charge identities, the centroid budget, the matched
reserve, the graph Laplacian, all three energy bounds and the joint
charge Gram bound on two complete positive 143 controls, using independent
rational coordinate and valuation arithmetic. It also checks active-band
connectivity, physical population partitions, and every graph-cut capacity
on those controls. The [exact replay](../contact-budget/CONTACT_BUDGET_REPLAY.json)
records their scope; the universal assertion is the written proof above.
