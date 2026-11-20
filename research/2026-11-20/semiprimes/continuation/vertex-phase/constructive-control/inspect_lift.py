from pathlib import Path
import sys
s=Path('lift_macro.py').read_text();s=s[:s.index('res=milp(')]
exec(compile(s,'lift_macro.py','exec'))
parametric=next(iter(sp.linsolve((M,rhs),vars)))
for v in sizes:print(v,'=',sp.factor(parametric[vars.index(v)]))
