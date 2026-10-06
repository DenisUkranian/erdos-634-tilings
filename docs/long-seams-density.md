# Long one-type seams and the density question

Denis Paliy, research with ChatGPT assistance.

**Provenance:** the geometric lemmas and qualitative density-zero argument
were written in the project manuscript of 1 October 2026. This is their
repository integration after fresh internal audits on 6 October, not a claim
to have discovered them on that date. The archive was previously distinguished
from the weaker published concentration theorem in the
[3 October review](audits/research-2026-10-03.md) and
[4 October review](audits/finite-schemes-2026-10-04.md).

The arguments below allow arbitrary T-junctions. They establish necessary
scale bounds, not existence at every scale and not a full solution of
Erdős problem 634. Their new quantitative consequence is proved separately
in [the counting theorem](quantitative-density.md). No external referee
acceptance, proof-assistant verification, or priority is claimed.

The source-to-relation argument is a length-sensitive use of Laczkovich's
established directed-graph method, also developed by Beeson. The geometry
is proved here rather than inferred from finite regression. The angular
classification and rationality remain the explicit published inputs [BZ].

## 1. The two geometric inequalities

### Theorem 1: geometric lower bounds for the scale

**Theta branch.** Let
\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\qquad 0<u<v,\quad\gcd(u,v)=1.
\]
The tile angles satisfy \(3\alpha+2\beta=\pi\); put \(\theta=\alpha+\beta\). If the theta-isosceles target, with sides
\[
(tbv,tbv,tbu),
\]
is tiled by this tile, then
\[
\boxed{tb\ge uv.}\tag{1.1}
\]

**Double-angle branch.** Let
\[
a=u^2,\quad b=v^2-u^2,\quad c=uv,
\quad 0<u<v<2u,\quad\gcd(u,v)=1.
\]
The tile angles are \((\alpha,\beta,2\alpha)\). If its isosceles target, with sides
\[
(tbu,tbu,tbv),
\]
is tiled by this tile, then
\[
\boxed{tb\ge u^2.}\tag{1.2}
\]
Here the common integer-scale necessity, proved below using the earlier two-character argument, gives \(t\in\mathbb Z_{>0}\) and \(N=bt^2\) in either branch. Both inequalities are necessary only; their satisfaction is not a construction.

## 2. Normalization and the integer scale

The external geometric inputs are the exhaustive angular classification of Laczkovich and the rationality theorem consolidated in Beeson–Zhang [BZ, Table 1 and Theorem 1.2]. They apply after separating similar-tile, right-tile, and rational-angle cases. Their classical counts are contained in
\[
\{r^2,r^2+s^2,2r^2,3r^2,6r^2:r,s\in\mathbb Z_{>0}\}.
\]
The familiar square cases include zero-square variants. The other relevant tiles have primitive integer sides after a common normalization. No claim is made here to reprove the angular classification or rationality theorem.

For the theta branch, rationality and the sine law yield the primitive tile \((uv,v^2-u^2,v^2)\), and the target has primitive proportions \((v,v,u)\). For the double-angle branch they yield \((u^2,v^2-u^2,uv)\), with target proportions \((u,u,v)\). These parametrizations and the other count spectra were established in the earlier uniform-reduction note [U].

Every exterior target side is a union of whole tile edges, because the target is convex. Thus all exterior lengths are integers. Since \(\gcd(u,v)=1\), the target is a positive integer scale \(\lambda\) times its primitive proportions. Area comparison gives \(N=\lambda^2/b\).

Here is the two-character refinement, included because integrality of t is essential to the summation in Section 5. In the direction group \(n\eta+j\pi\), \(\eta/\pi\) irrational, use the characters
\[
f(n\eta+j\pi)=(-1)^j,\qquad
 g(n\eta+j\pi)=(-1)^{n+j}.
\]
Sum edge length times the character around a counterclockwise boundary. Contributions of opposite internal subsegments cancel, including at T-junctions. Rotating or reflecting a tile changes each normalized tile value only by a sign. Dividing the target value by the reference tile value therefore gives integers U,V with
\[
U\equiv V\equiv N\pmod2.\tag{2.1}
\]
Connectivity across positive-length tile contacts propagates a single direction group throughout the tiling; a generic connecting path avoids the finitely many vertices.

