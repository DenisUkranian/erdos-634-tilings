# Fresh literature audit and an exact overlap obstruction

8 October 2026. This audit found no inspected external theorem that closes
the unresolved general small-scale tiling conditions. It did obtain the
[complete obstruction](CLASS15_NO_W_F3.md): no member of square class 15 can
be realized in W or F3, although all `15m²` with `m>=4` are realized in other
branches. The proof includes an elementary two-isogeny descent and exact
modular checks, and received a separate internal mathematical review.

This disproves covering the *whole positive set* by W, F3, and finitely many
individual counts. It does not disprove keeping other known infinite sectors
and then attempting to reduce only the still-unresolved remainder to W/F3.
The F1/minus-norm coefficient correspondence remains arithmetic; this audit
obtained no geometric if-and-only-if transfer between their tilings.

## Primary-source checks made in this turn

| Source | Identity checked on 8 October | Consequence |
|---|---|---|
| [Harries, progress634.tex](https://github.com/jphme/math-problems/blob/main/progress634/progress634.tex) | Current blob `85536aabe013ad393e33985cbfcadbae50722f08`, dated 28 August 2026; unchanged from the previous audit | The constructive transfers and finite multiplier windows are already incorporated. The windows fix the ordered tile and target; they do not classify the union over all primitive tiles. |
| [Zhang, 2512.22696](https://arxiv.org/abs/2512.22696) | Current version v4, 4 April 2026 | The published record still distinguishes constructions from the conjecture that they exhaust the counts. No later version supplies the missing converse. |
| [Beeson, 1206.2229](https://arxiv.org/abs/1206.2229) | Current version v4, 25 September 2026 | The current version expressly retracts necessity of `K | M²` and leaves the W and base-beta prime exclusions open. Older exact spectra depending on that necessity are not usable. |
| [Beeson, 2607.19572](https://arxiv.org/abs/2607.19572) | Current version v2, 24 September 2026, withdrawn | The record identifies the faulty Lemma9. Its abstract cannot be imported as a valid proof. |
| [Beeson, Triangle Tiling V, 1206.2228](https://arxiv.org/abs/1206.2228) | Version v2 withdrawn27 May2024; author identifies incorrect Theorem1 and the error onp8 line4 | Search indexes still display its2012 Lemma13 excluding equilateral60. That old claim is not a sound shortcut or an independently valid prior-proof attribution here. |
| [Bonfioli paper](https://github.com/ElVec1o/erdos_634_proof/blob/main/paper/erdos-634.tex) and [README](https://github.com/ElVec1o/erdos_634_proof/blob/main/README.md) | Paper blob `b7a471881297a7cb0e44dc80ae3f65df60e8e076`, README blob `1b7466eedb7bf258b266325f72f4d4037f99f056` | The current detailed scope still states that the base-beta wall/configuration attachment is missing. Conditional local theorems do not establish that every tiling presents the required configuration. |
| [Cremona, Algorithms for Modular Elliptic Curves](https://johncremona.github.io/book/fulltext/chapter3.pdf), §3.6 | Author-hosted text inspected, especially pp.84–85 and formula (3.6.2) | Supplies the standard two-isogeny descent formula used by our fully worked class-15 calculation. |
| [LMFDB class900.g data](https://www.lmfdb.org/EllipticCurve/Q/data/900.g) | Exact curve `[0,0,0,0,125]`, Cremona900b1 / LMFDB900.g4, rank0 and torsion2 | Independent external consistency check; the proof does not depend on the table. |

## An attribution correction found in the full Bonfioli source

The current Bonfioli paper, immutable commit
`4bb61193bafa4471f7ba3a35324ae0f70bd2177c`, lines 2056–2062 and 2155–2160, already **reports
an exclusion of 60**, including an 853,731-node exhaustion of the equilateral
side-30 target with tile `(5,3,7)` and separate elimination of its other
branches. It reports agreement between two engine implementations. Those
external trees were not replayed in this audit, so we distinguish the source's
claim from our own independently certified proof. Our complete structural
and positional proof of60 must therefore be described as an independent
proof, not as the first exclusion. The same manuscript still lists135 and154
among its unresolved counts, at lines2297–2301.

The manuscript also reports exclusions of14 and56, including the corrected
W56 branch. The [separate56 audit](BONFIOLI_56_AUDIT.md) records the exact
remaining candidates, mathematical source review, a completed original
equilateral56 replay, the W14 GMP cross-check, and the still-incomplete W56
replay. The latter distinction matters for a proposed complete square-class14
classification.

## Counts versus fixed-tile constructions

The new beta368 certificate must not be presented as the first realization
of count368. Beeson's standard W construction already gives that count with
`(u,v)=(3,4)`, tile`(12,7,16)`, target`(256,276,112)`, and scale`v=4`:
`(2v²-u²)v² = 23*16 = 368`. The beta certificate instead realizes368 with
tile`(6,5,9)` and target`(108,108,184)`. Its useful contribution is completing
the missing even starting scale in that fixed-tile beta family.

The candidate audit for224 and240 found no corresponding construction in
the inspected prior families. In particular, the existence of an arithmetic
theta candidate is not a sufficient condition. Zhang's published equilateral
construction for`(3,5,7)` supplies the old tail fromm=9; it does not contain
the new equilateral m=4 seed. These checks support the modest wording
“new to this investigation”; they do not establish exhaustive priority.

Exact candidate lists for14,56,224,368,240 are saved in
`attribution_candidate_gate.json`.

The public [Erdős634 page](https://www.erdosproblems.com/634) and its
[forum thread](https://www.erdosproblems.com/forum/thread/634) returned HTTP403.
Searches of both available indexes and a fresh GitHub repository search were
also made. These limitations prevent any claim to have read all current forum
comments or to have exhausted the literature.

The source-specific dependency audit in
[the prior literature note](../../final-synthesis-oct7/LITERATURE.md) remains
relevant. The old note's numerical status of154 has been superseded by the
subsequent complete exclusion; that does not change its source analysis.

## Parallel independent verification

[SAT_AUDIT.md](SAT_AUDIT.md) audits the signed endpoint-row to CNF translation
used in the new135 investigation. The algebra and auxiliary-variable namespace
check pass; an independent Glucose3 replay also passes37,871 small assignments.
This is separate from the required proof of pool completeness and independent
DRAT verification, and is not itself a decision of135.
