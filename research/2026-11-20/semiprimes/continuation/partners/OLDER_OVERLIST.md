# Complete rows without the two later geometric exclusions

At least **67,058 of the 78,496 prime endpoints** $5\le P\le10^6$ have a complete decision for $T(PQ)$ for every prime $Q$ using the older [necessary prime-pair reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md), the small-prime rules and the unit staircase. The later moving-bank exclusions of the adjacent BQ and I120 boards are unnecessary for these rows. The second prime has no upper bound in the statement.

For mixed residues, retain the [312 residual pairs](residuals.csv) with 511 endpoints in range. For equal residues both 1 modulo 4 the classical construction decides everything. For two distinct primes $p<q$ both 3 modulo 4, the Paliy rule is exact below $2p$. If $q>2p$, retain **all** prime pairs on the older necessary list
$$
4q\in\{p^2+6p+1,\ 3p^2+6p-1,\ p^2+6p-3\}.
$$
A pair meeting the endpoint bound always has $p\le10^6$. These polynomials yield 11,838 distinct distant pairs. They account for 10,997 distinct endpoints within the bound. Exactly 70 also occur among the 511 mixed endpoints. This leaves $78496-10997-511+70=67058$ endpoints with complete rows. Some retained distant pairs also have independent small-count exclusions. The figure is a lower bound obtained without selectively removing those pairs.

Run `python3 classify.py 7 47 --older-overlist` to see how the proof dependencies change a particular answer. To replay the count, run the following commands in this directory. The C++ program sieves all primes through a million and checks every candidate partner by trial division through its square root. The greatest proposed partner is below $10^{12}$. The endpoint calculation was also checked using a separate Python implementation with SymPy.

```sh
c++ -std=c++17 -O2 check_older_overlist.cpp -o /tmp/check-prime-rows
/tmp/check-prime-rows residuals.csv
```

[Complete counts](older_overlist.txt) · [Trial-division checker](check_older_overlist.cpp).
