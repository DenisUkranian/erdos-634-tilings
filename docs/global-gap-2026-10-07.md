# The remaining global classification problem

7 October 2026. This note distinguishes the proved necessary spectra,
the available constructions, and the missing implications. It does
not claim a complete solution of Erdős problem 634. It uses the
exhaustive angular classification, rationality and primitive integral
normalization recorded in the [uniform-reduction proof](../research/uniform-reduction/PROOF.md).

## 1. What has to be decided

Write \(\mathcal S\) for the positive integers that count congruent
nondegenerate tiles in a dissection of a nondegenerate triangle.
Reflections and arbitrary T-junctions are allowed.

The classical count families

\[
r^2,\quad r^2+s^2,\quad2r^2,\quad3r^2,\quad6r^2
\]

have their existing arithmetic criteria and constructions. After these
are separated, the classified possibilities are the thirteen rows
below. Each has an integer residual scale \(t\ge1\) and count \(Dt^2\).

For Group 1 use coprime integers \(0<u<v\), tile
\((uv,v^2-u^2,v^2)\), and

\[
b=v^2-u^2,\qquad Q=2v^2-u^2,\qquad P=3v^2-u^2.
\]

The independent double-angle row has tile
\((u^2,v^2-u^2,uv)\), with \(0<u<v<2u\) and \(\gcd(u,v)=1\).
The norm rows use positive primitive short sides a,b and an integer c
satisfying the indicated norm. Both orders of a,b are included.

| Row | Necessary coefficient D | Available positive coverage; remaining issue |
| --- | --- | --- |
| Group-1 W | Q | Explicit cap semigroup and every-integer tail; smaller omitted scales are not generally excluded. |
| Group-1 beta-isosceles | P | W-to-beta attachment and the cap/tail construction; no general converse that extracts a W patch from an arbitrary beta tiling. |
| Group-1 theta-isosceles | b | Every-integer tail and complete first-tile spectrum; general smaller scales remain. Scale one is excluded. |
| Group-1 alpha-isosceles | bQ | Theta-to-alpha construction and explicit tails; the general below-tail region is not classified. |
| Group-1 QP | QP | **Every positive integer scale is constructive. This entire necessary row is globally positive.** |
| Double-angle isosceles | \(v^2-u^2\) | Necessary scale and long-seam restrictions, including exclusion of scale one; no complete general scale criterion is supplied here. |
| 60-degree equilateral | ab, \(c^2=a^2-ab+b^2\) | Explicit every-integer tail; remaining smaller scales are not generally decided. |
| 120-degree equilateral | ab, \(c^2=a^2+ab+b^2\) | Explicit every-integer tail; same limitation. |
| 120-degree F1 | b(a+b), plus norm | Positive attachment from an equilateral core and a tail; existence of that core in an arbitrary F1 tiling is not proved. |
| 120-degree isosceles | b(a+2b), plus norm | Positive attachments and a tail; smaller scales remain. |
| 120-degree F2 | (a+2b)(2a+b), plus norm | Equilateral-core and reflected-corner constructions, including the new three-generator domain; no necessity of either chosen decomposition. |
| 120-degree F3 | 3(a+2b)(a+b), plus norm | F2 attachments, nested corners, ordered gamma for b<a<=2b at every scale, and the staircase for b<a<=5b/2 at every scale t>=2. Exact staircase scales and a tail cover every positive gamma remainder; complementary cases remain. |
| 120-degree F4 | (2a+b)(a+b), plus norm | Every scale for a<b; reversed orientation has nested-corner and tail constructions, with an undecided complementary domain. |

