# Independent adversarial audit of the reverse-apex candidate

29 September 2026. Source audited:
the earlier draft of `docs/prime-case-candidate.md`, especially Sections 3–5.
This records an internal proof check, not external verification or
literature novelty. No counterexample or missing geometric implication
was found in the argument as stated.

## Exact hypotheses

The target is the scale-one beta triangle. Its equal sides have length
v c, its apex consists of three alpha sectors, and each equal side has
only a/c boundary edges. The argument uses actual complete tile-edge
components, convexity, and the previously proved short-a and short-b
lemmas. The final contradiction uses the W theorem (or, alternatively,
the base count theorem and localized c-prefix lemma). It makes no assumption that the equal sides
were c-grids at the outset.

The no-b equal-side hypothesis can also be recovered directly: a
boundary side with no c-edge would force two gamma endpoint angles at
some interior boundary vertex, because no target corner admits a gamma
tile angle. At a beta corner its fan is one beta; at the apex, the
irrational angle equation forces exactly three alpha sectors. This is
an angle-decomposition fact: the total apex angle 3alpha can exceed
gamma.
Every equal side therefore has a c-edge. The arithmetic for length v c
shows that any decomposition containing b must be exactly v b+u a,
which has no c-edge. Thus all equal-side boundary edges are a/c.

## Apex initialization

The three apex tiles all have alpha there. The two external apex edges
are c, since alpha is incident to b/c and the external sides have no b.
The central tile has one b and one c at its alpha corner. Relabeling
left/right therefore guarantees an outer b opposed to its c. Since
c>b, the first grid endpoint is strictly inside this actual opposite
edge. The positive q direction enters its interior and blocks the
upper end of the first column. No hypothetical ray is prolonged.

## Reverse horizontal caps

At an interior horizontal cap junction, the supplied T region fills
the whole upper straight sector. This follows from its D/U index
conditions, including the near-diagonal endpoint cases. Thus the lower
side really is a complete chain of whole tile edges, rather than a
chain that can stop at a grid vertex.

The cap endpoints are blocked by the external supporting line and the
actual crossing tile. Its length m a with m<v forces all lower edges
to be a. At the right endpoint the remaining sector is theta<gamma,
so the a-tile has beta there. Consecutive gamma exclusion then forces
the entire normal U row from right to left. This orientation argument
works for both a<b and a>b.

At the external end, the old beta and new gamma leave alpha; absence
of external b forces the normal D. At every interior gap the upper
straight sector and the two new U angles leave exactly alpha.

## Earlier-column use is legitimate

The new left U supplies a real downward c-edge on M_i, attached to its
already actual upper component through T. Since i<m, the complete
component's no-opposite-b property has already been established.
This excludes the b-on-q realization of the alpha gap and forces D.
There is no call to completion of column m to prove itself.

If an earlier maximal component had ended before this forced edge,
the newly forced extension would itself contradict maximality. One
cannot discard the edge, but this is a contradiction case, not a gap.

## Downward continuation

At X=Z(m,t), the two old left tiles contribute gamma+alpha=pi-beta.
If the actual component continues downward, its left side therefore
has exactly one beta tile. This follows from the irrational angle
equation; several smaller tile angles cannot replace beta.

Putting a on its q-ray would put c on the left horizontal ray. The
actual upper horizontal chain from t q to X fills the upper straight
sector at all its internal points, so the lower side must be a full
chain from X to the external side. It would have length m a and contain
c, contrary to short-a purity. Hence the downward edge is c and the
tile is the normal U. The entire next U row and then D row are forced
exactly as in the initialization.

Every continuation adds a complete c-edge. A maximal component cannot
end strictly inside that edge. Boundedness therefore ends it at an
integer grid height r>=0, and its length is n c with
0<n<=v-m<v. The arithmetic in Section 1 is correct: any b count is
v ell, and ell>0 forces n>=v. Thus the opposite side has no b, even
though compensation by a-edges is allowed. This is exactly the weaker
property required in the subsequent alpha fans.

## Diagonal advance and final geometry

At V_m, the crossing tile's straight sector, old D gamma, and first U
beta leave exactly alpha on the right of the downward q-ray. The newly
classified M_m excludes b there, so c forces the next D and advances
the actual b diagonal.

For m<v-1, short-b purity forces the next endpoint to remain strictly
inside an actual opposite edge. At the final m=v-1 step no short-b
statement at index v is invoked: its forced D merely reaches the base.
The initialization of this last column reaches height zero, supplies
T(v-1,0), and the last D completes the actual standard K_v.

The simplest final step removes this actual K_v from the tiling. Its
complement is exactly the scale-one W triangle, with side lengths
v c, v b, and u(2v²-u²), and with 2v²-u² tiles. The already audited W
theorem excludes it. No additional base count theorem or c-prefix
lemma is required for this reduction.

The original candidate's alternate last step is also valid: the
target base starts with v a-edges; the boundary count theorem forces
k=0 and exhausts all a-edges in this prefix. From the other beta corner
there is a nonempty pure c-run followed by b, of at most u edges. The
localized c-prefix lemma excludes it. Its strict incident-length bounds
hold for this target.

## Assessment

The reverse-apex argument passes this independent internal audit and,
together with the already audited W theorem, excludes the full
scale-one beta family. It does not classify composite tilings of larger scale.
Any global prime or squarefree consequence must retain the separate
classification and parameterization dependencies that put an arbitrary
candidate into this family.
