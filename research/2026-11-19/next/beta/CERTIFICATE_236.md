# A computer-assisted exclusion for 236 congruent (9,20,25) triangles

**Theorem.** A triangle of sides 250, 250, 472 has no dissection into congruent copies of a triangle of sides 9, 20, 25.

**Coordinates.** Write d=i√21 and z=(−2+d)/5. The target is (0,472,236+18d). A counterclockwise tile with its directed short edge starting at its anchor has relative vertices **0, 9u, (e+4d)u**, where e is −8 or 17 and u=±zʰ.

The doubled axial areas of one tile and the target are 9·4=36 and 472·18=8496=236·36. Hence every such tiling would contain exactly 236 tiles. To check the two prototypes use the norm x²+21y². The tile angles satisfy α=2γ−π, β=2π−3γ, where γ=arg z is irrational as a fraction of π: otherwise 2cos γ=−4/5 would be a rational algebraic integer. All tiles have a direction exponent h, since positive-length contacts join their edge directions and connect all tiles to the base by a path through tile interiors avoiding vertices. Each side of a tile of short-edge height h has edge direction z^j with |j−h|≤2.

**The finite angular window applies to every tiling.** At a vertex of a tile, the other incident tiles can contribute their corner angle or a straight angle when the point lies inside a tile side. The total angle of the domain near the vertex is 2π or π except at the three target corners, where it is β or 3α. Write γ=2α+β and π=3α+2β. Because α/β is irrational, the total positive coefficients of α and β consumed by all incident tiles are at most 6 and 4. Traverse any consecutive group of these physical sectors. Its directed change in unoriented ray exponent is the number of α angles times 2, minus the number of β angles times 3, plus the number of γ angles. The straight angle contributes zero. The sum of its positive terms is at most 12, and the absolute sum of negative terms is at most 12. Thus any two incident rays differ in exponent by at most 12. At a boundary point take the path inside the domain. Any two incident tiles have their short-edge exponents within 16. At a target corner there is an outer ray with exponent 0 or ±3, so every incident tile has |h|≤17.

Store 420 orientation types, four for each height from −52 to 52. Check the 292 types with |h|≤36 and leave the other 128 permanently available wherever geometrically possible. In an actual tiling, every incident tile needed to keep a checked tile belongs to the stored range. This construction permits tiles of arbitrarily high orientation in the hypothetical full tiling.

**Cell and vertex test.** The two mesh indices of a point x+yd are (⌊25x⌋,⌊25y⌋). For each known displacement, independently allow the mathematical floor and ceiling of each scaled coordinate. This includes every possible motion of a true point's cell, with either sign and without any assumption that the point is a grid point. For each candidate tile, retain cells where all three vertices can lie in the target. For an oriented target edge of vector (a,b), use c=a(y−Aᵧ)−b(x−Aₓ). In mesh units its upper bound in a given unit cell is its value at the lower-left corner plus max(0,a)+max(0,−b). Retain a cell when that upper bound is nonnegative for every tile vertex and every target halfplane. The present certificate uses only this containment test for initialization.

At every candidate vertex cell, enumerate the following counterclockwise angular arcs:

- A corner of a stored tile contributes its opening sector at every candidate anchor plus the corner displacement.
- An edge through the point contributes its straight angle at each interior integer offset. These offsets exhaust the possibilities for a tile vertex on another tile side. On the maximal connected straight contact segment, the banks are both partitioned into complete tile sides of integral lengths, beginning at the same endpoint.
- The outside of a target wall contributes its exterior angle at every possible boundary joint. Distances from a joint to both ends of the wall are sums of 9, 20 and 25. The target vertices have their exterior reflex angles.

To close any specific tile corner at physical P, the complementary angle must be traversable by these arcs in positive circular order, ending at the start direction of the corner. A fixed point test in the *same cell* is weaker than the true same-point requirement and necessary. The finite dynamic program takes intersections along paths and unions over paths. A tile anchor must admit the resulting complement at each of its corners, allowing all shifts for that corner. Recompute the masks synchronously. By induction, no tile of a true tiling can disappear: the actual incident star on a very small circle gives the required path. In particular the exterior arc at the actual target apex must have a complementary path.

**Contradiction.** Starting with 696,515,374 oriented shape/anchor cells, the 29th generation loses the mandatory exterior arc at (236,18), while 292,784,658 cells still survive elsewhere or in the frozen shell. This eliminates unrestricted tilings. The verifier, its independently written Python counterpart, and the generation counts are [mesh_replay.cpp](mesh_replay.cpp), [mesh_stars.py](mesh_stars.py) and [unbounded-no-clearance.log](unbounded-no-clearance.log).

```sh
g++ -O3 -std=c++20 -DWIDE_INIT mesh_replay.cpp -lgmpxx -lgmp -o replay
./replay 52 25 55 2 36 0
python mesh_stars.py 52 25 --freeze-outside 36 --no-clearance
```

The supplied positive control `python mesh_control.py` checks each of 1,475 specified tiles on three meshes. At Q=7 and Q=11, 1,241 anchors have nonintegral mesh coordinates. All placements survive, and removing the compulsory origin tile immediately eliminates its corner star. The input block coordinates are included in `control1475-blocks.json`.

The separate earlier arithmetic classification is needed to infer that **no** triangle can be tiled by 236 congruent triangles of any shape. The numerical exclusion is one case of Erdős problem 634. These calculations have not undergone outside peer review or Lean verification.
