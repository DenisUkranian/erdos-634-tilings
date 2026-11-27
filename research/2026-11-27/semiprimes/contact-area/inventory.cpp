// Maximal area over the one-factor grammar for a fixed six-letter multiset.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using Counts=std::array<int,6>;
using Packed=std::uint64_t;
constexpr int absent=-1000000000;
struct Block { int index,x,y,value; Packed counters; };

int main(int argc,char** argv) {
    if (argc!=11) return 1;
    int a=std::atoi(argv[1]),b=std::atoi(argv[2]),c=std::atoi(argv[3]),q=std::atoi(argv[4]);
    Counts count{},stride{},dx{},dy{},axis{},power{};
    Counts ux{1,0,-1,-1,0,1},uy{0,1,1,0,-1,-1};
    int states=1;
    Packed guard=0;
    for (int j=0;j<6;++j) {
        int k=(j+5)%6;
        count[j]=std::atoi(argv[5+j]);
        if(count[j]<0 || count[j]>=32) return 1;
        stride[j]=states;
        states*=count[j]+1;
        guard|=Packed(32)<<(6*j);
        bool low=j%2==0;
        dx[j]=low ? a*ux[j]+b*ux[k] : c*ux[j];
        dy[j]=low ? a*uy[j]+b*uy[k] : c*uy[j];
        int h=low && q==a ? k : j;
        axis[j]=h%3;
        power[j]=(h<3 ? 1 : -1)*(low ? (q==a ? b:a) : c);
    }
    std::vector<int> best(states,absent);
    best[0]=0;
    std::vector<Block> neutral;
    for (int i=1;i<states;++i) {
        int code=i,x=0,y=0;
        std::array<int,3> residue{};
        Counts used{};
        Packed packed=0;
        for (int j=0;j<6;++j) {
            used[j]=code%(count[j]+1);
            code/=count[j]+1;
            x+=used[j]*dx[j];
            y+=used[j]*dy[j];
            residue[axis[j]]+=used[j]*power[j];
            packed|=Packed(used[j])<<(6*j);
        }
        if(x==0 && y==0 && i!=states-1) continue;
        int active=-1;
        for(int k=0;k<3;++k) if(residue[k]%q) {
            if(active!=-1) { active=-2; break; }
            active=k;
        }
        if(active==-2) continue;
        int value=absent;
        for(int j=0;j<6;++j) if(used[j] && (active<0 || axis[j]==active)) {
            int prev=best[i-stride[j]];
            if(prev!=absent) value=std::max(value, prev+x*dy[j]-y*dx[j]);
        }
        if(active>=0) for (const Block& sub:neutral) {
            if(((guard+packed-sub.counters)&guard)!=guard) continue;
            int prev=best[i-sub.index];
            if(prev!=absent) value=std::max(value,prev+sub.value+x*sub.y-y*sub.x);
        }
        best[i]=value;
        if(active==-1 && value!=absent) neutral.push_back({i,x,y,value,packed});
    }
    std::cout<<best.back()<<"\n";
}
