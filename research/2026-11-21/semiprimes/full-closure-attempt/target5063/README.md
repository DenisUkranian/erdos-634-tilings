# A unique empty-remote native profile at 215, and an exact relaxation witness

21 November 2026. **Neither 5063 nor 3431 is excluded.**

This note sharpens one restricted part of the surviving 5063 mode and
records an exact limitation of that sharpening. The unrestricted target,
the other one/two/four-cell configurations, and larger odd populations
remain open.

## 1. Precisely stated physical hypothesis

Use the path frame for `(a,b,c)=(35,13,43)`, with
`z=(a+b*rho)/c`. Suppose all 215 odd tiles lie in the native height-one
class `zR`, and every remote even child gate is **empty**. Equivalently,
under the already proved height support `{0,1,2}` in this mode, suppose
that all height-zero tiles belong to `R` and all height-two tiles to
`z^2R`.

The hypotheses concern actual occupied nodes. A remote gate having signed
current zero does not imply that it is empty. A balanced occupied branch
must not be silently removed.

At a nonnative long-side gate, all banks of the maximal supporting runs
then contain only height-one long sides of length `c`; there is no outer
edge or neighboring short edge in that gate. The common finite run is
partitioned into equal lengths on both banks, so each tile has its actual
whole half-turn mate. There are no other odd heights here, which is
essential for obtaining a mate at the same short height. General T-junctions
are still allowed elsewhere.

For a normalized tile `(q,j,s)`, with

\[
 u=q-aU_j,\quad w=q+bU_{j+s},\quad
 \epsilon=s(-1)^j,
\]

the mate has labels

\[
 q'=u+w-q,\qquad j'=j+3\pmod6,\qquad s'=s.
\]

It has the same long side and gate and opposite sign. Therefore the
periodic multiplicities of each such pair agree, a stronger condition
than a zero scalar gate current.

## 2. Exact single/pair inequality

The complete residue catalogue contains 22,188 tile types. Leave the 516
native-gate types as single columns and merge the other types into their
10,836 unordered half-turn pairs.

The integer certificate
[`EMPTY_REMOTE_EXACT_DUAL_5063.json`](EMPTY_REMOTE_EXACT_DUAL_5063.json)
contains three endpoint tables and gate weights. Each native single has
score at most 13, and each remote pair has score at most 26. The complete
endpoint currents vanish; all remote gate currents vanish because they
are paired. The weights of the two native currents are 83 and -3.
Consequently, for any population satisfying this necessary projection,

\[
 \boxed{13n_{\rm odd}\ge83Q_+-3Q_-.}                 \tag{1}
\]

The normalized isometry `w -> -conjugate(w)` preserves the sign and
exchanges the two hands. It preserves the native gate and maps nonnative
gates to nonnative gates. Applying (1) to the transformed columns gives

\[
 \boxed{13n_{\rm odd}\ge83Q_--3Q_+.}                 \tag{2}
\]

For a hypothetical full tiling under Section 1, the complete native cut
identities give

\[
 Q_+=86+22e,\qquad Q_-=-43-22e,\qquad e\in\mathbb Z.
                                                               \tag{3}
\]

These are the previously established native charge transport equations,
with every remote branch empty. They do not assume that the native even
nodes have zero charge.

At `n_odd=215`, equations (1)--(2) and `Q_++Q_-=43` imply

\[
 Q_+\le\left\lfloor\frac{13\cdot215+3\cdot43}{86}\right\rfloor=34,
 \qquad Q_-\le34.
\]

Hence `9<=Q_+<=34`. Its congruence in (3) leaves exactly one value:

\[
 \boxed{Q_+=20,\qquad Q_-=23,\qquad e=-3.}           \tag{4}
\]

In particular the formerly convenient profile `(42,1)` is impossible
under the empty-remote hypothesis at 215. It would require

\[
 n_{\rm odd}\ge\frac{42\cdot83-3}{13}
              =\frac{3483}{13}>215.
\]

**This does not exclude all native 215 configurations.** The profile
in (4) is different and survives the stronger continuous projection,
as certified next.

## 3. An exact positive rational witness for the remaining profile

[`EMPTY_REMOTE_RATIONAL_215_5063.json`](EMPTY_REMOTE_RATIONAL_215_5063.json)
gives a nonnegative rational solution of the entire single/pair model,
with

\[
 n_+=129,\quad n_-=86,\quad Q_+=20,\quad Q_-=23.
\]

