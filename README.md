# Erdős Problem 634 — How many congruent triangles can tile a triangle?

[Erdős problem 634](https://www.erdosproblems.com/634) asks which integers $N$ can occur when a triangle is cut into $N$ congruent triangles. The pieces may be reflected, and one edge may meet several shorter edges.

[Project page with the 280-triangle dissection](https://denisukranian.github.io/erdos-634-tilings/).

**What happens if you keep the tile?** Fix any triangular tile and let the outside triangle vary. Apart from finitely many exceptions, every possible count belongs to one of finitely many families $Ck^2$, and every member of those families occurs. The proof builds large triangles from two smaller tilings of the same shape. The remaining problem is to describe the counts when the tile can vary too. [Proof and example](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/structural/FIXED_SHAPES.md).

**The 280-tile example.** A triangle with sides 90, 90 and 140 can be tiled by 280 copies of the triangle with sides 6, 5 and 9. This fills the last gap for the counts $70m^2$, which occur exactly when $m≥2$. [Picture, coordinates and both checks](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/positive280/README.md).

The project records 141 positive and 142 negative decisions through 283. Its next undecided count is 284. A separate arithmetic result decides an infinite set of inputs with a large prime factor. [Results and sources](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/README.md) · [Large-prime theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/a837eb58e837132734342a53b889aade5cad723b/research/2026-11-19/structural/PROOF.md) · [Earlier work](RESULTS_INDEX.md).

Denis Paliy, with ChatGPT assistance. The new results are shared for review. [Reproduction guide](REPRODUCIBILITY.md) · [Status](STATUS.md) · [Citation](CITATION.cff) · [Software license](LICENSE) · [Documentation license](LICENSE-DOCUMENTATION.md).

**Задача Эрдёша №634.** Для каких чисел $N$ найдётся треугольник, который можно разрезать на $N$ равных треугольников? В репозитории есть чертежи разбиений, координаты плиток и код для проверки примеров.

See also Denis Paliy’s work on [Erdős Problem 506, the minimum number of circles determined by planar points](https://github.com/DenisUkranian/erdos-506-circles).
