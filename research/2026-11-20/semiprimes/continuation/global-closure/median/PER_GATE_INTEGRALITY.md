# A complete-residue test with integer neighboring-node charges

21 November 2026. This is a necessary relaxation of a hypothetical complete
tiling with total odd population `3c`. It is not an exact geometric
tiling model. Continuous placement weights are allowed; only the signed
charges of the neighboring exact phase nodes are required to be integers
in units of `c`.

Use the path frame and the proved minimal-population localization:
only short heights 0, 1, 2 occur, and all height-one tiles have vertices
in `zR`. They have sign populations `2c,c`. After division by `z`, a
height-one placement has an integral anchor `q=(x,y)` and acute endpoint
`u=q-a*rho^j`.

## The two full residue coordinates

For an upward long edge use

\[
 r_+(u)=a u_y-b u_x\pmod c.
\]

For a downward long edge use

\[
 r_-(u)=a u_x-b u_y\pmod c.
\]

The downward zero condition is equivalent to
`b*u_x+(a+b)*u_y=0 mod c`, since the norm relation makes the two
numerators of `z*u` dependent modulo `c`. The two functions are the
two distinct prime residues. In particular both must be retained;
reducing to either one alone would lose the coupling at a common anchor.

Among endpoints in the native height-one class, the upward residue
labels the `c` child edge nodes at height 2 of its increasing-tree
node. The downward residue labels the `c` child edge nodes at height 0
in the conjugate tree. Residue zero contains the corresponding outer
edge node. All other nodes in each list are ordinary.

Let `Q_r^+` and `Q_r^-` be the signed sums of height-one tiles with
upward or downward long edges in the indicated classes. The exact
node equation is `dG_v-cH_v=b_v`, with `d=a-b`.

At height 2, only height-one upward long edges contribute to `H_v`:
height 3 is absent. For a remote node `G_v=c*g`, giving
`Q_r^+=d*g`. The native node has exterior current
`-(c^2+3ab)=d^2-2c^2`, so its charge is `G_v=d+c*g`, giving
`Q_0^+=2c+d*g`.

At height 0, height minus one is absent. The native base current is
`c^2`, every height-zero charge is divisible by `c`, and therefore

\[
 \boxed{Q_r^+=d g_r^+ +2c\,\mathbf1_{r=0},\qquad
 Q_r^-=d g_r^- -c\,\mathbf1_{r=0},\qquad
 g_r^+,g_r^-\in\mathbb Z.}                            \tag{1}
\]

These constraints count exact phase nodes, rather than arbitrarily
grouped Euclidean translates. No omission of an internal height-zero
contact, or pairing of every nonnative long edge, is assumed in (1).
Possible height-zero/height-two reflected contacts along long-height-one
edges do not enter `H_v` at heights 0 and 2.

## Finite residue projection and its scope

`per_gate_integrality.py` takes every anchor in `(Z/cZ)^2`, every one of
six rotations, and both hands. It has a nonnegative **continuous**
weight for each of these `12c^2` placement classes. The constraints are:

* zero short-height-one endpoint current on all `3c^2` axis/residue rows;
* total positive and negative weights `2c,c`;
* the `2c` equations (1), with integer `g` variables.

Every complete tiling in the minimal mode projects into this finite
model, regardless of its actual anchor denominators elsewhere or the
number of individual placements in a residue class. There is no bounded
position catalogue. The short-endpoint equations remain a necessary
projection: they do not preserve every real supporting line, physical
bank, nonoverlap condition, or closed-gate matching condition.

For numerical stability the integer charge bounds follow only from
`-c<=Q_r<=2c`. The solver's time budget is recorded in the output.
A feasible solution is an algebraic projected witness, not a tiling.
A timeout gives no mathematical verdict. A numerical infeasibility
result would still require an exported independently verifiable exact
argument before use as a theorem.

## Recorded numerical diagnostics

The two mixed-integer runs used a requested solver time limit of 60
seconds. They returned a time-limit status after approximately 84.9 and
83.9 wall seconds, with no feasible point and no infeasibility verdict.
No larger mixed-integer run was used to support a theorem.

For a smaller diagnostic, set every remote charge to zero and fix

\[
 g_0^+=-f,\qquad g_0^-=f.
\]

