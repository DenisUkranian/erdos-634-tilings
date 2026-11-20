# Completed exact searches

With REVERSE_TIES, IGNORE_CHIRALITY, IGNORE_SIGNS and IGNORE_CONTACTS, using the directed-side fan test:

|a,b,c|t,k|height range|result|nodes|
|---|---|---|---|---:|
|33,7,37|13,8|[-2,1]|NO|1472|
|33,7,37|13,8|[0,3]|NO|775|
|33,7,37|26,23|[-1,1]|NO|30735|
|33,7,37|26,23|[0,2]|NO|6497|
|35,13,43|11,2|[0,1]|NO|54215|
|5,3,7|14,5|[0,1]|YES|33594|
|35,13,43|3,0|[0,1]|YES|8|

The initial three negative boards also completed with IGNORE_SIDE_FANS
and REVERSE_TIES with respective counts 1673, 991; 33554, 10504;
55793. With the default tie order and IGNORE_SIDE_FANS, the first
board required 48332 and 779 nodes, and the third required 205268.
The 195-tile quadrilateral exhausted the [0,3] and [−1,2] palettes
(1,904,004 and 2,785,857 nodes), with REVERSE_TIES, IGNORE_CHIRALITY,
IGNORE_SIGNS, IGNORE_CONTACTS and IGNORE_SIDE_FANS. The signed-residue
argument in NOTCH_ENUMERATION.md proves the second palette already
contains every possible orientation. The same [−1,2] palette exhausted
again in 2,406,118 nodes after enabling the directed-side fan test.

The (33,7,37,t=26,k=23,j=1) pentagon of 206 tiles exhausted its complete
[−1,2] palette at 2,447,956 nodes, with WALL_FIRST, REVERSE_TIES,
IGNORE_CHIRALITY, IGNORE_SIGNS and IGNORE_CONTACTS. Reproduce with

    g++ -O3 -std=c++20 -DWALL_FIRST -DREVERSE_TIES -DIGNORE_CHIRALITY -DIGNORE_SIGNS -DIGNORE_CONTACTS dfs.cpp -o notch
    ./notch 33 7 37 26 23 -1 2 3000000 1

The signed residues were used only to prove the finite palette complete,
not as an implementation pruning rule in either of these two negative
replays. With chirality and signed pruning enabled and IGNORE_CONTACTS
and REVERSE_TIES set, the 171-tile positive control also succeeds
(32,352 nodes).

On the larger pentagon (35,13,43,t=22,k=17,j=1), use the complete
[−1,2] palette established by the three consecutive boundary sides.
A terminated budget is an inconclusive result.

The elementary positive construction has a separate coordinate generator,
`python coarse_construction.py`. Four exact geometric control outputs were

    (5,3,7,12,5) 119 tiles
    (5,3,7,14,5) 171 tiles
    (5,3,7,19,9) 280 tiles
    (8,7,13,21,4) 425 tiles

These counts are for the stated notch shapes. They have no implication for
the full F2 boards with different shapes at the same counts.

A separate relaxation tried the 44 projective phase directions modulo 43
at heights 0 and 1 on the 250 pentagon. The largest floating-point LP
lower bounds were approximately 10.63 and 12.05 respectively. Each
surviving integral population exceeds these values. This exploratory
relaxation supplies no exclusion certificate for this pentagon.

Two whole-paletted exploratory runs for 250 reached their 5,000,000-node
budgets in different traversals. Neither termination exhausted the tree.
The smaller inventories are reproduced by `python check_populations.py`.

The independent unseeded packing replay subsequently finished the 250
pentagon. Its 31 disjoint terminal records cover the complete [−1,2]
palette with 5,331,660 node visits. No corner tile was assumed.
The original 5063 triangle can avoid this pentagon.