In the theta case take \(\eta=\gamma=(\pi+\alpha)/2\). The reference values are
\[
b+c-a=(v-u)(2v+u),\qquad b+c+a=(v+u)(2v-u).
\]
The target values are \(\lambda(u+2v),\lambda(u-2v)\), respectively, so
\[
U=\frac{\lambda}{v-u},\qquad V=-\frac{\lambda}{v+u}.
\]
Their integer half-sum and half-difference are \(\lambda u/b\) and \(\lambda v/b\).

In the double-angle case take \(\eta=\alpha\). A reference tile has edge directions \(0,3\alpha,\pi+\alpha\), and its values are
\[
c+a-b=(2u-v)(u+v),\qquad c-a+b=(v+2u)(v-u).
\]
The target edge directions are \(0,\pi-\alpha,\pi+\alpha\), giving normalized values
\[
U=-\frac{\lambda}{u+v},\qquad V=\frac{\lambda}{v-u}.
\]
Again the half-sum and half-difference give \(\lambda u/b,\lambda v/b\in\mathbb Z\). Bézout now implies \(b\mid\lambda\) in both branches. Write \(\lambda=bt\); then
\[
N=bt^2,\qquad t\in\mathbb Z_{>0}.\tag{2.2}
\]
No integer length assumption on partial interior edges was used in this argument.

## 3. A boundary source must reach a whole-edge relation

This is a length-sensitive application of Laczkovich's directed graphs, not a new invention of the graph method. The definitions below retain left-maximality and actual whole-edge endpoints to avoid a false truncation at a T-junction. Compare [I, Section 6 and Lemmas 10.5–10.6].

Fix one side label x of a scalene tile; call the other two labels y,z. An x-incidence at a tile vertex means that one of that tile's two incident sides has label x. It contributes one, never two. Assume the following property:

**Even-fan hypothesis:** every possible collection of tile angles whose sum is pi has an even number of x-incidences.

A mismatch ray is an internal ray starting at a genuine vertex of each of its two adjacent tiles, with an x-edge on one side and a non-x edge on the other. Call its start protected if the backward ray is outside the target or enters the interior of a tile. A protected start is the left endpoint of the relevant maximal connected straight component of the edge skeleton.

### Lemma 3.1: source-to-relation lemma

If there is a protected mismatch ray starting on the target boundary and the even-fan hypothesis holds, then the tiling contains a segment of length at most the target diameter which witnesses
\[
nx=A x+B y+C z,\quad n\ge1,\quad A,B,C\in\mathbb Z_{\ge0},\quad B+C>0.\tag{3.1}
\]
Both sides of that segment are chains of whole tile edges.

**Proof.** Assume there is no segment witnessing (3.1). Start from any protected mismatch ray. Follow consecutive whole x-edges on its x-side until that side changes label, or the straight component ends.

An endpoint of one of these x-edges cannot also be an endpoint in the opposite side's partition: the segment from the protected start to that common endpoint would have whole-edge chains on both sides, including the initial non-x edge on the opposite side. It would be exactly (3.1). This observation also ensures that, whenever needed, the *whole* initial opposite edge has been counted, rather than just a portion of it.

Consequently the maximal x-run must end at a point Q strictly inside an opposite tile edge. The component cannot end there, since the opposite edge continues. On the x-side, the next tile along the straight line has a non-x edge. Call the directed segment from its protected start to Q a link.

At Q the opposite tile fills a half-disk, and all tiles with vertices on the other side form a pi-fan. Exactly one of the fan's two boundary half-rays has label x. By the even-fan hypothesis, an odd number of the x-incidences lie on internal rays. Incidences paired x/x contribute two. Therefore at least one internal ray is x/non-x. Its backward ray enters the spanning tile, so its start is protected. It produces an outgoing link by the same construction.

A point Q can have at most one incoming link. A link head is in the strict interior of a single spanning tile edge; two different supporting lines through it would enter that tile. Of the two directions along the unique line, only one approaches from the x-run, since the outgoing half-ray on that same side is non-x. The left-maximal starting point along the remaining direction is uniquely determined by the skeleton. Thus the indegree is at most one.

