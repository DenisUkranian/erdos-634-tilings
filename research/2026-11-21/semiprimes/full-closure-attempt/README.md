# Native boundary costs, whole-gate integrality, and the remaining gap

21 November 2026. **Neither 3431 nor 5063 is closed.** This continuation
adds exact necessary conditions and checks proposed ways to finish the
two exclusions. It supplies no tiling of either board and no contradiction
covering all their possible odd populations.

## New results

| Scope | Exact consequence | What remains |
|---|---|---|
| 3431, minimal odd population 111 | Native currents `(-4,41)` with every remote current zero require more than 157 odd tiles and are excluded | Other native/remote current profiles and larger odd populations |
| 3431, 111 odd tiles, native currents `(22,15)`, all remote currents zero | At most **34** remote even cells are actually occupied | The physical configurations with at most 34 cells remain |
| 3431, minimal odd normal form | The exceptional native core needs at least **212, 397, or 582** tiles for core parameters `g_up=-2,-3,-4` | These floors do not exceed the full budget in every profile |
| 3431, profile `(-3,2,1,0)` in the charge-parameter table | At most **32** balanced remote even cells are occupied | This profile is not completely excluded |
| 5063, 215 odd tiles in the native cell, all remote even nodes empty | The only possible native current pair is **`(20,23)`** | An exact strictly positive rational witness survives the whole-pair periodic model |
| 5063, that surviving profile | Native even populations are at least **677** and **903** | With 215 odd tiles the sum is only **1795**, below 5063 |

All statements use the fixed target shapes `(33,7,37)` and `(35,13,43)`.
The words *native*, *height*, *charge*, and *gate* use the reflected path
frame of the existing phase classification. A zero net gate current does
not mean the neighboring phase node is empty.

## 1. Keep the exceptional core's exterior current

The native height-two core has an inhomogeneous endpoint source. After
normalizing its cell, the exterior vertices are

\[
O=(0,0),\qquad X=(B,-A),\qquad Y=(B,0),
\quad A=b(2a+b),\quad B=a(a+2b).
\]

Its short endpoint source is

\[
b_0=\delta_O-\delta_Y,\qquad b_1=\delta_Y-\delta_X.
\]

Every inaccessible long edge has an actual whole mate when the odd
population occupies only the native cell and short heights are 0, 1, 2.
Remote even nodes are allowed. Exact single/pair inequalities then give

\[
n_{\rm core}\ge\frac{\langle f,b\rangle+tG_{\rm core}}{D}.
\]

Rounding both sign populations, not just their difference, gives the
212/397/582/677 bounds above. The ordinary native height-zero node instead
has zero periodic source because its exterior side has length `c^2`.
This permits the existing homogeneous one-gate bounds there.

[Complete core proof and four exact certificates](core-budget/README.md)
and [independent polygon-current audit](target5063/CORE_BUDGET_INDEPENDENT_AUDIT.md).

## 2. Full endpoint rows remove one 3431 profile and constrain another

For native currents `(-4,41)` with zero remote currents, an exact dual on
all 16,428 tile columns proves

\[
n_{\rm odd}\ge\frac{15776947829}{100000002}>157>111.
\]

For `(22,15)` with signs `(74,37)`, let `m_nat` be the negative odd
population at the native gates and `m_g` the negative population at
remote gate `g`. A second dual proves

\[
E=m_{\rm nat}+\sum_g(m_g-1)_+
\ge\frac{2173857481}{10^9}>2.
\]

Integer unsigned gate populations make `E` an integer. Since remote
currents are zero, `E=37-K`, where `K` counts remote gates containing
parent odd tiles. Therefore `K<=34`. The separate geometric visibility
theorem below implies that every occupied remote even cell is among these
parent-used gates. Thus there are at most 34 occupied remote even cells
in this profile. An upper bound on support alone is not a contradiction.

[Proofs, two certificates, and exact replay](target3431/README.md).
The [13-profile budget table](global/EMPTY_GATE_BUDGET_LIMIT_3431.md)
combines them with the native even reserves and the geometric visibility
theorem. It keeps parent-used gates, residue mate defects, and actually
occupied even nodes as distinct objects.

