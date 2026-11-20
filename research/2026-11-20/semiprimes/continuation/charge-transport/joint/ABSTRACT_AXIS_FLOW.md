# An exact two-tree axis-flow countermodel

20 November 2026. This note records a limit of the current population
and phase-transport relaxation. **It is not a tiling, a partial geometric
packing, or a counterexample to an unrestricted impossibility theorem.**
Both target questions remain open.

The model below uses exactly `N` nonnegative integer tile copies and
satisfies both prime trees, the joint-cell signed reserves, every signed
axis current in each joint cell, whole-side boundary-length partitions,
closed-gate half-turn pairing, and connectivity of an abstract contact-port
graph. It has no common vertex coordinates, per-supporting-line identities,
planar sector embedding, nonoverlap or coverage.

In particular, the listed population/transport conditions cannot by
themselves force the population above `N`, or force an occupied
exterior-free gate. More geometric information is necessary.

## 1. Four joint cells and two occupied populations

Use the standard frame

\[
 R=\mathbb Z[\rho],\quad z=(a+b\rho)/c,\quad
 A=b(2a+b),\quad H=a(a+2b),\quad d=a-b,
\]

with outer vertices `0,A,H*rho`. The height-two outer side goes from
`A` to `H*rho` and has displacement `c^2*rho*z^2`.

The joint cells are

| Name | Height | Euclidean coset | Own tile population |
|---|---:|---|---:|
| Core | 0 | `R` | `N-Kc` |
| Closed gate | 1 | `zR` | 0 |
| Middle spine | 1 | `H*rho+zR` | `Kc` |
| Outer edge | 2 | `A+z^2R` | 0 |

Here `K>=3` is odd and is chosen so the counts below are nonnegative.
The middle cell is exterior-containing in both prime trees. In the
increasing-height tree it contains the ancestor of the outer height-two
edge. In the conjugate tree it contains the height-zero exterior nodes.
The closed gate is exterior-free in the increasing-height tree; its own
population and every descendant population are zero.

All used short/long cell pairs are legitimate adjacent-node pairs in
both trees. For example `H*rho` belongs to the intersection of the
core and middle cells, and to the outer cell. These assertions use
actual cosets, not an arbitrary graph with invented phase labels.
Each listed orientation can separately have vertices in its specified
cells; no simultaneous contained placements are asserted.

## 2. A universal integer inventory

Set

\[
 t=\frac{(K-3)c}{2},\qquad m=\frac{N-Kc-d}{2}.
\]

Both are nonnegative integers in the cases used below. The orientation
convention is `(h,j,s)` with `epsilon=s*(-1)^j`.

| Short cell | Long cell | `h` | `j` | `s` | Copies |
|---|---|---:|---:|---:|---:|
| Core | Closed gate | 0 | 0 | +1 | `m` |
| Core | Closed gate | 0 | 3 | +1 | `m` |
| Core | Middle spine | 0 | 3 | +1 | `d` |
| Middle spine | Core | 1 | 0 | -1 | `c+t` |
| Middle spine | Core | 1 | 3 | -1 | `t` |
| Middle spine | Core | 1 | 4 | -1 | `c` |
| Middle spine | Outer edge | 1 | 4 | +1 | `c` |

The first two rows are designated whole-long-side half-turn pairs.
Among the fourth and fifth rows, `t` pairs are designated likewise.
Thus all long edges through the closed exterior-free gate have their
required mates. The remaining number `d+3c` of unpaired long sides
belongs to this particular witness; it is **not** claimed to be the
minimum of a transport optimization.

The total population and characters are

\[
 n_0=2m+d=N-Kc,\quad n_1=3c+2t=Kc,
 \qquad G_0=-d,\quad G_1=-c.
\]

Consequently `G_even=-d` and `G_odd=-c` exactly. The middle positive
and negative populations are `(K-1)c/2,(K+1)c/2`. Each prime tree has
only one occupied ordinary node. The joint charge graph therefore
has one ordinary charged cell and no cycle.

For that cell `g=-1` and its paired-sign reserve is `(K-1)c/2`, which
is a multiple of `c`. All joint reserve inequalities hold. The core
sign counts have precisely the required residues. Shared physical-
height capacities agree between the two trees because they describe
the same two populations.

There is no occupied exterior-free short node and no exterior-free
ancestor required by an occupied short node. Thus neither a balanced
nonempty exterior-free-cut perimeter bound nor a required active-gate
cost applies to this support. The existence of many balanced pairs
inside the two spine populations is not the existence of a balanced
ordinary phase node.

## 3. All three axis currents, not only the two scalar characters

Represent directed length on the three height-`h` axes
`1,rho,rho^2` by a three-vector, with opposite directions negative.
For opposite-rotation net counts `(x,y,z)`, the short-edge contributions
of the two hands are

\[
 S_+(x,y,z)=(ax-bz,\ bx+ay,\ by+az),
\]
\[
 S_-(x,y,z)=(-ax-by,\ -ay-bz,\ bx-az).
\]

The net orientation vectors of core-up, middle-down and middle-up
copies in the inventory are respectively

