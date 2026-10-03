"""Polynomial/rational identity checks complementing the universal proof.

Uses exact Laurent polynomials over Q, with no external dependency.
Positivity and quantifiers are proved in PROOF.md, not by symbolic sampling.
"""
from laurent import u,v,T,Vector as V


def run():
    a,b,c=u*v,v*v-u*u,v*v;Q,P=b+c,b+2*c;D=4*v*v-u*u
    p=V(a,0);w=V(-u*P/(2*v),b/(2*v))
    r=V(u*Q/(2*v),u*u/(2*v));s=V(-u*b/(2*v),b/(2*v))
    k,h,q=u*v,u*(v-u),u*u
    O=V(0,0);K=V(u*v**3,0);R=r*b;J=(r+s)*h;C=K+p*h;E=R+s*h
    L0=h*b;B=E-V(L0,0)
    norm=lambda z:z[0]**2+D*z[1]**2
    det=lambda z,t:z[0]*t[1]-z[1]*t[0]
    identities={}
    def scalar(name,expression):
        assert not expression,(name,expression)
        identities[name]=True
    def vector(name,left,right):
        for i in range(2):scalar(name+f'[{i}]',left[i]-right[i])
    for name,z,length in [('p',p,a),('w',w,c),('r',r,a),('s',s,b),
                          ('r+s',r+s,c),('p+w',p+w,b)]:
        scalar('length:'+name,norm(z)-length**2)
    scalar('grid_det_rs',det(r,s)-u*b/2)
    scalar('grid_det_pw',det(p,w)-u*b/2)
    vector('p+w=s',p+w,s);vector('R=K+qw',R,K+w*q)
    vector('E=C+kw',E,C+w*k);vector('B_simple',B,V(u*u*b/2,u*b/2))
    vector('J_on_OB',J*(v+u),B*v)
    A=(v-u)*b/v**3;F=u/v;G=u*u*(v-u)/v**3
    vector('R_barycentric',R,K*A+E*F+O*G)
    scalar('barycentric_sum',A+F+G-1)
    scalar('bottom_length',C[0]-L0-u*u*Q)
    scalar('left_leg',norm(B)-(u*v*b)**2)
    scalar('right_leg',norm(E-C)-(u*v*c)**2)
    scalar('b_minus_h',b-h-v*(v-u))
    scalar('cap_count',k*k+3*h*h+2*(b-h)*h+2*h*q-u**4-2*u*v*b)
    L=u*Q*T-L0
    scalar('strip_decomposition',L-a*v*T-b*u*(T-v+u))
    scalar('collar_count',u**4+2*u*v*b+2*L-Q*((T+u)**2-T*T))
    apex=V(u*b*(T+u)/2,b*(T+u)/2)
    outer=V(u*Q*(T+u),0);inner_right=B+V(u*Q*T,0)
    vector('left_homothety',B*(T+u),apex*(T+u)+(O-apex)*T)
    vector('right_homothety',inner_right*(T+u),apex*(T+u)+(outer-apex)*T)
    scalar('outer_left_length',norm(O-apex)-(v*b*(T+u))**2)
    scalar('outer_right_length',norm(outer-apex)-(v**3*(T+u))**2)
    M=lambda z:V((-u*z[0]+D*z[1])/(2*v),(-z[0]-u*z[1])/(2*v))
    e1,e2=M(V(1,0)),M(V(0,1))
    scalar('isometry_e1',norm(e1)-1)
    scalar('isometry_e2',norm(e2)-D)
    scalar('isometry_dot',e1[0]*e2[0]+D*e1[1]*e2[1])
    z=V(-v*Q/2,-u*v/2);cv=V(-b*Q/(2*v),u*b/(2*v))
    z2=z+V(u*u/(2*v),u/(2*v))*P
    vector('beta_collinearity',(z2-z)*Q,(cv-z)*P)
    vector('canonical_left',M(O-apex),cv*(T+u))
    vector('canonical_right',M(outer-apex),z*(T+u))
    scalar('beta_side_z2',norm(z2)-v**6)
    scalar('beta_base',norm(z2-z)-(u*P)**2)
    for name,vec,side in [('0cv',cv,v*b),('0z2',z2,v*c),('cvz2',cv-z2,v*a)]:
        scalar('beta_complement:'+name,norm(vec)-side**2)
    return dict(status='PASS',symbolic_identities=len(identities),identities=identities)


if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
