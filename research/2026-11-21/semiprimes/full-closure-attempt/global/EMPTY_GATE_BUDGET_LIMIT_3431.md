# Integer gate and core budgets in the 111-tile 3431 mode

21 November 2026. **3431 and 5063 remain open.** In the minimal odd
mode for 3431, combining exact core certificates, whole-edge mate
constraints, and the population budget gives three new restrictions:

- The charge profile `(-3,2,1,0)` has at most 32 occupied balanced
  remote even nodes; the earlier odd-population count allowed 33.
- The profile `(-3,3,0,0)`, with native currents `(-4,41)` and all
  remote currents zero, is excluded by an exact endpoint certificate.
- In the profile `(-2,2,0,0)`, with native currents `(22,15)` and all
  remote currents zero, at most 34 remote gates contain any odd-parent
  tiles. The visibility theorem consequently permits at most 34 occupied
  remote even nodes.

These are necessary conditions on a hypothetical tiling. The surviving
rows below are not constructions or feasibility certificates. The result
is confined to the established 111-odd-tile normal form for 3431; it does
not exclude that whole mode, the larger odd populations, or 5063.

## 1. Empty gates and whole-edge mates

Use the path frame of the established minimal-odd normal form, with
`(a,b,c)=(33,7,37)`, `n_odd=111`, signs `(74,37)`, and the native
height-one class `zR`. Every short height is 0, 1, or 2. Write a residue
column as `(q,j,s)`, with `q in (Z/cZ)^2`, and put

`u=q-a U_j`, `w=q+b U_(j+s)`.

The actual half-turn mate across its whole long edge has residue label

\[
 (q,j,s)^*=(q-aU_j+bU_{j+s},j+3,s).                 \tag{1}
\]

This is a fixed-point-free involution. The mate has the opposite sign,
the same hand, and the same long-edge gate. Its acute beta endpoint is
`w`, and the original endpoints `u,w` belong to the same gate.

If the corresponding nonnative even node is empty, the established
closed-gate theorem forces every incident actual height-one tile to have
this whole half-turn mate. Consequently the aggregate residue inventory
satisfies `x_t=x_(t*)` at that gate. Zero signed gate current alone does
not imply this equality.

For each two-element mate orbit cancel `min(x_t,x_(t*))` copies from
each side. For integral `x`, the uncancelled population at a gate is

\[
 D_g=\sum_{\{t,t^*\}\text{ at }g}|x_t-x_{t^*}|.
\]

It satisfies `D_g>=|Q_g|` and `D_g=Q_g (mod 2)`. A zero-current
gate with nonzero mate defect therefore uses at least two uncancelled
columns. Also `sum D_g<=111`. This is cancellation of residue counts;
it does not assert actual spatial matching.

Three different notions must be kept separate:

| Gate or node condition | What it implies here |
|---|---|
| A remote zero-current gate is **mate-defective**, meaning `D_g>0` | Its even node must be occupied; it uses at least two uncancelled odd residue columns. |
| A remote zero-current gate is **parent-used**, meaning at least one odd long edge belongs to it | It has equal positive and negative odd populations, both nonzero. Its residue mate defect may be zero. |
| A remote even node is physically occupied | It costs at least 74 tiles when balanced. The visibility theorem below forces its parent gate to be used, although its residue mate defect may be zero. |

Every mate-defective gate is parent-used. The identification needed for
bounding occupied nodes is supplied by the following additional geometric
argument, not by zero signed current or a periodic mate equality.

### Visibility of occupied remote even nodes

Under the one-native-odd-cell, three-height hypotheses above, an occupied
remote even node must have a nonempty odd-parent long-edge gate. To see
this, suppose its parent long-edge population were zero. Integral offsets
then force every selected short-side interval to cancel against another
tile in the same selected cell; there is no exterior short side and no
complementary odd long side. The one-accessible-gate theorem pairs all
inaccessible long sides. The remaining boundary has only long sides of
length `c` at height one.

Normalized to the selected short lattice, each such long vector is a unit
rotation of `(a,b)` or `(a+b,-b)`. It is primitive because `gcd(a,b)=1`.
Thus selected long edges cannot overlap partially or contain another
selected vertex in their relative interiors. The nonempty boundary is a
balanced embedded graph of whole length-`c` edges. It contains a simple
cycle whose vertices lie in one translate of `c*z*R`. The existing
supported-cycle theorem forbids this in either target board. Opposite-bank
odd T-junctions are allowed and do not split the selected graph.

The complete proof is in
[INVISIBLE_EVEN_NODES](../target3431/INVISIBLE_EVEN_NODES.md), with the
[independent visibility audit](INVISIBLE_EVEN_NODES_AUDIT.md). Consequently
the number of occupied balanced remote even nodes is at most the number
of parent-used zero-current gates. A used gate can still have an empty
even node if its odd long edges pair with one another.

## 2. The thirteen charge profiles

The proved gate-capacity inequalities and sign inventories give
`-37<=Q_g<=44`. A remote current is `26g`, so its nonzero charge is
`g=+1` or `g=-1`. Let `s_+,s_-` count these remote gates. The
native charge variables and currents are