For `(22,15)`, the floors at 34 occupied remote cells total
`111+212+370+34*74=3209`. The remaining 222 tiles are three balanced
74-tile blocks. More generally, writing the actual populations as the
stated floors plus balanced blocks gives
`alpha+beta+sum gamma_g=37-K_occupied>=3`. No upper bound forbidding
those extra blocks in existing cells is proved here, so the reserve
identity supplies no full contradiction.

## 3. Empty remote nodes sharpen 5063, but leave a certified relaxation

In the native one-cell 215 mode, actual emptiness of every remote even
node forces all remote odd long edges to occur in whole half-turn pairs.
The exact inequalities

\[
13n_{\rm odd}\ge83Q_+-3Q_-,\qquad
13n_{\rm odd}\ge83Q_--3Q_+
\]

combine with the native cut congruences to leave only `(Q_+,Q_-)=(20,23)`.

An explicit **strictly positive rational** point satisfies every endpoint,
gate, sign, and remote mate row for that profile at population 215. A
separate **signed integer** point satisfies the same rows but has negative
coefficients. These prove two different limits of the projection; neither
is a nonnegative integer solution, an actual packing, or a full tiling.

[Physical reduction, exact dual, both witnesses, and replay](target5063/README.md).

## 4. Occupied remote even cells are visible to the odd parent

Under the one-native-odd-cell and height-0/1/2 hypotheses, an occupied
remote even cell cannot have no parent odd long edges at its gate.
Otherwise its actual short boundary cancels internally. Its inaccessible
long edges already pair, leaving a boundary consisting only of whole
long edges at height one.

Every long-edge vector is primitive in the even cell's own lattice:
after normalization its axial coordinates have greatest common divisor
one. Therefore a selected-cell vertex cannot split one of these edges,
and two selected long edges cannot overlap only partly. A nonempty
bounded union then has a supported simple cycle in a mesh of step `c`.
The existing ordered-boundary theorem excludes precisely such a cycle
in either target board.

This is a geometric proof of visibility. It does not identify a zero
scalar gate current, or equal periodic mate counts, with physical absence.
The conclusion applies to the 3431 minimal normal form and to the native
one-cell subcase of the 5063 215 mode; it is not transferred to other
odd-cell or height configurations.

[Visibility proof](target3431/INVISIBLE_EVEN_NODES.md) and the
[independent boundary audit](global/INVISIBLE_EVEN_NODES_AUDIT.md).

## 5. Checked geometric shortcuts that fail

An exact contained patch of the small primitive shape `(5,3,7)` has a
balanced 14-tile remote branch whose complete short-boundary current is
supplied by only **two whole parent tiles**. All 16 triangles have disjoint
interiors. This refutes the unrestricted proposal that such a branch
necessarily consumes at least `2b=6` parents; it makes no target-specific
existence claim. [Coordinates, proof, and checker](global/BALANCED_TWO_PARENT_CONTROL.md).

Other exact rigid cylinder controls of that small shape are monochromatic
at populations 21, 35, and 56. They refute general shortcuts `n>=c^2`
and charge units in the semigroup generated by `3,c` under cylinder
closure and nonoverlap alone. They do not assert mandatory-bank
compatibility or a full target tiling.
[Controls and precise qualifications](target5063/README.md#5-audited-limits-of-monochromatic-shortcuts).

The earlier unrestricted identity
`N=n_odd+B+2P` and its
[global pair reserve](../integer-closure/global-geometry/PAIRED_BANK_RESERVE.md)
remain valid. No universal lower bound exceeding 3431 or 5063 has been
obtained by combining them with the present conditional certificates.

## Reproduction and unresolved cases

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/replay.py
```

Eight proof checks use Python's standard library, including a fresh replay
of the supported-cycle theorem's exact board geometry. The optional discovery
programs use NumPy/SciPy and are not proof dependencies. Numerical search
timeouts and selected gate-mask experiments supply no exclusions.

The replay checks every new finite column inequality, exact rational and
signed integer witness, sign rounding, stated finite charge-budget table,
and rigid control. The geometric reductions are written arguments with
independent internal review and complete 143-tiling controls. No external
refereeing or proof-assistant formalization is claimed.

At 3431, other 111-tile odd profiles and larger odd populations remain.
At 5063, the 129 mode remains excluded by the earlier full certificate;
the 215 one/two/four-cell alternatives and larger odd populations remain.
The new native-cell assumptions must not be transferred silently to those
other cases. **The original two counts remain OPEN.**
