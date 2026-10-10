# Unrestricted W/beta positive tail — 9 October 2026

**Main result:** for every coprime 0<u<v, the fixed tile
(uv,v²-u²,v²) tiles its W and beta targets at every integer scale M>=v.
No bound on v/u is needed. The core is a new three-macro positive
partition with clipped width `u*K+v²*(w-1-j)`.

**Not the complete Erdős 634 solution.** No claim that M>=v is necessary.
Small W/beta scales and the separate F3 instance 14430 remain unclassified
by this result. The reverse-apex prime-case candidate is not a premise.

Read `PROOF.md` first. `construct.py` uses exact rational arithmetic;
`verify.py` is a separate verifier retained unchanged from the preceding
package. It does not import the constructor. The ordinary grids, old
scale-v seed and +u collar are credited prior inputs; the new code is the
three-macro residue seed.

## Reproduce

Python 3.10+ is sufficient for unit construction and the default exact
boundary verifier. SymPy is required for symbolic checks. NumPy and
Numba are optional, used only for the second all-unordered-pairs check.

    python check_symbolic.py
    python construct.py --u 2 --v 5 --m 6 --output test.json
    python verify.py test.json --all-pairs
    python regression.py

The regression takes longer than the basic boundary checks. To run the
independent metric, containment, area and complete boundary checks without
the additional all-pairs pass:

    python regression.py --skip-all-pairs

`construct.py` has a default 2000000-unit export limit. A refused large
export is not a negative mathematical answer. The proof supplies a finite
recipe for every admitted input regardless of export resources.

The complete retained examples have 1656, 2556, 27504 and 34272 tiles.
Their reports, the 22-case regression, 46 symbolic identities and 14
symbolic positivity checks are included. No external review, Lean
formalization or research-priority claim is made.

GitHub was not modified in this turn. The result is saved as this local
reproducible package.
