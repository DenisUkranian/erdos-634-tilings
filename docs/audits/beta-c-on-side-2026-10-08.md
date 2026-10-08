# Fresh audit of the beta reverse-apex reduction

8 October 2026. Research for Denis Paliy. This reviews the argument in
`docs/prime-case-candidate.md` through the extraction of its standard
corner and identifies exactly how it treats c/a relations and the two
base-corner orientations. It is an internal mathematical review, not
external acceptance, formal verification, or a new proof of all of 634.
Earlier files reporting PASS were not used as premises.

## Conclusion and scope

I did not find a missing implication in the reverse-apex extraction as
currently written. In particular, its induction does **not** require a
short c-chain to be opposed only by c-edges throughout its full range.
It allows c/a exchanges and needs only the exclusion of opposite b-edges.

This conclusion concerns the reduction of the scale-one beta target to
an actual W complement. The full beta nonexistence assertion still uses
the separate scale-one W argument (except for the special both-c-on-equal-
sides case discussed below). It does not make that candidate an accepted
result or certify its global published-classification dependencies.

## The relevant arithmetic really allows long c/a relations

Write

    a=uv, b=v²-u², c=v², 0<u<v, gcd(u,v)=1.

For a complete nonnegative whole-edge decomposition

    n c = A a + B b + C c,   0<n<v,

reduction modulo v gives B=v*ell. Put d=v-u. The length equation then
has the exact form

    A=v*h-d*ell,   n=C+u*h+d*ell.

If ell>0, A>=0 forces h>=1, and n>=u+d=v, a contradiction. Consequently

    B=0, A=v*h, C=n-u*h.

There can be a-edges when n>=u. For example `u c=v a` is explicitly
allowed. Only when n<u does the stronger c-only conclusion hold. The
reverse-apex induction uses the former no-b statement, not the latter
c-only statement. The W appendix uses c-only only after separately
proving its stricter bound n<u.

## Whole chains and maximality

For an actual maximal collinear component, each bank partitions the whole
component into whole tile edges. At an interior endpoint of an edge on
one bank, the other bank cannot supply the interior of a tile across the
supporting line: that would overlap the tile having the edge. The bank
therefore continues along the line. At a maximal endpoint, no constituent
edge can overrun, since it would extend the component. These statements
allow T-junctions; they do not assume matching endpoints between banks.

The argument also uses horizontal subsegments rather than maximal
components. Here the missing endpoint justification must be supplied
separately, and the current text does supply it:

* The left endpoint is on the supporting line of the outer equal side;
  a further horizontal extension leaves the convex target.
* In a reverse cap the right endpoint is interior to a crossing tile's
  edge on the diagonal. A positive horizontal extension enters that tile.
* In downward completion the hypothesized beta tile starts its whole
  horizontal edge at the right endpoint. The known region occupies the
  entire upper half-plane locally at every intermediate horizontal grid
  point. Thus that lower chain cannot stop at one of those grid points
  by allowing a tile to cross the line.

Accordingly the short-a lemma is being applied to a whole chain of length
m a, with m<v, and not to an arbitrary portion of an unbounded seam.

## Why the column induction is not circular

Fix the tiling throughout. The column M_m is the actual maximal component
from V_m downward; the positive q-ray is blocked by the tile crossing
the apex b-diagonal. Its upper endpoint is therefore V_m.

The reverse horizontal cap creates its first actual normal U tile and
whole c-edge. If the component continues from a reached point Z(m,t),
the two old left tiles leave exactly a beta sector on the left of the
continuing q-ray. Its beta tile has a or c on that ray.

Putting a there would put c on the horizontal ray to the left. The full
opposite horizontal chain would then have length m a and contain c,
contradicting short-a purity. Thus the left tile has c on the column.
The remaining horizontal lower row is forced using the same short-a
lemma and the exclusion of two gamma sectors in one half-plane.

