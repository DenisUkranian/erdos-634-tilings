# A restriction on tile directions in the reflected-corner construction

Let the tile have primitive sides a>b>0, c²=a²+ab+b². Set p=a+2b, q=2a+b, n=a−b and u/v=(a+c)/b in lowest terms. The primitive F2 triangle has sides ap, bq, c². All axes below are unoriented. Copies may be reflected, and edges may meet partially.

**Theorem.** Suppose the reflected-corner quadrilateral Q defined below can be tiled so that each tile has at least two sides parallel to sides of Q. Then

                         2(a−2b)(a+b) ≤ 3vab.                         (1)

For **every odd mixed-residue semiprime beyond the unit staircase**, a tiling of Q must use at least **two distinct orientations**, each having at least two edge directions absent from the boundary of Q. Orientations are counted up to translation; a half-turn counts separately. In fact this holds for all primitive parameter pairs with a,b odd outside that staircase, without primality. The claim includes the entire unresolved range of the mixed semiprime reduction. Q is a sufficient construction for the original triangle; a general F2 tiling can bypass Q. No negative verdict on an unrestricted F2 triangle follows here.

## The four-direction model

Use coordinates x+y z with ρ=exp(iπ/3), z=(a+bρ)/c. Put T_o=conv{(0,0),(c,0),(0,a)}, T_i=conv{(0,0),(a,0),(0,c)} in these coordinates. Q is the closure of cT_o minus nT_i. Both coordinate axes and both negative slants are its four side directions. The [coordinate calculation](PLACEMENT.md) identifies Q with the complement of two c-fold standard triangles in F2 after a rigid motion. A direct area calculation gives c²−n²=3ab elementary tiles in Q. The slants of both unit triangles have Euclidean length b. Write plus for a translated copy of either of these triangles and minus for its half-turn.

Here are all placements of a tile using at least two of the four axes. In addition to the four axial halves T_o,−T_o,T_i,−T_i, there are eight types up to translation. They come in four half-turn pairs, each with exactly one new axis, distinct among the four pairs. To verify completeness, write the oriented edge directions of an (a,b,c) tile as z^hρ^j, z^hρ^(j+s), z^(h+s)ρ^(j+3), with s=±1, j mod 6; for s=−1 the order around the triangle is reversed in the labels. Tilings use this direction group by propagation across positive-length contacts; the positive-contact graph is connected by perturbing a path away from vertices. Alternatively a single matched axis already fixes a tile orientation. The codes are unique since 2cos(arg z)=q/c is rational strictly between 1 and 2 and hence is not the sum of a root of unity and its inverse. The four axes in (h,j mod 3) are (0,0),(0,1),(1,0),(1,2). An edge on one of these requires −1≤h≤2. Enumerating these four heights and twelve types per height gives the list in directions.py. On a fresh axis both banks of any maximal connected segment are made of whole edges of the same length, and neither bank can extend past the other. Starting at its endpoint forces complete edge matching. Its two incident tiles are half-turn mates. Thus every nonaxial tile belongs to an actual parallelogram pair. No assumption about contacts on the other axes enters.

Each of the four possible parallelograms has a short side parallel to x or y of length b and another side on one of the two slants. On the outer slant its length is c for a horizontal b and a for a vertical b. On the inner slant the lengths are reversed. These follow from the unit slant vectors (−c,a)/b and (−a,c)/b and the four types. Denote the numbers of the four parallelograms by K_{o,x},K_{o,y},K_{i,x},K_{i,y}, where the subscript x or y is the coordinate along their b-side. Let U count the outer minus halves and L the inner plus halves. Opposite edges on the slants of each parallelogram cancel in the total signed length. The c outer boundary units and n reversed inner boundary units give #outer plus=U+c and #inner minus=L+n. Consequently

                     U+L+sum K = B = (3ab−c−n)/2.                   (2)

## Two one-dimensional equations that remember the positions of edges

