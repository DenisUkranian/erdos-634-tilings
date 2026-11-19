# What the vertex filters determine for 280

The remaining candidate for the global count 280 has target sides \(90,90,140\) and unit tile \(6,5,9\). Using the axial basis \(1,i\sqrt2\), its vertices are \((0,0),(140,0),(70,40)\). The smaller auxiliary theta target has sides \(90,90,60\), vertices \((0,0),(60,0),(30,60)\), and count 180. The auxiliary target has now been excluded by a full computation. Consequently any 280 tiling must avoid a complete straight vertex seam. [Full proof for 180](../theta6/PROOF.md). [Seam theorem](../alpha/VERTEX_SEAMS.md).

For a directed length-five side \(5u\), the third vertex is \((-2+4i\sqrt2)u\) or \((7+4i\sqrt2)u\), \(u=\pm [(-1+2i\sqrt2)/3]^h\). With all orientations restricted to \(|h|\le1\), vertices of the required exterior corners fail on pass 27 for 280 and on pass 11 for 180. Allowing \(|h|\le2\) leaves possible placements even after checking each half-unit boundary sample against the opposite side. At \(Q=9\), 212,110 shape/cell pairs survive for 280 and 66,214 for 180. These nonempty sets do not provide a dissection. A positive control covered by 16 tiles keeps exactly 16 placements. The frozen exterior-shell experiment at \(B=40,Q=9\) also leaves all central heights nonempty.

The geometric filters, including permissive rounding for arbitrary translations, are described in [the general mesh note](../beta/MESH_PROOF.md). Compilation with HALF_EDGES uses the shared half-unit checker.

~~~sh
g++ -std=c++20 -O3 -DWIDE_INIT -DHALF_EDGES -I../cubes/beta_shapes mesh.cpp -lgmpxx -lgmp -o /tmp/ep634-280-star
/tmp/ep634-280-star 1 9 100 2
/tmp/ep634-280-star 1 9 100 3
/tmp/ep634-280-star 2 9 100 2
/tmp/ep634-280-star 2 9 100 3
/tmp/ep634-280-star 2 9 100 4
~~~

[Earlier exact-geometry work and positive 320-tile control](../../nov19/alpha280/RESULTS.md).

An analytic argument gives absolute bounds of 129 (alpha) and 80 (theta). Starting from those unconditional bounds, the Q=3 star/half-edge/mirror test with no clearance leaves respectively only heights from −37 to 37 and from −30 to 30. This narrows every genuine tiling, without assuming a bound on an untested region. The reflection test maps each absolutely positioned candidate to possible cells for its vertical mirror in the reflected tiling. It does not require the original tiling to be symmetric. [Height proof](HEIGHT.md) · [Alpha trace](global-q3-alpha.log) · [Theta trace](global-q3-theta.log) · [The exact 277 packing](../audit/transfer280/RESULT.md) · [Drawing of the packing and obstruction](packing277.png).

~~~sh
g++ -std=c++20 -O3 -DWIDE_INIT -DMIRROR_CELLS -DHALF_EDGES -I../cubes/beta_shapes mesh.cpp -lgmpxx -lgmp -o /tmp/ep634-659-mirror
/tmp/ep634-659-mirror 129 3 60 2 500 0
/tmp/ep634-659-mirror 80 3 60 3 500 0
~~~

At mesh 18, starting with the unconditional alpha height bound 37, the no-clearance test narrows the band to 26. [Trace](alpha37-q18.log). Three tests starting separately from height 26 bound the possible true heights by 21 at \(Q=36\), 15 at \(Q=54\), and 14 at \(Q=72\). Each retains admissible cells. [Trace 36](alpha26-q36.log) · [Trace 54](alpha26-q54.log) · [Trace 72](alpha26-q72.log). Starting from the absolute bound 14, the \(Q=108\) run further gives \(|h|\le8\); its 2,878,449 remaining cells include all possibilities. [Trace 108](alpha14-q108.log). Each run uses the same no-clearance executable and arguments with target 2, cutoff 500 and clearance 0.

