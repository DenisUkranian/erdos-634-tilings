#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using U64=std::uint64_t;
struct Point {
    int x,y;
    Point operator+(Point v) const { return {x+v.x,y+v.y}; }
    Point operator*(int scale) const { return {scale*x,scale*y}; }
    int det(Point v)const{return x*v.y-y*v.x;}
};
constexpr Point unit[]={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}};
int a,b,c,r;
U64 weight[6], area_weight;
int opposite(int k){return k/6*6+(k+3)%6;}
U64 mix(U64 v){
    v+=0x9e3779b97f4a7c15ULL;
    v=(v^(v>>30))*0xbf58476d1ce4e5b9ULL;
    v=(v^(v>>27))*0x94d049bb133111ebULL;
    return v^(v>>31);
}
struct Move {Point first, second, displacement;int i,j;U64 charge;};
Move moves[2][12];
struct Item {U64 key, word;};
std::vector<Item> left;
std::vector<U64> bloom;
std::array<U64,3> matches{};
U64 lookup[2][3][50][50];
int positive_mod(int x,int m){int v=x%m;return v<0?v+m:v;}
U64 potential(int j,Point p){
    return lookup[0][j][positive_mod(p.x,a)][positive_mod(p.y,a)]
         + lookup[1][j][positive_mod(p.x,b)][positive_mod(p.y,b)];
}
U64 increment(const Move &m,Point p,Point q){
    Point mid=p+m.first;
    U64 boundary=potential(m.i,mid)-potential(m.i,p);
    if(m.j>=0)boundary+=potential(m.j,q)-potential(m.j,mid);
    int twice_area=p.det(m.displacement);
    assert(twice_area%c==0);
    return m.charge+boundary+area_weight*U64(twice_area/c);
}
void walk(bool back,int length,Point p,U64 key,U64 code,int last){
    if(length==r){
        if(!back){left.push_back({key,code});return;}
        for(unsigned k=1;k<matches.size();++k){
            U64 wanted=key+area_weight*U64(2*a*b*k);
            U64 bucket=mix(wanted);
            if(!(bloom[(bucket>>6)%bloom.size()] & (U64(1)<<(bucket&63))))continue;
            auto it=std::lower_bound(left.begin(),left.end(),wanted,[](Item v,U64 value){return v.key<value;});
            for(;it!=left.end() && it->key==wanted;++it){
                if((it->word%12)==(code%12))continue; // immediate retrace at midpoint
                ++matches[k];
                std::cout<<k<<" "<<it->word<<" "<<code<<"\n";
            }
        }
        return;
    }
    int begin=(length==0 && back)?6:0;
    int end=(length==0 && !back)?1:12;
    for(int t=begin;t<end;++t){
        if(last>=0 && t==opposite(last))continue;
        const Move &m=moves[back][t];Point q=p+m.displacement;
        walk(back,length+1,q,key+increment(m,p,q),12*code+t,t);
    }
}
int main(int argc,char** argv){
    assert(argc==5);a=std::atoi(argv[1]);b=std::atoi(argv[2]);c=std::atoi(argv[3]);r=std::atoi(argv[4]);
    assert(a<50 && b<50 && c*c==a*a+a*b+b*b && 1<=r && r<=8);
    for(int i=0;i<6;i++)weight[i]=mix(1+i);
    area_weight=mix(7);
    for(int which=0;which<2;which++)for(int j=0;j<3;j++)for(int x=0;x<50;x++)for(int y=0;y<50;y++)
        lookup[which][j][x][y]=mix(100+((3*which+j)*50+x)*50+y);
    for(int rev=0;rev<2;rev++)for(int t=0;t<12;t++){
        int j=t%6,k=(j+5)%6;auto &m=moves[rev][t];
        m.charge=weight[3*(t/6)+j%3]*(j<3?U64(1):U64(-1));
        if(t>=6){m.first=unit[j]*c;m.second={0,0};m.i=j%3;m.j=-1;}
        else{m.first=unit[j]*a;m.second=unit[k]*b;m.i=j%3;m.j=k%3;
             if(rev){std::swap(m.first,m.second);std::swap(m.i,m.j);}}
        m.displacement=m.first+m.second;
    }
    std::size_t count=1;for(int j=1;j<r;j++)count*=11;
    left.reserve(count);walk(false,0,{0,0},0,0,-1);
    assert(left.size()==count);
    std::sort(left.begin(),left.end(),[](Item u,Item v){return u.key<v.key;});
    bloom.resize(count/2+1);
    for(auto v:left){U64 h=mix(v.key);bloom[(h>>6)%bloom.size()]|=U64(1)<<(h&63);}
    walk(true,0,{0,0},0,0,-1);
    std::cerr<<c<<" length "<<2*r<<" left "<<count<<" matches "<<matches[1]<<" "<<matches[2]<<"\n";
}
