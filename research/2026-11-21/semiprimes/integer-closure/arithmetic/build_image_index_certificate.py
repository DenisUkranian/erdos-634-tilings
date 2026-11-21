#!/usr/bin/env python3
"""Find small exact full-rank determinant certificates of the gate image."""
from collections import defaultdict
from itertools import combinations
import json
import gzip
from math import gcd
from pathlib import Path

from probe_integer_image import eliminate
from probe_full_kernel_image import generators,feature

HERE=Path(__file__).resolve().parent


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def build(a,b,c):
    kernels,keys=generators(a,b,c)
    # Delete the negative-population row. The identity Qup+Qdown=P-N
    # makes this an integral coordinate chart on the compatible targets.
    rows=[{} for _ in range(2*c+1)]
    for k,kernel in enumerate(kernels):
        for r,v in feature(kernel,a,b,c).items():
            if r<len(rows):rows[r][k]=v
    result=eliminate(rows,[0]*len(rows),len(kernels),include_pivots=True)
    assert not result['divisions']
    rem=result['remaining'];assert len(rem)==3
    maps=[dict(row['coefficients']) for row in rem]
    representatives={}
    for k in sorted(set(k for row in maps for k in row)):
        pattern=tuple(row.get(k,0) for row in maps)
        representatives.setdefault(pattern,k)
    patterns=list(representatives)
    minors=[];g=0
    for indices in combinations(range(len(patterns)),3):
        determinant=det3(*(patterns[i] for i in indices))
        ng=gcd(g,determinant)
        if ng and ng!=g:
            g=ng
            selected=[representatives[patterns[i]] for i in indices]
            minors.append({'columns':[keys[p[1]] for p in result['pivot_indices']]+[keys[k] for k in selected],
                'residual_determinant':determinant})
            if g==c:break
    assert g==c
    catalogue=[];indices={}
    for minor in minors:
        entries=[]
        for kernel in minor.pop('columns'):
            key=json.dumps(kernel,separators=(',',':'))
            if key not in indices:
                indices[key]=len(catalogue);catalogue.append(kernel)
            entries.append(indices[key])
        minor['column_indices']=entries
    return {'tile':[a,b,c],'projected_rows':2*c+1,'rank':2*c+1,
        'unit_pivots':len(result['pivot_indices']),'kernel_catalogue':catalogue,'minors':minors,
        'gcd_of_absolute_determinants':g,
        'scope':'The integer span of these whole endpoint kernels has index c in the integer gate/positive-population chart. Signed coefficients are permitted.'}


def main():
    out={'cases':[build(*shape) for shape in ((33,7,37),(35,13,43))]}
    with gzip.GzipFile(filename=str(HERE/'GATE_IMAGE_INDEX_CERTIFICATE.json.gz'),mode='wb',mtime=0) as stream:
        stream.write((json.dumps(out,indent=2)+'\n').encode())
    print(json.dumps({'cases':[{k:v for k,v in case.items() if k not in ('minors','kernel_catalogue')}|{'determinants':[m['residual_determinant'] for m in case['minors']]} for case in out['cases']]},indent=2))

if __name__=='__main__':main()
