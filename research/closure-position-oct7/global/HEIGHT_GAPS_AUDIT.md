# Independent internal review of the empty-height theorem

7 October 2026. This is a separate derivation inside this research session,
not an external mathematical referee report.

Reviewed: `../heights/HEIGHT_GAPS.md`.

**Outcome: the stated square-divisibility and contiguous-support conclusions
follow from the repository's whole-edge cut and height-population lemmas.**
They do not exclude every 154 tiling.

1. At a cut k>=1, the I120 exterior boundary has no part strictly above
   k. Its higher-height tile union therefore has a closed boundary equal
   to the whole-edge cut chain, with no missing exterior correction.
2. The cut chain in the 120-degree case selects exactly two possible
   kinds of c-edge: short height k / long height k+1, with negative sign,
   and short height k+1 / long height k, with positive sign. Absence of
   short height k removes the first kind. Every remaining whole step
   belongs to c*z^k*Z[rho]. This conclusion does not assume absence of
   intermediate vertices, convexity of the high-tile union, or disjoint
   cycles in the chain decomposition.
3. A balanced sum of these actual segments decomposes into closed walks
   using their actual endpoints. Translating each walk does not change its
   signed area. The shoelace sum is consequently divisible by c^2 in units
   sqrt(3)/4. Since tile area is ab in those units and gcd(ab,c^2)=1, the
   number of tiles in the whole higher tail is divisible by c^2.
4. Reflection of an I120 target reverses all heights, proving the negative
   tail assertion. If c does not divide N, the population theorem forces
   level zero. If also N<c^2, an empty nonzero level cannot have a nonempty
   tail beyond it. Hence the occupied levels are consecutive.
5. For 154, each nonzero level contributes at least 13 tiles and level zero
   at least 11, so width<=11. There are sum_{w=0}^{11}(w+1)=78 intervals
   containing zero. Removing the three intervals of width 0 or 1 leaves 75.
   Exactly five of those 75 are reflection-fixed, namely [-j,j], 1<=j<=5;
   Burnside's elementary pairing count gives (75+5)/2=40 reflection orbits.
6. The partial-placement budget rounds each occupied/required nonzero
   population up to a positive multiple of 13 and level zero up to 11 mod 13.
   Thus its formula is a valid lower bound for every completion.

The precise limit is also correct: if the missing level is filled, selected
steps can have two adjacent heights. The generated cut lattice then has
area index c rather than c^2. This proof gives no license to keep square
rather than linear divisibility at such a cut.