Choose t=x or t=y and one slant (outer or inner). Let d be the span in t of its unit triangular half and e the height in the other coordinate. Then {d,e}={a,c}. For the outer slant t=x gives d=c, t=y gives d=a. For the inner slant the assignments are reversed. Set W=de/b and project t to the circle R/WZ. The residue classes of integer t in this circle form a cycle of order de, because gcd(b,de)=1. Throughout this proof U or L without a subscript counts actual tiles in the plane. Projecting a subset and then forgetting other cosets only lowers such counts.

Let P and M count starts of plus and minus halves of the selected slant when projected as intervals [s,s+d]; a plus half has its height-e coordinate edge on the left, a minus half on the right. Counts may be regarded as finite atomic measures on the circle. Let T_j denote translation by j. For the outer slant set H=c, ε=+1; for the inner set H=n, ε=−1. Write D=ε sum_{l=0}^{H−1} δ_{ld}. The following two identities hold for the atoms:

    (1−T_d)(P−M−D) = (1−T_b)(1−T_R)K,        R=d²/b,              (3)
           P−T_d M ≡ εH δ_0  (mod d).                               (4)

Here K records starts of parallelograms on the *selected* slant whose b-edge is parallel to t. A common translation of the starts can be absorbed in K. Its mass is at most the number K_{slant,t}, and all its weights are positive. The sign in (3) matters. In the plane with horizontal coordinate t, call the slanted bank positive when the triangle lies below it, as for the plus half. For a parallelogram with its horizontal side b, the upper, positive slanted bank is the lower, negative bank shifted to the right by b. Its signed projected intervals thus contribute (T_b−1) times the unshifted interval on the left side of the balance; moving it to the right gives 1−T_b. This argument also applies after exchanging the coordinate names. For (3), take the signed projected boundary intervals in this slant direction, then their endpoint differences. A parallelogram with its b-side perpendicular to t in coordinate variables (t constant along that b-side) has coincident projected slant intervals. The species with b parallel to t has intervals of width R displaced by b. The other slant does not contribute. For (4), sum the signed lengths of edges parallel to the slicing lines at each value of t, counting left edges positively. Every triangle of the other slant contributes a multiple of d. Parallelograms with a coordinate edge on a slicing line have a pair of such edges separated by W, and therefore cancel on the circle. The other parallelograms have no edges along the slicing lines. The true boundary edge at zero has length H e with sign ε modulo d, the contribution from the other boundary triangle being a multiple of d. Divide by e, a unit modulo d. Both arguments work by subdividing edges at T-junctions. They do not require a lattice hypothesis on the actual tile positions.

## Folding the integer classes

On the integer cycle of order de, R is equivalent to κd where 0<κ<e and bκ≡d mod e. Indeed their difference is an integer multiple of W. Restrict (3) and (4) to the integer classes; all translations in them now preserve that set. Write an index as jb+id, i modulo e, choosing d consecutive values for j. This is a bijection. Use a j-row with the fewest atoms of K as the last row in this list; it contains k≤floor(K_{slant,t}/d) atoms. Sum rows at fixed i. The difference 1−T_b telescopes between successive rows, with a displacement by b indices i on wraparound. For example with j=1,…,d, the preceding row of j=1 has coordinate 0b+id=db+(i−b)d. Thus, writing T for one shift on the i-cycle, the right side of (3) folds to (1−T^b)(1−T^κ)J, with mass(J)=k. Any choice of last row yields this formula. Translate i so the source at 0 is indexed by 0; all source atoms ld belong to that same row.

Put I_h=1+T+…+T^(h−1). Write bars over the sums across rows. Cancelling 1−T in (3) leaves an additive constant, since a shift-invariant vector on a cycle is constant:

             P̄−M̄−D̄ = constant + (1−T^b) I_κ J.

The constant vanishes modulo d. Summing (4) gives sum(P̄−M̄)≡εH mod d, sum D̄=εH, the transport term sums to zero and gcd(e,d)=1. Define a baseline vector F on the i-cycle by its differences, with any additive constant:

    outer: (1−T)F = c δ_0 − sum_{j=0}^{c−1} δ_j,
    inner: (1−T)F = −n δ_0 + sum_{j=1}^{n} δ_j.

Substituting in (4) and cancelling one more 1−T modulo d gives the central estimate. The vector M̄ (outer) or P̄ (inner) is congruent, modulo d and a constant, to

                          F − I_b I_κ J.                            (5)

