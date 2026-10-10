# Run this validation with Python assertions enabled.
if not __debug__:
    raise RuntimeError('Run without the -O option.')
#!/usr/bin/env python3
from pathlib import Path
import json,time
from verify import Replay
from check_gate import gate
P=Path(__file__).resolve().parent
start=time.monotonic()
gates=[gate(n) for n in (14,56)]
assert not any(x['classical_witnesses'] for x in gates)
assert {(r['branch'],r['scale'],tuple(sorted(r['tile']))) for r in gates[0]['after_proved_scale_one_isosceles_exclusions']}=={('W',1,(5,6,9))}
assert {(r['branch'],r['scale'],tuple(sorted(r['tile']))) for r in gates[1]['after_proved_scale_one_isosceles_exclusions']}=={('W',2,(5,6,9)),('E120',1,(7,8,13))}
reports=[]
for filename,kind,root in [('W56proof0.json','W_short',0),('W56proof1.json','W_short',1),('E56.json','empty',0)]:
 d=json.loads((P/filename).read_text());r=Replay(d,kind,root).run();r['file']=filename;reports.append(r);print(json.dumps(r),flush=True)
result={'status':'PASS','global_56_geometric_candidates_all_refuted':True,'classification_is_external_input':True,'nodes':sum(r['nodes'] for r in reports),'terminal_contradictions':sum(r['corner_leaves']+r['boundary_leaves'] for r in reports),'reports':reports,'seconds':time.monotonic()-start,'all_small_scales_solved':False,'erdos634_fully_solved':False}
(P/'replay_report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
