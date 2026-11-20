# Independent audit: supported cycles and empty phase roots

The audit-time paths and hashes below identify the working snapshots. Publication relocates imports, renames the signed replay scripts, and adds the separately checked shared-height explanation and explicit conjugate-tree scope. The final code hashes and fresh executed controls are recorded in [the package replay](../REPLAY.json). These internal audits are not external refereeing.

20 November 2026. Scope: the supported-cycle theorem in `pure_cycles/NO_REMOTE_GAPS.md` and its proposed application to the subtree cut in the earlier `phase-height/PHASE_BRANCHES.md`. This is a mathematical/code audit within the project, not external refereeing or proof-assistant verification.

**Assessment.** I found no gap in the cylinder argument for the two boards, including its use at arbitrary mesh rotation and translation. The implication from an exterior-free empty phase root to a forbidden supported simple cycle is valid. The result excludes such empty roots; it does not decide whether either whole board can tile. It does not prohibit an empty node whose subtree contains an exterior edge node.

## 1. The word deletions retain original endpoint information

Fix the one possible mesh axis supporting a length-`a` board chord and call its unit vector `e0`. If no axis supports such a chord, choose any axis. Start with the actual closed unit-mesh walk and its trivial word in `C_a*C_a*C_a`.

After any sequence of the permitted deletions, the surviving letters retain their order in the original walk. Every removed intervening original subwalk has displacement in `a Z e0`. This is an induction: an inverse-pair deletion adds two opposite surviving displacements to previously removed displacements; a horizontal `a`-letter deletion adds `+a e0` or `-a e0` to them. Both preserve the stated subgroup.

If a nonempty word remains, its maximal same-axis runs have one sign, and every horizontal run is nonzero modulo `a`. Triviality in the free product therefore requires a nonhorizontal run whose exponent is zero modulo `a`; otherwise all its syllables are nonidentity and the word is already reduced. Choose `a` letters from that run. Their corresponding **original** initial and terminal vertices differ by

`a (±ei + n e0)`, with integer `n` and a nonhorizontal mesh direction `ei`.

The squared norm of the vector in parentheses is `n^2 ± n + 1`. It is either 1 or at least 3. The latter contradicts the strict diameter bound. In the former case the displacement is a length-`a` chord in a different mesh axis: its transverse component is nonzero. This contradicts the one-axis hypothesis. Thus the restricted deletions really do empty the word.

The underlying pure-mesh word is justified by the stated unit-edge tile labelling. For the order-`a` group, `s=b/c mod a` satisfies `s^2=1`, and each direct or reflected tile relator is trivial. On a pure height, the common exponent `c*s^h` is a unit modulo `a`, so an automorphism in each cyclic factor converts one mesh step to its ordinary axis letter. The argument requires the integer-offset lemma for collinear tile sides; it does not assume an edge-to-edge tiling.

## 2. Why nonhorizontal chain cancellation gives the slice conclusion

Project the retained walk to the cylinder of circumference `a` in direction `e0`. Removed original subwalks have displacement in `a Z e0`, so later surviving edges start at the same cylinder positions as their original edges. An inverse pair retraces exactly one cylinder edge. A deleted horizontal block traverses one whole horizontal circle. By induction, the projected original edge chain is a sum of horizontal circles. Its nonhorizontal oriented edges cancel as geometric chains on the cylinder, not only as an abstract group word.

Let `P` be the interior of a supported simple cycle. At a nonvertex height `y`, periodize `1_P(x,y)` by translations of `a e0`. Its jumps in `x` are the signed crossings of the nonhorizontal boundary chain. They vanish by the preceding chain equality; no horizontal edge occurs at a nonvertex height. The periodization is consequently a constant nonnegative integer almost everywhere on the circle.

Because `P` is connected and open, its projection onto the transverse axis is the entire open interval between its extreme heights. Every intermediate slice has positive length. Its total length is at most the containing triangle's chord length, hence at most its diameter, strictly below `2a`. The constant integer must therefore be 1, and every regular slice has total length exactly `a`. Disconnected slices cause no difficulty: their lengths add in the periodization integral.

The earlier pure-boundary area and character calculations force the cycle to enclose `2c^2` tiles, or `ab` mesh-rhombi. Integration now forces transverse axial span exactly `b`. Thus a necessary board condition is a span of at least `b` on which its horizontal chords have length at least `a`.

## 3. Exact geometry replay

The normalized 60-degree-corner frame uses `A=ap/c`, `B=bq/c`; the actual exterior side lengths before dividing by `c` are `(1551,511,1369)` and `(2135,1079,1849)`, respectively. In particular the 5063 side pair is **2135 and 1079**, not the erroneous values in an earlier chat summary.

Running the supplied `check_remote_cycles.py` passed and returned:

| Board | A | B | Maximum squared chord in `D intersect rho^-1 D` | `a^2` | Upper span with chord at least a |
|---:|---:|---:|---:|---:|---:|
| 3431 | 1551/37 | 511/37 | 1331780030161/3293267769 | 1089 | 5110/1739 < 7 |
| 5063 | 2135/43 | 1079/43 | 9230010672961/8428158025 | 1225 | 19422/2623 < 13 |

I also checked the simpler bounds independently with exact fractions. The diameter squares are `2405601/1369 < 3267=3a^2` and `4558225/1849 < 3675=3a^2`. The two-axis squared chord bounds are `3B^2=783363/1369 < 1089` at 3431, and `(7/4)B^2=8149687/7396 < 1225` at 5063. The latter uses `B/A=1079/2135>1/2`.

For any chosen horizontal mesh axis, let `M` be the largest board chord and `H` its transverse axial span. The triangular slice profile gives `MH=AB`. The span with chords at least `a` is `AB(M-a)/M^2` when `M>=a`. Since `M<=A<2a`, this is at most `B(1-a/A)`, giving exactly the final column above. These bounds hold for arbitrary mesh rotation. Both are strictly below the required span `b`, proving the contradiction.

## 4. From a phase-root boundary to a supported simple cycle

Let `U` be the union of tiles in a nonempty exterior-free subtree whose root contains no short tiles. The phase cut formula represents its boundary by a finite integer chain of **whole actual long tile sides**, all of length `c` and the same direction height `k`. No additional Euclidean-lattice assumption on the subtree's tile vertices is required here.

Consolidate coincident oriented edges, cancel oppositely directed copies, and orient every remaining edge according to its nonzero coefficient. The chain is balanced at every endpoint because it is the boundary of `U`. It is not zero: its boundary area integral is the positive area of `U`.

Every endpoint-connected component of this graph lies in one translate of the mesh `c z^k Z[rho]`, since all its edge displacements are mesh unit steps. A nonzero finite balanced directed graph contains a directed cycle; choose one with the fewest edges. It has no repeated vertex. Unit edges of a single triangular mesh have no crossings in their relative interiors, and any coincident opposite edges have already been cancelled. This cycle is therefore a simple polygonal loop in the actual tile skeleton. Intersections with *other* endpoint components do not affect its own simplicity or support.

It is exactly a supported cycle excluded by Sections 1–3. Hence an exterior-free phase root with occupied descendants must itself be occupied. The same argument applies to the reverse valuation tree.

This removes the previously allowed exterior-free empty-root exception. Any subsequent count of required nodes must still separate exterior-free nodes from the exterior-containing spine: the proof does not make every node of that spine occupied. The original existence/nonexistence questions for 3431 and 5063 remain unresolved by this corollary.
