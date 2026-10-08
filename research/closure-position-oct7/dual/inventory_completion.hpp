#pragma once
#include <array>
#include <algorithm>
#include <cstdlib>

// Necessary completion test for the canonical (91,91,154)/(8,7,13) problem.
// Index groups by h+11, h=-11,...,11. Four entries are U+,U-,V+,V-.
// For CCW gamma anchored (0,x*rho^j*z^h,y*rho^(j+2)*z^h):
// (x,y)=(7,8) contributes U with sign -(-1)^j;
// (x,y)=(8,7) contributes V with sign  (+1)*(-1)^j.
// Relies on independently proved contiguous support and 3<=K<=8.
// true means FORMAL COMPLETION ONLY, not geometric feasibility.
namespace erdos154_inventory {
using Groups = std::array<std::array<int,4>,23>;
constexpr int INF=10000, M=13, WIDTH=27;

inline int cost(int h,int p,int w,int q,const std::array<int,4>& g) {
    const int u=(h==0?-8:0)+w-13*q;
    const int v=(h==0?-7:(h==1?-13:0))-w+13*p;
    const int s=g[0]+g[1]+std::abs(u-g[0]+g[1])
               +g[2]+g[3]+std::abs(v-g[2]+g[3]);
    int n=h==0?11+13*std::max(0,(s-11+12)/13)
              :13*std::max(1,(s+12)/13);
    if ((n-u-v)%2) n+=13;
    return n;
}

inline bool band_completion(const Groups& groups,int lo,int hi) {
    using Layer=std::array<int,WIDTH*WIDTH>;
    Layer current,following;current.fill(INF);
    current[M*WIDTH+M]=0;
    for(int h=lo;h<=hi;++h) {
        following.fill(INF);
        for(int p=-M;p<=M;++p) for(int w=-M;w<=M;++w) {
            const int old=current[(p+M)*WIDTH+w+M];
            if(old>154 || (h==hi && w!=(hi==0?1:0)))continue;
            const int qlo=h==hi?0:-M, qhi=h==hi?0:M;
            for(int q=qlo;q<=qhi;++q) {
                const int value=old+cost(h,p,w,q,groups[h+11]);
                if(value>154)continue;
                int& best=following[(w+M)*WIDTH+q+M];
                if(value<best)best=value;
            }
        }
        current=following;
    }
    return *std::min_element(current.begin(),current.end())<=154;
}

inline bool completion(const Groups& groups) {
    int lo=0,hi=0,total=0;
    for(int i=0;i<23;++i) {
        int n=0;
        for(int g:groups[i]){if(g<0)return false;n+=g;}
        if(n){lo=std::min(lo,i-11);hi=std::max(hi,i-11);}
        total+=n;
    }
    if(total>154 || hi-lo>7)return false;
    for(int k=std::max(3,hi-lo+1);k<=8;++k) {
        const int first=std::max(1-k,hi-k+1),last=std::min(0,lo);
        for(int left=first;left<=last;++left)
            if(band_completion(groups,left,left+k-1))return true;
    }
    return false;
}
} // namespace erdos154_inventory