At the interior alpha gaps, only columns M_i with i<m are used. A newly
supplied U edge is connected to the already actual upper segment of M_i.
Its no-opposite-b property therefore excludes the b-side version of
that alpha tile. If the new edge would extend M_i below a formerly
determined maximal endpoint, that is already a contradiction in the
fixed tiling. It is not permission to redefine M_i or an assumption
that all columns initially reach the base.

Every actual continuation of M_m thus adds a whole normal left c-edge.
Boundedness ends the component at Z(m,r), with r>=0 because negative q
height lies below the external horizontal base. Hence its total length is

    n c,  n=v-m-r,  0<n<=v-m<v.

Only **now**, after completing and bounding the actual component, does
the proof infer no b on its opposite bank. No no-b property of M_m was
used to establish its own downward completion.

## The exact point where c/a exchanges become harmless

At V_m the crossing tile contributes a straight angle, and the already
forced D and U tiles leave exactly one alpha sector on the right of
the downward q-ray. The two possible side lengths for an alpha tile
on that ray are b and c; **a is not an alternative**.

The newly proved no-b property of M_m therefore forces c and the next
diagonal D tile. The argument never concludes that all the other edges
on that opposite bank are c. It is consistent with c/a exchanges at
other places on the bank, insofar as subsequent geometry allows them.

Repeating the process reaches m=v-1, whose initialization reaches height
zero. The conditional completion property for the earlier columns then
gives the whole standard corner K_v; adding D(v-1,0) finishes its v²
tiles. No short-chain assertion at index v is invoked.

## Both base corners with c on the equal sides

The initial conditions do not choose either base-corner orientation.
They use the apex instead: its three alpha tiles have c on the external
equal sides, and the central alpha tile has one c and one b radial side.
Reflection lets the proof select the outer b edge opposed by the central
c edge. This is why no base-corner case is omitted at initialization.

After extraction, one base corner A is incident to the standard corner
K_v. It has c on the equal side AB and a on the original base AC.
The complementary triangle BLC has sides `(v³, v b, u(2v²-u²))`.
The following short deduction gives **no a-edge** on its side LC
without using the W nonexistence induction.

**Both-c-on-equal-sides corollary, conditional on the reverse-apex
extraction.** A scale-one beta tiling cannot have c on the equal side
at both of its base corners.

**Proof.** The three angles of BLC are beta, 2 alpha and
theta=alpha+beta, all strictly smaller than gamma. Its side LC must
therefore contain at least one c-edge: every boundary a- or b-edge has
a gamma endpoint, none can occur at the two target corners, and no
internal straight junction can accommodate two gamma angles.

Write the whole-edge counts on LC as A_0,B_0,C_0, with C_0>=1. Since
`|LC|=u(b+c)`, reduction of

    A_0 a+B_0 b+C_0 c=u(b+c)

modulo v gives B_0=u+v*k, with k>=0. Subtract u*b to obtain

    u c=A_0 a+v*k*b+C_0 c.

Here u<v, so the no-b statement already checked above forces k=0.
Its remaining solutions are

    A_0=v*h, C_0=u(1-h), h>=0.

Since C_0>=1, h=0. Thus `(A_0,B_0,C_0)=(0,u,u)`.

If the other original beta corner C also had c on its equal side CB,
its unique beta tile would have a on the original base CA, and hence
on LC. That contradicts A_0=0. ∎

Thus the
both-c-on-equal-sides configuration is included by the extraction and
then excluded; it is not assumed absent. This observation uses the
extraction and the elementary side-count argument, but not the W
nonexistence induction.

If “c on the side” refers instead to a different convention for naming
the two incident sides, it should be restated as the explicit equal-side
versus base distinction before comparing arguments.

## Appropriate statement to an external reader

The precise defensible claim is: the present candidate was designed to
cover both base-corner orientations; its reverse-apex step permits
`u c=v a` and other positive c/a exchanges, because it uses only no-b
for columns shorter than v c. A fresh review of those steps found no
gap, but the argument remains a candidate awaiting external assessment.
The old internal-review wording is not a substitute for that assessment.
