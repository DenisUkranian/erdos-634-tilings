import sys,json,time
from pathlib import Path
from collections import defaultdict
repo=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(repo/'research/final-closure-oct8/e60-structure'))
import check_structure as base
sys.path.insert(0,str(repo/'research/final-closure-oct8/e60-inventory'))
import line_filter as line
N=14
if not __debug__:
 raise RuntimeError('Run without -O so exact assertions execute.')
started=time.monotonic();bank=defaultdict(list)
for n in range(N+1):
 for b in base.compositions(n,6):bank[n,base.signature(b,6)].append(b)
count=0;survivors=[];pattern=defaultdict(int)
for n in range(N+1):
 for a in base.compositions(n,6):
  sig=tuple(-t%7 for t in base.signature(a))
  for b in bank[N-n,sig]:
   inv=a+b;count+=1
   totals=[[0]*4 for _ in range(3)]
   for ni,edges in zip(inv,line.EDGES):
    for j,t in edges:totals[j][t]+=ni
   bad=False
   for ni,edges in zip(inv,line.EDGES):
    if not ni:continue
    bounds=[line.max_lines(tuple(totals[j]),t,10000) for j,t in edges]
    if ni>bounds[0]*bounds[1]:bad=True;break
   if not bad:
    if len(survivors)<100:survivors.append(inv)
    pattern[base.canonical(inv)]+=1
report={'N':N,'modular_count':count,'surviving_orbits':len(pattern),'surviving_inventories':sum(pattern.values()),'examples':survivors[:5],'first_orbits':list(sorted(pattern))[:10],'seconds':time.monotonic()-started}
assert count==13362 and sum(pattern.values())==12954 and len(pattern)==1176
Path(__file__).with_name('fourteen_inventory_probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('N','modular_count','surviving_orbits','surviving_inventories')}))