For the inner vector there is one additional cyclic shift of J, harmless for its nonnegative weights. In particular the perturbation is subtracted in *both* cases. Adding it to the nonnegative folded vector gives F up to a constant modulo d. The sum of entries of the nonnegative tile-count vector is at most U or L, respectively. Different projections of one slant charge the same minority of tiles; estimates for that minority must be averaged or maximized. The two slants charge disjoint tiles. This distinction permits mixed parallelograms of both axis directions.

## A uniform inequality

Write [w]_d for the representative in {0,…,d−1} at integer w, extended to [0,d) on real inputs. Let S=1+T^κ+…+T^((v−1)κ). Since bu=v(a+c), vκ≡u mod e. One has 0<u<a: from a=(u²−v²)/g with g=gcd(3,u−v) and u>(1+sqrt(3))v this follows for u≥4, and u=3 has v=1,g=1. Consequently S I_κ=I_{vκ} equals I_u plus a constant convolution kernel on the cycle. Apply S to (5), and add the nonnegative convolution I_b I_u J (translated by one position in the inner case). The result is S F plus a constant modulo d. Taking least residues coordinate-wise gives

            v H_min + k b u ≥ D = min_C sum_i [(S F)_i+C]_d .       (6)

Here H_min is U or L. Applying S to its nonnegative folded count vector counts at most v H_min tiles with multiplicity. The convolution added has total mass kbu. This proof also works when other cosets contain axial tiles or parallelograms. The fixed sign is used when taking least nonnegative residues.

Here are lower bounds on D. The periodic function f(x)=[x]_d satisfies ∫_0^d f=d²/2, 0≤f≤d, and f(x+t)≤f(x)+t for all t≥0. Along a forward increment t the integral is therefore at most t f(x)+t²/2. Traversing the cyclic list of levels in reverse order preserves the sum of f at the levels. All estimates hold after an arbitrary additive shift C.

* Outer, d=c,e=a. Traverse the i-cycle backwards. The increments of S F, modulo c, are v plus some extras, since each shifted block of c unit sources covers the a-cycle at least once. The total of the extras is v(c−a). Lift to a forward walk of length vc. Take each ordinary step of length v first and then its extras. The latter contribute at most v(c−a)c to the integral. Comparing to v periods gives D≥[a²−(c−a)²]/2−av/2.
* Outer, d=a,e=c. Traverse backwards again. Each ordinary forward step has size v. At v marked places the correction −c can be represented by the backward step −(c−a). Take this correction after the forward step, so the latter starts at a sampled level. The net lifted displacement is vc−v(c−a)=va. The backward steps have nonpositive oriented integral. Hence D≥a²/2−cv/2.
* Inner, either projection. Traverse forward. The positive unit-source increments of S F have local size between 0 and v and total nv because n<min(d,e). There are also v source terms −n, which we lift as forward increments d−n. Take the small steps first at each index. This makes v full periods. The large increments contribute at most v(d−n)d. The squares of the small steps sum to at most v²n. Thus D≥[n²−(d−n)²]/2−vn/2.

Since k≤K_{slant,t}/d and bu=v(a+c), (6) gives H_min+(a+c)K_{slant,t}/d ≥ D/v. Multiply the two inequalities for one slant by d/(a+c) and add. Their weights sum to one. The bound for U plus its two K's is at least (a²−b²)/(2v)−c/2 since 0<c−a<b. The bound for L plus its two K's is at least (n²−4b²)/(2v)−n/2 since both d−n<2b. Substituting in (2) gives 3vab≥a²+n²−5b²=2(a−2b)(a+b), proving (1). Before the estimates, the sharper exactly computable condition is

                 B ≥ sum_over_four_projections(d D)/[v(a+c)].        (7)

## Every mixed semiprime outside the staircase

In this sector a,b are odd. Their parameter formulas force u even and v odd. Set x=u/v and r=a/b=(x²−1)/(2x+1)>x/2−1/2, increasing with x. Inequality (1) becomes 2(r−1−2/r)≤3v, with strictly increasing left side. The source staircase threshold is 4v², except that it is 4v(v−1) for g=3 and v≡2 mod 3.