No link can end on the exterior boundary. At a flat exterior point a spanning tile on the supporting line already occupies the entire available half-disk; the other side cannot contain the required supported fan. At a target corner there is no spanning tile edge. Equivalently, a link and its straight continuation must lie internally on both sides of its head, impossible at a boundary point of a convex target.

There are finitely many links: every endpoint is a tile vertex, and the tiling is finite. In the finite directed graph of all such links, every vertex with indegree one has outdegree at least one, vertices of indegree zero have nonnegative outdegree, and the assumed boundary source has indegree zero and positive outdegree. Summing outdegree minus indegree gives a strictly positive number. Every directed link contributes zero to that total, a contradiction. Therefore (3.1) exists. As the segment is contained in the target, its length does not exceed the diameter. QED.

### Two elementary ways to obtain a boundary source

At a straight boundary junction between an x-edge and a non-x edge, the even-fan hypothesis gives an internal mismatch ray by the same parity argument. Its backward ray leaves the convex target.

At a target corner, if both incident exterior edges are non-x but the corner fan has an odd number of x-incidences, an internal mismatch ray again exists. A ray strictly inside a corner of angle less than pi has its backward ray outside the target.

These arguments concern actual tile edges emanating from a vertex. They do not treat a tile merely touching a boundary by its vertex as an exterior edge. They do not forbid partial-edge contacts elsewhere.

## 4. Applying the graph and bounding its length

### 4.1 Theta: use a-edges, not b-edges

In the theta family,
\[
\beta=(\pi-3\alpha)/2,\qquad \gamma=(\pi+\alpha)/2.
\]
Also \(2\cos\alpha=2-u^2/v^2\) is a rational number strictly between 1 and 2. If \(\alpha/\pi\) were rational, that rational number would be an algebraic integer, hence an integer. Thus \(\alpha/\pi\) is irrational.

Writing the angle inventory of a pi-fan as \((p,q,r)\) gives
\[
q+r=2,\qquad 2p-3q+r=0.
\]
The only nonnegative solutions are
\[
(1,1,1),\qquad(3,2,0).
\]
An a-edge is incident precisely to a beta or gamma angle, so both fans have exactly two a-incidences. The even-fan hypothesis holds for a. It need not hold for b; this parity argument must not be applied indiscriminately to a different edge label.

At the apex alpha there is one alpha tile, hence neither of its incident exterior edges is an a-edge. At a theta corner there is one alpha and one beta, hence exactly one a-incidence. These inventories follow by the same irrational-coefficient comparison.

Suppose some target side contains both a and non-a edges. At a transition there is a boundary source; Lemma 3.1 supplies a nontrivial a-relation. Otherwise each side is either pure a or contains no a. Both equal sides are non-a because their apex edges are non-a. If the base also has no a, either theta corner gives a boundary source. The sole remaining possibility is a base made entirely of a-edges.

A pure-a base satisfies \(tbu=k uv\); since \(\gcd(b,v)=1\), it forces \(v\mid t\). Then \(tb\ge vb>uv\), because \(b\ge2v-1>u\). Thus (1.1) already follows in that exceptional boundary case.

