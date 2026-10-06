# A bounded split part in four 120-degree branches

6 October 2026. Internal continuation; no priority claim. This extends
the elementary factor bound of
[the F3 note](F3_SPLIT_PART_REDUCTION.md). The positive construction
tails are prior inputs, not new dissections. The remaining branches
and small geometric scales are not classified here.

Let d>=1 be squarefree, m>=1, and let h be the product of the full
p-parts of m at primes p>3 with `(3/p)=1`. Put

    d_+ = gcd(d,2) product_{p|d, p>3, (3/p)=1} p.

For a primitive tile `c²=a²+ab+b²`, define the four rows as follows.

| Row | Distinguished factor U | Coefficient D | Recover (a,b), for `1<=r<U/2` |
|---|---|---|---|
| I120, base-alpha isosceles | `a+2b` | `b(a+2b)` | `(U−2r,r)` |
| F2 | `a+2b` | `(a+2b)(2a+b)` | `(U−2r,r)` |
| F3 | `a+2b` | `3(a+2b)(a+b)` | `(U−2r,r)` |
| F4 | `2a+b` | `(2a+b)(a+b)` | `(r,U−2r)` |

These names follow the repository's
[norm-row table and constructive tails](../../docs/square-class-tails.md#appendix-a-every-integer-tails-for-all-norm-rows).
They refer to the displayed coefficient for the displayed ordered tile;
interchanging a,b is not silently identified with the same target.

For each row, form a finite list `L_row(d,h)` by enumerating
`U|d_+h²` and `1<=r<=floor((U−1)/2)`. Recover a,b from the table,
retain only `gcd(a,b)=1` and an integral square root c of the norm,
and retain only `D=ds²` with a positive integer s. The arithmetic test
for a multiplier m asks whether some entry has `s|m`.

**Theorem.** A realization of `dm²` in one of these four rows implies
its arithmetic test. Conversely, the test implies a realization in
that row whenever

    m >= 15dh³.

For d>=2 the sharper sufficient bound is `m>=12dh³`. F3 retains the
stronger bounds 8dh³ and 6dh³, respectively, proved in its separate
note. These are sufficient thresholds, not necessary lower bounds.

**Proof of necessity.** Write `dm²=Dt²` using the existing integral
scale spectrum. Squarefreeness gives `t|m` and `D=ds²` for `s=m/t`.
For either choice `U=a+2b` or `U=2a+b`, the norm modulo a prime
dividing U proves `3∤U` and `(3/p)=1` for every odd prime p|U.
The nonzero short side used as denominator is coprime to that prime.
The argument modulo 9 excluding 3 is the one in the F3 note.

The distinguished factor and the other factor in D are coprime.
For F2 their gcd divides 3, which is absent; the other rows follow
directly from `gcd(a,b)=1`. Thus every odd prime exponent in U is
`v_p(d)+2v_p(s)` and is bounded by its exponent in d_+h².

If U is even, the short side appearing with coefficient one in U is
even and hence divisible by 8. The other short side is odd. It follows
that `v_2(U)=1`, while the other factor in D is odd. Consequently
`v_2(D)=1`, so d must be even and s odd. No restriction on the parity
of m is imposed. This proves `U|d_+h²` and the stated finite list.

**Proof of sufficiency.** A retained list entry supplies a positive
primitive tile and integral scale `t=m/s`. Every row in the table has

    max(a,b)<U,    D<3U²,    U<=dh².

For `A=max(a,b)`, `B=min(a,b)`, the integer
`q=2c−2A−B>0` obeys `3B²=q(4A+2B+q)>4A`. Hence

    A/B < sqrt(3U)/2,    s < sqrt(3/d)U.

The cited positive constructions work in all four rows at every
integer scale at least `M=3(floor(A/B)+2)`. F2 and F3 in fact need
only `ceil(M/2)`, but the common bound M suffices here. Therefore

    sM <= s(3A/B+6)
        < (9/2) U^(3/2)/sqrt(d) + 6sqrt(3/d)U
        <= (9/2)dh³ + 6sqrt(3d)h²
        < 15dh³.

The last inequality uses `sqrt(3)<7/4` and h>=1. For d>=2,
`sqrt(3/d)<=sqrt(3/2)<5/4` sharpens it to `sM<12dh³`.
The applicable size bound on m therefore gives `t>=M`, proving the
claimed sufficiency.

For fixed d,h this is one finite coefficient list per row and an
ordinary size cutoff, even when the complementary factor m/h uses
arbitrarily many primes from `{2,3}` and the four nonsplitting residue
classes modulo 24. The finitely many multipliers below the cutoff
remain geometric questions if their arithmetic tests pass. No claim
is made here for the E60, E120, F1 or Group-1 rows, and no global
classification follows without separately excluding those branches.

`check_other_split_branches.py` compares each restricted list against
direct factorizations of `ds²` for `s|m`. It checks both multiplier
parities, ordered tiles, and the 2-adic factor issue explicitly. The
finite checks support the formulas; the universal statement is the
argument above.
