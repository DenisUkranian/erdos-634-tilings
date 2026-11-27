# Area behind a gate carrying a unit of alternating charge

Let $E,O$ be the signed even and odd short populations on the far side of an exterior-free gate in the standard frame. Suppose $|E-O|=c$ and its two banks contain exactly $m=c+a-b$ unmatched owners. These are local hypotheses. The total unmatched population of the board is unrestricted. The gate is a single Jordan circuit by the [circuit theorem](../../../2026-11-26/semiprimes/charged-contour/README.md). Its far union consists of the enclosed tiles. The following bounds include all occupied descendants.

| Board | Gate length in owners | Possible absolute ordinary charge | Maximum far tiles | Minimum tiles on the side containing the exterior path |
|---|---:|---|---:|---:|
| 3431 | 63 | 37 or 111 | **2849** | **582** |
| 5063 | 65 | 43 | **2107** | **2956** |

In particular at 5063 one of the two signed parity totals is zero. If a branch with $|E-O|=c$ contains more than the specified far population it costs at least 65 owners at 3431, or 67 at 5063. The alternating character is a sum of unit signs, so the next possible cost is two higher. At 5063 this applies in particular to a branch containing half the board or more.

## The outer triangle limits the area behind a contact

This geometric bound applies to any connected polygonal tile union with boundary length at most $P$, including holes and pinches. The original F2 triangle has sides $A=b(2a+b)$, $B=a(a+2b)$ and $c^2$, making a $60$ degree angle between $A$ and $B$. On both boards its perimeter equals $N$. Write $t=ab\sqrt3/4$ for a tile area. The outer area is $Nt$ and its inradius is $R=2t$. For $\pi\sqrt3\,ab\le P\le N$ its number of tiles satisfies
$$
 n\le N-\frac{(N-P)^2}{N-\pi\sqrt3\,ab}.
$$
For a single gate circuit use $P=cm$. A disconnected cut can instead be bounded one positive Jordan circuit at a time.

To prove the bound, take the convex hull $K$ of the connected region. Its perimeter is at most the total boundary length. For a single circuit this follows by traversing its extremal vertices in cyclic order and shortening each arc to its chord. More generally the projected boundary variation is at least twice the projection width because the connected set projects to an interval and almost every interior level crosses its boundary at least twice. Integrating over directions gives the same perimeter bound by the polygonal Cauchy projection formula.

Move every support of $K$ inward by distance $s$ to form $K_s$. While it has interior, its area decreases at rate $P(K_s)$: on an interval with unchanged side incidence each moving side sweeps its length per unit distance. The finitely many incidence changes preserve continuity. Adding a disk of radius $s$ to $K_s$ gives a subset of $K$. Its perimeter is $P(K_s)+2\pi s$ by summing the straight sides and exterior circular arcs. Perimeter is monotone on convex sets by projection widths, so $P(K_s)\le P-2\pi s$. The erosion of the original triangle $T$ has area $Nt(1-s/R)^2$ for $0\le s\le R$. Consequently
$$
 |K|\le sP-\pi s^2+Nt(1-s/R)^2\qquad(0\le s\le R).
$$
If $K$ disappears before $s$, integrate only until disappearance. The function $uP-\pi u^2$ is increasing through $R$ under $P\ge 2\pi R$, so the same inequality holds. Minimize the right side at $s=(N-P)/(2(Nt/R^2-\pi))$. The perimeter interval puts this $s$ in $[0,R]$. Substitution and division by $t$ give the formula.

At 3431 the physical perimeter is 2331. Even replacing $\pi\sqrt3$ by the smaller $543/100$, the far population is at most $625815477/217667<2876$. Since $n/c$ is odd, $n\le2849$. On the 5063 board the geometric bound alone gives 3053. [triangle.py](triangle.py) independently reconstructs every atomic tile contact on both complete 143 tilings and grows connected unions. The rational inequality passes on 93 and 96 nontrivial perimeter tests. For example, a union of 141 actual tiles has perimeter 135 on each board and the upper bound is less than 142. [TRIANGLE.json](TRIANGLE.json) gives the exact values.

## Which signs and directions are available

