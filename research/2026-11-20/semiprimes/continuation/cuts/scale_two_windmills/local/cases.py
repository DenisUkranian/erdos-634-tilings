"""Replay local obstructions for the supporting banks in the cap list."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json,subprocess,sys,tempfile
p=Path(__file__).resolve().parent

def run(entry):
    a,b,c,label,word=entry
    data=str(len(word))+'\n'+''.join('%d %d %d\n'%tuple(edge) for edge in word)
    # The checker reports OPEN rather than rejecting at arithmetic, depth or work limits.
    result=subprocess.run([exe,str(a),str(b),str(c)],input=data,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return label,result.returncode,result.stderr.strip()

if __name__=='__main__':
 with tempfile.TemporaryDirectory() as tmp:
    exe=str(Path(tmp)/'polygon_runs');subprocess.run(['c++','-std=c++20','-O2',str(p/'polygon_runs.cpp'),'-o',exe],check=True)
    jobs=[]
    for n,a,b,c in [(3431,33,7,37),(5063,35,13,43)]:
        for idx,((cap,word),where) in enumerate(json.loads((p/f'cases_{n}.json').read_text())):
            jobs.append((a,b,c,f'{n}-{idx}',word))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=[]
        for label,rc,summary in pool.map(run,jobs):
            print(label,rc,summary,flush=True);results.append(rc)
    raise SystemExit(int(any(results)))
