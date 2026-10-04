# Finite construction schemes: an orientation test and a quantitative constraint

3 October 2026; scope corrected 4 October 2026.
Research with ChatGPT assistance directed by Denis Paliy.
The finite-scheme conjecture and Erdős problem 634 remain unresolved.
The results below are elementary deductions, reviewed separately within
this investigation; no external acceptance or priority is asserted.

## The conjecture and its quantifiers

The broad conjecture concerns a finite library of explicit positive
construction recipes with a fixed number of parameters. Grid sizes and
specified repetition counts may be arbitrarily large. A recipe cannot
hide an arbitrary unresolved tiling problem inside a named region.
For example, a parameterized stack of explicitly tiled trapezoid bands
is a permitted recipe, although its number of individual grid regions
can grow without bound. This differs from requiring a fixed number of
ordinary grid blocks.

The strong conjecture is that there is a finite catalog of such schemes
so that every tileable pair consisting of a triangular target T and a
triangular tile R has an alternative tiling by the same R, with the same
T and tile count, described by a catalog scheme. This is an existence
claim about an alternative; the original tiling need not be transformable
by prescribed local moves.

The earlier 1 October archive posed and then **refuted** the absolute
bound for ordinary triangular and parallelogram grid blocks, even when
the tile and target may change while preserving N. The later
`Erdos634_unbounded_blocks_PROOF` manuscript supersedes the earlier
positive-normal-form conjecture; the [archive reconciliation](audits/research-2026-10-03.md)
already recorded that distinction. The original version of this note
omitted that negative result. It is not an unresolved route to reuse.
Its proof does not refute the broader repetition grammar above.

## A necessary intermediate statement

For the subclass in which each permitted recipe uses at most d
orientations of R, counting reflections separately, and each scheme
uses at most K recipes, the conjecture would imply:

> Every tileable pair (R,T) has an alternative tiling using at most dK
> orientations, independently of its number of unit tiles.

This follows by taking the union of the orientation sets of its recipes.
Ordinary triangular grids, parallelogram grids, and grid regions formed
by deleting a grid corner each use at most two orientations. Mixed strips
may instead be one repeated recipe if their positive filling is explicit.
Their orientation bound must then be proved for the whole recipe,
uniformly in its repetition count. A rule that repeatedly rotates a
patch through an irrational angle need not have such a bound: finite
description alone does not imply finitely many orientations uniformly.

This statement is weaker than bounded block complexity, and a precise
first target for the uniformly bounded-orientation subclass. To refute it,
one needs a sequence of tileable pairs for which **every** tiling requires
an unbounded number of orientations. Exhibiting one intricate tiling,
many T-junctions, or a particular tiling with many orientations is not
enough. Conversely, proving this orientation bound would not alone prove
the finite-scheme conjecture. A counterexample to it would rule out that
subclass, but not every possible finite recursive grammar.

The [capacity extension](grid-capacity-and-orientations.md) now gives
explicit tileable equilateral pairs requiring an unbounded number of
convex single-grid regions, including corner-deleted grids. The same
pairs have tilings with at most 18 rigid orientations, supplied by a
fixed repeated-band recipe. Thus this obstruction separates the two
notions instead of refuting the broad conjecture.

## A quantitative restriction on grid schemes

Assume a nonsimilar triangular target has a checkerboard tiling by R,
with every exterior-contact tile black. Let p be the tile perimeter,
s its shortest side, and M=perimeter(T)/p. Suppose a description consists
of ordinary triangular grids, parallelogram grids, and exceptional
patches containing altogether A unit tiles. Let D be the sum of the
integer side scales of triangular grids whose boundary tiles are white.
All blocks have positive geometric area; white is only a checkerboard
color, not a negative tile.

Then

\[
\boxed{D+A\ge \frac{Ms}{2(p-s)}.}
\]

**Proof.** Internal contact lengths cancel, giving B-W=M, where B,W
are the numbers of black and white unit tiles. A triangular grid of
side scale k has imbalance +k or -k according to its boundary color;
a parallelogram grid has imbalance zero. If q is the imbalance of the
exceptional patches and S is the sum of all triangular-grid side scales,
then |q|<=A and M=S-2D+q.

