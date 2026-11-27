# Native contacts with two unmatched middle owners

Use the reflected native chart and both two-owner hypotheses of the [native interface theorem](../TWO_OWNER.md). Each exceptional middle step is opposite to the other on its cut. The pure steps belong to the opposite bank. Counts below are necessary conditions on arbitrary complete tilings subject to these hypotheses. Retained words need not be realizable by an interior tiling.

## A length-independent restriction at 3431

Suppose both exceptional steps of each cut lie on the simple path from O to D. On the axial and slant cut let s=+1 and −1 respectively and let j be the heading of the first exceptional step as the path moves from O to D. If j+s is nonzero modulo three on **both** cuts, there are just two possible pairs of positioned paths left. Both force the entire middle region to contain 148 tiles on two adjacent lifts of 74 tiles each, one of them B. The words are in [UNBOUNDED.json](UNBOUNDED.json). The conclusion has no upper bound on the number of steps. The other headings and the case of a separate exceptional circuit are outside this enumeration.

To check finiteness, multiply all mesh coordinates by c. Each pure step is c times a unit. The first bridge is v=(a+bρ)ρʲ or its conjugate factor times ρʲ; the second is −v. The path visits only cR and v+cR, with R the axial lattice. Enumerate the points in both cosets inside the physical board and the undirected unit edges they support. The bounding box in the verifier allows the unit-length bridge shift on both ends. Number the pure edges and record their mod-two endpoint incidence.

Append rows for the endpoint incidence on each axis separately modulo a and modulo b in both coordinates. A pure edge of heading k contributes its endpoints on axis k modulo three. A bridge contributes on axis j+s modulo a and axis j modulo b, by reducing its two ordered short steps. Traversing the corresponding power of a generator gives exactly the endpoint difference by telescoping. Erasing a whole period or an inverse pair leaves these currents unchanged. Multiplication by c in the coordinates preserves the row comparisons since c is invertible in both residue rings. Hence the entire vector equals that of the canonical path by the [two boundary words](../../charge-variation/CANONICAL_SEAM.md). Physical subdivision at T-junctions preserves endpoint currents. Separate pure circuits are excluded by the supported-cycle theorem.

Reduce the two bridge columns modulo the binary span of all pure edge columns. They must have identical remainders, since the canonical vector already belongs to that span. For every pair with equal remainders obtain one support by adding the canonical mask and the two reduction masks. Add all elements of the explicitly computed binary kernel. Its dimension is at most eight for these headings. A simple path uses each pure edge at most once, so its mod-two support determines the available edges exactly. Trace each resulting graph, checking the endpoint path, both oriented bridges, absence of extra edges, both reduced words and the signed area. Place the actual owner triangles from their endpoints and hands. Verify physical containment, disjoint interiors, side membership and compatibility of the two cuts by winding numbers. The [verifier](unbounded.py) finds four pairs with area difference at least 74 tiles. The differences are 74,74,148,148. The one-lift moment and width test in [middle_pairs.py](../middle_pairs.py) excludes a sole B lift in all four. Every other occupied lift costs at least 74, B is occupied by its unmatched owners, and an occupied exterior-free descendant has occupied ancestors. This proves the conclusion.

## Opposite banks within two steps of minimum

Now allow any heading. On each cut suppose the opposite bank has at most a+b+2 steps. Abelianizing the two boundary words and cancelling the two opposite exceptional contributions fixes the signed pure counts on each axis modulo both a and b. Their discrepancy from the canonical count is less than ab, so equality holds as integers. Thus the bank consists of the a east and b southeast steps, with at most one additional inverse pair on an arbitrary axis.

A decomposition into a chord path and supported circuits could put the two exceptional steps together on a detached circuit. It cannot put only one there because the shift changes coset. In the detached case the horizontal displacement of the pure chord path already costs at least a+b pure steps. The circuit therefore has at most two pure steps. The exceptional pair by itself has zero area. With two pure steps it is a parallelogram with opposite unit steps, enclosing 2cL/(ab) tiles for L one of a,b,a+b. This follows by taking the determinant of the unit step with v/c in the three mesh directions. None of these counts is integral on either board. Thus both exceptional steps belong to the chord path and the enumeration covers the cap, including boundaries that pinch before decomposition.

For each position, prune a prefix only when a remaining axis syllable cannot be completed with the available pure steps and exceptional powers in the two boundary groups. The negative pure letters beyond the canonical counts are additional corrective letters in that suffix bound. Check the exact completed words, area and the positioned owner tests just described. The [replay](near.py) counts the resulting pairs by axial/slant excess and middle population. Each entry below is in blocks of c. A one in the column label means two extra pure steps on that bank.

| Board | (0,0) | (1,0) | (0,1) | (1,1) |
|---|---|---|---|---|
| 3431 | 4,6,8,10,12 | 4,6,8,10,12,14 | 4,6,8,10,12,14 | 4,6,8,10,12,14,16 |
| 5063 | 4,6,8 | 4,6,8 | 4,6,8,16,18 | 4,6,8,12,14,16,18 |

All differences of just 2c fail the sole-lift strip and moment test. The [balanced transfer theorem](../../gate-displacement/balanced-transfers/README.md) also excludes every charged middle region of size at most 12c at 3431 under these native hypotheses. The prior neutral-region floor of 14c at 5063 excludes charges in each listed region of size at most 12c.

Run these checks from this directory. The last independently reconstructs the actual 16 and 7 native owners on the two complete 143 boards and checks their modular endpoint currents against the canonical paths.

```sh
python unbounded.py | diff - UNBOUNDED.json
python near.py | diff - NEAR.json
python control.py | diff - CONTROL.json
```
