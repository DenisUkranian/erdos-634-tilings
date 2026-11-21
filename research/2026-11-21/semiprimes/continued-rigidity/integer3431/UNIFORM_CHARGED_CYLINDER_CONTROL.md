# A rigid integer cylinder control with population 3c

21 November 2026. **Theorem.** Let `(a,b,c)` be any of `(5,3,7)`,
`(33,7,37)`, or `(35,13,43)`. There is a partial packing in the
unbounded plane consisting of `3c` actual congruent triangles, with
`2c` positive and `c` negative signs, whose complete short-edge
cylinder current vanishes.

The construction is integral and the triangle interiors are pairwise
disjoint. It does **not** satisfy the remote gate congruences required
by a tiling, and target-board containment is not asserted. Thus
integrality and nonoverlap, even when combined with exact cylinder
rows, do not by themselves improve the lower bound `n >= 3c` in this
unbounded partial-packing model.

## Construction

Use the Eisenstein coordinate basis `1,rho`, where `rho=exp(i*pi/3)`,
and unit directions

\[
U_0=(1,0),\quad U_1=(0,1),\quad U_2=(-1,1),\quad
U_3=(-1,0),\quad U_4=(0,-1),\quad U_5=(1,-1).
\]

A tile with obtuse vertex `q`, orientation `j` and hand `s` has
vertices `q`, `q-aU_j`, `q+bU_(j+s)` and sign `epsilon=s(-1)^j`.
Put `L=2c+1`. For each `r=0,...,c-1`, set

\[
q_r=(0,Lr)
\]

and take the three orientations

\[
(j,s)=(0,-1),\ (0,+1),\ (4,+1).                 \tag{1}
\]

The signs of (1) are `-1,+1,+1`. Hence the population is `3c` and
the charge is `c`.

## Exact cylinder cancellation

At one anchor `q`, the a-edge currents of `(0,-1)` and `(0,+1)`
cancel exactly. The b-edge currents of `(0,-1)` and `(4,+1)` also
cancel exactly. The remaining current consists of two endpoints
on the vertical supporting line:

\[
 [q+bU_1]-[q+aU_1].                            \tag{2}
\]

All anchors have actual transverse coordinate `x=0`. The cylinder
keeps this exact coordinate and reduces the longitudinal coordinate
`y` modulo `c`. Since `L=1 mod c`, the positive endpoints in (2)
run through all residues once, and so do the negative endpoints.
Their aggregate cylinder current is zero.

For clarity, the checker retains the following row coordinates:

| Axis | Exact transverse coordinate | Longitudinal coordinate |
|---|---|---|
| 0 | `y` | `x mod c` |
| 1 | `x` | `y mod c` |
| 2 | `x+y` | `y mod c` |

The unreduced physical endpoint current is not zero: it has exactly
`2c` nonzero rows. This is a partial odd-layer packing, not a complete
filling of the plane or of a board.

## Nonoverlap

After subtracting the common anchor, the three polygons have vertices

\[
\begin{aligned}
T_-&=\{(0,0),(-a,0),(b,-b)\},\\
T_+&=\{(0,0),(-a,0),(0,b)\},\\
T_4&=\{(0,0),(0,a),(b,-b)\}.
\end{aligned}
\]

The pair `T_-,T_+` is separated by `y=0`; the pair `T_+,T_4` by
`x=0`; the pair `T_-,T_4` by `x+y=0`. Their interiors are disjoint.
Every triangle lies in the closed Euclidean radius-a disk centered
at its obtuse vertex. Distinct anchors are at least `L=2c+1>2a`
apart because `a<c`. Thus triangles at different anchors are also
disjoint. The replay additionally verifies every triangle pair using
exact integer separating-axis inequalities.

## Why the construction is not a tiling witness

The upward gate coordinate is `phi(u)=a u_y-b u_x mod c`; the
downward one is `psi(u)=a u_x-b u_y mod c`, with `u=q-aU_j`.
For each of the three orientation families, the corresponding gate
coordinate is a permutation of the residues. The two positive
families have upward hand and the negative family has downward hand.
Consequently

\[
 Q_r^+=2,\qquad Q_r^-=-1\qquad\text{for every }r.       \tag{3}
\]

An actual complete neighboring node requires every remote gate
current to be divisible by `d=a-b`. Here `d` is `2`, `26`, or `22`,
and the downward current `-1` fails that condition. For both target
shapes the upward current `2` fails it as well. Board containment
and completion by all other heights have not been supplied either.

In particular, this control cannot contradict the established
exclusion of the 5063 population-129 regime: that proof uses the
neighboring-node gate conditions that (3) violates.

## Reproduction

Run:

```sh
python3 verify_uniform_charged_cylinder.py
```

The standard-library checker reconstructs all triangles, checks every
actual cylinder row, verifies all pairwise separating inequalities,
and reports the failed remote-gate congruences. It writes
`UNIFORM_CHARGED_CYLINDER_REPLAY.json`.

The earlier discovery script `probe_translation_orbits.py` used the
compact torus representatives `q=(0,r)`. The files
`TRANSLATION_ORBITS_7_3.json`, `TRANSLATION_ORBITS_37_3.json`, and
`TRANSLATION_ORBITS_43_3.json` contain these full integer torus
supports. The proof above supplies the separated actual-cylinder lift.
