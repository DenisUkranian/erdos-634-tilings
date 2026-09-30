#!/usr/bin/env python3
"""Replay the supplementary tests; this is not a full-problem certificate."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess,sys,time

def main():
    root=Path(__file__).resolve().parent;start=time.monotonic()
    for p in root.glob('*.py'):ast.parse(p.read_text(),filename=p.name)
    results={}
    for script,result in [('check_symbolic.py','symbolic_checks.json'),('check_reduction.py','reduction_checks.json'),('check_search.py','search_checks.json')]:
        print('Running '+script,flush=True)
        subprocess.run([sys.executable,str(root/script)],cwd=root,check=True,stdout=subprocess.DEVNULL)
        results[script]=json.loads((root/result).read_text())
    sources={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))}
    report={'date':'2026-09-30','result':'ALL_SUPPLEMENTARY_CHECKS_PASSED',
            'written_theorems':'PROOF.md; geometry/classification inputs are not machine-formalized',
            'mathematical_results':[
                'Squarefree N = 19 mod 24 cannot tile any triangle.',
                'Squarefree N = 35 mod 120 cannot tile any triangle.',
                'For squarefree N = 3 mod 8, 3 not dividing N, only the primitive beta scale-one norm remains.',
                'Double-angle isosceles count N=(v^2-u^2)t^2, t>=2 is necessary, not sufficient.',
                'Explicit formal boundary orientation witnesses for every Group-1 W/beta scale-one target.',
                'Explicit finite arithmetic overlist and bounded exact geometric search.'],
            'checks':results,'source_sha256':sources,
            'full_problem_solved':False,'global_finite_exception_list_proved':False,
            'candidate_all_primes_proof_used':False,'old_N105_certificates_replayed':False,
            'external_peer_review':False,'proof_assistant_formalization':False,'priority_established':False,
            'gitHub_changed':False,'emails_sent':False,'seconds':round(time.monotonic()-start,4)}
    (root/'VERIFIED_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['result']);print('Full Erdős 634 classification: not supplied by this note.')
if __name__=='__main__':main()
