# Two unmatched owners on a bank constrain the entire interface

Both original F2 counts remain open. Work from main at `f74707ff02ea898036539c0d1b9d5fda3ad474fd`. The two banks of a cut consist of whole long edges after removal of actual half-turn mates. Their oriented sum is the [physical cut boundary](../joint-cell-tree/TREE.md). The conclusions below allow T-junctions, arbitrary reflections, heights and translates.

## Exterior-free cut

Suppose one bank of an occupied exterior-free branch has exactly two unmatched owners. Let n be the number of tiles in the entire branch and m the number of unmatched owners on both banks. If m−2<a, the following table lists all remaining pairs for the two boards. Entries are necessary; the enumeration tests word, area and simple-polygon constraints. It does not tile the interiors.

| Tile | n | Possible m |
|---|---:|---|
| (33,7,37) | 74 | 16, 24 |
| | 148 | 24, 30, 34 |
| | 222 | 24, 32, 34 |
| | 296 | 32, 34 |
| | 370 | 32 |
| | 740 | 34 |
| (35,13,43) | 86 | 16, 28 |
| | 172 | 30 |

In particular a branch with occupied descendants and a two-owner bank costs **at least 24 or 30 unmatched tiles** respectively. Each occupied ordinary lift needs at least 2c short tiles. At 5063 a branch larger than 172 with a two-owner bank costs at least 38. Indeed the opposite exceptional steps have opposite signs. Writing x,y for the parity sums in blocks, a zero bank gives cx=dy or dx=cy by the [remote cut equations](../charge-variation/ROOTED.md). Both absolute block sums are strictly below c by the parity variation bounds. Coprimality forces x=y=0, so the opposite signed bank also vanishes and m is even. These contact payments can be measured for each physical edge separately.

### Global contact and population inequality

In any complete target tiling let Z count the occupied exterior-free branches with zero total charge at both parities. Among them let I count those with an occupied strict descendant and J count those of I with a two-owner bank. For 5063 let K count the branches in J containing more than 172 tiles. Nested branches are counted by their entering edges. Let V be the sum of absolute odd short charges in units of c and let M count all unmatched tiles. With the exterior contribution A from the [global reserve](REMOTE_BOUNDARY.md), one has

| Board | Necessary inequality |
|---|---|
| 3431 | N ≥ M ≥ 16Z + 2I + 6J + max(A,63V) |
| 5063 | N ≥ M ≥ 16Z + 2I + 12J + 8K + max(A,65V) |

Here A is 107 or 149 respectively, rising to 149 or 171 if some lift off the exterior path has nonzero short charge. For each member of J the table raises its own nonterminal payment from 18 to 24 or 30. At 5063 the larger branches pay at least 38. In the 3431 proof the two units borrowed for a nonterminal length-16 branch come only from its unique terminal child. That child belongs to none of I, J, K. A member of J pays its entire increment directly. The previous disjoint-owner summation and exterior charge term therefore still apply. These inequalities do not require any two-height hypothesis. Both complete 143 controls have no occupied exterior-free branches, as checked in the linked reserve.

### Reduction to two paths and a short word

Use units of the other bank's long mesh. Rotate or conjugate the whole configuration and orient the positive boundary so the two exceptional steps are v=(a+bρ)/c and −v. They are opposite by the [displacement divisibility](../charge-variation/AREA_RESIDUE.md). A circuit with only one such step cannot close modulo the other mesh. A circuit without either step would be a forbidden supported pure cycle. The [Jordan decomposition](../charged-contour/README.md) therefore consists of one polygon. Its boundary can be written v,P,−v,reverse(Q), where P,Q are two pure unit walks with the same displacement L. Here reverse means traversing a path backwards. The coset shift by v distinguishes the two walks. Neither may backtrack.

Use the two free products of three cyclic groups from the [canonical-seam proof](../charge-variation/CANONICAL_SEAM.md). Normalize so that a pure unit step has its own axis letter. Modulo a the exceptional letter is Y to the power t, where Y has direction ρ and t is b/c modulo a, chosen as 10 or 6 respectively. Thus Q represents the conjugate of P by Y to the power t. Modulo b the exceptional letter is X to the power −1, where X has horizontal direction 1, because a/c is −1 modulo b on both boards.

