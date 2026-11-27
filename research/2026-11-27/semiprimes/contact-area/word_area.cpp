// Maximum doubled axial area for a closed word in a single projected free product.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <tuple>
#include <utility>
#include <vector>

using Point = std::tuple<int,int,int>;
using Area = std::int64_t;
using Scores = std::map<Point,Area>;

void append(Scores& out, const Scores& prefix, const Scores& suffix) {
    for (const auto& [p,s] : prefix) for (const auto& [q,t] : suffix) {
        const auto [x,y,l] = p;
        const auto [u,v,h] = q;
        Point endpoint{x+u,y+v,l+h};
        Area score = s+t+Area(x)*v-Area(y)*u;
        auto [i,added] = out.try_emplace(endpoint,score);
        if (!added && score > i->second) i->second = score;
    }
}

int main(int argc,char** argv) {
    if (argc!=7) return 1;
    int a=std::atoi(argv[1]), b=std::atoi(argv[2]), c=std::atoi(argv[3]);
    int modulus=std::atoi(argv[4]), limit=std::atoi(argv[5]);
    bool saturated=std::atoi(argv[6])!=0;
    if (modulus!=a && modulus!=b) return 1;
    std::array<std::pair<int,int>,6> units{{{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}};
    std::array<Scores,3> letters;
    for (int j=0;j<6;++j) {
        auto [x,y]=units[j];
        auto [u,v]=units[(j+5)%6];
        if (!saturated || j%2==1) letters[j%3][{c*x,c*y,0}]=0;
        int axis=modulus==a ? (j+5)%3 : j%3;
        if (!saturated || j%2==0) letters[axis][{a*x+b*u,a*y+b*v,saturated ? 1 : 0}]=0;
    }
    std::vector<std::array<Scores,3>> factor(limit+1);
    std::vector<Scores> neutral(limit+1);
    neutral[0][{0,0,0}]=0;
    for (auto& f:factor[0]) f=neutral[0];
    for (int n=1;n<=limit;++n) {
        for (int k=0;k<3;++k) {
            Scores& f=factor[n][k];
            append(f,factor[n-1][k],letters[k]);
            for (int i=1;i<n;++i) append(f,factor[n-i][k],neutral[i]);
            for (const auto& [p,score]:f) {
                if (std::get<0>(p)%modulus || std::get<1>(p)%modulus) continue;
                auto [it,added]=neutral[n].try_emplace(p,score);
                if (!added) it->second=std::max(it->second,score);
            }
        }
        for (auto& f:factor[n]) {
            for (const auto& [p,score]:neutral[n]) {
                auto [it,added]=f.try_emplace(p,score);
                if (!added) it->second=std::max(it->second,score);
            }
        }
        for (int low=0;low<=(saturated ? n : 0);++low) {
            Point origin{0,0,low};
            if (auto i=neutral[n].find(origin); i!=neutral[n].end()) {
                std::cout<<n<<" "<<low<<" "<<i->second<<"\n";
                neutral[n].erase(i);
            }
            for (auto& f:factor[n]) f.erase(origin);
        }
    }
}
