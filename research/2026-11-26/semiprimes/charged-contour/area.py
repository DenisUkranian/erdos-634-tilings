"""Bound the charged terminal's tile count using oriented shoelace accumulation."""
from functools import lru_cache
import subprocess

import numpy as np

from geometry import det
from grammar import restrict_edges


def ints(values):
    return np.asarray(values,dtype='<i4').tobytes()


def indices(mask):
    packed = mask.to_bytes((mask.bit_length()+7)//8,'little')
    return np.flatnonzero(np.unpackbits(np.frombuffer(packed,dtype=np.uint8),bitorder='little'))


def positions(mask, ind):
    data = np.unpackbits(np.frombuffer(mask.to_bytes((int(ind[-1])+8)//8,'little'),dtype=np.uint8),
                         bitorder='little')
    return np.flatnonzero(data[ind])


def encode(rules, displacements, offsets, a, c):
    records = []
    for node,terms in enumerate(rules,7):
        records.extend((offsets[node],len(terms)))
        for i,j in terms:
            cross = det(displacements[i],displacements[j])
            assert cross % (a*c)==0
            records.extend((i,j,cross//(a*c)))
    return ints(records)


def evaluate(binary, bytecode, rules, shifts, edges, active):
    sites = indices(active)
    header = [ints((len(sites),len(rules)+7)), ints(sites)]
    for shift,mask in zip((*shifts,0), [*restrict_edges(edges,shifts,active),active]):
        support = positions(mask,sites)
        header.extend([ints((shift,len(support))),ints(support)])
    out = subprocess.run([binary],input=b''.join(header)+bytecode,stdout=subprocess.PIPE,check=True)
    values = np.frombuffer(out.stdout,dtype='<i4')
    assert len(values)==len(sites)
    return sites,values


def select(sites, keep):
    bits = np.zeros(int(sites[-1])+1,dtype=np.uint8)
    bits[sites[keep]]=1
    return int.from_bytes(np.packbits(bits,bitorder='little').tobytes(),'little')
