# Congruent triangle dissections, 19 November 2026

Erdős problem 634 asks which positive integers occur as the number of congruent triangles in a dissection of some triangle. The results below combine cited earlier theorems with new computer-assisted exclusions. The new computations were developed with ChatGPT assistance. Separate implementations and integer certificates were checked within this project. External peer review and Lean verification of the new exclusions are outstanding. [Problem statement](https://www.erdosproblems.com/634).

| Scope | Result | Proof or data |
|---|---|---|
| All triangles, 1 ≤ N ≤ 283 | 141 counts occur and 142 are excluded. Decisions through 279 use Bonfioli's theorem through 200 and the geometric exclusions at 231 and 236. The four additions are YES, YES, NO, NO at 280–283. | [Frozen decisions through 279](next/global/CENSUS_279.md) · [extension](structural/census_extension.py) · [280 witness](positive280/README.md) |
| All triangles, \(N=236\) | Excluded. The only surviving arithmetic candidate is a \(250,250,472\) triangle with tile \(9,20,25\). Exact conservative tests rule out every way to fill its apex. | [Geometric argument](next/beta/CERTIFICATE_236.md) · [standalone source and certificate](next/beta/Erdos634-N236-certificate.zip) |
| Tile \(6,5,9\), target \(15t,15t,10t\) | Exactly the integer scales \(t\ge7\). The first example uses 245 tiles. | [Both directions](next/theta6/SPECTRA.md) · [exclusion at \(t=6\)](next/theta6/PROOF.md) |
| Tile \(3,8,9\), target \(72g,72g,136g\) | Exactly the integer scales \(g\ge2\). The first example uses 544 tiles. The \(g=1\) instance was a test case in Beeson §14.3. As an unrestricted numerical count, \(136=10^2+6^2\) is realizable. | [Both directions](next/theta6/SPECTRA.md) · [integer certificate for \(g=1\)](next/alpha136mesh/PROOF.md) |
| All triangles, N = 70m² | A tiling exists exactly for positive integers m ≥ 2. All these counts are attained with the same (5,6,9) tile and board sides (45m,45m,70m). | [Both directions, exact coordinates and two verifiers](positive280/README.md) |

At 281 the classical construction uses 16² + 5². For 282 = 6·47 the squarefree-cofactor large-prime theorem applies since 4·47 > 3·6² + 6·6 − 1 and 47 has odd valuation. At 283 the prime theorem of Beeson and Roşu excludes the count. The first outstanding count in this project is 284. [Earlier large-prime test, §3](continuation/RESULTS.md) · [Prime theorem](https://arxiv.org/abs/2607.23453v4).

[Large prime factors and delayed square classes](structural/PROOF.md) gives an arithmetic equivalence on a sector of natural density (log 2)/4, and a lower density estimate for kernels whose first positive multiplier grows as a power of the kernel. [Gluing theorem](structural/FIXED_SHAPES.md) constructs all sufficiently large multiples of the gcd of two attained scales for every fixed triangle and tile. Allowing all real scales gives at most three square-multiple families for two fixed shapes. For one fixed tile and arbitrary triangular targets there are finitely many such families and finitely many omissions. The explicit 280 witness and these deductions were obtained with AI assistance. Internal mathematical and computational checks are documented; external review of these contributions is pending.

Bonfioli's notch and unit extension give the positive theta cases. The new step in the first exact threshold is the negative certificate at scale six. The second threshold uses Bonfioli's scale necessity, the positive theta construction and the new scale-one exclusion. Beeson and Paliy are credited in the cited sources for the earlier gluing and eventual-existence results. [Pinned sources for 245, 288 and 544](next/positive/SOURCES.md) · [Bonfioli's release 6.0](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex).

## Paliy's September result and Beeson's November revision

In [the September 29 construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/0730aafe18109b70ef356a7bab4c6acc959b0c89/docs/two-piece-construction.md), Denis Paliy gave the two-piece construction and the count criterion for a target with angles \((2\alpha,\alpha,2\beta)\). The first piece uses Beeson's earlier triquadratic tiling. For a fixed primitive positive integral tile \((a,b,c)\), with opposite angles \((\alpha,\beta,\gamma)\) and \(3\alpha+2\beta=\pi\), the counts are precisely \(j^2(b+c)(b+2c)\) for positive integral \(j\). Theorem 15 of Beeson v6 gives the constructive direction. Theorem 18 gives the converse and includes the normalized coloring number \(M=j(b+c-a)\). The two examples have \(322=126+196\) and \(897=368+529\) tiles. Vico Bonfioli subsequently found another 322-tiling, shown in Figure 29. [Beeson §11.3](https://arxiv.org/html/1206.2229v6#S11.SS3) · [§11.6](https://arxiv.org/html/1206.2229v6#S11.SS6) · [Figure 29, §15](https://arxiv.org/html/1206.2229v6#S15).

Just before Table 6, §16 still presents \(N=322\) as undecided. §§11.3 and 11.6 establish existence, including \(s=2/3,M=8\). The universal wording about undecided cases in §1 should also be narrowed. The limitation in §11.2 applies to the first construction. Appendix A associates Theorems 15 and 18 with the names <code>TriangleTiling.ThreeAlpha.existencePaliy</code> and <code>TriangleTiling.ThreeAlpha.Paliy</code>. As of 19 November, neither declaration was found in the inspected public main/v1.0 snapshot. Their Lean types and proofs could not be independently replayed from that snapshot. The author's report of formalization, the September construction and the computer checks in this supplement have separate provenance. [§16](https://arxiv.org/html/1206.2229v6#S16) · [Appendix A](https://arxiv.org/html/1206.2229v6#A1) · [inspected Lean revision](https://github.com/mjbeeson/TriangleTiling3Lean/tree/69ae049fb8cafd8aff9c326d3c8d86048f5495c9).

## Reproduction

From the repository root, run the quick verification with Python 3.9 or later. It checks the frozen census through 279 and the four new decisions, replays the 280 witness in two ways, tests the large-prime bound at its finite boundary and builds example dissections for the general gluing theorem. It also replays the earlier coordinate and exclusion certificates.

~~~sh
python3 research/2026-11-19/verify.py
~~~

The two heavier checks regenerate the 236 obstruction and the full candidate list for the 180-tile target. They require a C++20 compiler named <code>g++</code>, Python 3 and GMP with development headers. Their reference traces and integrity checks are included.

~~~sh
python3 research/2026-11-19/verify.py --rebuild-236
python3 research/2026-11-19/next/theta6/reproduce.py --rebuild
~~~
