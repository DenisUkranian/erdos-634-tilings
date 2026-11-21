# Independent audit of the native 215 fractional and packing limit

21 November 2026. **Audit passed. The original 5063 question and the
actual one-height 215 regime remain open.**

The [new 5063 cylinder theorem](../exact-lines-3431/native-215-5063/CYLINDER_PACKING_LIMIT_5063.md)
and its [exact checker](../exact-lines-3431/native-215-5063/verify_5063_cylinder_packing.py)
were independently reviewed after the files were frozen. The final
checker was run once, completed successfully in 7.590 seconds in the
audit environment, and reproduced the recorded JSON exactly. It
also reruns the full rational source certificate, rather than relying
on a saved numerical result.

## 1. The rational source certificate transfers correctly to 43

The [native periodic witness](../five-block-two-heights/N5063_NATIVE_215_PROFILE_LIMIT.md)
uses 22,188 variables and 5,634 equations, with population 215 and
native signed gate currents 42 and 1. Their sum gives charge 43,
so the exact positive and negative masses are 129 and 86.

The reused Fourier inverse routine is parameterized by `a,b,c`.
Its root enclosures, axis-null rows, gate-frequency lines and Gram
blocks are recomputed at `(35,13,43)`; no bound computed only at 37
is imported. The 1,849 verified blocks have row-size histogram
`{2:126,3:1639,4:84}`. Their 5,505 rows are exactly the 5,634
equations less the 129 identically zero transformed endpoint rows.
Those null rows have zero target entries. The inverse checks establish
the required range condition and uniform bound `K=3`.

The unitary transforms and subsequent gate/population row scalings
do not enlarge the residual norm. Solving the normalized blocks and
using the original matrix's least-norm correction therefore validates
the stated bound on `M^dagger(b-Mx_0)`. The exact positivity check is

\[
 3\cdot26076270=78228810
 <1538690768^2=2367569279528429824.
\]

The reconstructed integer columns have the same CCW endpoint and
gate conventions as the lifting checker. The positive gate capacity
94 survives the correction by the supplied exact slack inequality.
The negative capacity 121 is automatic from total negative mass 86.
Thus the source defines a strictly positive rational feasible point
with the asserted sign and gate data. It does not define integer
tile multiplicities.

## 2. The finite cylinder lift and contained translates are correct

The convolution uses `q=(1000+X-K,-42+Y+K)` for independently uniform
`X,Y,K` in `0,...,42`. The conditional longitudinal parameter still
runs through every residue on each actual supporting line. Endpoint
offsets are longitudinal to their own row axis. The same proof as
at 3431 therefore gives `A_cylinder L=E A_torus`, preserving every
residue-column mass, sign and gate label.

The exact replay checks 5,547 axis/residue marginals and all 22,188
operator columns. Its 5,419 anchors support 65,028 actual oriented
placements, all strictly inside the normalized board. The minimum
board-side determinant is 739,733,128.

The enclosing hexagon has centre `(1000,0)` and radius `42+35=77`.
Its three containment inequalities and the finite centre search box
agree with the stated scaled board. Exactly 410 translations by
`43R` pass, all strictly, with minimum determinant 1,468,880.
Their average has 855,572 anchors and 10,266,864 oriented columns.

Distinct preimages at any averaged anchor belong to one residue;
their original convolution mass is at most 43. Hence
`mbar(q)<=43`, and the global pointwise density bound is

\[
 \frac{215}{410}=\frac{43}{82}<1.
\]

## 3. Every convex component has exactly 215 nonoverlapping tiles

Here `D=43*410=17630`. In a fixed residue/orientation family use
integer interval lengths `w_q=215*mbar(q)`. They obey
`0<w_q<=9245<D` and sum to `215D=3790450`.

Each sampling residue modulo `D` occurs 215 times in the concatenated
interval range. Since every interval is shorter than `D`, it selects
215 distinct anchors. The checker verifies all 32,597,870 such
residue/sampling-offset cases. Multiplying by the twelve orientations
and hands gives 391,174,440 components with repetitions.

Within each component, anchors differ by nonzero vectors in `43R`.
Their distances are at least 43, equal to the tile diameter; two
interior points of a triangle are strictly closer than its diameter.
The corresponding tile interiors are therefore disjoint. Every tile
is contained by the translated-hull check.

Choosing the family with probability `x_(r,j,s)/215` and the sampling
offset uniformly gives each placement marginal
`x_(r,j,s)*mbar(q)/D`, exactly the averaged cylinder point. This
proves the claimed membership in `conv(P_215) intersect H`.

**The signs, gate profile and cylinder equations hold only in the
mixture.** Each component has one orientation and one sign, so it
does not itself have sign populations 129 and 86. The result proves
no point in `P_215 intersect H`, no full physical current closure,
and no complete even population or tiling. A constraint derived
jointly from packing and the required sign/contact data may still
exclude configurations that ordinary packing inequalities alone
cannot exclude.

## 4. Audited files

| File | SHA-256 |
|---|---|
| `CYLINDER_PACKING_LIMIT_5063.md` | `5ac18c540a40f36edac2439f13c8dd5eef3de2bed1a1c63f2471fffe171a4081` |
| `verify_5063_cylinder_packing.py` | `ef508c99cdc752cfd538bd4b2ee7b5c612bde67b1ecb6cf73b923526e231713c` |
| `N5063_CYLINDER_PACKING_REPLAY.json` | `1891fffdf82c070a8f3964ac496b4a228a6e7e960ce0449aa56b05bb18d09812` |
| `verify_native_215_projection.py` | `e41c25e6cfbee44d4826e5659b8f3b16d4ef7270f4244abf5c0730ae74f0e01a` |
| `N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz` | `9ef122e71386df768bf0d3930d3826a62addfdba49d1ae14617adb3ced21ebec` |
| Shared exact Fourier checker | `c7684b7fe7f7dab79739ba16a872215f036e1363a3da021e2a8d88e0c395a79f` |

A LaTeX form-feed typo in the density fraction was identified during
review and corrected by the file owner before the final document
hash above was recorded. No mathematical correction was required.
