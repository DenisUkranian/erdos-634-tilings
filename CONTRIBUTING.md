# Reviewing and contributing

Mathematical corrections, exact replays and alternative constructions are welcome through [GitHub issues](https://github.com/DenisUkranian/erdos-634-tilings/issues) or pull requests.

## Reviewing the prime-case candidate

Please identify the exact statement, file and step you are checking. The most useful targets include the forced triangular patch in the isosceles argument, the boundary induction and column-completion steps in the $W$ argument, and the passage from the versioned classification inputs to an exhaustive prime-count conclusion.

For a proposed counterexample or gap, state which hypotheses are being used. Reflections and T-junctions are permitted. If a boundary configuration is claimed to be impossible, explain why a tile ending in the interior of another tile's edge is excluded or accommodated.

Distinguish a local lemma check from an audit of the whole candidate. A computational success on the 322 instance does not validate a nonexistence proof.

## Replaying the construction

Include the repository commit, Python version, platform, exact command, exit code and complete output. If you use a new verifier, explain how it differs from the supplied implementations. Exact arithmetic is preferred for an affirmative geometric certificate.

Do not treat a timeout, search exhaustion under an unproved bound or floating-point visualization as a proof of nonexistence.

## Changes and provenance

Keep mathematical claims, explanatory text and checks consistent. Changes to a claimed theorem or certificate should state the previous claim, the correction and the verification scope. Retain citations and source provenance.

Contribute only material you have the right to publish. Original code contributions are expected under MIT and original research documentation under CC BY 4.0, unless a different arrangement is explicitly agreed and recorded. Do not add third-party paper PDFs, code with unresolved redistribution terms, credentials or private correspondence.

Reviewers and contributors will be credited accurately for their actual contributions. A submitted issue or a limited check is not automatically represented as endorsement of the entire project.
