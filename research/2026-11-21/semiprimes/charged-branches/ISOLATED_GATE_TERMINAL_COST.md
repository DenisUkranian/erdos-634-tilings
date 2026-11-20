# A charged remote terminal requires 301 tiles at 5063

21 November 2026. These are necessary conditions for a **complete** unit
F2 tiling in the proved minimal odd-population mode `n_odd=3c`. They
allow arbitrary reflections, partial contacts, and all the remote even
classes in the complete phase normal form. They do not decide either
3431 or 5063, and do not apply without qualification to an arbitrary
terminal node in a tiling with a larger odd population.

The main new consequence is

| Target | Nonzero remote charge `G=cg` | Previous minimum | New minimum |
|---:|---:|---:|---:|
| 3431 | `g=+/-1` | 111 | **185** |
| 5063 | `g=+/-1` | 129 | **301** |
| 5063 | `g=2` | 172 | **602** |

The previously established
[forced-charge theorem](../../../2026-11-20/semiprimes/continuation/global-closure/median/REMOTE_ZERO_OBSTRUCTION_5063.md)
therefore forces a remote even terminal population of at least **301**,
rather than merely 129, in every hypothetical 5063 tiling with 129 odd
tiles. Its actual parent bank still requires at least 22 tiles for unit
charge. Those 22 are already included in the 129 odd tiles.

## 1. Why each remote class has only one accessible long-edge gate

Use the path frame with

\[
 R=\mathbb Z[\rho],\qquad \rho=e^{i\pi/3},\qquad
 z=(a+b\rho)/c.
\]

The complete
[minimal-odd phase classification](../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md)
gives only short heights 0, 1, and 2. All height-one tiles have vertices
in `zR`; this is their unique occupied exact node in either prime tree.
The permitted even classes are

\[
 L_r^-=rz+R\quad(h=0),\qquad
 L_r^+=rz+z^2R\quad(h=2),\qquad 0\le r<c.
\]

For nonzero `r`, each is one actual exterior-free terminal node in its
appropriate tree. All height-two tiles, including the remote classes,
share the native height-two node in the decreasing-height tree. All
height-zero tiles share the native height-zero node in the increasing
tree.

Fix a nonnative height-two class `L=L_r^+`.

* Its upward long sides have height 3. Its increasing-tree node is
  terminal and exterior-free. Hence both banks of each maximal run at
  those child nodes contain only length-`c` long sides of height-two
  tiles. The partitions into equal lengths coincide, and every such
  side belongs to an actual whole half-turn pair in `L`.
* For a downward long side of height 1, inspect its edge node in the
  decreasing-height tree. If that node is the unique occupied native
  height-one node, the side is allowed to meet parent tiles. Otherwise
  it is an exterior-free child of the native height-two node. It has no
  height-one tiles. An occupied height-zero descendant would force
  its immediate height-one parent to be occupied by the published
  occupied-parent theorem, which is impossible. There are no lower
  short heights. Thus its entire descendant subtree contains no tile.
  The same equal-length-bank argument pairs every long side at this
  gate into an actual half-turn pair of height-two tiles.

In the second case a reflected mate would have short height zero and
would belong to the excluded descendant subtree. The actual mate is
therefore the half-turn mate at height two. Its vertices have the same
class `L`, since the shared long-edge endpoints and the half-turn
formula differ by vectors in `z^2R`.

Thus **every tile in `L` whose long side is not at the native parent
gate belongs to a whole half-turn pair within `L`**. The native gate
may also have pairs; they may be kept as pairs or treated as two singles.
This is a decomposition of the actual tiles. It does not identify a
balanced occupied node with an empty gate.

The height-zero case is symmetric, exchanging the two prime trees.
The only accessible long-edge gate is again the unique height-one
class. The proof uses the entire minimal-odd normal form, including
the occupied-parent theorem. Mere terminality in one tree would not
exclude all the other Euclidean parent gates.

## 2. Normalize the class and its accessible gate

For `L_r^+`, use origin `q_0=rz` and divide all differences by `z^2`.
Every normalized obtuse vertex is `q=(x,y) in R`. A tile has rotation
`j in {0,...,5}`, hand `s in {-1,+1}`, and sign

\[
 \epsilon=s(-1)^j.
\]

