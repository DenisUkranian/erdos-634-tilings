# A global capacity certificate with shared physical owners

This note formulates a sound certificate target for the new model. It is not
a separating certificate for 3431 or 5063 and assumes no positive-load or
staircase necessity conjecture.

## Sign completion reserve

Let `P` be any finite selected subset of a hypothetical full tiling. Write
`m=|P|` and let `g_o,g_e` be its odd/even signed populations in the standard
frame. Since the full signed totals are `-c` and `-(a-b)`, the omitted tiles
must contain at least `|c+g_o|` odd tiles and `|a-b+g_e|` even tiles. Therefore

\[
\boxed{m+|c+g_o|+|a-b+g_e|\le N.}
\]

Expanding the two absolute values gives exactly the four charge-reserve
cardinality cuts. This inequality is valid without fixing the odd population
or the number of heights. It counts a selected whole tile once even when that
tile serves several contacts.

## Contact and spatial capacity

Let `Q` be a finite canonical whole-tile pool containing all candidates for
the installed contact obligations. Let `B` be chosen exterior unit intervals;
every real tiling satisfies `sum_{q covers b} x_q=1`. Each installed directed
contact obligation `e` has a selected source tile `T_e` and its **complete**
opposite-bank catalogue `D_e`, so

\[
x_{T_e}-\sum_{q\in D_e}x_q\le0.
\]

Each certified spatial clique `C` satisfies `sum_{q in C}x_q<=1`.
The four signed classes `S_r` have the preceding capacities `M_r`.

Choose rational weights `beta_b` on boundary equalities (either sign is
allowed) and nonnegative rational weights `lambda_e,mu_C,rho_r` on the
contact, clique and signed-capacity inequalities. Define

\[
w_q=
\sum_{b:q\text{ covers }b}\beta_b
-\sum_{e:T_e=q}\lambda_e
+\sum_{e:q\in D_e}\lambda_e
-\sum_{C:q\in C}\mu_C
-\sum_{r:q\in S_r}\rho_r.
\]

If the finite, exact coefficient check gives `w_q<=1` for every `q in Q`,
then every tiling satisfies

\[
\boxed{
\sum_b\beta_b-\sum_C\mu_C-\sum_r\rho_r M_r
\le \sum_{q\in Q}x_q\le N.
}
\]

**Proof.** Subtract the weighted necessary inequalities from the weighted
boundary identities. The result is

\[
\sum_b\beta_b\le
\sum_qw_qx_q+\sum_C\mu_C+\sum_r\rho_rM_r.
\]

All `x_q` are nonnegative and each `w_q<=1`, which proves the displayed
bound. Completeness of each installed contact catalogue makes the argument
valid for a restriction of any full tiling to `Q`; no omitted placement can
serve an installed demand. The coefficient of a shared tile includes every
contact it can serve, preventing an unjustified one-contact/one-tile cost.

Root equalities `x_q=1` and complete endpoint equalities may be added with
arbitrary rational multipliers in exactly the same way. This can strengthen
a root branch certificate. A valid global certificate would have left-hand
side greater than `N`; each exact coefficient and sign can be replayed with
rational arithmetic. The present work has not produced such weights for
either target.
