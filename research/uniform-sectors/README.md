# Erdős 634: uniform sectors and asymptotic concentration

**1 October 2026 · Denis Paliy's research project, with ChatGPT assistance**

This package contains written proofs, exact arithmetic code, and independently checked constructive certificates. It does **not** solve the complete all-integer problem. External refereeing, formal proof verification, and first priority have not been established.

Read `RESULT_RU.md` for the Russian overview and `PROOF.md` for the complete English argument and dependency ledger.

## Results in this continuation

The main exact theorem concerns N≡6 (mod 16), 3∤N, with no prime p≡7 (mod 8) occurring to an odd exponent. On this domain, N is a tiling count if and only if it has the constructive form

    N = (2v²−u²)(3v²−u²)t²,  0<u<v, gcd(u,v)=1, t≥1.

Equivalently, finite factor pairs satisfy N=t²QP, gcd(Q,P)=1, 3Q<2P<4Q, and P−Q and 2P−3Q are integer squares. An additional Legendre-symbol partition test enlarges this domain; a surviving local partition is not a sufficiency claim.

A uniform negative consequence is

    2p m² is impossible whenever p is prime, p≡19 (mod 24), and gcd(m,6)=1.

The global theorem states that all tiling counts outside two specified difference-of-squares isosceles branches form a density-zero set. The arithmetic envelope of those two remaining branches has density

    3/4 − 9/(2π²) = 0.29405467360948… .

Thus the upper density of all admissible counts is at most this value. This is **not** a statement that 70.59% of the research task is complete, nor a point-by-point classification of all but finitely many integers.

Positive certificates include N=2006 and N=22·248599631². The second has an odd multiplier prime to 6. It is verified as a five-block grid dissection, without expanding approximately 1.36×10¹⁸ tiles.

## Run the complete finite suite

Use Python 3.10 or later. No third-party packages or network access are needed.

```bash
python run_checks.py --output verification.json
```

The suite checks exact arithmetic, exhaustive modular residue tables, independent parameter/factor enumeration, necessary local tests, the primitive norm parametrization, the exact arithmetic-envelope identity, macrogeometry, invalid-certificate rejection, the fully expanded 2006 construction, and the elliptic-curve witness.

Finite checks supplement the universal proofs; they do not establish unbounded claims by extrapolation.

## Use the exact arithmetic module

```bash
python arithmetic_sectors.py 22 38 950 2006 17542 154
```

`YES` is accompanied by parameters for the constructive QP family. `NO` is returned only within a proved negative domain. `NOT_COVERED` means that this module does not answer that input; it must never be read as `NO` or as a statement about the full literature. In particular, neither 105 nor 154 is answered here.

The factorization implementation uses exact trial division. It terminates, but it is not intended for arbitrarily large difficult-to-factor inputs.

## Verify a supplied geometric certificate

```bash
python verify_macro.py construction_2006.json
python verify_macro.py construction_17542.json
python verify_macro.py construction_22_large.json
python check_expanded.py construction_2006.json
```

`verify_macro.py` does not import the generator or the arithmetic sector solver. It checks tile-side congruence of unit cells, positive integer grid sizes, all macroregion containment and pairwise intersections, and exact area coverage. Together these certify a finite formula for the entire dissection. Arbitrary T-junctions are permitted.

`check_expanded.py` separately expands the modest-sized example, checks every triangle and every unordered tile pair with exact integer geometry. Its default 5,000-tile limit prevents accidental expansion of the enormous example; that limit is a safety guard, not a mathematical exclusion.

To create another QP certificate:

```bash
python generate_macro.py --help
```

For the elliptic witness:

```bash
python elliptic_witness.py --output elliptic_witness_report.json
```

This computes one rational point and its triple exactly. It makes no claim about elliptic rank, the smallest possible count in square class 22, or completeness of rational-point enumeration.

## Provenance: what is new here and what was already present

The immediate inputs were the project's 30 September necessary spectra and its 29 September complete QP construction. The repository was read at commit

    50d7459bd1d3f41352630323f1c55a92e8d9b64e

of `DenisUkranian/erdos-634-tilings`.

The angular classification and rationality inputs are attributed to Laczkovich and Beeson–Zhang. Classical/right-tile restrictions are separately identified in `PROOF.md`. The equilateral divisibility and previously reproduced 120-degree cutoff/example are credited to the earlier Harries manuscript, not claimed as new here.

The new work in this package is the modulo-16 integration into an exact all-tile criterion on a stated domain, the local square-class extension and uniform negative corollaries, the global sparse-branch count/density reduction, and the exact example/verification work. No first-priority claim is made for these deductions.

The proposed scale-one W/beta proof and the all-primes candidate are **not** proof inputs. No withdrawn packing lemma, construction-specific necessary divisibility, inferred lattice, or geometric timeout is used to obtain a negative conclusion.

## Files and integrity

`MANIFEST.json` records SHA-256 hashes of the package contents. The manifest does not hash itself. Verification reports record actual local runs; they do not assert remote continuous-integration success or external review.

This package was prepared separately. No email was sent and no remote GitHub commit was made in this continuation.
