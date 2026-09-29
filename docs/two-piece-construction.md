# A complete construction for the other scalene Group 1 branch

29 September 2026. Internal research result; external review and priority have not been established. This settles one target family, not all of Erdős problem 634.

## 1. Exact branch classification

Let `0<u<v` be coprime integers and put

    a=uv, b=v²−u², c=v²,
    Q=b+c=2v²−u², P=b+2c=3v²−u².

The tile has angles `(alpha,beta,gamma)` opposite `(a,b,c)`, with

    3alpha+2beta=pi, gamma=2alpha+beta.

**Theorem.** A triangle with angles `(2alpha,alpha,2beta)` is tiled by congruent copies of this tile precisely at the counts

    N=k² Q P,  k=1,2,3,... .

Here the triangle and tile are allowed an arbitrary common scaling. With tile sides fixed at `(a,b,c)`, the target at scale `k` has sides

    k cQ, k c², k bP

opposite `(2alpha,alpha,2beta)`, respectively.

The sufficiency holds for every coprime pair `u<v`. In particular no inequality `c<2b` is required.

### Necessity

The target shape has side proportions `(c²,cQ,bP)`, as the explicit construction below also proves geometrically. This integer triple is primitive:

    gcd(c²,cQ)=c,  gcd(c,bP)=1,

because `gcd(u,v)=1` implies `gcd(c,b)=gcd(c,Q)=gcd(c,P)=1`.

Write the target sides as `k(c²,cQ,bP)` for a positive real scale `k`. Each side of a triangle tiled by the primitive integer-sided tile is a complete chain of tile edges and hence has integer length. Integer Bezout coefficients for this primitive triple therefore show that `k` itself is an integer. The unit-scale target has `QP` tile areas, so the area equation forces `N=k²QP`.

This argument, independently identified during the composite-structure audit, avoids any coloring equation. For an initially unspecified tile, Beeson's rationality theorem remains the source reduction to the primitive parameters above; for the specified tile family, necessity is elementary.

For comparison, the older valuation route starts from the second tiling equation `N R²=M² QP`, where `R=(v−u)(2v+u)`. No odd prime dividing R divides QP, and `v_2(QP)<=1`, so valuation comparison gives `R|M`. It yields the same integer scale.

### Sufficiency: the two-piece construction

Start with Beeson's triquadratic W-tiling at

    M=a=uv, K=c=v², N_W=cQ.

The hypotheses of his Theorem 11 hold:

    M²+N_W=a²+cQ=2c²=2K²,
    M²<N_W,  K|M².

The tile supplied by that theorem is exactly

    (M,N_W/K−K,K)=(a,b,c).

Its target W-triangle has sides

    (aQ,bc,c²)

and angles `(2alpha,beta,alpha+beta)`. Along its side `aQ`, the endpoint angles are `beta` and `alpha+beta`.

Now attach, on the other side of this edge, an ordinary quadratic tiling of a `Q`-fold similar copy of the tile. Its sides are

    aQ,bQ,cQ,

and it contains `Q²` congruent tiles. Match the common side `aQ` so that its `beta` corner meets the W-triangle's `beta` corner, while its `gamma` corner meets the W-triangle's `alpha+beta` corner.

The latter endpoint disappears from the outer boundary because

    gamma+(alpha+beta)=3alpha+2beta=pi.

At the former endpoint the outer angle is `2beta`. The other two vertices have angles `2alpha` and `alpha`. Thus the union is a single triangle, with sides

    c², cQ, bc+bQ=bP.

Its tile count is exactly

    cQ+Q²=Q(c+Q)=QP.

Quadratic subdivision gives every multiplier `k²`. This proves the theorem.

This is the complete construction. The explicit coordinates below independently verify the W input and the gluing, including the small case 322 that v4 lists as unresolved.

## 2. The 322 construction

Take `(u,v)=(2,3)`. Then

    (a,b,c)=(6,5,9), Q=14, P=23.

Beeson's existing 126-tiling has target sides `(84,45,81)`. Attach a 14-fold similar tile, with sides `(84,70,126)`, subdivided into `14²=196` tiles, along the side of length 84. The edges of lengths 45 and 70 join into one straight edge. The resulting triangle has sides

    81,115,126

and contains

    126+196=322

copies of the `(6,5,9)` tile.

This is a construction of a global admissible count `N=322`; it is not merely an arithmetic necessary condition.

For a concrete coordinate description, coordinates `(x,y)` in this paragraph mean the physical point `(x,y sqrt(2))`. Put

    O=(0,0), A=(25,0), C=(-10,20), D=(-10,-20),
    E=(-28,-16), B=(-38,-36), H=(-580/9,460/9).

The W-triangle is `ABC`. Its pieces are the triangles `OAC`, `OAD`, `OCE`, with quadratic scales `5,5,6`, and the parallelogram `ODBE`. The parallelogram is a `5` by `4` grid with edge steps `(-2,-4)` and `(-7,-4)`, split along the difference diagonal into congruent triangles. It contains 40 tiles. Hence W contains `25+25+36+40=126` tiles.

The triangle `BCH` is the 14-fold copy, contributing 196 tiles. The final target is `ABH`.

## 3. Explicit uniform coordinates

These coordinates also give a self-contained construction without having to reconstruct a printed figure.

Put `D0=4v²−u²`, and let coordinate pairs `(x,y)` denote physical points `(x,y sqrt(D0))`. Set

    O=(0,0),
    A=(b²,0),
    C=(-u²b/2, ub/2),
    D=(-u²b/2,-ub/2),
    E=(-u²Q/2,-u³/2),
    B=D+E,
    H=C+(Q/c)(C−A).

The following are exact identities:

