# Erdős 634: nonadjacent W/beta all-scale construction

9 October 2026. Denis Paliy, research with ChatGPT assistance.

## Main result

For the tile `(uv, v²-u², v²)`, the W and beta target families have explicit tilings at **every integer scale M>=v** whenever

    0<u<v, gcd(u,v)=1, v²<u²+uv.

Equivalently, `1<v/u<(1+sqrt(5))/2`. The same positive conclusion extends to nonprimitive parameters by normalization.

The stronger sufficient test is

    Omega = uv+(v-u)*(u²+uv-v²+u+v) > 0,
    Omega in <u,v>.

This admits additional pairs outside the cone, such as `(u,v)=(6,11)`.

**Not claimed:** necessity of `M>=v`; exclusion of smaller scales; resolution of F3 14430 or the full problem; validation of the disputed beta reverse-apex proof; external peer review or priority.

## Files

* `PROOF.md`: full mathematical proof, source attributions, scope and limitations.
* `construct.py`: solver-free constructor; standard-library rational arithmetic. Supports old scale-v seeds, new residue seeds, repeated +u caps and beta attachments.
* `verify.py`: independent integer-metric/containment/area/positioned-boundary checker. No import from the constructor. Optional full pairwise check.
* `check_symbolic.py`: 39 exact symbolic identities and a 213005-seed arithmetic regression.
* `regression.py`: 21 end-to-end example constructions and separate checks.
* Three retained complete certificates: `W_8343.json`, `beta_13527.json`, `W_34814.json`.
* Exact verification reports, rejection controls, and `SHA256SUMS`.

The main proof uses the previously established triquadratic seed (credited to Beeson) and the project's positive +u cap, not its candidate nonexistence arguments.

## Reproduce

For construction and the positioned-boundary verifier, Python's standard library suffices:

```sh
python construct.py --u 5 --v 8 --m 9 --output my_W_8343.json
python verify.py my_W_8343.json
python construct.py --u 5 --v 8 --m 9 --beta --output my_beta_13527.json
python verify.py my_beta_13527.json
python construct.py --u 6 --v 11 --m 13 --output my_W_34814.json
python verify.py my_W_34814.json
```

For symbolic checks and the optional independently implemented all-pairs check, install `sympy`, `numpy`, and `numba` in your Python environment:

```sh
python check_symbolic.py
python verify.py W_8343.json --all-pairs
python verify.py beta_13527.json --all-pairs
python verify.py W_34814.json --all-pairs
python regression.py
```

`regression.py` saves progress locally in `regression_partial.json` and can resume an interrupted run. The saved final report's `last_invocation_seconds` measures its last invocation only, not the total duration across resumed runs.

The optional all-pairs check rejects inputs whose coordinate size risks overflowing its int64 determinants. The default positioned-boundary check uses Python arbitrary-precision integers.

A constructor rejection means **NOT COVERED BY THIS RECIPE**, never that the target is impossible. Generating very large scales can require substantial memory because complete unit coordinates have size proportional to the actual number of tiles. The written proof does not require expanding those lists.

## Verification scope

The explicit 8343, 13527 and 34814 certificates passed both positioned-boundary cancellation and all-pairs separation. Their respective pair counts are 34,798,653; 91,483,101; and 605,989,891.

The 21-case regression checked 358,827 tiles and 5,770,147,225 unordered pairs. It includes new examples and prior constructions as controls. The symbolic/arithmetic report distinguishes identities valid for all parameters from finite regression; no infinite claim is inferred from a finite sample.

The repository itself was not changed by producing this package.
