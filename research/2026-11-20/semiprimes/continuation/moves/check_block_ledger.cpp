// Necessary formal boundary-word identities for the two primitive F2 controls.
// Build with c++ -std=c++17 -O2 check_block_ledger.cpp -o /tmp/check-blocks
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdlib>
#include <iostream>
#include <set>
#include <tuple>
#include <vector>

struct Pair { int x = 0, y = 0; };
Pair rotate(Pair v) { return {-v.y, v.x+v.y}; }
struct Profile { int cost,x,y,z,j; std::array<Pair,3> coefficient; };
using Word = std::array<int,3>;
struct Audit {
    int a,b,c,step_cost,budget,count,offset;
    long long accepted = 0;
    std::set<std::pair<int,int>> first;
    std::set<std::array<int,4>> both;
    std::vector<int> heights,chosen;
    bool signed_test;
    std::vector<int> character;
    std::vector<Profile> terms;
    std::vector<Pair> sum;
    bool found = false;

    Audit(int a0,int b0,int c0,int m,int cap,int k,bool sign):
        a(a0),b(b0),c(c0),step_cost(m-2),budget(cap),count(k),offset(2*k+1),
        heights(k),chosen(k),signed_test(sign),character(4*k+5),sum(4*k+5) {
        auto words=[&](int length) {
            std::vector<Word> res;
            for (int x=0;x*a<=length;++x)
                for(int y=0;x*a+y*b<length;++y) {
                    int left=length-x*a-y*b;
                    if(left%c==0)res.push_back({x,y,left/c});
                }
            return res;
        };
        for(auto u:words(b*(2*a+b)))for(auto v:words(a*(a+2*b))) {
            Pair l={v[0]-u[1],u[0]-v[0]+v[1]};
            Pair r={-u[2]+2*v[2],2*u[2]-v[2]};
            first.emplace(l.x,l.y);
            both.insert({l.x,l.y,r.x,r.y});
        }
        int maxnorm=budget-(count-1)*step_cost+2;
        for(int x=0;x<=maxnorm;++x)for(int y=-maxnorm;y<=maxnorm;++y) {
            int n=-a*x-b*y;
            if(n%c)continue;
            int z=n/c, cost=x+std::abs(y)+std::abs(z)-2;
            if(std::make_tuple(x,y,z)<=std::make_tuple(0,0,0)||cost>maxnorm-2)continue;
            Profile t{cost,x,y,z,0, {{{-y,x},{-z,2*z},{y-x,x}}}};
            for(int j=0;j<6;++j) {
                t.j=j;terms.push_back(t);
                for(auto& v:t.coefficient)v=rotate(v);
            }
        }
        std::sort(terms.begin(),terms.end(),[](auto t,auto u){
            return std::tie(t.cost,t.x,t.y,t.z,t.j)<std::tie(u.cost,u.x,u.y,u.z,u.j);
        });
    }

    bool valid_through(int degree) const {
        // All coefficients through this degree have received their last contribution.
        for(int d=heights.front()-1;d<=std::min(degree,-2);++d)
            if(sum[offset+d].x||sum[offset+d].y)return false;
        auto l=sum[offset-1],r=sum[offset],e=sum[offset+2],f=sum[offset+3];
        if(degree>=-1&&!first.count({l.x,l.y}))return false;
        if(degree>=0&&!both.count({l.x,l.y,r.x,r.y}))return false;
        if(degree>=2&&(e.x!=-2*e.y||e.y<1||e.y>c))return false;
        if(degree>=3&&(f.x>0||f.y<0||-a*f.x+b*f.y+c*e.y!=c*c))return false;
        for(int d=4;d<=degree;++d)
            if(sum[offset+d].x||sum[offset+d].y)return false;
        return true;
    }

