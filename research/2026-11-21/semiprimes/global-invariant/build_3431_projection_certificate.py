#!/usr/bin/env python3
"""Discover a rational approximate point and exact-checkable Fourier inverses."""
from pathlib import Path
import json,math
import numpy as np
HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
a,b,c=33,7,37
Q=10**12;R=10**6;DEN=10**12
roots=[(round(Q*math.cos(2*math.pi*r/c)),round(Q*math.sin(2*math.pi*r/c))) for r in range(c)]

def block(kx,ky):
    shapes=[(j,s) for j in range(6) for s in [-1,1]]
    if kx==ky==0:
        return [[complex(s*(-1)**j if s==1 else 0) for j,s in shapes],
                [complex(s*(-1)**j if s==-1 else 0) for j,s in shapes],
                [1.+0.j]*12]
    axes=[i for i in range(3) if (kx*U[i][0]+ky*U[i][1])%c]
    isup=ky%c==a*(kx*pow(-b,-1,c)%c)%c
    isdown=ky%c==-b*(kx*pow(a,-1,c)%c)%c
    out=[]
    for axis in axes:
        row=[]
        for j,s in shapes:
            uu=(-a*U[j][0],-a*U[j][1]);ww=(b*U[(j+s)%6][0],b*U[(j+s)%6][1])
            ru=roots[(kx*uu[0]+ky*uu[1])%c];rw=roots[(kx*ww[0]+ky*ww[1])%c]
            zu=complex(*ru)/Q;zw=complex(*rw)/Q
            row.append(s*((1-zu) if j%3==axis else 0)+s*((zw-1) if (j+s)%3==axis else 0))
        out.append(row)
    if isup or isdown:
        row=[]
        for j,s in shapes:
            uu=(-a*U[j][0],-a*U[j][1]);ru=roots[(kx*uu[0]+ky*uu[1])%c]
            row.append(s*(-1)**j*complex(*ru)/Q if (s==1)==isup else 0j)
        out.append(row)
    return out

blocks=[]
for kx in range(c):
    for ky in range(c):
        B=np.array(block(kx,ky));G=B@B.conj().T;inv=np.linalg.inv(G)
        C=[[[round(float(z.real)*R),round(float(z.imag)*R)] for z in row] for row in inv]
        blocks.append({'frequency':[kx,ky],'inverse_numerators':C})
old=json.loads((HERE/'N3431_NATIVE_PROFILE_IPM.json').read_text())
uniform=(3*c-old['population'])/(12*c*c);base=round(uniform*DEN)
incs=[]
for x,y,j,s,gate,v in old['support']:
    inc=round((v+uniform)*DEN)-base
    if inc:incs.append([x,y,j,s,inc])
cert={'tile':[a,b,c],'point_denominator':DEN,'uniform_point_numerator':base,'point_increments':incs,
      'root_denominator':Q,'root_numerators':roots,'inverse_denominator':R,'fourier_blocks':blocks,
      'target_population':111,'native_gate_currents':[22,15],'positive_gate_capacity':44,
      'scope':'Finite certificate for the existence of a strictly positive rational full residue-relaxation point. The witness is the exact least-norm rational correction of the supplied rational point; no physical tiling is asserted.'}
(HERE/'N3431_RATIONAL_PROJECTION_CERTIFICATE.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
print('wrote',len(blocks),'Fourier blocks and',len(incs),'point increments')
