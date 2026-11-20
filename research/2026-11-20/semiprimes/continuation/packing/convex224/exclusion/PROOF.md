# The 224-tile quadrilateral does not tile

The convex quadrilateral with CCW directed sides
```
(length, height, phase) = (143,0,0), (172,−1,1), (260,1,2), (315,1,4)
```
cannot be tiled with the (35,13,43) tile. A direction with height h and phase j is zʰρʲ, where ρ=exp(iπ/3) and z=(35+13ρ)/43. This excludes the specific construction with two translated holes of 224 tile units. It does not decide whether the board for 5063 can be tiled by crossing their boundaries.

The [source guide](SOURCES.md) links the exact earlier lemmas and includes offline copies. The population table, translated lattice choices and finite vertex checks below are specific to the present quadrilateral.

## All orientation populations

Write R=ℤ[ρ]. In axial coordinates the vertices are
```
O=(0,0), A=(143,0), C=(195,140), D=(−4095/43,15120/43).
```
Both O and C lie in R∩zR, since C/z=260+55ρ. The point D is 315ρz. The determinant area of the quadrilateral is 224·455 and one unit tile has determinant area 455.

At a cut between short heights h and h+1, the boundary of the union of high tiles differs from the exterior edges above h by whole long edges with displacements in 43zʰ(R+zR). This lattice has axial covolume 43. Closing the high exterior-side chain by a chord in that lattice therefore gives the count of high tiles modulo 43, by signed area and coprimality of 455 and 43. For h=0, the chain is C→D→O. Its closing vector C belongs to 43(R+zR); indeed C=4·43·ρz⁻¹+143 lies in R, and reduction at the prime 6+ρ gives 195−6·140≡0 mod 43. Equivalently 43(R+zR) is the norm-43 Eisenstein ideal (6+ρ). The determinant area of OCD is 81,900=180·455. For h=−1 the missing edge AC is itself four whole 43-steps of height −1, so closing the chain gives the entire board. Below −1 or at and above 1 the exterior term is respectively the whole board or empty. This gives n₀≡1 and n₁≡8 (mod 43), with all other n_h divisible by 43.

Let G_h be the signed population whose positive convention assigns the CCW a-edge even rotation phase. The signed exterior totals by height are E₋₁=−172, E₀=143 and E₁=575. The ordinary and alternating characters give ΣG_h=−26 and Σ(−1)ʰG_h=−4. Each height also obeys 22G_h≡E_h (mod 43). Thus level zero has at least 36 positive and 8 negative tiles, and level one has at least 20 positive and 31 negative tiles. Nonzero populations away from those two levels cost at least 86 tiles by the per-line exclusion of a 43-tile level, since each exterior side there is a multiple of 43. The budget leaves space for at most one such height. A vacancy past the last exterior height cannot be crossed: the detached far tail would have a one-height whole-long-edge boundary and its size would be divisible by 43²>224. Consequently only −2,−1,0,1,2 need be tested.

Writing U_h and V_h for the signed counts of tiles with long height h+1 and h−1 gives U_h+V_h=G_h and 22G_h−43(U_{h−1}+V_{h+1})=E_h. Also |U_h|+|V_h|≤n_h. The independent standard-library integer enumeration in `profiles.py` checks these equations for every permitted population, with the following possible unsigned populations in order from height −2 to 2.

| n₋₂ | n₋₁ | n₀ | n₁ | n₂ |
|---:|---:|---:|---:|---:|
| 0 | 0 | 87 | 137 | 0 |
| 0 | 0 | 173 | 51 | 0 |
| 0 | 86 | 87 | 51 | 0 |
| 0 | 0 | 44 | 51 | 129 |
| 0 | 0 | 87 | 51 | 86 |
| 86 | 0 | 87 | 51 | 0 |

## The possible translated lattices

Let π=6+ρ and π′=7−ρ. They have norm 43, ππ′=43, and z=π/π′. At π, a short-height h node is a residue class of vertex coordinates modulo the valuation ball {vπ(x)≥h}. At π′ the threshold is −h. Every short-h tile has its three vertices in a common node at each prime. All coordinates lie in R[1/43] by the integer-offset lemma. In a band [L,H] every vertex has vπ≥L and vπ′≥−H: all tile displacements are in this module and the polygon includes the origin. The endpoint-coset proof is independent of connectedness through full edges: the oriented boundary currents from any other coset have zero derivative at every endpoint and hence vanish line by line. Integration then contradicts positive area.

