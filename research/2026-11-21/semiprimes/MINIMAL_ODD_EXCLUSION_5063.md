# Every complete 5063 tiling has at least 215 odd-height tiles

21 November 2026. This note excludes the **entire** minimal odd-population
case, including arbitrary charged and balanced remote branches. The
original tileability questions for **5063 and 3431 remain OPEN**.

## 1. Statement and dependency boundary

Use the unit F2 tile `(a,b,c)=(35,13,43)` and put

\[
\rho=e^{i\pi/3},\quad R=\mathbb Z[\rho],\quad
z=(35+13\rho)/43,\quad d=a-b=22.
\]

In the path frame the board is

\[
T=\operatorname{conv}\{0,1849,2135z^2\}.
\]

A tile has short height `h` when its two short-side headings are
`z^h rho^j` and `z^h rho^(j+s)` for `j in Z/6` and `s in {-1,1}`.
Let `n_odd` count all tiles at odd short heights, in every phase and
both hands.

**Theorem.** A complete positive tiling of this board by the specified
5063 congruent tiles cannot have `n_odd=129`. Consequently every such
tiling satisfies

\[
\boxed{n_{\mathrm{odd}}\ge215.}
\]

Reflections, arbitrary T-junctions, and all phases permitted by the
previous complete-tiling reduction are included. No geometric search
window, guessed height cutoff, or assumed balanced-branch condition is
used.

The geometric inputs are the previously established
[actual-median localization](../../2026-11-20/semiprimes/continuation/charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md),
[complete minimal-odd phase classification](../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md),
[integer gate-current identities](../../2026-11-20/semiprimes/continuation/global-closure/median/PER_GATE_INTEGRALITY.md),
and [single-gate capacity theorem](../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md).
Their reference snapshot is commit
`e2f3cba5e1e046e78fae853ca17ff54c2e8f8a72`.
The present proof adds an exact finite contradiction after those
geometric reductions. It is not a Lean formalization or an external
referee report.

## 2. What every hypothetical 129-tile odd population must satisfy

Suppose `n_odd=3c=129`. The cited localization gives:

* all short heights belong to `{0,1,2}`;
* all 129 odd tiles have short height 1 and vertices in `zR`;
* their sign populations are exactly `n_+=86` and `n_-=43`;
* every remote even class is an actual exterior-free terminal node.

Divide height-one coordinates by `z`. A tile is specified by its
integral obtuse vertex `q=x+y rho`, rotation `j`, and hand `s in {-1,1}`.
Its other vertices and sign are

\[
u=q-a\rho^j,\qquad w=q+b\rho^{j+s},\qquad
\epsilon=s(-1)^j.
\]

The two gate labels are

\[
\phi(u)=a u_y-bu_x\pmod c,\qquad
\psi(u)=a u_x-bu_y\pmod c.
\]

Let `Q_+(r)` and `Q_-(r)` be the signed currents of height-one tiles
whose long side uses gate `r` in the upward or downward family. Every
height-one tile belongs to exactly one of these `2c` bins. The exact
neighboring-node equations give integers `g_+(r),g_-(r)` with

\[
Q_+(r)=22g_+(r)+86\mathbf1_{r=0},\qquad
Q_-(r)=22g_-(r)-43\mathbf1_{r=0}.                 \tag{1}
\]

Summation counts every signed tile once, so

\[
\sum_r Q_+(r)+\sum_r Q_-(r)=43,
\qquad \sum_r g_+(r)+\sum_r g_-(r)=0.             \tag{2}
\]

A zero remote `g` is permitted to have a nonempty balanced node.
No whole-side pairing is imposed at such a gate in this proof.

The certified positive capacity of any single gate is 51. Negative
current has magnitude at most the full negative population 43. Thus
each remote charge is in `{-1,0,1,2}`. Because the bins are disjoint,

\[
\sum_{r\ne0,\,\pm}\max(g_\pm(r),0)\le3,
\qquad
\sum_{r\ne0,\,\pm}\max(-g_\pm(r),0)\le1.         \tag{3}
\]

These are bounds on physical disjoint long-side bins, not a sum of two
overlapping prime-tree population budgets.

## 3. Exhaustive finite charge profiles

There are 84 remote bins. Represent the positive part of their charges
by a sorted multiset of at most three indices, each repeated at most
twice. Represent the negative part by either no index or one index
outside that multiset. This is a unique representation of the **net**
remote charge vector. Hidden balanced tile populations are still
allowed.

The native upward charge parameter is necessarily

\[
g_+(0)\in\{-5,-4,-3,-2\},
\]

by `-43<=86+22g_+(0)<=51`. The native downward charge is determined
by (2) and must satisfy `-43<=-43+22g_-(0)<=51`. Finally, the disjoint
sign reserves require

\[
\sum_{r,\pm}\max(Q_\pm(r),0)\le86,\qquad
\sum_{r,\pm}\max(-Q_\pm(r),0)\le43.              \tag{4}
\]

Every actual tiling supplies one profile in this list. The list has
**34,672,599** profiles before (4), and **17,800,359** after (4).
These counts were also obtained independently, without the recursive
enumerator. With `p` positive units on `k` positive bins and `m=0,1`
negative units, the number of remote choices is

\[
\binom{84}{k}\binom{k}{p-k}(84-k)^m,
\]

summed over allowed `k`, then multiplied by the directly checked native
choices. See [the independent enumeration audit](audit/PROFILE_CUT_AUDIT.md).

