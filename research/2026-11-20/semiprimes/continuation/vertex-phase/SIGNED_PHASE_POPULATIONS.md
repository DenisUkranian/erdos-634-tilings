# Signed populations in individual phase nodes

20 November 2026. Necessary conditions for arbitrary tilings in the
project's exact `Geometry` convention. This continues the phase-tree
population argument and uses the two established direction characters.
It does not decide the 3431 or 5063 board.

## 1. Fixing the sign convention

Let the primitive odd tile have sides `a>b>0`, with
`c^2=a^2+ab+b^2`, and put `d=a-b`, `rho=exp(i*pi/3)`, and
`z=(a+b rho)/c`. The target has counterclockwise vertices

\[
 O=0,\quad X=A=b(2a+b),\quad Y=B\rho=a(a+2b)\rho.
\]

In `Geometry`, the placement `(q,h,j,s)`, with `s=+1` or `-1`, has
vertices

\[
 u=q-a z^h\rho^j,\qquad q,\qquad
 w=q+b z^h\rho^{j+s}.
\]

The counterclockwise order is `(u,q,w)` for `s=+1` and `(w,q,u)`
for `s=-1`. Define its sign to be

\[
 \boxed{\epsilon=s(-1)^j.}
\]

This is the alternating direction sign of its counterclockwise
`a` edge. Both sign classes consist of ordinary positive-area tiles;
the signs here are not geometric area signs.

For a directed segment of length `L` with heading `z^h rho^j`, use

\[
 C=L(-1)^j,\qquad C_*=L(-1)^{h+j}.
\]

Both characters reverse on reversal and add on subdivided segments.
For the first hand, the directed sides have data
`(a,h,j)`, `(b,h,j+1)`, `(c,h+1,j+3)`. For the second hand they have
`(b,h,j+2)`, `(a,h,j+3)`, `(c,h-1,j)`. Consequently a tile contributes

\[
 C(T)=(d-c)\epsilon,
 \qquad C_*(T)=(d+c)(-1)^h\epsilon.
\tag{1}
\]

The numerical sign labels below are for this fixed board frame and
placement convention. A normalization that reverses the direction
character must also interchange the positive and negative labels.

## 2. Nodewise signed congruence

Use either prime phase tree from the
[phase-tree population theorem](../phase-height/PHASE_BRANCHES.md).
For a node `v` at physical short height `h`, let

\[
 n_v^+=\#\{T:\text{short node}(T)=v,\ \epsilon(T)=+1\},
 \quad
 n_v^-=\#\{T:\text{short node}(T)=v,\ \epsilon(T)=-1\},
\]

and write `n_v=n_v^++n_v^-`, `G_v=n_v^+-n_v^-`. These are exact-node
populations, not populations of the entire descendant subtree.

On any supporting line of height `h`, directed edge cancellation
holds separately in its phase node: endpoints on one maximal run
differ by integral physical offsets. The selected short edges of
tiles in `v` contribute `(a-b)G_v` after summing the three axes.
Every complementary long edge contributes an integral multiple of
`c`. Hence

\[
 dG_v\equiv C(\text{exterior edges in node }v)\pmod c.
\tag{2}
\]

At every ordinary node the exterior term is zero modulo `c`: the
only nonzero-height outer side has length `c^2`, and the two
height-zero sides belong to the single core node. At the height-zero
core both axial boundary directions have positive sign, so that term
is `A+B`.

Since `gcd(d,c)=1`, this proves

\[
 G_v\equiv0\pmod c\quad\text{at every ordinary node},
 \qquad dG_0\equiv A+B\equiv N\pmod c
\tag{3}
\]

at the core. Here
`N=(a+2b)(2a+b)=2c^2+3ab` and `N+d^2=3c^2`, so the latter
congruence is equivalently `G_0=-d (mod c)`.

The earlier phase theorem gives `n_v=0 (mod c)` for ordinary nodes
and `n_0=N (mod c)` for the core. As `c` is odd, division by 2
modulo `c` is permitted. Therefore

\[
 \boxed{n_v^+,n_v^-\in c\mathbb Z_{\ge0}}
 \quad\text{at every ordinary node}.
\tag{4}
\]

For the core let `j=N mod c`, and let `r_+`, `r_-` denote the least
nonnegative residues

\[
 r_+\equiv (N-d)/2\pmod c,
 \qquad r_-\equiv (N+d)/2\pmod c.
\tag{5}
\]

