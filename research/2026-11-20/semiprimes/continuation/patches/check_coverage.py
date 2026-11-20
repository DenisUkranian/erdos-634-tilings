"""Replay the two area bounds, their identities and all seven triple exclusions."""
from fractions import Fraction
from json import loads
from math import gcd, isqrt
from pathlib import Path
from notch_check import verify

HERE=Path(__file__).resolve().parent
controls={3431,5063,19367,60023,64367,271151,641591}
found=set()
total=0
for u in range(6,801,2):
    for v in range(1,u,2):
        g=gcd(3,u-v)
        if gcd(u,v)>1 or u<=4*v*(v-1 if g==3 and v%3==2 else v):
            continue
        a,b,c=(u*u-v*v)//g,v*(2*u+v)//g,(u*u+u*v+v*v)//g
        assert a>b and c>3*b
        N=(a+2*b)*(2*a+b)
        missing=[]
        for copies in [1,2]:
            r,s,t=(c-b)//copies,(c-a)//copies,(a-b)//copies
            k=r-b
            M=t*t-k*k+2*(a-s)+1
            assert all(i%copies==0 for i in (c-b,c-a,a-b))
            missing.append(copies*M)
            if copies==2:
                assert g*g*(3*a*b-4*M)==(8*(3*v*v-g)*u*u+4*g*u*v+3*v**3*(2*u-v)+4*g*(4*v*v-g))
                assert 4*M<3*a*b
        assert 3431*missing[0]<=206*N and 3431*missing[1]<=336*N
        if N in controls:
            assert not (a>4*b and isqrt(b)**2==b and isqrt(a+5*b)**2==a+5*b)
            found.add(N)
        total+=1
assert found==controls
print(f'Checked both coverage bounds through u=800 on {total} odd residual shapes; all seven triples fail the exact square test.')
for path in sorted(HERE.glob('*.json')):
    data=loads(path.read_text())
    count,holes,(_,_,size)=verify(data)
    print(f'{path.name}: triangle {count}; {count-holes*size} placed; {holes} equal hole(s) of {size}.')

# Check the displayed sharp positivity identities as polynomial identities.
# Their left and right sides have degree at most four, so five evaluations suffice.
for x in range(10,15):
    H=(x*x+4*x+1)*(2*x*x+2*x-1)
    num2=Fraction(3*x*(x-4)*(2*x+1),2)+6*(2*x*x-x-4)+18
    num1=(x-3)*(x-1)*(2*x+1)+6*(x*x-x-3)+9
    w=x-10
    assert 2*(336*H-3431*num2)==3*w*(448*w**3+13298*w*w+128725*w+404100)
    assert 206*H-3431*num1==w*(412*w**3+11678*w*w+108425*w+326412)
print('Both sharp-limit polynomial identities checked.')
