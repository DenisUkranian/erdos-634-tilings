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
| 120-degree F3 | 3(a+2b)(a+b), plus norm | **Every positive integer scale for 0<a<2b**, combining the new a<b construction with ordered gamma. The staircase also covers b<a<=5b/2 at every scale t>=2. Further nested-corner and tail cases are positive; the remaining a>2b cases are not generally classified. |
| 120-degree F4 | (2a+b)(a+b), plus norm | Every scale for a<b; reversed orientation has nested-corner and tail constructions, with an undecided complementary domain. |

The positive sources are the [QP construction](two-piece-construction.md),
[Group-1 caps](../research/w-beta-caps/PROOF.md),
[universal rational-scale theorem](universal-rational-scales.md),
[norm constructions and transfers](square-class-tails.md#appendix-a-every-integer-tails-for-all-norm-rows),
[oriented F4 construction](../research/group2-f4/PROOF.md),
[new a<b F3 construction](../research/best-move-oct7/hexagon/F3_SMALL_A.md),
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
is already positive. The same holds for the a<b half of F4, the
0<a<2b sector of F3, and each proved nested-corner instance. No proposed
universal removal of the other rows has been established.

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

## 11. Three-route audit and an exact moment hierarchy

The [executed strategy audit](../research/strategy-oct7/README.md) tests
global geometric normalization, same-count parameter descent and direct
overlap control. None supplies a full classification.

The [parameter calculation](../research/strategy-oct7/plan-b.md) makes one
barrier exhaustive: 4830 has only the ordered primitive F3 tile
`(24,11,31)` at residual scale one. In variables `s=a+b`, `t=a+2b`, its
only divisor pair with `st=1610` and `s<t<2s` is `(35,46)`. Hence a
different primitive tile cannot automatically transfer this candidate
to an existing constructive cone. A theorem applying only to realizable
counts could still exclude 4830, but would need new geometric necessity.

The [moment analysis](../research/strategy-oct7/plan-c.md) now proves a
uniform limitation rather than a single numerical example. For every
fixed degree d, there are `(d+3)^2` distinct contained triangular copies
matching every area moment and each direction's signed boundary moments
through d, with the correct orientation populations, but with overlaps.
The argument uses polynomial translations and Newton identities and
persists after refining any existing nonclassical tiling. It does not
produce an untileable target passing an existence test.

There is also a precise complementary sufficiency theorem: for a
specified N-placement, matching signed directional boundary moments
through degree 2N forces a genuine tiling. A line-isolating polynomial
reduces the claim to step measures on a line; their at most 2(N+1)
endpoints are determined by the moment equations via Vandermonde.
The resulting zero boundary current makes the coverage discrepancy
identically zero almost everywhere, and closedness gives exact coverage.
This verifies finite placement data; it does not find placements or
classify their possible counts.

The [normalization audit](../research/strategy-oct7/plan-a.md) shows why
even a uniform short-height window would leave an additional positive-
completion theorem. Its proved conditional lattice bound and one-height
I120 exclusion do not provide the missing global replacement. Thus the
remaining work is a substantive geometric existence theorem, not merely
a fixed-order moment extension or a change of primitive parameters.

## 12. A new positive macro partition and three precise barriers

An [earlier three-route continuation](../research/final-push-oct7/README.md)
tested a different positive F3 partition, an all-orientation W cap repair,
and decomposition of exact multiple covers. That continuation produced
general lemmas, but no new decision of a previously unresolved count.
Section 13 records the later positive construction and complete class
result, which go beyond those earlier barriers.

For every ordered plus-norm tile with `a>b`, three c-fold sectors and
four further triangular grids fit inside the primitive F3 target. The
seven grids contain `3c²+7b²` unit tiles and leave the explicit simple
hexagon `H(ab,b²)` of `2b(3a−2b)` tile areas. The
[universal containment and disjointness proof](../research/final-push-oct7/f3/FAN_HEXAGON.md)
has no aspect-ratio cutoff. At 4830 its remainder has 1100 tile areas.
That remainder has not been filled. Its direction-resolved boundary
current excludes every filling restricted to the one displayed short
height, including the obvious parallelogram grids. The
[two-height formal inventory](../research/final-push-oct7/pentagon/SHORT_HEIGHT_OBSTRUCTION.md)
still passes with positive unplaced counts, so this obstruction does
not exclude an unrestricted filling. The macro partition supplies a
sufficient route only; it is not forced in arbitrary F3 tilings.

In W, a [new parity argument](../research/final-push-oct7/w/PARALLELOGRAM_PARITY_AND_CAP.md)
shows that any parallelogram tiled by the primitive W tile contains an
even number of copies, with no orientation or edge-matching restriction.
The problematic parallelogram of the scaled `+d` cap therefore requires
`u|d²`. For squarefree u it is tileable exactly when `u|d`. This closes
repair of that unchanged region in additional orientations, but does
not rule out a replacement crossing its boundary or another W tiling.

For every 120-degree triangle a
[nine-copy angular construction](../research/final-push-oct7/duality/LOCAL_MULTIPLICITY.md)
exactly double-covers a small punctured disk while its intersection graph
contains an induced odd cycle. It cannot split into two local single
covers. No completion to an exact double cover of an entire triangular
target is supplied, so this is a local decomposition barrier, not a
counterexample to a global existence equivalence. Separately, all F3
boundary words vanish in every prime-exponent quotient of the ordered
tile group; the [proof](../research/final-push-oct7/duality/NONCOMMUTATIVE_BOUNDARY.md)
includes nonabelian quotients but makes no claim about all groups or
positive geometric diagrams.

Those routes left the same decisive obligation: prove a complete
positive-filling criterion or a necessary global normal form, and cover
every remaining branch before excluding a count. Those lemmas did not
settle 154 or 4830 or complete the all-integer classification.

## 13. A complete ordered F3 sector and the entire square class 78

The [new positive construction](../research/best-move-oct7/hexagon/F3_SMALL_A.md)
proves, for every positive integral plus-norm tile with a<b,

\[
3(a+b)(a+2b)m^2\in\mathcal S\qquad(m\ge1).
\]

The target is dissected into a c-fold tile, two b-fold tiles, the
already constructible F4(a,b) triangle, and an ideal trapezoid with
short base `2ab+b²` and leg `ab`. Its difference from the existing
trapezoid seed is `a(3b-c)>0`, an explicit short-grid width. All pieces
have positive fillings and disjoint interiors; there is no unresolved
hexagon in this partition. The
[independent symbolic audit](../research/best-move-oct7/geometry/F3_A_LT_B_AUDIT.md)
checks the exact dissection and the orientation of its F4 block.

Together with the earlier ordered gamma construction, this supplies
**every positive integer multiplier throughout 0<a<2b**. The new
theorem covers the previously missing a<b order even when b/a is
arbitrarily large; swapping short-side labels was not previously a
valid transfer between the two F3 targets.

The construction at `(a,b,c)=(3,5,7)` gives the independently checked
312-tile target `(49,91,120)`. Combining that seed with the
[elementary local obstruction](../research/best-move-oct7/new-arithmetic/CLASS78.md)
now proves the complete global criterion

\[
\boxed{78m^2\in\mathcal S\quad\Longleftrightarrow\quad 2\mid m.}
\]

For odd m the existing exhaustive residue theorem leaves only F3.
A putative F3 coefficient gives a positive rational point on
`y²=x³+156x²-2028x` with `v_2(x)=1`. Its only possible positive square
classes are `2,6,26,78`, all excluded by explicit congruences modulo
13. The proof uses no rank computation or unproved completeness of
rational-point data. Every even m follows by subdivision of 312.
The [separate audit](../research/best-move-oct7/geometry/CLASS78_AUDIT.md)
checks both directions for arbitrary multipliers.

The new construction also makes an additional positive decision in
the prior project ledger: **573390**, with tile `(136,209,301)` and
target `(90601,166754,216315)`. The
[arithmetic audit](../research/best-move-oct7/new-arithmetic/COUNT_573390.md)
proves that every realization must belong to F3 and that this ordered
primitive tile at residual scale one is its unique candidate. It also
checks why the previously recorded sufficient constructions did not
supply this count. No priority over the literature is claimed.

These are genuine geometric and all-multiplier classification gains,
but the full problem remains open in this repository. In particular,
**154 and 4830 remain unresolved**. The latter has a/b=24/11>2 and
therefore lies outside the newly completed sector; its multiples
`4830m²`, m>=2, were already constructed by the staircase theorem.
General W/beta small-scale questions, other norm branches, and the
remaining F3 domain still prevent a characterization of every N.

## 14. An infinite product extension of the class-78 obstruction

The [quartic-descent theorem](../research/quartic-descent-oct7/PROOF.md)
extends the negative half of Section 13 to squarefree products with
unbounded prime support. Let R be a product of an odd number of distinct
primes p satisfying

\[
p\equiv13\pmod{24},\qquad 3^{(p-1)/4}\equiv1\pmod p.
\]

Then

\[
\boxed{6Rm^2\notin\mathcal S\qquad\text{for every odd positive integer }m.}
\]

The existing all-branch residue reduction isolates F3. Its coefficient
would give a positive rational point with odd 2-adic x-valuation on
`y²=x³+12Rx²-12R²x`. Every possible square class of x determines a
partition R=AB. The local quartic equations require `(A/p)=-1` at
each prime dividing B and `(B/p)=-1` at each prime dividing A. All
primes are 1 modulo 4, so quadratic reciprocity equates the products
of these symbols; their signs are opposite because R has an odd
number of prime factors. This excludes every cover without a rank
or Mordell–Weil basis calculation. The
[independent internal audit](../research/quartic-descent-oct7/AUDIT.md)
checks the rational map, local equations and reciprocity argument.

The qualifying primes have density **1/16 among rational primes**, by
Chebotarev applied to the explicit degree-16 splitting field in the
proof. This infinitude input is separate from the elementary exclusion
for each specified R. Initial kernels include 78, 654, 1086, 1374 and
1662; products can involve arbitrarily many qualifying primes.

For each fixed R, the existing effective theta construction supplies
every sufficiently large even multiplier. Consequently membership in
this square class is eventually equivalent to evenness, with a
computable sufficient threshold. **Only R=13 is currently closed at
every even multiplier**, through the 312-tile seed; no assertion that
all small even multipliers work is made for the other R.

This adds infinitely many complete odd-multiplier exclusions, not a
complete classification of their small even sectors or of all counts.
**154 and 4830 remain unresolved**, and the remaining geometric scale
predicates in the other branches still require a general solution.

## 15. Final synthesis addendum: local decisions and a sparse F3 remainder

7 October 2026. The [final synthesis](../research/final-synthesis-oct7/README.md)
adds the following results without changing the unresolved all-N status.

For odd squarefree R with `3∤R` and `R≡5 mod8`, the
[full local matrix](../research/final-synthesis-oct7/arithmetic/FULL_LOCAL_MATRIX.md)
is an exact linear test over F₂ for the relevant quartic covers at every
prime dividing 6R, with the required 2-adic valuation. **Inconsistency
excludes every odd multiplier in `6Rm²`**, using the exhaustive F3
isolation. A surviving assignment supplies local points only; rational
points, coefficient witnesses and geometric tilings remain separate
requirements. The [independent audit](../research/final-synthesis-oct7/arithmetic/FULL_LOCAL_AUDIT.md)
checks both the local equivalence and this one-way global implication.

The [class-38 nonperiodicity theorem](../research/final-synthesis-oct7/STRUCTURAL_AUDIT.md),
with a [separate audit](../research/final-synthesis-oct7/CLASS38_AUDIT.md),
rules out another proposed simplification: for every modulus M, some
residue class contains infinitely many odd realizable multipliers and
infinitely many odd impossible ones. Thus no fixed congruence test becomes
exact after finitely many exceptions in this square class.

Nevertheless, the [fixed-class F3 density theorem](../research/final-synthesis-oct7/F3_FIXED_CLASS_DENSITY.md)
proves that the actual odd F3 multiplier set has a natural density among
odd integers. For each fixed squarefree d, let A_d be its necessary
coefficient-divisibility envelope, F_d the actual F3 set, and C_d the
subset supplied by the established every-integer constructive tails.
Then `C_d⊆F_d⊆A_d`; all three densities agree, and

\[
\#((A_d\setminus C_d)\cap[1,X])
=O_d\!\left(X^{1/3}(1+\log X)^{r_d/2}\right),
\qquad r_d=\operatorname{rank}\bigl(Y^2=X^3+(3d)^3\bigr).
\]

The [density audit](../research/final-synthesis-oct7/DENSITY_AUDIT.md)
checks the elliptic height bound, geometric threshold and order of density
limits. The bound counts a superset of unresolved F3 multipliers, not
proven negative cases; its constants depend on d. In class 38 all odd
realizations are F3, so this is a global density result with
`0<δ_38≤1/3`, compatible with nonperiodicity. No numerical density or
certified numerical error constant has been computed.

The geometric obligations remain concrete. For
[154](../research/final-synthesis-oct7/i120/README.md), subtracting the
49-tile corner from the `(91,91,154)` target would leave the excluded
105-tile F1 target, but no theorem forces that corner in every tiling.
The stronger search remains incomplete. For
[4830](../research/final-synthesis-oct7/f3/README.md), the sole primitive
F3 candidate `(24,11,31)` at scale one remains undecided; all `4830m²`
with `m≥2` are already constructive. The 792-area quadrilateral is one
sufficient route, and its four-macro obstruction is not an obstruction
to arbitrary unit tilings. For
[W/beta](../research/final-synthesis-oct7/w-beta/BOUNDARY_FILTER_BARRIER.md),
the combined boundary-word tests pass every scale `m≥2` and scale one
when `u≥2` and `v−u≥2`; their compatibility does not supply a global disk
or the missing forced-patch converse.

The [fresh source audit](../research/final-synthesis-oct7/LITERATURE.md)
finds no inspected external result closing those implications. Harries's
finite generator windows fix the ordered tile and target; the solution
of problem 633 has a different quantifier; older all-prime statements
cannot restore retracted W/base-beta lemmas. This is a bounded literature
audit, not a claim to have exhausted every source. **154, 4830 and the
full classification remain unresolved.**