The positive sources are the [QP construction](two-piece-construction.md),
[Group-1 caps](../research/w-beta-caps/PROOF.md),
[universal rational-scale theorem](universal-rational-scales.md),
[norm constructions and transfers](square-class-tails.md#appendix-a-every-integer-tails-for-all-norm-rows),
[oriented F4 construction](../research/group2-f4/PROOF.md),
[nested-corner theorem](../research/group2-nested-corners/PROOF.md),
[ordered gamma-corner theorem](../research/group2-gamma-corners/PROOF.md), and
[staircase extension](../research/global-classification-continuation/GAMMA_STAIRCASE.md).
The [long-seam proof](long-seams-density.md) supplies the stated necessary
isosceles inequalities. A sufficient tail is not asserted to be an
exact minimum scale.

## 2. The two predicates must not be conflated

For a prescribed N, let A(N) mean that the classical tests or at least
one of the finite primitive arithmetic candidates survives all
necessary conditions currently used. Let C(N) mean that an identified
proved construction, complete branch criterion or positive certificate
establishes membership. The valid implications are

\[
\boxed{C(N)\Longrightarrow N\in\mathcal S\Longrightarrow A(N).}
\]

Failure of A is a global exclusion. Passing C is a global positive
answer. Passing A but not C means that these tests do not decide the
count; it does not mean either that a tiling exists or that it is
impossible. Enlarging a construction domain improves C without
automatically proving the missing implication \(A\Rightarrow C\).

The complete QP construction eliminates that entire row from the
undecided remainder: if a candidate in that row exists, the integer
is already positive. The same holds for the a<b half of F4 and each
proved nested-corner instance. No proposed universal removal of the
other rows has been established.

## 3. At least W and F3 are globally indispensable

There are infinite families of actual counts which can occur only
in W, and others which can occur only in F3. Thus an arithmetic
replacement that discards either family in favor of the other
classified rows cannot give a full classification.

**W-only family.** For every odd t>=5 with 3 not dividing t,

\[
N=14t^2\in\mathcal S,
\]

and every classified realization belongs to W.

For positivity, choose u=2,v=3, giving tile (6,5,9) and coefficient
Q=14. The proved cap threshold is uv−u+1=5. For necessity, every
such N is 14 modulo 16. The complete residue argument in
[F3 global overlap](f3-global-overlap.md), Section 1, leaves only
W and F3 at this residue. F3 always has a count divisible by 3,
whereas this N does not. Only W remains. In particular no 60-degree
or 120-degree norm row realizes these counts.

**F3-only family.** For every odd positive k,

\[
N=990k^2\in\mathcal S,
\]

and every classified realization belongs to F3.

Positivity follows by refining the new 990-tiling. These counts
are 14 modulo 16 and have odd valuation at 5. The same isolation
theorem excludes W and all other branches. This is also a special
case of the [complete odd-multiplier class-110 criterion](square-class-110-odd.md).

These are obstructions to reducing all counts to one existing
angular branch or to one norm row. They do not rule out a common
new geometric theorem applicable to several branches. They also
do not imply that every listed branch is independently indispensable;
that stronger assertion has not been proved.

## 4. A genuine coefficient redundancy, but not a geometric converse

The 60-degree equilateral and plus-norm F1 **arithmetic coefficient
sets coincide**, apart from the classical equilateral tile.

Indeed, from a primitive plus-norm tile (a,b,c), set

\[
(A,B,C)=(b,a+b,c).
\]

Then \(\gcd(A,B)=1\) and

\[
C^2=A^2-AB+B^2,
\qquad AB=b(a+b).
\]

Conversely, order a nonclassical primitive minus-norm pair as
\(0<A<B\), and set \((a,b,c)=(B-A,A,C)\). This gives a positive
primitive plus-norm triple and the same coefficient. If A=B,
primitivity gives the classical equilateral tile (1,1,1).

Thus a necessary-coefficient enumeration can share these two
rows' arithmetic work. The transformation changes both the tile
shape and the target. It supplies no same-count transformation
of arbitrary tilings, so the two remaining geometric predicates
cannot yet be merged into an if-and-only-if construction rule.

There is nevertheless a valid global overlap consequence. **For every
primitive plus-norm tile with a<b, every count**

\[
b(a+b)t^2,\qquad t\ge6,
\]

**is globally admissible**, through the equilateral 60-degree tile
\((b,a+b,c)\). Its aspect ratio is \((a+b)/b\), strictly between
1 and 2, so the established 60-degree threshold
\(3(\lfloor\max(A,B)/\min(A,B)\rfloor+1)\) is exactly 6.
Thus the a<b half of the F1 arithmetic row contributes possible
global uncertainty only at the five scales t=1,...,5, regardless
of its original tile's aspect ratio. This does not assert a tiling
of the original F1 target by the original tile. When a>=b, the
transferred threshold equals the standard F1 threshold and gives
no further improvement.

## 5. Square-class tails do not remove the primitive front

Some large sectors are already uniform. Every fixed odd squarefree
d has an eventual positive multiplier tail: for d>1 choose
u=(d−1)/2, v=(d+1)/2, so the theta coefficient is d; d=1 is classical.
For even squarefree d and even m, choose u=d−1,v=d+1, whose primitive
theta coefficient is 4d. This supplies every sufficiently large
even multiplier in that class. These are existing constructions,
not assertions that all smaller multipliers are positive.

For even d and odd m, the
[fixed-split-part theorem](../research/arithmetic-continuation/GLOBAL_FIXED_SPLIT_PART.md)
reduces the problem to a finite primitive list and finite remainder
for each fixed joint split part H. Its bounds depend on d and H.

Even H=1 leaves an infinite primitive front as d varies. The
[squarefree F3 family](../research/arithmetic-continuation/SQUAREFREE_F3_FRONT.md)
gives infinitely many squarefree arithmetic candidates D whose
every possible realization must be F3 at residual scale one.
Their number through X is asymptotic to a positive constant times
X^(1/4). In global square-class notation they have d=D,m=1,H=1.
No such candidate is declared positive or negative by that family
theorem. Increasing residual multipliers through coefficient
replacement cannot resolve them, because squarefreeness forces
the residual multiplier to remain one.

## 6. A route that would actually close the gap

A complete answer needs a proved necessary-and-sufficient criterion
for every remaining integer. It need not separately solve every
fixed tile if a rigorous global overlap theorem eliminates some
cases. It must, however, cover every surviving branch whenever it
declares a count impossible.

For the current constructive approach, the decisive next result
would be a **necessary normal-form theorem**, or an exact substitute:
prove that every remaining tiling admits one of an explicit set of
positive decompositions, with a terminating arithmetic test for
their parameters. The existing rectangle, equilateral-core and
corner formulas would then be matched to necessary conditions.
At present their successful use is sufficient, not necessary.

The alternatives are to enlarge the constructive domains while
simultaneously proving that the remaining arithmetic candidates
are impossible, or to establish valid same-count overlap
equivalences that remove them. More constructions alone, more
finite examples, and an exact checker for a supplied disk do not
provide that missing universal implication. Nor does the existing
fixed-N decision perspective by itself supply the desired global
classification rule.

The result is therefore an exact description of the logical gap
and several rigorous reductions, not a declaration that all N
have been classified.

## 7. Execution of this plan: a new positive domain and its exact limit

The first geometric step produced an actual extension: the
[gamma-corner theorem](../research/group2-gamma-corners/PROOF.md) proves
ordered F3 for every positive multiplier whenever `b<a<=2b`. It gives a
264-tile `(5,3,7)` certificate in `(49,77,72)`, independently checked both
by rational geometry and by incidence-only disk development. This example
also disproves the proposed universal necessity `bc>=a²`.

The same proof gives an exact boundary for a restricted class of fillings.
At primitive multiplier one, its gamma remainder has a tiling using one
common short-edge direction class if and only if `a<2b` (provided the
remainder is geometrically defined). For `a>2b`, the axis boundary length
`E=2ab+2b²-a²` is not in `<a,b>`. Thus, at that primitive scale, a staircase
using arbitrarily many pieces of that same direction class cannot extend the construction.
Any extension must introduce another class or use another macro partition.
For `(24,11,31)`, the side E=194 permits c-edges but cannot consist of
24- and 11-edges alone. This is not a negative decision of 4830.

The matching negative-proof route was also tested: the
[full directed-edge signature](../research/f3-descent-attempt/F3_FULL_SIGNATURE_BARRIER.md)
has a positive unplaced inventory with the exact F3 tile count for every
parameter in the stated range, including 4830. Those translation-invariant
conditions cannot decide the remaining geometry. In Group 1, the
[scale-descent audit](../research/group1-continuation/SCALE_DESCENT_AUDIT.md)
exhibits an actual `uc=va` exchange seam where the scale-one purity
argument stops. A global collar extraction is still needed.

These are concrete outcomes of the plan, but neither missing global
implication has been proved. The full classification remains unresolved.

## 8. Further execution: staircase scales and a remaining primitive gap

The [common-cell staircase theorem](../research/global-classification-continuation/GAMMA_STAIRCASE.md)
removes the unnecessary upper corner of the earlier bounding rectangle.
For `a>b`, it constructs the ordered F3 target whenever

    b+a*ceil(m(a-b)/b) <= m(a+2b).

This is an exact criterion for that grid recipe and a sufficient condition
for genuine geometry. If `E=2ab+2b²-a²>0`, it holds at every integer
`m>=ceil((b(a+b)-a)/E)`. Its successful scales have a finite residue
description modulo b. In particular **every m>=2 works throughout
b<a<=5b/2**. This is a general family, not an inference from a search sample.

For `(24,11,31)`, all `4830m²` with m>=2 are now positive. The first case,
19320, has a [complete exact unit-coordinate certificate](../research/group2-mixed-gamma/README.md)
and an independent checker. Thus **4830 is the only remaining integer in
that whole square class**. Its primitive gamma remainder still requires
additional short-direction classes or a different macro partition.

A converse based on bounded gamma scales is now excluded: for every K,
[infinitely many positive gamma remainders](../research/f3-position-invariants/GAMMA_BOUNDARY_OBSTRUCTION.md)
fail to tile at every scale 1,...,K, even with arbitrary directions.
Their exterior side has length outside `<a,b,c>`; the infinite-family
proof uses Siegel's integral-point theorem. The new staircase tail proves
eventual filling for each fixed such tile. These two assertions are
compatible and neither says the corresponding full F3 targets are impossible.
In fact necessity of this macro partition is false: tile `(2024,741,2479)`
has an F3 tiling at scale 6 by the established general tail, whereas its
gamma remainder has exterior length 6924 outside `<2024,741,2479>`.
It cannot be filled even with arbitrary directions. The cited proof
also supplies infinitely many such examples at each fixed scale m>=6.

The other attempts did not yield a matching global converse. The
[I120 identity](../research/i120-continuation/README.md) shows that full
directed-edge signatures also pass 154. The
[diameter barrier](../research/global-normal-forms/DIAMETER_EXCHANGE_BARRIER.md)
proves that replacing genuine seams by their shortest arithmetic lengths
discards all discriminatory power on the norm rows. W/beta collar
extraction and unrestricted fillings at 154 and 4830 remain missing.
For W56, an [eleven-tile partial patch](../research/group1-global-scales/README.md)
exhibits the three-acute-angle alternative to the next supposedly forced
gamma tile. It is a real local escape, with neither completion nor a
global impossibility asserted. At multiplier two the gamma remainder's
[single-short-class criterion](../research/global-normal-forms/GAMMA_SCALE_TWO_AUDIT.md)
is now exact, `a<5b/2`, but that restricted converse is not a converse
for unrestricted F3.
Consequently `C(N) => N in S => A(N)` is still the proved global relation;
the reverse implication has not been obtained.

The subsequent [I120 boundary lemma](../research/i120-continuation/BOUNDARY_ADJACENCY.md)
extends the F1 blocked-endpoint argument: when a>b, every external I120
side has two consecutive c-edges. For 154 this reduces each length-91
side from six possible count rows to four, and its base from 17 to 14.
It supplies no exclusion of the remaining rows. A proposed lower bound
`N>=c²` for the remaining nonclassical targets has not been proved and
is not used as a necessary condition. In particular neither this bound
nor an unfinished search changes the unresolved status of 154 or 4830.

## 9. Further general results without the missing converse

The [exact Apéry formula](../research/global-criterion-oct7/SHARP_NESTED_CONE.md)
extends the nested-corner construction from `1<a/b<=7/5` to the sharp
initial open cone `1<a/b<45/32`, uniformly at every positive multiplier.
It covers reversed F4, F2, and both F3 orientations. The endpoint is
sharp for this construction criterion only; it does not exclude arbitrary
tilings. Its proof is general, with exact finite arithmetic regressions.

The [Group-1 boundary theorem](../research/w-global-oct7/ADJACENT_C_EDGES.md)
forces two consecutive longest edges on every side of W, beta and theta
targets. Its blocked-endpoint proof works with either ordering of a,b
and includes a separate theta-apex argument. The
[independent audit](../research/barriers-oct7/W_BOUNDARY_INDEPENDENT_AUDIT.md)
also checks the complete two-root reduction for W56's short boundary.
The bounded continuation from those roots remains incomplete.

The [orientation-level theorem](../research/i120-global-oct7/HEIGHT_LEVELS.md)
gives `c | n_h` outside one exceptional height for five plus-norm rows:
height zero for equilateral, F1 and I120, and height two for F2 and F3
in their stated canonical orientations. The exceptional population is
congruent to N modulo c. The proof uses actual positive tile unions and
whole-edge chains, rather than a formal unplaced orientation inventory.
Even so, the existing unplaced 154 inventory passes these congruences.

A fresh 154 search added integer residual-seam and vertex-on-edge
checks to the previous fan-propagation engine. Its 300-second run
visited 2674 nodes and stopped at `INCOMPLETE`; the additional pruning
found only two incompatible tile pairs. The
[primitive F3 macro searches](../research/f3-primitive-oct7/README.md)
also stopped incomplete. None supplies a negative decision.

Thus these improvements enlarge the proved constructions and necessary
conditions, while 154, 4830 and the general below-tail geometric
criterion remain unresolved. No complete classification is asserted.

## 10. Stronger geometric attempts and their remaining limits

An [exact position-moment witness](../research/f3-moments-oct7/README.md)
now assigns actual rational positions and positive integer multiplicities
to 4830 congruent `(24,11,31)` triangles inside the correct F3 target.
It matches the full directed-edge signature, both coordinate first
moments in every edge direction, total area, area centroid and height
populations `(93,4737)`. Nevertheless, it has only nine distinct placements,
and one positive-area triangle is repeated 2385 times. Two exact checkers,
one independent of the optimization model, verify this explicit overlapping
multiset. Thus even these position-sensitive additive conditions and
individual containment do not establish a genuine dissection. This is
neither a positive nor a negative decision of 4830.

For W with `u=v-1`, `v>=3`, the forced scale-two word `c,c,a,a` has a
[universal nine-tile collar](../research/w-scale-two-oct7/README.md).
It fills the five angle fans along that entire short side, including
both target corners. Congruence and target shape are rational identities;
containment and all 36 pairwise separations are proved by polynomial
coefficient signs after `v=3+x`, `x>=0`. Consequently the short-side word
and these local fans alone give no contradiction for any such parameter.
The remaining region is not filled, and scale-two W is not classified.

The [population-budget continuation](../research/i120-boundary-oct7/README.md)
adds a necessary rounded count bound for partial placements. Connectivity
of positive-length tile contacts also implies that consecutive occupied
short-edge heights differ by at most two. For 154 the existing congruences
therefore confine all heights to `[-22,22]` in canonical coordinates.
The pure-long-91-side search treated 128 initial orientation patterns:
112 exhausted in the search engine without independent certificates,
and 16 remained incomplete. None of these reports supplies a global
exclusion or a proof that a pure-long side forces a complete grid.

Two [prescribed six-macro searches](../research/f3-construction-oct7/README.md)
also exhausted without finding a construction; their narrow scopes and
lack of independent refutation certificates are explicit. A proposed
two-height interface divisibility was discarded because it omitted one
of the two allowed whole-edge lattice contributions.

The decisive missing statement remains a necessary-and-sufficient global
geometric criterion. The cases 154 and 4830 are still unresolved here;
the two new exact results above restrict particular methods, not the
set of admissible integers. A complete classification has not been proved.
