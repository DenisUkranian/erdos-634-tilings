# The two-row pentagon for 5063 cannot be tiled

Let the tile have sides 35, 13, 43 with the 120-degree angle opposite 43. The convex 245-tile pentagon in the symmetric two-step construction has no tiling. Reflections, arbitrary translations and T-junctions are allowed.

Use physical axial coordinates in the basis 1 and rho = exp(i pi/3). In the notation of the symmetric pentagon construction set a=35, b=13, c=43, t=11, k=2, s=4 and j=2. Set X=(0,sc), Y=X+(0,tb), W=Y+(ta−kc,0), D=X+(ta,tb)−k(a²,ab)/c and V=(ab,b²)/c−(0,c). The five points in boundary order are (0,(s−j)c), Y, W, D, D+jV. The area in tile units is t²−k²+2j(a−s)+j² = 245. Two translates of this pentagon occur in a sufficient 5063 construction.

Write z=(a+b rho)/c, and let n_h count tiles whose two short edges have directions z^h rho^i. The higher/lower orientation cut yields n_h divisible by c for all h other than 0 or 1. At the cut between 0 and 1, close the two adjacent horizontal and vertical exterior sides with their chord. Its displacement is tc z−kc+jc rho, an element of the cut lattice M=c Z[rho]+cz Z[rho] of index c in Z[rho]. The low-side area differs from the triangle of this two-edge arc by a multiple of c, in doubled axial area units. Its doubled axial area is (ta−kc)(jc+tb). Dividing by ab modulo c gives n_0≡t²≡35. Subtracting all other counts gives n_1≡245−35≡38 modulo 43. Each short height outside 0 and 1, when occupied, takes at least 2c = 86 tiles by the common-sign supporting-line argument. Since 245−35−38=172, at most two such heights occur. A gap between the exterior heights and a nonempty farther height would bound that tail with edges of a single 43-step mesh, forcing its positive tile count to be a multiple of 43². Thus the support is contained in one of [-2,1], [-1,2], [0,3].

The C++ program is the published exact exposed-corner search, Git blob 9f969403db869b6c952091ae3ed57173f3b4d1b7. At a strictly convex exposed corner it tests every complete fan of tile angles meeting the two frontier rays. Each rotation, hand and vertex assignment of each permitted height is included. A tile placement based at the corner has a forced translation in these coordinates. The checks use containment, disjoint interiors, line/angle tests and signed height inventories. Each complete search returned NO; budget and singular exits are distinguished by the program. The positive control is a four-fold similar tile subdivided into 16 tiles. The earlier 180-tile excluded pentagon is a negative control.

| Short height interval | Nodes in the 245 polygon | Outcome |
|---|---:|---|
| [-2,1] | 136248 | NO |
| [-1,2] | 139924 | NO |
| [0,3] | 129429 | NO |

The geometric meanings of the intermediate cut, integer-line bounds and fan checker are given in the original project notes. The 245 result applies to this particular pentagon. Filling the scale-one 5063 triangle could avoid this perimeter.

- [Height and congruence arguments](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/patches/decision/SMALL_HEIGHT_BUDGETS.md)
- [Exact exposed-corner procedure and earlier controls](https://github.com/DenisUkranian/erdos-634-tilings/blob/aff4ab39ec4365fd72f29aab9f7beb04adc817f4/research/2026-11-20/semiprimes/continuation/patches/decision/PENTAGON_SWEEP.md)