Otherwise we have an actual whole-edge relation
\[
n a=Aa+Bb+Cc,\qquad B+C>0.
\]
We record the short-a arithmetic (already present in [U] and the project's c-relation audit). Put j=n-A>0. Reduction modulo v forces \(B=v\ell\), so
\[
ju=\ell(v^2-u^2)+Cv.
\]
Modulo u this gives \(\ell v+C=uh\), and substitution gives \(j=vh-u\ell\). Nontriviality and v>u imply \(h\ge\ell+1\), hence
\[
j\ge v+(v-u)\ell\ge v.
\]
Therefore n>=v, sharply, since \(va=uc\). The witnessed segment has length at least \(va=uv^2\). The diameter of the theta target is tbv. Thus \(tbv\ge uv^2\), which is (1.1). QED.

### 4.2 Double angle: use c-edges

Here \(\beta=\pi-3\alpha\), \(\gamma=2\alpha\), and \(2\cos\alpha=v/u\in(1,2)\) again proves irrationality of \(\alpha/\pi\). The pi-fan equations are
\[
q=1,\qquad p+2r=3,
\]
so the two possibilities are
\[
(1,1,1),\qquad(3,1,0).
\]
A c-edge is incident at alpha or beta, giving two or four c-incidences. The even-fan hypothesis holds. This particular continuation parity is also Beeson's Lemma 10.5 [I]; essential c-segments are established there in Lemma 10.6. We give the following independent boundary case split to keep the length argument self-contained.

The base, between the two alpha corners, must contain a c-edge. Otherwise every boundary a- or b-edge contributes one gamma endpoint. No gamma fits either alpha corner, and the pi-fan inventory allows at most one gamma at an internal straight junction. A side with k edges would then require k distinct internal junctions, though it has only k-1.

If any target side mixes c and non-c, Lemma 3.1 supplies a c-relation. If no side mixes them, the base must be pure c. Its length gives \(tbv=k uv\), so \(u\mid t\) and \(tb\ge ub>u^2\), since b>=2u+1. Hence (1.2) follows in this pure-boundary case.

For a nontrivial c-relation cancel the c-edges common to its two chains:
\[
j uv=A u^2+B(v^2-u^2),\quad A+B>0,\quad j>0.
\]
Modulo u, \(B=u\ell\). Dividing by u and then reducing modulo v gives
\[
A=\ell u+vk,\qquad j=\ell v+uk
\]
for an integer k. If ell=0, nontriviality forces k>=1, and j>=u. If ell>=1 and k>=0, j>=v>u. If k=-h<0, nonnegativity of A gives \(\ell u\ge vh\), so \(\ell\ge h+1\) and \(j\ge v+h(v-u)>u\). Thus the original pure-c chain has at least u edges. The threshold is sharp because \(uc=va\).

Its length is at least \(uc=u^2v\), while the target diameter is tbv. This proves (1.2). QED.

## 5. The previously derived qualitative consequence

Both inequalities imply `u² <= tb`, where `b=v²-u²` and `N=bt²`.
Consequently, writing `b=(v-u)(v+u)=rs`, both positive factors are at most
`2 sqrt((t+1)b)`. For each fixed positive integer `t`, coefficients with
`bt²<=X` lie in a multiplication table of side `O_t(sqrt(X))`.
Erdős's qualitative multiplication-table theorem says that this table has
`o(X)` distinct products. The distinction between products and factor pairs
is essential.

The union over scales `t>K` has at most

$$
\sum_{t>K}\lfloor X/t^2\rfloor\le X/K
$$

counts. First taking `X` to infinity for fixed `K`, then taking `K` to
infinity, gives density zero for the union of both isosceles branches.
The [uniform-sectors theorem](../research/uniform-sectors/PROOF.md),
Section 5, had already shown that all other branches together have density
zero. Thus the archived combination gives `S(X)=o(X)` for all triangle
counts, with its exhaustive-classification and integer-spectrum inputs.

The [6 October quantitative continuation](quantitative-density.md) supplies
a stronger uniform bound and repeats the complete thirteen-row bookkeeping.
Neither statement decides every number in the remaining sparse set.

## Sources and archive record

- **[BZ]** M. Beeson and Y. X Zhang, *Rationality of certain triangle tilings*,
  [arXiv:2604.01314v1](https://arxiv.org/html/2604.01314v1), Table 1 and
  Theorem 1.2. The classification there is credited to Laczkovich.
- **[I]** M. Beeson, *Tilings of an Isosceles Triangle*,
  [arXiv:1206.1974v7](https://arxiv.org/html/1206.1974v7), Section 6 and
  Lemmas 10.5–10.6, for the graph-method precedent. The particular
  protected-source and length argument used here is explicitly proved above.
- **[U]** [Uniform finite reduction](../research/uniform-reduction/PROOF.md)
  and [sharp arithmetic edge thresholds](../research/c-relations/audit.md),
  with their original source attributions.
- **Multiplication-table input:** the qualitative result is due to Erdős;
  the quantitative version and attribution are stated on the first page of
  K. Ford's [author-hosted paper](https://www.ford126.web.illinois.edu/wwwpapers/hxy2y.pdf).

The integrated source is `Erdos634_density_zero_PROOF_2026-10-01.md`,
SHA-256 `a14e360d81efceade8607160ee4f0988447c197c196581a30f55db0d2991b9d4`. This note retains the geometric proof and qualitative
deduction; the archive's separate finite checks and `4p` exclusion are not
claimed to have been re-run or imported by this integration.