First suppose P consists only of Y steps. Normal form modulo a and the length bound imply the same for Q. The common displacement makes them identical straight runs. Positive area gives n=2c times the run length divided by b. The remote parity totals vanish, so n is a multiple of 2c, and the run length is a multiple of b.

Otherwise write P=Yʳ U Yˢ with U beginning and ending off the Y axis; similarly for Q. The reduced syllables of U survive conjugation modulo a. The corresponding signed run lengths in Q are literally the same: they are congruent and the sum of the lengths of both words is less than a. Therefore Q=Yⁱ U Yʲ. Equal spatial displacement gives i−r=s−j. This difference is t modulo a and twice its absolute value is at most m−2<a, so it equals t as an integer. In particular U has length at most 6 or 11, strictly less than b in each case. As a separate area check the polygon has doubled area in mesh units equal to 2 det(v−tρ,L): shifting the initial Y run by t and shortening the final run by t changes the chord-closed determinant sum by 2t det(ρ,L).

The literal word relation now also holds modulo b, where Q is conjugate to P by both Yᵗ and X⁻¹. Hence Q commutes with g=X⁻¹Y⁻ᵗ. The centralizer of g in this free product is generated by g. To see this, use the tree of reduced words with one type of vertex for a group element and one for each factor coset containing it. Repetition of the two nonidentity syllables of g gives its bi-infinite translation axis. A commuting element acts on the axis by translation and preserves factor labels, so it shifts by a whole two-syllable period. After multiplying by a power of g it fixes a group-element vertex, whose stabilizer under left multiplication is trivial.

Consequently Q is a nonzero power of g: U contains a non-Y run which survives modulo b. Every non-Y syllable of U is on the X axis. For a positive power its X exponents are −1 modulo b and its internal Y exponents are −t. The boundary exponents i,j are 0,−t modulo b. For a negative power these four residues are 1,t,t,0. The [integer enumeration](two_bank_words.py) lists every signed run length allowed by

    2 length(U) + |i| + |i−t| + |j| + |j+t| < a.

It checks the two original reduced words, exact axial area, endpoint coincidence and polygon simplicity. The length-16 result agrees with the independently computed [unrestricted contact census](REMOTE_BOUNDARY.md). Its 5063 local example uses the walks X Y⁶ and Y⁶ X up to the choice of axes.

## Two native cuts at minimum length on their opposite banks

Now suppose **each** of the two native cuts has two unmatched middle owners, and **each** opposite bank has the smallest possible length a+b. Use the reflected middle mesh chart, O=(0,0) and D=(a+b,−b). The two exceptional steps sum to zero. Each pure step contributes at most one to the first coordinate of D. Thus all a+b pure steps are E=(1,0) or S=(1,−1), with counts a,b. There is no circuit: an exceptional step on a circuit requires the other, and then every pure step advances the first coordinate. The two exceptional edges alone could only form a whole cancelled pair. The chain is a simple O-to-D path even if it shares segments with the slant chord.

The total population in the component of the middle lift B after deleting the two native edges, including all its branches, must lie in the following sets.

| Board | Middle population | Possible signed charges within that region |
|---|---|---|
| 3431 | 148, 222, 296, 370, 444 | All lifts are balanced below 444. At 444 any nonzero charges require the three-lift configuration described below. |
| 5063 | 172, 258, 344 | Every lift is balanced. |

These are conditional restrictions on arbitrary tilings. The middle lift is occupied by its four physical owners. All middle tiles lie on the slant side of the axial cut and outside the slant side of the other cut. Zero signed middle currents force the two slant-side signed totals to coincide at even zero and odd −c in reflected path signs, by the [native equations](../charge-variation/ROOTED.md). The intervening region is thus neutral in both parities.

### Positioned enumeration and checks