    bool signed_full(int degree) const {
        Pair f=sum[offset-1],d=sum[offset],s=sum[offset+3];
        int xc=(d.x+2*d.y)/3, yc=(2*d.x+d.y)/3;
        int p=a+2*b,q=2*a+b;
        int ya=(b*(b*q-c*xc)-a*b*f.y+a*(a*p-c*yc)+b*b*f.x)/(c*c);
        int yb=(a*p-c*yc-a*ya)/b;
        int xa=f.y+ya-yb, xb=ya-f.x;
        return character[offset]==xa+xb+ya+yb && (degree<3 || character[offset+2]==s.x-s.y);
    }
    void select_terms(int idx,int spent,int start) {
        if(found)return;
        int degree=idx==count ? std::max(3,heights.back()+1) : heights[idx]-2;
        if(!valid_through(degree))return;
        if(signed_test && degree>=0 && !signed_full(degree))return;
        if(signed_test && idx>0 && (idx==count || heights[idx-1]!=heights[idx])) {
            int previous=heights[idx-1],value=character[offset+previous];
            if((previous==0&&value<=0)||(previous==2&&value>0)||
               (previous!=0&&previous!=2&&value!=0))return;
        }
        if(idx==count) {
            
            found=true;
            std::cout<<"witness cost "<<spent;
            for(int i=0;i<count;++i) {
                auto t=terms[chosen[i]];
                std::cout<<" (h,j,x,y,z)="<<heights[i]<<","<<t.j<<","<<t.x<<","<<t.y<<","<<t.z;
            }
            std::cout<<"\n";
            return;
        }
        int h=heights[idx], available=budget-spent-(count-idx-1)*step_cost;
        for(int p=start;p<int(terms.size());++p) {
            auto& t=terms[p];
            if(t.cost>available)break;
            chosen[idx]=p;
            int chi=((t.j%2)?-1:1)*(t.x+t.y);
            character[offset+h]+=chi;
            for(int j=0;j<3;++j){auto& v=sum[offset+h-1+j];v.x+=t.coefficient[j].x;v.y+=t.coefficient[j].y;}
            select_terms(idx+1,spent+t.cost,(idx+1<count&&heights[idx+1]==h)?p:0);
            for(int j=0;j<3;++j){auto& v=sum[offset+h-1+j];v.x-=t.coefficient[j].x;v.y-=t.coefficient[j].y;}
            character[offset+h]-=chi;
            if(found)return;
        }
    }
    void select_heights(int i,int low) {
        if(found)return;
        if(i<count) {
            int high=2+2*count;
            // The remaining supports need an overlap chain to the board.
            if(i>0&&low>=2) high=std::min(high,low+2);
            for(int h=low;h<=high;++h) {
                heights[i]=h;select_heights(i+1,h);
                if(found)return;
            }
            return;
        }
        bool z0=false,z2=false;
        for(auto h:heights){z0|=std::abs(h)<=1;z2|=std::abs(h-2)<=1;}
        if(!z0||!z2)return;
        if(signed_test && std::find(heights.begin(),heights.end(),0)==heights.end())return;
        std::set<int> used(heights.begin(),heights.end());used.insert(0);used.insert(2);
        for(auto it=std::next(used.begin());it!=used.end();++it)
            if(*it-*std::prev(it)>2)return;
        if(heights[0]<0&&std::count(heights.begin(),heights.end(),heights[0])<2)return;
        if(heights.back()>2&&std::count(heights.begin(),heights.end(),heights.back())<2)return;
        ++accepted;select_terms(0,0,0);
    }
};
int main(int argc,char**argv) {
    if(argc!=3 && argc!=4){std::cerr<<"usage: check-blocks 3431|5063 budget\n";return 2;}
    int n=std::atoi(argv[1]), cap=std::atoi(argv[2]);
    if((n!=3431&&n!=5063)||cap<0||cap>100)return 2;
    int a=n==3431?33:35, b=n==3431?7:13, c=n==3431?37:43, m=n==3431?10:8;
    for(int k=1;k<=cap/(m-2);++k){
        Audit test(a,b,c,m,cap,k,argc==4);test.select_heights(0,-2*k);
        std::cout<<"blocks "<<k<<", height multisets "<<test.accepted<<", admissible "<<test.found<<"\n"<<std::flush;
        if(test.found)return 0;
    }
    std::cout<<"No ledger up to total cost "<<cap<<"\n";
}
