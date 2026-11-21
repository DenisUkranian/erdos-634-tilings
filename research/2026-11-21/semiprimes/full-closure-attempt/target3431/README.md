# A native-profile exclusion and a whole-gate integrality cost at 3431

21 November 2026. **The original count 3431 remains OPEN.**
These results concern the established necessary periodic projection of a
hypothetical minimal odd population, `n_odd=111`, with tile `(33,7,37)`.
They do not enumerate all charge profiles or geometric placements, and do
not address the larger odd populations.

Two exact certificates are new:

1. The native profile `Q_up=-4 delta_0`, `Q_down=41 delta_0`, with all
   remote currents zero, already requires more than 157 tiles in the
   full continuous endpoint model. It cannot occur at population 111.
2. For the remaining native profile `(22 delta_0,15 delta_0)`, the complete
   endpoint equations and the sign counts `(74,37)` force a positive
   **excess negative population**. When the unsigned gate populations
   are integral, at most **34 remote gates contain any parent odd tile**.

The second certificate counts the long-edge gate inventory of the odd
parent cell. A separate [geometric visibility theorem](INVISIBLE_EVEN_NODES.md)
proves that every occupied remote even cell in this normal form has an
actual contact with a parent odd long side. It follows that this profile
also has at most **34 occupied remote even cells**. The written geometric
deduction uses the existing supported-cycle exclusion for these target
boards; it is distinct from the finite periodic certificate.

## 1. Necessary model and exact column convention

Use the path frame of the existing
[minimal-odd phase classification](../../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md).
All odd tiles have short height one, their normalized anchors lie in
`R=Z[rho]`, and their signs have populations `n_+=74`, `n_-=37`.

Let `c=37`, `a=33`, `b=7`. A residue tile has anchor `q=(x,y)` in
`(Z/cZ)^2`, rotation `j` modulo six, and hand `s=+1` or `-1`. Put

\[
 U_j=(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1),
 \quad u=q-aU_j,\quad w=q+bU_{j+s},
 \quad\epsilon=s(-1)^j.
\]

Its short-edge **end-minus-start** column is

\[
 s(e_{j,q}-e_{j,u}+e_{j+s,w}-e_{j+s,q}),
\]

with axes reduced modulo three and positions modulo `c`. The corresponding
long-edge gate is `a*u_y-b*u_x` for an upward tile, or
`a*u_x-b*u_y` for a downward tile. The gate-current coefficient is
`epsilon`. Every actual tiling induces a nonnegative integral vector on
these `12c^2=16,428` columns, permitting residue multiplicities larger than
one. Every full short-endpoint row sums to zero.

The present certificates retain **all** `3c^2` endpoint rows. They are not
one-coordinate marginal certificates. They require no spatial box,
embedding, or restriction on residue multiplicities.

## 2. Excluding the all-balanced-remote native profile `(-4,41)`

Assume the upward current is `-4` at the native gate and zero at every
remote gate, while the downward current is `41` at the native gate and
zero remotely. Let `A` contain the complete endpoint and gate rows, and
let `b` be this right-hand side.

The first certificate supplies integer row weights `w` and

\[
 D=100000002
\]

such that, for **every** residue tile column,

\[
 w^T A_t\le D.
\]

The independently reconstructed right-hand side evaluates to

\[
 w^T b=15776947829.
\]

For every nonnegative combination of tile columns satisfying the stated
profile, summation proves

\[
 \boxed{n\ge\frac{15776947829}{100000002}>157>111.}
\]

Thus this complete fixed profile is impossible at `n_odd=111`, even when
the tile coefficients are allowed to be fractional. No empty-gate pairing
assumption or gate-cap hypothesis is used in this exclusion.

This removes the all-zero-remote-charge profile with native charge
parameters `g_up=-3`, `g_down=3`. It does not remove profiles having
nonzero remote charges, nor the different all-zero-remote profile `(22,15)`.

## 3. A convex excess cost for profile `(22,15)`

Now prescribe native currents `22` upward and `15` downward, with all
remote gate currents zero, and sign populations `74,37`.

For a remote gate `g`, let `m_g` count its negative odd tiles. Let
`m_nat` be the total negative population at the two native gates. Define

\[
 E=m_{\rm nat}+\sum_{g\text{ remote}}(m_g-1)_+.
\tag{1}
\]

Introduce nonnegative auxiliary variables `t_g` with

\[
 m_g-t_g\le1.
\]

Minimizing `m_nat+sum t_g` recovers (1). This is only a convenient way
to discover a certificate; the proof below is the exact column check.

