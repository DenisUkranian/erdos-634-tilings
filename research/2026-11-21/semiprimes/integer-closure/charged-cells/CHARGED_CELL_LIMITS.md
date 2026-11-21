# What rigid charged-cell bounds do and do not imply

21 November 2026. **Neither 3431 nor 5063 is excluded.** The numerical
unit-charge question at the two target shapes remains open in this note.

The proposed universal inequality

\[
n_L\ge 3|G_L|
\tag{1}
\]

cannot follow from integer whole triangles, pairwise interior nonoverlap,
and cylinder short-endpoint closure alone. It fails for higher charges at
both target shapes. It also fails at unit charge for the smaller primitive
shape `(5,3,7)`. These are exact geometric countercontrols, not relaxed
fractional points. They have no complete board filling or complete
neighboring-node gate compatibility.

A second useful control shows that balanced population six survives even
the new mandatory short-to-long bank condition. The corresponding patch
fits strictly inside either target board at height one. Thus that stronger
condition must be used together with the remaining phase and gate data;
it does not automatically eliminate a six-tile balanced cell.

## 1. Definitions and exact verification

Use axial coordinates with

\[
U_0=(1,0),\ U_1=(0,1),\ U_2=(-1,1),\quad U_{j+3}=-U_j.
\]

For a tile `(q,j,s)`, `s=+/-1`, its vertices and charge are

\[
q,\qquad u=q-aU_j,\qquad w=q+bU_{j+s},\qquad
\epsilon=s(-1)^j.
\]

Its short-endpoint column is

\[
s(j,q)-s(j,u)+s(j+s,w)-s(j+s,q),
\tag{2}
\]

with the axis label reduced modulo three. Cylinder rows retain the actual
supporting line and reduce only its longitudinal coordinate modulo `c`:

| Axis | Row at `(x,y)` |
|---|---|
| 0 | `(0,y,x mod c)` |
| 1 | `(1,x,y mod c)` |
| 2 | `(2,x+y,y mod c)` |

Every asserted row equality is checked with integers. Pairwise nonoverlap
is checked by separating axes of the actual convex triangles. Axial
coordinates preserve intersections and separation because they are related
to orthogonal Euclidean coordinates by an invertible linear map.

## 2. Higher-charge countercontrol at both targets

Assume `a>b>0`, `gcd(a,c)=1`, and `a^2+ab+b^2=c^2`. Take

\[
q_{r,t}=(ar,at),\qquad 0\le r,t<c,\qquad(j,s)=(0,+1).
\tag{3}
\]

Each triangle lies in the axial parallelogram

\[
a(r-1)\le x\le ar,\qquad at\le y\le a(t+1).
\]

Different parallelograms have disjoint interiors, and the triangle's actual
vertical extent is `b<a`. Thus (3) is a finite rigid packing. On each actual
horizontal support line, the `a`-side anchors run through all residues
modulo `c`; on each actual vertical support line the `b`-side anchors do
the same. Both short endpoint currents vanish on their cylinders.

All tiles have positive charge. Consequently

\[
n_L=G_L=c^2<3G_L.
\]

The gates are explicit: `Q_up(r)=c` at every residue, and `Q_down(r)=0`.
This disproves an unrestricted-charge version of (1) for the exact target
shapes `(33,7,37)` and `(35,13,43)`, as well as `(5,3,7)`. No target-board
containment or full adjacent-node gate profile is asserted.

## 3. A unit-charge rigid cylinder counterexample at `(5,3,7)`

The following thirteen whole triangles have ten positive and three
negative signs, hence `G=7`, whereas `13<3*7`.

| Index | x | y | j | s |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 |
| 1 | 105 | 0 | 2 | 1 |
| 2 | 0 | 105 | 4 | 1 |
| 3 | 0 | 285 | 4 | 1 |
| 4 | 30 | 135 | 5 | 1 |
| 5 | 165 | 0 | 2 | 1 |
| 6 | 165 | 120 | 2 | 1 |
| 7 | 270 | 120 | 4 | -1 |
| 8 | 270 | 15 | 4 | 1 |
| 9 | 390 | 0 | 1 | -1 |
| 10 | 390 | -105 | 1 | 1 |
| 11 | 285 | 0 | 2 | 1 |
| 12 | -30 | 135 | 2 | 1 |

The exact verifier checks every cylinder row and all 78 triangle pairs.
The support is recorded in
[CHARGED_COUNTERCONTROLS.json](CHARGED_COUNTERCONTROLS.json).

The construction starts with an integer periodic kernel discovered by a
mixed-integer search. The discovered point has all multiplicities one and
is checked independently with integer arithmetic; no optimization status
is used as a proof. Every occupied endpoint row has exactly one positive
and one negative contribution. Their transverse equalities have the form
`T_axis(q_i)=T_axis(q_j)`: the transverse offsets from `q` to `u` or `w`
vanish because those offsets lie along the relevant short edge. These are
homogeneous actual-line conditions.

For the orientation list in the table, a family of solutions is

