# Sources, provenance and redistribution

This is an original research snapshot directed by Denis Paliy, with ChatGPT assistance as described in [the disclosure](../AI_USAGE_DISCLOSURE.md). Internal reviews are separately written checks within the same project; they are not external refereeing.

## Primary sources used

- Michael Beeson, *Triangle Tiling: The Case 3α+2β=π*, [arXiv:1206.2229v4](https://arxiv.org/abs/1206.2229v4), revised 25 September 2026. Version numbers matter: some earlier necessary divisibility assertions are explicitly withdrawn. The construction comparison concerns the remark after Theorem 14; the theta correction concerns Lemma 55 and its use of Theorem 18.
- Michael Beeson, *Tilings of an Isosceles Triangle*, [arXiv:1206.1974v7](https://arxiv.org/abs/1206.1974v7).
- Michael Beeson, *Tiling an Equilateral Triangle*, [arXiv:1812.07014v3](https://arxiv.org/abs/1812.07014v3).
- Michael Beeson and Yan X. Zhang, *Rationality of certain triangle tilings*, [arXiv:2604.01314v1](https://arxiv.org/abs/2604.01314v1).
- Michael Beeson, *Tiling a triangle into a prime number of congruent triangles*, [arXiv:2607.23453v1](https://arxiv.org/abs/2607.23453v1). Only the individually identified branch calculations are used; its broad prime conclusion is not an input.
- Vico Bonfioli, [erdos_634_proof](https://github.com/ElVec1o/erdos_634_proof), including the signed-direction invariant and the companion's complete W/beta spectra for tile (2,3,4). The scale note identifies the examined snapshot and files. Known constructions and results remain credited to their source.

The [prime dependency ledger](prime-case-dependencies.md) gives the theorem-level inputs and qualifications. Primary sources, rather than a general abstract or a withdrawn whole-paper claim, determine the scope of each dependency.

## What this repository contains

The source manuscripts, figures, coordinate data and verification programs were assembled for this project. The 77, 322 and 897 certificates retain their original bytes, including historical timing metadata; replay compares their geometric payloads. New theta and boundary-collar certificates are supplied as inspectable coordinates. Checker code does not import or execute a third-party search engine.

The 48 and 108 theta seeds reproduce Beeson's construction. The mixed-strip 147 and 243 variants extend that macrogeometry. New to this investigation does not establish first discovery: no priority claim is made.

The optional Bonfioli seed checker reads an independently obtained upstream tree as data. Upstream code, coordinate files, PDFs, and material with unclear redistribution terms are not bundled. This repository also excludes private correspondence, unsent email drafts and the unrelated #506 research archive.

Original software is covered by [MIT](../LICENSE). Original prose, proofs, diagrams and other documentation are covered by [CC BY 4.0](../LICENSE-DOCUMENTATION.md). Those licenses do not relicense cited works or third-party materials. Mathematical attribution remains required independently of software licensing.