Normalize the two alphabets as in [the contact theorem](README.md). The alternating character gives $|L-H|=m$, where $L,H$ count even headings minus odd headings on the low and high alphabets. A half-turn lets us take every low heading even and every high heading odd. The six resulting directions in heading order are the low vectors $D\rho^j$ for even $j$ and the high vectors $c\rho^j$ for odd $j$. Write their counts $w_0,\ldots,w_5$ and put $u=w_0+w_2+w_4$. Then $|E+O|=c|2u-m|/(c-a+b)$ by the ordinary cut character, independently of the local normalization sign.

For each $u$ enumerate the three nonnegative low counts summing to $u$. If these are $i,j,k$, their displacement is $D(x+y\rho)$ with $(x,y)=(i-j,j-k)$. The three high counts sum to $m-u$ and must have the opposite displacement. Also each axis sum of projected exponents is zero in each order. These tests leave ten inventories up to rotations by two headings at 3431 and four at 5063. The possible $u$ are $15,26,37,48$ and $22,43$ respectively. This proves the ordinary charge restrictions in the table. [SATURATION.json](SATURATION.json) gives every representative.

For a fixed inventory compute the [word area bound](README.md) in each cyclic order. The endpoint of every subinventory is now known exactly. [saturation.py](saturation.py) computes the maximum by recursive factor parsing. [inventory.cpp](inventory.cpp) computes the same quantity independently by increasing mixed-radix indices. If at least two abelian factor residues are nonzero a subword belongs to no single factor. With one active factor the last letter can belong to it, or a shorter identity suffix can be removed. With zero residues it suffices to choose the factor of the last letter, since the prefix of an identity word always belongs to that factor. A proper spatial return is discarded before it can become a constituent. None of these prunings needs any assumption about the tiles inside the circuit.

For the heaviest remaining inventories also keep a finite image of the other boundary group throughout the order-$b$ computation. Over the prime field $\mathbb F_p$, map generator $f=0,1,2$ of the order-$a$ group to $x\mapsto z_f+g^{e_f}(x-z_f)$ where $g^a=1$. These maps have orders dividing $a$. Each valid word therefore acts identically. Its linear coefficient on any subinventory is determined by its letter counts. Store the best area separately for each translation coefficient. Composition of profiles with coefficients $(h,s),(k,t)$ gives $(hk,s+ht)$. Earning a large area in one projection with a different witness in the other projection cannot evade this joint test. The full inventory has trivial abelian residues, hence linear coefficient one. Keep the entry with translation zero.

[charged.py](charged.py) specifies each homomorphism. For the representative $(3,16,9,10,10,17)$ on 5063, the order-13 test together with the action over $\mathbb F_{11}$ gives doubled axial area at most 981045. The odd-multiple condition gives $n\le2107$. The other inequivalent inventory with low count 22 already has cap 1849. For the 3431 representative $(5,12,12,9,9,16)$ the joint upper bound is 760683. The board containment inequality above is stronger for this board.

The word relaxation is invariant under exchanging the banks by reflection across the bisector of $D$ and $c$ and reversing the circuit to preserve its area. A step of heading $j$ becomes one of the other kind at $3-j$. In the order-$b$ projection the old directed heading $h$ maps to $3-h$, and its exponent magnitude is multiplied by $c/a$ modulo $b$. This exchanges $a$ and $c$ since $c^2\equiv a^2\pmod b$. In the order-$a$ projection use $h\mapsto 2-h$ and multiply by $c/b$ modulo $a$, using $c^2\equiv b^2\pmod a$. These are automorphisms of the cyclic-factor free products. Reversing the sequence of syllables also preserves identity, by inversion followed by the generator-inverting automorphism. The transfer compares only necessary word tests and areas. It does not assert that a reflected bank exchange is a physical retiling. It transfers the 2107 bound to the heavy inventory with low count 43.

## Reproduction and scope

```sh
python3 triangle.py | diff - TRIANGLE.json
python3 saturation.py | diff - SATURATION.json
python3 charged.py | diff - CHARGED.json
```

The final replay compiles both integer checkers, compares both separate-order calculations on every inventory, and tests the affine composition independently by literal permutations on all 3003 interleavings of a two-heading path with the 143 tile parameters. Both complete 143 boards also pass the physical word checks in [CHECK.json](CHECK.json), computed from segment displacements without either parser. The 143 examples have no occupied exterior-free branch. An unrestricted tiling may have a gate with more owners, a different signed charge or a different location of the odd imbalance.
