# Fast additive endpoint duals for the minimal odd mode

21 November 2026. This note proves validity of a smaller certificate
generator. It does **not** assert that its two marginal feasibility
model is equivalent to the full endpoint model, or that either model
is equivalent to a geometric tiling.

The complete-profile exclusion, if established by a separate exhaustive
exact replay, uses the exported inequalities. It does not need to trust
the optimizer or the smaller model's primal solutions.

## 1. The geometric necessary projection

Use the path frame and the previously proved localization under
`n_odd=3c`: all odd tiles have short height one and their vertices are
in `zR`. Divide by `z`. An odd tile now has integral anchor
`q=(x,y)`, rotation `j in {0,...,5}`, and hand `s in {-1,+1}`.
Its two other vertices are

\[
 u=q-aU_j,\qquad w=q+bU_{j+s},\qquad
 \epsilon=s(-1)^j,
\]

where `U_j` are the six Eisenstein unit vectors. Its CCW short-edge
endpoint functional is

\[
 W_F(q,j,s)=s\bigl(F_j(q)-F_j(u)+F_{j+s}(w)-F_{j+s}(q)\bigr).
 \tag{1}
\]

Subscripts on the three unoriented-axis functions are taken modulo
three. Introduce the two residue coordinates

\[
 \phi(q)=ay-bx\pmod c,\qquad
 \psi(q)=ax-by\pmod c.
\]

An upward long edge belongs to gate `phi(u)` and a downward one to
gate `psi(u)`. The established exact neighboring-node equations give

\[
 Q_r^+=(a-b)g_r^++2c\,\mathbf1_{r=0},\qquad
 Q_r^-=(a-b)g_r^--c\,\mathbf1_{r=0},
 \qquad g_r^\pm\in\mathbb Z.
 \tag{2}
\]

Here `Q` is signed physical parent-tile current; it is not a count
of abstract tiles inserted into a missing region. The same equations
allow balanced occupied remote branches. In particular `Q_r=0`
does not impose a half-turn mate on every tile using that gate.

## 2. Two marginal families

For each of the twelve orientations `(j,s)`, retain one nonnegative
distribution `x_(j,s)(r)` on the `phi(q)` residues and another
`y_(j,s)(t)` on the `psi(q)` residues. Impose:

* the three axis endpoint equations on each of the `c` phi residues;
* the three axis endpoint equations on each of the `c` psi residues;
* all `2c` specified gate-current equations;
* equality of the two total masses for each of the twelve orientations.

Minimize the total mass of the phi marginals. A full odd-tile inventory
projects to these distributions simply by summing its tile counts.
Each original short-edge equation implies its marginal counterpart,
and each tile occurs once in each of its two orientation marginals.
Thus any actual tiling supplies a feasible solution of this smaller
problem with objective `n_odd`.

The model has `24c` nonnegative variables and `8c+12` equality rows:
**1032 variables and 356 rows for c=43**, compared with the full
`12c^2=22188` placement-residue columns. It has no physical position
box and does not impose a guessed geometric catalogue.

Some full two-coordinate endpoint constraints are discarded. No reverse
implication is used. In particular equality of marginal orientation
totals does not by itself make the unprojected endpoint currents vanish.

## 3. Why every additive dual is valid on every original tile

Let a dual solution assign endpoint tables `f_i(r)` to the phi rows
and `h_i(t)` to the psi rows, gate weights `v_r^+,v_r^-`, and
orientation multipliers `lambda_(j,s)` to the equality of the two
orientation masses.

Write `W_f` and `W_h` for (1) evaluated with the respective
one-coordinate tables. The dual inequality for a phi marginal column
is

\[
 W_f(r,j,s)
 +\epsilon\,\mathbf1_{s=+1}v^+_{\phi(u)}
 +\lambda_{j,s}\le1.
 \tag{3}
\]

The inequality for the corresponding psi marginal column is

\[
 W_h(t,j,s)
 +\epsilon\,\mathbf1_{s=-1}v^-_{\psi(u)}
 -\lambda_{j,s}\le0.
 \tag{4}
\]

