#!/usr/bin/env python3
"""Generate and separately verify seed, old-seed, cap and beta examples."""
import json,tempfile,time
from pathlib import Path
from construct import construction
from verify import verify

def main():
    cases=[(2,3,4,False),(3,4,5,False),(3,4,6,False),
           (4,5,8,False),(5,7,10,False),(5,8,8,False),
           (5,8,9,False),(5,8,10,False),(5,8,11,False),(5,8,12,False),
           (5,8,14,False),(5,8,19,False),(5,8,9,True),
           (4,6,9,False),(4,6,13,True),(6,11,12,False),(6,11,13,False),
           (6,11,14,False),(6,11,15,False),(6,11,16,False),(1,3,4,False)]
    store=Path(__file__).with_name('regression_partial.json')
    out=json.loads(store.read_text()) if store.exists() else [];st=time.monotonic()
    done={(r['u'],r['v'],r['m'],r['branch']=='beta') for r in out}
    with tempfile.TemporaryDirectory() as td:
        for u,v,m,beta in cases:
            if (u,v,m,beta) in done:continue
            p=Path(td)/f'{u}_{v}_{m}_{beta}.json'
            p.write_text(json.dumps(construction(u,v,m,beta),separators=(',',':')))
            r=verify(p,all_pairs=True);out.append(r);store.write_text(json.dumps(out))
            print(u,v,m,'beta' if beta else 'W',r['N'],r['status'],flush=True)
    report={'status':'PASS','cases':out,'case_count':len(out),
            'unit_tiles_checked':sum(x['N'] for x in out),
            'exact_tile_pairs_checked':sum(x['all_pairs_checked'] for x in out),
            'last_invocation_seconds':round(time.monotonic()-st,3),
            'sum_verifier_seconds':round(sum(x['elapsed_seconds'] for x in out),3),
            'scope':'finite geometric regression; not an external review or a universal proof by samples'}
    Path(__file__).with_name('regression_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
