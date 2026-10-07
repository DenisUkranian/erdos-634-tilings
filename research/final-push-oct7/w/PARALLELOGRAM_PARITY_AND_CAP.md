# Parallelogram parity and an all-orientation obstruction for scaled W caps

7 October 2026. Internal research note. This does not classify W scales or
solve Erdős problem 634. Reflections and arbitrary T-junctions are allowed.

Let `0<u<v`, `gcd(u,v)=1`, and put

    a=uv, b=v²−u², c=v², δ=v−u.

The angle gamma opposite c satisfies `cos(gamma)=−u/(2v)`. Write
`η=exp(i gamma)`. The primitive tile can be placed at

    0, a, bη,

and its counterclockwise boundary vectors are

    a, −cη³, −bη.

Indeed `a−bη=cη³`, which follows from

    q(η)=0,  q(X)=vX²+uX+v,
    f(X)=a−bX−cX³=−(vX−u)q(X).

## 1. Every tiled parallelogram has an even tile count

**Theorem.** If a parallelogram is tiled by congruent copies of this tile,
the number of tiles is even.

**Proof.** First, gamma/pi is irrational. Otherwise η is a root of unity,
so the rational algebraic integer `η+η⁻¹=−u/v` would be an integer,
which it is not. Thus distinct integer powers of η have distinct
directions modulo a half-turn.

The positive-edge adjacency graph of a finite tiling of a polygon is
connected: a generic path between two tile interiors can avoid every
tile vertex, and hence passes from tile to tile across positive-length
edges. Relative orientations of adjacent tiles differ by products of
reflections in their side lines. Since all angle differences of the
primitive tile are integer multiples of gamma modulo pi, a common
rotation of the whole tiling makes each tile a translate of either

    ε η^h T  or  ε η^h conjugate(T),   ε∈{−1,+1}, h∈Z,

where `T=(0,a,bη)`. The reflection in this expression is in the real axis;
translations do not affect boundary-vector signatures.

Assign the direction `η^j` the formal symbol `X^j`; a vector
`r η^j` with real signed r has signature `r X^j`. The irrationality just
proved makes this assignment unambiguous on every tile edge. The
counterclockwise signature of the first tile type is `ε X^h f(X)`.
Reflection reverses orientation, so the second type has signature
`−ε X^h f(X⁻¹)`.

Let U and V be the integer Laurent polynomials obtained by summing
`ε X^h` over the first and second types, respectively. Internal edge
portions cancel exactly, including at T-junctions. Opposite sides of the
outer parallelogram also cancel exactly: they have opposite equal
vectors. Therefore

    U(X)f(X) − V(X)f(X⁻¹) = 0.                         (1)

Evaluating this *formal polynomial identity* at `X=1` gives

    (a−b−c)(U(1)−V(1))=0.

The triangle inequality gives `a−b−c<0`, hence `U(1)=V(1)`. Every tile
contributes either +1 or −1 to one of these two evaluations, and both
are congruent to +1 modulo 2. Consequently

    N ≡ U(1)+V(1) = 2U(1) ≡ 0 (mod 2).

This proves the theorem. The proof uses neither whole-edge matching nor
any restricted set of tile orientations. ∎

## 2. Consequence for the unchanged +d cap macroregion

The scaled six-block cap investigated in
[`../../group1-global-scales/README.md`](../../group1-global-scales/README.md)
has one problematic parallelogram. Its sides are

    X=cK, Y=bK, K=dδ,

and their included angle is `pi−gamma`. Its area in primitive tile
units is exactly

    N_R = 2XY/(ab) = 2v δ² d²/u.                     (2)

The earlier two-axis-cell argument showed that this parallelogram can
be filled by those cells if and only if `u|d`. The parity theorem gives
the following stronger necessity for *arbitrary congruent-triangle
tilings*, with no restriction to cells or orientations:

    R tileable  ⇒  N_R is an even integer  ⇒  u|d².  (3)

The last implication uses `gcd(u,vδ)=1`. Equivalently, if
`u=product p^e`, every admissible d must be divisible by
`product p^ceil(e/2)`.

**Corollary.** If u is squarefree, this particular parallelogram is
tileable by the primitive triangle if and only if `u|d`.

Necessity follows from (3). For sufficiency use the original grid,
whose dimensions are `X/a=vK/u` and `Y/b=K`, both integers.

For `(u,v)=(2,3)` and `d=1`, the problematic parallelogram has sides
9 and 5 and area exactly three tile areas. No tiling by the `(6,5,9)`
triangle is possible, even using additional orientations. Thus a +1
construction cannot be repaired merely by retiling this unchanged
macroregion; a successful construction would have to alter its boundary
or permit tiles to cross it.

For nonsquarefree u, (3) is only necessary. For example it allows
`u=4,d=2`; no existence claim for that case is made.

## 3. A related signed-inventory lower bound

Equation (1) also gives a quantitative restriction. Since

    X³ f(X⁻¹)=(uX−v)q(X),

canceling q yields

    (vX−u)U=(v−uX)X⁻³V.

The two linear factors are relatively prime over Q[X], and primitive
over Z[X]. Gauss's lemma therefore gives an integer Laurent polynomial
H such that

    U=(v−uX)H, V=X³(vX−u)H.                         (4)

If `H≠0`, let h_min and h_max be its first and last nonzero coefficients.
For a non-monomial H, the extreme coefficients in the two products
give

    ||U||₁+||V||₁ ≥ (u+v)(|h_min|+|h_max|) ≥ 2(u+v).

For a monomial the same bound follows directly. Thus every tiling with
nonzero net orientation inventory has at least `2(u+v)` tiles. Equality
forces `H=±X^k`: if H had at least two terms, equality would require all
interior coefficients of both products to vanish, and their first
interior equations would require simultaneously
`v h_(k+1)=u h_k` and `u h_(k+1)=v h_k`, impossible for nonzero h_k.

This is an algebraically sharp inventory bound. Geometric realizability
at equality is **not established** here. In particular, the earlier
`2(u+v)`-tile c/a exchange parallelogram is made of half-turn pairs and
has `U=V=0`; it is not an equality witness for the nonzero-inventory
statement. If `N<2(u+v)`, every orientation type is balanced by its
half-turn, but that count balance does not geometrically pair the tiles.

## 4. Scope

The new conclusion closes the additional-orientation repair of the
unchanged cap macroregion whenever u is squarefree. It does not exclude
W or beta targets at those increments or scales. No general collar
extraction, alternate collar construction, or solution of the W scale
spectrum is obtained here.
