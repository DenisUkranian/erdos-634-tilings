# Every W and beta scale passes the full formal direction-count system

7 October 2026. An explicit all-scale restatement of an existing
limitation theorem for position-independent additive boundary invariants.
The scale-one result, with the same sparse population counts and padding,
is already Theorem E in `../../uniform-reduction/PROOF.md`, Section 8.
The extension to arbitrary m is immediate by scaling its boundary
identity and adding half-turn pairs. This is not a new obstruction or a
construction of a tiling.

Let `0<u<v` be coprime, and put

    a=uv, b=v²-u², c=v², Q=2v²-u², P=3v²-u².

## Theorem

For every integer m>=1, both the W target with sides
`m(v³,uQ,vb)` and the beta-isosceles target with sides
`m(v³,v³,uP)` admit the following formal data:

* a nonnegative integer population of allowed oriented/reflected copies
  of the primitive tile;
* the exact required population size, respectively `Qm²` and `Pm²`;
* exact equality of the complete direction-labelled boundary sum of
  those copies with the direction-labelled outer boundary.

Thus no necessary test consisting solely of this formal direction
equation and the exact tile count can exclude any W or beta scale.
In particular, taking more linear functionals of this same equation
cannot close the missing scale-one or small-scale cases.

The formal data omit tile positions. No nonoverlap, connectedness,
seam incidence, or disk-development claim follows from them. The
population witness here and the separate side-word witnesses in
`BOUNDARY_FILTER_BARRIER.md` are not claimed to combine into one
globally compatible incidence system.

## Formal boundary module

Let gamma be the obtuse tile angle and let eta=exp(i gamma). Then

    cos(gamma)=-u/(2v),
    v eta²+u eta+v=0,
    a-b eta=c eta³.

The last identity follows by expanding

    a-bX-cX³ = -(vX-u)(vX²+uX+v).

The angle gamma/pi is irrational. Otherwise eta would be a root of
unity, and eta+eta^(-1)=-u/v would be both rational and an algebraic
integer, hence an integer, which it is not. In particular no two
powers eta^j have the same unoriented direction.

Use the formal Laurent variable X to label these directions. A vector
`r eta^j`, with real signed r, receives the signature `r X^j`.
The counterclockwise boundary of the tile `T=(0,a,b eta)` has signature

    f(X)=a-bX-cX³.

A translated, rotated tile `epsilon eta^h T` contributes
`epsilon X^h f(X)`, with epsilon in {1,-1}. A reflected tile contributes
`-epsilon X^h f(X^(-1))`, since reflection reverses the orientation of
the boundary. Thus any actual tiling supplies integer Laurent
polynomials U,V with

    B(X)=U(X)f(X)-V(X)f(X^(-1)).                 (1)

Interior edge subsegments cancel in this module, including at arbitrary
T-junctions. A signed coefficient in U or V is a difference between
two half-turn orientations; it does not mean a negatively counted tile.

Conversely, any particular integer U,V can be realized as a population
of `||U||_1+||V||_1` positive-count oriented copies: choose the half-turn
sign of each copy according to its coefficient. Their positions are
left unspecified. Adding any tile orientation together with its
half-turn adds two copies and zero formal boundary signature.

## W target: explicit inventory

The canonical vertices used in the cap construction can be written

    0, z=v³ eta², w=vb eta^(-2).

They satisfy `w-z=-uQ eta^(-1)`. Their counterclockwise order is
`0,w,z`, so the scale-m target boundary is

    B_W(X)=m(vbX^(-2)+uQX^(-1)-v³X²).

Set

    U_W=m(vX^(-1)-uX^(-2)),
    V_W=mvX.

Direct Laurent-polynomial multiplication gives the identity

    B_W=U_W f-V_W f(X^(-1)).                    (2)

Its positive orientation population has size

    n_W=m(u+2v).

This is no larger than the prescribed `N_W=Qm²`. Indeed, for
`1<=u<=v-1`, the quantity `2v²-u²-u-2v` decreases as u grows, so

    Q-u-2v >= v(v-1)>0.

Moreover

    Qm²-m(u+2v) = 0 mod 2,

because `Q=2v²-u²` and `k²=k mod 2` for every integer k. Add exactly
`(Qm²-n_W)/2` half-turn pairs to the population in (2). The result
has the exact required number of tiles and the exact formal boundary.

## Beta target: explicit inventory

Its canonical third vertex is

    z2=z+(P/Q)(w-z)=-v³ eta^(-4).

This identity follows from the same quadratic equation for eta. The
counterclockwise outer boundary therefore has signature

    B_beta(X)=m(-v³X²+uPX^(-1)-v³X^(-4)).

Set

    U_beta=m(vX^(-1)-uX^(-2)),
    V_beta=mv(X-X^(-1)).

Again direct multiplication gives

    B_beta=U_beta f-V_beta f(X^(-1)).            (3)

The sparse population now has size `n_beta=m(u+3v)`. It satisfies

    P-u-3v >= 2v(v-1)>0,

by the same monotonicity in u. Also

    Pm²-m(u+3v)=0 mod 2.

Add `(Pm²-n_beta)/2` half-turn pairs to obtain precisely `Pm²`
positive-count oriented tiles and the required formal boundary.

Equations (2) and (3), together with the padding, prove the theorem.

## Concrete controls and scope

For `(u,v,m)=(1,2,1)`, equation (2) uses five oriented copies, and one
half-turn pair raises the population to seven. Equation (3) uses seven
copies, and two pairs raise it to eleven. These are formal witnesses
for the classical impossible counts 7 and 11, not geometric tilings.
They illustrate exactly which information the relaxation discards.

For W56, the sparse count is sixteen and twenty half-turn pairs supply
the remaining forty copies. This formal population is not a proposed
placement of the 56 tiles.

The theorem does not rule out successful positional invariants,
noncommutative boundary arguments, area moments involving coordinates,
or complete global incidence certificates. It says that the full
position-independent additive direction equation, even with exact area
expressed as the required number of congruent copies, is always
feasible in both families.

## Reproducible algebra

`check_formal_direction.py` verifies equations (2) and (3) coefficient
by coefficient over the Laurent polynomial ring `Q[u,v,X,X^(-1)]`.
The common factor m is omitted in that symbolic calculation. Separate
integer regressions check population positivity, parity, and padding.
No geometric placement verifier is invoked or claimed.

The scale-one content is credited to the existing Theorem E, not newly
claimed here. The alternate normalization matches the formal-signature
method used for the parallelogram parity theorem in
`../../final-push-oct7/w/PARALLELOGRAM_PARITY_AND_CAP.md` and uses the
canonical W/beta targets in `../../w-beta-caps/PROOF.md`. It does not
use the candidate prime-case proof. This is an internally checked
restatement, with no claim of novelty, external priority or peer review.
