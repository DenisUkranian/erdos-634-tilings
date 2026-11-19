"""Finite part of the row 21*q after the effective large-prime bound."""
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"continuation"))
from arithmetic import prime_sieve, squarefree_parameter_rows

bound=(3*21**2+6*21-1)//4
primes=prime_sieve(bound)
arithmetic=squarefree_parameter_rows(21*bound)
candidates={q:sorted(arithmetic[21*q]) for q in primes if q not in (3,7) and 21*q in arithmetic}
assert bound==362
assert candidates=={5:["eq60","f1"],11:["eq120"],37:["f4"]}
print(json.dumps(dict(q_max=bound,finite_primes=len(primes),repeated_prime_factors=[3,7],squarefree_candidates=candidates),indent=2))
