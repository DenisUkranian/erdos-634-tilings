# The 280-tile alpha-isosceles candidate

For tile sides $(a,b,c)=(6,5,9)$, the candidate has sides $(90,90,140)$. Its existence remains undecided. The following restricted obstructions are calculations of this investigation, dated 19 November 2026. The geometric notation and existing tilings in this note draw on [Bonfioli's paper](https://github.com/ElVec1o/erdos_634_proof/blob/119bec0dd0158ddeb239686d5464eb7104e3b42d/paper/erdos-634.tex). The scale construction for $W$ and the two-piece constructions should be compared with [Paliy's repository](https://github.com/DenisUkranian/erdos-634-tilings/tree/0f7935b71fd958bd764bccf079e1e70bc68ce351).

## Accounting for two corners

Write $(x,y)$ for the Euclidean point $(x,\sqrt2 y)$. The target vertices are $A=(0,0)$, $B=(140,0)$ and $C=(70,40)$. With $D=(50,0)$, triangle $ADC$ has sides $(50,60,90)$ and the ordinary $10^2$-tile triangular grid. The remaining $DBC$ has sides $(60,90,90)$ and area 180 tiles. This is Bonfioli's $\theta_6(2,3)$. A tiling of that smaller triangle therefore suffices. Putting a second mirrored grid against the other equal leg leaves the centrally located $(40,60,60)$ triangle, or $\theta_4(2,3)$. Bonfioli's lower bound $T\ge f+2=5$ in the corollary labelled `cor:thetakill` rules out this pair of grids. Bonfioli's 18 November update gives $\theta_7(2,3)$ at its notch threshold and lists $\theta_6(2,3)$ as open. His exact 320-tile $\theta_8(2,3)$ is the positive control below. [Updated notch theorem and example](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L389-L411).

## Three macropiece obstructions

Let $\alpha$ be opposite 6, $\beta$ opposite 5. Thus $\cos\alpha=7/9$, $3\alpha+2\beta=\pi$ and $\beta<\alpha<2\beta$. A macropiece here means that a complete edge-to-edge exterior triangle appears as the union of its assigned unit tiles. Its outer sides may have T-junctions with other pieces.

* The published 224-tile triangle has sides $(60,108,112)$. Its smallest width is its altitude $40\sqrt2$ to the longest side, exactly the height of $ABC$. Any copy in $ABC$ must therefore have its length-112 edge horizontal on $AB$ and its opposite vertex at $C$. There the copy occupies $2\alpha$, since the law of cosines gives $\cos(2\alpha)=17/81$. The total angle left is $\pi-4\alpha=2\beta-\alpha$, strictly between zero and the smallest tile angle $\beta$. Even if this gap has two components, no tiles can fill it.
* The published 207-tile triangle has sides $(81,81,138)$ and base angles $\beta$. At each of $A,B$, the only possible single original tile angle is $\alpha$, as $\beta<\alpha<2\beta$. The 207-tile piece cannot contain either corner: its larger angle exceeds $\alpha$, while its $\beta$ angle would leave a positive gap below $\beta$. Delete the two mandatory base-corner unit tiles. Each may have either a 5- or a 9-edge on the base. The remaining convex pentagons, in orientation order $(5,5),(5,9),(9,5),(9,9)$, have squared diameters $16900,17200,17200,1416100/81$, all below $138^2$. No one of them contains the 207-tile triangle. Exact vertex and distance checks are in `check_geometry.py`.
* Two 126-tile $W$ pieces, each with sides $(45,81,84)$, cannot occur together. Put $z=(-1+2\sqrt{-2})/3$. The tile angles give directed side orientations $\pm z^j$; positive-length edge contacts propagate this description from the target boundary to all tiles, allowing both chiralities. The sign is unambiguous because $z$ has infinite order ($z+z^{-1}=-2/3$ is rational and not an algebraic integer). Give a counterclockwise edge the signed value $\pm\ell/8$ according to this direction. Opposite interval chains cancel even at T-junctions. The perimeter values are $40$ for $ABC$, $\pm 1$ for a unit tile and $\pm 6$ for $W$. For example, $W$ with vertices $(0,0),(45,0),(17,56)$ has directed edges $45,84z,-81z^4$. Two $W$ pieces leave 28 units. The upper bound $6+6+28=40$ forces every piece to have positive total. Each then has exactly one negative edge (81 for $W$, 6 for a unit). In a genuine T-junction let $k$ pieces have corners and one pass straight through the vertex. There are $k+1$ rays, each requiring exactly one negative incidence across it. A positive straight edge supplies none and the $k$ corner pieces supply at most $k$. Hence no positive edge passes through such a junction. Since the exterior has only positive edges, each negative edge is internal and its opposite bank partitions it into whole positive edges. A unit's length 6 cannot be made of lengths $5,9,45,84$.

These arguments do not presuppose how a hypothetical remainder would be tiled.

## Exhaustive integer-scaled triangular pieces through twelve

A similar piece of integer scale $s$ has area $s^2$ and perimeter value $\pm s$. The necessary equations are $\sum s^2=280$ and $\sum\pm s=40$. Cauchy excludes at most five pieces. The exact geometric enumeration in `macro.cpp` excludes every count from six through twelve, allowing both signs and both chiralities.

| Pieces | Visited states | Maximum placed |
|---:|---:|---:|
| 6 | 68 | 3 |
| 7 | 1,630 | 6 |
| 8 | 13,163 | 7 |
| 9 | 71,620 | 8 |
| 10 | 313,076 | 9 |
| 11 | 1,020,813 | 10 |
| 12 | 2,874,799 | 11 |

At a convex corner of the remaining region, a tile must place a vertex there and have a side along the first bounding ray. The search tries the three possible corner angles, both incident-side assignments and every possible scale $1\le s\le16$. It exactly checks triangle containment and disjoint interiors, and recursively subtracts the three oriented sides. The signature and area equations prune branches via integer dynamic programming. Every maximal connected straight seam has two banks of whole integer-length sides, with shared extreme endpoints. Hence every breakpoint has integer distance from either end. On an exposed boundary subinterval bounded by two convex corners, its length must be a sum of $5,6,9$. These necessary tests permit arbitrary T-junctions. Direction exponents outside the implemented coordinate range signal an incomplete search, as do resource limits. All seven listed runs reach exhaustion; the threefold-dilated tile control yields valid dissections both as one scale-3 piece and as nine scale-1 pieces.

For the smaller $\theta_6$ target the same program rules out all layouts with at most 14 integer-scaled similar macrotriangles. Here the signature is $30$ and the area is 180, so at least five pieces are required. The complete counts for 5 through 14 pieces were 5, 245, 1,309, 9,370, 29,601, 78,305, 220,481, 495,663, 1,099,162 and 2,401,587 visited states. The 15- and 16-piece searches stopped at the four-million-node cap. Thus a construction by a corner grid and a $\theta_6$ dissection needs at least fifteen integer-scaled similar pieces in the $\theta_6$ part.

## Endpoint tests on fixed orientation sets

For denominator $D$, `pool.cpp` enumerates all counterclockwise shapes whose two displacement vectors from the corner between sides 5 and 6 have coordinates in $D^{-1}\mathbb Z^2$. It solves the three squared-length equations with the exact metric $x^2+2y^2$. On each affine line, interval endpoints of the oriented boundaries must cancel with the outer polygon. A placement with an endpoint of a sign that lacks opposite support can be eliminated, and a missing required exterior endpoint proves impossibility. Even if arbitrary real translations are permitted, tracing support back from an exterior vertex can stay in its own lattice coset, since every enumerated displacement preserves that coset. This checks an orientation restriction, without assuming all valid tilings use these orientations.

| Target | $D=3$, 12 shapes | $D=9$, 20 shapes, initial | $D=9$, surviving |
|---|---|---:|---:|
| $(90,90,140)$ | Contradiction, sweep 19 | 3,486,452 | 259,328 |
| $\theta_6$, $(90,90,60)$ | Contradiction, sweep 9 | 2,138,946 | 76,470 |
| $\theta_8$, $(120,120,80)$ | Contradiction, sweep 12 | 4,127,226 | 456,106 |

All 320 exact triangles from Bonfioli's $\theta_8$ witness survive the $D=9$ filter, as checked against its published rational coordinates. The supplied script independently checks that each of the 320 is congruent to the unit tile, inside the target, pairwise interior-disjoint, and that their areas sum to its area. Search of the 280 individual tiles with higher orientations permitted reached depth 234/280 in 531,969 calls at its time limit. A separate $D=9$ search reached 241/280 and the smaller $\theta_6$ reached 164/180. These depths supply neither a complete tiling nor a negative certificate.

## Reproduce

The macro search uses C++20 and GMP. Each resource limit produces a distinct incomplete status. The geometry and published-witness check use Python's standard library.

```sh
g++ -O3 -std=c++20 macro.cpp -lgmpxx -lgmp -o macro
for k in 6 7 8 9 10 11 12; do ./macro "$k" 900 8000000 candidate.txt; done
for k in 5 6 7 8 9 10 11 12 13 14; do ALPHA_TARGET=180 ./macro "$k" 900 8000000 theta6.txt; done
ALPHA_CONTROL=1 ./macro 1 60 1000 scale3.txt
ALPHA_CONTROL=1 ./macro 9 60 1000 nine_units.txt
g++ -O3 -std=c++17 pool.cpp -o pool
for t in 280 180 320; do ./pool 3 "$t"; ./pool 9 "$t" "pool$t"; done
python3 check_geometry.py
python3 check_geometry.py --theta8-witness tiling_320_6_5_9_on_80_120_120.exact.txt --pool pool320
```

[Bonfioli's exact 320-tile witness](https://github.com/ElVec1o/erdos_634_proof/blob/119bec0dd0158ddeb239686d5464eb7104e3b42d/data/witnesses/tiling_320_6_5_9_on_80_120_120.exact.txt).