The second certificate supplies integer equality weights `u`, nonpositive
weights `v_g` on these 72 inequalities, and `D=10^9`. With `A` now also
containing the two sign-count rows, every tile column satisfies

\[
 u^T A_t+\sum_g v_g C_{g,t}
 \le D\,\mathbf1_{\{t\text{ negative at a native gate}\}},
\tag{2}
\]

where `C_{g,t}=1` for a negative tile at remote gate `g` and is zero
otherwise. Every auxiliary column satisfies

\[
 -v_g\le D.
\tag{3}
\]

Multiplying (2)--(3) by the nonnegative tile and auxiliary variables gives

\[
 D\left(m_{\rm nat}+\sum_g t_g\right)
 \ge u^T b+\sum_gv_g(m_g-t_g)
 \ge u^T b+\sum_gv_g.
\]

The last step uses `v_g<=0` and `m_g-t_g<=1`; its direction is essential.
The exact right-hand side is `2173857481`. Taking
`t_g=(m_g-1)_+` therefore proves

\[
 \boxed{E\ge\frac{2173857481}{10^9}>2.}
\tag{4}
\]

When the unsigned gate populations are integral, `E` is an integer, so
`E>=3`. Since there are exactly 37 negative odd tiles, and every remote
net current is zero, put

\[
 K=\#\{g\text{ remote}:m_g>0\}.
\]

A remote gate contains any odd tile if and only if `m_g>0`, because its
positive and negative populations are equal. The elementary identity

\[
 E=m_{\rm nat}+\sum_gm_g-K=37-K
\]

then gives

\[
 \boxed{K\le34.}
\tag{5}
\]

In particular the putative saturation having 37 remote gates each carrying
one positive and one negative odd tile, with only positive tiles at the
native gates, is excluded. So are the analogous `K=35,36` inventories.
The theorem permits `K<=34`; it does not show that any such inventory is
physically realizable or that all of them are impossible.

The integrality used to deduce (5) is only that of the **unsigned gate
populations**. Integer individual tile multiplicities imply it. The bound
(4) itself holds for all nonnegative real tile vectors in the prescribed
full periodic model.

By the separately proved [visibility theorem](INVISIBLE_EVEN_NODES.md),
every occupied remote even cell has an actual short-to-parent-long
contact, so its corresponding remote gate is nonempty. The gates of
distinct remote even cells are distinct in their appropriate hands.
Consequently the actual occupied remote-cell count also satisfies

\[
\boxed{K_{\rm occupied}\le K\le34.}
\tag{6}
\]

The first inequality is geometric. Zero signed current alone would not
justify it, and a nonempty parent gate need not have an occupied even
cell: its odd long sides may instead pair with each other.

## 4. Why this is not yet a closure

The profile `(22,15)` survives the older continuous endpoint model. The
new excess cost supplies an integer consequence, but an upper bound on
used gates is not an impossibility proof. A complete exclusion would need
an incompatible lower bound on their support, stronger physical contacts,
or a different necessary condition. Other remote-charge profiles and
larger odd populations must also be handled.

Several fixed empty-gate patterns were tested using a stronger full
periodic pairing projection. These were discovery experiments, not an
exhaustive search. A chosen pattern being infeasible at 111 does not
establish that every pattern of the same size is infeasible. No such
cardinality conclusion is asserted here.

The visibility theorem resolves the specific possibility of an occupied
remote even cell invisible to the parent long-edge inventory under the
stated normal form. It strengthens the interpretation of the upper bound
in (5), but does not exclude any inventory with at most 34 occupied remote
cells. Its three-height, one-native-odd-cell hypotheses are essential to
the present proof.

## 5. Independent exact replay

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/target3431/verify_gate_excess.py
```

The standard-library checker reads
[`GATE_EXCESS_CERTIFICATE.json.gz`](GATE_EXCESS_CERTIFICATE.json.gz),
reconstructs all 16,428 columns separately for each inequality, checks
all 72 auxiliary columns and their signs, and recomputes both integer
objectives. It also checks the gate identity on 4,096 small integer
inventories. The same endpoint/sign/gate convention is checked on the
native odd projection of an independently verified complete 143 tiling.
The 3431-specific inequalities are not applied to that different shape.
The replay is [`GATE_EXCESS_REPLAY.json`](GATE_EXCESS_REPLAY.json).

The discovery programs `probe_full_gate_pairs.py` and
`probe_gate_excess.py` use NumPy/SciPy. No numerical solver result,
iteration count, or timeout is used in the exact proofs. The certificate
and checker are sufficient to verify the stated finite inequalities;
their application to hypothetical tilings uses the separately cited
phase classification and the written deductions above.
