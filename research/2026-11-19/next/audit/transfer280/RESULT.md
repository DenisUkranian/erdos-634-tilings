# Cutting and repairing the known 320-tile example

An exact packing of **277 tiles** in the \((90,90,140)\) candidate uses 100 grid tiles and 177 further tiles in \(\theta_6=(90,90,60)\). Its complement is an untileable hexagon of area three tiles. A separate exhaustive check proves that any complete \(\theta_6\) obtained from a single rigid placement of the known 320-tile \(\theta_8\) witness must contain **at least 13 new tiles**. A new tile here is one that is not identical in position and shape to any of the 320 placed source tiles. All real translations, rotations, and reflections of the source are allowed. Arbitrary tilings of \(\theta_6\) and of the 280 target remain undecided by these results.

The starting \(\theta_8\) is the published exact dissection of \((120,120,80)\) into 320 copies of \((5,6,9)\), rendered here in axial coordinates \(x+\sqrt{-2}\,y\). It has vertices \((0,0),(80,0),(40,80)\). A single copy of the same unit tile scaled by ten adjoins \(\theta_6\) to form the 280 target, as in Beeson's gluing. [Source witness](../../cubes/tiling_320_6_5_9_on_80_120_120.exact.txt) · [Original public coordinates](https://github.com/ElVec1o/erdos_634_proof/blob/119bec0dd0158ddeb239686d5464eb7104e3b42d/data/witnesses/tiling_320_6_5_9_on_80_120_120.exact.txt) · [280 geometry](../../../nov19/alpha280/RESULTS.md)

## The partial packing and its obstruction

To reproduce the positive placement, place the canonical \(\theta_6\) in \(\theta_8\) with its base endpoints at \((10,20),(70,20)\) and its apex at \((40,80)\). Exactly 176 original tiles lie wholly inside. Remove original tiles in four successive neighborhoods defined by positive-length side contact with the clipped tiles, leaving 146 pins. A convex-corner search placed 31 further unit tiles but could not complete this pin set. Glue the ordinary 100-tile grid along the adjoining side. The independently checked coordinates in [packing277.json](packing277.json) are integers divided by 9. There are 38,226 tile pairs. Each pair is interior-disjoint, and all 277 tiles have the required squared lengths \(25,36,81\) and lie in the target. [Coordinate verifier](packing.py) · [Receipt](packing.log)

The uncovered hexagon, in counterclockwise order and divided throughout by 9, has vertices
\[
(630,180),\ (720,180),\ (690,240),\ (648,216),\ (645,210),\ (699,210).
\]
This boundary results from canceling the oriented edges of the 277 cells against the outside. The fourth edge has squared physical length \((3^2+2\cdot6^2)/9^2=1\). Both its ends are convex. A tile bordering the open edge cannot continue through either end, so the edge would have to be a union of full sides of lengths 5, 6 or 9. This proves that these specific 277 placements cannot be extended.

## Why 12 replacement tiles cannot suffice

If at most 12 unit tiles of a tiling of \(\theta_6\) are new, at least two distinct sides of \(\theta_6\) have segments on old tiles. Otherwise two sides, of combined length at least 150, would be covered entirely by new tiles. A new tile normally contributes at most its longest edge, of length 9, to this pair of sides. A tile contributing positive lengths on both sides must occupy their common corner; at most one such tile exists. Its second side contributes at most 6. The total is at most \(12\cdot9+6<150\).

The two supported sides determine the search. Rotate coordinates so that the canonical base is horizontal. The rotated source must have one of 16 directions, because at least one of the three target sides must have an edge direction of the source. The extra two sets of possible base directions are found by multiplying the source edge directions by the conjugate unit leg directions \((1/3,\pm2/3)\). Reflection introduces no additional triangular regions, since \(\theta_6\) is isosceles. For a candidate translation let the three lower halfplane thresholds, against \(2x-y,-2x-y,2y\), be \(u,v,w\). They satisfy \(u+v+w=-120\). A source tile is contained precisely when its three minima exceed or equal the respective thresholds. Each of the two old-supported sides has a threshold equal to a minimum of a contained triangle. Enumerating all pairs of such attained thresholds and obtaining the third from their sum is therefore exhaustive for this edit bound.

At least \(180-12=168\) old tiles must be available. The 16 orientation checks leave only six translations, all with horizontal base and the following numbers of contained old tiles.

| Base left endpoint | Whole old tiles | Deletion masks checked |
|---|---:|---:|
| \((10,20)\) | 176 | 56,371 |
| \((35/3,50/3)\) | 170 | 184 |
| \((15,10)\) | 169 | 16 |
| \((10,0)\) | 168 | 1 |
| \((55/3,10/3)\) | 168 | 1 |
| \((20,0)\) | 168 | 1 |

All six placements are contained in the source triangle. Thus the unfilled part after keeping every whole source tile consists of clipped portions of source tiles. Suppose some old tiles are deleted in a completion. Any component of deleted tiles that is separated from all clipped tiles in the graph of positive-length side contacts can be filled back with its old tiles. A new tile cannot cross from one such component to another solely through an isolated point. Restoration preserves the tiling and decreases the number of new tiles. It suffices, therefore, to grow deletion sets from the clipped tiles along positive-length tiling contacts. The program uses the entire original tile adjacency relation, which also allows contacts beyond the target corner. That enlarges the search conservatively. Retaining at least 168 old tiles bounds the number of deletions in each of the six rows.

The 56,574 resulting masks were all checked. In the last five rows the retained tiles violate the necessary boundary-joint positions for every mask. In the first row the exact residual polygon solver explored 72,925 states in total. At a convex corner it tries all unit tiles that start on the bounding ray, tests all three sides, and checks containment, signed boundary cancellation and nonoverlap with the pins. If a true filling exists it contains one of these corner choices. The underlying search is the archived point-exact solver for this tile. Its necessary angle, integer-offset, and perimeter tests also apply in the presence of T-junctions. Every mask exited through exhaustion; resource exits are separate. [Orientations and translations](crop.json) · [Deletion counts by depth](editsets.json) · [Replay results](results.json) · [Archived solver](../../../nov19/alpha280/macro.cpp)

An independent family of 92 repair jobs removed successive neighborhoods or trapezoidal strips from the same six translated positions. All reached exhaustion after 243,801 enumerator states across the jobs. These 92 selected pin sets do not cover every possible large alteration. The bound of 13 uses the exhaustive edit-mask argument above.

## Reproduction

From this directory, use a C++20 compiler with GMP and Python 3.

~~~sh
python3 crop.py > crop-replay.json
python3 editsets.py /tmp/edits280 > editsets-replay.json
g++ -O3 -std=c++20 small_edits.cpp -lgmpxx -lgmp -o /tmp/small-edits280
for j in 0 1 2 3 4 5; do /tmp/small-edits280 /tmp/edits280/$j.pins /tmp/edits280/$j.edits; done
python3 jobs.py /tmp/pins280
python3 build_capture.py /tmp/capture280.cpp
g++ -O3 -std=c++20 /tmp/capture280.cpp -lgmpxx -lgmp -o /tmp/capture280
AUDIT280_CAPTURE=/tmp/packing177.txt /tmp/capture280 /tmp/pins280/r0-edge4.txt 60 1000000 /tmp/unused280
python3 packing.py --source /tmp/packing177.txt
~~~

The first two programs expect the preserved exact input files. Running `python3 packing.py` alone verifies the shipped 277-cell artifact and its residual hexagon.
