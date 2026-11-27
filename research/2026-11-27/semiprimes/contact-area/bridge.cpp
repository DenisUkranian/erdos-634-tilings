// Order-13 factor parser with the order-35 block order and a signed C level.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using Counts=std::array<int,6>;
using Packed=std::uint64_t;
constexpr int absent=-1000000000;
struct Block { int index,x,y,numberA,numberB,level; Packed counters; };

int main(int argc,char** argv) {
    if (argc != 2) return 1;
    const int bridge = std::atoi(argv[1]);
    if (bridge < -24 || bridge > 24) return 1;
    constexpr int q = 13;
    const Counts count{17,2,23,4,24,3};
    const Counts dx{48,0,-35,43,-13,43}, dy{-13,43,48,0,-35,-43};
    const Counts axis{0,1,2,0,1,2}, power{35,43,35,43,-35,-43};
    Counts stride{};
    int states = 1;
    Packed guard = 0;
    for (int j=0; j<6; ++j) {
        stride[j] = states;
        states *= count[j]+1;
        guard |= Packed(32) << (6*j);
    }
    std::vector<int> slot(states,-1);
    using Levels=std::array<int,49>;
    std::vector<Levels> profiles;
    Levels empty; empty.fill(0);profiles.push_back(empty);slot[0]=0;
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
        int A=used[0]+used[5],B=used[1]+used[2];
        int level=used[4]-6*used[3];
        Levels value; value.fill(absent);
        for(int j=0;j<6;++j) if(used[j] && (active<0 || axis[j]==active)) {
            if((j==0||j==5) && B) continue;
            int id=slot[i-stride[j]];
            if(id<0) continue;
            int from=level-(j==4 ? 1 : (j==3 ? -6 : 0));
            for(int k=-24;k<=24;++k){
                int at=k+from;
                if(at < -24 || at>24 || k+level< -24 || k+level>24) continue;
                if((j==0||j==5) && at!=0) continue;
                if((j==1||j==2) && at!=bridge) continue;
                int prev=profiles[id][k+24];
                if(prev!=absent) value[k+24]=std::max(value[k+24],prev+x*dy[j]-y*dx[j]);
            }
        }
        // A suffix with identity product may be appended in any active factor.
        if(active>=0) for (const Block& sub:neutral) {
            if(((guard+packed-sub.counters)&guard)!=guard) continue;
            if(sub.numberA && B>sub.numberB) continue;
            int pre=slot[i-sub.index]; if(pre<0) continue;
            int post=slot[sub.index];
            for(int k=-24;k<=24;++k){
                int at=k+level-sub.level;
                if(at < -24 || at>24) continue;
                int l=profiles[pre][k+24],r=profiles[post][at+24];
                if(l!=absent && r!=absent) value[k+24]=std::max(value[k+24],l+r+x*sub.y-y*sub.x);
            }
        }
        if(*std::max_element(value.begin(),value.end())!=absent) {
            slot[i]=profiles.size();profiles.push_back(value);
            if(active==-1) neutral.push_back({i,x,y,A,B,level,packed});
        }
    }
    std::cout<<(slot.back()<0 ? absent : profiles[slot.back()][24])<<"\n";
}
