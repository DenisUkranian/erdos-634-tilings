"""Recompute the exact two-hand census at the charged-leaf equality."""
from collections import Counter
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import tempfile

from area import encode, evaluate, select
import argparse
import gzip
import numpy as np

from currents import discover, gap, system
from geometry import chart, exact_profiles
from grammar import boolean, program, restrict_edges, shifted_program

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=24)
def instructions(profile,a,c,s,directions,shifts):
    rules, displacements = program(profile,a,c,s,directions)
    offsets = shifted_program(rules,shifts)
    return rules,offsets,encode(rules,displacements,offsets,a,c)


def one(binary,a,b,c,l,word_id,s,t,certificates,search=False):
    directions,shifts,edges,domain = chart(a,b,c,l,word_id,s,t)
    result = []
    floor = 5 if c==37 else 7
    for idx,profile in enumerate(exact_profiles(a,b,c,directions)):
        rules,offsets,bytecode = instructions(profile,a,c,s,directions,shifts)
        active = domain
        while active:
            mask = boolean(rules,offsets,restrict_edges(edges,shifts,active),active)
            if mask==active:
                break
            active = mask
        if not active:
            continue
        if word_id==0:
            result.append([idx,None])
            continue
        while active:
            sites,values = evaluate(binary,bytecode,rules,shifts,edges,active)
            # Twice axial area / (ac) equals b times the population in c-blocks.
            viable = select(sites,values>=b*floor)
            if viable==active:
                hi = int(values.max())//b
                key=f"{c}/{word_id}/{s}/{t}/{idx}"
                if search or key in certificates:
                    matrix,rhs=system(a,b,c,l,word_id,s,t,profile,edges,shifts,active)
                    if key not in certificates:
                        proposal=discover(matrix,rhs)
                        if proposal is not None:
                            certificates[key]=[[int(i),int(proposal[i])] for i in np.flatnonzero(proposal)]
                    if key in certificates:
                        y=np.zeros(len(rhs),dtype=np.int64)
                        for i,n in certificates[key]:
                            y[i]=n
                        assert gap(matrix,rhs,y)>0
                        break
                result.append([idx,hi if hi%2 else hi-1])
                break
            active = viable
    return result


def census(binary,certificates):
    data = {}
    for a,b,c,l in [(33,7,37,3),(35,13,43,5)]:
        rows = {}
        for word_id in (0,1):
            for s in (1,-1):
                grouped = {}
                for t in range(1 if s==1 else 0,c):
                    result = one(binary,a,b,c,l,word_id,s,t,certificates)
                    grouped.setdefault(tuple(map(tuple,result)),[]).append(t)
                rows[f"{'AC'[word_id]} hand {s:+d}"] = [
                    dict(profile_and_max_odd_blocks=key, translations=val)
                    for key,val in grouped.items()]
        profiles = {}
        for s in (1,-1):
            ds,*_ = chart(a,b,c,l,0,s,0)
            profiles[str(s)] = exact_profiles(a,b,c,ds)
        data[str((a+2*b)*(2*a+b))] = dict(profiles=profiles,by_outer_word=rows,original_status="OPEN")
    return data


if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Enable Python assertions.")
    from review import controls
    with tempfile.TemporaryDirectory() as tmp:
        binary=Path(tmp)/"area"
        subprocess.run(["c++","-O3","-std=c++17",str(HERE/"area.cpp"),"-o",str(binary)],check=True)
        with gzip.open(HERE/"certificates.json.gz","rt") as stream:
            certificates=json.load(stream)
        result = census(binary,certificates)
        result["independent_checks"] = controls(binary)
    print(json.dumps(result,indent=2))