\[
 u=74+26g_u,\qquad v=-37+26g_d,
\]

with `g_u in {-4,-3,-2}` and `g_d in {0,1,2,3}`. They satisfy

\[
 g_u+g_d+s_+-s_-=0,
\]
\[
 u_++v_++26s_+\le74,\qquad
 (-u)_++(-v)_++26s_-\le37.
\]

Thus `s_+<=2`, `s_-<=1`, and exactly thirteen charge profiles remain.
Put `S=s_++s_-`. From here onward `K` denotes the number of **occupied
balanced remote even nodes**. Let `K_parent,0` count parent-used
zero-current remote gates. Every such used gate has at least one positive
and one negative odd tile. Visibility and the unsigned odd populations
therefore give

\[
 K\le K_{\rm parent,0}\le K_{\rm orbit}:=
 \frac{111-|u|-|v|-26S}{2}.                         \tag{2}
\]

Every numerator in the finite list is nonnegative and even. The notation
`K_orbit` retains the earlier numerical cap, but its application to actual
occupied nodes now uses visibility and unsigned gate counts. It does not
assume that every occupied node produces a residue mate defect.

## 3. The native population floors

### The exceptional height-two core

In this reflected path frame the exceptional height-two core has sign
residues `(8,19)` modulo 37 and charge `26+37g_u`. The independently
checked inhomogeneous core certificates give:

| `g_u` | Exact rational lower bound | Population residue modulo 74 | Rounded core floor `C_u` |
|---:|---:|---:|---:|
| -2 | `21064508116/100000001` | 64 | 212 |
| -3 | `35970666295/100000001` | 27 | 397 |
| -4 | `51093809348/100000001` | 64 | 582 |

The middle population residue is also written as 101 before reduction
modulo 74; the last is also written as 138. The rounding uses separate
sign congruences, not rounding to the next arbitrary integer. These
certificates include the nonzero exterior endpoint source of the core.

### The native ordinary height-zero node

The native height-zero node has charge `37g_d`. The homogeneous
one-accessible-gate charged inequality applies to it despite its exterior
base: at short height zero, its only exterior side has length `c^2`.
The two endpoints agree modulo `cR`, so every periodic endpoint weight
used in the certified `91/22` inequality has zero total on that side.
Other exterior sides have height two and weight zero.

Every long side outside the unique native height-one parent gate has an
actual half-turn mate. Height minus one is absent. A nonnative
height-one child has neither an occupied node nor an exterior-containing
descendant in this normal form. Therefore the same single/pair
decomposition as in the remote-node proof applies. Its periodic exterior
term is zero, as checked above. Consequently

\[
 n_0/c\ge(91/22)|g_d|.
\]

Separate sign divisibility gives `n_0/c = g_d (mod 2)`. It follows
that the necessary native height-zero floors are

\[
 C_d=37f(g_d),\qquad
 f(0)=0,\quad f(1)=5,\quad f(2)=10,\quad f(3)=13.   \tag{3}
\]

The nonzero-charge floors are 185, 370, and 481. At `g_d=0` the node
may be empty. The list of permitted phase classes does not force each
of them to be occupied, so 74 is not an unconditional floor for this
native zero-charge node.

## 4. The global budget in this normal form

Each charged remote node costs at least 185 tiles. Every occupied
balanced remote node costs at least 74 tiles. The height-zero and
height-two classes are disjoint physical
populations, so these costs can be added to the native costs and to the
111 odd tiles:

\[
 3431\ge C(K):=111+C_u+C_d+185S+74K.                \tag{4}
\]

This adds disjoint populations in the proved normal form, not the entire
budgets of two prime trees. Other occupied nodes can only increase the
total. The population cap is

\[
 K_{\rm budget}=
 \left\lfloor\frac{3431-111-C_u-C_d-185S}{74}\right\rfloor.
\]

The complete table includes the endpoint refinements proved in Section 5.
`C(K_orbit)` is the necessary total from (4) at the earlier orbit cap.
The last column is the cap after all inputs in this note; an excluded
row has no surviving `K`.

| `g_u` | `g_d` | `s_+` | `s_-` | `(u,v)` | `K_orbit` | `K_budget` | `C(K_orbit)` | Remaining `K` cap |
|---:|---:|---:|---:|:---:|---:|---:|---:|:---|
| -4 | 2 | 2 | 0 | (-30,15) | 7 | 27 | 1951 | 7 |
| -4 | 3 | 1 | 0 | (-30,41) | 7 | 28 | 1877 | 7 |
| -3 | 1 | 2 | 0 | (-4,-11) | 22 | 32 | 2691 | 22 |
| -3 | 2 | 1 | 0 | (-4,15) | 33 | 32 | 3505 | **32** |
| -3 | 2 | 2 | 1 | (-4,15) | 7 | 27 | 1951 | 7 |
| -3 | 3 | 0 | 0 | (-4,41) | 33 | 33 | 3431 | **Excluded** |
| -3 | 3 | 1 | 1 | (-4,41) | 7 | 28 | 1877 | 7 |
| -2 | 0 | 2 | 0 | (22,-37) | 0 | 37 | 693 | 0 |
| -2 | 1 | 1 | 0 | (22,-11) | 26 | 37 | 2617 | 26 |
| -2 | 1 | 2 | 1 | (22,-11) | 0 | 32 | 1063 | 0 |
| -2 | 2 | 0 | 0 | (22,15) | 37 | 37 | 3431 | **34** |
| -2 | 2 | 1 | 1 | (22,15) | 11 | 32 | 1877 | 11 |
| -2 | 3 | 0 | 1 | (22,41) | 11 | 33 | 1803 | 11 |

