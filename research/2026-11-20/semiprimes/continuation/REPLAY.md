# Reproducing this checkpoint

Run from this directory with Python 3 and assertions enabled. The geometry uses integer or rational coordinates. The squarefree census uses floating point only for the numerical approximation of its separately proved leading constant.

```sh
python3 check_simultaneous.py
python3 counting/replay_3pq.py
python3 counting/mixed_ratio.py --wide
python3 counting/verify_mixed_ratio.py 199/100  # optional second method, requires SymPy
python3 patches/check_coverage.py
python3 patches/notch_check.py
python3 notches/check_cone_threshold.py
python3 notches/check_near_threshold.py
python3 notches/verify_control.py
python3 paths/check_upper_rigidity.py
python3 paths/check_upper_odd_formula.py
python3 paths/verify_cut_currents.py
python3 paths/verify_phase.py
python3 paths/verify_paths.py
python3 check_squarefree_mass.py
python3 check_sector.py
python3 dilations/double_exceptional.py
python3 dilations/extract.py
```

The [pentagon decision](patches/decision/PENTAGON_SWEEP.md) and [quadrilateral decision](notches/NOTCH_ENUMERATION.md) contain compiler options, coverage arguments and positive controls. The [older 231 verifier](https://github.com/DenisUkranian/erdos-634-tilings/tree/6c0a28e1902062ef661413427560960e210dc693/research/2026-11-19/nov19/equilateral231/cert) was compiled anew from the deposited C++ source. Both previously generated binary traces were read to completion. Arithmetic enumeration checks the claimed support of candidate shapes. Geometric nonexistence additionally uses the reductions given in the proofs.

## The simultaneous criterion and an actual four-prime positive control

```text
3pq <= 3000000: 139667 prime pairs, 14 F2 inputs, 8 Paliy triples, zero overlaps.
Four-prime positive control: N=132542399 (147 verified grids), triple=397627197.
```

## The seven F2 test inputs and exact pentagon coordinates

```text
Checked both coverage bounds through u=800 on 1563 odd residual shapes; all seven triples fail the exact square test.
hexagon_3431.json: triangle 3431; 3183 placed; 1 equal hole(s) of 248.
hexagon_5063.json: triangle 5063; 4235 placed; 2 equal hole(s) of 414.
pentagons_3431.json: triangle 3431; 3095 placed; 2 equal hole(s) of 168.
pentagons_5063.json: triangle 5063; 4703 placed; 2 equal hole(s) of 180.
single_3431.json: triangle 3431; 3225 placed; 1 equal hole(s) of 206.
single_5063.json: triangle 5063; 4813 placed; 1 equal hole(s) of 250.
Both sharp-limit polynomial identities checked.
```

## Independent comparison of signed-path arithmetic

```text
10 1 40 40 [[(33, 0, -7), (0, 0, 0)]]
6 1 48 48 [[(35, 0, -13), (0, 0, 0)]]
12 1 168 168 [[(143, 0, -25), (0, 0, 0)]]
16 1 96 96 [[(85, 0, -11), (0, 0, 0)]]
22 1 176 176 [[(161, 0, -15), (0, 0, 0)]]
18 1 360 360 [[(323, 0, -37), (0, 0, 0)]]
40 1 560 560 [[(533, 0, -27), (0, 0, 0)]]
44 3 2200 2200 [[(1927, 0, -273), (0, 0, 0)]]
62 3 4216 4216 [[(3835, 0, -381), (0, 0, 0)]]
122 5 5368 5368 [[(4953, 0, -415), (0, 0, 0)]]
```

## Finite exact height certificates

```text
(33, 7, 37)  N=3431  n1 >= 27681846/100001,  blocks >= 8,  two heights >= 9c
(35, 13, 43)  N=5063  n1 >= 32029539/100001,  blocks >= 8,  two heights >= 9c
(85, 11, 91)  N=19367  n1 >= 100221576/100001,  blocks >= 12,  two heights >= 13c
(143, 25, 157)  N=60023  n1 >= 211583719/100001,  blocks >= 14,  two heights >= 15c
(161, 15, 169)  N=64367  n1 >= 242708167/100001,  blocks >= 15,  two heights >= 15c
(323, 37, 343)  N=271151  n1 >= 668335500/100001,  blocks >= 20,  two heights >= 21c
```

## The 3pq parameter census

```text
All 139667 squarefree products 3pq ≤ 3,000,000 with 3<p<q passed.
Primitive count-row support after adjacent BQ and defect-one I120 removal: {'BQ': 8, 'E+': 1, 'E-': 1, 'F1': 1, 'F4': 2, 'I120': 10, 'QP': 8}
The replay verifies arithmetic compatibility. Geometric exclusions and constructions are inputs.
```

## Two endpoint-certificate replays for the equilateral 231 input

```text
PASS band 0 2 verified_packed_rows 13601241 endpoint_deductions 346727411 root -7623 9240 axis 40 -7 sign -1
```

## Second 231 orientation band

```text
PASS band -1 1 verified_packed_rows 14129619 endpoint_deductions 354827395 root 0 8547 axis 0 1 sign 1
```

## The squarefree split sector

```text
X=1000000: equilateral candidates=2, F2 candidates=26, staircase=13, overlap=0, union outside staircase=15
X=100000000: equilateral candidates=16, F2 candidates=267, staircase=198, overlap=0, union outside staircase=85
X=10000000000: equilateral candidates=119, F2 candidates=2628, staircase=2277, overlap=0, union outside staircase=470
Four-line sieve counts checked directly at four forbidden primes.
```

## Independent squarefree F2 counts

```text
Local counts at seven primes and three quartic identities verified.
Unit primitive, odd squarefree, all squarefree numerical constants: 0.085049208 0.026360590 0.079081771
X=1000000 odd_only=True, all primitive distinct=28: 26 parameter pairs, 26 distinct candidates, 13 staircase realizations, 13 outside; coefficient=0.0260000
X=1000000 odd_only=False, all primitive distinct=84: 79 parameter pairs, 79 distinct candidates, 46 staircase realizations, 33 outside; coefficient=0.0790000
X=100000000 odd_only=True, all primitive distinct=285: 267 parameter pairs, 267 distinct candidates, 198 staircase realizations, 69 outside; coefficient=0.0267000
X=100000000 odd_only=False, all primitive distinct=850: 786 parameter pairs, 786 distinct candidates, 593 staircase realizations, 193 outside; coefficient=0.0786000
X=10000000000 odd_only=True, all primitive distinct=2831: 2628 parameter pairs, 2628 distinct candidates, 2277 staircase realizations, 351 outside; coefficient=0.0262800
X=10000000000 odd_only=False, all primitive distinct=8503: 7909 parameter pairs, 7909 distinct candidates, 6865 staircase realizations, 1044 outside; coefficient=0.0790900
X=1000000000000 odd_only=True, all primitive distinct=28351: 26358 parameter pairs, 26358 distinct candidates, 24340 staircase realizations, 2018 outside; coefficient=0.0263580
X=1000000000000 odd_only=False, all primitive distinct=85053: 79096 parameter pairs, 79096 distinct candidates, 73084 staircase realizations, 6012 outside; coefficient=0.0790960
```

## Verified doubled constructions

```text
4 [5, 3, 7] {'count': 572, 'regions': 19, 'pairs': 171}
7 [16, 5, 19] {'count': 3848, 'regions': 91, 'pairs': 4095}
10 [33, 7, 37] {'count': 13724, 'regions': 115, 'pairs': 6555}
13 [56, 9, 61] {'count': 35816, 'regions': 139, 'pairs': 9591}
16 [85, 11, 91] {'count': 77468, 'regions': 163, 'pairs': 13203}
19 [120, 13, 127] {'count': 147752, 'regions': 187, 'pairs': 17391}
22 [161, 15, 169] {'count': 257468, 'regions': 211, 'pairs': 22155}
25 [208, 17, 217] {'count': 419144, 'regions': 234, 'pairs': 27261}
```

## Unit-board extraction from those eight constructions

```text
u=4, unit count=143, intact unit copies=0
u=7, unit count=962, intact unit copies=0
u=10, unit count=3431, intact unit copies=0
u=13, unit count=8954, intact unit copies=0
u=16, unit count=19367, intact unit copies=0
u=19, unit count=36938, intact unit copies=0
u=22, unit count=64367, intact unit copies=0
u=25, unit count=104786, intact unit copies=0
```

## The 250-tile pentagon, with no tile fixed in advance

The independent partition-tree check covers all 16×4×8 deepest labels exactly once by the 31 terminal records, totalling 5,331,660 node visits. From patches/decision run `python3 replay_p250.py --ledger pentagon_250_unseeded.json --jobs 16` to rerun every search, check each node count and validate the partition. The [geometric proof of orientation coverage](notches/NOTCH_ENUMERATION.md) is a separate input to this exhaustive search.
