# Independent internal audit of the full local matrix

7 October 2026. This is an independent internal derivation and computational check, not external human refereeing or proof-assistant verification.

**Verdict: `FULL_LOCAL_MATRIX.md` passes the audit.** Its exact equivalence concerns local points at the primes dividing `6R`, with the specified valuation at 2. Its conclusion for tilings is one-way: inconsistency excludes every odd multiplier. The text correctly makes no local-to-global claim.

## Odd primes

For a prime dividing B, normalization leaves exactly two cases: u a unit, or u divisible by p and v a unit. In the second case the constant term has uniquely smallest valuation 2, so there is no omitted cancellation case. The two resulting characters are `(e/p)` and `(-12/e /p)`. Their product is `(-3/p)`. The explicit choices `(u,v)=(1,p)` and `(p,1)` prove sufficiency in the respective cases.

For a prime dividing A, either nonunit coordinate would leave a uniquely minimal term of valuation one. Thus both coordinates must be units. Dividing by p gives the quadratic with discriminant 48. It follows that primes 5 or 7 modulo 12 must be allocated to B. When p is 11 modulo 12, the two nonzero roots have opposite characters, so one always has the prescribed character. When p is 1 modulo 12, the two characters agree and give the previously audited row. The divided quartic has nonzero derivative at every admissible root; Hensel lifting with W=0 supplies a local point. These arguments establish the claimed necessity and sufficiency for all four prime classes.

The p=7 modulo 12 row has the correct coefficient of f: `(3/p)=-1`. The p=5 modulo 12 class contributes only its allocation constraint. The p=11 modulo 12 class contributes no equation. These distinctions are essential and have not been inferred from the selected-prime matrix by an invalid symmetry assumption.

## The primes 2 and 3

The required valuation of x makes both u and v odd at 2. Direct reduction modulo 16 yields `εA≡3 mod4`, exactly the displayed parity row.

The claimed sufficiency at 2 was checked algebraically. With `AB≡5 mod8`, the four residue cases listed in the proof are exhaustive. In each case `F(1)/16≡1 mod4`. Changing A or B by 8 preserves this residue. Moreover,

\[
\frac{F(3)-F(1)}{16}=2A(5\varepsilon+3B)\equiv4\pmod8,
\]

because `B≡3ε mod4`. Therefore one of the two quotients is 1 modulo 8; its square root exists in the 2-adic field. This proves sufficiency, not just a necessary congruence test.

At 3 the exact conditions are `A≡2 mod3` for ε=1 and `A≡1 mod3` for ε=3. The primitive cases excluded in the proof have odd valuation; the displayed sufficient choices produce a square unit. The resulting parity row is identical to the 2-adic row only **after** imposing the allocation constraints at primes 5 and 7 modulo 12. The proof performs this step in the correct order.

## Independent computations

A separate pure-Python calculation, without importing either authored checker, tested every cover of every squarefree product of at most four primes from

`{5,7,11,13,17,19,23,29,31,37,41,43}`

whose product is 5 modulo 8. The results were:

| Check | Number | Result |
| --- | ---: | --- |
| Squarefree products | 196 | PASS |
| Full variable assignments / covers | 4952 | PASS |
| Direct local tests at odd primes dividing R | 18688 | PASS |
| Independent 2-adic residue tests | 2048 | PASS |

At primes dividing A, the direct test enumerated nonzero roots of the divided quartic over the finite field, rather than using the proposed matrix formula. At primes dividing B, it enumerated nonzero square residues and checked both normalized cases. Each individual odd-prime row and the complete combined system agreed with those direct conditions.

The 2-adic test used all odd A,B modulo 128 with `AB≡5 mod8`, both ε choices, and direct membership of `F(1)` or `F(3)` in the square residues modulo 4096, with valuation four. It agreed in every case with `εA≡3 mod4`.

## Scope

The branch isolation, rational map, and completeness of the relevant square classes were audited separately in [AUDIT.md](AUDIT.md). Thus the universal odd-multiplier exclusions inherit an explicit exhaustive branch reduction, rather than an assumption that a supplied F3 candidate represents every tiling.

The new result classifies these local covers. A surviving cover can still lack a rational point, a primitive integral norm triple at a chosen multiplier, or a geometric tiling. None of those implications is supplied by this audit or the theorem. In particular, 154, 4830, and the general classification remain unresolved.