* `OAC` and `OAD` are `b`-fold similar copies of the tile.
* `OCE` is an `a`-fold similar copy of the tile.
* `E=(u²/b)(D−A)`, so `A,D,B` are collinear with `D` between `A,B`.
* `D=(b/c)(E−C)`, so `C,E,B` are collinear with `E` between `C,B`.
* The parallelogram `ODBE` has elementary step vectors `d=D/b` and `e=E/u²`; they satisfy `|d|=a`, `|e|=c`, and `|d−e|=b`.

Consequently its `b*u²` elementary parallelograms each split into two copies of the tile. Around O, the three large triangles each occupy angle gamma and the parallelogram occupies the remaining angle beta, because `3gamma+beta=2pi`. They have disjoint interiors and their union is the W-triangle `ABC`.

The W side lengths are

    AC=bc, AB=c², BC=aQ.

Since `H` lies beyond C on line AC and `CH=bQ`, the triangle `BCH` has sides `(aQ,bQ,cQ)`. Its interior is opposite to A across BC. The union is exactly the target `ABH`, with side lengths `(c²,cQ,bP)`.

The piece counts are

    Q² + 2b² + a² + 2bu² = Q²+cQ=QP.

There are four quadratic triangular blocks and one parallelogram block, all with positive integer subdivision parameters. This remains valid when `c>=2b`.

## 4. Exact certificate and independent-review status

`scripts/generate_tiling.py` generates every individual tile using rational coordinates. It then rescales all coordinates by one common denominator and verifies using integer arithmetic:

1. every tile has the required three squared side lengths;
2. every tile is inside the target;
3. the sum of exact oriented tile areas equals the target area;
4. every pair of tiles has disjoint interiors, using exact separating-axis checks.

The generated certificates are:

| Parameters | Count | Certificate | Checks |
|---|---:|---|---|
| `(1,2)` | 77 | `data/tiling-77.json` | All pass |
| `(2,3)` | 322 | `data/tiling-322.json` | All pass |
| `(3,4)` | 897 | `data/tiling-897.json` | All pass; includes `c>2b` |

The general construction is proved symbolically above. Finite checks validate the coordinate generator; they are not a substitute for the uniform proof. Separate internal reviews reconstructed the coordinate formulas, checked the uniform gluing, and supplied the simpler Bézout necessity proof. A separately implemented exact checker verifies the complete 322 certificate; see [its audit](audits/construction-322.md). No formal proof assistant or external referee has reviewed the result.

## 5. A local obstruction from the unsuccessful first approach

Before the two-piece construction was found, we tried to shrink Beeson's earlier four-component layout. That would require, at `(u,v)=(2,3)`, a parallelogram with sides 9 and 30 and included angle gamma to be tiled by 18 copies of `(6,5,9)`. It cannot be done. The following uniform lemma explains why, but this obstruction does not obstruct the successful construction above.

**One-c-edge cap lemma.** Assume `u>1`. A convex polygon with one side of length `c`, whose adjacent interior angles are `gamma` and `theta=alpha+beta`, cannot be tiled by copies of `(a,b,c)`.

First, the only whole-edge decomposition of each of lengths `a` and `b` is the corresponding single edge. For length b, reduction modulo v forces the b-edge count to be 1 modulo v, and its size forces that count to equal 1. For length a, reduction modulo v makes the b-edge count a multiple of v; since `v b>a`, it must vanish, and `a<c` leaves a single a-edge. Similarly a decomposition of c has no b-edge because `v b>c`; it is either a single c-edge or consists of a-edges only. The latter requires `u|v`, impossible when `u>1`.

Let the polygon side be AB, with angle gamma at A and theta at B. The boundary side is therefore one tile's c-edge; call its third vertex R. Its angle at R is gamma.

There are two orientations.

* If the tile has alpha at A and beta at B, the angle still to fill at B is alpha. The tile next to BR therefore has a b- or c-edge along BR, whose length is a. The opposite whole-edge chain on BR cannot end at R, by the single-a property. Hence R is inside a genuine edge of another tile, whose interior lies opposite the original tile across BR. The extension of AR beyond R enters that crossing tile. Thus the whole opposite chain on AR has endpoints A and R and total length b. It is a single b-edge. Its endpoint angle at A must be alpha, because the available angle theta is smaller than gamma. Its angle at R is gamma. At R there would then be two gamma sectors plus the crossing tile's straight sector pi, exceeding `2pi`.
* If the tile has beta at A and alpha at B, the angle still to fill at B is beta. The next tile starts the opposite chain on BR with an a- or c-edge, while BR has length b. The single-b property again gives a crossing tile at R. The opposite chain on AR is now a single a-edge. Its angle at A is beta or gamma. But the available angle is `gamma−beta=2alpha`, which can only be filled by two alpha angles. This is impossible.

The angle assertions follow from irrationality of `alpha/pi`: since `2cos(alpha)=2−u²/v²` is rational strictly between 1 and 2, rationality of `alpha/pi` would make this nonintegral rational number an algebraic integer. The only rational relation among these angles is consequently generated by `3alpha+2beta=pi`.

The proof uses maximal actual edge chains and a genuine crossing edge; it does not assume an edge-to-edge tiling or a global lattice. In particular it permits T-junctions.

This lemma received a separate internal check. An exploratory finite search suggested the obstruction; the uniform proof above supersedes those computational observations.

## 6. Scope

This theorem completely settles the `(2alpha,alpha,2beta)` branch for rational `3alpha+2beta=pi` tiles. It produces an explicit new-to-this-investigation 322 construction and every admissible count in this branch. It does not classify the other target families, nor all integers in Erdős 634. Those tasks must remain separate in any letter or announcement.