Here `f=G_(native height-zero node)/c`. It is not automatically the
upper-median parameter `n=G_even(lower median region)/c`: native
height-two islands below that path can contribute to the latter.
The two fixed native signed currents are
`Q_0^+=2c-df`, `Q_0^-=-c+df`.

| Target | Test | Native currents `(up,down)` | Recorded numerical status |
|---:|---|---|---|
| 3431 | Integer gate charges unrestricted | — | Time limit; no verdict |
| 5063 | Integer gate charges unrestricted | — | Time limit; no verdict |
| 3431 | All remote charges zero, `f=2` | `(22,15)` | Continuous feasible point; maximum equality residual `1.42e-13` |
| 5063 | All remote charges zero, `f=2` | `(42,1)` | Numerical infeasible |
| 5063 | All remote charges zero, `f=3` | `(20,23)` | Numerical infeasible |
| 5063 | All remote charges zero, `f=4` | `(-2,45)` | Numerical infeasible |

The 3431 point is a floating continuous projection with 3,867 nonzero
placement weights. It is not an integer placement certificate, a
packing, or a full tiling. The 5063 statuses are not exact certificates
by themselves. A separate minimum-population dual check is required
before using those diagnostics as a mathematical exclusion.

## Why zero remote current is weaker than a closed gate

In the localized `3c` mode every nonnative height-two node in the
increasing tree is exterior-free and terminal, and the corresponding
height-zero statement holds in the conjugate tree. Thus absence of a
charged even exterior-free terminal node implies that every remote
`g` in (1) is zero. The converse statement that every such gate is
empty, or that every corresponding long side has a half-turn mate,
does not follow. Balanced occupied terminal nodes are permitted.
The model retains this distinction and places no mate assumption on
zero-current gates.

## Certified follow-up for 5063

The fixed-charge numerical tests were followed by a separate
minimum-population model with all remote currents zero, charge `G=c`,
and both native currents left free. Its independently checked integer
certificate gives

\[
 n_1\gerac{66,991,549}{500,001}>129.
\]

This removes the need to rely on the three numerical fixed-`f`
infeasibility statuses. The certificate uses all single-tile classes
and imposes no whole-edge pairing at a zero-current gate. Its exact
replay is `REMOTE_ZERO_MINIMUM_REPLAY.json`; see
`REMOTE_ZERO_OBSTRUCTION_5063.md` and
`AUDIT_REMOTE_ZERO_MINIMUM.md` for the theorem and audit.

The resulting conclusion is conditional and geometric: a hypothetical
5063 tiling with total odd population `3c` must contain a charged even
exterior-free terminal node. The unrestricted integer-gate model still
has only a time-limit result, and the entire `3c` mode remains open.

## A finite charged-node profile in the entire minimal mode

For a remote node, (1) reads `Q=d*g`. If `g>0`, at least `d*g`
positive parent tiles pass through its gate. The exact gate-capacity
bounds for the single height-one population are 44 at 3431 and 51
at 5063. If `g<0`, at least `d*abs(g)` negative parent tiles pass
through it, and there are only `c` negative height-one tiles in all.
Therefore every remote charge satisfies

\[
 \begin{array}{c|c}
 3431 & g\in\{-1,0,1\}\\
 5063 & g\in\{-1,0,1,2\}.
 \end{array}                                           \tag{2}
\]

There is also a legitimate aggregate across the upward and downward
remote gates in this particular situation. Each height-one tile has
one long edge, one hand, and one gate. Thus those parent-tile classes
are disjoint, and

\[
 d\sum_{\text{remote }g>0}g\le2c,\qquad
 d\sum_{\text{remote }g<0}|g|\le c.                    \tag{3}
\]

This is not an addition of two arbitrary prime-tree population budgets.
It counts disjoint long-edge classes of the one physical height-one
population.

For 3431, (3) allows at most two positive unit charges and at most
one negative unit charge: at most three charged remote nodes in all.
The all-zero profile is not excluded here. For 5063, there are at
most three positive charge units and at most one negative charge
unit. Together with (2), there are at most four charged remote
nodes. The independently verified zero-remote-current obstruction
requires at least one of them to be charged.

These bounds do not count balanced occupied remote nodes. A zero
entry may still contain an actual terminal population and cannot be
replaced by a closed or empty gate without an additional argument.