The core and population inputs remove `K=33` from the fourth row:
its necessary total is 3505, whereas `K=32` costs exactly 3431. The
budget alone does not exclude that whole profile. The excluded sixth
row and the reduction from 37 to 34 in the eleventh row require the
endpoint certificates below. No other displayed profile or orbit cap is
removed by these inputs.

## 5. Two exact endpoint refinements

### Native currents `(-4,41)`, all remote currents zero

The profile-exclusion dual in
`../target3431/GATE_EXCESS_CERTIFICATE.json.gz` bounds every residue
tile column by `100000002`. Its right-hand side is `15776947829`,
so every nonnegative inventory satisfying these endpoint and gate
equations would have population at least

\[
 \frac{15776947829}{100000002}>111.
\]

This excludes the entire row `(-3,3,0,0)`. It does not apply to
`(-3,3,1,1)`, whose charged remote gates change the dual right-hand side.

### Native currents `(22,15)`, all remote currents zero

For the fixed sign inventory `(74,37)`, define the minority excess

\[
 E=n^-_{\rm native}
   +\sum_{\text{remote }g}\max(n^-_g-1,0).
\]

The native term sums negative odd columns at the two native gates.
The exact excess dual gives

\[
 E\ge\frac{2173857481}{1000000000}>2.
\]

For an integer inventory, `E>=3`. Every parent-used remote zero-current
gate contains equal positive and negative populations, so its negative
population is at least one. If `K_parent` counts those gates, summing
the 37 negative columns gives

\[
 E=37-K_{\rm parent}.
\]

Consequently `K_parent<=34`. The visibility theorem now gives `K<=34`
for actual occupied remote even nodes; all are balanced in this profile.
The endpoint certificate alone bounds parent-used gates, while the
geometric theorem supplies this further interpretation. This gives
`C(34)=3209` in (4). It does not exclude the charge profile, because no
incompatible lower bound on the occupied-node count has been proved.

## 6. What the earlier weaker projection argument establishes

Before the inhomogeneous core certificates were added, the only core
input in this calculation was its sign-residue cost

\[
 C_u^{\rm weak}=27+37|g_u+1|.
\]

For that weaker arithmetic relaxation, one can optionally allocate 74
tiles to the native `g_d=0` node, use the nonzero native costs in (3),
185 per charged remote node, and 74 per mate-defective zero-current
remote gate. All thirteen profiles and all 214 choices
`0<=K<=K_orbit` then fit within 3283 tiles. The deficit to 3431 is
always a nonnegative multiple of 74; adding balanced sign blocks in a
native node fills that arithmetic deficit without changing any charge.

Accordingly, empty-gate mate equalities plus those weaker population
costs do not shrink the projection onto integer odd inventories:
declare every mate-defective gate occupied, declare other zero-current
gates empty, and choose the indicated arithmetic even populations.
This conditional construction does not assert that such an integer odd
inventory exists, or that the selected even populations are geometrically
realizable. It only explains why those particular weaker costs could not
give a contradiction. The stronger core and endpoint certificates in
Sections 3–5 change the projection and must be retained.

## 7. Dependencies and exact replay

The phase normal form and gate equations are in
[MINIMAL_ODD_PHASE_CLASSIFICATION](../../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md)
and [PER_GATE_INTEGRALITY](../../../../2026-11-20/semiprimes/continuation/global-closure/median/PER_GATE_INTEGRALITY.md).
The homogeneous charged cost is in
[ISOLATED_GATE_TERMINAL_COST](../../charged-branches/ISOLATED_GATE_TERMINAL_COST.md).
The new core certificates and checker are in
[core-budget](../core-budget/), and the endpoint certificates are verified
by [verify_gate_excess.py](../target3431/verify_gate_excess.py).

Run, from the repository root:

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/global/verify_empty_gate_budget.py
```

The standard-library checker verifies all three inhomogeneous core
certificates, independently reconstructs every one of the 16428 odd
residue columns for both endpoint certificates, enumerates the thirteen
strengthened profiles, and checks the complete residue mate involution
at the control and target shapes `(5,3,7)`, `(33,7,37)`, and
`(35,13,43)`. It also retains the 214 weaker arithmetic allocations as
explicit projection controls. The exact report is
[EMPTY_GATE_BUDGET_REPLAY.json](EMPTY_GATE_BUDGET_REPLAY.json).

The universal orbit-cancellation implication, the visibility theorem,
and the native height-zero extension are the written arguments cited
above. The supported-cycle dependency also has its own exact board
geometry replay. The present checker establishes its stated finite
column checks and arithmetic consequences; it is not a nonexistence
certificate for either full target.
