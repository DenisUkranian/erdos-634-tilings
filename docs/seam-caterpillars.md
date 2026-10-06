# Seam contact components are caterpillars

This strengthens the side-contact forest obstruction in
[exact-seam-certificates.md](exact-seam-certificates.md), Section 2. It is
a local theorem about a single straight seam, not a classification of
triangle tilings or a solution of Erdős 634. No claim of priority is made
for this elementary interval-partition observation.

## 1. Two interval partitions

Let a closed interval J have two finite partitions into closed intervals
of positive length, one on each bank. Interiors of distinct intervals in
the same partition are disjoint. Form the bipartite overlap graph H:
vertices are the intervals, and an edge means positive-length overlap.
Point contacts do not count.

A **caterpillar** is a tree whose vertices of degree at least two induce
a path, a single vertex, or the empty graph. Equivalently, deleting all
original leaves once leaves a path or nothing. The single-edge tree is
included.

**Theorem 1.** Every connected component of H is a caterpillar.

**Proof.** Write p and q for the numbers of intervals on the two banks,
and h for their common internal breakpoints. Their combined breakpoint
set cuts J into p+q-1-h positive atoms. Every atom belongs to exactly one
interval on each bank and hence determines one overlap edge. A given
pair of intervals has connected intersection, so it cannot account for
two different atoms: an intervening breakpoint would end one of those
two intervals. Thus H has p+q vertices and p+q-1-h edges.

Precisely the h common breakpoints separate components. Between two
successive common breakpoints, consecutive atoms share the interval on
the bank whose interval does not end at their intervening breakpoint;
their overlap edges therefore form a connected sequence. Hence H has
h+1 components and is a forest.

Fix a vertex v with interval I. Its neighbors correspond to intervals
on the other bank, with pairwise disjoint interiors. A neighbor whose
interval is contained in I has no other positive overlap and is a leaf.
Consequently any nonleaf neighbor must extend past an endpoint of I.
At most one neighboring interval can extend past each endpoint, so v
has at most two nonleaf neighbors. In a tree the induced subgraph on
nonleaf vertices is connected whenever it is nonempty: the unique path
between two nonleaves has only nonleaf internal vertices. It is thus
a connected acyclic graph of maximum degree at most two, which is a
path or a single vertex. QED.

**Tiling corollary.** In any finite triangle tiling of a convex polygon,
every nontrivial component of the original-side contact graph is a
caterpillar. This applies to noncongruent tiles and arbitrary real side
lengths. Integer side lengths are needed only for the integrality
conclusion below. Boundary side occurrences are isolated.

Indeed, each maximal collinear seam has complete-side partitions on its
two banks, as proved in the linked certificate note. Common breakpoints
may split one maximal seam into several contact components.

## 2. Exact converse for one isolated seam component

Let H be a finite tree with at least one edge. Prescribe a positive full
side length l(v) at each vertex. Consider the equations

    sum(x(e) : e incident with v) = l(v), for every vertex v.

These equations have at most one solution. Leaf elimination recovers it:
the edge at a leaf has the leaf's residual length, which is subtracted
from its neighbor before deleting the leaf. The final residual must be
zero. A solution is admissible here only when every edge length is
strictly positive. With integer l(v), all recovered lengths are integers.

**Theorem 2.** There exist two partitions of one interval whose full
interval lengths are the prescribed l(v), and whose positive-overlap
graph is H, if and only if:

1. H is a caterpillar; and
2. the displayed equations have a strictly positive solution.

The two parts of H's bipartition specify the two banks, up to interchange.

**Proof.** Necessity follows from Theorem 1 and from adding the lengths
of the overlaps along each full interval.

For sufficiency, let x(e)>0 be the solution. We first give a linear
ordering of the edges such that all edges incident with any one vertex
are consecutive.

If H is a single edge, use its one-element ordering. If the nonleaf
subgraph has one vertex, H is a star; order its edges arbitrarily.
Otherwise write its nonleaf spine as v1,...,vk. List, in order:

    pendant edges at v1,
    edge v1-v2,
    pendant edges at v2,
    edge v2-v3,
    ...,
    edge v(k-1)-vk,
    pendant edges at vk.

The order within each block of pendant edges is arbitrary. Every leaf
occurs on one edge. For each spine vertex, its incoming spine edge,
pendant edges, and outgoing spine edge form one consecutive block
(with the absent incoming or outgoing edge omitted at the endpoints).

For this ordering e1,...,er, place consecutive atoms of lengths
x(e1),...,x(er) on J=[0,L], where L is their sum. For each vertex v,
take the union of its incident atoms. By the ordering property this is
one interval I(v), of length l(v). At every atom exactly one vertex of
each bank is incident; consequently the intervals on each bank partition
J with disjoint interiors. Two intervals from opposite banks overlap in
positive length exactly when the corresponding vertices are joined by
an edge. These are the required partitions. QED.

For a prescribed forest of nontrivial components, the same result
applies component by component; the realized intervals can be
concatenated at common breakpoints.

