# Triangle tilings, 19 November 2026

**Two results.** One fixed triangular tile can produce only finitely many families of counts $Ck^2$, with finitely many missing values, even if the outside triangle may take any shape. An explicit example answers the “280?” in Beeson's §14.3. The drawing and all 280 exact coordinates are public. [Gluing proof](structural/FIXED_SHAPES.md) · [280-tile dissection](positive280/README.md) · [Beeson’s table](https://arxiv.org/html/1206.2229v6#S14.SS3).

| Question | Answer and evidence |
|---|---|
| Which counts $70m^2$ occur? | Exactly those with $m≥2$. Bonfioli excluded 70. The new dissection gives 280. Bonfioli's construction and Paliy's gluing give every $m≥3$. [Derivation and checks](positive280/README.md) |
| How far does the project classify every count? | Through 283, with 141 positive and 142 negative answers. The next undecided count here is 284. [Through 279](next/global/CENSUS_279.md) · [280–283](structural/census_extension.py) |
| What about the 136 row in Beeson §14.3? | A $(72,72,136)$ board cannot be tiled with the $(3,8,9)$ tile. At integer board multiples $g≥2$, tilings exist. The number 136 itself occurs with a different tile since $136=10^2+6^2$. [Fixed-shape proof](next/alpha136mesh/PROOF.md) · [All scales](next/theta6/SPECTRA.md) |
| Are there other infinite results? | A large-prime criterion gives an equivalence on an arithmetic sector containing a subset of natural density $(\log 2)/4$. A second result bounds how late square classes can start. [Statements and dependencies](structural/PROOF.md) |
| Which other geometric exclusions enter the census? | The 236 certificate excludes its only candidate board. For tile $(6,5,9)$ and target $(15t,15t,10t)$ the allowed integer scales are exactly $t≥7$. [236 certificate](next/beta/CERTIFICATE_236.md) · [Theta proof](next/theta6/SPECTRA.md) · [Positive cases and attribution](next/positive/SOURCES.md) |

## A decision test for one input

For any specified $N$, normalize two outside vertices to $(0,0),(1,0)$ and write the third as $(u,v)$ with $v>0$. Introduce three counterclockwise vertices for each tile. Require them to lie in the outside triangle, give each tile determinant $v/N$, and require the same three squared side lengths up to permutation. For each pair of tiles, ask for a line with nonzero normal that puts their vertices on opposite closed sides. A separating line exists exactly when their open interiors are disjoint. These requirements are finite polynomial equalities and inequalities with integer coefficients after clearing $N$. Equal total area and containment give coverage, including the boundary by closure. Effective quantifier elimination therefore returns yes or no for each input. This gives decidability. The arithmetic classification as the tile varies is still open. [Basu, survey of effective quantifier elimination](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf) · [Beeson’s computational discussion](https://arxiv.org/html/1206.2229v6#S16).

## Paliy's September result and Beeson's November revision

In [the September 29 construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/0730aafe18109b70ef356a7bab4c6acc959b0c89/docs/two-piece-construction.md), Denis Paliy gave the two-piece construction and the count criterion for a target with angles \((2\alpha,\alpha,2\beta)\). The first piece uses Beeson's earlier triquadratic tiling. For a fixed primitive positive integral tile \((a,b,c)\), with opposite angles \((\alpha,\beta,\gamma)\) and \(3\alpha+2\beta=\pi\), the counts are precisely \(j^2(b+c)(b+2c)\) for positive integral \(j\). Theorem 15 of Beeson v6 gives the constructive direction. Theorem 18 gives the converse and includes the normalized coloring number \(M=j(b+c-a)\). The two examples have \(322=126+196\) and \(897=368+529\) tiles. Vico Bonfioli subsequently found another 322-tiling, shown in Figure 29. [Beeson §11.3](https://arxiv.org/html/1206.2229v6#S11.SS3) · [§11.6](https://arxiv.org/html/1206.2229v6#S11.SS6) · [Figure 29, §15](https://arxiv.org/html/1206.2229v6#S15).

Immediately before Table 6, §16 still describes \(N=322\) as undecided. §§11.3 and 11.6 establish existence, including \(s=2/3,M=8\). The universal wording about undecided cases in §1 should also be narrowed. The limitation in §11.2 applies to the first construction. A minimal replacement for the obsolete example is “Figure 13 in §11.3 gives the 322-tiling with $s=2/3$ and $M=8$.” Appendix A associates Theorems 15 and 18 with the names <code>TriangleTiling.ThreeAlpha.existencePaliy</code> and <code>TriangleTiling.ThreeAlpha.Paliy</code>. As of 19 November, neither declaration was found in the inspected public main/v1.0 snapshot. Their Lean types and proofs could not be independently replayed from that snapshot. The author's report of formalization, the September construction and the computer checks in this supplement have separate provenance. [§16](https://arxiv.org/html/1206.2229v6#S16) · [Appendix A](https://arxiv.org/html/1206.2229v6#A1) · [inspected Lean revision](https://github.com/mjbeeson/TriangleTiling3Lean/tree/69ae049fb8cafd8aff9c326d3c8d86048f5495c9).

## Reproduce the results

From the root of this revision, run the coordinate checks or the whole November set with ordinary Python 3.9 or later.

~~~sh
python3 research/2026-11-19/positive280/verify.py
python3 research/2026-11-19/positive280/verify_slices.py
python3 research/2026-11-19/verify.py
~~~

To rebuild the heavier 236 and 180 computations, use a C++20 compiler named `g++` and GMP development headers.

~~~sh
python3 research/2026-11-19/verify.py --rebuild-236
python3 research/2026-11-19/next/theta6/reproduce.py --rebuild
~~~

Denis Paliy directed this investigation with ChatGPT assistance. Separate exact implementations were run within the project. The new November results await external scholarly review. [Earlier results](../../RESULTS_INDEX.md) · [Assistance disclosure](../../AI_USAGE_DISCLOSURE.md).
