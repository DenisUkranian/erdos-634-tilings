# Local descent certificates for odd triangle-tiling multipliers

This package implements the necessary F3 cover obstruction and the two uniform count-exclusion families proved in [local-descent-obstructions.md](../../docs/local-descent-obstructions.md). It uses exact integers, modular arithmetic, and deterministic trial division. It does not compute ranks or Mordell–Weil bases.

## Interfaces and scope

```bash
python local_obstructions.py f3 434
python local_obstructions.py count 1302 3
python local_obstructions.py predicate 37
python run_checks.py
```

Commands print JSON and are read-only by default. An explicit `--report PATH` writes the same JSON. Run without Python's `-O` option; the regression checker deliberately rejects it.

The Python interfaces are `odd_f3_sieve(k)`, `classify_count(d,m)`, and `prime_family_predicate(p)`.

| Operation | Required input | Possible result |
|---|---|---|
| Generic odd-F3 sieve | Positive even squarefree `k` | `NO_ODD_F3` or `INCOMPLETE` |
| Two-family count decision | Positive squarefree `d`, positive integer `m` | `NO` or `NOT_COVERED` |
| Prime-family predicate | Prime `p ≡ 13 (mod 24)` | Exact Boolean residue predicate |

The generic sieve concerns **only the F3 branch with an odd coefficient multiplier**. A surviving cover is not asserted globally or locally soluble. `INCOMPLETE` never means a tiling exists. A generic F3 exclusion alone does not exclude every tiling branch.

The count classifier returns `NO` only when `m` is odd and one of these proved hypotheses holds:

1. `d=6R`, where `R>1` is a squarefree product of an even number of distinct primes, all congruent to 7 modulo 24.
2. `d=30p`, where `p` is prime, `p≡13 (mod 24)`, and
   
   \[
   3^{(p-1)/4}\equiv5^{(p-1)/2}\pmod p.
   \]

Every recognized family decision includes a complete F3 cover certificate. The remaining branch exclusions use the mathematical proof linked above: the existing exhaustive reduction leaves only alpha, QP, and F3 for squarefree `d>6`, `d≡6 (mod16)` and odd `m`; the family-specific elementary arguments exclude alpha and QP. These classification and geometry inputs are not replaced by a finite test.

Even multipliers return `NOT_COVERED`. Valid inputs outside the two hypotheses, including the failed prime predicates at `p=13` and `p=61`, also return `NOT_COVERED`. No positive count classification or eventual-multiplier threshold is implemented here. Trial division and cover enumeration terminate, but can be expensive for large inputs or many prime factors.

## What each cover certificate proves

For `k=sf(3d)`, an odd F3 witness requires a rational point on

\[
E'_k:y^2=x^3+6kx^2-3k^2x
\]

with `v₂(x)=1`. Its squareclass is a signed even squarefree divisor `D` supported on `3k`. Writing `x=D(u/v)²` in lowest terms gives the necessary integral cover

\[
Z^2=D u^4+6k u^2v^2-\frac{3k^2}{D}v^4,
\qquad\gcd(u,v)=1.
\]

The report explicitly lists **every** such signed cover. `NO_ODD_F3` is returned only when every cover has a killing certificate.

The first tests enumerate primitive projective residues modulo `2^7` and `3^4`. Over `p^e`, every primitive pair has either `u` a unit, in which case normalize to `(1,v)`, or `u` divisible by `p` and `v` a unit, in which case normalize to `(u,1)`. Scaling by a unit preserves the square condition because the polynomial is homogeneous of degree four. This remains valid for negative `D` and when `3|k`.

At odd primes `p|k`, `p>3`, the package uses two compressed finite modular obstructions:

- If `p∤D`, and both `D` and `−3D` are nonresidues, the unit-`u` chart is impossible modulo `p`. In the other primitive chart, dividing the equation by `p²` gives another nonsquare modulo `p`. The combined certificate therefore excludes primitive solutions modulo **`p³`**, not merely `p²`.
- If `p|D`, put `δ=D/p`, `κ=k/p`. The divided bracket must vanish modulo `p`; its two-variable reduction is controlled by `t²+6t−3`. A nonsquare 3, or two roots in the wrong squareclass relative to `δκ`, excludes primitive solutions modulo `p²`. The report retains the exact discriminant/root/Legendre residues.

Survival of these necessary conditions is not asserted sufficient. The public APIs reject odd or nonsquarefree `k`, invalid signed cover classes, and nonpositive or nonintegral count inputs.

## Retained verification

[verification.json](verification.json) contains complete cover reports for 19 kernels, including 380 independently replayed killing certificates. The checker independently enumerates all primitive residue pairs for the small-modulus certificates, checks the odd-prime certificates with direct square-residue sets and divided polynomials, and reconstructs the full signed cover universe independently. Dropped covers and corrupted modular counts are rejected.

The controls include:

- Genuine primitive cover solutions for `k=2,114,330`; the `k=330` controls include a negative `D` and ramification at 3.
- Seven positive primitive F3 coefficient witnesses with **odd** multipliers, generated from small norm triples; none is excluded. The small generation bound is used only for controls.
- The distinction between modulus `p²` and `p³`, checked explicitly at `k=14,D=−2,p=7`.
- The positive-rank point `(-471,73947)` on `E'₁₅₇₀`, associated with `d=4710`. Its double has nonintegral coordinate on an integral short Weierstrass model, giving an exact Nagell–Lutz nontorsion certificate. Thus the odd obstruction is compatible with positive rank.
- The primitive F3 triple `(159711,13889,167089)` with coefficient `1302·8660²`. Its multiplier is **even**, and the count classifier correctly leaves it outside its scope. This is an arithmetic coefficient witness; small-scale geometric realization is not asserted.
- Both prime-predicate outcomes, eight family exclusions, eleven scope controls, and sixteen rejected invalid inputs.

All files are covered by [SHA256SUMS.txt](SHA256SUMS.txt). To regenerate the retained report explicitly:

```bash
python run_checks.py --report verification.json
```

The rank-positive and even-multiplier controls prevent the local obstruction from being misreported as an empty square class, a rank-zero theorem, or a complete solution of Erdős problem 634.
