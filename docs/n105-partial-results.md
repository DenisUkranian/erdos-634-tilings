# N = 105: an elementary branch exclusion and a precise invariant barrier

> **Historical stage — 29 September 2026.** Its limited claims remain as written. The later [global N=105 proof](n105-global.md) supersedes statements here that the count is unresolved. These old partial certificates are retained as regression evidence, not as the new proof.

29 September 2026. Internal research note; no claim of external review or priority.

This note gives two actual mathematical results, neither of which settles global N=105:

1. An equilateral triangle cannot be tiled by 105 congruent triangles whose irrational-angle tile has a 120-degree angle. This follows from six integer checks after a short, subdivision-compatible direction invariant argument. There is no bounded search over tile triples.
2. Every primitive rational 120-degree F1 candidate at its minimal arithmetic scale passes the full formal additive direction/edge-length boundary system. In particular, this entire class of position-independent additive invariants cannot exclude the unresolved candidate (8,7,13) on (105,56,91).

The two surviving 60-degree equilateral candidates are recovered by the same elementary method. No new geometric tiling or geometric nonexistence proof for either of them, or for the F1 target, was found in this round.

## 1. Direction characters, including T-junctions

Assume the tile has angles alpha, beta, gamma, with alpha/pi irrational and gamma equal to either pi/3 or 2pi/3. Rotate the target so one external side is horizontal. Every tile-edge direction belongs to the group

    theta = n alpha + j pi/3,  n in Z, j in Z/6Z.

To justify this without an edge-to-edge hypothesis, the adjacency graph of tiles sharing a segment of positive length is connected: a path through the interior of the target, avoiding the finitely many tile vertices, crosses only such adjacencies. Across a shared edge, the directions of the next tile differ by integer combinations of its angles. These angles are themselves integer combinations of alpha and pi/3. An external edge supplies the initial horizontal direction.

Irrationality makes n and j unique, with j read modulo 6. Define

    f(theta) = (-1)^j,
    g(theta) = (-1)^(j+n).

Both change sign under a reversal theta -> theta+pi. For any polygon whose boundary lies in these directions, define the f-flux as the sum of length(edge) times f(direction(edge)), traversing counterclockwise. Define the g-flux similarly.

These quantities are additive over a dissection. At a T-junction subdivide the longer edge at the other vertices: additivity in length and the reversal sign cancel every internal subsegment. Reflection reverses a traversal and negates both fluxes; arbitrary allowed rotations multiply a flux by a sign. Consequently, if a reference tile has f-flux X, every congruent tile has f-flux +X or -X. The boundary flux divided by X must therefore be an integer congruent to the number of tiles modulo 2. The same is true for g.

The rationality of tile side ratios is an input from the classification/rationality results, not proved here. After primitive normalization, a,b,c are positive integers, and each external side length S is integral because it is a union of complete boundary tile edges.

## 2. The 120-degree calculation

Let a,b,c be opposite alpha,beta,gamma=2pi/3. Then

    alpha+beta=pi/3,   c^2=a^2+ab+b^2.

Place the directed c-edge at direction 0 and traverse a reference tile counterclockwise. Its next a-edge is at direction 2pi/3+alpha; its final b-edge is at pi+alpha. Thus its f- and g-fluxes are respectively

    X = c+a-b,       Y = c+b-a.

They are positive, and

    XY = 3ab.

An equilateral target of side S has boundary directions 0, 2pi/3, 4pi/3. Both fluxes therefore equal 3S. Any N-tiling supplies positive integers

    s = 3S/X,       t = 3S/Y,
    s == t == N (mod 2),
    st = 3N,

where the last identity uses S^2=Nab, the area equation.

There is a further necessary square condition:

    (t-s)^2 + 16N = [2S(a+b)/(ab)]^2.

The quantity in brackets is rational. Since its square is an integer, it must itself be an integer. Hence

    (t-s)^2+16N = q^2,    q a positive integer.

This derivation proves that factor pairs of 3N provide an exhaustive finite necessary test, without any upper bound on a,b,c.

### Application to N=105

Interchange a,b if needed, so s<=t. The only factor pairs of 315 and their radicands are:

| s | t | (t-s)^2+1680 | Consecutive bounding squares |
|---:|---:|---:|---|
| 1 | 315 | 100276 | 316^2=99856 < 100276 < 317^2=100489 |
| 3 | 105 | 12084 | 109^2=11881 < 12084 < 110^2=12100 |
| 5 | 63 | 5044 | 71^2=5041 < 5044 < 72^2=5184 |
| 7 | 45 | 3124 | 55^2=3025 < 3124 < 56^2=3136 |
| 9 | 35 | 2356 | 48^2=2304 < 2356 < 49^2=2401 |
| 15 | 21 | 1716 | 41^2=1681 < 1716 < 42^2=1764 |

None is a square. This proves the stated 120-degree equilateral exclusion.

A previously reported area-only candidate is (a,b,c)=(21,320,331), S=840. It already fails the first flux condition:

    3S/(c+a-b) = 2520/32 = 315/4.

No geometric exhaustive search is needed for that instance.

### Source audit consequence

