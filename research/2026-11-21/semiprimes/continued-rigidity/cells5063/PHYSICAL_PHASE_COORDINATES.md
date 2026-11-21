# Physical coordinates for the remaining 5063 cell constraints

21 November 2026. This note audits the coordinate transfer needed to use
the established one/two/four-cell classification in an actual-placement
search. It supplies necessary population caps, not a finite tiling or an
infeasibility certificate. **5063 remains open.**

Let `rho=exp(i*pi/3)`, `R=Z[rho]`, `(a,b,c)=(35,13,43)`,
`z=(a+b*rho)/c`, `A=b(2a+b)`, and `B=a(a+2b)`. Under the complete
`n_odd=215` hypothesis, all short heights are 0, 1, or 2, and the
common vertex ideal is

\[
 I=(z/c)R.
\]

This is a proved envelope from the
[one-height classification](../../global-closure-next/global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md),
not an imposed coordinate cutoff.

## 1. Standard coordinates, native class, and the two phase labels

The standard-to-path isometry is

\[
 F(w)=Bz^2-\rho z^2\overline w.
\]

Direct multiplication gives `F(A)=c^2`. Moreover `c^2 in zR`, so the
path-frame native class `zR` pulls back to the standard-frame class

\[
 \boxed{A+zR.}
\]

For a standard-frame vertex or obtuse anchor `q`, put

\[
 U=(c/z)(q-A).
\]

Since `A in I`, membership `q in I` is exactly `U in R`. Write
`U=u+v*rho` and define

\[
 \phi(U)=av-bu\pmod c,\qquad
 \psi(U)=au-bv\pmod c.                       \tag{1}
\]

The determinant of this map on `R/cR` is `b^2-a^2=19 mod 43`, which
is nonzero. Thus the ordered pair `(phi,psi)` gives all `43^2=1849`
joint phase classes without duplication. The two native exact-node
labels are zero, and the joint native cell has `(phi,psi)=(0,0)`.

For the path-frame coordinate `U_path=(c/z)F(q)`,

\[
 U_{\rm path}=c^3/z-\rho\overline U.
\]

The first term is divisible by `c` in `R`. In axial coordinates
`-rho*conjugate(u+v*rho)=(-v,-u)`, so

\[
 \boxed{\phi(U_{\rm path})=-\psi(U),\qquad
        \psi(U_{\rm path})=-\phi(U)\pmod c.}       \tag{2}
\]

The two trees swap, with a harmless sign change in their nonnative
labels. Native label zero remains zero. The isometry sends
`(h,j,s)` to `(2-h,4-j,-s)`, so it preserves short-height support
`{0,1,2}` and reverses the tile sign `epsilon=s*(-1)^j`.

In particular the path sign inventory `(129,86)` becomes standard
inventory `(86,129)`. Balanced cells stay balanced. The charged entry
`(43+x,x)` in the path-frame four-cell matrix becomes `(x,43+x)`.

## 2. Tile vertices remain in the envelope

For `h=0,1,2`,

\[
 (c/z)z^h=\overline{a+b\rho},\quad c,\quad a+b\rho,
\]

respectively. These are elements of `R`. Thus a physical tile whose
anchor belongs to `I` has all three vertices in `I` at each allowed
short height. At height one the vertex differences are in `zR`,
so all its vertices have the same pair of phase labels (1).

The converses required by an incident search are exact: an anchor
outside `I` cannot belong to a tiling in this proved regime, and a
height-one tile cannot change cells by choosing another of its
vertices as a coordinate reference. No floating tolerance is used.

## 3. How complete population restrictions apply to partial selections

Every complete 215-odd configuration occupies the native exact node
in both trees. Each tree has either one occupied node of size 215, or
one balanced 86-tile node and one charged 129-tile node. Consequently there is
at most one occupied nonnative label in either tree.

In a search with a partial set of selected actual tiles, these are
**upper caps from one common complete skeleton**. For example, in
the four-cell case and standard signs, the cap matrix is

\[
 \begin{pmatrix}
 (x,x)&(43-x,43-x)\\
 (43-x,43-x)&(x,43+x)
 \end{pmatrix}.                                  \tag{3}
\]

The first row and first column are the balanced 86-tile nodes; their
native/non-native status is chosen independently. A valid necessary
model chooses one common value of `x` and one common assignment of
phase labels for all caps. Each selected positive or negative count
must be at most its corresponding entry. Equality is required only
after the entire odd population is selected; it must not be imposed
on a partial placement pool.

Likewise an unoccupied native node in the current partial selection
does not contradict eventual native occupancy. New columns may fill
that node. A complete incident row, however, must include every
candidate satisfying the established height and ideal envelope, with
population exclusions justified by the same global skeleton.

## Exact coordinate replay

`verify_phase_coordinates.py` checks the Eisenstein arithmetic,
both board-frame constants, all 1849 phase representatives, the
native equivalence, label swap (2), all allowed vertex increments,
and every old four-cell matrix with standard/path sign transfer.
These checks audit the coordinates and finite caps. They do not
enumerate placements or prove that any skeleton is geometrically
realizable.
