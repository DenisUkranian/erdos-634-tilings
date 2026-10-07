# Independent internal check of the class-38 nonperiodicity deduction

7 October 2026. This audit checks the new implications in
[STRUCTURAL_AUDIT.md](STRUCTURAL_AUDIT.md), retaining the explicitly cited
earlier classification and prime-avoidance theorems as inputs. It is an
internal review, not external refereeing or formal verification.

1. For an odd admissible multiplier `m=3q^k`, the earlier all-branch
   isolation forces F3. Its coefficient multiplier `s` divides `m` and
   is divisible by 3, including when `q=3`. Thus `s=3q^r`, `0<=r<=k`.
2. The two factors `A=a+b`, `B=a+2b` are coprime, satisfy `A<B<2A`,
   and have product `114q^(2r)`. For `r>0`, exactly one contains `q`,
   and the other divides 114, even if `q` itself divides 114. If the
   bounded factor is A, the product is less than `2*114^2`; if it is
   B, the stronger bound `AB<114^2` holds. Hence `q^(2r)<228`.
3. Independent coprime-factor enumeration gives the primitive rows
   `(A,B)=(27,38),(38,75),(50,57),(57,98),(114,121),(114,169)`.
   Their candidate squared longest sides are respectively
   `553,1407,2199,2593,12247,9751`, all nonsquares. The author's extra
   nonprimitive `(81,114)` row is also harmless and nonsquare.
4. For any modulus M, prime avoidance supplies a genuine odd positive
   multiplier `m0` with `v3(m0)=1` and no other prime factor dividing
   `2M`. Therefore `h=m0/3` is coprime to `2M`, including when `3|M`.
   Dirichlet applies to `q=h mod 2M`. The negative sequence `3q` is
   congruent to `m0 mod M`; the positive sequence `m0(1+2Mj)` is odd
   and in that same residue. Both are unbounded.
5. This disproves eventual periodicity, but does not disprove divisor
   tests, input-dependent moduli, or any arbitrary algorithmic or
   parameterized characterization. Infinite minimal divisibility
   generators alone would not imply this stronger result.

The exact finite checker was run separately and passed. The infinite
argument uses the written earlier prime-avoidance proof and Dirichlet's
theorem; neither is inferred from that computation. No small-scale
geometric case, including 154 or 4830, is settled by this deduction.