## 4. An exact dual inequality valid for every physical placement

A base certificate consists of a positive integer `D`, three integer
tables `F_j(x,y)` on `(Z/43Z)^2`, and integer gate weights
`lambda_+(r),lambda_-(r)`. Give a directed height-one segment the
difference of the appropriate axis table at its endpoints, using zero
outside the Euclidean class `zR`. Let `W(T)` be the total on the two
CCW short sides of a height-one tile.

There is no outer side at height one. Endpoint differences telescope
on every partial contact. Complementary whole long sides at height one
have normalized displacement `43 rho^j`, so their endpoint residues
agree. Short sides in other Euclidean classes have zero weight.
Consequently the complete tiling satisfies

\[
\sum_{T:\,h(T)=1} W(T)=0.                         \tag{5}
\]

Each supplied certificate is independently checked against all
`12c^2=22,188` translated orientation/hand classes:

\[
W(T)+\epsilon(T)\lambda_{s(T)}(r(T))\le D.        \tag{6}
\]

This finite check covers **all integral translations**, by periodicity,
not just a bounded catalogue of positions. Summing (6) over the real
height-one population and using (5) yields

\[
\sum_r\lambda_+(r)Q_+(r)+
\sum_r\lambda_-(r)Q_-(r)\le129D.                 \tag{7}
\]

The older zero-remote certificate has an additional charge multiplier
`t`; its form (7) is obtained by adding `t` to both gate-weight arrays,
because the total signed current is 43.

### All translations and geometric symmetries of a certificate

The map `(x,y)->(phi(x,y),psi(x,y))` has nonzero determinant modulo 43.
Thus one integral translation can produce any ordered pair of shifts
of the two gate-weight arrays. The endpoint tables are translated at
the same time. For each base inequality, every charge profile must
therefore satisfy

\[
\max_{u\in\mathbb Z/43}\sum_r\lambda_+(r+u)Q_+(r)
+\max_{v\in\mathbb Z/43}\sum_r\lambda_-(r+v)Q_-(r)
\le129D.                                        \tag{8}
\]

The equality between the maximum over all shift pairs and the sum of
the two separate maxima is exact. It does not assert that a translated
tiling fits the board. Only the universally checked column inequality
is translated.

All six rotations and both reflected variants supply further valid
column inequalities. A 60-degree rotation changes both signs together;
reflection exchanges the two gate families as prescribed by the
actual coordinate map. The independent checker derives these
permutations from the images of the residue points themselves.

## 5. The finite contradiction

The [certificate index](gate-model/CERTIFICATES_5063.json) lists every
base file and its SHA-256 hash. There are 65 base certificates and
780 transformed cuts. Their discovery used numerical linear programs,
but their proof consists of the subsequent integer checks and finite
exhaustion. In particular, no numerical solver's infeasibility status
is used as a premise.

| Verification item | Exact result |
|---|---:|
| Independently reconstructed single-tile inequalities | 1,442,220 |
| Base certificates | 65 |
| Serialized transformed cuts | 780 |
| Complete native/remote profiles | 34,672,599 |
| Profiles satisfying sign reserves | 17,800,359 |
| Profiles satisfying all exact cuts | **0** |

The final C++ execution starts from the **entire** profile universe.
Its result is [the complete enumeration record](gate-model/FINAL_PROFILE_ENUMERATION_5063.jsonl).
Every profile satisfying (1)--(4) violates at least one instance of
(8). Such a profile cannot come from the hypothetical tiling, proving
the theorem's exclusion of `n_odd=129`.

The independent [final replay](audit/FINAL_DUAL_REPLAY_5063.json)
checks all base inequalities, exact transformed arrays, geometric
symmetries, integer-range bounds, and complete profile accounting.
Separately, the current C++ enumerator agrees with an independently
written Cartesian enumeration on small finite controls. The adaptive
intermediate pool is also audited, but is **not needed** for the final
full-exhaustion argument.

## 6. From 129 to the unconditional lower bound 215

The established signed-population theorem gives
`G_odd=c` in this frame. Separate divisibility of positive and negative
odd-height populations by `c` makes `n_odd/c` odd. The earlier
single-block exclusion gives `n_odd>=3c`. The only allowed value below
`5c` was therefore `3c=129`, which has just been excluded. Hence
`n_odd>=5c=215` for every complete tiling of the specified board.

This does **not** prove that such a tiling exists, or that it cannot
exist with at least 215 odd tiles. It does not decide 3431, for which
the same complete profile exclusion has not been obtained. Nor does
it finish the classification of all products of two primes.

## 7. Replay and stronger local branch costs

From the repository root, the complete replay needs Python 3 with
assertions enabled and a C++17 compiler. NumPy, SciPy, and an optimizer
are unnecessary:

```sh
python3 research/2026-11-21/semiprimes/replay.py
```

The package also proves the independent
[single-accessible-gate terminal bounds](charged-branches/ISOLATED_GATE_TERMINAL_COST.md):
185 tiles for unit remote charge at 3431, and 301 or 602 for the
previously possible charges at 5063. Exact rational primal controls
show the limits of that local periodic relaxation. The final 5063
minimal-mode exclusion above uses the coupled parent profile, rather
than attempting to obtain a contradiction from those individual costs.

The [additive marginal dual construction](global-invariant/ADDITIVE_GATE_DUALS.md)
made later certificate discovery faster. It is used only to produce
candidate full-column inequalities; no equivalence between its
fractional feasible points and real tilings is asserted.
