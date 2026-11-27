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
constexpr int field=FIELD_SIZE;
using Profile=std::array<int,field>;
struct Block { int index,x,y,slope; Packed counters; };
void merge(Profile& dst,const Profile& left,const Profile& right,int slope,int area) {
    for(int i=0;i<field;++i) if(left[i]!=absent) {
        for(int j=0;j<field;++j) if(right[j]!=absent) {
            int out=(i+slope*j)%field;
            dst[out]=std::max(dst[out],left[i]+right[j]+area);
        }
    }
}

int main(int argc,char** argv) {
    if (argc!=14 && argc!=15) return 1;
    int last=argc==15 ? std::atoi(argv[14]) : -1;
    if(last< -1 || last>=6) return 1;
    int a=std::atoi(argv[1]),b=std::atoi(argv[2]),c=std::atoi(argv[3]),q=std::atoi(argv[4]);
    int r=q==a ? b : a;
    int generator=2;
    for(;generator<field;++generator) {
        int t=1; for(int i=0;i<r;++i) t=t*generator%field;
        if(t==1) break;
    }
    if(generator==field) return 1;
    Counts slopes{},intercepts{};
    std::array<int,3> exps{1,std::atoi(argv[11]),std::atoi(argv[12])};
    std::array<int,3> centers{0,1,std::atoi(argv[13])};
    auto power_mod=[](int v,int n) {
        int y=1;
        for(int i=0;i<n;++i) y=y*v%field;
        return y;
    };
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
        int other=low && r==a ? k : j;
        int e=(other<3 ? 1 : -1)*(low ? (r==a ? b:a) : c)*exps[other%3];
        slopes[j]=power_mod(generator,(e%r+r)%r);
        intercepts[j]=(((1-slopes[j])*centers[other%3])%field+field)%field;
        axis[j]=h%3;
        power[j]=(h<3 ? 1 : -1)*(low ? (q==a ? b:a) : c);
    }
    std::vector<int> ids(states,-1);
    std::vector<Profile> profiles;
    Profile empty; empty.fill(absent); empty[0]=0;
    profiles.push_back(empty); ids[0]=0;
    std::array<std::array<int,32>,6> powers;
    for(int j=0;j<6;++j) for(int i=0;i<32;++i) powers[j][i]=power_mod(slopes[j],i);
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
        Profile value; value.fill(absent);
        int slope=1;
        for(int j=0;j<6;++j) slope=slope*powers[j][used[j]]%field;
        for(int j=0;j<6;++j) if(used[j] && (active<0 || axis[j]==active)) {
            int prev=ids[i-stride[j]];
            if(prev<0) continue;
            int lead=slope*power_mod(slopes[j],field-2)%field;
            const auto& pre=profiles[prev];
            for(int z=0;z<field;++z) if(pre[z]!=absent) {
                int w=(z+lead*intercepts[j])%field;
                value[w]=std::max(value[w],pre[z]+x*dy[j]-y*dx[j]);
            }
        }
        if(active>=0) for (const Block& sub:neutral) {
            if(((guard+packed-sub.counters)&guard)!=guard) continue;
            int prev=ids[i-sub.index];
            if(prev>=0) merge(value,profiles[prev],profiles[ids[sub.index]],
                              slope*sub.slope%field,x*sub.y-y*sub.x);
        }
        if(*std::max_element(value.begin(),value.end())!=absent) {
            ids[i]=profiles.size(); profiles.push_back(value);
            if(active==-1) neutral.push_back({i,x,y,power_mod(slope,field-2),packed});
        }
    }
    std::cout<<(ids.back()<0 ? absent : profiles[ids.back()][last<0 ? 0 : intercepts[last]])<<"\n";
}
