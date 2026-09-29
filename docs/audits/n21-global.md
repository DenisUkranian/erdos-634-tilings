# Independent audit of the global N=21 reduction

29 September 2026. Internal mathematical audit; no priority or external-review
claim. This checks the passage from the standard exhaustive shape
classification to the independently refuted `(2,3,4)`-tile instance.

**Finding: PASS, with the explicitly cited classification and rationality
theorems as outside inputs.** The arithmetic reduction has no prime-only
hypothesis. Together with the independently replayed 391-node alpha21
certificate, it proves that no triangle admits a dissection into 21 congruent
triangles. This settles one integer count, not Erdős problem 634 in general.

## 1. Outside theorem statements checked afresh

The following primary sources were opened directly, rather than relying solely
on the repository's earlier prime-case ledger.

| Needed input | Checked location | What is used |
|---|---|---|
| Similar tile and target | Beeson, [1206.1974v7](https://arxiv.org/html/1206.1974v7), Theorem 2.1, restating Snover–Waiveris–Williams | Counts are squares, sums of two squares, or three times squares. |
| Non-equilateral isosceles shapes | Same source, Theorem 3.1 and Table 1, spelling out Laczkovich's classification | Right, double-angle, 120-degree, or the three Group-1 isosceles shapes, after removing similarity. |
| Isosceles right and double-angle restrictions | Same source, Theorems 7.8 and 11.7 | The right case is square or even; the irrational double-angle case is not squarefree. Both apply to composite counts. |
| Equilateral shapes and 60-degree rationality | Beeson, [1812.07014v3](https://arxiv.org/html/1812.07014v3), Introduction | Five tile types; irrational 60-degree tiles are rational. The three rational-angle count restrictions are also checked directly by area rather than relying on the source's incomplete count summary. |
| Nonsimilar irrational 120-degree rationality | Beeson–Zhang, [2604.01314v1](https://arxiv.org/html/2604.01314v1), Theorem 1.1 | Integer primitive side normalization is legitimate for all nonsimilar targets. |
| Non-isosceles shapes | Beeson, [2607.23453v1](https://arxiv.org/html/2607.23453v1), Theorems 6 and 9, restating Laczkovich | Rational-angle non-isosceles targets are reptilings; the irrational case has two Group-1 and four 120-degree shapes. |
| Group-1 rationality and parameters | Local primary PDF/text of [1206.2229v4](https://arxiv.org/abs/1206.2229v4), Lemmas 4 and 11, Theorem 9 | All five nonsimilar shapes have primitive sides `(uv,v²-u²,v²)`. |

The four 120-degree target side proportions and area formulas were checked
against the explicit sine-law computations in Theorems 18–21 of
`2607.23453v1`. Its broad prime-count conclusion and disputed older dependencies
are not used; rationality is supplied by Beeson–Zhang Theorem 1.1 instead.
The formulas themselves hold for arbitrary positive integer N.

This is a verification of the statements and sufficiency of the outside inputs,
not an independent reproof of every published classification theorem.

## 2. Arithmetic and shape coverage

21 is squarefree, odd, nonsquare, not three times a square, and not a sum of two
squares. These facts remove reptilings and the right/double-angle isosceles
branches. Equilateral rational-angle tile types give a square or 2, 3, or 6
times a square and are also impossible.

For an irrational equilateral tile, the signed-direction equations give
positive integer factor pairs of 63. Independently simplifying the two flux
products gives the necessary square conditions

$$
(t-s)^2-84\quad(60\text{-degree tile}),\qquad
(t-s)^2+336\quad(120\text{-degree tile}).
$$

The pairs `(1,63)`, `(3,21)`, `(7,9)` give no nonnegative square. The invariant
is valid for reflected tiles and T-junctions because it is additive in edge
length and odd under reversing a directed segment. The step from a rational
square to an integer square is legitimate.

In Group 1, the integer-scale equations for W and beta follow from primitive
target side triples and integer external side lengths, independently of
coloring divisibility. Their forms are `Q T²` and `P T²`. W is excluded by
`Q mod8` in `{1,2,6,7}`; beta by the three coprime pairs with `v<=3`. The
other scalene count `QP K²` is at least 77.

The theta and alpha necessary forms `b T²` and `bQ K²` were independently
checked from the two genuine Group-1 characters and their common parity. For
theta the half-sum and half-difference force `b|uL,vL`, hence `b|L`. For alpha
the half-difference is `LQ/b`, and `gcd(b,Q)=1` forces `b|L`. Neither argument
requires primality or squarefree b. Alpha leaves exactly `(u,v)=(1,2)` and
therefore tile `(2,3,4)` in target `(12,12,21)`.

### A simpler theta exclusion

The reduction can avoid the stronger two-c-edge boundary lemma entirely.
Since 21 is squarefree, `N=b T²` forces `T=1`, so an equal side has length
`X=vb`. The unique alpha tile at the apex contributes a b-edge to one equal
side. In its whole-edge decomposition, reduction modulo v forces the number
B of b-edges to satisfy `v|B`. Thus `B>=v`, exhausting the entire length X.
The side consequently consists only of b-edges.

If it consists of m such edges, their m adjacent tiles each have an obtuse
gamma angle at one endpoint. Neither target corner can contain gamma. There
are only m-1 internal boundary vertices, and each accommodates at most one
gamma because `2gamma>pi`. This is impossible. This pigeonhole argument
explicitly allows T-junctions and uses only whole tile edges on the convex
external boundary.

## 3. Independent F1 signed-flux computation

The 120-degree F1 target has sides `k(a+b),ka,kc`. Orient its boundary
counterclockwise with the first side horizontal. The next side has direction
`2pi/3`; the final side has direction `pi+alpha`. For

$$
f(n\alpha+j\pi/3)=(-1)^j,
$$

its boundary flux is

$$
k(a+b)+ka-kc=k(2a+b-c).
$$

A reference tile with its c-edge horizontal has edge directions `0`,
`2pi/3+alpha`, and `pi+alpha`, and therefore flux `c+a-b`. Rotations in the
propagated direction group and reflections give its positive or negative.
Dividing the target flux by the tile flux must be an integer. Hence the unique
structural candidate `(a,b,c;k)=(5,16,19;4)` is impossible because the ratio
is `28/8=7/2`.

This derives the obstruction directly; it does not import the prime-only
isosceles specialization or the condition `k²=b`. Indeed here `k²=b` happens
to hold, but the target shape and relevant flux are different.

For the other 120-degree shapes, primitive side proportions force integer
scales. The three product counts exceed 21 since every primitive positive
integer 120-degree triple has `a+b>=8`. The isosceles count equation restricts
`a+2b` to divisors of 21; its four square-scale candidates all have nonsquare
`a²+ab+b²`. These finite lists were replayed exactly.

## 4. The final geometric input

The separate checker [`verify_alpha21.py`](../../scripts/verify_alpha21.py) has already verified the
391-node certificate, expanding every repeated reference under each actual
placement history. It checks 437 expanded states and 158 dead ends, using
exact local tangent cones and rational polygon clipping independently of the
search's residual-boundary and separating-axis machinery.

No direction grid, denominator cap, edge-to-edge condition, prime-count
candidate, or external search certificate is needed. The proof chain is:
exhaustive published shape classification; explicit arithmetic and signed
flux reductions for 21; the exact alpha21 nonexistence certificate.

## 5. Attribution and limitation

Bonfioli's current source already reports a global exclusion of 21, and the
F1 `28/8` obstruction also occurs there. Therefore no first-discovery claim
should accompany this result. The present contribution is an explicit
reviewed reduction joined to an independently reproducible small exact
certificate. The full set of possible counts in Erdős 634 remains unresolved.
