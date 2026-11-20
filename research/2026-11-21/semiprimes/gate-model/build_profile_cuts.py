#!/usr/bin/env python3
"""Generate exact, translation-saturated cuts from saved endpoint duals.

The finite profile filter is necessary only; survivors are not tilings.
"""
import argparse,json
from pathlib import Path


def load_cut(path):
    cert=json.loads(path.read_text())
    if 'certificate' in cert:cert=cert['certificate']
    a,b,c=cert['tile']
    if 'up_remote_weights' in cert:
        t=cert['charge_multiplier_t']
        up=[t+x for x in cert['up_remote_weights']]
        down=[t+x for x in cert['down_remote_weights']]
    else:
        up=cert['up_weights'];down=cert['down_weights']
    return (a,b,c),cert['D'],up,down


def transforms(a,b,c,D,up,down):
    # q -> rho*q multiplies phi by -a/b and psi by -b/a.
    # q -> -conjugate(q) swaps hands and preserves epsilon.
    lu=(-a*pow(b,-1,c))%c;ld=(-b*pow(a,-1,c))%c
    for k in range(6):
        sign=(-1)**k
        u=[sign*up[(pow(lu,k,c)*r)%c] for r in range(c)]
        v=[sign*down[(pow(ld,k,c)*r)%c] for r in range(c)]
        yield D,u,v
        # Reflected placement has new-down=(a/b)*old-up,
        # new-up=(b/a)*old-down, modulo c.
        yield D,[v[(a*pow(b,-1,c)*r)%c]for r in range(c)],[u[(b*pow(a,-1,c)*r)%c]for r in range(c)]


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('certificates',nargs='+',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--solutions',type=int,default=1)
    ar=p.parse_args();cuts=[];tile=None
    for path in ar.certificates:
        t,D,u,v=load_cut(path)
        if tile is None:tile=t
        assert t==tile
        cuts.extend(transforms(*tile,D,u,v))
    a,b,c=tile;d=a-b;cap=51 if c==43 else 44
    lines=[f'{c} {d} {cap} {2*c//d} {c//d} {len(cuts)} {ar.solutions}']
    for D,u,v in cuts:
        lines.extend([str(D),' '.join(map(str,u)),' '.join(map(str,v))])
    ar.out.write_text('\n'.join(lines)+'\n')
    print(json.dumps({'tile':tile,'certificates':len(ar.certificates),'transformed_cuts':len(cuts),'output':str(ar.out)}))