With `U_j=rho^j`, its acute endpoints are

\[
 u=q-aU_j,\qquad w=q+bU_{j+s}.
\]

For a downward tile, its long edge is at the accessible gate precisely
when `q_0+z^2u in zR`, or `zu in R`. Since `c^2=a^2+ab+b^2`, this
is the residue condition

\[
 \psi(u)=a u_x-bu_y=0\pmod c.                 \tag{1}
\]

In these normalized coordinates the class is therefore decomposed into:

1. downward single tiles satisfying (1);
2. whole half-turn pairs of arbitrary hand and residue.

For a height-zero class the accessible singles are upward and satisfy
`phi(u)=a u_y-bu_x=0 mod c`. Reflection `U -> conjugate(U)` swaps
the hands and changes the sign. In axial coordinates
`conjugate(x+y rho)=(x+y)-y rho`, and

\[
 \psi(\overline U)=a x+(a+b)y
 \equiv(-a/b)\phi(U)\pmod c.
\]

Thus it maps the upward zero gate to the downward zero gate. The
absolute-charge estimates below apply to both even heights.

## 3. An exact endpoint inequality for a single accessible gate

There are three integer tables `f_0,f_1,f_2` on `(Z/cZ)^2`, one for
each unoriented short-edge axis. For a directed segment at the selected
short height, assign the difference of the table values at its endpoints
when those endpoints lie in the selected Euclidean class, and use value
zero outside that class. Segments at other heights have weight zero.
Write `W(T)` for the sum on a tile's two counterclockwise short sides.

The whole-tiling sum isolates the selected class:

\[
 \sum_{T\in L}W(T)=0.                       \tag{2}
\]

Indeed, a whole long side at this short height has normalized displacement
`c U_j`, so its endpoint weights agree modulo `cR`; if one endpoint
lies outside `L`, both do. Short sides in other Euclidean classes have
zero weight. Endpoint differences telescope even on partial contacts
and subdivisions. The outer boundary contributes zero: its sides at
the selected even height have endpoints in the native Euclidean class,
which is disjoint from this nonnative class; its other sides have zero
weight by height. No truncation of a placement catalogue is involved.

The supplied tables satisfy two finite, exact families of inequalities:

\[
 W(T)+t\epsilon(T)\le D
 \quad\text{for every downward single at gate }\psi(u)=0,\tag{3}
\]

\[
 W(T)+W(T^*)\le2D
 \quad\text{for every half-turn pair }\{T,T^*\}.        \tag{4}
\]

All integral translations are covered by their residues modulo `cR`.
The exact coefficients are

| Tile | `D` | `t` | `t/D` |
|---|---:|---:|---:|
| `(33,7,37)` | 506 | 2093 | `91/22` |
| `(35,13,43)` | 13 | 83 | `83/13` |

A half-turn pair has opposite signs. Sum (3) over actual unpaired
singles and (4) over the disjoint paired tiles. By (2), for class
population `n_L` and signed population `G_L`,

\[
 Dn_L\ge tG_L.                               \tag{5}
\]

For negative `G_L`, use the same table after the normalized half-turn
`q -> -q`, `j -> j+3`. It preserves the zero gate and pair structure,
reverses all signs, and retains the zero total endpoint weight. Hence

\[
 \boxed{n_L\ge\frac{91}{22}|G_L|\quad(3431),\qquad
        n_L\ge\frac{83}{13}|G_L|\quad(5063).}           \tag{6}
\]

These are exact rational inequalities. The numerical optimization was
only used to obtain candidate tables; the integer column checks and
summation prove (6).

## 4. Signed divisibility gives the stated integer populations

Each remote class is an ordinary exact node, so

\[
 n_L^+,n_L^-\in c\mathbb Z,\qquad G_L=cg,\qquad
 n_L/c\equiv g\pmod2.
\]

At 3431, the previously proved gate capacity restricts nonzero remote
charges to `g=+/-1`. Equation (6) gives `n_L/c>=91/22>4`; the block
count is odd, hence `n_L>=5c=185`.

At 5063 the permitted nonzero charges are `g in {-1,1,2}`. For a unit
charge, `n_L/c>=83/13>6`; odd block parity gives `n_L>=7c=301`.
For `g=2`, `n_L/c>=166/13>12`; even block parity gives
`n_L>=14c=602`.

