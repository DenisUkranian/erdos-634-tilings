# Two exact seeds close the scale-four cap gap for (6,5,9)

Denis Paliy, research with ChatGPT assistance, 8 October 2026.

This note proves positive results for two fixed target families. It does
not classify all counts in Erdős problem 634, and makes no claim of
priority over constructions outside the sources inspected in this project.

## 1. Statement

Let T be the triangle with sides (6,5,9). For every integer m >= 3:

* the triangle with sides (27m,28m,15m) has a tiling by 14m² copies of T;
* the isosceles triangle with sides (27m,27m,46m) has a tiling by 23m²
  copies of T.

The new finite construction is the scale-four W triangle: **224 tiles in
the target (108,112,60)**. The existing beta transfer supplies **368 tiles
in the target (108,108,184)**. The already proved scale-increment cap then
gives the stated infinite families.

The novelty here is the fixed tile and target shape. In particular, the
integer count 368 was already realizable by Beeson's triquadratic seed
with parameters (u,v)=(3,4): tile (12,7,16), scale four, target
(256,276,112). Thus the beta construction does not establish a previously
unknown admissible count. The global positive statements for the
23-square-class tail also already follow by combining the prior cap with
that other 368 construction. The present result supplies every m>=3
using the single fixed tile (6,5,9) in its beta shape.

The old sufficient construction set for this tile was

    3 + <2,3> = {3,5,6,7,...}.

Since scale four is now constructed, this set is strictly smaller than the
actual fixed-tile scale spectrum. Thus its membership condition cannot be
turned into a necessary condition for arbitrary tilings. The scale-two
W target, with count 56, is not decided by this note.

## 2. The exact finite witness

Represent physical points by (x,y sqrt(2)); their squared distance is
dx²+2dy². The W target at scale m has vertices

    O=(0,0), A=(28m,0), C=(23m,10m).

Its side lengths are 28m, 15m and 27m. Its determinant area is 140m²,
whereas each primitive tile has determinant area 10; the area ratio is
14m². Here “determinant area” means ordinary coordinate area before the
common metric factor sqrt(2) is restored.

`W224_m3_p1.certificate.json` is the complete witness at m=4. It lists
224 positively oriented triangles, with all coordinates given as integers
over the common denominator 81. (The denominator can be reduced to 9;
the unreduced format is retained to match the search export.) This is a
unit-coordinate certificate, not a proposed arrangement of macroregions.

The independent script `verify_geometry.py` reads only this certificate;
it imports neither the search code nor a solver. It checks with integer
arithmetic:

1. every tile has positive orientation and squared side lengths
   25,36,81 after dividing by the denominator squared;
2. every tile vertex is inside all three target half-planes;
3. the sum of tile areas equals the target area;
4. every one of the 224*223/2 = **24,976** pairs has disjoint interiors.

For the last check, two convex triangles have disjoint interiors exactly
when a line supporting an edge of one of them weakly separates their
interiors; the script tests all six candidate lines by determinant signs.
Boundary contacts, including T-junctions, are permitted.

These four conditions prove that the certificate is a tiling. Indeed,
the contained tiles have disjoint interiors and full target area. A
missing interior point would have a relatively open neighbourhood missing
from their finite closed union, contradicting area equality; the closure
then also covers the target boundary.

The separate root-level checker `../verify_w_boundary.py` independently
verifies the same certificate by exact cancellation of boundary currents
on every positioned supporting line. It obtains PASS, without using the
pairwise separating-axis implementation. These are independent internal
checks, not an assertion of external mathematical review.

## 3. The beta seed is a disjoint geometric extension

Put D=(46m,0). Since 0 < 28m < 46m, the triangle O,D,C is the disjoint
union of O,A,C and A,D,C. The first is the W target. The second is an
ordinary tile triangle enlarged by the integer factor 3m:

    |AD|=18m=(3m)*6,
    |AC|=15m=(3m)*5,
    |DC|=27m=(3m)*9.

Hence the standard triangular grid adds (3m)² tiles, giving
14m²+9m²=23m². Its two long exterior sides have length 27m and its base
has length 46m, as claimed.

`beta_lift.py` reproduces this extension. For m=4 it writes
`B368_scale4.certificate.json`: the 224 W tiles plus 144 ordinary grid
tiles. The complete unit-coordinate geometry checker returns PASS after
checking all **67,528** pairs. The independent positioned-boundary checker
also returns PASS.

## 4. Every scale at least three

The existing [six-block cap theorem](../../w-beta-caps/PROOF.md), Sections
3–6, uses primitive parameters 0<u<v and proves that every existing W
or beta tiling at integer scale T >= v-u extends to scale T+u. Its collar
lies entirely outside the inner target and therefore applies to an
arbitrary tiling of that inner target, including the present seed.

For (u,v)=(2,3), the tile is (uv,v²-u²,v²)=(6,5,9); the increment is
u=2 and the cutoff is v-u=1. The existing triquadratic construction of
Michael Beeson supplies W at scale v=3 (126 tiles); its beta extension
supplies scale three in the beta family (207 tiles). These seeds and the
cap theorem are prior inputs, not new claims in this note. Their exact
macrocoordinates and the seed attribution appear in the cited proof.

Start with scale three and repeatedly add the cap to obtain every odd
scale at least three. Start with the new scale-four seed and do the same
to obtain every even scale at least four. Every cap application starts at
a scale >=1. This proves both universal quantifiers in Section 1 without
inferring an infinite statement from finite experiments.

## 5. Discovery, reproducibility and limits

The search `w56_position.py` enumerates contained tile positions in a
prescribed finite band of edge directions, imposes equality of the exact
positioned boundaries, and asks for Boolean tile selections. Its band
[-3,1] found the scale-four certificate after exact propagation and a
small residual CP-SAT solve. Completeness of that search is not needed
for this positive result: the two independent checks of its exported
coordinates establish existence directly.

The same band has no W56 solution, but larger bands are not excluded.
Its negative report is explicitly labelled restricted. In particular,
neither a direction bound for arbitrary W56 tilings nor a complete
classification of the W or beta scale spectrum is asserted here.

To check the positive witnesses using only Python's standard library,
run from this directory:

```sh
python verify_geometry.py W224_m3_p1.certificate.json
python beta_lift.py W224_m3_p1.certificate.json B368_scale4.certificate.json --scale 4
python verify_geometry.py B368_scale4.certificate.json
```

The known 126-tile seed was also recovered as a positive search control
and passed the same independent check (7,875 pairs). Its certificate is
`W126_control_m3_p1.certificate.json`; recovering it is not a new tiling
claim.