**Exact D9 experiment for 280.** From the earlier 259,328 D9 candidate placements, exact vertex stars and complete facing whole-side chains reduce the pool to 196,212. The same filter retains all 320 actual placements of the known theta-eight witness, and removing a corner tile makes that control fail. This run is limited to the denominator-nine grid for the full alpha target. The nonsymmetric, no-vertex-seam possibility remains open. [Implementation](sparse_fans.cpp) · [All pass counts](d9-whole-edge.log).

The unrestricted height-eight run at \(Q=162\) stabilizes after 25 passes, with 1,639,815 surviving shape/anchor cells. The uppermost positive height contributes 201 of them. Recreate the final cell list with the no-clearance executable and the command below. [Q=162 trace](alpha8-q162.log).

~~~sh
DUMP_CELLS=/tmp/ep634-alpha8-q162.cells /tmp/ep634-659-mirror 8 162 95 2 500 0
~~~

**All corner choices.** Read the three sectors of the apex from its left leg to its right leg. They are a permutation of \(\alpha,\beta,\beta\); each sector has two choices for the order of its two incident tile sides. Each base corner gives a single \(\alpha\) tile with two choices. This gives 96 distinct configurations of five locally compatible tiles. Vertical reflection pairs them into 48 classes. Coordinates use the basis \(1,i\sqrt2\). The least common denominators of the five tiles' coordinates in those 48 classes are 3 (4 classes), 9 (20), 27 (8), and 81 (16). This is an exhaustive count of local patterns allowed by shape, prior to completing a tiling. It also explains why limiting the full triangle to a denominator-nine lattice omits 24 of the 48 potential corner classes immediately. [Exact enumeration, containment, disjointness and reflection check](corner_patterns.py). Run with Python 3.9 or newer.

## Finite reduction for every possible 280-tiling

The mesh at (Q=108) proves that every unit tile has short-edge exponent of absolute value at most eight. Complete tile edges connect every corner to the base, by the argument in the [theta proof](../theta6/PROOF.md). All five-edge displacements are in (3^{-8}mathbb Z[isqrt2]). The factors 6 and 9 absorb the one or two additional powers of three in the other edges. Thus all placements can be enumerated at denominator (3^8=6561). This is a completeness deduction from the angle bound and connectivity of whole sides.

Lifting the (Q=162) cells to that exact grid and imposing exact containment first yields 2,722,267,266 placements. Oriented endpoint balance leaves 1,141,260 positions. Exact vertex fans and whole-side opposite-bank chains reduce that set to 1,000,898. Pass 32 is the fixed point. No short-edge exponents of absolute value eight survive this last test. A tiling, if it exists, has all its corners on (3^{-7}mathbb Z[isqrt2]). The surviving pool is an overestimate of what can participate in a single tiling. The existence of a simultaneous selection of 280 tiles is unresolved. [Exact lift trace](alpha-d6561-lift.log) · [Fan and contact trace](alpha-d6561-fan.log).

To reproduce, first generate the cells using the command above. Run these commands from this directory. The exact lift uses substantial memory and temporary space. Its output SHA-256 is <code>cf491b5c80a9659256b6ee2a24534fd2b91e4a7b67c304c82f5742c052940ec7</code>. The filtered output digest is <code>d0e75e8a09847b30ad03c030942d4a20a0a66bd3166b5465c31481e09d746246</code>.

~~~sh
g++ -O3 -std=c++20 ../theta6/lift_cells.cpp -lgmpxx -lgmp -o /tmp/ep634-alpha-lift
/tmp/ep634-alpha-lift 6561 280 /tmp/ep634-alpha-pool /tmp/ep634-alpha8-q162.cells
g++ -O3 -std=c++20 sparse_fans.cpp -o /tmp/ep634-alpha-fans
/tmp/ep634-alpha-fans /tmp/ep634-alpha-pool /tmp/ep634-alpha-filtered
~~~
