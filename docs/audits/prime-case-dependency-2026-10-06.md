# Independent dependency audit of the existing Group-1 arguments

6 October 2026. This is an internal rechecking of
`docs/prime-case-candidate.md`, not a new proof-priority claim or external review.
The audit found no gap in the current W appendix or reverse-apex proof. It does
not certify a full classification in Erdős problem 634.

## The W appendix

The initial column uses the **actual** strip between the external supporting
line and the first internal column. Its width is precisely the tile altitude
to its longest side. The reflected placement of a whole c-edge is excluded by
the nonintegral distance of its third vertex along the integer-sided external
boundary. This establishes the complete left c-chain before any assertion
about its opposite bank.

The opposite bank is c-only only after its full length is shown to be `n*c`
with `n<u`. The extra boundary c-edge needed to establish this strict bound
comes from an actual boundary angle fan; the upper boundary point cannot be
the target's theta corner. No c-only conclusion for arbitrary `n<v` is used.

The horizontal-cap lemma has two independent endpoint caps: the external
supporting line at its left end and the interior of the crossing tile at its
right end. Thus short-a purity applies to a whole opposite chain, including
when that chain changes tile at T junctions.

The diagonal-chain obstruction uses completion properties only for columns
of index strictly smaller than its starting index. Every newly supplied
c-edge is connected to the earlier column through an already actual
rectangle. If it passed a previously established maximal endpoint, this
would contradict maximality; it cannot be reinterpreted as a new disconnected
column. The opposite diagonal chain may change tile. Short-b purity says
that it crosses each intermediate grid endpoint, not that one original edge
continues artificially through the entire construction.

The strong column induction first completes the full normal left chain;
only then does it derive the opposite-bank restriction. Its local forcing
uses already established smaller columns. Finally, each new corner front
uses established columns up to its own index. This gives a noncircular
dependency order:

`K_m -> opposite b-row -> column m -> K_(m+1)`.

No generic strip-packing assertion or purity of long c-seams occurs in these
steps.

## The reverse-apex argument

The equal outer sides have no b-edge by short-a purity and the existence of a
boundary c-edge. The three-alpha apex therefore starts an actual b/c mismatch.
At every diagonal endpoint of index below v, short-b purity forces an
opposite edge to cross the endpoint.

The cap at that endpoint initializes a whole horizontal chain. Downward
completion of column `M_m` excludes a switched beta tile by a complete
short-a chain containing a c-edge. Filling the other gaps uses only the
no-opposite-b properties of strictly smaller, previously completed columns.
Their connectivity is supplied by the already actual truncated corner.

Only after the whole column is completed is its length `n*c`, `0<n<v`, used
to exclude opposite b-edges. The arithmetic permits opposite a-edges here;
the proof never excludes them. This is exactly the restriction needed by
the next alpha fan. The final column reaches height zero by its initialization,
so the whole `v^2` patch follows from the established completion statement,
not from a packing or area assertion. Its complement is an actual tiled W
triangle.

The new universal two-c-edge lemma is consistent with these arguments but
is not a dependency of either proof.

## Boundary inventories obtained from the two-c-edge lemma

Write `delta=v-u`, `Q=2*v^2-u^2`, and `P=3*v^2-u^2`. Let `(A,B,C)` count
whole a-, b-, c-edges on one outer side. In each formula retain only
nonnegative integer counts and impose `C>=2`.

For W the complete possibilities are:

| Side length | Counts `(A,B,C)` | Integer parameter |
| --- | --- | --- |
| `v^3` | `(v*h, 0, v-u*h)` | `1 <= h <= floor((v-2)/u)` |
| `v*b` | `(v*k-u, 0, v-u*k)` | `1 <= k <= floor((v-2)/u)` |
| `u*Q` | `(0,u,u)` | none |

Here `h>=1` uses the beta corner: the uQ side has no a-edge, so its incident
beta tile has c on that side and a on the v-c side. The arithmetic alone
allows `h=0`. These inventories imply `u>=2` and `v-u>=2`, but do not alone
exclude every scale-one W.

For the beta target each equal side has counts
`(v*h,0,v-u*h)`, with `0<=h<=floor((v-2)/u)`. Its base `u*P` has precisely:

* `(0,u,2*u)`; or
* `(v-k*delta, u+v*k, u-k*delta)` for integers `k>=0` with
  `u-k*delta>=2`.

In the first base case both equal sides must have `h>=1`, because the base
has no a-edge and each base corner is a single beta tile. In the second
case `h=0` is not excluded just by the side counts. These inventories are
necessary conditions; the universal exclusion still uses the geometric
proofs audited above.
