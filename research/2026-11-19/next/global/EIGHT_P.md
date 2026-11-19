# The complete row of counts \(8p\)

For every prime \(p\), some triangle splits into \(8p\) congruent triangles exactly when \(p\equiv1\bmod4\) or \(p\in\{2,3,11\}\).

The usual sum-of-two-squares constructions handle \(p=2\) and \(p\equiv1\bmod4\); \(24=6\cdot2^2\) is classical. Harries' exhibited dissection supplies \(88\). Consider the remaining \(p\equiv3\bmod4,\ p>3\). The classical cases fail. In each nonclassical row the integer multiplier is 1 or 2, since its square divides \(8p\). For W, beta and both difference-of-squares families multiplier 1 is excluded. At multiplier 2 the coefficient would be \(2p\). No difference of two squares has 2-adic valuation one. An even primitive beta coefficient \(3v^2-u^2\) requires both \(u,v\) odd, so is \(2\bmod8\), whereas \(2p\equiv6\bmod8\). W multiplier 2 can produce only \(28\), which is outside this row. [Geometric inputs and W multiplier 2](../../continuation/RESULTS.md).

For the nine remaining product rows the unbalanced-prime bound of the same note, §3, excludes every \(p>(3\cdot8^2+6\cdot8-1)/4=239/4\). That portion of the proof uses the explicit positive product factorizations and primitive relation \(c^2=a^2\pm ab+b^2\); no condition on the quadratic characters of \(p\) occurs in the nine-row bound.

It remains to test \(7,11,19,23,31,43,47,59\). The exactly reproduced primitive-product overlist is:

| \(p\) | \(8p\) | Product rows, before geometric decisions |
| ---: | ---: | --- |
| 7 | 56 | equilateral 120°, \((a,b,c)=(7,8,13)\) up to their exchange |
| 11 | 88 | F4, \((3,5,7)\) |
| 23 | 184 | isosceles 120°, \((7,8,13)\) |
| 19, 31, 43, 47, 59 | 152, 248, 344, 376, 472 | empty |

All surviving product shapes have multiplier 1. The complete classification through 200 excludes 56 and 184 and includes 88. This proves the assertion. It uses that classification for two negative geometric inputs. [Bonfioli, Theorem 1.3 and attribution for 88](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/README.md) and [standalone exact enumeration](check.py).
