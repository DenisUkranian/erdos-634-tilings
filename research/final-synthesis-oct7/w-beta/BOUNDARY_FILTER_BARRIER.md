# A uniform blind spot of the W and beta boundary filters

7 October 2026. This is a limitation theorem for specified necessary
conditions. It neither constructs a triangular tiling nor excludes an
integer tile count. The full Erdős problem 634 remains unresolved.

## Statement

Let `0<u<v` be coprime and set

    a=uv, b=v²-u², c=v², Q=2v²-u², P=3v²-u², delta=v-u.

The following four tests, taken together, **cannot reject any integer
scale m>=2** in either the W or beta-isosceles family:

1. Each outer side is a sum of complete a-, b-, and c-edges.
2. Every side contains two consecutive c-edges.
3. The edge labels at each target corner agree with its exact tile-angle
   inventory, including the single tile at a beta corner.
4. Each straight boundary junction has a nonnegative tile-angle
   completion summing to pi.

The same conclusion holds at m=1 whenever `u>=2` and `v-u>=2`.
Thus even this combined boundary filter leaves the entire interior
parameter range of the scale-one W candidate, and every larger scale.

These are explicitly the four tests above. They do not include geometric
placement, compatibility between consecutive fans, or full opposite-bank
seam equations. No assertion is made that a complete incidence disk, or
even the entire geometric boundary collar, exists.

## Exact side words for W

Write the W corners as B, C, A, with angles beta, 2alpha, theta=alpha+beta.
Orient its side words as follows; exponents denote repetitions:

| Oriented side | Length | Word | Angles at the start and end of each supported edge |
| --- | --- | --- | --- |
| B to C | mv³ | a^v c^(mv-u) | a: beta,gamma; c: beta,alpha |
| B to A | muQ | c^(mu) b^(mu) | c: beta,alpha; b: gamma,alpha |
| C to A | mvb | c^(m delta) a^(m delta) | c: alpha,beta; a: gamma,beta |

The length identities are

    va+(mv-u)c=mv³,
    mu(b+c)=muQ,
    m delta(a+c)=mvb.

For m>=2, all displayed c-run lengths are at least two:

    mv-u >= v+1 >= 3,  mu>=2,  m delta>=2.

For m=1 they are at least two under the stated interior-parameter
hypotheses. All repeated-edge counts are positive.

At B, the first a-edge of BC and first c-edge of BA belong to the same
beta tile: the incident side lengths of a beta tile are precisely a,c.
Hence there is one beta angle there, not two. At C the two supported
c-edges supply alpha+alpha; their inward sides both have length b.
At A the last b-edge and last a-edge supply alpha+beta; their inward
sides both have length c. These match all three exact corner inventories.

Along BC, the residual angle at an a/a or a/c junction is alpha, and at
a c/c junction it is gamma. Along BA, c/c leaves gamma, while c/b and
b/b leave beta. Along CA, c/c leaves gamma, while c/a and a/a leave
alpha. Each is a valid tile angle because

    alpha+beta+gamma=pi.

This establishes all four formal boundary tests, including adjacent
c-edges, by one explicit word system for every specified pair and scale.

## Exact side words for beta-isosceles

Let B and A be the beta corners and C the 3alpha apex. On each equal
side, oriented from its beta corner to C, use

    a^v c^(mv-u),

with the same supported endpoint-angle assignments as on BC above.
On the base from B to A use

    c^(mu) b^(mu) c^(mu).

On its first c-run assign beta,alpha; on the b-run assign gamma,alpha;
on the last c-run assign alpha,beta. The base length is

    mu(c+b+c)=muP.

At each beta corner the first equal-side a-edge and the corresponding
base c-edge support a single beta tile. At C the two supported alpha
angles leave one additional alpha angle, giving exactly 3alpha.

All equal-side junctions are as before. On the base, c/c leaves gamma,
c/b and b/b leave beta, and the b/c transition leaves alpha+2beta,
which is a valid three-tile angle inventory because

    2alpha+(alpha+2beta)=3alpha+2beta=pi.

The c-run lengths again meet the adjacent-c requirement. This proves
the beta assertion.

## Consequence for the remaining research

The universal adjacent-long-edge theorem remains a genuine necessary
geometric result, and its forced words can help a positional search.
But side-length arithmetic, that adjacency conclusion, and abstract
boundary angle counts cannot by themselves finish the low-scale W/beta
classification: the explicit words above satisfy them uniformly.

For example, the words at `(u,v,m)=(2,3,2)` are

    W:  a³c⁴ on length 54; c⁴b⁴ on length 56; c²a² on length 30.

This does not assert that all the supporting triangles are jointly
nonoverlapping. It supplies necessary-data witnesses, not a tiling.
The scale-two nine-tile collar already in the repository gives a
separate actual local realization on the last side; it does not fill
the other sides or the interior.

The missing ingredients remain positional compatibility or a global
construction/descent theorem. The sharp actual seam exchange `uc=va`
and the local three-angle escape at the second W56 junction prevent
replacing these missing ingredients with short-chain purity or immediate
corner forcing alone.

## Verification and dependencies

`check_boundary_filter.py` independently recomputes the side lengths,
checks the angle complements as integer pairs in `(alpha,beta)`, and
checks the c-run thresholds. Its finite regression range supports the
implementation; the formulas above prove the unbounded statement.

Dependencies: the target side formulas and primitive parameters from
`../../w-beta-caps/PROOF.md`; the adjacent-c necessary theorem from
`../../w-global-oct7/ADJACENT_C_EDGES.md`. The argument makes no use of
the proposed scale-one prime-case proof or any retracted divisibility
claim. It is a project-internal structural observation, with no external
priority or referee claim.
