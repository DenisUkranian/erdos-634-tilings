#!/usr/bin/env python3
"""Compare the C++ partial-inventory filter with an integer Python reference."""
import json,random,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent

def reference(groups):
    used=[i-11 for i,g in enumerate(groups) if sum(g)]
    lo=min([0]+used);hi=max([0]+used)
    if sum(map(sum,groups))>154 or hi-lo>4:return False
    for K in range(max(3,hi-lo+1),6):
      for L in range(max(1-K,hi-K+1),min(0,lo)+1):
        U=L+K-1;states={(0,0):0}
        for h in range(L,U+1):
            new={};g=groups[h+11]
            for (p,w),old in states.items():
                if h==U and w!=(1 if U==0 else 0):continue
                for q in ([0] if h==U else range(-13,14)):
                    u=(-8 if h==0 else 0)+w-13*q
                    v=(-7 if h==0 else -13 if h==1 else 0)-w+13*p
                    required=sum(g)+abs(u-g[0]+g[1])+abs(v-g[2]+g[3])
                    possible=[n for n in range(24 if h==0 else 26,155,13) if n>=required and (n-u-v)%2==0]
                    if not possible:continue
                    total=old+possible[0]
                    if total<=154 and total<new.get((w,q),10000):new[w,q]=total
            states=new
        if states:return True
    return False

def full_groups(witness):
    G=[[0]*4 for _ in range(23)]
    for block in witness:
        h=block['h'];n=block['n'];g=G[h+11];population=0
        for key,offset,flip in [('A',2,1),('B',0,-1)]:
            for j,x in enumerate(block[key]):
                signed=flip*((-1)**j)*x
                g[offset+(signed<0)]+=abs(x);population+=abs(x)
        extra=n-population;assert extra>=0 and extra%2==0
        g[2]+=extra//2;g[3]+=extra//2
    return G

def main():
    controls=[r for r in json.loads((HERE.parent.parent/'closure-position-oct7/oct8-structural/all_height_direction_probe.json').read_text())['records'] if 'witness' in r]
    cases=[[[0]*4 for _ in range(23)]]+[full_groups(r['witness']) for r in controls]
    rng=random.Random(634154)
    for original in cases[1:].copy():cases.append([[rng.randrange(x+1) for x in g] for g in original])
    for _ in range(12):
        g=[[0]*4 for _ in range(23)]
        for j in range(rng.randrange(30,160)):g[11+rng.randrange(-3,4)][rng.randrange(4)]+=1
        cases.append(g)
    g=[[0]*4 for _ in range(23)];g[0][0]=1;cases.append(g)
    expected=[reference(g) for g in cases]
    code='#include "inventory_completion.hpp"\n#include <iostream>\nint main(){int n;std::cin>>n;while(n--){erdos154_inventory::Groups g{};for(auto& a:g)for(auto& x:a)std::cin>>x;std::cout<<erdos154_inventory::completion(g)<<"\\n";}}\n'
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        tmp=Path(tmp);src=tmp/'main.cpp';binary=tmp/'check';src.write_text(code)
        subprocess.run(['g++','-std=c++17','-O2','-I',str(HERE),str(src),'-o',str(binary)],check=True)
        inp=str(len(cases))+'\n'+'\n'.join(' '.join(str(x) for g in case for x in g) for case in cases)+'\n'
        result=subprocess.run([str(binary)],input=inp,text=True,capture_output=True,check=True)
        got=[bool(int(s)) for s in result.stdout.split()]
    assert got==expected
    assert all(got[:11]) # empty, five full inventories, five subinventories
    out={'status':'PASS','cases':len(cases),'formal_completion_true':sum(got),'formal_completion_false':len(got)-sum(got),'full_Erdos634_solved':False,'scope':'Strengthened C++ partial signed-inventory filter vs direct-enumeration Python reference, all full-support extensions allowed', 'central_floor':24, 'nonzero_floor':26, 'support_lengths':[3,5], 'N154_decided':False}
    (HERE/'inventory_completion_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O.')
    main()
