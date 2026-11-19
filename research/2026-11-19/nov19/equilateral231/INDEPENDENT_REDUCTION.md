# Independent arithmetic and height check for 231

The reduction uses the primitive-triangle classification and count forms collected in Denis Paliy, [uniform reduction §§3–5](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md). This is an internal mathematical check. Michael Beeson had already identified this equilateral target explicitly in [arXiv:1812.07014v4, §7, Table 2](https://arxiv.org/html/1812.07014v4#S7.T2), listing it among the cases surviving his necessary conditions. None of the sources examined assigns that entry a completed tiling or an impossibility proof.

## Unique shape

Since \(231=3\cdot7\cdot11\) is squarefree, every multiplier \(t\) in a form \(dt^2\) equals one. The classical rows fail: 231 is neither a square nor two or six times a square, 77 is not square, and 231 is 3 modulo 4 so it cannot be a sum of two squares. The double-angle and theta cases require \(t\ge2\). Since \(231\equiv7\pmod8\), the residue tables of §5 leave only W, beta, F2 and the plus-norm equilateral branch.

* W would give \(2v^2-u^2=231\), so \(u^2\equiv2v^2\pmod3\), impossible for coprime \(u,v\).
* Beta would give \(3v^2-u^2=231\), so \(u^2\equiv3v^2\pmod7\), again impossible for coprime \(u,v\).
* In F2, divisibility of \((a+2b)(2a+b)\) by 3 forces both factors divisible by 3, contradicting \(9\nmid231\).
* In the remaining row \(ab=231\). The unordered factor pairs \((1,231),(3,77),(7,33),(11,21)\) give \(a^2+ab+b^2=53593,6169,1369,793\). The only square is \(37^2\) from \((7,33)\).

Therefore 231 is a possible tile count exactly if an equilateral triangle of side 231 can be tiled by copies of \((33,7,37)\).

## Height populations

Use \(\rho=e^{i\pi/3}\), \(z=(33+7\rho)/37\), and the height and sign conventions of [the 329 calculation](../iso329/README.md). The three counterclockwise exterior directions are \(1,\rho^2,\rho^4\), all at height 0 and all with positive ordinary current. For each short height \(h\), let \(n_h\) be its total population and \(g_h\) its signed population (with the short edges of a positive tile contributing \(+33,-7\)). Summing the ordinary and height-alternating currents gives
\[
 -11\sum g_h=693,\qquad 63\sum(-1)^h g_h=693 .
\]
Consequently the total signed counts on the odd and even heights are \(-37\) and \(-26\), respectively.

[Paliy's height-population theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/i120-global-oct7/HEIGHT_LEVELS.md) explicitly includes equilateral targets, so \(37\mid n_h\) off zero and \(n_0\equiv9\pmod{37}\). Modulo 37 the signed edge balance gives \(37\mid g_h\) off zero and \(26g_0\equiv693\pmod{37}\), or \(g_0\equiv11\). Hence \(n_0\ne9\). Every populated nonzero level has at least 74 tiles by the 37-tile contradiction in the 329 calculation; here there are no exterior sides at nonzero height. One odd level has odd signed population, hence odd total population, at least 111.

There are no gaps between populated levels and zero. At a vacant intermediate height \(k\), the nonempty union of tiles beyond \(k\) has its entire boundary in full 37-edges of that height; no target side is beyond the cut. Indeed any interface with the remaining tiles must have height \(k\), at which only whole 37-edges occur and the two adjacent banks of each maximal collinear segment have the same length-37 step. The boundary walks have steps in \(37 z^k\mathbb Z[\rho]\), hence Euclidean area expressed in units \(\sqrt3/4\) is a multiple of \(37^2\). Each tile has area 231 in the same units, coprime to \(37^2\). More than 231 tiles would be needed beyond the gap.

Four heights require at least \(9+111+74+74>231\). Thus all support is in a three-height band containing zero. Every shorter admissible interval is contained in such a band. Up to reflection these maximal test bands are \([-1,1]\) and \([0,2]\).

If exactly three heights occur, the populations must be 46 at zero, and 111 and 74 at the other two. Parity and \(g_0\equiv11\pmod{37}\) yield \(g_0=-26\). The 111-tile level has \(g=-37\) and the 74-tile level has \(g=0\). For the one-sided band this follows immediately by odd versus even height. In the centered band each extreme \(h=\pm1\) needs signed balancing long edges at \(h\) coming from height zero: at least \(26|g_h|/37\) of them. These neighbors come from disjoint subsets of the 46 height-zero tiles, giving \(26(|g_{-1}|+|g_1|)/37\le46\). With odd-height sum \(-37\), this forces the asserted signs. In particular the 46 tiles at zero split ten positive and 36 negative.
