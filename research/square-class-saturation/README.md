# Erdős 634: constructive square-class saturation

Read [PROOF.md](PROOF.md) for the mathematical statements and dependency boundary, or [README_RU.md](README_RU.md) for the Russian explanation.

For squarefree d whose odd primes are 1 or7 modulo8, a fixed W tile constructs every d*m² for m≥2d (kernels1 and2 are classical). A companion negative-norm test supplies beta constructions. There is a sharper computable C<2d. On the W-only sector d≡14 modulo16, 3∤d, gcd(m,6)=1, this gives an exact all-tile tail criterion. It is **not a complete solution** of Erdős634. No external review or priority is claimed.

## Reproduce without third-party packages

Python3.10 or newer:

```sh
python run_checks.py
python saturation.py 1694 38686 215822 342698 13310 154
python saturation.py 1694 --certificates output
```

Only `run_checks.py --output verification.json` refreshes the committed regression report and example JSON files. A plain run does not refresh the saved report or example files. All scripts use explicit checks rather than assertions that optimization could disable.

The geometric verifier is a separate implementation that imports neither the generator nor the arithmetic classifier. It verifies the entire compressed-grid dissection with exact rational arithmetic. This separation is not a claim of independent human refereeing or formal verification. Individual tiles in large grids are not enumerated.

YES means a known classical construction or a verified generated W/beta certificate. NO is restricted to the global inert-prime obstruction in the precise W-only sector. UNKNOWN means this module has not decided the input; other modules or the literature may have an answer. In particular, this program is not intended to replace the earlier complete QP generator or the earlier exact-sector filters.

`manifest.json` records SHA-256 for the package files except itself. `verify_manifest.py` checks them without modifying anything. Source citations and attribution are in the proof. Only the specifically required previous proof is included, not every artifact in the research project. No repository write or external submission occurs when these programs run.
