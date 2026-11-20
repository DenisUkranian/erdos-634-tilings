// Exact finite charge-profile filter. It does not solve geometric tiling.
// Input: c,d,capacity,maxPositive,maxNegative,numberOfCuts,maxSolutions;
// then for each cut: D and c upward and c downward integer weights.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <limits>
#include <vector>

using I = std::int64_t;
struct Cut { I D; std::vector<I> up,down; };
struct Current { int r; I q; };
int c,d,cap,maxP,maxM,cutCount,maxSolutions;
std::vector<Cut> cuts;
std::vector<int> positives;
std::vector<std::vector<int>> positiveSets;
I visited=0,reservePassed=0,cutPassed=0;
std::vector<I> rejected;
bool stop=false;
I bestNumerator=std::numeric_limits<I>::max(),bestDenominator=1;
int bestUp=0,bestDown=0,bestNegative=-1;
std::vector<int> bestPositives;
std::ofstream poolOutput;

void output_profile(int u,int v,const std::vector<int>& pos,int neg) {
    std::cout<<"{\"native_up\":"<<u<<",\"native_down\":"<<v<<",\"remote_positive_indices\":[";
    for(std::size_t i=0;i<pos.size();i++){if(i)std::cout<<',';std::cout<<pos[i];}
    std::cout<<"],\"remote_negative_index\":"<<neg<<"}"<<std::endl;
}

I max_correlation(const std::vector<I>& weights,const std::vector<Current>& current) {
    I best=std::numeric_limits<I>::min();
    for (int shift=0;shift<c;shift++) {
        I value=0;
        for (auto e:current) value+=e.q*weights[(e.r+shift)%c];
        best=std::max(best,value);
    }
    return best;
}

void examine(int neg) {
    if(stop)return;
    int P=static_cast<int>(positives.size()), M=neg>=0;
    int total=P-M;
    // These are exactly the bounds -c <= Q_up(0) <= capacity.
    for(int u=-2*c;u<=2*c;u++) {
        int q0=2*c+d*u;
        if(q0 < -c || q0 > cap)continue;
        int v=-u-total, q1=-c+d*v;
        if(q1 < -c || q1 > cap)continue;
        visited++;
        if(std::max(q0,0)+std::max(q1,0)+d*P>2*c)continue;
        if(std::max(-q0,0)+std::max(-q1,0)+d*M>c)continue;
        reservePassed++;
        std::vector<Current> up{{0,q0}},down{{0,q1}};
        auto insert=[&](int index,int charge){
            auto &a=index<c-1 ? up:down;
            int r=index%(c-1)+1;
            for(auto &entry:a) if(entry.r==r){entry.q+=d*charge;return;}
            a.push_back({r,d*charge});
        };
        for(int index:positives)insert(index,1);
        if(neg>=0)insert(neg,-1);
        bool pass=true;
        I lowerN=std::numeric_limits<I>::min()/2,lowerD=1;
        for(int k=0;k<cutCount;k++) {
            I score=max_correlation(cuts[k].up,up)+max_correlation(cuts[k].down,down);
            if(score>cuts[k].D*3*c) {
                rejected[k]++;pass=false;break;
            }
            if((__int128)score*lowerD>(__int128)lowerN*cuts[k].D){lowerN=score;lowerD=cuts[k].D;}
        }
        if(!pass)continue;
        cutPassed++;
        if(poolOutput) {
            poolOutput<<u<<' '<<v;
            for(int k=0;k<maxP;k++)poolOutput<<' '<<(k<(int)positives.size()?positives[k]:-1);
            poolOutput<<' '<<neg<<'\n';
        }
        if(maxSolutions>0) {
            output_profile(u,v,positives,neg);
            if(cutPassed>=maxSolutions){stop=true;return;}
        } else if((__int128)lowerN*bestDenominator<(__int128)bestNumerator*lowerD) {
            bestNumerator=lowerN;bestDenominator=lowerD;
            bestUp=u;bestDown=v;bestPositives=positives;bestNegative=neg;
        }
    }
}

void populate(int count,int start) {
    if(stop)return;
    if(count==0) {
        examine(-1);
        if(maxM>0)for(int n=0;n<2*(c-1)&&!stop;n++) {
            if(std::find(positives.begin(),positives.end(),n)==positives.end())examine(n);
        }
        return;
    }
    for(int index=start;index<2*(c-1)&&!stop;index++) {
        int copies=static_cast<int>(std::count(positives.begin(),positives.end(),index));
        if((copies+1)*d>cap)continue;
        positives.push_back(index);populate(count-1,index);positives.pop_back();
    }
}

int main(int argc,char **argv) {
    if(!(std::cin>>c>>d>>cap>>maxP>>maxM>>cutCount>>maxSolutions))return 2;
    if(maxM!=1 || c<=0 || d<=0 || maxP!=2*c/d)return 3;
    cuts.resize(cutCount);rejected.assign(cutCount,0);
    for(auto &cut:cuts){std::cin>>cut.D;cut.up.resize(c);cut.down.resize(c);for(auto &x:cut.up)std::cin>>x;for(auto &x:cut.down)std::cin>>x;}
    if(!std::cin)return 4;
    if(argc>1){poolOutput.open(argv[1]);if(!poolOutput)return 5;}
    auto start=std::chrono::steady_clock::now();
    for(int p=0;p<=maxP&&!stop;p++)populate(p,0);
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    if(maxSolutions<=0 && cutPassed>0)output_profile(bestUp,bestDown,bestPositives,bestNegative);
    std::cout<<"{\"summary\":true,\"exhaustive\":"<<(stop?"false":"true")<<",\"visited\":"<<visited
        <<",\"reserve_passed\":"<<reservePassed<<",\"cut_passed\":"<<cutPassed<<",\"seconds\":"<<seconds<<",\"rejected\":[";
    for(std::size_t i=0;i<rejected.size();i++){if(i)std::cout<<',';std::cout<<rejected[i];}
    std::cout<<"]}"<<std::endl;
}