At any fixed h and prime, all nodes disjoint from exterior subtrees have population divisible by 43 and a nonempty one has at least 86 tiles. This follows from the project’s phase-subtree cut identity and line-count lemma. The same conclusions on a node's own short population hold if its subtree and each child are exterior-free. At heights zero and one, all relevant exterior nodes at any ancestral cut lie in one distinguished node. For the positive valuation the two height-one exterior edges lie in its zero-residue level-one node (O,C,D belong to z times the π-integral ball); all exterior edges of height zero or higher lie in its zero-residue level-zero node. For the reversed valuation, the edge AC of height −1 has integer endpoints in the level-zero core, as does OA; all exterior edges lie in the level-one core vπ′≥−1. Subtracting exterior-free nodes from the total therefore gives the previously computed residues in the core at each prime. The same per-node line congruences for G show that the zero core costs at least 36+8=44 and the one core at least 20+31=51. In a nonempty exterior-free subtree a vacant root cannot have occupied descendants: its boundary is a chain of whole 43-edges of a single height, which forces 43² to divide its tile count.

At heights −1,−2,2, a nonzero population is 86 or 129, and all its tiles lie in one translate of zʰR. At height 2 there is no exterior node in a descendant subtree for the positive valuation. For the reversed valuation every vertex of the entire board is automatically in its one global level-two ball by the band bound. The statements at −2 and −1 work the other way, with the one possible exterior edge AC at −1. At level −1 for the reversed valuation that edge has whole length 4·43. If the −1 short population is 86, its core may be empty, but two occupied nodes are impossible. For clarity, any off-core node costs 86; if it costs 86 the whole 86-population is already in that node. At the other valuation the global band bound applies when −1 is minimal. At −2 the band bound applies in the same way. Integrality away from 43 and primeness of the two factors convert the single-node restrictions into a Euclidean lattice translate.

In all rows start with R at height zero and zR at height one. The following list of optional or actual third lattices exhausts the overlist, with each integer r ranging from 0 to 42.

| Mode | Population alternative | Additional short height and lattice |
|---:|---|---|
| 0 | n₁=137 | h=1, r+zR |
| 1 | n₀=173 | h=0, rz+R |
| 2 | n₋₁=86 | h=−1, r+z⁻¹R |
| 3 | n₂=129 or 86 | h=2, rz+z²R |
| 5 | n₋₂=86 | h=−2, 143+rz⁻¹+z⁻²R |

When n₀=87 or 44 a further 86-tile node cannot coexist with the 44-tile core (at either prime), so all zero vertices lie in R. Likewise n₁=51 forces all one vertices into zR. For mode 0 the other prime at h=1 is fixed by the global band bound, and at π there is room for at most one additional 86-tile node. Its parent at height zero is the core; if a different parent with a descendant were vacant, its subtree would need at least 1849 tiles. The 43 residues of an integer r represent exactly these first-level choices. For mode 1 use the reversed valuation and its parent bound vπ′≥−1; the 43 representatives rz supply all level-zero choices. For mode 2 the parent at reverse height zero must again be its occupied core, leaving 43 representatives r. For mode 3 the positive level-one parent must be the unique core, and multiplication by z gives all 43 possibilities rz of the next digit. In mode 5 the level −1 is vacant, so the reverse parent at −1 must be the exterior node of AC. Its representative is 143. Moving down one digit gives precisely 143+rz⁻¹. The unused prime in each of the last three cases is controlled by the global band bound. Each integer representative system is complete because R/(π) and R/(π′) both have 43 elements represented by the rational integers.

## Finite vertex-fan check

For each lattice, enumerate all translations of the twelve oriented triangle templates whose vertices satisfy the four target half-planes. A lattice bounding box is obtained by applying the inverse basis matrix to the four target vertices and rounding outward. All physical coordinates are scaled by 43² and stored as integers. The directions, including the possible long sides at height ±3, are sorted using exact axial cross products.

At an interior tile vertex the incident vertex angles form a fan of 360 degrees or a fan of 180 degrees bounded by a through-edge of a tile. At a regular boundary vertex they fill the inward half-plane, and at a target corner they fill the precise corner wedge. Every sector in the fan must be an actually available placement translated to that vertex. A candidate sector can therefore be removed if it does not belong to any admissible fan. This implication remains valid at T-junctions. At a regular point that has no tile vertex there is no obligation. A target corner, however, requires at least one fan.

The checker represents available sectors as edges of an ordered circular graph of rays. Reachability from the first ray and reverse reachability to the last one identify all sectors occurring on some path through the prescribed wedge. The internal test tries each initial ray and a half-turn or full-turn span. Removal of a triangle removes its incidence at its other two vertices and schedules those points for a fresh check. Missing every fan at a required target corner is an exact contradiction. The code imposes no population constraint during this stage, giving a larger search than required.

Run `sh replay.sh` using Python 3 and a C++20 compiler. All 43 shifts of each of the five different lattice cases yield a corner contradiction. As a positive control, an a-by-b parallelogram spanned by 35 and 13ρ² retains both of its actual triangles, including when an optional extra translated grid is present. This computational exclusion is an internally reproducible research result, separate from independent external review.
