# Triangle tilings, 19 November 2026

An exact construction settles the 280 row in Beeson §14.3 and the remaining case of $70m^2$. The census now reaches 283. The updated research note also gives a gluing theorem for every fixed triangular tile. [Current note and replay instructions](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/README.md) · [280-tile picture](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/positive280/README.md) · [Gluing proof](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/structural/FIXED_SHAPES.md).

<details>
<summary>Earlier snapshot through 279, with the original checks</summary>

Erdős problem 634 asks which positive integers occur as the number of congruent triangles in a dissection of some triangle. The results below combine cited earlier theorems with new computer-assisted exclusions. The new computations were developed with ChatGPT assistance. Separate implementations and integer certificates were checked within this project. External peer review and Lean verification of the new exclusions are outstanding. [Problem statement](https://www.erdosproblems.com/634).

| Scope | Result | Proof or data |
|---|---|---|
| All triangles, \(1\le N\le279\) | 139 counts occur and 140 are excluded, including the trivial positive count 1. The extension uses Bonfioli's theorem through 200 and the geometric exclusions at 231 and 236. | [Individual decisions and sources](next/global/CENSUS_279.md) · [machine-readable table](next/global/census279.json) |
| All triangles, \(N=236\) | Excluded. The only surviving arithmetic candidate is a \(250,250,472\) triangle with tile \(9,20,25\). Exact conservative tests rule out every way to fill its apex. | [Geometric argument](next/beta/CERTIFICATE_236.md) · [standalone source and certificate](next/beta/Erdos634-N236-certificate.zip) |
| Tile \(6,5,9\), target \(15t,15t,10t\) | Exactly the integer scales \(t\ge7\). The first example uses 245 tiles. | [Both directions](next/theta6/SPECTRA.md) · [exclusion at \(t=6\)](next/theta6/PROOF.md) |
| Tile \(3,8,9\), target \(72g,72g,136g\) | Exactly the integer scales \(g\ge2\). The first example uses 544 tiles. The \(g=1\) instance was a test case in Beeson §14.3. As an unrestricted numerical count, \(136=10^2+6^2\) is realizable. | [Both directions](next/theta6/SPECTRA.md) · [integer certificate for \(g=1\)](next/alpha136mesh/PROOF.md) |
| Tile \(6,5,9\), target \(45g,45g,70g\) | \(g=1\) is excluded and every integer \(g\ge3\) works. At the time of this snapshot the only undecided scale was \(g=2\), corresponding to 280. | [Geometry of 280](next/alpha280mesh/README.md) · [proof for complete straight seams](next/alpha/VERTEX_SEAMS.md) |

The placement reduction for \(N=280\) showed that any dissection must be asymmetric and have no full straight segment of tile edges joining a vertex to the opposite side. A segment starting at the apex would force either a piece of area \(810/7\) in tile units or a tiling of the excluded \(90,90,60\) target. The tests permit T-junctions, rotations, reflections and arbitrary real translations. The exact finite reduction for 280 leaves 1,000,898 individually possible tile placements after vertex and contact tests. Whether 280 of them can cover the target jointly remains undecided. The classifications are for the specified tile and target shape. The general problem remains open.

Bonfioli's notch and unit extension give the positive theta cases. The new step in the first exact threshold is the negative certificate at scale six. The second threshold uses Bonfioli's scale necessity, the positive theta construction and the new scale-one exclusion. Beeson and Paliy are credited in the cited sources for the earlier gluing and eventual-existence results. [Pinned sources for 245, 288 and 544](next/positive/SOURCES.md) · [Bonfioli's release 6.0](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex).

## Paliy's September result and Beeson's November revision

In [the September 29 construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/0730aafe18109b70ef356a7bab4c6acc959b0c89/docs/two-piece-construction.md), Denis Paliy gave the two-piece construction and the count criterion for a target with angles \((2\alpha,\alpha,2\beta)\). The first piece uses Beeson's earlier triquadratic tiling. For a fixed primitive positive integral tile \((a,b,c)\), with opposite angles \((\alpha,\beta,\gamma)\) and \(3\alpha+2\beta=\pi\), the counts are precisely \(j^2(b+c)(b+2c)\) for positive integral \(j\). Theorem 15 of Beeson v6 gives the constructive direction. Theorem 18 gives the converse and includes the normalized coloring number \(M=j(b+c-a)\). The two examples have \(322=126+196\) and \(897=368+529\) tiles. Vico Bonfioli subsequently found another 322-tiling, shown in Figure 29. [Beeson §11.3](https://arxiv.org/html/1206.2229v6#S11.SS3) · [§11.6](https://arxiv.org/html/1206.2229v6#S11.SS6) · [Figure 29, §15](https://arxiv.org/html/1206.2229v6#S15).

Just before Table 6, §16 still presents \(N=322\) as undecided. §§11.3 and 11.6 establish existence, including \(s=2/3,M=8\). The universal wording about undecided cases in §1 should also be narrowed. The limitation in §11.2 applies to the first construction. Appendix A associates Theorems 15 and 18 with the names <code>TriangleTiling.ThreeAlpha.existencePaliy</code> and <code>TriangleTiling.ThreeAlpha.Paliy</code>. As of 19 November, neither declaration was found in the inspected public main/v1.0 snapshot. Their Lean types and proofs could not be independently replayed from that snapshot. The author's report of formalization, the September construction and the computer checks in this supplement have separate provenance. [§16](https://arxiv.org/html/1206.2229v6#S16) · [Appendix A](https://arxiv.org/html/1206.2229v6#A1) · [inspected Lean revision](https://github.com/mjbeeson/TriangleTiling3Lean/tree/69ae049fb8cafd8aff9c326d3c8d86048f5495c9).

## Reproduction

From the repository root, run the quick verification with Python 3.9 or later. It recomputes the finite table, checks the positive coordinates for 240, 264, 322 and 897, checks the exact weight bounds for the 136 and 180 targets, and checks the 277-tile packing and local corner choices for 280.

~~~sh
python3 research/2026-11-19/verify.py
~~~

The two heavier checks regenerate the 236 obstruction and the full candidate list for the 180-tile target. They require a C++20 compiler named <code>g++</code>, Python 3 and GMP with development headers. Their reference traces and integrity checks are included.

~~~sh
python3 research/2026-11-19/verify.py --rebuild-236
python3 research/2026-11-19/next/theta6/reproduce.py --rebuild
~~~


</details>
