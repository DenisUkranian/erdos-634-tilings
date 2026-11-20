# Each prime has at most one mixed F2 partner

For distinct primes greater than three in opposite residue classes modulo four, the [prime-product reduction](../../README.md) leaves only the unit F2 board. For fixed prime P this board can arise with **at most one other odd prime**, counting both smaller and larger partners together. The following algorithm constructs its sole integer candidate; that candidate may be even or composite.

## Partner theorem

Let p,q be the two factors in either order, put P=p, Q=q, and suppose the F2 conic and range hold. Then 3 divides P+Q and
$$
 y=(2Q-P)/3, \qquad x=2c, \qquad x^2-3y^2=P^2,\qquad 0<y<P .
$$
Here x is even, y is odd and P does not divide y. Conversely such x,y yield the integer Q=(P+3y)/2. It lies strictly between P/2 and 2P. If Q is an odd prime, the legs y and (P-y)/2 are positive, odd and relatively prime, the factors are P,Q, and c=x/2 is their norm hypotenuse. The oddness of the second leg uses odd Q and the equality P= y+2((P-y)/2): because 2Q=P+3y is 2 modulo four, P-y is 2 modulo four. Their product of factors is 7 modulo eight by the primitive odd norm identity, so the prime partners automatically have opposite residues modulo four.

Here is a short uniqueness proof. The congruence (x/y)^2=3 modulo P² has at most two roots, opposite to each other: if two roots are not congruent up to sign modulo P², their sum and difference would both be divisible by P, impossible for a unit since P is odd. Write A=x+y√3, e=2+√3. Since Norm(A)=P² and 0<y<P, P<A<eP. For two solutions on the same root line, A1 conjugate(A2)/P² has integral coefficients: its rational numerator vanishes modulo P² by the common square root equation, and its irrational coefficient by equality of the roots. It is a positive norm-one element strictly between 1/e and e. The only such element is 1, since every integral positive norm-one element bigger than 1 has irrational coefficient at least 1 and is at least e. For opposite roots, A1 A2/P² instead has integral coefficients, norm one and lies strictly between 1 and e², hence equals e. Its rational coefficient must be odd (divide an odd numerator by the odd denominator P²), contrary to the rational coefficient 2 of e. This proves uniqueness on both sides of P simultaneously.

The candidate exists as an integer exactly for P=1 or 11 modulo 12. In one direction this follows by reducing the equation modulo P and applying quadratic reciprocity. Conversely work in the norm-Euclidean ring of x+y√3 with integral x,y. Division with both rational coefficients rounded to nearest integers has absolute norm error at most 3/4. For a root r of 3 modulo P, the ideal (P,r+√3) has index P by evaluation at √3=-r modulo P. A Euclidean gcd therefore gives a generator t with |Norm(t)|=P. The conjugate ideal is distinct because r is nonzero modulo P. In particular t² cannot be an associate of P. Multiply t² by a suitable integral power of e to obtain an element A strictly between P and eP. Endpoints would make t² associate to P. Its paired element e conjugate(A) lies in the same interval. They have opposite rational coefficient parity: multiplication by e and conjugation swap the two coefficient parities, and odd norm means the parities differ. Exactly one gives the desired even x. This is also a construction from P alone.

This arithmetic statement provides a unique candidate board, including for the outstanding mixed pairs 47 with 73 and 61 with 83. Actual tileability of each candidate requires a dissection or a geometric obstruction.

## Census of prime endpoints

All partners are included whenever **at least one** endpoint prime P satisfies 5 ≤ P ≤ 1,000,000. The other endpoint may exceed a million. The unsigned row counts below count endpoints; an edge with both endpoints below the bound contributes twice.

| Outcome for P | Number of primes |
| --- | ---: |
| 3 is a nonsquare modulo P | 39,278 |
| Even integer partner | 19,612 |
| Odd composite integer partner | 13,557 |
| Odd prime partner with a staircase tiling | 5,538 |
| Odd prime partner outside the staircase | 511 |
| Total | 78,496 |

There are 3,459 distinct incident arithmetic prime pairs. The [unit staircase](../../staircase/SHARP_STAIRCASE.md) supplies 3,147 positive tilings. There are 312 pairs outside its parameter range, including 199 with both endpoints at most a million. The largest residual product in this census is 1,977,914,809,727. These counts concern the mixed sector; a failed staircase test leaves the geometric question.

From this directory, run standard Python 3 with assertions enabled:

```sh
python3 partners.py
python3 census.py --write-residuals residuals.csv
```

The first script compares prime outputs to exhaustive exact square testing through 10,000. The second recovers the entire list independently by enumerating ordered (u,v) with u²<3,000,000 and checking both factors for primality in a sieve. The two computations must agree on every row, including all parameter values. The [replay](census.txt) records SHA-256 digests for the complete list and the [residual CSV](residuals.csv).

## Consequences for the original tiling question

* [All odd prescribed factors](PARTNERS.md) gives the exact number of primitive boards even for a composite endpoint.
* [Paliy paths](PALIY_PATHS.md) shows how the other nonclassical family fits with the F2 partners. It gives the complete row for 1031, with an arithmetic check of all distant primes.
* [Residual bound](SIEVE.md) shows that at most $O(Y^{3/4}/(\log Y)^2)$ primes up to $Y$ can have any mixed partner still requiring geometry. Thus for a set of primes of relative density one the mixed-residue question is decided for **all** other primes simultaneously. The estimate gives no decision for a specified residual pair.

For every fixed prime $P\equiv1\pmod4$, this also describes its **entire** row. The primes $q=2$ and $q\equiv1\pmod4$ always give a tiling of $Pq$ by the classical sum-of-two-squares construction or the square grid. The small-prime rules exclude $q=3$. Of the remaining primes, only the unique F2 partner can give a tiling. When it is prime and passes the staircase threshold, it occurs. The unresolved alternative is exactly whether the specified unit board tiles for a prime partner outside the threshold. These statements follow from the [prime-pair reduction](../../README.md) and the [small-prime rules](../SIMULTANEOUS.md).

### Test any two input primes

Run `python3 classify.py 47 73` for a result with its reason. A result of OPEN identifies the exact fixed board and tile. The NO cases explicitly identified as manuscript exclusions use [I120 §5 and its adjacent-BQ input](../counting/inputs/I120_THEOREM.md). The degree bound beyond the ratio of two uses the same inputs. All other prime pairs are handled by the established reductions and constructions cited above. With these manuscript inputs, 77,985 of the 78,496 primes from 5 to one million have a decided answer for **every** prime partner, with no bound on that partner. The other 511 each have one residual partner. For primes equal to 1 modulo 4 the whole-row result is independent of both additional exclusions.

Internal checks are recorded here. No independent referee report or formal proof of these new results is claimed.

The [all-prime row estimate](ALL_PRIME_ROWS.md) controls actual positive counts as well. Only $O(Y/(\log Y)^2)$ primes $P\le Y$ have any nonclassical positive product $PQ$, even allowing arbitrary primes $Q$. It uses the older necessary geometric overlist and hence avoids the two additional manuscript exclusions.

The classifier also reproduces the project census on all 88 products of two primes through 279, including repeated primes (31 YES, 57 NO). [Census and sources](../../../../2026-11-19/next/global/CENSUS_279.md).