For hand s=1 at the axial cut and −1 at the slant cut, insert steps v=zˢρʲ and −v in all orders among the E and S steps. The [suffix test](two_native.py) retains words equal to the canonical EᵃSᵇ in both free products. At any prefix reduce its inverse times the target word. Each syllable of that remainder comes from a disjoint set of suffix letters. On each axis assign the remaining exceptional powers to candidate syllables or omit them. Minimize the sum of nonnegative residues still required; all remaining ordinary letters on that axis have positive exponent in generators E,S. If even this minimum exceeds the available count, the prefix is impossible. Each accepted word is recovered a second time by reading from the other endpoint. Oriented area uses the clockwise path closed by its slant chord, permitting cancellation along that chord.

The [position check](native_positions.py) places the actual owner triangle on each step. In physical units after rotating away the middle height, a step w has apex displacement (a/c)z⁻ʰ w from its start, with h=s on an exceptional step and h=−s otherwise. This follows from w being the directed sum of the two shorts. The choice puts a middle owner in the intervening region and the opposite owner outside it. Require containment in the board, no interior overlap, and the correct winding number at each owner centroid for both cut chains. Subtract the two actual areas. Both columns of path checks include all six headings and both possible first exceptional directions through this heading choice.

For a difference of only 2c tiles all of them would have short lift B, so its sole unmatched tiles would be the four on the native interfaces. Remove the four triangles by replacing their exceptional edges by the ordered shorts. The difference of the resulting paths is the boundary of (2c−4)/2 actual half-turn pairs. Its three directional first moments and cumulative widths must obey the [pair identities](TERMINAL.md). Every two-block case fails, including 252 positioned pairs for 3431 and 144 for 5063. Larger populations in the table are retained even when a test proved only for one occupied lift would fail.

### Detecting hidden charges in a neutral region

The same argument applies to any exterior-free neutral branch, or to the neutral middle region with both native middle currents zero. Span all its nonzero short charges by their minimal subtree. Each leaf is charged and has exactly one nonzero signed gate. Indeed any incident direction containing no charge from this region has zero current by the cut equations with its other boundary currents zero. For the middle region this can also be checked directly by rooting each nonnative branch at B and using its zero-exterior equations, then using the two zero native currents at B. Balanced occupied components are retained.

Each such leaf costs at least 5c at either modulus by the [single-signed-gate estimate](../axial-reserve/README.md) and block parity. At 5063 a leaf directed away from the entrance of the region (away from B in the middle case) pays at least 7c counting its own outward component: a physical terminal uses the stronger 83/13 bound, and otherwise an occupied descendant adds at least 2c to the single-gate bound. At most one hull leaf faces the entrance. If two leaves have the same parity, an occupied intermediate lift costs at least 2c more. If the only two leaves have opposite parity, each parity needs another nonzero charge for its total to be zero. Three or more leaves already cost at least 15c. Consequently a neutral region containing any charged lift costs at least **12c or 14c**, respectively. No vacancy on an exterior-free route to an occupied descendant is possible. For the middle case B itself is occupied under the stated two-owner hypothesis.

At 12c for 3431 only two leaves of the same parity can attain the bound. An opposite-parity pair would require at least four more blocks at two further charged lifts. Equality requires populations 5c,2c,5c on three consecutive lifts, leaf charges ±c and a balanced center. Its two nonzero signed gate currents are ±26 by the character equations. Three [integer potentials](two_gate_potentials.json) further require the two directions at the center to have the same hand. Normalize the positive gate to the negative hand at label zero in the projected chart of [the gate verifier](../axial-reserve/reserve.py), using the sign-preserving hand exchange and residue translation. The negative gate must have offset **3, 4 or 30 modulo 37**. For every other offset, including the opposite hand, a potential has 26 times the difference of its two gate weights strictly above 74 times the verified per-tile upper bound. All other signed gate currents are zero. These three offsets form one orbit under the sign-preserving 120-degree rotation: on the projected coordinate its multiplier is 10 modulo 37. This is a necessary restriction only.

Run `python3 two_owner_replay.py | diff - TWO_OWNER.json` in this directory. The [recorded output](TWO_OWNER.json) includes an exact check of the physical apex formula on all 16 axial and 7 slant unmatched owners in each complete 143 example. Those examples do not satisfy the two-middle-owner hypothesis. The unrestricted 5063 partial contour and its independently verified tile coordinates give a nonvacuous check of the short exterior-free case. Other bank populations and the remaining candidate regions prevent a conclusion for either original number.
