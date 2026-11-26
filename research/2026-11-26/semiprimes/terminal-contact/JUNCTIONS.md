# The two saturated slant paths must have compatible whole owners

Assume equality in the earlier unconditional bound, $M=107$ at 3431 or $149$ at 5063. Use the increasing tree in the standard vertex-phase frame, $X=A$, $Y=B\rho$, where $A=b(2a+b)$, $B=a(a+2b)$. Write $d=a-b$. At equality every unmatched tile is on one of the two nested cuts. The effective crossing graphs from $Y$ to $X$ use only the even headings $0,2,4$ of each of their two alphabets. The first cut has $2c-d$ low and $c-d$ high letters, the second $c$ low and $c-d$ high letters. Here low/high always denotes the effective direction alphabet, as in the [nested-cut calculation](../boundary-word/README.md).

## Every equality inventory is a single path

Take any directed circuit in a crossing graph and let $u,v$ count its low and high edges. The circuit is physically supported. Weight each tile by its winding number, exactly as in the [terminal proof](TERMINAL.md). All active headings are even. Applying the two boundary characters gives $(c-d)\mid(u+v)$ and $(c+d)\mid(u-v)$. Both bank inventories are smaller than $c+d$. Since $c-d$ is odd, a nonempty circuit must have $u=v=c-d$, exhausting every high letter. On cut two, the remaining $d<c$ letters cannot span $|X-Y|=c^2$. On cut one there remain exactly $c$ letters of length $c$. Equality in the triangle inequality would make every one parallel to the exterior slant. These are height-zero letters and the slant has height two, a different physical direction class. This excludes every directed circuit. Endpoint divergence is a unit source at $Y$ and sink at $X$. Decomposition of an integral nonnegative flow into a simple path and circuits therefore gives one positioned path, also for the six-direction inventories.

## Simultaneous exclusion of the three-direction combination

Use, on cuts one and two respectively, the low/high triples
$$
((c-a,0,c+b),(c-d,0,0)),\qquad ((0,0,c),(b,0,c-a)).
$$
Every owner is determined by the position on its path, its bank and its heading. Remove the $c-d$ unmatched height-zero owners from the axial core, the complement of the first slant component. The rest of the core consists of actual half-turn pairs. The core is on the opposite bank of the first path to the slant component. In the travel order $Y$ to $X$ in standard unrotated coordinates, its effective high step $(a,b)$ is replaced by $(a,0)$ and $(0,b)$ in that order. Its two low steps are $(c,0),(0,-c)$. The boundary also includes the axial walls. Its only directions are the two coordinate axes. Each pair in the remainder must then use those two axes: a maximal supporting line in any third edge direction would expose a positive subinterval of a pair edge on the outside bank, since a covering pair on that bank would reach a strictly larger supporting line. This contradicts the boundary identity. All pairs here are therefore axial $a$-by-$b$ rectangles with either alignment.

The replaced path never decreases its first coordinate. At a generic column inside either forward horizontal step, the core slice extends from the lower wall up to the path. A sum of rectangle heights gives a value in $a\mathbb N_0+b\mathbb N_0$. For prefix counts $(i,j,k)$ of the two low moves and the high move, respectively, the required value is $B-cj+bk$. This applies before either move that has a forward horizontal piece, including before the vertical part of the repaired high move. The second cut instead uses the [height-two staircase and its two residue constraints](../boundary-word/RECTANGLES.md). It has 42 candidate words at 3431 and 109 at 5063.

To compare both paths in one frame `junction.py` uses the integer axial coordinates $c z^{-1}(p-Y)$. In that frame $Y=(0,0)$, $X=(bc^2,-(a+b)c^2)$ and $O=(-bB,-aB)$. For a row below the edge vector is $c$ times the displayed move; the third vertex is the start plus the displayed offset.

| Cut | Token | Move divided by $c$ | Third vertex offset |
|---|---|---|---|
| 1 | low 0 | $(a+b,-b)$ | $(ac,0)$ |
| 1 | low 4 | $(-b,-a)$ | $(0,-ac)$ |
| 1 | high 0 | $(c,0)$ | $(a(a+b),-ab)$ |
| 2 | low 4 | $(0,-c)$ | $(ab,-a(a+b))$ |
| 2 | high 0 | $(a,b)$ | $(ac,0)$ |
| 2 | high 4 | $(b,-a-b)$ | $(0,-ac)$ |

For each second word, keep all its positioned triangles fixed. Start the first path at $Y$ with zero counts. Extend it with each of its three moves that still has inventory, passes the column test, lies in the board, and gives no interior overlap with the last owner or any fixed second-path owner. The state (three counts, previous token) fixes the position and preceding owner. More distant first-path self-conflicts may be ignored for this necessary test. Disjointness uses the separating-axis test with exact signed determinants. Bounding-box buckets only omit triangles in disjoint coordinate ranges. No first path reaches $X$ for any second word. Thus this combination is impossible on both boards.

The independent `review_junction.py` starts at $X$ on the 3431 board. It places triangles from the original tile parameterization in unrotated coordinates and retains all feasible eight-edge suffixes for each cut with the applicable width tests. It finds 13 and 7 suffixes and a positive-area overlap in each of the 91 pairings. This argument needs only a neighborhood of $X$.

