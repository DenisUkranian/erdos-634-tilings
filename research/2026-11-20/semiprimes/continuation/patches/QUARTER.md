# Size of one remaining pentagon

Take any odd primitive F2 triangle beyond the [unit staircase](../../staircase/SHARP_STAIRCASE.md). The pair of congruent pentagons in [the partial dissection](PENTAGONS.md) gives a sufficient test for tiling the whole unit triangle. Write n for the area of one pentagon in unit tiles and Q for the old [reflected-corner quadrilateral](../../corners/PROOF.md), of area 3ab in the same units.

**One pentagon always has strictly less than one quarter of the area of Q.** Together the two copies occupy less than half the area of Q. Filling either one by congruent tiles suffices, since the filling translates onto the second copy. This compares two sufficient constructions. An arbitrary solution can avoid both.

Indeed the two equal loads have bridge size t=(a−b)/2, overrun k=(c−3b)/2, and vertical advance s=(c−a)/2. The one-row extension of a notch adds 2(a−s)+1 tiles' worth of area. With c²=a²+ab+b² this says
$$
 n=t^2-k^2+2(a-s)+1
   =\frac{3b(2c-a-3b)}4+3a-c+1.
$$
Substitute (ga,gb,gc)=(u²−v²,v(2u+v),u²+uv+v²) and g=gcd(3,u−v). Direct expansion gives
$$
 g^2(3ab-4n)
   =8(3v^2-g)u^2 + 4guv + 3v^3(2u-v)+4g(4v^2-g).
$$
Every term is nonnegative and the last three are positive because u>v≥1 and 1≤g≤3. The inequality follows, including for the infinite thin family g=3, v=1 for which the first term vanishes.

The factor one quarter cannot be lowered uniformly over odd primitive residual shapes: take v=1, g=3, u congruent to 4 modulo 6 and let u tend to infinity. Here 3ab−4n=2u+1 and ab grows cubically. An infinity of prime products on this family is not assumed.

Uniformly on the remaining ordered parameter pairs, v=O(√u), a is comparable with u² and b=O(uv). Thus the uncovered part is O(N^(7/8)) on a board with N tiles' worth of area, as N is comparable with u⁴. The entire covering except for those two holes consists of actual congruent tiles.
