# Impossibility of a dissection into 231 congruent triangles

**Claim.** Under the shape classification and scale restrictions cited below, no nondegenerate triangle admits a dissection into 231 congruent triangles. Reflections and T-junctions are allowed.

**Step 1.** An equilateral target of side 231 and tile (7,33,37) already appear in Table 2 of Beeson among the cases his conditions leave open. For an arbitrary triangular target, squarefreeness and the residues of 231 modulo 3, 7 and 8 leave this one geometric case. INDEPENDENT_REDUCTION.md derives this reduction and checks both norm forms separately. [Beeson, §7, Table 2](https://arxiv.org/html/1812.07014v4#S7.T2) · [Paliy, classification inputs and residue tables](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md).

**Step 2.** The sides of lengths 7 and 33 meet at 120°. Their directions have an integer index h modulo rotations through 60°. Paliy’s theorem gives divisibility by 37 of the tile count at each nonzero index. Counting along individual lines also excludes exactly 37 tiles at one index. Two signed identities force at least 111 tiles at some odd index and at least 74 at every other occupied nonzero index. A missing intermediate index would isolate a component with tile count divisible by 37², which exceeds 231. Up to reflection, it suffices to test the strips [0,2] and [−1,1]. These also contain all shorter possibilities. [Index theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/i120-global-oct7/HEIGHT_LEVELS.md) · [Line-count proof of the lower bound 74](../iso329/README.md) · [Specialization to 231](INDEPENDENT_REDUCTION.md).

**Step 3.** Fix a point and an unoriented line through it. Orient each tile boundary counterclockwise and count each edge with a positive contribution at its start and a negative one at its end. Along the line the signed endpoint count must equal the corresponding outer-boundary count. This is the derivative of the one-dimensional edge-coverage identity and includes T-junctions. If only one sign is available, no opposite sign is present and the point is not a corresponding outer endpoint, the placement may be eliminated. A missing required sign at a target corner rules out a tiling.

The enumeration includes both reflected orientations and all translations allowed by Paliy’s vertex-lattice lemma. All coordinates and half-plane tests use integers. A second implementation uses bit masks and a different traversal order. These are two internal replays.

| Allowed indices | Single-tile placements inside target | Pass finding an unsupported outer corner (intervals) | Corresponding pass (bit masks) |
|---|---:|---:|---:|
| [0,2] | 884 470 557 | 48 | 28 |
| [−1,1] | 891 002 742 | 57 | 34 |

One contradiction in each strip, together with completeness of Steps 1–2, proves the claim for arbitrary triangular targets. The update orders explain the different pass counts. The argument does not assume that searching a partial-tiling tree to a fixed depth suffices.

**Replaying the interval check.** Use Python 3 and a C++17 compiler. Run the following commands from this directory.

    python build.py /tmp/eq231
    /tmp/eq231/strip_replay 0 2
    /tmp/eq231/strip_replay -1 1
    /tmp/eq231/strip_replay 0 1 2

The first two runs should print CONFLICT at the passes in the table. The last is a positive control using the square subdivision of one tile into four and should leave four placements. Neither the code nor its results have undergone independent external review or Lean kernel checking. Priority for this exclusion has not been established.

## Consequence for the unrestricted family 21q

For prime q, these tests leave **only q=37** undecided for T(21q). The answer is positive for q=3,7 and negative for every other prime except 37.

For q>362, the large-prime-divisor theorem for the squarefree cofactor h=21 leaves only sums of two squares, impossible because 3 and 7 have odd exponents. For q=3 the W construction with (u,v)=(1,2), Q=7 and scale 3≥v gives 63. For q=7 the classical count 3·7² gives 147. The remaining primes q≤362 give squarefree 21q. The sources in the preceding study exclude W, β, θ and the double-angle case at scale 1. Enumerating the nine product forms through 21·362 leaves only 105, 231 and 777. An earlier argument excludes 105, and the proof above excludes 231. For 777 the remaining case is F4 with tile (16,5,19) and target (304,185,399). This note leaves that case open. The script row21.py reproduces the finite enumeration. [Large-prime-divisor theorem, §3](../../continuation/RESULTS.md) · [Paliy’s earlier exclusion of 105](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/n105/PROOF_N105.md).