After this first test one of two angular combinations remains at 3431 and seven of eight remain at 5063. Excluding one joint inventory does not exclude the second-cut inventory in isolation. Outside equality, mixed-height cycles and the other configurations in the common-obstruction checkpoint remain admissible in this analysis.

## The remaining 3431 inventory also fails

At 3431 the other first-cut inventory has low triple $(14,1,33)$ and high triple $(0,1,10)$. Its second-cut inventory is unchanged. In native core coordinates, start at $Y=(0,B)$ and take every low step as $37\rho^j$ and every high step as $33\rho^j$ followed by $7\rho^{j+1}$. Include the sides $O\to Y$ and $X\to O$. This closed chain is the negative of the residual core boundary. The third axis can now occur among the physical pairs. The endpoint-current test remains valid for each of their three directions.

For an oriented primitive lattice axis, separate the projected endpoint differences modulo $s$ according to the normal coordinate modulo $s$. In each such class, the sum of signed steps along the axis is zero modulo $s$. To see this, use any integer linear functional taking the primitive unit along the axis to 1. Applying it modulo $s$ to each endpoint difference yields the stated signed length sum. Vertex positions in this test are integral because each crossing graph is a single path with a known start. The following four restrictions precede the full endpoint test.

1. On the vertical axis modulo 33, all pieces except the 33 low-4 steps have length divisible by 33 (including the wall of length $B$). Since $37$ is invertible modulo 33, the number of low-4 steps in each $x$-residue is a multiple of 33. All use the same residue.
2. On axis 2 modulo 33, there is one low-2 step of length 37. The ten high-4 steps each contribute a short piece of length 7 in the opposite direction. All other contributions vanish. Any normal residue without the low-2 step would need a multiple of 33 such short pieces; there are only ten in total. Thus these eleven letters share the same starting $x+y$ modulo 33. For high-4 the previous piece inside the same letter changes this coordinate by a multiple of 33.
3. On the horizontal axis modulo 33, apart from the fourteen low-0 steps only the horizontal wall at $y=0$ and the single high-2 short piece of length 7 can contribute. Any nonzero residue different from that high-2 residue would need a multiple of 33 low-0 steps. Thus every low-0 start with $y\not\equiv0$ shares its residue with high-2. Its repaired short piece has the same $y$ modulo 33 as the start.
4. On axis 2 modulo 7 only the low-2 step of length 37 and the high-2 piece of length 33 survive. Their starting $x+y$ residues therefore coincide.

With the five letter types in the order low-0, low-2, low-4, high-2, high-4, the dynamic program remembers inventory, previous owner, and these four residues, initially unspecified. Each extension must lie inside the board and avoid overlap with the immediately preceding owner. Exactly 6186 words satisfy these tests. Evaluating the full direction-labeled endpoint differences modulo both 7 and 33 leaves 85. Checking all pairs of owners within the first path leaves 30. Each of these 30 paths overlaps every one of the 42 possible second-cut paths in at least one positive-area triangle intersection. The exact replay is [rare_core.py](rare_core.py).

Consequently both 3431 angular inventory combinations fail at $M=107$. Since $3431-M$ is twice the number of half-turn pairs, $M$ is odd. Every complete 3431 tiling would therefore have **at least 109 unmatched tiles**. This rules out the entire equality population at that board. Larger unmatched populations remain open.

## Residues in the seven surviving 5063 combinations

The first-cut inventory has low/high triples
$$
(8+6i,i,56-7i),\quad (21-7i,i,6i),\qquad 0\le i\le3 .
$$
In the native core frame the diagonal axis 2 of the repaired path receives $i$ positive low steps of length 43, $i$ positive pieces of length 35 from high-2, and $6i$ negative pieces of length 13 from high-4. The two exterior sides have different directions from this axis. Fix a normal residue $x+y$ modulo 35. With $u$ low-2 steps and $v$ high-4 pieces there, the projected current forces $8u-13v\equiv0\pmod {35}$. Hence $v\equiv6u\pmod {35}$. Both $v$ and $6u$ are between 0 and 18. **Exactly six high-4 pieces are required for each low-2 step in the same normal residue, counting multiplicities.** The shift within a high-4 letter is zero modulo 35 in this coordinate. Modulo 13 the length-13 pieces drop out, and the numbers of low-2 and high-2 starts agree in each normal residue, since $43\equiv-35\pmod {13}$ and both counts are at most three. At $i=3$, the 35 low-4 steps also share one $x$ residue modulo 35. Indeed all contributions to this axis other than low-4 have length divisible by 35, as there are no high-0 pieces and $35\mid B$.

For the other height-two inventory the low/high triples are $(6,1,36),(6,1,14)$. Rotate by $z^{-2}$ about $Y$ as in the height-two paper. Each low letter $j$ repairs to $35\rho^j,13\rho^{j-1}$, each high letter remains $43\rho^j$, and the slant is vertical. Axis 2 has one high-2 letter, one low-2 length-35 piece, and six opposite length-13 pieces from low-0. The same normal-residue proof places all six pieces at the high-2 normal residue modulo 35, and identifies the low-2 and high-2 normal residues modulo 13. These top and core conditions are in their respective physical frames. The two sets of residues cannot be identified without transforming coordinates.
