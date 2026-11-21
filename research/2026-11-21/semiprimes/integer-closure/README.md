# Whole odd packings, mandatory neighbors, and a global pair budget

21 November 2026. **The original counts 3431 and 5063 remain OPEN.**

This continuation gives one necessary theorem that couples a complete odd
packing to its exact neighboring geometry and the remaining tile budget.
It also closes two tempting shortcuts: a general unit-charge `3c` bound is
false for rigid cylinder packings, and the full periodic integer lattice
has no unaccounted-for modular obstruction for either target shape.

## 1. A global physical theorem

Fix the complete family `O` of odd-short-height tiles in a hypothetical
tiling. At every actual supporting line, reconstruct the whole long edges
of neighboring even tiles by an exact prefix sum of the odd short endpoint
current. No longitudinal positions are identified in the result. The net
long-edge chain is unique.

If a reconstructed long edge has multiplicity greater than one, or two
same-side long edges overlap, the proposed odd packing is impossible.
Otherwise each required edge has exactly **two** possible neighboring
triangles. Containment, intersection with `O`, and mutual triangle
intersections give an exact 2-SAT test for the mandatory neighbors.

Let `B(O)` count those mandatory neighboring tiles. Every remaining even
tile pairs with a tile on the other side of the **same entire long side**.
These pairs may use different short heights and need not be half-turn mates.
Each pair has one positive and one negative tile. Consequently

\[
\boxed{N=|O|+B(O)+2P.}
\]

The mandatory neighbors already carry the entire even charge
`G_e=(a-b)G_o/c`. Separately rounded positive/negative populations at the
actual prime-tree nodes, required empty ancestors, and charge transport
between even heights give a computable pair reserve `mathcal P(M)` for
each compatible mandatory selection `M`:

\[
\boxed{N\ge |O|+B(O)+2\min_{M\text{ compatible}}\mathcal P(M).}
\]

The theorem uses no minimum odd-population assumption, terminal-branch
hypothesis, or guessed height cutoff. Minimizing its reserve over every
possible complete odd packing has **not** been achieved. It is a global
necessary condition and an exact geometric elimination step, not an
exclusion of either target.

An explicit consequence applies without specifying the odd coordinates.
If an odd cell has charge `c g_L` and `V=sum |g_L|`, its distinct mandatory
even bank costs at least `(a-b)|g_L|` tiles. Rounding the total even sign
populations to their proved residues gives **`V<=53` at 3431 and `V<=77`
at 5063**. At `V=77`, the latter would need exactly 3311 odd and 1752 even
tiles, with every odd cell monochromatic. That extremal case is not excluded.

- [Full reconstruction, two-neighbor theorem, pairing, and scope](long-banks/README.md).
- [Explicit prime-node and height-transport pair reserves](global-geometry/PAIRED_BANK_RESERVE.md).
- [Independent implementation audit](arithmetic/LONG_BANK_INDEPENDENT_AUDIT.md).
- [Exact geometric replay](long-banks/LONG_BANK_REPLAY.json).

## 2. The geometric test is strictly stronger than cylinder packing

An exact 13-tile packing of `(5,3,7)` has ten positive and three negative
tiles, hence unit charge seven, zero cylinder current, and no overlapping
triangle interiors. It disproves a general claim that these conditions
alone imply at least `3c=21` tiles.

The full neighbor reconstruction nevertheless excludes this proposed
complete cell. A separated realization requires 522 long segments and
violates same-side capacity. A compact realization passes that line-capacity
test but has 32 compulsory long segments; for one of them **both** whole
neighboring triangles overlap an existing odd tile. These are exact local
obstructions for the supplied configurations.

The test also excludes the previously exhibited separated balanced six-tile
hexagon and contained balanced 16-tile cylinder control. However a different
compact six-tile patch has zero **unreduced** short current and passes the
bank test. Thus the theorem does not exclude all balanced six-tile cells.
No remaining 5063 parameter is deleted on that unsupported premise.

- [Countercontrols, compatible six-tile patch, and finite search scope](charged-cells/CHARGED_CELL_LIMITS.md).
- [Exact charged controls](charged-cells/CHARGED_COUNTERCONTROLS.json).
- [Exact compatible balanced patches](charged-cells/BALANCED_SIX_PATCH.json).

## 3. The complete periodic signed integer image

For both `(33,7,37)` and `(35,13,43)`, prescribed integer gate vectors
`Q^+,Q^-` and sign totals `P,N` have a **signed integer** representation
with all complete periodic endpoint rows zero if and only if

\[
\sum Q^++\sum Q^-=P-N,\qquad c\mid(P-N).
\]

The representation may use negative tile multiplicities. This result
therefore does not establish a nonnegative integer packing or a tiling.
It does establish that another linear congruence, including prime-power
torsion, cannot settle a cell in this projection.

The sufficiency certificates check 167 positive endpoint kernels and seven
exact square minors. Their determinant gcds are respectively 37 and 43.
Explicit signed witnesses are also supplied for the former difficult native
profiles, including `(22,15;74,37)` at 3431 and `(42,1;129,86)` at 5063.
Their negative coefficients are explicitly counted by the verifier.

[Theorem, complete proof, exact determinants, and witnesses](arithmetic/README.md).

## 4. Status of the original numbers

| Target | Still established | Still open |
|---|---|---|
| 3431 | The established prime-tree and geometry constraints; the new global bank and pair reserve | `n_odd=111`, every larger allowed odd population, and the full target |
| 5063 | `n_odd>=215`; at 215 every short height is 0, 1, or 2, with the previously reduced one/two/four-cell classification | All remaining 215 configurations, larger odd populations, and the full target |

The earlier [31-value four-cell list](../continued-rigidity/cells5063/REDUCED_CELL_CLASSIFICATION_5063.md)
is unchanged. The conditional claim `n_L>=3c` for a unit-charge cell at the
two target shapes has not been proved or refuted here. The `(5,3,7)` control
refutes the unrestricted generalization; it is not a target counterexample.

The assertion that adding rigid whole nonoverlapping tiles *automatically*
settles 3431 is not justified by the existing evidence. The new theorem
derives a concrete extra physical condition and demonstrates exact
eliminations, while a universal target contradiction remains outstanding.

## 5. Exact reproduction and audit

```sh
python3 research/2026-11-21/semiprimes/integer-closure/replay.py
```

The six standard-library suites reconstruct the certificates and controls.
They include both complete 143-tile tilings, 288 local long-side choices,
72,384 pair-reserve arithmetic checks, and 28,933 small 2-SAT formulas
checked against exhaustive truth assignments. The geometric bank replay
checks 18 specified configurations. Numerical minimization and finite
exploratory lift scans are not used as target exclusions.

[Independent internal review and exact scope](INTERNAL_AUDIT.md).
The package is included in the root `scripts/verify_all.py` coordinator.
These are original written research arguments with internal review and
exact finite controls; external mathematical refereeing and proof-assistant
verification are not claimed.