\[
 V=(-d,0,0),\quad W=(c,-c,0),\quad U=(0,-c,0).
\]

The phase-local balances are exactly

\[
 \begin{aligned}
 \text{Core:}\quad&S_+(V)+cW=(A,-H,0),\\
 \text{Middle:}\quad&S_+(U)+S_-(W)-cV=(0,0,0),\\
 \text{Outer:}\quad&-cU=(0,c^2,0).
 \end{aligned}
\]

The closed gate has zero current because its long sides are paired.
For the core identity, `c^2-ad=A` and `c^2+bd=H`; these are direct
consequences of `c^2=a^2+ab+b^2`. No floating-point calculation is used.
The three nonzero vectors are precisely the actual outer side currents
in their respective edge nodes.

Thus every linear sum of these joint-node balances, including ordinary
and alternating characters, individual-prime node equations, subtree
cut balances and phase-node potential identities, holds in this model.
A contradiction derived only from those equations and the population
constraints listed above would also contradict this explicit integer
assignment. This conclusion does not extend to potentials or bounds
which retain supporting-line positions or actual geometric areas.

## 4. Counts and whole boundary ports

The following choices meet even the previously proved conditional
native population lower bounds, although the model itself is only an
abstract assignment:

| Shape | `N` | `K` | Core signs `(+,-)` | Middle signs `(+,-)` | Core / middle populations |
|---|---:|---:|---|---|---|
| `(33,7,37)` | 3431 | 15 | `(1425,1451)` | `(259,296)` | `2876 / 555` |
| `(35,13,43)` | 5063 | 17 | `(2155,2177)` | `(344,387)` | `4332 / 731` |
| `(5,3,7)` | 143 | 15 | `(18,20)` | `(49,56)` | `38 / 105` |

The 143 row has the same height/sign populations as the known complete
control, but the abstract orientation inventory need not be that
control's geometric inventory.

Each axis side can be assigned whole ports of the indicated types,
and the third side receives exactly `c` whole long ports:

| Shape | Side `A` | Side `H` | Side `c^2` |
|---|---|---|---|
| `(33,7,37)` | `11a+4c=511` | `211b+2c=1551` | `37c=1369` |
| `(35,13,43)` | `21a+8c=1079` | `151b+4c=2135` | `43c=1849` |
| `(5,3,7)` | `5a+2c=39` | `16b+c=55` | `7c=49` |

All demanded port counts are available in the integer inventory. Each
outer side has at least one long tile side, as required by the obtuse-
corner argument. No tile side is partly assigned to the outer boundary
and partly to an interior contact.

## 5. What the abstract contact graph does and does not realize

Give each combinatorial tile three ports of lengths `a,b,c`, labeled by
its side type, edge joint cell, axis and directed sign. First match the
designated long-side mates as whole edges. Next assign the whole outer
ports in the preceding table. Every remaining cell/axis group has equal
positive and negative total integer length by Section 3.

Subdivide those remaining ports into unit stubs and match opposite
stubs within each cell/axis group. This supplies a finite integer
contact-port graph. A matched pair has compatible edge-node labels
and short heights differing by at most two. The exact checker produces
a connected tile-contact graph for all three listed cases, independently
of joining the outer sides into an exterior vertex. All copies are also
connected to the exterior vertex. It fixes the mate edges and the outer ports
before performing that matching.

**These are abstract ports.** The matching assigns no common Euclidean
supporting line or endpoint to their stubs. It supplies no cyclic sector
order and makes no planar-disk claim. In particular it does not check
that the short sides of a designated half-turn pair occupy the positions
forced by its long side. Integer phase/axis/length compatibility alone
does not supply those missing coordinates.

The counts of remaining matched unit stubs are 69,439 and 122,227 at
the targets. These are bookkeeping sizes, not tile placement searches.
The construction is a direct integer realization of a finite relaxation;
no SAT, LP or MILP solver is used.

## 6. Consequence for the proposed population proof

The unavoidable odd charge can remain on the exterior-containing
middle spine in both prime trees, with all additional population in
balanced pairs inside that spine and the core. Neither shared-height
counting nor a charge-graph cycle exclusion forces a new occupied
exterior-free branch in this assignment.

This identifies the missing step precisely: one must derive a condition
on where the required contacts lie, on the compatible cyclic sectors,
or on the area bounded by their actual embedded chains. Adding only
more linear combinations of the current phase-node conservation laws
will not eliminate the integer assignment above.

It does **not** show that those geometric conditions are insufficient,
or that either target tiles. Both original problems remain open.

## Reproduction

From this directory, with ordinary Python and the existing continuation
package supplied explicitly:

```sh
python3 abstract_flow.py --out ABSTRACT_FLOW.json
```

The script checks the actual phase cosets and both tree adjacencies using
the existing exact phase arithmetic, all inventory and axis identities,
signed populations, reserve inequalities, required ancestor flags,
whole-port boundaries, fixed long-edge pairs and contact-graph connectivity.
The output is an abstract witness, not a coordinate certificate.
An explicit `--base /path/to/semiprimes/continuation` may be supplied when
replaying outside the repository layout.
