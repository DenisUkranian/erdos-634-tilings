# Why the seven-tile exclusion does not immediately strengthen to fourteen

8 October 2026. A bounded investigation for the remaining equilateral
(3,5,7) count135. No tiling or nonexistence proof for135 is claimed.

The preceding E60 argument excludes population7 at every nonzero short
height. A hoped-for strengthening would exclude14 and21 and give a
population floor28. The direct supporting-line method does not do so.
The obstruction is visible even with exact local geometry inside E45.

## A genuine fourteen-tile patch inside E45

Set rho=exp(i pi/3), z=(3+5 rho)/7, v=3z. For k=0,...,6 take the two
triangles

    (kv, kv+7, (k+1)v),
    (kv+7, (k+1)v+7, (k+1)v).

Since |v|=3 and |7-v|=5, these are14 congruent (3,5,7) triangles.
They tile exactly the parallelogram

    [0, 7, 16+15 rho, 9+15 rho].

Its vertices have nonnegative Eisenstein coordinates and x+y<=31<45,
so it is contained in the side45 equilateral target. All14 tiles have
short height1 and long height0. The only nonzero signed currents on
separate short supporting lines are +21 and -21. They are divisible
by7, as required by the affine-line argument.

Thus containment, exact pairwise nonoverlap, and all supporting-line
divisibility conditions cannot by themselves forbid population14.
This example is a specialization of the mixed-height-c-boundary
parallelogram already recorded in
`../../i120-global-oct7/HEIGHT_LEVELS.md`; the underlying construction
is not claimed as new here.

The complement of this patch has **not** been tiled. The patch is not
a counterexample to a theorem about completed equilateral tilings;
it identifies why stronger global completion information would be
needed to prove such a theorem.

## Exact inventory tests

The full14-tile residue enumeration finds13,362 unsigned orientation
inventories with all three short currents divisible by7. Allowing both
character signs, the affine-line gamma-intersection filter rejects408
and leaves12,954 inventories in1,176 rotation/reflection orbits. These
survivors are formal inventories, not12,954 geometric tilings.

A particularly simple population21 inventory also survives the same
method:

    A0=7, A3=7, B5=7.

For the signed edge kinds (3+,3-,5+,5-), its three direction totals are

    (7,7,0,0), (0,7,0,0), (0,0,7,14).

Every current is divisible by7. The maximum supporting-line products
for the three used orientations are56,49,8, respectively; each is at
least the multiplicity7. These bounds still hold if each individual
line bank is limited to length38. That is no larger than the floor of
any maximal chord length in an equilateral triangle of side45.

Consequently the previous affine-line and chord-cap necessary tests
do not establish either n_h!=14 or n_h!=21.

## Remaining arithmetic bounds

The existing population theorem gives n_0=135=2 mod7. Each outer side45
must contain a short edge, because45 is not divisible by7. One tile
cannot have short edges on two different exterior sides: those two
edges meet at120 degrees, whereas the target corner is60 degrees.
Therefore n_0>=3, hence n_0>=9. With n_h>=14 off zero, there are at most
ten occupied short heights.

An empty nonzero height isolates a positive multiple of49 tiles. The
earlier modulus45 proof excludes49, so a gap in a135-tile target would
isolate98 tiles. For such a tail, the same character proof gives
45|M, M even and |M|<=98. The choices M=+/-90 would force at least110
tiles by its L1 estimate. Therefore a possible98-tile tail must have
M=0. This restriction does not rule out the tail or prove contiguity
at135.

## Reproduction

    python research/final-closure-oct8/e135-structure/check_local_barriers.py
    python research/final-closure-oct8/e135-structure/probe_fourteen.py

The first program verifies the explicit local patch, all91 tile pairs,
line divisibilities and the population21 inventory. The second performs
the exhaustive finite population14 inventory probe. Neither program
claims an unrestricted geometric decision for135.
