#!/usr/bin/env python3
"""Package approximate rational points; the independent checker proves them."""
import gzip
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'research').is_dir() and (p/'scripts').is_dir())
SOURCE=ROOT/'research/2026-11-21/semiprimes/global-closure-next/five-block-two-heights/N5063_NATIVE_215_RATIONAL_CERTIFICATE.json.gz'


def main():
    cases=[]
    denominator=10**12
    for tag,round_index in (('two_native_balanced_fixed_full',1),('two_native_charged_long',0)):
        run=HERE/tag
        master=json.loads((run/f'master_{round_index:03d}.json').read_text())
        records=[]
        for h,(row,col,pos,neg) in enumerate(master['cells']):
            lp=json.loads((run/f'full_cell_{round_index:03d}_{h}.json').read_text())
            support=lp['floating_support']
            actual=sum(item[-1] for item in support)
            uniform=(pos+neg-actual)/(12*43**2)
            assert uniform>0
            base=round(uniform*denominator)
            increments=[]
            for x,y,j,hand,gate,value in support:
                inc=round((value+uniform)*denominator)-base
                if inc:increments.append([x,y,j,hand,inc])
            records.append({'node_row':row,'node_column':col,
                            'positive_population':pos,'negative_population':neg,
                            'gate_currents':master['finite_pool_witness']['cell_currents'][h],
                            'point_denominator':denominator,'uniform_point_numerator':base,
                            'point_increments':increments})
        cases.append({'name':'native_balanced' if master['native_col']==0 else 'native_charged',
                      'native_row':master['native_row'],'native_column':master['native_col'],
                      'cells':records})
    certificate={'tile':[35,13,43],'cases':cases,
                 'fourier_bound_source':str(SOURCE.relative_to(ROOT)),
                 'fourier_bound_source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                 'scope':'Two-cell strictly positive rational witnesses in the full periodic endpoint model for each native role in the split tree. Their individual gate currents and complete-node charge units are integral. Individual tile multiplicities are fractional; no physical placements or target tiling are asserted.'}
    encoded=json.dumps(certificate,separators=(',',':')).encode()+b'\n'
    path=HERE/'TWO_CELL_RATIONAL_CERTIFICATE.json.gz'
    path.write_bytes(gzip.compress(encoded,mtime=0))
    print(json.dumps({'file':path.name,'bytes':path.stat().st_size,
                      'increments':[[len(cell['point_increments']) for cell in case['cells']] for case in cases]},indent=2))


if __name__=='__main__':main()