The remote class populations at heights zero and two are disjoint
physical populations. Consequently in the minimal-odd mode, if
`S=sum_remote |g_r|`,

\[
 n_{\rm remote,charged}\ge5cS\quad(3431),\qquad
 n_{\rm remote,charged}\ge7cS\quad(5063).              \tag{7}
\]

The bounds on charge magnitudes quoted above are needed when replacing
the general rational bound by (7). Balanced occupied remote classes
are not included in `S`; each still has at least `2c` tiles.

For 5063, the prior zero-remote-current obstruction proves `S>=1`.
Thus the entire minimal-odd mode has at least 129 odd tiles and at
least 301 tiles in a charged even remote class. This only proves a
lower bound of 430 on those disjoint populations. It leaves room
within 5063 and is not an impossibility argument. No `c^2` charged
terminal lower bound is claimed.

## 5. Independent exact replay and a positive geometric control

The certificate files are `terminal_3431_exact.json` and
`terminal_5063_exact.json`. The standalone standard-library verifier
`verify_terminal_gate.py` does not import the LP generator. It
reconstructs every counterclockwise polygon, recognizes short-edge
axes using the exact Eisenstein norm, checks the accessible-gate
condition, and reconstructs the actual half-turn mate. It verifies:

| Tile | Single columns | Distinct half-turn pairs | Maximum single score | Maximum pair score |
|---|---:|---:|---:|---:|
| `(33,7,37)` | 222 | 8,214 | 506 | 1,012 |
| `(35,13,43)` | 258 | 11,094 | 13 | 26 |

Every inequality is checked with integers. The verifier also builds the
standard `c`-grid of the scale-`c` tile, the charged triangular part of
the previously verified
[charged terminal polygon](../../../2026-11-20/semiprimes/continuation/common-obstruction/terminal/CHARGED_TERMINAL_PATCH.md).
After a half-turn it has `c^2` tiles, charge `+c`, zero total endpoint
weight, and precisely `c` unpaired long edges, all at the selected
gate. Both positive controls pass the new inequalities. They are
one-gate tiled domains, not complete tilings of the target boards.

```sh
python3 verify_terminal_gate.py terminal_5063_exact.json \
  terminal_3431_exact.json --out TERMINAL_GATE_REPLAY.json
```

The independent geometric and certificate review is recorded in
[`../audit/TERMINAL_GATE_AUDIT.md`](../audit/TERMINAL_GATE_AUDIT.md).
Neither this exact replay nor that internal review is Lean formalization
or external peer review. The conclusion remains the necessary bound (6),
with the exact minimal-mode application above.

## 6. The one-class periodic relaxation is now solved exactly

There is also an exact limit to this particular proof route. The reduced
generator `terminal_gate_reduced_lp.py` uses endpoint functions of the
single residue `psi`, only `3c` endpoint rows, six possible single
columns, and `6c` half-turn-pair columns. It produces rational **fractional
residue inventories**, not actual placements, at the following populations
with charge `+c`:

| Tile | Periodic fractional population | Population/charge |
|---|---:|---:|
| `(33,7,37)` | `3367/22` | `91/22` |
| `(35,13,43)` | `3569/13` | `83/13` |

Each reduced column of weight `v` lifts uniformly with weight `v/c` to
the `c` two-coordinate residues having its `psi` value. A pair is lifted
with its actual mate. The independent standard-library checker
`verify_periodic_primal.py` reconstructs those tiles and verifies all
`3c^2` exact rational endpoint-current equations, nonnegativity, charge
`c`, and equality with the already checked dual value. The saved replay
is `PERIODIC_LIMIT_REPLAY.json`.

Thus (6) is optimal for this **continuous periodic endpoint relaxation**,
even when all two-coordinate residue equations modulo `cR` are retained.
No stronger linear bound within that same relaxation can establish a
larger coefficient. This is not a counterexample to a stronger geometric
bound: finite support on actual supporting lines, nonoverlap, the board
boundary, and simultaneous interaction with the parent are absent. The
exact witness does not assert feasibility with integer tile multiplicities.

```sh
python3 verify_periodic_primal.py terminal_5063_reduced.json \
  terminal_3431_reduced.json --out PERIODIC_LIMIT_REPLAY.json
```
