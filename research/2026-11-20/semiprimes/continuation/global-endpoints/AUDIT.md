# Scope audit of the semiprime classification

20 November 2026. Independent arithmetic check for the Denis Paliy Erdős 634 project.
This note does not settle an additional residual F2 unit board.

## Exact remaining issue

Let T(n) mean that some triangle can be tiled by n congruent triangles, with
reflections and T-junctions allowed. For distinct primes 3<p<q of opposite
residues modulo four, the recorded geometric reduction gives exactly one
possible board whenever

    q < 2p,   3 | (p+q),   (p²-pq+q²)/3 = c².

Its tile is (a,b,c), with a=(2q-p)/3 and b=(2p-q)/3, and its exterior
sides are ap, bq, c². A necessary conic identity is not a construction.

The existing unit staircase proves existence when u is at most 4v², except
for the class g=3, v=2 modulo 3, where its threshold is 4v(v-1). Here
u/v=(a+c)/b is reduced, g=gcd(3,u-v). The theorem is necessary and sufficient
for the staircase load system, and sufficient for an unrestricted tiling.
No argument reviewed here makes it necessary for all tilings.

Thus 3431 and 5063 are the first two outstanding examples, not the entire
remaining semiprime problem. The known finite enumeration already has 312
residual prime pairs with at least one endpoint at most one million. No
proof that the full residual set is finite or infinite is supplied.

## An independent finite census

Run `python3 audit_semiprimes.py --output census_million.json`.
The code independently enumerates products pq with p<=q and pq<=10^6,
and applies the arithmetic reduction without importing the repository's
classifier. It checks 210,035 semiprimes, including repeated primes.

| Status from the selected inputs | Count |
|---|---:|
| Positive: prime squares | 168 |
| Positive: other classical counts | 55,164 |
| Positive: Paliy construction | 20 |
| Positive: unit F2 staircase | 7 |
| Negative: small-factor rules | 49,468 |
| Negative: necessary-overlist exclusion | 105,183 |
| Distant BQ/I120 candidates requiring an additional input | 18 |
| Residual mixed F2 boards | 7 |

The seven F2 products are 3431, 5063, 19367, 60023, 64367, 271151,
and 641591. The eighteen distant candidates are retained conservatively;
161, for instance, has a separate small-count exclusion. With the recorded
moving-bank BQ/I120 manuscript theorems admitted, all eighteen are negative,
giving 55,359 YES, 154,669 NO, and seven OPEN. This is a finite census and
does not prove a classification of every semiprime.

## A structural consequence: the nonclassical near-prime graph is a forest

Use primes greater than three as vertices. Join p and q if T(pq), pq is
nonclassical, and max(p,q)<2min(p,q). The graph is a union of paths with
at most one pendant leaf attached to each path vertex.

Indeed, by the arithmetic reduction, its edges are either Paliy edges
or realized F2 edges. The former join two primes equal to 3 modulo four.
The existing norm-unit proof gives at most one increasing and at most one
decreasing Paliy neighbor, so the Paliy subgraph is a union of paths.
Every F2 edge joins a prime equal to 3 modulo four to one equal to 1
modulo four. The F2 partner uniqueness theorem gives degree at most one
to every vertex in the F2 subgraph. A prime equal to 1 modulo four has no
Paliy neighbor and therefore is a leaf in the full nonclassical graph.
Adding these leaves to the Paliy paths cannot produce a cycle.

In particular every finite induced subgraph is acyclic and has fewer
edges than vertices in each nonempty connected component. The same
statement holds for the arithmetic supergraph obtained by retaining all
F2 candidates, whether or not their unit board actually tiles. With the
two recorded distant-branch exclusions admitted, the ratio restriction
can be removed. This structural consequence gives no decision for an
unresolved F2 leaf.

## Dependencies

The arithmetic overlist is in `research/2026-11-19/continuation/RESULTS.md`.
The construction is in `research/2026-11-20/semiprimes/staircase/SHARP_STAIRCASE.md`.
The unique F2 partner proof is in
`research/2026-11-20/semiprimes/continuation/partners/PARTNERS.md`; the Paliy
path proof is in the adjacent `PALIY_PATHS.md`.
The distant-branch manuscript dependencies are explicitly identified in
`research/2026-11-20/semiprimes/continuation/counting/inputs/I120_THEOREM.md`.
Their geometric inductions have not been independently verified here.

The scripts verify the finite arithmetic statements only. They do not
verify the geometric overlist, the staircase dissection, or the moving-bank
proofs, and they do not search arbitrary tilings.
