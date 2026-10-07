# Independent internal audit of the rectangular obstruction

7 October 2026. This audit was carried out independently of the authoring agent. It is not external human refereeing or proof-assistant verification.

**Verdict: the theorem and corollaries in `MATRIX_OBSTRUCTION.md` pass the checks below.** Inconsistency is a sufficient obstruction to all odd multipliers. Consistency is not asserted to imply a tiling.

## 1. Exhaustive branch reduction

The hypotheses `R` odd squarefree, `3∤R`, and `R≡5 (mod 8)` give

\[
6Rm^2\equiv14\pmod{16},\qquad v_3(6Rm^2)=1+2v_3(m)
\]

for every odd `m`. The existing [F3 isolation theorem](../../../docs/f3-global-overlap.md) applies using the nonresidue prime 3, including when 3 divides the multiplier. Its proof explicitly accounts for classical tilings, all five Group-1 rows, the double-angle row, and the seven norm rows. The only residue survivors are W and F3; primitive W cannot have 3 dividing its coefficient. No candidate W/base-β scale-one argument is imported.

Because `6R` is squarefree, the F3 square scale divides `m` prime by prime. Thus the residual `s` is odd regardless of its prime support. This is essential: the theorem covers all odd multipliers, not merely those coprime to `6R`.

## 2. Rational map and cover completeness

The identities `ST=2Rs²` and `c²=T²−3ST+3S²` imply the stated elliptic equation after direct substitution. The 2-adic parity argument gives `S` odd and `v₂(T)=1`. The map has positive x because `2c−a+b>0`; its numerator parenthesis is odd, so `v₂(x)=1`.

For primes outside `6R`, odd valuation of x is incompatible with the unique term of smallest valuation in the elliptic equation. Hence every relevant positive square class is `e=2εA`, with `ε=1` or `3` and `A|R`. The quartic right side is integral, so its rational square root W is integral. No relevant negative class or zero point is lost: positivity of x excludes negative classes and x is nonzero.

## 3. Local necessity and sufficiency at selected primes

For each selected `p≡1 (mod 12)`, both `(-1/p)` and `(3/p)` equal 1. If `p|B`, the unit-u case and the `p|u` case give the same required character of e; the latter follows by division by p², with the omitted `(R/p)²` factor a unit square.

If `p|A`, primitiveness requires both u and v to be units. The normalized quadratic has roots `−3±2r`, where `r²=3`. Their product is a square and neither root vanishes. The identity with `r(r−1)²/2` therefore gives the exact character used in the proof, including the `p≡1 (mod 24)` case where the factor `(2/p)` is +1.

The local sufficiency claims are valid as scoped. For `p|B`, `u=1,v=p` gives a unit with square residue. For `p|A`, putting W=0 in the equation divided by p leaves a polynomial whose derivative is `4κu₀(q+3)`. It is nonzero modulo p because `u₀,κ,r` are units and `q+3=±2r`. Hensel lifting therefore works. This proves solubility of each cover separately at each selected prime, without invoking an invalid local-to-global inference.

## 4. Matrix and examples

The binary variable records allocation of each prime to A. Substituting its values 0 and 1 recovers exactly the two local character requirements. The diagonal term includes the quartic-character bit; deleting that bit would make the mixed-character claims false. The rectangular left-nullspace certificate is correct. Symmetry is invoked only when every prime factor is selected, so quadratic reciprocity applies with both primes 1 modulo 4.

The zero row at 13 gives the broad single-prime corollary even when some other prime is outside the selected rows. For example, it excludes all odd multipliers in class `1326=78·17`: 17 is 1 modulo 8 and 4 modulo 13. No quartic character of 17 is needed.

The displayed five-prime matrix, its vector `(0,1,1,1,0)`, kernel `3473211534`, and the mixed example `747006` were independently recomputed and agree with the proof. The arithmetic progressions used for infinitude have coprime initial term and modulus; Dirichlet's theorem supplies the asserted infinitude. They do not assert that every small even multiplier is realizable.

## 5. Exact computational spot checks

An independent pure-Python calculation, without importing the author's checker, returned:

| Check | Scope | Result |
| --- | --- | --- |
| Characters of both roots of `q²+6q−3` | All 36 primes `p≡1 mod12` below 1000 | PASS |
| Partition-to-matrix comparison | 1546 partitions of squarefree products of at most five primes from `{5,7,11,13,17,23,29,37,61}`, retaining `R≡5 mod8` and at least one selected row | PASS |
| Direct quartic local conditions | 4692 checks, both ε covers, comparing direct finite-field quartic roots/unit-square tests with the matrix row | PASS |
| Rational map | 12 primitive norm triples with `a,b≤180` in the required parity and square-class sector | PASS |
| Nonzero-row dual certificate and mixed-character example | Exact symbols, matrix multiplication, and integer products | PASS |

For `p|A`, the independent direct test enumerated all nonzero u modulo p in the quartic divided by p with `v=1`; it did not use the closed-form root-character criterion. For `p|B`, it checked both normalized valuation cases directly. These finite calculations support the universal written argument; they are not its replacement.

The result still leaves 154, 4830, and the general small-scale geometric classification unresolved.
