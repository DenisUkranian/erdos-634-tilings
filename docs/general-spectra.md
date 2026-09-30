# Necessary spectra and explicit sufficient multipliers

The [proof](../research/general-spectra/PROOF.md), [PDF](../research/general-spectra/paper.pdf), [generator](../research/general-spectra/build_certificate.py), and [separate checker](../research/general-spectra/verify_certificate.py) are published together.

For a primitive integer tile with sides a,b,c, irrational alpha/pi and gamma=60° or 120° opposite c, an equilateral target necessarily has side **S=abm** and count **N=abm²**, with positive integral m. The normalized direction values have the parity of N; their half-sum gives the divisibility without a squarefree assumption.

For a 120° tile, the F1 target has necessary count **b(a+b)m²** and the isosceles base-alpha target has necessary count **b(a+2b)m²**. These spectra are credited to Bonfioli; the note supplies a short half-difference derivation rather than claiming first discovery.

Writing A=max(a,b), B=min(a,b), explicit constructions cover all m≥3(floor(A/B)+2) for the 120° equilateral case and all m≥3(floor(A/B)+1) for the 60° equilateral case. The 120° F1/isosceles cases inherit the same bound by gluing. The smaller multipliers are **not** thereby decided.

The exact (45,32,67) example uses multiplier 9, target side 12960 and 116640 tiles. It contradicts necessity of the displayed cutoff 12 in the literal Conjecture 2 of Zhang's inspected v4. It does not refute the sufficient theorem, determine the optimum cutoff, or establish a new globally admissible integer.

The expanded coordinate file is generated from the small macro-certificate. Its **uncompressed** SHA-256 is `86710b7ea51c174e070bf1cc4cda6860815f9e9c790529008caca53d49bf0f23`. Gzip headers may differ between executions without changing that coordinate stream. Full quadratic pairwise testing of all small triangles was not run; disjointness follows from the macroregion intersections and explicit standard subdivisions.

Attribution, source-version limitations and the distinction between finite tests and universal proofs are in the manuscript. The [full-solution roadmap](full-solution-roadmap.md) explains the unresolved quantifiers.