\[
\begin{split}
q_0&=(0,0),&q_1&=(T,0),&q_2&=(0,T),&q_3&=(0,H),\\
q_4&=(I-W,W),&q_5&=(I,0),&q_6&=(H-V,V),&q_7&=(R,V),\\
q_8&=(R,H-R),&q_9&=(S,0),&q_{10}&=(S,H-S),\\
q_{11}&=(H,0),&q_{12}&=(T-W,W).
\end{split}
\]

The required residues are

\[
(T,H,I,W,V,R,S)\equiv(0,5,4,2,1,4,5)\pmod7.
\]

Choose `(7,19,11,9,8,18,26)` and scale all anchors by `15`, which is one
modulo seven. Homogeneity preserves actual supporting-line equalities;
the congruence preserves endpoint residues. The resulting triangles have
disjoint interiors as checked directly. This is a finite packing in the
unbounded plane, not a tiling of the 143 board.

### Why the new bank condition still matters

The separated thirteen-tile packing fails the full longitudinal bank
condition: the required neighboring length-seven segments overlap on the
same side. More compact lifts can pass that line capacity test and still
fail the actual neighboring-triangle choices. One exact example in
[COMPACT_C7_LIFTS.json](COMPACT_C7_LIFTS.json) has 32 mandatory long
segments, no line capacity conflicts, and an unsatisfiable two-choice
neighbor system because required triangles meet the existing odd tiles.

The exploratory lift search tested a selected finite set of 12,401
parameter tuples. Of these, 1,768 give nonoverlapping odd tiles; six also
pass the long-segment capacity check; all six fail the geometric bank
test. These finite counts do not exclude untested lifts or prove a
unit-charge theorem after bank completion.

## 4. A compact six-tile patch that passes bank completion

For any positive `a>b`, put `t=-(a+b)` and take

\[
\begin{array}{c|ccc}
q=(0,0)&(j,s)=(0,+1)&(2,-1)&(2,+1)\\
q=(t,0)&(j,s)=(3,+1)&(5,-1)&(5,+1).
\end{array}
\tag{4}
\]

Each row is a fan of three triangles in disjoint 120-degree sectors. The
second fan is the central inversion of the first, translated by `(t,0)`.
The first fan has minimum `x=-a`; the second has maximum `x=-b`.
On their potentially common strip `-a<=x<=-b`, the first fan lies above
the horizontal line and the second below it. The two fans therefore
have disjoint interiors.

Within the first fan all short currents cancel except

\[
\delta_{(-b,0)}-\delta_{(-a,0)}
\]

on axis zero. Within the second fan the remainder is

\[
\delta_{(t+b,0)}-\delta_{(t+a,0)}
=\delta_{(-a,0)}-\delta_{(-b,0)}.
\]

Thus **the entire unreduced physical short current is zero**, not only
its cylinder reduction. There are three tiles of each sign and no
mandatory neighboring long segments from this short current. The full
mandatory short-to-long bank test is satisfied with the empty bank.
The patch's outer long boundary still needs the other parts of a tiling.

The exact gate signature is

\[
Q_{\rm up}=0,\qquad
Q_{\rm down}=\delta_{2b^2\bmod c}-\delta_{-b^2\bmod c}.
\tag{5}
\]

For example, the nonzero down currents are `+1` at 24 and `-1` at 25
for 3431; they are `+1` at 37 and `-1` at 3 for 5063. A translation shifts
both residues by the same down-gate phase. Formula (5) is a unit dipole;
it does not satisfy an arbitrary complete neighboring-node profile.

For the two target shapes, translate every normalized vertex by
`(150,100)` and rotate by `z=(a+b*rho)/c`. The verifier checks strict
containment in the standard board with vertices

\[
(0,0),\quad\bigl(b(2a+b),0\bigr),\quad
\bigl(0,a(a+2b)\bigr).
\]

Full coordinates, all 15 separation checks, the zero unreduced short
current, and the integer containment margins are in
[BALANCED_SIX_PATCH.json](BALANCED_SIX_PATCH.json).

This construction blocks a proposed universal exclusion of balanced
population six using mandatory short-to-long neighbors alone. It does
not eliminate or realize any remaining 5063 four-cell profile.

## 5. Status of the target unit-charge bound

No construction or impossibility proof for `G=c`, `n<3c` at `c=37` or
`c=43` is established here. Direct full periodic integer optimization
probes returned no incumbent within their limits; those runs provide
neither a witness nor a mathematical exclusion. The `c=7` counterexample
does not automatically transfer to a different residue root `a/b mod c`.

Any valid theorem for the target charged cells must state which of the
following it uses: target arithmetic, complete phase-node gate currents,
the mandatory geometric bank, global board containment, and closure of
the remaining boundary. Integer triangles and disjoint interiors, even
together with all cylinder rows, are not sufficient hypotheses for an
unrestricted version of (1).

## Replay

From the repository root:

```sh
python3 research/2026-11-21/semiprimes/integer-closure/charged-cells/verify_charged_countercontrols.py
python3 research/2026-11-21/semiprimes/integer-closure/charged-cells/verify_balanced_six_patch.py
```

These replays use no floating-point optimization. The discovery and
selected-lift probe scripts are separate from the proof verifiers.