This converse permits choosing the order of contacts. If a larger disk
certificate already prescribes the orders along its sides, those orders
must additionally be consistent with a common ordering along each
seam. More importantly, realizing every straight seam separately does
not ensure that the triangles joining three such seams fit into one
nonoverlapping triangular disk. That global condition remains exactly
the one in Section 4 of the linked certificate theorem.

## 3. A positive balanced tree that is impossible

Use full-side labels from the actual primitive tile (5,6,9). Take a
subdivided three-arm star with center o, intermediate vertices u1,u2,u3,
and leaves w1,w2,w3. Its edges are o-ui and ui-wi, for i=1,2,3.

Assign the following full lengths and recovered contact lengths:

| Side occurrence | Full length | Incident contact lengths |
|---|---:|---|
| o | 5 | 1, 1, 3 |
| u1 | 6 | 1, 5 |
| u2 | 6 | 1, 5 |
| u3 | 9 | 3, 6 |
| w1 | 5 | 5 |
| w2 | 5 | 5 |
| w3 | 6 | 6 |

This is a tree. Its two bank sums both equal 21:

    l(o)+l(w1)+l(w2)+l(w3) = 5+5+5+6 = 21,
    l(u1)+l(u2)+l(u3) = 6+6+9 = 21.

Leaf elimination succeeds and every recovered contact length is a
positive integer. Nevertheless it is not an overlap graph of two
interval partitions. The nonleaf subgraph is the three-arm star on
o,u1,u2,u3, so o has three nonleaf neighbors. It is not a caterpillar.

Thus the caterpillar condition strictly strengthens forest structure,
alternating balance, and positivity, even when all labels are valid
side lengths of a single primitive integer-sided tile. This does not
claim that the example extends to a disk satisfying the full angle and
topology tests; the disk sufficiency theorem would already exclude it.

## 4. Retained N=322 example

Extracting the actual side-contact graph of
[`data/tiling-322.json`](../data/tiling-322.json) gives:

| Component vertices | Nonleaf spine vertices | Number of components |
|---:|---:|---:|
| 2 | 0 | 444 |
| 5 | 3 | 5 |
| 11 | 9 | 1 |

Every component is a caterpillar. These counts concern the finite
retained certificate; they do not establish a bound on spine lengths
for arbitrary tilings or a uniform construction theorem.

## 5. A finite automaton for one seam

For a fixed finite set S of positive integer full-side lengths, put
L=max(S). The two-bank partitions of a connected seam component can
also be generated by a finite signed-offset automaton. Its nonterminal
states are

    -(L-1), ..., -1, 1, ..., L-1,

which is an empty set if L=1, and 0 is the terminal state. A separate start operation chooses the
first full length p on the plus bank and q on the minus bank. Set
delta=p-q. If delta=0, stop immediately: this is one matching pair of
whole sides, hence a single-edge component. Otherwise enter state
delta. The first atom has length min(p,q).

At any nonterminal state, delta is the difference between the current
cumulative bank endpoints. Extend the bank whose endpoint is earlier:

* If delta>0, append a length l in S on the minus bank and replace
  delta by delta-l.
* If delta<0, append a length l in S on the plus bank and replace
  delta by delta+l.

Each extension contributes one new atom, of length min(abs(delta),l),
where delta denotes the state before that extension. Stop at the first
visit to 0. Only finite paths that reach 0 are accepted.

All indicated nonterminal states stay within the stated finite range.
Initially abs(p-q)<=L-1. If 1<=delta<=L-1, then
1-L<=delta-l<=L-2; the negative case is symmetric. Every atom is
strictly positive and integral.

**Proposition.** The accepted paths generate exactly all connected
pairs of interval partitions whose full lengths belong to S.

**Proof.** Given such a pair, sweep from the common left endpoint.
Until the common right endpoint, the two cumulative endpoints are
unequal, since an earlier equality would disconnect the overlap graph.
The next whole interval must be appended on the bank that ends first,
which is exactly the indicated transition. The last equality accepts
the path. Conversely, successive transitions append positive intervals
on the indicated bank. Before termination one active interval always
continues across the other bank's endpoint. Thus consecutive atoms are
connected in the overlap graph; there is no common internal
breakpoint. At termination both partitions have the same right
endpoint, so they form one connected seam component. QED.

For example, with S={5,6,9}, choose p=6 and q=5 to reach delta=1.
Appending 5 on the minus bank and then 5 on the plus bank gives the
loop

    1 -> -4 -> 1.

Repeat it k>=0 times, then append 6 on the minus bank and 5 on the
plus bank to exit:

    1 -> -5 -> 0.

The result is a connected seam of total length 11+5k, with 4+2k
full side occurrences and 3+2k atoms, all using the same set of full
lengths. Thus finite local transition rules can encode unbounded seam
components. This example is an isolated seam construction; no claim
is made that every such path extends to a triangle tiling.

The automaton solves a local order-and-length compatibility problem.
It provides no rule for coupling three sides of each triangle into an
oriented disk with the necessary angle sums and triangular boundary.
In particular, it is not a pumping theorem for complete tilings and
does not prove a finite repetition grammar for all admissible N.