The independent checker verifies every one of the 5,547 periodic endpoint
rows, all 86 gate rows, both sign totals, and all 10,836 remote mate
equalities. It also checks strict positivity of all 22,188 expanded tile
columns.

The certificate stores a sparse positive rational point in the merged
single/pair variables and a positive rational coefficient `kappa` of the
uniform whole-column kernel. Adding that kernel makes the total exactly
215 while preserving every endpoint row, gate current, and remote mate
equality. It does not change the signed charge.

The sparse point was discovered by linear optimization. Its support was
reconstructed with exact rational elimination: 2,887 unit pivots followed
by an 80-variable rational remainder. The saved point and all its
asserted properties are rechecked using only Python integer/Fraction
arithmetic; no solver status is used as proof.

**The tile coefficients are rational, not nonnegative integers.** The
point supplies neither actual transverse line coordinates, containment,
nonoverlap, a compatible even filling, nor a full tiling. It proves only
that no linear inequality valid for this precise strengthened continuous
projection can exclude the remaining profile at population 215.

A separate exact witness,
[`EMPTY_REMOTE_SIGNED_INTEGER_215_5063.json`](EMPTY_REMOTE_SIGNED_INTEGER_215_5063.json),
represents the same profile and sign totals by **signed integer** single/pair
coefficients. It has 949 negative group coefficients. All rows and mate
equalities are checked independently. Thus an extra linear congruence in
this particular paired projection cannot exclude the remaining profile
either. This is not a characterization of its entire integer image.

The two witnesses solve different relaxations: the rational one is
strictly positive but fractional; the integer one has negative
coefficients. Neither supplies a **nonnegative integer** solution. A
direct nonnegative-integer probe reached its limit without an incumbent;
that status is not an infeasibility certificate.

## 4. Positive control and reproducibility

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/target5063/verify_empty_remote_profile.py
```

The checker is independent of the discovery matrix builder. It constructs
all oriented columns and the mate involution directly, checks the integer
dual inequalities, and verifies the explicit rational point.

It also transforms the existing complete 143 tiling into the native path
frame. Its 105 odd tiles have native currents `(14,-7)`, and every remote
long tile has its actual mate: there are 42 remote whole pairs. Thus the
pairing condition preserves this genuine positive control. The result is
[`EMPTY_REMOTE_PROFILE_REPLAY.json`](EMPTY_REMOTE_PROFILE_REPLAY.json).

The physical reductions use the existing
[native current law](../../global-closure-next/large-population/GLOBAL_ODD_BRANCH_BUDGET.md)
and the
[five-block height classification](../../global-closure-next/five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md).
The old [native two-height gate proof](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/NATIVE_GATE_BOUND.md)
contains the same equal-length-bank reasoning under its stated,
different hypotheses; its numerical bounds are not imported here.

## 5. Audited limits of monochromatic shortcuts

The extremal variation `V=77` in the preceding global bank theorem would
make every odd cell monochromatic. Two tempting universal shortcuts for
eliminating this endpoint are false under actual-cylinder closure alone.
For the primitive control `(5,3,7)`, this package supplies exact finite
nonoverlapping packings consisting entirely of positive tiles, at
populations 21, 35, and 56. Every actual supporting-line cylinder row
vanishes. Their charge units are 3, 5, and 8.

Thus a proposed universal bound `n>=c^2` fails already at 21 and 35.
The proposed charge semigroup `g in <3,c>` fails at 5 and 8; in particular
`g=5<c=7` need not be divisible by three. These are **mixed-hand**
monochromatic packings. Mandatory neighboring-bank compatibility and
containment in either target board are not asserted.

A separate signed periodic one-hand kernel at `(5,3,7)` has total
multiplicity seven, with 41 negative coefficients. It refutes a universal
`c^2` divisibility statement for the signed one-hand image. It does not
refute a positivity or physical lower bound for one-hand packings.

The controls do not settle the analogous target-specific conjectures at
37 or 43. They prevent promoting these unrestricted shortcuts to proofs.

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/target5063/verify_monochromatic_controls.py
```

The checker independently tests all endpoint rows and 2,345 exact triangle
separations. Coordinates and formal coefficients are in
[`MONOCHROMATIC_COUNTERCONTROLS.json`](MONOCHROMATIC_COUNTERCONTROLS.json),
with replay in
[`MONOCHROMATIC_CONTROL_REPLAY.json`](MONOCHROMATIC_CONTROL_REPLAY.json).
