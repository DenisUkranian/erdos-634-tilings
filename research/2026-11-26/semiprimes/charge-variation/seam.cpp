// Exact necessary torus test for the first charged axial-leaf equality.
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using namespace std;
using Pt = pair<int,int>;
Pt add(Pt p, Pt q){ return {p.first+q.first,p.second+q.second}; }
Pt sub(Pt p, Pt q){ return {p.first-q.first,p.second-q.second}; }
int mod(int a,int s){return (a%s+s)%s;}

using Triangle=array<Pt,3>;
long long cross(Pt a,Pt b,Pt c){
    Pt u=sub(b,a),v=sub(c,a);
    return 1LL*u.first*v.second-1LL*u.second*v.first;
}
Triangle triangle(Pt p, Pt q, Pt r){
    assert(cross(p,q,r));
    if(cross(p,q,r)<0) swap(q,r);
    return {p,q,r};
}
bool contains(const Triangle& t,Pt p){
    for(int i=0;i<3;++i) if(cross(t[i],t[(i+1)%3],p)<0)return false;
    return true;
}
bool separated(const Triangle& t,const Triangle& u){
    for(int i=0;i<3;++i){
        bool outside=true;
        for(Pt p:u) if(cross(t[i],t[(i+1)%3],p)>0) outside=false;
        if(outside)return true;
    }
    return false;
}
struct Residues {
    int y4=-1, y0=-1, x5=-1, diag=-1;
    uint64_t starts4=0, starts0=0;
};
bool bind(int& field,int value){
    if(field>=0 && field!=value) return false;
    field=value; return true;
}
bool mark(uint64_t& mask,int x){
    uint64_t bit=uint64_t(1)<<x;
    if(mask&bit) return false;
    mask|=bit; return true;
}
struct Check {
    int a,b,c,l;
    array<Pt,5> move;
    array<int,5> available;
    vector<int> word;
    long long leaves=0,pass=0,disjoint=0,stripPass=0;
    Check(int A,int B,int C,int L):a(A),b(B),c(C),l(L),
        move{{{a+b,-b},{a,-a-b},{-b,-a},{c,-c},{0,-c}}},
        available{{b,l,a,l,l}},word(b+a+3*l){}
    bool necessary(Pt p,int j,Residues& r) const {
        auto [x,y]=p;
        if(j==2 && (!bind(r.y4,mod(y,a)) || !mark(r.starts4,mod(x,a)))) return false;
        if(j==0 && (!bind(r.y0,mod(y,b)) || !mark(r.starts0,mod(x,b)))) return false;
        if((j==1 || j==4) && !bind(r.x5,mod(x,a))) return false;
        int t=mod(x+y,a);
        if((j==0 || j==3) && t && !bind(r.diag,t)) return false;
        return true;
    }
    bool torus(int s) const {
        map<tuple<int,int,int>,int> current;
        auto side=[&](Pt p,Pt q){
            Pt h=sub(q,p);
            int axis=h.second==0?0:h.first==0?1:2;
            assert(axis!=2 || h.first==-h.second);
            --current[{axis,mod(p.first,s),mod(p.second,s)}];
            ++current[{axis,mod(q.first,s),mod(q.second,s)}];
        };
        Pt p={0,0};
        array<Pt,3> apex{{{a,0},{a,-a},{0,-a}}};
        for(int j:word){
            Pt q=add(p,move[j]);
            if(j<3){Pt h=add(p,apex[j]); side(p,h);side(h,q);}
            else side(p,q);
            p=q;
        }
        assert(p==Pt(b*c,-(a+b)*c));
        for(int i=0;i<c;++i){
            Pt q=add(p,{-b,a+b});
            Pt h=add(p,{-b,b});
            side(p,h);side(h,q);p=q;
        }
        assert(p==Pt(0,0));
        for(auto entry:current) if(entry.second) return false;
        return true;
    }
    bool strips() const {
        array<map<int,int>,3> jumps;
        auto side=[&](Pt p,Pt q){
            Pt h=sub(q,p);
            if(h.second==0) jumps[0][p.second]+=h.first;
            else if(h.first==0) jumps[1][-p.first]+=h.second;
            else {assert(h.first==-h.second);jumps[2][-p.first-p.second]+=h.second;}
        };
        Pt p={0,0};
        array<Pt,3> apex{{{a,0},{a,-a},{0,-a}}};
        for(int j:word){
            Pt q=add(p,move[j]);
            if(j<3){Pt h=add(p,apex[j]); side(p,h);side(h,q);}
            else side(p,q);
            p=q;
        }
        for(int i=0;i<c;++i){
            Pt q=add(p,{-b,a+b}),h=add(p,{-b,b});
            side(p,h);side(h,q);p=q;
        }
        array<int,3> counts{};
        for(int axis=0;axis<3;++axis){
            int width=0,prev=0,integral=0;
            for(auto [t,jump]:jumps[axis]){
                integral+=width*(t-prev);prev=t;width+=jump;
                bool ok=false;
                for(int i=0;i*a<=width;++i)if((width-i*a)%b==0)ok=true;
                if(!ok)return false;
            }
            if(width || integral%(a*b))return false;
            counts[axis]=integral/(a*b);
        }
        int total=counts[0]+counts[1]+counts[2];
        if(total%2 || (total+a+b+l+c)%(2*c))return false;
        for(int n:counts) if(2*n>total)return false;
        return true;
    }
    bool physical() const {
        int B=a*(a+2*b);
        Triangle board=triangle({0,0},{-b*B,-a*B},{b*c*c,-(a+b)*c*c});
        vector<Triangle> placed;
        auto append=[&](Pt p,Pt q,Pt h){
            Triangle t=triangle(p,q,h);
            for(Pt z:t)if(!contains(board,z))return false;
            for(const auto& u:placed)if(!separated(u,t)&&!separated(t,u))return false;
            placed.push_back(t);return true;
        };
        Pt p={0,0};
        for(int i=0;i<c;++i){
            Pt q=add(p,{b*c,-(a+b)*c});
            if(!append(p,q,add(p,{0,-a*c})))return false;
            p=q;
        }
        p={0,0};
        // High letters use the axial-core owner on the other bank.
        Pt high0={a*(a+b),-a*b};
        auto rotate=[](Pt z,int j){
            while(j--){z={-z.second,z.first+z.second};}
            return z;
        };
        array<Pt,5> offset{{{a*c,0},{a*c,-a*c},{0,-a*c},rotate(high0,5),rotate(high0,4)}};
        for(int j:word){
            Pt q=add(p,{c*move[j].first,c*move[j].second});
            if(!append(p,q,add(p,offset[j])))return false;
            p=q;
        }
        return true;
    }
    void visit(int left,int right,Pt p,Pt q,Residues r){
        if(left==right){
            assert(p==q);
            ++leaves;
            if(torus(a)&&torus(b)){++pass;if(physical()){++disjoint;if(strips()){
                    ++stripPass;
                    for(int token:word) cout<<token;
                    cout<<'\n';
                }}}
            return;
        }
        bool forward=left<=int(word.size())-right;
        for(int j=0;j<5;++j) if(available[j]){
            Pt start=forward?p:sub(q,move[j]);
            Residues next=r;
            if(!necessary(start,j,next)) continue;
            --available[j];
            word[forward?left:right-1]=j;
            if(forward) visit(left+1,right,add(p,move[j]),q,next);
            else visit(left,right-1,p,start,next);
            ++available[j];
        }
    }
    void run(){
        visit(0,word.size(),{0,0},{b*c,-(a+b)*c},{});
        cout<<c<<" "<<leaves<<" "<<pass<<" "<<disjoint<<" "<<stripPass<<endl;
    }
};
int main(){Check(33,7,37,3).run();Check(35,13,43,5).run();}