Take an arbitrary original translated tile and substitute its actual
`r=phi(q)` and `t=psi(q)` into these inequalities. Add them. The
orientation multipliers cancel, and the right sides add to one.
Define the complete two-coordinate endpoint potential

\[
 F_i(x,y)=f_i(ay-bx)+h_i(ax-by),
 \tag{5}
\]

with residues taken modulo `c`. Then every original tile satisfies

\[
 W_F(q,j,s)+\epsilon v^{s}_{r_s(u)}\le1.
 \tag{6}
\]

This argument proves dual validity without requiring a lift of any
marginal primal solution. It is also valid if the marginal model is
strictly weaker than the full residue model.

## 4. The exact integer certificate is self-contained

The discovery script uses numerical optimization only to propose
the tables in (5) and the gate weights. It rounds scaled tables to
integers and then recomputes the integer score on **every** anchor
`(x,y) in (Z/cZ)^2`, every rotation and every hand. Set

\[
 D=\max\left(1,\max_{x,y,j,s}
 \{W_F(x,y,j,s)+\epsilon v^s_{r_s(u)}\}\right).
 \tag{7}
\]

The exported certificate therefore has the exact inequalities

\[
 W_F(q,j,s)+\epsilon v^s_{r_s(u)}\le D
 \tag{8}
\]

on all translated tiles, regardless of numerical solver residuals.
Independent replay should reconstruct CCW polygons and check these
inequalities directly from the exported integer tables. The
orientation multipliers and the marginal optimization matrix are
not needed in that replay.

To sum (8) on a physical tiling, use the usual endpoint weighting on
short-height-one edges in the native cell, and zero outside that cell
or on other edge heights. Endpoint differences telescope even under
partial contacts. A complete long edge at height one has length `c`,
so its endpoints have equal residues in (5) and its weight is zero.
Other Euclidean cells contribute zero. There is no exterior side at
short height one. Consequently the total endpoint contribution is zero.
The remaining terms give the global necessary inequality

\[
 \boxed{D\,n_{\rm odd}
 \ge\sum_r v_r^+Q_r^+ +\sum_r v_r^-Q_r^-.}
 \tag{9}
\]

Substituting an integer profile from (2) makes its right side an
explicit integer. If that integer exceeds `3cD`, the entire profile
is excluded under the minimal-odd hypothesis. Such an exclusion
does not depend on the relative placement of its charged branches,
on a bound for their tile coordinates, or on absence of balanced
remote nodes.

## 5. Software interface and observed scope

`additive_gate_model.py` exports

```python
solve(a, b, c, up_gate_charges, down_gate_charges)
```

It returns the usual full certificate keys:

`tile`, `endpoint_tables`, `up_weights`, `down_weights`, `D`,
`lower_numerator`, `lower_denominator`, and
`exact_column_inequalities`. It additionally records the marginal
tables and orientation multipliers for provenance. The full endpoint
tables and gate weights alone suffice for independent proof replay.

Command-line use accepts a JSON file containing the tile and its two
gate-charge arrays:

```sh
python3 additive_gate_model.py profile.json --out additive_cut.json
```

As a diagnostic, the previously selected 5063 profile with native
charges `(-3,2)`, upward remote charges `+1` at residues 9 and 13,
and `-1` at residue 31 has the same observed optimum
`166.281791659...` in both models. The smaller model exports the
exact bound `166281799/1000001 > 129`. Its recorded optimization
time is approximately 0.15 seconds; timing is not part of the proof.

The comparison file records thirty previously generated profiles.
The additive bounds exceed 129 on all thirty, although several are
strictly weaker than their full-model counterparts. These comparisons
are performance diagnostics, not an exhaustive profile theorem.

There is a material limitation: the additive model with all remote
charges zero and native charges `(-3,3)` has a numerical feasible
129-population point, whereas the previously verified full-model
certificate excludes that case. Therefore a complete exclusion must
retain appropriate full-model cuts or use another exact argument
for profiles that survive the additive cuts. The separate full
finite-profile replay, rather than the numerical comparison or a
mixed-integer solver status, establishes whether the combined
certificate set covers every allowed profile.