The examined Bonfioli main source, `paper/erdos-634.tex` in [the upstream repository](https://github.com/ElVec1o/erdos_634_proof), Theorem `thm:eq105`, attempts to exhaust the 120-degree branch by enumerating a<=b<4000 and then geometrically excluding (21,320,331). Its stated proof provides no bound implying b<4000. The finite invariant argument above removes that particular gap for the 120-degree branch. It does not validate the separate search certificates in the 60-degree branch, and does not prove global N=105 impossible.

The two fluxes and their equilateral product are already in the source corpus; priority is not claimed. The contribution of this check is a self-contained exact application that renders the unbounded tile-triple enumeration unnecessary.

## 3. The 60-degree branch gives exactly the two familiar candidates

Now gamma=pi/3 and beta=2pi/3-alpha, so

    c^2 = a^2-ab+b^2.

The canonical tile directions are 0, pi/3+alpha, pi+alpha. The two flux magnitudes are

    a+b-c,       a+b+c.

Set

    s=3S/(a+b+c),       t=3S/(a+b-c).

Both are positive integers of the parity of N, st=3N, and

    (t-s)^2-4N = [2S(a-b)/(ab)]^2.

Again the right side is the square of an integer. Also s^2<N for a nonequilateral tile: a+b+c>3 sqrt(ab), with equality only when a=b. Thus for N105 only s=1,3,5,7,9 can occur. The radicands are respectively

    98176, 9984, 2944, 1024=32^2, 256=16^2.

The last two give, after primitive normalization and interchange of a,b:

    (a,b,c;S)=(5,21,19;105), (7,15,13;105).

For reconstruction, if q^2=(t-s)^2-4N, then a:b=(s+t+q):(s+t-q).

This gives a complete necessary reduction of the irrational 60-degree branch, but it supplies no tiling and does not rule either candidate out geometrically. Both pass the additive flux tests.

## 4. A universal additive-invariant barrier for the F1 branch

Let c^2=a^2+ab+b^2 be a primitive positive integer 120-degree triple. The minimal F1 candidate has target sides

    b(a+b), ab, bc,

and target angles pi/3, alpha, pi/3+beta. The area ratio is

    N=b(a+b).

Use formal generators E_(n,j) for a unit of directed boundary length in direction n alpha+j pi/3, with the only relations

    E_(n,j+3) = -E_(n,j).

Unlike scalar fluxes, this records the entire signed length in every distinct direction independently. Every additive direction/length invariant is an evaluation of this formal object.

The boundaries of two congruent orientations of the tile are

    R_(n,j) = c E_(n,j) + a E_(n+1,j+2) - b E_(n+1,j),
    S_(n,j) = c E_(n,j) - a E_(n-1,j+1) - b E_(n-1,j).

R is a rotation of the reference orientation. S is the reflected orientation with the counterclockwise traversal restored, then rotated by pi; hence it is also an actual positive-area placement of the same tile. Negating R or S is achieved by rotating the corresponding placement by pi, not by using a negatively weighted tile.

Orient the F1 target so that its side b(a+b) is horizontal. Its formal boundary is

    F = b(a+b) E_(0,0) - ab E_(0,1) - bc E_(-1,0).

The following identity is exact:

    F = a R_(-1,1) + c S_(0,0).

Indeed,

    R_(-1,1)=c E_(-1,1)-a E_(0,0)-b E_(0,1),
    S_(0,0)=c E_(0,0)-a E_(-1,1)-b E_(-1,0),

so their indicated linear combination cancels E_(-1,1), and its horizontal coefficient is c^2-a^2=b(a+b).

The right side contains a+c positive tile placements. Moreover N-a-c is a nonnegative even integer. Evenness follows from

    c == a+b+ab (mod 2),

which is the norm identity modulo 2. Positivity follows from b>=2 and c<a+b; a positive integer 120-degree triple cannot have b=1 since a^2+a+1 lies strictly between a^2 and (a+1)^2. Finally add (N-a-c)/2 pairs of a tile and its 180-degree rotation. Each pair contributes zero formal boundary and contributes two tiles.

Thus a multiset of exactly N oriented congruent tiles has precisely the F1 target's entire formal direction/length boundary. This is not a geometric dissection: no positions, nonoverlap or coverage have been asserted. It proves that a contradiction based only on additive boundary direction/length data and tile count is unavailable for this entire family. The positions and local geometric compatibility have to enter.

### The concrete 105 instance

For (a,b,c)=(8,7,13), the identity is

    105 E_(0,0)-56 E_(0,1)-91 E_(-1,0)
       = 8 R_(-1,1)+13 S_(0,0).

There are 21 tiles on the right. Add 42 cancelling opposite-orientation pairs to obtain 105 tiles. All formal additive boundary conditions pass simultaneously.

This also explains why simply seeking a third signed direction character cannot settle this remaining F1 candidate. It might still be excluded by a positional invariant, a noncommutative boundary group, or a forcing argument, or it might admit a tiling. No conclusion in either direction follows from this formal identity.

## 5. Exact checks and the remaining scope

`scripts/check_n105_invariants.py` checks all six 120-degree factor pairs, reconstructs the two 60-degree primitive candidates, verifies the complete formal identity for (8,7,13), and checks its general formulas on all 36 ordered primitive triples with a,b<=100. All computations use integer arithmetic. The general proofs above do not depend on that finite sample.

Its exact output is reproduced in `verification/replay.json`. An exploratory bounded integer linear program independently found the 21-tile formal solution for orientation ranges -1..1, -2..2 and -3..3; this optimization is not used in any proof.

The full Erdős problem remains unclosed. The present work removes a complete 120-degree equilateral branch at105 and proves a limitation of the most natural additive-invariant route to its F1 instance. It does not turn a branch result into a global count classification.
