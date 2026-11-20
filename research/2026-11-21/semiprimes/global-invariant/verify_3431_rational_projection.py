#!/usr/bin/env python3
"""Exact finite certificate of rational feasibility of the full residue relaxation.

The proof uses a rational approximate point and a verified norm bound on
small Fourier blocks. The exact witness is x0 + M^dagger(b-Mx0), which is
rational; the bounds certify its positivity and all gate capacities.
Only the standard library and integer/Fraction arithmetic are used.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def add(z,w):return z[0]+w[0],z[1]+w[1]
def sub(z,w):return z[0]-w[0],z[1]-w[1]
def mul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def conj(z):return z[0],-z[1]
def ab(z):return abs(z[0])+abs(z[1])
def scale(z,k):return z[0]*k,z[1]*k

def pi_interval():
    def atan_bounds(m):
        n=20;v=sum((F((-1)**k,(2*k+1)*m**(2*k+1)) for k in range(n)),F(0))
        rem=F(1,(2*n+1)*m**(2*n+1))
        return v,v+rem
    l5,u5=atan_bounds(5);l239,u239=atan_bounds(239)
    return 16*l5-4*u239,16*u5-4*l239

def check_roots(roots,Q,c):
    lower,upper=pi_interval();mid=(lower+upper)/2
    assert F(3)<lower<upper<F(22,7)
    tail=F(22,7)**36/factorial(36)
    for r,(re,im) in enumerate(roots):
        k=r if r<=c//2 else r-c;theta=2*mid*k/c
        co=sum(((-1)**j*theta**(2*j)/factorial(2*j) for j in range(18)),F(0))
        si=sum(((-1)**j*theta**(2*j+1)/factorial(2*j+1) for j in range(18)),F(0))
        err=tail+(upper-lower)*abs(k)/c
        assert abs(F(re,Q)-co)+err<=F(1,Q),(r,'real')
        assert abs(F(im,Q)-si)+err<=F(1,Q),(r,'imag')
    return True

def block(a,b,c,kx,ky,roots,Q):
    shapes=[(j,s) for j in range(6) for s in [-1,1]]
    if kx==ky==0:
        return [[(s*(-1)**j*Q if s==1 else 0,0) for j,s in shapes],
                [(s*(-1)**j*Q if s==-1 else 0,0) for j,s in shapes],
                [(Q,0)]*12]
    axes=[i for i in range(3) if (kx*U[i][0]+ky*U[i][1])%c]
    isup=ky%c==a*(kx*pow(-b,-1,c)%c)%c
    isdown=ky%c==-b*(kx*pow(a,-1,c)%c)%c
    assert not(isup and isdown)
    out=[]
    for axis in axes:
        row=[]
        for j,s in shapes:
            uu=(-a*U[j][0],-a*U[j][1]);ww=(b*U[(j+s)%6][0],b*U[(j+s)%6][1])
            ru=roots[(kx*uu[0]+ky*uu[1])%c];rw=roots[(kx*ww[0]+ky*ww[1])%c]
            z=(0,0)
            if j%3==axis:z=add(z,sub((Q,0),ru))
            if (j+s)%3==axis:z=add(z,sub(rw,(Q,0)))
            row.append(scale(z,s))
        out.append(row)
    if isup or isdown:
        row=[]
        for j,s in shapes:
            uu=(-a*U[j][0],-a*U[j][1]);ru=roots[(kx*uu[0]+ky*uu[1])%c]
            row.append(scale(ru,s*(-1)**j) if (s==1)==isup else (0,0))
        out.append(row)
    return out

def inverse_bound(cert):
    a,b,c=cert['tile'];Q=cert['root_denominator'];R=cert['inverse_denominator'];roots=cert['root_numerators']
    assert Q>=100
    check_roots(roots,Q,c);K=0;seen=set();hist={}
    for item in cert['fourier_blocks']:
        kx,ky=item['frequency'];assert 0<=kx<c and 0<=ky<c and (kx,ky) not in seen;seen.add((kx,ky))
        B=block(a,b,c,kx,ky,roots,Q);r=len(B);hist[r]=hist.get(r,0)+1
        assert all(ab(z)<=3*Q for row in B for z in row)
        C=item['inverse_numerators'];assert len(C)==r and all(len(row)==r for row in C)
        G=[[tuple(sum(mul(B[i][k],conj(B[j][k]))[t] for k in range(12)) for t in [0,1]) for j in range(r)] for i in range(r)]
        cn=max(sum(ab(z) for z in row) for row in C)
        er=0
        for i in range(r):
            rowsum=0
            for j in range(r):
                z=(R*Q*Q if i==j else 0,0)
                for k in range(r):z=sub(z,mul(C[i][k],G[k][j]))
                rowsum+=ab(z)
            er=max(er,rowsum)
        # Each entry of the exact Gram matrix differs by at most 200/Q
        # in |Re|+|Im|; the constant follows from twelve products of
        # entries of size <=3 and entry errors <=2/Q.
        eta_num=er+cn*r*200*Q
        assert 2*eta_num<R*Q*Q,(kx,ky,'inverse residual')
        bound=(2*cn+R-1)//R;K=max(K,bound)
    assert len(seen)==c*c
    return K,hist

def point_checks(cert,K):
    a,b,c=cert['tile'];D=cert['point_denominator'];base=cert['uniform_point_numerator'];nt=12*c*c
    vals=[base]*nt
    def col(x,y,j,s):return ((x*c+y)*6+j)*2+(s==1)
    seen=set()
    for x,y,j,s,inc in cert['point_increments']:
        assert 0<=x<c and 0<=y<c and 0<=j<6 and s in [-1,1]
        ix=col(x,y,j,s);assert ix not in seen;seen.add(ix);vals[ix]+=inc
    small=min(vals);assert small>0
    gb=3*c*c;population_row=gb+2*c;curr=[0]*(population_row+1);pbins=[0]*(2*c)
    def row(axis,x,y):return (axis%3)*c*c+(x%c)*c+y%c
    for x in range(c):
        for y in range(c):
            for j in range(6):
                for s in [-1,1]:
                    v=vals[col(x,y,j,s)];eps=s*(-1)**j
                    ux=x-a*U[j][0];uy=y-a*U[j][1];wx=x+b*U[(j+s)%6][0];wy=y+b*U[(j+s)%6][1]
                    for ax,px,py,sign in [(j,x,y,s),(j,ux,uy,-s),(j+s,wx,wy,s),(j+s,x,y,-s)]:curr[row(ax,px,py)]+=sign*v
                    gate=(a*uy-b*ux)%c if s==1 else c+(a*ux-b*uy)%c
                    curr[gb+gate]+=eps*v;curr[population_row]+=v
                    if eps>0:pbins[gate]+=v
    target=[0]*len(curr);target[gb]=22*D;target[gb+c]=15*D;target[-1]=111*D
    residue=[v-w for v,w in zip(target,curr)];res2=sum(v*v for v in residue)
    assert K*res2<small*small
    capacity=cert['positive_gate_capacity'];slack=min(capacity*D-v for v in pbins);assert slack>0
    assert (3*c)**2*K*res2<slack*slack
    return {'variables':nt,'equations':len(curr),'point_denominator':D,
            'minimum_approximate_numerator':small,'residual_squared_numerator':res2,
            'norm_bound_K':K,'positivity_inequality':[K*res2,small*small],
            'positive_gate_capacity':capacity,'minimum_gate_slack_numerator':slack,
            'gate_capacity_inequality':[(3*c)**2*K*res2,slack*slack],
            'exact_corrected_population':111,'exact_corrected_positive_population':74,
            'exact_corrected_negative_population':37,'exact_gate_currents':{'native_up':22,'native_down':15,'all_remote':0},
            'exact_node_charge_units':{'native_up':-2,'native_down':2,'all_remote':0}}

def main():
    path=HERE/'N3431_RATIONAL_PROJECTION_CERTIFICATE.json';cert=json.loads(path.read_text())
    assert cert['tile']==[33,7,37] and cert['target_population']==111 and cert['native_gate_currents']==[22,15]
    K,hist=inverse_bound(cert);point=point_checks(cert,K)
    report={'status':'PASSED','target_existence_status':'OPEN','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'root_enclosures_checked':37,'fourier_blocks_checked':1369,'block_row_counts':hist,
            'point':point,
            'conclusion':'A strictly positive rational feasible point exists in the full periodic endpoint relaxation with integer gate charges and the positive gate caps. The exact point is x0+M^dagger(b-Mx0); it is not a physical tiling.'}
    (HERE/'N3431_RATIONAL_PROJECTION_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
