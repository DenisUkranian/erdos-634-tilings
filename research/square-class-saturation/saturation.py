"""A one-sided construction/exclusion module, not a full solver of Erdős 634.
YES: classical construction or a checked compressed W/beta certificate.
NO: the stated W-only congruence sector has an inert-prime obstruction.
UNKNOWN: this module has not decided the input (not a proof of an open problem).
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from arithmetic import classify
from generate import generate
from verify_geometry import check


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('N',nargs='+',type=int)
    parser.add_argument('--certificates',type=Path,
                        help='Write checked compressed W/beta certificates to this directory.')
    args=parser.parse_args()
    if args.certificates: args.certificates.mkdir(parents=True,exist_ok=True)
    results=[]
    for n in args.N:
        try:
            result=classify(n)
            if result['status']=='YES' and 'parameters' in result:
                u,v=result['parameters']
                data=generate(u,v,result['multiplier'],result['family'])
                result['geometry_verification']=check(data)
                if args.certificates:
                    path=args.certificates/f'tiling_{n}_{result["family"]}.json'
                    path.write_text(json.dumps(data,indent=2)+'\n')
                    result['certificate']=str(path)
            elif result['status']=='YES':
                result['geometry_verification']='Classical construction; no coordinate certificate generated.'
            results.append(result)
        except (ValueError,TypeError) as exc:
            parser.error(f'N={n}: {exc}')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