The fractions in (5) mean multiplication by the inverse of 2 modulo
`c`. The actual populations have the form

\[
 \boxed{n_0^+=r_++c t_+,\qquad
 n_0^-=r_-+c t_-,\qquad t_+,t_-\ge0.}
\tag{6}
\]

In particular the lower bound for the core is `r_++r_-`, which can
be `j+c` rather than `j`.

The ordinary-node lower bound remains relevant: a nonzero population
is at least `2c`, even if only one sign is present. An occupied node
cannot have just one block of `c` tiles. The
[no-vacant-ancestor theorem](NO_PHASE_GAPS.md) forces this occupancy
for every exterior-free ancestor of a required tile.

## 3. Whole-board totals and height parity

The three directed target sides have data `(A,0,0)`, `(c^2,2,1)`,
and `(B,0,4)`. Both characters therefore have boundary total

\[
 A-c^2+B=3ab.
\]

Summing (1) over all tiles cancels internal edges and yields

\[
 G_{\rm all}=\sum_T\epsilon(T)=-(c+d),
 \qquad
 G_*=\sum_T(-1)^{h(T)}\epsilon(T)=c-d.
\tag{7}
\]

The full positive and negative populations are consequently

\[
 \boxed{P=(N-c-d)/2,\qquad Q=(N+c+d)/2.}
\tag{8}
\]

The signed differences at odd and even short heights are separately
fixed:

\[
 \boxed{G_{\rm odd}=-c,\qquad G_{\rm even}=-d.}
\tag{9}
\]

The height here is the physical `h` in `Geometry`. Reversing descent
for the conjugate prime tree does not change either the tile sign or
the parity of this physical height.

| `N` | Tile `(a,b,c)` | Core residues `(r_+,r_-)` | Full `(P,Q)` | Remaining positive/negative `c`-blocks `(K_+,K_-)` |
|---:|---|---|---|---|
| 3431 | `(33,7,37)` | `(19,8)` | `(1684,1747)` | `(45,47)` |
| 5063 | `(35,13,43)` | `(5,27)` | `(2499,2564)` | `(58,59)` |
| 143 | `(5,3,7)` | `(4,6)` | `(67,76)` | `(9,10)` |

Here `K_+=(P-r_+)/c`, `K_-=(Q-r_-)/c`. The 143 row is a positive
control for the formulas. Its signed core lower bound is 10 although
`143 mod 7=3`. The other two signed core lower bounds equal their
ordinary residues, 27 and 32.

For example, 46 ordinary nodes at 3431 cannot all contain a required
positive tile. Each would require at least one positive block of 37,
but only 45 such blocks remain after the mandatory core residue.
The unsigned bound of 46 nodes by itself does not see this obstruction.

### A parity bound for the number of ordinary nodes

Let `R_all` be the total number of occupied ordinary nodes in either
prime tree. At each odd physical height, every node is ordinary.
Equations (4) and (9) give

\[
 \sum_{v:\ h(v)\text{ odd}}\frac{n_v^+-n_v^-}{c}=-1.
\]

Modulo 2, the summand has the same parity as `n_v/c`. Thus the sum
of the population blocks at odd heights is odd. At least one
ordinary node has an odd number of blocks. Since an occupied ordinary
node has at least two blocks, that particular node has at least three.
Summing over all ordinary nodes and adding the signed core minimum
proves

\[
 \boxed{N\ge r_++r_-+2cR_{\rm all}+c.}                 \tag{10}
\]

The resulting upper bounds for the total number of occupied ordinary
nodes are **45 at 3431**, **58 at 5063**, and **9 at the 143 control**.
In particular any finite set of required ordinary nodes has at most
45 or 58 members. The node carrying the extra block need not belong
to that finite set: (10) is a bound on the complete tiling, so the
same numerical upper bound still applies to its subsets.

This supplies the additional block without locating a special tile
or assuming that a finite catalogue exhausts the placements. For an
exterior-free demand set, the no-vacant-ancestor theorem establishes
the required occupancy before this count is applied.

## 4. Safe projections for a finite partial catalogue

For an ordinary node introduce nonnegative integers `u_v^+`, `u_v^-`
representing full-population blocks, so `n_v^+=c u_v^+` and
`n_v^-=c u_v^-`. If selected placements contribute `s_v^+`, `s_v^-`,
then the necessary lower bounds are

\[
 u_v^+\ge\lceil s_v^+/c\rceil,
 \qquad u_v^-\ge\lceil s_v^-/c\rceil.
\]