* Beyond the ordinary threshold with v≥5 one has r>2v−1/2≥3v/2+2, which violates (1). At v=3 the smallest possible even u above 36 is 38, where r=1435/237>6, already violating (1). At v=1 every even u≥8 works by r≥63/17; the omitted u=6 is checked below.
* In the exceptional residue class, v is 5 or at least 11. For v≥11 one has r>2v−5/2≥3v/2+2. At v=5 the conditions are u>80, u even and u≡2 mod 3. For u≥92, r≥8439/945>35/4, violating (1). The only smaller eligible u is 86. Its first factor is 3047=11·277, so it is already outside the prime-pair problem. For completeness (7) also excludes its auxiliary tiling.

For the remaining u=6,v=1, take (a,b,c)=(35,13,43), n=22. Then S is the identity, and the four exact D's are 623,623,517,517. Their weighted lower bound from (7) is 1140 versus B=650. At (u,v)=(86,5), the four values, in the order outer x, outer y, inner x, inner y, are 3099847, 3057116, 2874199 and 2827571. Their weighted lower bound is 30085293861/25370, strictly larger than B=1084833. `cycles.py` recomputes every entry from the cyclic differences and integer residues. The supplementary Python checks test the geometric endpoint signs, the row fold, smoothing and the size estimates separately. At the two principal prime-pair controls we obtain:

| N | tile | Q in elementary tiles | B from (2) | required by (7) |
|---:|---|---:|---:|---:|
| 3431 | (33,7,37) | 693 | 315 | 1041 |
| 5063 | (35,13,43) | 1365 | 650 | 1140 |

The bounds concern counts of pairs after accounting for the signed surpluses of c outer and n inner halves fixed by the boundary lengths; they are not direct counts of triangles in the full board.

## A single exceptional orientation is also impossible

Call an orientation exceptional if at most one of its axes belongs to the four boundary axes. If exactly one exceptional orientation occurs, it cannot introduce an axis outside the eight axes used by the twelve earlier types: on such an axis all parallel edges would come from this one orientation, with the same directed sign, and the total signed boundary length cannot cancel. Among tiles with all three axes in the eight-axis set, the only exceptional possibilities are (0,1,+), (0,4,+), (1,2,−), (1,5,−), as follows from the same short enumeration in directions.py. The first two are half-turns of one another and have their c-edge on (1,1); the latter two have their c-edge on (0,2). Of the twelve ordinary types, only a-edges use either respective axis. Neither is a boundary direction of Q.

The real Euclidean vertical extent of Q in the embedding x+y z is at most ac sin(arg z)=√3 ab/2. The axes (0,2) and (1,1) make angles 120° and 60°+arg z with the horizontal, both having sine at least √3/2 since 0<arg z<30°. Every chord on either axis has length at most ab. Take a maximal connected seam interval on the c-axis of a present exceptional tile, with its c-edge in the interval. Both banks consist of whole edges up to the ends of the interval; partial matches within the interval are allowed. Since only one exceptional orientation is present, its c-edges all have the same sign. If k>0 of them occur on one bank, signed balance reads kc=ha for some integer h. Coprimality forces a to divide k. This interval would have length at least ac>ab, a contradiction. Thus whenever the twelve-orientation model is excluded at least two distinct exceptional orientations are necessary, with no restriction on the other tiles of Q.

## Consequences and open geometry

Every mixed prime candidate which fails the staircase is covered by the obstruction to this twelve-orientation construction. The union of two positive methods — the unit staircase and any reflected-corner filling using at least two boundary axes on every tile — gives exactly the same semiprimes as the staircase. No assumption on T-junctions or tile locations was imposed within the orientation condition. The first seven residuals through 10⁶ all have v=1. Each can still be realized in principle by a different placement of corner pieces, by a tiling of Q with a tile having at least two new directions, or by another unrestricted F2 tiling. This record adds no yes/no verdict on an unclassified semiprime. BOUNDARY.md separately determines exactly when a particular scalar side-length obstruction at the smallest F2 corner persists.