Use the additive signed-direction boundary signature described in the
[matching argument](checkerboard-matching-limit.md). Apply the linear
functional that keeps the target's three directed boundary coordinates
with their boundary signs and sets all other coordinates to zero. Its
value on T is its perimeter. A parallelogram contributes zero. Since R
and T are not similar, no orientation of R has all three edge directions
parallel to those of T. At least one side, of length at least s, is
omitted. Thus the functional on any unit tile is at most p-s; signs can
only decrease that upper bound. On a side-k triangular grid its value
is at most k(p-s). Additivity now gives

\[
Mp\le(p-s)(S+A)
 =(p-s)(M+2D-q+A)
 \le(p-s)(M+2D+2A),
\]

which is the assertion. Atomizing contact segments makes every step valid
with T-junctions. No geometric pairing of an arbitrary tiling is assumed.

## Sharper form for every rational Group-1 beta target

Put a=uv, b=v²-u², c=v², with coprime integers 0<u<v. At scale t the
beta target has sides t(v³,v³,u(3v²-u²)), and M=t(u+v).
The checkerboard hypotheses hold by the angle inventories in the
[matching argument](checkerboard-matching-limit.md).

Here the stronger conclusion is

\[
\boxed{D+A\ge\frac{t(v^2-u^2)}{2v}.}
\]

Indeed, write the tile angles as alpha,beta,gamma, with
3alpha+2beta=pi and gamma=2alpha+beta. The cosine law gives
2 cos(alpha)=2-u²/v² in (1,2). If alpha/pi were rational, this rational
number would be an algebraic integer, hence an integer, a contradiction.

Modulo sign and pi, the tile's edge-direction gaps are alpha,beta,gamma;
the target's are beta,beta,3alpha. Their only common gap is beta: every
other equality, after substituting beta=(pi-3alpha)/2 and
gamma=(pi+alpha)/2, would make alpha/pi rational. If two tile edges
align with target directions, they are therefore a,c and the b-edge
is omitted. If at most one aligns, the total aligned length is at most
a+c, also by the triangle inequality. Replace p-s by a+c=p-b in the
preceding proof, and use a+c=v(u+v), to obtain the displayed bound.

For A=0, at least one white-boundary triangular grid is required. If
there are at most K such grids, their combined number of tiles is at
least D²/K, hence at least t²b²/(4v²K). For a fixed tile and fixed K,
these blocks must therefore occupy an amount of area proportional to
t². A bounded collection of exceptional unit tiles cannot replace them.

This does **not** refute the proposed grid grammar: white-boundary grids
were already allowed. It rules out a narrower attempted proof in which
all large grids have black boundaries and only a bounded number of unit
tiles handle the remaining geometry.

## Exact outstanding obligation

The next global lemma to investigate is the existence of an absolute
orientation bound for some witness of every tileable pair (R,T). A
counterexample must establish a lower bound over all alternative tilings;
a proof must accommodate arbitrary T-junctions and reflected tiles.
Neither that bound nor bounded block complexity is established here.

The [orientation reduction audit](orientation-reduction-audit.md) now
proves a bound of 24 for the classical branches, including a separate
[whole-hypotenuse parity argument](right-tile-orientation-bound.md) for
irrational right tiles. Its published inputs are stated explicitly.
It also proves a restriction on orientation cuts and identifies a false
arbitrary-patch replacement rule. These results do not establish the
universal bound or the finite-scheme conjecture.

The [whole-edge area argument](height-cut-area.md) proves that cut chains
are boundaries of actual nested tile unions, then uses their exact
rank-two displacement lattices. For every theta tiling with consecutive
parameters u=v-1, it bounds the number of rigid orientations by 8t².
The dependence on t remains. Replacing an arbitrary such union with a
tiling using fewer directions is still unproved; the chain identity
alone does not perform that replacement.

The [4 October continuation audit](audits/finite-schemes-2026-10-04.md)
records the scope corrections and the exact unresolved implication.