Every node required to be occupied also satisfies
`u_v^++u_v^->=2`. The core excess blocks `t_+`, `t_-` satisfy (6)
and the corresponding selected-population lower bounds.

The counts of selected catalogue columns themselves need not be
multiples of `c`; unlisted completion tiles may supply the rest.
The block variables reserve that missing population. Similarly,
selected positive and negative counts have unconditional upper bounds
`P` and `Q`, whereas equality requires a full tiling or explicit
completion variables.

There is a useful exact elimination of the unknown population slack
when the height parity is recorded. Let `P_e,P_o,Q_e,Q_o` be the
positive and negative block amounts already allocated at even and
odd heights. Include the core excess blocks in the even amounts,
but remove the fixed core residues before forming these four totals.
All four amounts are nonnegative integers.

Put

\[
 \delta_e=(d+r_+-r_-)/c.
\]

Its values are 1 at 3431 and 0 at 5063 and 143. Equation (9) says
that the completed block counts have the form

\[
 (P_e^{\rm full},P_o^{\rm full},Q_e^{\rm full},Q_o^{\rm full})
 =(E,O,E+\delta_e,O+1),\qquad E+O=K_+.
\]

Thus a numerical completion of the four allocated block amounts is
possible if and only if

\[
 \max(P_e,Q_e-\delta_e)+\max(P_o,Q_o-1)\le K_+.
\tag{11}
\]

Equivalently, the following four linear inequalities all hold:

\[
\begin{aligned}
 P_e+P_o&\le K_+,\\
 Q_e+Q_o&\le K_-,\\
 P_e+Q_o&\le K_++1,\\
 Q_e+P_o&\le K_++\delta_e.
\end{aligned}
\tag{12}
\]

Indeed `K_-=K_++delta_e+1`; expanding the two maxima in (11)
gives precisely the four inequalities. Conversely take `E` and `O`
initially equal to those two maxima and distribute the remaining
nonnegative integer slack to make their sum `K_+`. Their induced
negative counts then dominate the allocated negative amounts as well.

This equivalence is only for the population projection: it does not
construct geometric completion tiles. Its necessity holds for any
finite partial catalogue, without assuming that catalogue exhaustive.
The four inequalities may therefore be used for unconditional
pruning of simultaneous selected placements.

Apply a separate copy of these constraints to each prime tree.
Adding the two trees' budgets would double-count the same actual
tiles and is not justified.

## 5. Coupling the two trees through physical height

The two trees count the same tiles, so their global costs cannot be added.
They can nevertheless be coupled more strongly than two separate budgets.
For every physical short height `h` and sign introduce a nonnegative integer
capacity `H_h^sign`. At `h!=0` its full-tiling witness is the actual signed
height population divided by `c`. At `h=0` subtract the fixed core residue
`r_sign` before dividing by `c`.

Each tree partitions the tiles of a fixed height into its exact short nodes.
Its exceptional core occurs exactly once, at physical height zero. Thus the
sum of the allocated blocks of either tree at height `h` must satisfy

\[
 \sum_{v:\,\operatorname{height}(v)=h}u_{v,\,\mathrm{tree}\,i}^{\mathrm{sign}}
 \le H_h^{\mathrm{sign}},\qquad i\in\{1,2\}.
\tag{13}
\]

Use these common height capacities, separated by even and odd `h`, in the
four inequalities (12). The actual height populations give a witness for
every full tiling, including when the generated placement catalogue omits
most of its tiles. If node capacities have been reduced to witnesses for a
partial catalogue, they remain below the actual height populations.

One may further reduce each `H_h^sign` to the maximum of the two allocated
tree sums at that height. Every constraint on a height capacity other than
(13) is an upper bound, so this reduction preserves feasibility. The resulting
restriction accounts for demands at different physical heights together:
the sum of the per-height maxima can exceed the maximum of the two global
tree sums. This supplies a strict strengthening without counting any tile
twice. The physical height of a node with stored level `l` is `h=l` in the
positive-valuation tree and `h=-l` in the conjugate tree. Its parity is
unchanged.

## 6. Exact replay

Run `python3 verify_signed_arithmetic.py` with assertions enabled.
The checker uses rational Eisenstein coordinates to verify the
placement convention, counterclockwise orientation, both tile
characters, both boundary characters, the core residues, and the
numeric block budgets for the two targets and the 143 control. The
nodewise cancellation and arithmetic lifting to populations are the
arguments in Section 2.

