# Semiprimes: the 5063 minimal mode and a global contact theorem

21 November 2026. **3431 and 5063 remain OPEN as original tile counts.**
This continuation closes the entire `n_odd=129` case for the 5063 board,
including all charged remote even branches. Every hypothetical complete
5063 tiling consequently has at least **215 odd-height tiles**.

The latest [physical completion theorem and integer cell restrictions](continued-rigidity/README.md)
combine actual contact rows with the spatial allocation of retained odd
signs and the remaining tile budget. Unit-charge cell minima are 41 and
53 for the two targets, and balanced cell populations 2, 4, 8, 10, and 14
are excluded independently. The remaining 5063 four-cell parameter now
has 31 values, giving 218,905 containing phase/sign schemes. Exact rational
witnesses show that both two-cell native roles survive the full continuous
periodic endpoint model; physical integrality and contacts remain unresolved.

The latest [two-height exclusion](global-closure-next/five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md)
shows that equality forces all 215 odd tiles to height one, with every
short height in `{0,1,2}`. Exact node balance and joint-cell analysis
then leave [one, two, or four middle classes](global-closure-next/global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md).
This does not yet exclude equality or larger odd populations.

The next continuation gives a [global charge, contact, and tile-budget
theorem](global-closure-next/README.md), valid at every odd population in
the established phase framework. Its joint graph assigns one edge to each
unmatched physical tile and couples both prime trees through charge flows,
area demands, and one exact centroid budget. This supplies a common
necessary theorem without deciding the two target counts. An exact
3431 lifting theorem also identifies why containment and first transverse
moments do not exclude its existing fractional minimal profile.

The proof uses 65 exact endpoint certificates and a complete finite
enumeration of neighboring integer charges. Of 34,672,599 profiles,
17,800,359 pass the sign reserves, and **none** passes all certificates.
The independent checker reconstructs all 1,442,220 single-tile
inequalities and all 780 transformed cuts with integers.

* [Full proof and geometric dependencies](MINIMAL_ODD_EXCLUSION_5063.md).
* [Certificate index and exact scope](gate-model/CERTIFICATES_5063.json).
* [Final independent replay](audit/FINAL_DUAL_REPLAY_5063.json).
* [Independent mathematical and enumeration audit](audit/PROFILE_CUT_AUDIT.md).

## Additional checked results and limits

The new [unrestricted odd-branch budget](global-closure-next/large-population/GLOBAL_ODD_BRANCH_BUDGET.md)
also shows that a native 129-tile height-one layer with signs `(86,43)`
requires at least 387 odd tiles globally at 5063. In the total-215 mode,
it excludes height-one population 129, after proving the required native
phase and sign inventory. The subsequent two-height theorem excludes
the alternatives with 86 at height one and 129 at height -1 or 3 by a
fresh exhaustive scan of 9,112,001 different profiles. Only the one-height
215 alternative remains at equality. The general lower bound remains
215; the 387 bound has the stated native-layer hypothesis.

At the next odd population `5c`, height one must occur. The possible
odd-height sets are exactly the necessary alternatives `{1}`, `{-1,1}`,
and `{1,3}`; all short heights lie in `[-2,2]` or `[0,4]`.
This theorem applies to both targets, does not force a unique native
height-one phase, and does not exclude the five-block mode itself.
[Five-block structure, proof and exact arithmetic controls](charged-branches/FIVE_BLOCK_SCOPE.md).
The later reduction above is stronger specifically at 5063.

For 3431 an exact strictly positive rational witness satisfies the
entire periodic endpoint relaxation at `n_odd=111`, with integer
neighboring charges and the required gate capacities. It proves that
more linear cuts from this same relaxation cannot exclude every 3431
profile. It is not a geometric tiling.
[Exact witness, finite verifier and method boundary](global-invariant/N3431_PROFILE_LIMIT.md).

The [new cylinder lift](global-closure-next/exact-lines-3431/CYLINDER_LIMIT.md)
preserves exact transverse supporting lines and puts a feasible 111-profile
point inside the convex hull of actual contained nonoverlapping integer
packings of exactly 111 tiles. This proves a stronger limit of linear
packing cuts: the contact and sign conditions need not hold in any one
integer packing of that mixture. The
[physical charge-budget theorem](global-closure-next/rigid-body/PHYSICAL_CHARGE_BUDGET.md)
retains that missing integer coupling explicitly.

An [exact native 215 profile at 5063](global-closure-next/five-block-two-heights/N5063_NATIVE_215_PROFILE_LIMIT.md)
also survives the fractional periodic model. Its
[410-translate cylinder and packing lift](global-closure-next/exact-lines-3431/native-215-5063/CYLINDER_PACKING_LIMIT_5063.md)
lies in the convex hull of actual nonoverlapping packings of exactly
215 tiles. The sign and contact requirements hold only after averaging;
the single-height 215 mode is still unresolved.

The single accessible parent gate of a remote even class gives exact
population bounds of 185 at 3431 and 301/602 at 5063. Both signs and
both even heights are covered. The 5063 instances are now intermediate
restrictions in an excluded mode; the 3431 restriction remains relevant.
[Proof, exact duals, and positive controls](charged-branches/ISOLATED_GATE_TERMINAL_COST.md).

Exact fractional periodic witnesses attain the local ratios `91/22`
and `83/13`. Stronger conclusions require additional coupled or physical
constraints. A separate product-of-trees calculation records a precise
limit of calibrations supported only on the board filling; it does not
exclude larger or state-dependent geometric constructions.
[Product-tree limits](global-invariant/PRODUCT_TREE_LIMIT.md).

An exact balanced short-strip packing inside the 3431 board uses only
7 negative and 7 positive parent tiles. It disproves the proposed local
33-negative-parent lower bound under the stated terminality, phase and
containment conditions, while leaving the full completion problem open.
[Exact geometric countercontrol and its scope](charged-branches/BALANCED_SHORT_STRIP.md).

The additive marginal model accelerates candidate certificate discovery
without entering the final proof as a numerical solver assertion.
[Its dual-validity argument and API](global-invariant/ADDITIVE_GATE_DUALS.md).

## Reproduce the new finite proof

From the repository root:

```sh
python3 research/2026-11-21/semiprimes/replay.py
```

The replay uses Python's standard library and a C++17 compiler. It
checks the certificate hashes and integer inequalities, compiles the
enumerator, checks independent small controls, and repeats the entire
charge enumeration. It takes a few minutes on an ordinary CPU; no
optimizer is needed. `--saved-enumeration` checks the already recorded
complete enumeration instead of rerunning it and explicitly records
that distinction.

The two additional structural and method-limit controls use only the
Python standard library and are included in the root replay coordinator:

```sh
python3 research/2026-11-21/semiprimes/charged-branches/verify_five_block_scope.py
python3 research/2026-11-21/semiprimes/global-invariant/verify_3431_rational_projection.py
```

## What remains open

At 5063, possible complete tilings with `n_odd>=215` remain unexcluded.
At 3431, neither the entire minimal `n_odd=111` mode nor all larger odd
populations are excluded. No positive tiling or unrestricted global
contradiction for either original count is supplied here. The result
does not close all semiprimes.
