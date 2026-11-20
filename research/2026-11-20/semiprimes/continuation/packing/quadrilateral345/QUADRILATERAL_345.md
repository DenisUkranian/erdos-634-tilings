# The 345-tile quadrilateral cannot complete the displayed 5063 packing

The [coordinate certificate](placements345.json.gz) verifies 4373 ordinary unit tiles outside two translated copies of this quadrilateral. Run `python3 verify_packing.py` and `python3 check_345.py` for the covering, lengths, angles and inventories.

The [independent finite replay](LOCAL_OBSTRUCTION.md) also proves this result directly from the tile geometry. The analytic deduction below uses the project's manuscript version of the stopped-run theorem for 120-degree tiles, including its version with the acute labels interchanged. It concerns the specified quadrilateral. It leaves the original 5063 triangle undecided.

Let the tile sides opposite angles α, β and γ be 35, 13 and 43, with γ = 120° and α + β = 60°. Write ρ = exp(iπ/3) and z = (35 + 13ρ)/43 = exp(iβ). Use axial coordinates x + yρ. The four vertices in cyclic order, multiplied by 43, are (35217,0), (46397,0), (30212,32025), (35217,13545). The doubled axial area is 345 · 35 · 13. Its boundary vector lengths and headings, with heading z^h ρ^j, are

| Length | h | j |
|---:|---:|---:|
| 260 | 0 | 0 |
| 645 | 2 | 1 |
| 385 | 1 | 4 |
| 315 | 0 | 4 |

Along the line y = 0 the whole polygon meets that line precisely in the segment from (819,0) to (1079,0). Its interior angles at those ends are α + β and π − (π/3 + 2β) = 2α. In particular neither end admits a γ tile. The two adjacent boundary sides have physical lengths 315 and 645.

For every 1 ≤ j ≤ 5, any representation of j times one tile-side length as a nonnegative integer combination of 35, 13 and 43 consists entirely of sides of that same length. This is the v = 1 purity calculation with u = 6 and K = 5. The supplied arithmetic checker also verifies all fifteen instances directly. The acute angles are rationally independent, since 2 cos β = 83/43 is rational and nonintegral, while a rational multiple of π would give an algebraic integer.

Apply the manuscript's exterior stopped-run argument with β designated as the starting angle. At the left end a tile on the supporting side showing β on its c edge leaves precisely α. The adjacent tile has angle α and consequently puts a b or c edge across the starting tile's a-ray. At the right end the sector 2α contains no β. These are the two endpoint protection hypotheses with the labels exchanged. The available adjacent true boundary lengths 315 and 645 both exceed K · 35 = 175. The run lemma requires at least K + 1 = 6 consecutive c edges on this supporting side.

The distant reflex corner does not interrupt this application. Below axial height y = 315 the polygon is exactly the wedge strip given by x ≥ 819, y ≥ 0 and 2135x + 1079y ≤ 1079 · 2135. The boundary interval being tested lies on a single supporting line. In fact, to refute a run of length at most three, every triangle or trapezoid grid vertex in the stopped-run argument lies at axial height at most 3 · 35 · 13/43 < 32. The prospective tile incident to such a vertex can increase axial height by at most 2 · 43/√3 < 50. These bounds follow from the grid basis consisting of a horizontal c vector and a vector of length 35 making angle β with the horizontal, with sin β = 13 sin(π/3)/43. Thus the local configurations are in the portion with the two genuine adjacent sides. This argument also permits applying the run lemma with purity only through three to force four consecutive c edges.

If X, Y and Z count the 35, 13 and 43 edges on the 260 side, its partition satisfies 35X + 13Y + 43Z = 260. Reduction modulo 13 gives X ≡ Z modulo 13. The bounds X ≤ 7 and Z ≤ 6 force X = Z. It follows that Y = 20 − 6Z, so Z ≤ 3. This contradicts even the four-edge consequence. Reflections and T-junctions are allowed throughout.

The 120-degree stopped-run adaptation and the interchanged-label version are in [F2_V1_PURITY.md](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/counting/inputs/F2_V1_PURITY.md) and [I120_THEOREM.md, section 2](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/counting/inputs/I120_THEOREM.md). The source argument of [Beeson and Roşu, section 11, Lemmas 32–34](https://arxiv.org/html/2607.23453v4#S11), is stated for 3α + 2β = π. Its original Lean verification does not cover the project's changed hypotheses. This manuscript dependency also enters the project's earlier exclusion of the side-455 equilateral triangle. There the 455 side has at most five c edges and the run lemma requires six.
