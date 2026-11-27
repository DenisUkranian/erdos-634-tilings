# Slant-sector area modulo a mesh cell from one physical bank

For either target let m count all tiles on the slant side of either native cut. Fix the standard physical frame and rotate and rescale so that a whole long side at the middle height is a unit triangular mesh step. The complete slant chord has integral axial displacement in these units. Direct the middle-owned bank with the sign it has in the CCW boundary of the selected tiles. Opposite half-turn mates may be removed. For an endpoint p write p=P+t, with P its coordinatewise floor. For q=Q+s set

    f(p,q) = det(P+Q,s-t) + det(t,s).

Then the following congruence uses only the positioned whole edges of the middle-owned bank:

    ab m / c² ≡ sum f(p,q)  (mod 1).

It also holds on any exterior-free positioned cut using either bank as the measured bank, with mesh axes chosen for the opposite bank. It covers arbitrary finite contact subdivisions and holes. This is a necessary condition on the area and positions in the same physical tiling.

Indeed the complete [oriented cut chain](../joint-cell-tree/TREE.md) has determinant sum ab m / c² in the rescaled chart. Its endpoint divergence is zero. Adding det(q,s)−det(p,t) to the contribution det(p,q) at each edge therefore leaves the sum unchanged, even when the chord or another long side has subdivisions. Expansion gives det(P,Q)+f(p,q). For any integral displacement, s=t and f vanishes. All edges of the other bank and the native slant chord have integral displacements. The formula works with any single choice of origin throughout a cut. No charge convention changes the physical orientation.

## Two unmatched middle owners

If the middle bank has exactly two unmatched owners, their oriented steps must be opposite. In their own mesh the sum has norm at most two. Integrality in the opposite mesh implies that the norm squared of any nonzero sum is divisible by c, by the index-c congruence in the [native displacement proof](CANONICAL_SEAM.md). Here c exceeds four. Write the two directed edges as p to p+v and q+v to q. Endpoint balance modulo the opposite mesh implies that L=q−p is an integral mesh vector. Indeed each edge connects two distinct residue classes and the two arrows must close. L is nonzero because coincident opposite whole edges with this fixed hand would be half-turn mates.

There is a second derivation which makes the area restriction explicit. Subtract from the cut chain the oriented parallelogram through p,p+v,q+v,q. Every remaining edge now has integral displacement. The determinant sum of that remainder is an integer by translating each closed walk to its start. Hence

    ab m / c² ≡ 2 det(v,L)  (mod 1).

The signed middle bank is zero. Its slant side has total signed population −c in path signs by the [native cut equations](ROOTED.md), so m is odd. All its short populations are divisible by c. Writing M=m/c gives ab M ≡ 2 det(cv,L) modulo c. Since ab is invertible modulo c, the two positions thus determine M modulo 2c by parity, or **m modulo 2c²**. At N<3c² this leaves at most two populations. This conclusion concerns zero signed current with two physically unmatched owners, outside the earlier cancellation case.

If m=c², these two owners must be separated by at least c√c in physical length, comparing p to q. Indeed det(cv,L)=0 modulo c. After a rotation and possibly conjugation, cv has axial coordinates (a,b). It is nonzero modulo the prime c and its norm squared is c². Therefore L is a scalar multiple of cv modulo c and its integral squared norm is divisible by c. Noncoincidence gives the claimed separation. The argument applies to either native gate individually. The two resulting population residues, when both are available, can be subtracted to constrain the number of tiles at the middle lift together with its nonnative branches.

Run `python3 area_residue.py | diff - AREA_RESIDUE.json`. The [replay](AREA_RESIDUE.json) measures the oriented long sides in the two complete 143 controls. On the axial cut, the same count of 14 unmatched middle owners gives residues 1/7 and 6/7, agreeing with the respective 105 and 91 slant-side tiles. The separate two-owner area calculation gives 7/43 on the [physical 86-tile local polygon](../terminal-contact/TERMINAL.md), both by the parallelogram and by the sum of endpoint residues. That polygon is a partial control. The original 3431 and 5063 questions remain open.
