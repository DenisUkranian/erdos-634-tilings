# Sources for the three positive endpoint constructions

The constructive statements below refer to the indicated target and tile. A numerical count alone would also admit unrelated shapes.

| Count | Unit tile | Target sides | Published construction |
|---:|---|---|---|
| 245 | \((6,5,9)\) | \((105,105,70)\) | Bonfioli's notch theorem explicitly gives \(\theta_7(2,3)\) and \(5\cdot7^2=245\). [Paper, lines 389–410](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L389-L410) · [Lean declaration, lines 121–123](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaNotch3Gen.lean#L121-L123) |
| 288 | \((3,8,9)\) | \((144,144,48)\) | The constructive direction for \(e=1\) applies at \(f=3,t=2f=6\). Here \(b=8\) and \(bt^2=288\). [Paper, lines 412–421](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L412-L421) · [Constructive Lean declaration](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaNotch4E1.lean#L59-L75) |
| 544 | \((3,8,9)\) | \((144,144,272)\) | The alpha construction with \(g=2\) adjoins to that theta triangle a scale-16 tile subdivided into \(16^2=256\) unit tiles, giving \(256+288=544\). [Paper, lines 423–431, including credit to Beeson and Paliy](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L423-L431) · [Lean declaration alphaTiled_all](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaNotch4Alpha.lean#L31-L36) |

For the 544 construction the large tile has sides \(48,128,144\), with its side of length 48 glued to the base of the theta triangle. The resulting outer base has length \(128+144=272\).

The three complete recursive Git trees below contained 5,979, 9,124 and 1,781 entries respectively. A search of witness directories and filenames found no standalone per-tile coordinate lists for these three target/shape pairs. The corresponding theorem declarations are public. The separate geometric work in this packet includes no independent coordinate-by-coordinate replay or clean Lean build for these positive cases. Paliy's [explicit theta generator](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/scripts/generate_theta.py) lists six seeds for a different unit tile. Bonfioli's paper credits Paliy's earlier eventual-existence result for the theta family. [Prior art in the paper](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L383-L388)

- [Bonfioli, erdos_634_proof, commit 119bec0](https://api.github.com/repos/ElVec1o/erdos_634_proof/git/trees/119bec0dd0158ddeb239686d5464eb7104e3b42d?recursive=1)
- [Bonfioli, erdos634_primes_and_N200, commit 7520056](https://api.github.com/repos/ElVec1o/erdos634_primes_and_N200/git/trees/752005605ca4e607d2a08f57bdc2445dd5558dbb?recursive=1)
- [Paliy, erdos-634-tilings, commit 0f7935b](https://api.github.com/repos/DenisUkranian/erdos-634-tilings/git/trees/0f7935b71fd958bd764bccf079e1e70bc68ce351?recursive=1)
